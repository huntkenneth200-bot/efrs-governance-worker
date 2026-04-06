"""
FORMATION INTELLIGENCE PLATFORM — GOVERNANCE LAYER
Governance Adjudication Engine

Receives governance violation signals and contract breach reports from any cluster
or IC pathway and renders a formal adjudication verdict. Operates as the judicial
arm of the Governance Layer — all enforcement decisions flow through this engine
before being forwarded to the CouncilOfMetanoia (governance layer) for directive issuance.

Adjudication verdicts:
  Compliant            — No violation. Signal logged and cleared.
  Warning              — Minor deviation. Notification issued to cluster.
  Remediation-Required — Substantive breach. Cluster must remediate within window.
  Suspension           — Severe breach. Cluster operations suspended pending review.
  Disqualification     — Unresolvable theological or constitutional violation.
                         Permanent. Requires full Council ruling to reverse.

Authority: DOC-01.1, DOC-01.2, GC-01 through GC-07
Version: 1.0
Status: TRUSTED — Cleared for Governance Layer Integration
"""

from __future__ import annotations
import uuid
import datetime
from typing import TYPE_CHECKING, Optional, List, Dict, Any, Callable

if TYPE_CHECKING:
    from config import PlatformConfig
    from logs.platform_logger import PlatformLogger

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VIOLATION_TYPES = ("Constitutional", "Contractual", "Theological", "Operational")

VERDICTS = (
    "Compliant",
    "Warning",
    "Remediation-Required",
    "Suspension",
    "Disqualification",
)

ADJUDICATION_STATUSES = (
    "Queued",
    "Under-Review",
    "Verdict-Rendered",
    "Escalated",
    "Remediation-Open",
    "Closed",
)

REMEDIATION_STATUSES = ("Open", "Submitted", "Resolved", "Escalated", "Expired")

# Drift magnitude thresholds that trigger adjudication intake
_DRIFT_WARNING_THRESHOLD = 0.65       # matches DriftDetectionService.ALERT_THRESHOLD
_DRIFT_REMEDIATION_THRESHOLD = 0.85   # matches DriftDetectionService.CRITICAL_THRESHOLD

# Default remediation window length in days per violation type
_DEFAULT_REMEDIATION_DAYS: Dict[str, int] = {
    "Constitutional": 7,
    "Contractual":    14,
    "Theological":    7,
    "Operational":    21,
}

# Baseline verdict map: (violation_type, breach_severity) → verdict
# breach_severity mirrors GC contract severity levels: MINOR / MAJOR / CRITICAL
_VERDICT_MATRIX: Dict[tuple, str] = {
    ("Constitutional", "MINOR"):    "Warning",
    ("Constitutional", "MAJOR"):    "Remediation-Required",
    ("Constitutional", "CRITICAL"): "Suspension",
    ("Contractual",    "MINOR"):    "Warning",
    ("Contractual",    "MAJOR"):    "Remediation-Required",
    ("Contractual",    "CRITICAL"): "Suspension",
    ("Theological",    "MINOR"):    "Remediation-Required",
    ("Theological",    "MAJOR"):    "Suspension",
    ("Theological",    "CRITICAL"): "Disqualification",
    ("Operational",    "MINOR"):    "Warning",
    ("Operational",    "MAJOR"):    "Warning",
    ("Operational",    "CRITICAL"): "Remediation-Required",
}


class GovernanceAdjudicationEngine:
    """
    Judicial processing engine for governance contract violations and
    constitutional compliance failures.

    All state is in-memory; TODO annotations mark persistence integration points.
    Cross-service references (council, routing_table) are injected after init
    via set_council() / set_routing_table() to avoid circular dependencies.

    STATUS: TRUSTED — Cleared for Governance Layer Integration
    """

    def __init__(self, config: "PlatformConfig", logger: "PlatformLogger"):
        self.config = config
        self.logger = logger
        # adjudication_id (str) → adjudication record dict
        self._adjudication_log: Dict[str, Dict[str, Any]] = {}
        # remediation_id (str) → remediation record dict
        self._remediation_log: Dict[str, Dict[str, Any]] = {}
        # Injected cross-service references (set after init by GovernanceLayer)
        self._council = None
        self._routing_table = None
        # TODO (STEP 15C+): Load active adjudication queue from governance state store.
        # TODO (STEP 15C+): Load precedent index from AmendmentRulingRegistry (CLU-02.4).

    # ------------------------------------------------------------------
    # Dependency injection
    # ------------------------------------------------------------------

    def set_council(self, council) -> None:
        """Inject CouncilOfMetanoia reference. Called by GovernanceLayer after init."""
        self._council = council

    def set_routing_table(self, routing_table) -> None:
        """Inject GovernanceRoutingTable reference. Called by GovernanceLayer after init."""
        self._routing_table = routing_table

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _now(self) -> str:
        return datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="milliseconds").replace("+00:00", "Z")

    def _new_adjudication_record(self, cluster_id: str, contract_id: str,
                                  violation_type: str, violation_ref: uuid.UUID,
                                  evidence_refs: List[uuid.UUID]) -> Dict[str, Any]:
        adjudication_id = uuid.uuid4()
        return {
            "adjudication_id":       str(adjudication_id),
            "cluster_id":            cluster_id,
            "contract_id":           contract_id,
            "violation_type":        violation_type,
            "violation_ref":         str(violation_ref),
            "evidence_refs":         [str(r) for r in evidence_refs],
            "status":                "Queued",
            "created_at":            self._now(),
            "reviewing_authority_id": None,
            "verdict":               None,
            "rationale":             None,
            "scriptural_basis":      None,
            "directive_text":        None,
            "verdict_at":            None,
            "escalated_at":          None,
            "escalation_reason":     None,
            "remediation_id":        None,
            "history":               [],
        }

    # ------------------------------------------------------------------
    # Violation intake
    # ------------------------------------------------------------------

    def receive_violation_signal(self, cluster_id: str, contract_id: str,
                                  violation_type: str, violation_ref: uuid.UUID,
                                  evidence_refs: List[uuid.UUID]) -> uuid.UUID:
        """
        Receive a governance violation signal from a cluster or ICBus monitor.
        Creates an adjudication record and queues it for verdict processing.
        violation_type: Constitutional / Contractual / Theological / Operational.
        Returns adjudication_id.
        """
        if violation_type not in VIOLATION_TYPES:
            self.logger.log(
                f"GovernanceAdjudicationEngine.receive_violation_signal REJECTED | "
                f"invalid violation_type={violation_type} | cluster={cluster_id}"
            )
            # Return a sentinel UUID so callers always get a UUID back
            return uuid.UUID(int=0)

        record = self._new_adjudication_record(
            cluster_id, contract_id, violation_type, violation_ref, evidence_refs
        )
        adjudication_id = uuid.UUID(record["adjudication_id"])
        self._adjudication_log[str(adjudication_id)] = record

        self.logger.log(
            f"GovernanceAdjudicationEngine violation received | "
            f"adjudication_id={adjudication_id} | cluster={cluster_id} | "
            f"contract={contract_id} | type={violation_type}"
        )
        # TODO (STEP 15C+): Persist adjudication record; notify governance dashboard.
        return adjudication_id

    def receive_drift_alert(self, drift_report_id: uuid.UUID, cluster_id: str,
                             drift_type: str, drift_magnitude: float) -> Optional[uuid.UUID]:
        """
        Receive a drift alert from DriftDetectionService.
        Drift magnitude >= _DRIFT_REMEDIATION_THRESHOLD → Remediation-Required pathway.
        Drift magnitude >= _DRIFT_WARNING_THRESHOLD      → Warning pathway.
        Below warning threshold → logged and cleared (Compliant).
        Returns adjudication_id if a record was created, else None.
        """
        if drift_magnitude < _DRIFT_WARNING_THRESHOLD:
            self.logger.log(
                f"GovernanceAdjudicationEngine drift_alert BELOW_THRESHOLD | "
                f"drift_report_id={drift_report_id} | cluster={cluster_id} | "
                f"type={drift_type} | magnitude={drift_magnitude:.3f}"
            )
            return None

        # Map drift_type to violation_type
        theological_drift_types = {"Theological"}
        violation_type = (
            "Theological" if drift_type in theological_drift_types else "Operational"
        )

        adjudication_id = self.receive_violation_signal(
            cluster_id=cluster_id,
            contract_id="DRIFT-AUTO",
            violation_type=violation_type,
            violation_ref=drift_report_id,
            evidence_refs=[drift_report_id],
        )

        # Immediately set preliminary severity based on magnitude
        record = self._adjudication_log.get(str(adjudication_id))
        if record:
            if drift_magnitude >= _DRIFT_REMEDIATION_THRESHOLD:
                severity = "MAJOR"
            else:
                severity = "MINOR"
            record["_drift_preliminary_severity"] = severity
            record["history"].append({
                "event":     "drift_intake",
                "drift_type": drift_type,
                "magnitude":  drift_magnitude,
                "severity":   severity,
                "at":         self._now(),
            })

        self.logger.log(
            f"GovernanceAdjudicationEngine drift_alert QUEUED | "
            f"adjudication_id={adjudication_id} | drift_type={drift_type} | "
            f"magnitude={drift_magnitude:.3f}"
        )
        return adjudication_id

    # ------------------------------------------------------------------
    # Adjudication processing
    # ------------------------------------------------------------------

    def evaluate_violation(self, adjudication_id: uuid.UUID,
                            reviewing_authority_id: uuid.UUID) -> Dict[str, Any]:
        """
        Evaluate a queued violation against applicable Governance Contract rules
        and constitutional constraints.
        Applies the _VERDICT_MATRIX heuristic using violation_type + any
        preliminary severity set at intake. Transitions Queued → Under-Review.
        Returns evaluation summary dict.
        """
        record = self._adjudication_log.get(str(adjudication_id))
        if not record:
            self.logger.log(
                f"GovernanceAdjudicationEngine.evaluate_violation NOT FOUND | "
                f"adjudication_id={adjudication_id}"
            )
            return {"found": False, "adjudication_id": str(adjudication_id)}

        if record["status"] not in ("Queued", "Under-Review"):
            self.logger.log(
                f"GovernanceAdjudicationEngine.evaluate_violation INVALID_STATE | "
                f"adjudication_id={adjudication_id} | status={record['status']}"
            )
            return {
                "found":  True,
                "adjudication_id": str(adjudication_id),
                "status": record["status"],
                "error":  "Cannot evaluate — not in Queued/Under-Review state",
            }

        record["status"] = "Under-Review"
        record["reviewing_authority_id"] = str(reviewing_authority_id)
        record["history"].append({
            "event":                  "evaluation-started",
            "reviewing_authority_id": str(reviewing_authority_id),
            "at":                     self._now(),
        })

        # Derive breach severity from preliminary intake or apply MAJOR default
        violation_type = record["violation_type"]
        preliminary_severity = record.get("_drift_preliminary_severity", "MAJOR")
        preliminary_verdict = _VERDICT_MATRIX.get(
            (violation_type, preliminary_severity), "Warning"
        )

        # Check precedent: prior Suspension or Disqualification on same contract_id
        # escalates minimum verdict level
        prior_records = self.query_precedent(
            record["contract_id"], violation_type
        )
        prior_severe = any(
            r.get("verdict") in ("Suspension", "Disqualification")
            for r in prior_records
            if r.get("adjudication_id") != str(adjudication_id)
        )
        if prior_severe and preliminary_verdict == "Warning":
            preliminary_verdict = "Remediation-Required"

        self.logger.log(
            f"GovernanceAdjudicationEngine.evaluate_violation | "
            f"adjudication_id={adjudication_id} | type={violation_type} | "
            f"preliminary_verdict={preliminary_verdict}"
        )

        # TODO (STEP 15C+): Load full GC rule set for contract_id; apply rule engine.
        return {
            "found":               True,
            "adjudication_id":     str(adjudication_id),
            "status":              "Under-Review",
            "violation_type":      violation_type,
            "preliminary_verdict": preliminary_verdict,
            "prior_precedents":    len(prior_records),
        }

    def render_verdict(self, adjudication_id: uuid.UUID, verdict: str,
                        rationale: str, scriptural_basis: str,
                        directive_text: Optional[str] = None) -> Dict[str, Any]:
        """
        Render the final adjudication verdict.
        verdict must be one of: Compliant / Warning / Remediation-Required /
                                 Suspension / Disqualification.
        Disqualification requires Council escalation (VR-02-10).
        Transitions Under-Review → Verdict-Rendered (then Escalated if Disqualification).
        Returns verdict record dict.
        """
        if verdict not in VERDICTS:
            self.logger.log(
                f"GovernanceAdjudicationEngine.render_verdict REJECTED | "
                f"invalid verdict={verdict} | adjudication_id={adjudication_id}"
            )
            return {"success": False, "error": f"Invalid verdict: {verdict}"}

        record = self._adjudication_log.get(str(adjudication_id))
        if not record:
            self.logger.log(
                f"GovernanceAdjudicationEngine.render_verdict NOT FOUND | "
                f"adjudication_id={adjudication_id}"
            )
            return {"success": False, "error": "Adjudication record not found"}

        if record["status"] not in ("Queued", "Under-Review"):
            self.logger.log(
                f"GovernanceAdjudicationEngine.render_verdict INVALID_STATE | "
                f"adjudication_id={adjudication_id} | status={record['status']}"
            )
            return {
                "success": False,
                "error":   f"Cannot render verdict — status is {record['status']}",
            }

        record["verdict"]          = verdict
        record["rationale"]        = rationale
        record["scriptural_basis"] = scriptural_basis
        record["directive_text"]   = directive_text
        record["verdict_at"]       = self._now()
        record["status"]           = "Verdict-Rendered"
        record["history"].append({
            "event":            "verdict-rendered",
            "verdict":          verdict,
            "scriptural_basis": scriptural_basis,
            "at":               self._now(),
        })

        self.logger.log(
            f"GovernanceAdjudicationEngine verdict rendered | "
            f"adjudication_id={adjudication_id} | verdict={verdict} | "
            f"cluster={record['cluster_id']}"
        )

        # Disqualification must be escalated to Council for ratification (VR-02-10)
        if verdict == "Disqualification":
            self.escalate_to_council(
                adjudication_id,
                "Disqualification verdict requires full Council ratification (VR-02-10)"
            )

        # Forward to Council if injected
        if self._council is not None:
            self._council.receive_adjudication_result(
                adjudication_id=adjudication_id,
                verdict=verdict,
                directive_text=directive_text or "",
            )

        # Route verdict via routing table if injected
        if self._routing_table is not None:
            self._routing_table.route_verdict(
                adjudication_id=adjudication_id,
                cluster_id=record["cluster_id"],
                verdict=verdict,
                directive_text=directive_text,
            )

        # TODO (STEP 15C+): Persist verdict; emit IC-08 directive if required.
        return {
            "success":         True,
            "adjudication_id": str(adjudication_id),
            "verdict":         verdict,
            "cluster_id":      record["cluster_id"],
            "verdict_at":      record["verdict_at"],
        }

    def escalate_to_council(self, adjudication_id: uuid.UUID,
                             escalation_reason: str) -> bool:
        """
        Escalate an adjudication to full Council deliberation.
        Required for: Suspension, Disqualification, or theological disputes.
        Transitions current status → Escalated.
        Returns True on success.
        """
        record = self._adjudication_log.get(str(adjudication_id))
        if not record:
            self.logger.log(
                f"GovernanceAdjudicationEngine.escalate_to_council NOT FOUND | "
                f"adjudication_id={adjudication_id}"
            )
            return False

        record["status"]           = "Escalated"
        record["escalated_at"]     = self._now()
        record["escalation_reason"] = escalation_reason
        record["history"].append({
            "event":  "escalated-to-council",
            "reason": escalation_reason,
            "at":     self._now(),
        })

        self.logger.log(
            f"GovernanceAdjudicationEngine escalated to council | "
            f"adjudication_id={adjudication_id} | reason={escalation_reason}"
        )
        # TODO (STEP 15C+): Route adjudication_id to Council governance session agenda.
        return True

    # ------------------------------------------------------------------
    # Remediation tracking
    # ------------------------------------------------------------------

    def open_remediation_window(self, adjudication_id: uuid.UUID,
                                 cluster_id: str,
                                 remediation_days: Optional[int] = None) -> uuid.UUID:
        """
        Open a remediation window after a Remediation-Required verdict.
        Cluster must resolve breach within remediation_days.
        Defaults to _DEFAULT_REMEDIATION_DAYS per violation_type if not specified.
        Transitions Verdict-Rendered → Remediation-Open.
        Returns remediation_id.
        """
        record = self._adjudication_log.get(str(adjudication_id))
        if not record:
            self.logger.log(
                f"GovernanceAdjudicationEngine.open_remediation_window NOT FOUND | "
                f"adjudication_id={adjudication_id}"
            )
            return uuid.UUID(int=0)

        if remediation_days is None:
            vtype = record.get("violation_type", "Operational")
            remediation_days = _DEFAULT_REMEDIATION_DAYS.get(vtype, 14)

        deadline = (
            datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(days=remediation_days)
        ).date().isoformat()

        remediation_id = uuid.uuid4()
        remediation_record = {
            "remediation_id":   str(remediation_id),
            "adjudication_id":  str(adjudication_id),
            "cluster_id":       cluster_id,
            "deadline":         deadline,
            "remediation_days": remediation_days,
            "status":           "Open",
            "opened_at":        self._now(),
            "closed_at":        None,
            "outcome":          None,
            "submission_notes": None,
            "evidence_refs":    [],
            "history":          [],
        }
        self._remediation_log[str(remediation_id)] = remediation_record

        # Update adjudication record
        record["status"]         = "Remediation-Open"
        record["remediation_id"] = str(remediation_id)
        record["history"].append({
            "event":          "remediation-window-opened",
            "remediation_id": str(remediation_id),
            "deadline":       deadline,
            "at":             self._now(),
        })

        self.logger.log(
            f"GovernanceAdjudicationEngine remediation window opened | "
            f"remediation_id={remediation_id} | adjudication_id={adjudication_id} | "
            f"cluster={cluster_id} | deadline={deadline}"
        )
        # TODO (STEP 15C+): Persist remediation record; notify cluster via routing table.
        return remediation_id

    def receive_remediation_submission(self, remediation_id: uuid.UUID,
                                        evidence_refs: List[uuid.UUID],
                                        notes: str) -> bool:
        """
        Receive a cluster's remediation submission for review.
        Transitions Open → Submitted.
        Returns True on success.
        """
        record = self._remediation_log.get(str(remediation_id))
        if not record:
            self.logger.log(
                f"GovernanceAdjudicationEngine.receive_remediation_submission NOT FOUND | "
                f"remediation_id={remediation_id}"
            )
            return False

        if record["status"] != "Open":
            self.logger.log(
                f"GovernanceAdjudicationEngine.receive_remediation_submission INVALID_STATE | "
                f"remediation_id={remediation_id} | status={record['status']}"
            )
            return False

        record["status"]           = "Submitted"
        record["evidence_refs"]    = [str(r) for r in evidence_refs]
        record["submission_notes"] = notes
        record["history"].append({
            "event":       "submission-received",
            "notes":       notes,
            "evidence_ct": len(evidence_refs),
            "at":          self._now(),
        })

        self.logger.log(
            f"GovernanceAdjudicationEngine remediation submission received | "
            f"remediation_id={remediation_id} | evidence_count={len(evidence_refs)}"
        )
        # TODO (STEP 15C+): Trigger re-evaluation of original adjudication_id.
        return True

    def close_remediation(self, remediation_id: uuid.UUID, outcome: str) -> bool:
        """
        Close a remediation window with outcome: Resolved / Escalated / Expired.
        If Expired: automatically escalate adjudication to Suspension review.
        Returns True on success.
        """
        valid_outcomes = ("Resolved", "Escalated", "Expired")
        if outcome not in valid_outcomes:
            self.logger.log(
                f"GovernanceAdjudicationEngine.close_remediation REJECTED | "
                f"invalid outcome={outcome}"
            )
            return False

        record = self._remediation_log.get(str(remediation_id))
        if not record:
            self.logger.log(
                f"GovernanceAdjudicationEngine.close_remediation NOT FOUND | "
                f"remediation_id={remediation_id}"
            )
            return False

        if record["status"] not in ("Open", "Submitted"):
            self.logger.log(
                f"GovernanceAdjudicationEngine.close_remediation INVALID_STATE | "
                f"remediation_id={remediation_id} | status={record['status']}"
            )
            return False

        record["status"]    = outcome
        record["outcome"]   = outcome
        record["closed_at"] = self._now()
        record["history"].append({
            "event":   "remediation-closed",
            "outcome": outcome,
            "at":      self._now(),
        })

        self.logger.log(
            f"GovernanceAdjudicationEngine remediation closed | "
            f"remediation_id={remediation_id} | outcome={outcome}"
        )

        # Expired remediation → auto-escalate the parent adjudication to Suspension
        if outcome == "Expired":
            parent_adj_id_str = record.get("adjudication_id")
            if parent_adj_id_str:
                parent_adj_id = uuid.UUID(parent_adj_id_str)
                self.escalate_to_council(
                    parent_adj_id,
                    f"Remediation window expired without resolution "
                    f"(remediation_id={remediation_id})"
                )

        # TODO (STEP 15C+): Persist closure; route outcome to CouncilOfMetanoia.
        return True

    # ------------------------------------------------------------------
    # Precedent and audit
    # ------------------------------------------------------------------

    def query_precedent(self, contract_id: str,
                         violation_type: str) -> List[Dict[str, Any]]:
        """
        Query historical adjudication records for precedent on a contract / violation type.
        Returns all verdict-rendered records for the contract_id / violation_type pair,
        ordered by verdict_at ascending (oldest first — foundational precedent leads).
        """
        results = []
        for record in self._adjudication_log.values():
            if record.get("contract_id") != contract_id:
                continue
            if record.get("violation_type") != violation_type:
                continue
            if record.get("verdict") is None:
                continue
            results.append(dict(record))

        # Sort by verdict_at ascending (ISO strings sort correctly)
        results.sort(key=lambda r: r.get("verdict_at") or "")
        return results

    def get_adjudication_record(self,
                                 adjudication_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """
        Retrieve a full adjudication record including evidence, verdict, and rationale.
        Returns None if not found.
        """
        record = self._adjudication_log.get(str(adjudication_id))
        return dict(record) if record else None

    def get_active_adjudications(self,
                                   cluster_id: Optional[str] = None
                                  ) -> List[Dict[str, Any]]:
        """
        Return all adjudications not yet in a terminal state (Closed).
        Optionally filter by cluster_id.
        """
        terminal = {"Closed"}
        results = []
        for record in self._adjudication_log.values():
            if record["status"] in terminal:
                continue
            if cluster_id and record["cluster_id"] != cluster_id:
                continue
            results.append(dict(record))
        return results
