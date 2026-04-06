"""
FORMATION INTELLIGENCE PLATFORM — GOVERNANCE LAYER
Governance Council — CouncilOfMetanoia (Governance Layer Representation)

This is the governance-layer authority controller for the Council of Metanoia.
It is distinct from CLU-02 (CouncilOfMetanoia cluster), which handles operational
submodules (theological review, ruling registry, etc.). This class operates at the
governance abstraction layer and is responsible for:

  — Enforcing constitutional constraints across all six operational clusters
  — Receiving adjudicated governance decisions from GovernanceAdjudicationEngine
  — Issuing governance directives into the platform via IC-08
  — Maintaining the governance session lifecycle (quorum, deliberation, closure)
  — Serving as the root authority anchor for all Governance Contracts (GC-01–GC-07)

Relationship to CLU-02:
  CLU-02 is the operational cluster containing the Council's submodules.
  This class is the governance layer's representation of Council authority —
  it delegates operational execution to CLU-02 but owns the constitutional
  enforcement boundary.

Authority: DOC-01.1 (Platform Governing Charter), DOC-01.2 (Constitutional Bylaws)
Version: 1.0
Status: TRUSTED — Cleared for Governance Layer Integration
"""

from __future__ import annotations
import uuid
import datetime
import re
from typing import TYPE_CHECKING, Optional, List, Dict, Any

if TYPE_CHECKING:
    from config import PlatformConfig
    from logs.platform_logger import PlatformLogger

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SESSION_STATUSES = ("Open", "Closed", "Suspended")

# Verdicts that mandate a pending directive emission via IC-08
_DIRECTIVE_VERDICTS = {"Warning", "Remediation-Required", "Suspension", "Disqualification"}

# Verdicts that require escalation to a formal governance session
_ESCALATION_VERDICTS = {"Suspension", "Disqualification"}

# Minimum quorum for a governance session to issue rulings (DOC-01.2 Article III)
_DEFAULT_QUORUM = 3

# GC-XX contract ID validation pattern
_CONTRACT_ID_PATTERN = re.compile(r"^GC-\d{2}$")


class CouncilOfMetanoia:
    """
    Governance-layer authority controller for the Council of Metanoia.

    Instantiated by the GovernanceLayer controller. Holds constitutional
    authority over all governance contracts and adjudication decisions.

    All state is in-memory; TODO annotations mark persistence integration points.
    Cross-service references (adjudication_engine, routing_table) are injected
    after init via set_adjudication_engine() / set_routing_table() to avoid
    circular dependencies.

    STATUS: TRUSTED — Cleared for Governance Layer Integration
    """

    def __init__(self, config: "PlatformConfig", logger: "PlatformLogger"):
        self.config = config
        self.logger = logger
        # session_id (str) → session record dict
        self._sessions: Dict[str, Dict[str, Any]] = {}
        # contract_id (str) → contract instance
        self._contracts: Dict[str, Any] = {}
        # Pending directives awaiting IC-08 emission (wired in STEP 15C)
        self._pending_directives: List[Dict[str, Any]] = []
        # Injected cross-service references (set after init by GovernanceLayer)
        self._adjudication = None
        self._routing_table = None
        # TODO (STEP 15C+): Load active governance sessions from state store.
        # TODO (STEP 15C+): Load registered contracts from GC registry.

    # ------------------------------------------------------------------
    # Dependency injection
    # ------------------------------------------------------------------

    def set_adjudication_engine(self, adjudication) -> None:
        """Inject GovernanceAdjudicationEngine reference. Called by GovernanceLayer."""
        self._adjudication = adjudication

    def set_routing_table(self, routing_table) -> None:
        """Inject GovernanceRoutingTable reference. Called by GovernanceLayer."""
        self._routing_table = routing_table

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _now(self) -> str:
        return datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="milliseconds").replace("+00:00", "Z")

    def _quorum_minimum(self) -> int:
        return getattr(self.config, "COUNCIL_QUORUM_MINIMUM", _DEFAULT_QUORUM)

    # ------------------------------------------------------------------
    # Session lifecycle
    # ------------------------------------------------------------------

    def open_governance_session(self, session_id: uuid.UUID,
                                  agenda_refs: List[uuid.UUID]) -> bool:
        """
        Open a formal governance session for deliberation.
        Sessions require quorum per DOC-01.2 Article III before any ruling is issued.
        Returns True if session opened successfully.
        """
        sid = str(session_id)
        if sid in self._sessions:
            self.logger.log(
                f"CouncilOfMetanoia.open_governance_session DUPLICATE | "
                f"session_id={session_id}"
            )
            return False

        session = {
            "session_id":       sid,
            "status":           "Open",
            "agenda_refs":      [str(r) for r in agenda_refs],
            "opened_at":        self._now(),
            "closed_at":        None,
            "session_notes":    None,
            "rulings_issued":   [],
            "quorum_verified":  False,  # set True when quorum is confirmed at session
            "directives_issued": [],
            "history":          [],
        }
        self._sessions[sid] = session

        self.logger.log(
            f"CouncilOfMetanoia governance session opened | "
            f"session_id={session_id} | agenda_items={len(agenda_refs)} | "
            f"quorum_minimum={self._quorum_minimum()}"
        )
        # TODO (STEP 15C+): Persist session record; notify Council members.
        return True

    def close_governance_session(self, session_id: uuid.UUID,
                                   session_notes: str) -> bool:
        """
        Close an active governance session and record outcomes.
        Returns True if closed successfully.
        """
        sid = str(session_id)
        session = self._sessions.get(sid)
        if not session:
            self.logger.log(
                f"CouncilOfMetanoia.close_governance_session NOT FOUND | "
                f"session_id={session_id}"
            )
            return False

        if session["status"] != "Open":
            self.logger.log(
                f"CouncilOfMetanoia.close_governance_session INVALID_STATE | "
                f"session_id={session_id} | status={session['status']}"
            )
            return False

        session["status"]       = "Closed"
        session["closed_at"]    = self._now()
        session["session_notes"] = session_notes
        session["history"].append({
            "event": "session-closed",
            "notes": session_notes,
            "at":    self._now(),
        })

        self.logger.log(
            f"CouncilOfMetanoia governance session closed | "
            f"session_id={session_id} | "
            f"rulings_issued={len(session['rulings_issued'])}"
        )
        # TODO (STEP 15C+): Persist session closure; emit pending rulings.
        return True

    def get_session_status(self, session_id: uuid.UUID) -> Dict[str, Any]:
        """
        Return the current status of a governance session.
        Returns status dict including quorum state and agenda progress.
        """
        sid = str(session_id)
        session = self._sessions.get(sid)
        if not session:
            self.logger.log(
                f"CouncilOfMetanoia.get_session_status NOT FOUND | "
                f"session_id={session_id}"
            )
            return {"found": False, "session_id": sid}

        return {
            "found":             True,
            "session_id":        sid,
            "status":            session["status"],
            "quorum_verified":   session["quorum_verified"],
            "agenda_item_count": len(session["agenda_refs"]),
            "rulings_issued":    len(session["rulings_issued"]),
            "opened_at":         session["opened_at"],
            "closed_at":         session["closed_at"],
        }

    # ------------------------------------------------------------------
    # Constitutional enforcement
    # ------------------------------------------------------------------

    def assert_constitutional_compliance(self, ruling_id: uuid.UUID) -> bool:
        """
        Verify that a proposed ruling does not contradict Tier 1 documents or Scripture.
        No ruling may contradict Tier 1 or Scripture (VR-02-02).

        Current implementation: validates ruling_id is non-null and logs.
        Full rule-engine integration deferred to STEP 15C when CLU-02.4
        AmendmentRulingRegistry data is accessible.

        Returns True if no constitutional conflict detected.
        """
        if ruling_id is None or ruling_id == uuid.UUID(int=0):
            self.logger.log(
                f"CouncilOfMetanoia.assert_constitutional_compliance REJECTED | "
                f"null or sentinel ruling_id"
            )
            return False

        self.logger.log(
            f"CouncilOfMetanoia.assert_constitutional_compliance | "
            f"ruling_id={ruling_id} | result=COMPLIANT (rule-engine pending STEP 15C)"
        )
        # TODO (STEP 15C+): Load ruling from CLU-02.4; compare against DOC-01.1 and
        # DOC-01.6 Tier 1 constraints; return False on any contradiction.
        return True

    def enforce_governance_contract(self, contract_id: str, cluster_id: str,
                                     violation_ref: uuid.UUID) -> Dict[str, Any]:
        """
        Enforce a specific Governance Contract (GC-01 through GC-07) against a cluster
        violation. Routes enforcement action to GovernanceAdjudicationEngine.
        Returns enforcement result dict.
        """
        if contract_id not in self._contracts:
            self.logger.log(
                f"CouncilOfMetanoia.enforce_governance_contract CONTRACT_NOT_FOUND | "
                f"contract_id={contract_id} | cluster={cluster_id}"
            )
            return {
                "success":    False,
                "error":      f"Contract {contract_id} is not registered",
                "contract_id": contract_id,
            }

        self.logger.log(
            f"CouncilOfMetanoia enforce contract | contract_id={contract_id} | "
            f"cluster={cluster_id} | violation_ref={violation_ref}"
        )

        adjudication_id = None
        if self._adjudication is not None:
            adjudication_id = self._adjudication.receive_violation_signal(
                cluster_id=cluster_id,
                contract_id=contract_id,
                violation_type="Contractual",
                violation_ref=violation_ref,
                evidence_refs=[violation_ref],
            )

        # TODO (STEP 15C+): Invoke GC contract instance's evaluation logic.
        return {
            "success":         True,
            "contract_id":     contract_id,
            "cluster_id":      cluster_id,
            "violation_ref":   str(violation_ref),
            "adjudication_id": str(adjudication_id) if adjudication_id else None,
        }

    def receive_adjudication_result(self, adjudication_id: uuid.UUID,
                                     verdict: str, directive_text: str) -> None:
        """
        Receive a completed adjudication verdict from GovernanceAdjudicationEngine.
        Queues a directive emission if verdict requires one.
        Verdicts requiring escalation are noted for Council session scheduling.
        """
        self.logger.log(
            f"CouncilOfMetanoia adjudication result received | "
            f"adjudication_id={adjudication_id} | verdict={verdict}"
        )

        if verdict in _DIRECTIVE_VERDICTS and directive_text:
            directive_record = {
                "adjudication_id": str(adjudication_id),
                "verdict":         verdict,
                "directive_text":  directive_text,
                "queued_at":       self._now(),
            }
            self._pending_directives.append(directive_record)
            self.logger.log(
                f"CouncilOfMetanoia directive queued | "
                f"adjudication_id={adjudication_id} | verdict={verdict}"
            )
            # TODO (STEP 15C+): Emit IC-08 directive via CLU-02.1 GoverningAuthorityModule.

        if verdict in _ESCALATION_VERDICTS:
            self.logger.log(
                f"CouncilOfMetanoia SESSION REQUIRED | "
                f"verdict={verdict} requires Council session | "
                f"adjudication_id={adjudication_id}"
            )
            # TODO (STEP 15C+): Schedule governance session if none is open;
            # add adjudication_id to session agenda.

    # ------------------------------------------------------------------
    # Governance contract registry
    # ------------------------------------------------------------------

    def register_contract(self, contract_id: str, contract_instance: Any) -> bool:
        """
        Register a Governance Contract (GC-XX) with the council authority.
        Contracts must be registered before they can be enforced.
        contract_id must match the pattern GC-XX (two-digit numeric suffix).
        Returns True if registered, False if validation fails.
        """
        if not _CONTRACT_ID_PATTERN.match(contract_id):
            self.logger.log(
                f"CouncilOfMetanoia.register_contract REJECTED | "
                f"invalid contract_id format={contract_id} (expected GC-XX)"
            )
            return False

        self._contracts[contract_id] = contract_instance
        self.logger.log(
            f"CouncilOfMetanoia contract registered | contract_id={contract_id}"
        )
        return True

    def get_registered_contracts(self) -> Dict[str, Any]:
        """
        Return the currently registered Governance Contracts.
        Keys are contract_id strings (e.g. "GC-01"); values are contract instances.
        """
        return dict(self._contracts)

    # ------------------------------------------------------------------
    # Directive issuance
    # ------------------------------------------------------------------

    def issue_platform_directive(self, ruling_id: uuid.UUID, directive_text: str,
                                   affected_clusters: List[str],
                                   scriptural_basis: str) -> Dict[str, Any]:
        """
        Issue a platform-wide governance directive under a ratified ruling.
        Constitutional compliance check is performed before issuance.
        Delegates broadcast to GovernanceRoutingTable if injected.
        Returns issuance result dict.
        """
        if not self.assert_constitutional_compliance(ruling_id):
            self.logger.log(
                f"CouncilOfMetanoia.issue_platform_directive BLOCKED | "
                f"constitutional compliance failed | ruling_id={ruling_id}"
            )
            return {
                "success": False,
                "error":   "Constitutional compliance check failed",
                "ruling_id": str(ruling_id),
            }

        self.logger.log(
            f"CouncilOfMetanoia platform directive issued | "
            f"ruling_id={ruling_id} | clusters={affected_clusters} | "
            f"scriptural_basis={scriptural_basis!r}"
        )

        dispatch_results = []
        if self._routing_table is not None:
            dispatch_results = self._routing_table.broadcast_directive(
                ruling_id=ruling_id,
                directive_text=directive_text,
                affected_clusters=affected_clusters,
            )

        # TODO (STEP 15C+): Emit IC-08 via CLU-02.1 GoverningAuthorityModule for
        # each affected cluster; record ruling in CLU-02.4 AmendmentRulingRegistry.
        return {
            "success":          True,
            "ruling_id":        str(ruling_id),
            "directive_text":   directive_text,
            "affected_clusters": affected_clusters,
            "scriptural_basis": scriptural_basis,
            "dispatched":       len(dispatch_results),
            "issued_at":        self._now(),
        }

    def issue_cluster_suspension(self, cluster_id: str, ruling_id: uuid.UUID,
                                   basis: str) -> Dict[str, Any]:
        """
        Issue a cluster-level suspension directive under a ratified ruling.
        Cluster suspension requires unanimous Council vote (VR-02-09).
        Returns issuance result dict.
        """
        if not self.assert_constitutional_compliance(ruling_id):
            self.logger.log(
                f"CouncilOfMetanoia.issue_cluster_suspension BLOCKED | "
                f"constitutional compliance failed | ruling_id={ruling_id}"
            )
            return {
                "success":   False,
                "error":     "Constitutional compliance check failed",
                "ruling_id": str(ruling_id),
            }

        self.logger.log(
            f"CouncilOfMetanoia cluster suspension issued | "
            f"cluster_id={cluster_id} | ruling_id={ruling_id} | "
            f"basis={basis!r}"
        )

        # TODO (STEP 15C+): Verify unanimous Council vote record in CLU-02.4;
        # emit CLUSTER_SUSPENSION override via GovernanceOverrideManager;
        # emit IC-08 directive to cluster.
        return {
            "success":    True,
            "cluster_id": cluster_id,
            "ruling_id":  str(ruling_id),
            "basis":      basis,
            "issued_at":  self._now(),
        }

    # ------------------------------------------------------------------
    # Pending directive access
    # ------------------------------------------------------------------

    def get_pending_directives(self) -> List[Dict[str, Any]]:
        """
        Return the current queue of directives awaiting IC-08 emission.
        Used by GovernanceLayer for STEP 15C wiring verification.
        """
        return list(self._pending_directives)
