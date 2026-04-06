"""
FORMATION INTELLIGENCE PLATFORM — GOVERNANCE LAYER
Drift Detection Service

Monitors platform operational state against governance baselines to detect
constitutional drift before breach threshold. All state is in-memory;
TODO annotations mark persistence integration points.

Drift magnitude scale: 0.0 (nominal) → 1.0 (breach threshold).

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
# Drift type registry
# ---------------------------------------------------------------------------

DRIFT_TYPES = ("Formation", "Theological", "Financial", "Operational", "Language")

# Keys expected in observation_data per drift type.
# If a key is missing, that dimension contributes 0 to the drift score.
_FORMATION_KEYS = [
    "stage_completion_rate",     # float 0.0-1.0 — fraction of participants on schedule
    "milestone_completion_rate", # float 0.0-1.0
    "facilitator_attestation_rate", # float 0.0-1.0 — fraction with valid attestations
    "avg_days_in_stage",         # float — average days participants spend in current stage
    "overdue_assessment_count",  # int — participants past PERIODIC_ASSESSMENT_INTERVAL
]
_THEOLOGICAL_KEYS = [
    "clearance_rate",            # float 0.0-1.0 — fraction of content with valid clearance
    "flagged_content_count",     # int — content items currently flagged
    "disqualified_content_active", # int — disqualified items still in active pathways
    "expired_conditional_count", # int — conditionally cleared items past expiry
]
_FINANCIAL_KEYS = [
    "max_source_concentration_pct", # float — highest single-source concentration
    "clearance_lapse_count",     # int — sources with expired clearances
    "unauthorized_disbursement_count", # int — disbursements without authorization
    "sufficiency_breach_count",  # int — requests exceeding sufficiency standard
]
_OPERATIONAL_KEYS = [
    "ic_error_rate",             # float 0.0-1.0 — fraction of ICs with errors
    "hub_health_avg_score",      # float 0.0-100.0 — average hub health
    "below_threshold_hub_count", # int — hubs below HUB_HEALTH_BELOW_THRESHOLD_SCORE
    "escalation_backlog_count",  # int — unresolved IC-13 escalations
]
_LANGUAGE_KEYS = [
    "unauthorized_term_usage_count", # int — uses of terms not in authorized lexicon
    "audit_overdue_days",        # int — days since last language audit (if overdue)
    "disqualified_term_exposure_count", # int — detected exposures of disqualified terms
    "lexicon_review_overdue_days", # int — days since last lexicon review (if overdue)
]

_KEY_MAP: Dict[str, List[str]] = {
    "Formation":   _FORMATION_KEYS,
    "Theological": _THEOLOGICAL_KEYS,
    "Financial":   _FINANCIAL_KEYS,
    "Operational": _OPERATIONAL_KEYS,
    "Language":    _LANGUAGE_KEYS,
}


def _normalize(value: float, baseline: float, higher_is_worse: bool = True,
               scale: float = 1.0) -> float:
    """
    Normalize a single metric deviation to [0.0, 1.0] drift contribution.

    higher_is_worse=True  → metric above baseline contributes positive drift
    higher_is_worse=False → metric below baseline contributes positive drift
    scale                 → sensitivity multiplier (default 1.0)

    Returns clamped [0.0, 1.0] value.
    """
    if baseline == 0:
        return min(1.0, abs(value) * scale) if value != 0 else 0.0
    deviation = (value - baseline) / baseline
    if not higher_is_worse:
        deviation = -deviation
    raw = max(0.0, deviation) * scale
    return min(1.0, raw)


class DriftDetectionService:
    """
    Governance-layer drift detection and early-warning system.

    Drift measurement is additive and weighted. Each drift type produces a
    score in [0.0, 1.0]. Scores above ALERT_THRESHOLD trigger alerts to the
    GovernanceAdjudicationEngine (injected reference, set by GovernanceLayer).

    STATUS: TRUSTED — Cleared for Governance Layer Integration
    """

    # Drift magnitude thresholds
    ALERT_THRESHOLD:    float = 0.65
    CRITICAL_THRESHOLD: float = 0.85

    def __init__(self, config: "PlatformConfig", logger: "PlatformLogger"):
        self.config = config
        self.logger = logger
        # (cluster_id, drift_type) → baseline_record
        self._baselines: Dict[tuple, Dict[str, Any]] = {}
        # chronological list of measurement records
        self._history: List[Dict[str, Any]] = []
        # last sweep results: cluster_id → {drift_type → magnitude}
        self._last_sweep: Dict[str, Dict[str, float]] = {}
        # Reference to adjudication engine — injected by GovernanceLayer
        self._adjudication: Optional[Any] = None
        # TODO (STEP 15C+): Load baselines from governance state store.

    def set_adjudication_engine(self, adjudication_engine: Any) -> None:
        """Inject adjudication engine reference (called by GovernanceLayer)."""
        self._adjudication = adjudication_engine

    def _now(self) -> str:
        return datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="milliseconds").replace("+00:00", "Z")

    # ------------------------------------------------------------------
    # Baseline management
    # ------------------------------------------------------------------

    def register_baseline(self, cluster_id: str, drift_type: str,
                           baseline_data: Dict[str, Any]) -> bool:
        """
        Register a governance baseline for a cluster and drift type.
        Baselines are established at platform activation and updated by Council ruling only.
        Returns True on success.
        """
        if drift_type not in DRIFT_TYPES:
            self.logger.log(
                f"DriftDetectionService.register_baseline REJECTED | "
                f"invalid drift_type={drift_type}"
            )
            return False
        key = (cluster_id, drift_type)
        self._baselines[key] = {
            "cluster_id":      cluster_id,
            "drift_type":      drift_type,
            "baseline_data":   dict(baseline_data),
            "ruling_ref":      None,   # TODO: require ruling for updates (not initial set)
            "registered_at":   self._now(),
            "version":         1,
        }
        self.logger.log(
            f"DriftDetectionService baseline registered | "
            f"cluster_id={cluster_id} | drift_type={drift_type}"
        )
        # TODO (STEP 15C+): Persist baseline.
        return True

    def get_baseline(self, cluster_id: str,
                      drift_type: str) -> Optional[Dict[str, Any]]:
        """Retrieve the current governance baseline for a cluster / drift type pair."""
        record = self._baselines.get((cluster_id, drift_type))
        return dict(record) if record else None

    def update_baseline(self, cluster_id: str, drift_type: str,
                         new_baseline_data: Dict[str, Any],
                         ruling_id: uuid.UUID) -> bool:
        """
        Update a governance baseline. Requires a ratified Council ruling reference.
        No baseline may be modified without ruling authorization (VR-GL-01).
        """
        key = (cluster_id, drift_type)
        if key not in self._baselines:
            self.logger.log(
                f"DriftDetectionService.update_baseline NOT FOUND | "
                f"cluster_id={cluster_id} | drift_type={drift_type}"
            )
            return False
        current = self._baselines[key]
        current["baseline_data"] = dict(new_baseline_data)
        current["ruling_ref"] = str(ruling_id)
        current["updated_at"] = self._now()
        current["version"] = current.get("version", 1) + 1
        self.logger.log(
            f"DriftDetectionService baseline updated | "
            f"cluster_id={cluster_id} | drift_type={drift_type} | "
            f"ruling_ref={ruling_id} | version={current['version']}"
        )
        # TODO (STEP 15C+): Persist updated baseline.
        return True

    # ------------------------------------------------------------------
    # Drift measurement — deterministic heuristics
    # ------------------------------------------------------------------

    def _measure(self, cluster_id: str, drift_type: str,
                  observation_data: Dict[str, Any],
                  dimension_specs: List[tuple]) -> float:
        """
        Core measurement engine. dimension_specs is a list of:
            (key, higher_is_worse, sensitivity_scale, weight)
        Returns weighted average drift magnitude in [0.0, 1.0].
        If no baseline registered, returns 0.0 (cannot measure without baseline).
        """
        baseline_record = self._baselines.get((cluster_id, drift_type))
        if not baseline_record:
            return 0.0

        baseline = baseline_record["baseline_data"]
        total_weight = 0.0
        weighted_sum = 0.0

        for key, higher_is_worse, scale, weight in dimension_specs:
            obs_val = observation_data.get(key)
            base_val = baseline.get(key)
            if obs_val is None or base_val is None:
                continue
            drift = _normalize(float(obs_val), float(base_val), higher_is_worse, scale)
            weighted_sum += drift * weight
            total_weight += weight

        if total_weight == 0.0:
            return 0.0
        return min(1.0, weighted_sum / total_weight)

    def measure_formation_drift(self, cluster_id: str,
                                 observation_data: Dict[str, Any]) -> float:
        """
        Measure formation standard drift for a cluster against its Formation baseline.
        Dimensions weighted by criticality per DOC-03.3 formation stage standards.

        Key: (metric, higher_is_worse, sensitivity, weight)
        stage_completion_rate   — lower than baseline → bad → higher_is_worse=False
        milestone_completion    — lower than baseline → bad → higher_is_worse=False
        facilitator_attestation — lower than baseline → bad → higher_is_worse=False
        avg_days_in_stage       — higher than baseline → bad → higher_is_worse=True
        overdue_assessment_count— higher than baseline → bad → higher_is_worse=True
        """
        specs = [
            ("stage_completion_rate",        False, 1.5, 3.0),  # high weight, critical
            ("milestone_completion_rate",     False, 1.2, 2.5),
            ("facilitator_attestation_rate",  False, 1.8, 3.0),  # critical — VR-08-05
            ("avg_days_in_stage",             True,  1.0, 1.5),
            ("overdue_assessment_count",      True,  0.5, 1.0),
        ]
        score = self._measure(cluster_id, "Formation", observation_data, specs)
        self._record_measurement(cluster_id, "Formation", score, observation_data)
        return score

    def measure_theological_drift(self, cluster_id: str,
                                   observation_data: Dict[str, Any]) -> float:
        """
        Measure theological compliance drift. Disqualified active content weighted
        most heavily — represents an active constitutional breach.
        """
        specs = [
            ("clearance_rate",               False, 2.0, 3.0),
            ("flagged_content_count",         True,  0.4, 1.5),
            ("disqualified_content_active",   True,  5.0, 4.0),  # highest weight — critical
            ("expired_conditional_count",     True,  0.8, 2.0),
        ]
        score = self._measure(cluster_id, "Theological", observation_data, specs)
        self._record_measurement(cluster_id, "Theological", score, observation_data)
        return score

    def measure_financial_drift(self, cluster_id: str,
                                 observation_data: Dict[str, Any]) -> float:
        """
        Measure capital stewardship drift.
        Unauthorized disbursements weighted most heavily (direct VR-03-XX breach).
        """
        specs = [
            ("max_source_concentration_pct", True,  1.0, 2.5),
            ("clearance_lapse_count",         True,  0.6, 1.5),
            ("unauthorized_disbursement_count", True, 6.0, 4.0),  # critical
            ("sufficiency_breach_count",      True,  2.0, 2.0),
        ]
        score = self._measure(cluster_id, "Financial", observation_data, specs)
        self._record_measurement(cluster_id, "Financial", score, observation_data)
        return score

    def measure_operational_drift(self, cluster_id: str,
                                   observation_data: Dict[str, Any]) -> float:
        """
        Measure operational behavior drift (IC error rates, hub health).
        """
        specs = [
            ("ic_error_rate",                 True,  3.0, 3.0),
            ("hub_health_avg_score",          False, 1.2, 2.0),
            ("below_threshold_hub_count",     True,  1.0, 2.0),
            ("escalation_backlog_count",      True,  0.5, 1.0),
        ]
        score = self._measure(cluster_id, "Operational", observation_data, specs)
        self._record_measurement(cluster_id, "Operational", score, observation_data)
        return score

    def measure_language_drift(self, cluster_id: str,
                                observation_data: Dict[str, Any]) -> float:
        """
        Measure language usage drift against the authorized lexicon.
        Disqualified term exposure is the most critical indicator.
        """
        specs = [
            ("unauthorized_term_usage_count",      True,  0.8, 2.0),
            ("audit_overdue_days",                  True,  0.3, 1.0),
            ("disqualified_term_exposure_count",    True,  5.0, 4.0),  # critical
            ("lexicon_review_overdue_days",         True,  0.2, 1.0),
        ]
        score = self._measure(cluster_id, "Language", observation_data, specs)
        self._record_measurement(cluster_id, "Language", score, observation_data)
        return score

    def _record_measurement(self, cluster_id: str, drift_type: str,
                              magnitude: float,
                              observation_data: Dict[str, Any]) -> None:
        """Record a drift measurement in the history log."""
        self._history.append({
            "cluster_id":       cluster_id,
            "drift_type":       drift_type,
            "magnitude":        round(magnitude, 4),
            "measured_at":      self._now(),
            "observation_data": dict(observation_data),
        })
        # TODO (STEP 15C+): Persist measurement record.

    # ------------------------------------------------------------------
    # Sweep and alerting
    # ------------------------------------------------------------------

    def run_drift_sweep(self, sweep_date: datetime.date,
                         observations: Optional[Dict[str, Dict[str, Any]]] = None
                         ) -> Dict[str, Dict[str, float]]:
        """
        Execute a full-platform drift sweep.

        observations: {cluster_id: {drift_type: observation_data}}
        If observations is None, uses empty dicts (returns 0.0 for all — no baseline data).

        Returns {cluster_id: {drift_type: magnitude}}.
        Emits alerts for any cluster/type pair above ALERT_THRESHOLD.
        """
        if observations is None:
            observations = {}

        sweep_results: Dict[str, Dict[str, float]] = {}
        measure_map = {
            "Formation":   self.measure_formation_drift,
            "Theological": self.measure_theological_drift,
            "Financial":   self.measure_financial_drift,
            "Operational": self.measure_operational_drift,
            "Language":    self.measure_language_drift,
        }

        # Collect all cluster IDs from baselines
        cluster_ids: set = {key[0] for key in self._baselines.keys()}
        # Also include any in observations not yet in baselines
        cluster_ids.update(observations.keys())

        for cluster_id in sorted(cluster_ids):
            sweep_results[cluster_id] = {}
            for drift_type, measure_fn in measure_map.items():
                obs = observations.get(cluster_id, {}).get(drift_type, {})
                magnitude = measure_fn(cluster_id, obs)
                sweep_results[cluster_id][drift_type] = round(magnitude, 4)
                # Alert if threshold crossed
                if magnitude >= self.ALERT_THRESHOLD:
                    observation_ref = uuid.uuid4()
                    self.emit_drift_alert(cluster_id, drift_type,
                                         magnitude, observation_ref)

        self._last_sweep = sweep_results
        self.logger.log(
            f"DriftDetectionService sweep complete | "
            f"sweep_date={sweep_date} | "
            f"clusters={len(sweep_results)} | "
            f"alerted={sum(1 for cr in sweep_results.values() for m in cr.values() if m >= self.ALERT_THRESHOLD)}"
        )
        # TODO (STEP 15C+): Persist sweep record.
        return sweep_results

    def emit_drift_alert(self, cluster_id: str, drift_type: str,
                          drift_magnitude: float,
                          observation_ref: uuid.UUID) -> None:
        """
        Emit a drift alert. If adjudication engine is injected, forwards alert directly.
        Otherwise logs the alert (non-blocking).
        """
        level = "CRITICAL" if drift_magnitude >= self.CRITICAL_THRESHOLD else "ALERT"
        self.logger.log(
            f"DriftDetectionService.emit_drift_alert | "
            f"level={level} | cluster_id={cluster_id} | "
            f"drift_type={drift_type} | magnitude={drift_magnitude:.4f} | "
            f"observation_ref={observation_ref}"
        )
        if self._adjudication:
            self._adjudication.receive_drift_alert(
                drift_report_id=observation_ref,
                cluster_id=cluster_id,
                drift_type=drift_type,
                drift_magnitude=drift_magnitude,
            )
        # TODO (STEP 15C+): Persist alert record; route through GovernanceRoutingTable.

    def get_drift_history(self, cluster_id: str, drift_type: str,
                           from_date: datetime.date,
                           to_date: datetime.date) -> List[Dict[str, Any]]:
        """
        Retrieve historical drift readings for a cluster / type pair within a date range.
        Date filtering based on measured_at ISO string (ISO sort works correctly).
        """
        from_iso = from_date.isoformat()
        to_iso = to_date.isoformat()
        return [
            r for r in self._history
            if r["cluster_id"] == cluster_id
            and r["drift_type"] == drift_type
            and from_iso <= r["measured_at"][:10] <= to_iso
        ]

    def get_platform_drift_status(self) -> Dict[str, Any]:
        """
        Return a platform-wide drift status snapshot (most recent sweep results).
        Flags any cluster/type pair above ALERT_THRESHOLD.
        """
        alerts = []
        for cluster_id, types in self._last_sweep.items():
            for drift_type, magnitude in types.items():
                if magnitude >= self.ALERT_THRESHOLD:
                    alerts.append({
                        "cluster_id": cluster_id,
                        "drift_type": drift_type,
                        "magnitude":  magnitude,
                        "level":      "CRITICAL" if magnitude >= self.CRITICAL_THRESHOLD else "ALERT",
                    })
        return {
            "sweep_results": dict(self._last_sweep),
            "active_alerts": alerts,
            "alert_count":   len(alerts),
            "status":        "NOMINAL" if not alerts else (
                "CRITICAL" if any(a["level"] == "CRITICAL" for a in alerts) else "ALERT"
            ),
        }
