"""
FORMATION INTELLIGENCE PLATFORM — GOVERNANCE LAYER
Governance Override Manager

Manages exceptional governance overrides. All state is in-memory;
TODO annotations mark persistence integration points.

Authority: DOC-01.1, DOC-01.2
Version: 1.0
Status: TRUSTED — Cleared for Governance Layer Integration
"""

from __future__ import annotations
import uuid
import datetime
from typing import TYPE_CHECKING, Optional, List, Dict, Any

if TYPE_CHECKING:
    from config import PlatformConfig
    from logs.platform_logger import PlatformLogger

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OVERRIDE_TYPES = (
    "OPERATIONAL_HOLD",
    "FORMATION_FREEZE",
    "CAPITAL_HOLD",
    "LANGUAGE_LOCKDOWN",
    "CLUSTER_SUSPENSION",
    "THEOLOGICAL_QUARANTINE",
)

OVERRIDE_STATUSES = ("Pending", "Active", "Resolved", "Expired", "Escalated")

# Override types that require a ruling_ref at issuance time
_RULING_REQUIRED_TYPES = {
    "FORMATION_FREEZE",
    "CAPITAL_HOLD",
    "LANGUAGE_LOCKDOWN",
    "CLUSTER_SUSPENSION",
    "THEOLOGICAL_QUARANTINE",
}

# Override types that may be issued on emergency basis (ruling obtained within window)
_EMERGENCY_TYPES = {"OPERATIONAL_HOLD"}


class GovernanceOverrideManager:
    """
    Governance-layer exceptional override authority.
    Manages override lifecycle: Pending → Active → Resolved | Expired | Escalated.

    Override registry keyed by override_id (UUID string).
    Enforcement hooks called by ICBus and cluster logic (wired in STEP 15C).

    STATUS: TRUSTED — Cleared for Governance Layer Integration
    """

    def __init__(self, config: "PlatformConfig", logger: "PlatformLogger"):
        self.config = config
        self.logger = logger
        # override_id (str) → override_record dict
        self._overrides: Dict[str, Dict[str, Any]] = {}
        # TODO (STEP 15C+): Load active overrides from governance state store.

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _now(self) -> str:
        return datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="milliseconds").replace("+00:00", "Z")

    def _acknowledgment_deadline(self) -> str:
        """
        Compute the deadline by which an emergency OPERATIONAL_HOLD must
        be ratified by Council (PlatformConfig.COUNCIL_ACKNOWLEDGMENT_REQUIRED_DAYS).
        """
        days = getattr(self.config, "COUNCIL_ACKNOWLEDGMENT_REQUIRED_DAYS", 14)
        deadline = (
            datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(days=days)
        )
        return deadline.date().isoformat()

    # ------------------------------------------------------------------
    # Override issuance
    # ------------------------------------------------------------------

    def issue_override(self, override_type: str, target_id: str,
                        issued_by: uuid.UUID, basis: str,
                        ruling_ref: Optional[uuid.UUID] = None,
                        expiry_date: Optional[datetime.date] = None) -> Optional[uuid.UUID]:
        """
        Issue a governance override against a cluster, submodule, or IC pathway.
        Returns override_id on success, None on validation failure.

        OPERATIONAL_HOLD — emergency basis allowed; status=Pending until ruling obtained.
        All other types — ruling_ref required; status=Active immediately.
        """
        # Validate type
        if override_type not in OVERRIDE_TYPES:
            self.logger.log(
                f"GovernanceOverrideManager.issue_override REJECTED | "
                f"invalid override_type={override_type}"
            )
            return None

        # Ruling requirement enforcement
        if override_type in _RULING_REQUIRED_TYPES and ruling_ref is None:
            self.logger.log(
                f"GovernanceOverrideManager.issue_override REJECTED | "
                f"override_type={override_type} requires ruling_ref | target={target_id}"
            )
            return None

        override_id = uuid.uuid4()
        if override_type in _EMERGENCY_TYPES and ruling_ref is None:
            status = "Pending"
            acknowledgment_deadline = self._acknowledgment_deadline()
        else:
            status = "Active"
            acknowledgment_deadline = None

        record = {
            "override_id":             str(override_id),
            "override_type":           override_type,
            "target_id":               target_id,
            "issued_by":               str(issued_by),
            "basis":                   basis,
            "ruling_ref":              str(ruling_ref) if ruling_ref else None,
            "expiry_date":             expiry_date.isoformat() if expiry_date else None,
            "status":                  status,
            "issued_at":               self._now(),
            "acknowledgment_deadline": acknowledgment_deadline,
            "activated_at":            self._now() if status == "Active" else None,
            "resolved_at":             None,
            "resolution_notes":        None,
            "resolution_ruling_ref":   None,
            "history":                 [],
        }
        self._overrides[str(override_id)] = record
        self.logger.log(
            f"GovernanceOverrideManager override issued | "
            f"override_id={override_id} | type={override_type} | "
            f"target={target_id} | status={status} | "
            f"ruling_ref={ruling_ref}"
        )
        # TODO (STEP 15C+): Persist override record to governance state store.
        return override_id

    def activate_override(self, override_id: uuid.UUID,
                           ruling_ref: uuid.UUID) -> bool:
        """
        Activate a Pending override after Council ruling is obtained.
        Transitions Pending → Active. Returns True on success.
        """
        record = self._overrides.get(str(override_id))
        if not record:
            self.logger.log(
                f"GovernanceOverrideManager.activate_override NOT FOUND | "
                f"override_id={override_id}"
            )
            return False
        if record["status"] != "Pending":
            self.logger.log(
                f"GovernanceOverrideManager.activate_override INVALID_STATE | "
                f"override_id={override_id} | current_status={record['status']}"
            )
            return False
        record["status"] = "Active"
        record["ruling_ref"] = str(ruling_ref)
        record["activated_at"] = self._now()
        record["history"].append({
            "event": "activated", "ruling_ref": str(ruling_ref), "at": self._now()
        })
        self.logger.log(
            f"GovernanceOverrideManager override activated | "
            f"override_id={override_id} | ruling_ref={ruling_ref}"
        )
        # TODO (STEP 15C+): Persist status transition.
        return True

    def resolve_override(self, override_id: uuid.UUID,
                          resolved_by: uuid.UUID,
                          resolution_notes: str,
                          ruling_ref: uuid.UUID) -> bool:
        """
        Resolve an active override. Requires ruling reference.
        Transitions Active → Resolved. Returns True on success.
        """
        record = self._overrides.get(str(override_id))
        if not record:
            self.logger.log(
                f"GovernanceOverrideManager.resolve_override NOT FOUND | "
                f"override_id={override_id}"
            )
            return False
        if record["status"] not in ("Active", "Pending"):
            self.logger.log(
                f"GovernanceOverrideManager.resolve_override INVALID_STATE | "
                f"override_id={override_id} | current_status={record['status']}"
            )
            return False
        record["status"] = "Resolved"
        record["resolved_at"] = self._now()
        record["resolution_notes"] = resolution_notes
        record["resolution_ruling_ref"] = str(ruling_ref)
        record["history"].append({
            "event": "resolved", "resolved_by": str(resolved_by),
            "ruling_ref": str(ruling_ref), "at": self._now()
        })
        self.logger.log(
            f"GovernanceOverrideManager override resolved | "
            f"override_id={override_id} | resolved_by={resolved_by} | "
            f"ruling_ref={ruling_ref}"
        )
        # TODO (STEP 15C+): Persist resolution; notify target cluster via routing table.
        return True

    def escalate_override(self, override_id: uuid.UUID,
                           escalation_reason: str) -> bool:
        """
        Escalate an unresolved override to full Council session.
        Transitions Active/Pending → Escalated. Returns True on success.
        """
        record = self._overrides.get(str(override_id))
        if not record:
            self.logger.log(
                f"GovernanceOverrideManager.escalate_override NOT FOUND | "
                f"override_id={override_id}"
            )
            return False
        if record["status"] not in ("Active", "Pending"):
            self.logger.log(
                f"GovernanceOverrideManager.escalate_override INVALID_STATE | "
                f"override_id={override_id} | current_status={record['status']}"
            )
            return False
        record["status"] = "Escalated"
        record["escalated_at"] = self._now()
        record["escalation_reason"] = escalation_reason
        record["history"].append({
            "event": "escalated", "reason": escalation_reason, "at": self._now()
        })
        self.logger.log(
            f"GovernanceOverrideManager override escalated | "
            f"override_id={override_id} | reason={escalation_reason}"
        )
        # TODO (STEP 15C+): Route override_id to Council governance session agenda.
        return True

    # ------------------------------------------------------------------
    # Override queries
    # ------------------------------------------------------------------

    def get_active_overrides(self,
                              target_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Return all Active overrides, optionally filtered by target_id.
        """
        results = []
        for record in self._overrides.values():
            if record["status"] != "Active":
                continue
            if target_id and record["target_id"] != target_id:
                continue
            results.append(dict(record))
        return results

    def get_override(self, override_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """Retrieve a full override record by ID."""
        record = self._overrides.get(str(override_id))
        return dict(record) if record else None

    def is_target_under_override(self, target_id: str,
                                   override_type: Optional[str] = None) -> bool:
        """
        Check whether a target is under any active override.
        Optionally filter by override_type.
        """
        for record in self._overrides.values():
            if record["status"] != "Active":
                continue
            if record["target_id"] != target_id:
                continue
            if override_type and record["override_type"] != override_type:
                continue
            return True
        return False

    # ------------------------------------------------------------------
    # Enforcement hooks
    # ------------------------------------------------------------------

    def check_ic_override(self, ic_name: str,
                           target_cluster: str) -> Optional[Dict[str, Any]]:
        """
        Check whether an IC emit should be blocked by an active override.
        Blocks on: OPERATIONAL_HOLD or CLUSTER_SUSPENSION for target_cluster.
        Blocks IC-11/IC-12 on: LANGUAGE_LOCKDOWN for target_cluster.
        Returns blocking override record or None if clear.
        """
        blocking_types_general = {"OPERATIONAL_HOLD", "CLUSTER_SUSPENSION"}
        blocking_types_language = {"LANGUAGE_LOCKDOWN"}

        for record in self._overrides.values():
            if record["status"] != "Active":
                continue
            if record["target_id"] != target_cluster:
                continue
            otype = record["override_type"]
            if otype in blocking_types_general:
                return dict(record)
            if otype in blocking_types_language and ic_name in ("IC-11", "IC-12"):
                return dict(record)
        return None

    def check_formation_freeze(self,
                                participant_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """
        Check whether a participant's stage advancement is frozen.
        target_id for FORMATION_FREEZE is the participant_id string.
        Returns override record if frozen, None if clear.
        """
        pid = str(participant_id)
        for record in self._overrides.values():
            if record["status"] != "Active":
                continue
            if record["override_type"] != "FORMATION_FREEZE":
                continue
            # target_id may be a participant_id or "all-participants"
            if record["target_id"] in (pid, "all-participants"):
                return dict(record)
        return None

    def check_capital_hold(self,
                            transaction_ref: uuid.UUID) -> Optional[Dict[str, Any]]:
        """
        Check whether a capital transaction is under a CAPITAL_HOLD.
        target_id for CAPITAL_HOLD is a transaction scope or "all-capital".
        Returns override record if held, None if clear.
        """
        tref = str(transaction_ref)
        for record in self._overrides.values():
            if record["status"] != "Active":
                continue
            if record["override_type"] != "CAPITAL_HOLD":
                continue
            if record["target_id"] in (tref, "all-capital"):
                return dict(record)
        return None

    # ------------------------------------------------------------------
    # Expiry management
    # ------------------------------------------------------------------

    def sweep_expired_overrides(self,
                                 sweep_date: datetime.date) -> List[uuid.UUID]:
        """
        Sweep for overrides whose expiry_date has passed.
        Expired overrides without resolution ruling are automatically escalated.
        Returns list of expired override_ids.
        """
        expired_ids: List[uuid.UUID] = []
        sweep_iso = sweep_date.isoformat()

        for record in self._overrides.values():
            if record["status"] not in ("Active", "Pending"):
                continue
            expiry = record.get("expiry_date")
            if expiry and expiry <= sweep_iso:
                oid = uuid.UUID(record["override_id"])
                # If resolved ruling present, mark Resolved; else escalate
                if record.get("resolution_ruling_ref"):
                    record["status"] = "Resolved"
                    record["resolved_at"] = self._now()
                    record["history"].append({
                        "event": "auto-resolved-on-expiry", "at": self._now()
                    })
                else:
                    record["status"] = "Expired"
                    record["expired_at"] = self._now()
                    record["history"].append({
                        "event": "expired", "sweep_date": sweep_iso, "at": self._now()
                    })
                    self.escalate_override(
                        oid,
                        f"Override expired without resolution on {sweep_iso}"
                    )
                expired_ids.append(oid)
                self.logger.log(
                    f"GovernanceOverrideManager override expired | "
                    f"override_id={oid} | expiry_date={expiry}"
                )
        # TODO (STEP 15C+): Persist expiry transitions to governance state store.
        return expired_ids
