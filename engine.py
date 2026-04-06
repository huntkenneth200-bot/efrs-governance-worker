"""
FORMATION INTELLIGENCE PLATFORM
Engine — Primary Entry Point

Reference: ENGINE-01
Version: 1.0
Status: ACTIVE — Render deployment entry point

Exposes:
  - process_scenario(scenario: dict) -> dict
  - get_platform() -> FormationIntelligencePlatform
  - health_check() -> dict

Authority: Council of Metanoia (DOC-01.1 Platform Governing Charter)
"""

from __future__ import annotations

import datetime
import traceback
from typing import Any

from config import PlatformConfig
from main import FormationIntelligencePlatform
from governance import GovernanceLayer


# ── Module-level platform singleton ──────────────────────────────────────────
_config: PlatformConfig | None = None
_platform: FormationIntelligencePlatform | None = None
_governance: GovernanceLayer | None = None


def _now() -> str:
    return (
        datetime.datetime.now(datetime.timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def _initialize() -> FormationIntelligencePlatform:
    """
    Lazy singleton initializer.  Called on first access.
    Instantiates PlatformConfig, FormationIntelligencePlatform, and GovernanceLayer.
    Subsequent calls return the cached singleton.
    """
    global _config, _platform, _governance

    if _platform is not None:
        return _platform

    _config = PlatformConfig()
    _platform = FormationIntelligencePlatform(_config)

    # Activate Governance Layer (STEP 15C activation gate)
    _governance = GovernanceLayer(_config, _platform.logger)
    _platform.governance_layer = _governance

    _platform.logger.log(
        "ENGINE-01 | platform initialized | governance_layer=ACTIVE | status=READY"
    )
    return _platform


def get_platform() -> FormationIntelligencePlatform:
    """
    Returns the initialized platform singleton.
    Initializes on first call.
    """
    return _initialize()


def health_check() -> dict:
    """
    Returns a structured health report for the entire platform.

    Checks:
      - Platform cold-start integrity
      - All six clusters present
      - ICBus emitter count
      - GovernanceLayer health (status, wires, routes)

    Returns dict with keys:
      status         : "READY" | "DEGRADED"
      checked_at     : ISO-8601 UTC timestamp
      clusters       : dict of cluster name -> class name
      ic_bus         : dict with emitter_count
      governance     : GovernanceLayer.health_check() output | error string
      errors         : list of error strings (empty if READY)
    """
    errors: list[str] = []
    result: dict[str, Any] = {"checked_at": _now()}

    # Platform init
    try:
        platform = _initialize()
    except Exception as exc:
        return {
            "status": "DEGRADED",
            "checked_at": result["checked_at"],
            "errors": [f"Platform init failed: {exc}"],
        }

    # Cluster presence
    cluster_map = {
        "council": platform.council,
        "restoration_os": platform.restoration_os,
        "spikenard": platform.spikenard,
        "emmaus_road": platform.emmaus_road,
        "linguistic_engine": platform.linguistic_engine,
        "capital_engine": platform.capital_engine,
    }
    result["clusters"] = {k: type(v).__name__ for k, v in cluster_map.items()}
    for k, v in cluster_map.items():
        if v is None:
            errors.append(f"Cluster missing: {k}")

    # ICBus
    ic_emitters = [m for m in dir(platform.ic_bus) if m.startswith("emit_ic")]
    result["ic_bus"] = {"emitter_count": len(ic_emitters)}
    if len(ic_emitters) < 14:
        errors.append(f"ICBus: expected >=14 emitters, found {len(ic_emitters)}")

    # Governance Layer
    try:
        gov = platform.governance_layer
        if gov is None:
            errors.append("GovernanceLayer not activated (governance_layer is None)")
            result["governance"] = "NOT ACTIVATED"
        else:
            hc = gov.health_check()
            result["governance"] = hc
            if hc.get("status") != "READY":
                errors.append(f"GovernanceLayer degraded: {hc}")
    except Exception as exc:
        errors.append(f"GovernanceLayer check failed: {exc}")
        result["governance"] = str(exc)

    result["status"] = "READY" if not errors else "DEGRADED"
    result["errors"] = errors
    return result


# ── Scenario type constants ───────────────────────────────────────────────────

SCENARIO_FRACTURE_ASSESSMENT  = "fracture_assessment"
SCENARIO_STAGE_PROGRESSION    = "stage_progression"
SCENARIO_BLOCKAGE_DETECTION   = "blockage_detection"
SCENARIO_HUB_HEALTH           = "hub_health"
SCENARIO_THEOLOGICAL_REVIEW   = "theological_review"
SCENARIO_LEXICON_AUDIT         = "lexicon_audit"
SCENARIO_CAPITAL_CLEARANCE    = "capital_clearance"
SCENARIO_GOVERNANCE_DRIFT     = "governance_drift"
SCENARIO_HEALTH_CHECK         = "health_check"


def process_scenario(scenario: dict) -> dict:
    """
    Primary platform entry point.

    Accepts a scenario dict with at minimum:
      {
        "type": "<scenario_type>",
        "payload": { ... }
      }

    Supported scenario types:
      fracture_assessment   — run CLU-01.1 FractureAssessmentEngine
      stage_progression     — run CLU-01.2 StageProgressionLogic
      blockage_detection    — run CLU-01.4 BlockageDetectionModule
      hub_health            — run CLU-04.6 HubHealthAssessmentModule
      theological_review    — run CLU-02.6 TheologicalReviewEngine
      lexicon_audit         — run CLU-05.2 LanguageAuditModule
      capital_clearance     — run CLU-03.1 CapitalSourceIntegrityFilter
      governance_drift      — submit drift score to GovernanceLayer
      health_check          — return platform health check

    Returns:
      {
        "success": bool,
        "scenario_type": str,
        "processed_at": str,          # ISO-8601 UTC
        "result": dict | None,
        "error": str | None
      }
    """
    processed_at = _now()
    scenario_type = scenario.get("type", "unknown")
    payload = scenario.get("payload", {})

    try:
        platform = _initialize()
        result = _dispatch(platform, scenario_type, payload)
        return {
            "success": True,
            "scenario_type": scenario_type,
            "processed_at": processed_at,
            "result": result,
            "error": None,
        }
    except Exception as exc:
        return {
            "success": False,
            "scenario_type": scenario_type,
            "processed_at": processed_at,
            "result": None,
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }


def _dispatch(platform: FormationIntelligencePlatform, scenario_type: str, payload: dict) -> dict:
    """
    Internal dispatcher. Routes scenario_type to the appropriate cluster method.
    All cluster methods receive (platform, payload) and return a result dict.
    """

    if scenario_type == SCENARIO_HEALTH_CHECK:
        return health_check()

    if scenario_type == SCENARIO_FRACTURE_ASSESSMENT:
        return _scenario_fracture_assessment(platform, payload)

    if scenario_type == SCENARIO_STAGE_PROGRESSION:
        return _scenario_stage_progression(platform, payload)

    if scenario_type == SCENARIO_BLOCKAGE_DETECTION:
        return _scenario_blockage_detection(platform, payload)

    if scenario_type == SCENARIO_HUB_HEALTH:
        return _scenario_hub_health(platform, payload)

    if scenario_type == SCENARIO_THEOLOGICAL_REVIEW:
        return _scenario_theological_review(platform, payload)

    if scenario_type == SCENARIO_LEXICON_AUDIT:
        return _scenario_lexicon_audit(platform, payload)

    if scenario_type == SCENARIO_CAPITAL_CLEARANCE:
        return _scenario_capital_clearance(platform, payload)

    if scenario_type == SCENARIO_GOVERNANCE_DRIFT:
        return _scenario_governance_drift(platform, payload)

    supported = [
        SCENARIO_FRACTURE_ASSESSMENT, SCENARIO_STAGE_PROGRESSION,
        SCENARIO_BLOCKAGE_DETECTION, SCENARIO_HUB_HEALTH,
        SCENARIO_THEOLOGICAL_REVIEW, SCENARIO_LEXICON_AUDIT,
        SCENARIO_CAPITAL_CLEARANCE, SCENARIO_GOVERNANCE_DRIFT,
        SCENARIO_HEALTH_CHECK,
    ]
    raise ValueError(
        f"Unknown scenario type: '{scenario_type}'. Supported: {supported}"
    )


# ── Scenario handlers ─────────────────────────────────────────────────────────

def _scenario_fracture_assessment(platform: FormationIntelligencePlatform, payload: dict) -> dict:
    """
    Route: CLU-01.1 — FractureAssessmentEngine
    Expected payload keys: participant_id, facilitator_id, assessment_refs (optional)
    """
    # TODO (STEP 18+): Wire to FractureAssessmentEngine.run_assessment(payload)
    # Stub: confirm routing reaches the correct cluster submodule
    engine = platform.restoration_os.fracture_engine
    return {
        "routed_to": type(engine).__name__,
        "cluster": "CLU-01",
        "submodule": "01.1",
        "payload_received": list(payload.keys()),
        "status": "STUB — implement FractureAssessmentEngine.run_assessment()",
    }


def _scenario_stage_progression(platform: FormationIntelligencePlatform, payload: dict) -> dict:
    """
    Route: CLU-01.2 — StageProgressionLogic
    Expected payload keys: participant_id, current_stage, milestone_refs
    """
    logic = platform.restoration_os.stage_logic
    return {
        "routed_to": type(logic).__name__,
        "cluster": "CLU-01",
        "submodule": "01.2",
        "payload_received": list(payload.keys()),
        "status": "STUB — implement StageProgressionLogic.evaluate_advancement()",
    }


def _scenario_blockage_detection(platform: FormationIntelligencePlatform, payload: dict) -> dict:
    """
    Route: CLU-01.4 — BlockageDetectionModule
    Expected payload keys: participant_id, blockage_type, severity, facilitator_id
    """
    detector = platform.restoration_os.blockage_detector
    return {
        "routed_to": type(detector).__name__,
        "cluster": "CLU-01",
        "submodule": "01.4",
        "payload_received": list(payload.keys()),
        "status": "STUB — implement BlockageDetectionModule.receive_facilitator_submission()",
    }


def _scenario_hub_health(platform: FormationIntelligencePlatform, payload: dict) -> dict:
    """
    Route: CLU-04.6 — HubHealthAssessmentModule
    Expected payload keys: hub_id, hub_leader_id, component_data
    """
    hub_health = platform.emmaus_road.hub_health
    return {
        "routed_to": type(hub_health).__name__,
        "cluster": "CLU-04",
        "submodule": "04.6",
        "payload_received": list(payload.keys()),
        "status": "STUB — implement HubHealthAssessmentModule.run_assessment()",
    }


def _scenario_theological_review(platform: FormationIntelligencePlatform, payload: dict) -> dict:
    """
    Route: CLU-02.6 — TheologicalReviewEngine
    Expected payload keys: content_ref, content_type, requesting_module, priority
    """
    reviewer = platform.council.theological_review
    return {
        "routed_to": type(reviewer).__name__,
        "cluster": "CLU-02",
        "submodule": "02.6",
        "payload_received": list(payload.keys()),
        "status": "STUB — implement TheologicalReviewEngine.submit_for_review()",
    }


def _scenario_lexicon_audit(platform: FormationIntelligencePlatform, payload: dict) -> dict:
    """
    Route: CLU-05.2 — LanguageAuditModule
    Expected payload keys: content_ref, content_type, requesting_cluster
    """
    auditor = platform.linguistic_engine.language_auditor
    return {
        "routed_to": type(auditor).__name__,
        "cluster": "CLU-05",
        "submodule": "05.2",
        "payload_received": list(payload.keys()),
        "status": "STUB — implement LanguageAuditModule.audit_content()",
    }


def _scenario_capital_clearance(platform: FormationIntelligencePlatform, payload: dict) -> dict:
    """
    Route: CLU-03.1 — CapitalSourceIntegrityFilter
    Expected payload keys: source_id, source_name, source_type, proposed_conditions
    """
    integrity_filter = platform.spikenard.integrity_filter
    return {
        "routed_to": type(integrity_filter).__name__,
        "cluster": "CLU-03",
        "submodule": "03.1",
        "payload_received": list(payload.keys()),
        "status": "STUB — implement CapitalSourceIntegrityFilter.evaluate_source()",
    }


def _scenario_governance_drift(platform: FormationIntelligencePlatform, payload: dict) -> dict:
    """
    Route: GovernanceLayer.DriftDetectionService
    Expected payload keys: cluster_id, drift_score, metric_ref
    """
    gov = platform.governance_layer
    if gov is None:
        raise RuntimeError("GovernanceLayer not activated. Cannot process governance_drift scenario.")

    cluster_id  = payload.get("cluster_id", "CLU-01")
    drift_type  = payload.get("drift_type", "operational")
    observation = payload.get("observation_data", {})

    # Route to the appropriate measure_* method based on drift_type
    drift_service = gov.drift_detection
    measure_fn_map = {
        "formation":   drift_service.measure_formation_drift,
        "theological": drift_service.measure_theological_drift,
        "financial":   drift_service.measure_financial_drift,
        "language":    drift_service.measure_language_drift,
        "operational": drift_service.measure_operational_drift,
    }
    measure_fn = measure_fn_map.get(drift_type, drift_service.measure_operational_drift)
    drift_score = measure_fn(cluster_id=cluster_id, observation_data=observation)

    return {
        "routed_to":   type(drift_service).__name__,
        "cluster_id":  cluster_id,
        "drift_type":  drift_type,
        "drift_score": drift_score,
        "threshold_warning":     drift_service.ALERT_THRESHOLD,
        "threshold_remediation": drift_service.CRITICAL_THRESHOLD,
        "alert_triggered": drift_score >= drift_service.ALERT_THRESHOLD,
    }


# ── CLI / Render worker entry point ───────────────────────────────────────────

if __name__ == "__main__":
    import json

    # On startup: run health check and log result
    result = health_check()
    print(json.dumps(result, indent=2, default=str))

    if result["status"] == "READY":
        print("\nFormation Intelligence Platform — READY")
        platform = get_platform()
        platform.run()
    else:
        print("\nFormation Intelligence Platform — DEGRADED")
        for err in result.get("errors", []):
            print(f"  ERROR: {err}")
        raise SystemExit(1)
