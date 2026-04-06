"""
FORMATION INTELLIGENCE PLATFORM — GOVERNANCE LAYER
Governance Routing Table

Defines and maintains the authoritative routing map for all governance signals.
All state is in-memory; TODO annotations mark persistence integration points.

Authority: DOC-01.1, DOC-01.2
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

DESTINATION_TYPES = ("CLUSTER", "SUBMODULE", "BROADCAST", "COUNCIL")
SIGNAL_TYPES = ("VERDICT", "DIRECTIVE", "DRIFT_ALERT",
                "CONTRACT_ENFORCE", "OVERRIDE", "ESCALATION")

AUTHORITY_LEVELS = ("Council", "Governance-Layer", "Cluster-Operational")

# Default routes: (signal_type, source_id) -> destination
# These represent the constitutional routing baseline established at platform launch.
# Routes may only be amended via Council ruling (VR-GL-02).
_DEFAULT_ROUTE_SPECS = [
    # signal_type,        source_id,              dest_type,   dest_id,               authority_level
    ("VERDICT",           "adjudication-engine",  "CLUSTER",   "target-cluster",      "Governance-Layer"),
    ("DIRECTIVE",         "council",              "BROADCAST", "all-clusters",        "Council"),
    ("DRIFT_ALERT",       "drift-detection",      "CLUSTER",   "adjudication-engine", "Governance-Layer"),
    ("CONTRACT_ENFORCE",  "council",              "CLUSTER",   "target-cluster",      "Council"),
    ("OVERRIDE",          "override-manager",     "CLUSTER",   "target-cluster",      "Governance-Layer"),
    ("ESCALATION",        "adjudication-engine",  "COUNCIL",   "council-session",     "Governance-Layer"),
]


class GovernanceRoutingTable:
    """
    Authoritative routing registry for all governance layer signal dispatch.

    Route keys: (signal_type, source_id)
    Each route entry: {
        signal_type, source_id, destination_type, destination_id,
        authority_level, active, ruling_ref, registered_at, handler
    }

    Handlers are registered by destination_id string and resolved at dispatch time.
    This allows routes to be defined before handler objects exist.

    STATUS: TRUSTED — Cleared for Governance Layer Integration
    """

    def __init__(self, config: "PlatformConfig", logger: "PlatformLogger"):
        self.config = config
        self.logger = logger
        # Route registry: (signal_type, source_id) → route_record
        self._routes: Dict[tuple, Dict[str, Any]] = {}
        # Handler registry: destination_id → callable
        self._handlers: Dict[str, Callable] = {}
        # Dispatch audit log
        self._audit_log: List[Dict[str, Any]] = []
        # TODO (STEP 15C+): Load routes from governance state store.
        self._register_default_routes()

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def _now(self) -> str:
        return datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="milliseconds").replace("+00:00", "Z")

    def _register_default_routes(self) -> None:
        """Register the constitutional baseline routing table."""
        for sig_type, source_id, dest_type, dest_id, authority in _DEFAULT_ROUTE_SPECS:
            key = (sig_type, source_id)
            self._routes[key] = {
                "signal_type":       sig_type,
                "source_id":         source_id,
                "destination_type":  dest_type,
                "destination_id":    dest_id,
                "authority_level":   authority,
                "active":            True,
                "ruling_ref":        None,  # baseline routes require no ruling
                "registered_at":     self._now(),
            }

    # ------------------------------------------------------------------
    # Route registration
    # ------------------------------------------------------------------

    def register_route(self, signal_type: str, source_id: str,
                        destination_type: str, destination_id: str,
                        authority_level: str,
                        ruling_ref: Optional[uuid.UUID] = None) -> bool:
        """
        Register a governance signal route.
        Routes may only be added or modified by Council ruling (VR-GL-02).
        Non-baseline routes require ruling_ref.
        Returns True if registered, False if validation failed.
        """
        if signal_type not in SIGNAL_TYPES:
            self.logger.log(
                f"GovernanceRoutingTable.register_route REJECTED | "
                f"invalid signal_type={signal_type}"
            )
            return False
        if destination_type not in DESTINATION_TYPES:
            self.logger.log(
                f"GovernanceRoutingTable.register_route REJECTED | "
                f"invalid destination_type={destination_type}"
            )
            return False
        if authority_level not in AUTHORITY_LEVELS:
            self.logger.log(
                f"GovernanceRoutingTable.register_route REJECTED | "
                f"invalid authority_level={authority_level}"
            )
            return False
        key = (signal_type, source_id)
        self._routes[key] = {
            "signal_type":       signal_type,
            "source_id":         source_id,
            "destination_type":  destination_type,
            "destination_id":    destination_id,
            "authority_level":   authority_level,
            "active":            True,
            "ruling_ref":        str(ruling_ref) if ruling_ref else None,
            "registered_at":     self._now(),
        }
        self.logger.log(
            f"GovernanceRoutingTable route registered | "
            f"signal_type={signal_type} | source_id={source_id} | "
            f"dest={destination_type}:{destination_id} | ruling_ref={ruling_ref}"
        )
        # TODO (STEP 15C+): Persist route to governance state store.
        return True

    def register_handler(self, destination_id: str, handler: Callable) -> None:
        """
        Register a callable handler for a destination_id.
        Called by GovernanceLayer during service wiring.
        """
        self._handlers[destination_id] = handler

    def deactivate_route(self, signal_type: str, source_id: str,
                          ruling_ref: uuid.UUID) -> bool:
        """
        Deactivate a governance route. Requires ruling reference.
        Deactivated routes are retained for audit — not deleted.
        Returns True if deactivated, False if route not found.
        """
        key = (signal_type, source_id)
        if key not in self._routes:
            self.logger.log(
                f"GovernanceRoutingTable.deactivate_route NOT FOUND | "
                f"signal_type={signal_type} | source_id={source_id}"
            )
            return False
        self._routes[key]["active"] = False
        self._routes[key]["deactivated_at"] = self._now()
        self._routes[key]["deactivation_ruling_ref"] = str(ruling_ref)
        self.logger.log(
            f"GovernanceRoutingTable route deactivated | "
            f"signal_type={signal_type} | source_id={source_id} | ruling_ref={ruling_ref}"
        )
        # TODO (STEP 15C+): Persist deactivation to governance state store.
        return True

    def get_route(self, signal_type: str,
                   source_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve the active route for a signal_type / source_id pair.
        Returns route record dict or None if no active route found.
        """
        key = (signal_type, source_id)
        route = self._routes.get(key)
        if route and route.get("active"):
            return dict(route)
        return None

    def get_all_routes(self) -> List[Dict[str, Any]]:
        """Return all registered routes (active and inactive) for audit."""
        return [dict(r) for r in self._routes.values()]

    # ------------------------------------------------------------------
    # Signal dispatch
    # ------------------------------------------------------------------

    def dispatch(self, signal_type: str, source_id: str,
                  payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dispatch a governance signal to its registered destination.
        Returns dispatch acknowledgment dict.
        If no route found, logs and returns status=NO_ROUTE.
        If handler registered, calls handler(payload) and captures result.
        """
        route = self.get_route(signal_type, source_id)
        dispatch_id = str(uuid.uuid4())
        timestamp = self._now()

        if not route:
            self.logger.log(
                f"GovernanceRoutingTable.dispatch NO_ROUTE | "
                f"signal_type={signal_type} | source_id={source_id}"
            )
            ack = {
                "dispatch_id":    dispatch_id,
                "status":         "NO_ROUTE",
                "signal_type":    signal_type,
                "source_id":      source_id,
                "dispatched_at":  timestamp,
                "destination_id": None,
                "handler_result": None,
            }
            self._audit_log.append(ack)
            return ack

        dest_id = route["destination_id"]
        handler = self._handlers.get(dest_id)
        handler_result = None

        if handler:
            try:
                handler_result = handler(payload)
            except Exception as exc:
                self.logger.log(
                    f"GovernanceRoutingTable.dispatch HANDLER_ERROR | "
                    f"destination_id={dest_id} | error={exc}"
                )
                handler_result = {"error": str(exc)}

        self.logger.log(
            f"GovernanceRoutingTable.dispatch | "
            f"signal_type={signal_type} | source_id={source_id} | "
            f"dest={route['destination_type']}:{dest_id} | "
            f"handler={'registered' if handler else 'not-registered'}"
        )

        ack = {
            "dispatch_id":      dispatch_id,
            "status":           "DISPATCHED",
            "signal_type":      signal_type,
            "source_id":        source_id,
            "dispatched_at":    timestamp,
            "destination_type": route["destination_type"],
            "destination_id":   dest_id,
            "authority_level":  route["authority_level"],
            "handler_result":   handler_result,
        }
        self._audit_log.append(ack)
        # TODO (STEP 15C+): Persist dispatch event to audit store.
        return ack

    def broadcast_directive(self, ruling_id: uuid.UUID, directive_text: str,
                             affected_clusters: List[str]) -> List[Dict[str, Any]]:
        """
        Broadcast a Council directive to all affected clusters.
        Each cluster gets its own dispatch acknowledgment.
        Actual IC-08 emission delegated to the platform ICBus (wired in STEP 15C).
        """
        results = []
        for cluster_id in affected_clusters:
            ack = self.dispatch(
                signal_type="DIRECTIVE",
                source_id="council",
                payload={
                    "ruling_id":      str(ruling_id),
                    "directive_text": directive_text,
                    "target_cluster": cluster_id,
                },
            )
            results.append(ack)
        self.logger.log(
            f"GovernanceRoutingTable.broadcast_directive | "
            f"ruling_id={ruling_id} | clusters={affected_clusters} | "
            f"dispatched={len(results)}"
        )
        return results

    def route_verdict(self, adjudication_id: uuid.UUID, cluster_id: str,
                       verdict: str,
                       directive_text: Optional[str]) -> Dict[str, Any]:
        """
        Route an adjudication verdict to the target cluster's governance receiver.
        """
        return self.dispatch(
            signal_type="VERDICT",
            source_id="adjudication-engine",
            payload={
                "adjudication_id": str(adjudication_id),
                "cluster_id":      cluster_id,
                "verdict":         verdict,
                "directive_text":  directive_text,
            },
        )

    # ------------------------------------------------------------------
    # Routing integrity
    # ------------------------------------------------------------------

    def validate_routing_table(self) -> Dict[str, Any]:
        """
        Validate that all registered active routes are internally consistent.
        Checks: valid signal_type, valid destination_type, valid authority_level.
        Returns validation result dict with any dead or invalid routes listed.
        """
        issues = []
        active_count = 0
        for key, route in self._routes.items():
            if not route.get("active"):
                continue
            active_count += 1
            if route["signal_type"] not in SIGNAL_TYPES:
                issues.append(f"Invalid signal_type on route {key}")
            if route["destination_type"] not in DESTINATION_TYPES:
                issues.append(f"Invalid destination_type on route {key}")
            if route["authority_level"] not in AUTHORITY_LEVELS:
                issues.append(f"Invalid authority_level on route {key}")

        result = {
            "valid":        len(issues) == 0,
            "active_routes": active_count,
            "total_routes":  len(self._routes),
            "issues":        issues,
        }
        self.logger.log(
            f"GovernanceRoutingTable.validate_routing_table | "
            f"active={active_count} | issues={len(issues)}"
        )
        return result

    def get_routing_audit_log(self, from_date=None,
                               to_date=None) -> List[Dict[str, Any]]:
        """
        Return the chronological audit log of all governance signal dispatches.
        Date filtering is applied if from_date / to_date are provided (as ISO strings).
        """
        if from_date is None and to_date is None:
            return list(self._audit_log)
        # Filter by dispatched_at string comparison (ISO format sorts correctly)
        filtered = []
        for entry in self._audit_log:
            ts = entry.get("dispatched_at", "")
            if from_date and ts < str(from_date):
                continue
            if to_date and ts > str(to_date):
                continue
            filtered.append(entry)
        return filtered
