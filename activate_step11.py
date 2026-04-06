"""
FORMATION INTELLIGENCE PLATFORM
STEP 11 — System Activation Boot Script

Exercises the full platform initialization sequence:
  1. PlatformConfig load
  2. PlatformLogger initialization
  3. Cluster init in dependency order (CLU-02 first)
  4. ICBus construction + subscriber registration
  5. IC heartbeat probes (one call per IC emit method)
  6. Circular dependency detection (import-time check)
  7. Producer→consumer pathway smoke test

This script does NOT call any business logic — all submodule methods are
stubs (pass). It verifies that initialization completes without error and
all wiring resolves.

Authority: STEP 11 Activation
Status: Activation-only — not part of production runtime
"""

import sys
import traceback
from datetime import date
from uuid import uuid4

# ---------------------------------------------------------------------------
# Step 1 — Import resolution check
# ---------------------------------------------------------------------------

results = {}

def record(step: str, status: str, detail: str = ""):
    results[step] = {"status": status, "detail": detail}
    marker = "OK  " if status == "OK" else "FAIL"
    print(f"  [{marker}] {step}" + (f" — {detail}" if detail else ""))


print("\n" + "="*70)
print("  FORMATION INTELLIGENCE PLATFORM — STEP 11 ACTIVATION")
print("="*70 + "\n")

# ---------------------------------------------------------------------------
# PHASE 1 — Import resolution
# ---------------------------------------------------------------------------
print("PHASE 1: Import Resolution")
print("-"*40)

try:
    from config import PlatformConfig
    record("config.PlatformConfig", "OK")
except Exception as e:
    record("config.PlatformConfig", "FAIL", str(e)); sys.exit(1)

try:
    from logs.platform_logger import PlatformLogger
    record("logs.PlatformLogger", "OK")
except Exception as e:
    record("logs.PlatformLogger", "FAIL", str(e)); sys.exit(1)

try:
    import models
    record("models package", "OK",
           f"{len([n for n in dir(models) if not n.startswith('_')])} exports")
except Exception as e:
    record("models package", "FAIL", str(e)); sys.exit(1)

try:
    from ic_payloads import (
        IC01Payload, IC02Payload, IC03Payload,
        IC04HoldPayload, IC04ClearPayload,
        IC05Payload, IC06GovernancePayload, IC06CapitalPayload,
        IC07Payload, IC08Payload, IC09Payload, IC10Payload,
        IC11Payload, IC12Payload, IC13Payload, IC14Payload,
    )
    record("ic_payloads (14 IC payload classes)", "OK")
except Exception as e:
    record("ic_payloads", "FAIL", str(e)); sys.exit(1)

try:
    from ic_integration_stubs import (
        ic_01_stage_progression_stub,
        ic_01_pathway_router_stub,
        ic_05_hospitality_stub,
        ic_06_capital_stub,
        build_ic08_subscribers,
        build_ic11_subscribers,
        build_ic12_subscribers,
    )
    record("ic_integration_stubs (7 stub exports)", "OK")
except Exception as e:
    record("ic_integration_stubs", "FAIL", str(e)); sys.exit(1)

try:
    from clusters.clu_01_restoration_os import RestorationOS
    from clusters.clu_02_council_of_metanoia import CouncilOfMetanoia
    from clusters.clu_03_spikenard_foundation import SpikenardFoundation
    from clusters.clu_04_emmaus_road import EmmausRoad
    from clusters.clu_05_linguistic_diffusion_engine import LinguisticDiffusionEngine
    from clusters.clu_06_capital_access_engine import CapitalAccessEngine
    record("all 6 cluster packages", "OK")
except Exception as e:
    record("cluster packages", "FAIL", str(e)); sys.exit(1)

try:
    from ic_bus import ICBus
    record("ic_bus.ICBus", "OK")
except Exception as e:
    record("ic_bus.ICBus", "FAIL", str(e)); sys.exit(1)

try:
    from main import FormationIntelligencePlatform
    record("main.FormationIntelligencePlatform", "OK")
except Exception as e:
    record("main.FormationIntelligencePlatform", "FAIL", str(e)); sys.exit(1)

# ---------------------------------------------------------------------------
# PHASE 2 — Platform initialization
# ---------------------------------------------------------------------------
print("\nPHASE 2: Platform Initialization (dependency order)")
print("-"*40)

config = PlatformConfig()
logger = PlatformLogger(config)
record("PlatformConfig instantiated", "OK")
record("PlatformLogger instantiated", "OK")

try:
    council = CouncilOfMetanoia(config, logger)
    record("CLU-02 CouncilOfMetanoia (first — governs all)", "OK",
           "governing_authority, theological_review, operations_manager, "
           "ruling_registry, member_accountability, external_relations")
except Exception as e:
    record("CLU-02 CouncilOfMetanoia", "FAIL", str(e))

try:
    restoration_os = RestorationOS(config, logger)
    record("CLU-01 RestorationOS", "OK",
           "fracture_engine, stage_logic, milestone_tracker, "
           "blockage_detector, pathway_router, record_keeper")
except Exception as e:
    record("CLU-01 RestorationOS", "FAIL", str(e))

try:
    spikenard = SpikenardFoundation(config, logger)
    record("CLU-03 SpikenardFoundation", "OK",
           "integrity_filter, giving_engine, stewardship_formation, "
           "financial_reporting, fund_allocation, donor_relations")
except Exception as e:
    record("CLU-03 SpikenardFoundation", "FAIL", str(e))

try:
    emmaus_road = EmmausRoad(config, logger)
    record("CLU-04 EmmausRoad", "OK",
           "hub_formation, covenant_community, rhythm_scheduler, "
           "hospitality, local_church, hub_health")
except Exception as e:
    record("CLU-04 EmmausRoad", "FAIL", str(e))

try:
    linguistic_engine = LinguisticDiffusionEngine(config, logger)
    record("CLU-05 LinguisticDiffusionEngine", "OK",
           "semantic_enforcer, lexicon_manager, language_auditor, "
           "narrative_generator, disqualified_filter, external_router")
except Exception as e:
    record("CLU-05 LinguisticDiffusionEngine", "FAIL", str(e))

try:
    capital_engine = CapitalAccessEngine(config, logger)
    record("CLU-06 CapitalAccessEngine", "OK",
           "stream_manager, grant_pipeline, kingdom_economics, "
           "sufficiency_enforcer, capital_reporting, deployment_funding")
except Exception as e:
    record("CLU-06 CapitalAccessEngine", "FAIL", str(e))

# ---------------------------------------------------------------------------
# PHASE 3 — Full platform boot via main.py
# ---------------------------------------------------------------------------
print("\nPHASE 3: Full Platform Boot (main.py)")
print("-"*40)

try:
    platform = FormationIntelligencePlatform(config)
    record("FormationIntelligencePlatform.__init__", "OK")
except Exception as e:
    record("FormationIntelligencePlatform.__init__", "FAIL", str(e))
    traceback.print_exc()
    sys.exit(1)

try:
    assert hasattr(platform, 'ic_bus'), "ic_bus attribute missing"
    assert isinstance(platform.ic_bus, ICBus), "ic_bus is not an ICBus instance"
    record("ICBus wired to platform", "OK")
except Exception as e:
    record("ICBus wired to platform", "FAIL", str(e))

# ---------------------------------------------------------------------------
# PHASE 4 — IC broadcast subscriber registration
# ---------------------------------------------------------------------------
print("\nPHASE 4: IC Broadcast Subscriber Registration")
print("-"*40)

bus = platform.ic_bus

try:
    ic08_count = len(bus._ic08_subscribers)
    assert ic08_count == 6, f"Expected 6 IC-08 subscribers (1 direct + 5 stubs), got {ic08_count}"
    record("IC-08 subscribers registered", "OK", f"{ic08_count} subscribers (CLU-02.4 direct + 5 cluster stubs)")
except Exception as e:
    record("IC-08 subscribers", "FAIL", str(e))

try:
    ic11_count = len(bus._ic11_subscribers)
    assert ic11_count == 6, f"Expected 6 IC-11 subscribers, got {ic11_count}"
    record("IC-11 subscribers registered", "OK", f"{ic11_count} cluster stubs")
except Exception as e:
    record("IC-11 subscribers", "FAIL", str(e))

try:
    ic12_count = len(bus._ic12_subscribers)
    assert ic12_count == 6, f"Expected 6 IC-12 subscribers, got {ic12_count}"
    record("IC-12 subscribers registered", "OK", f"{ic12_count} cluster stubs")
except Exception as e:
    record("IC-12 subscribers", "FAIL", str(e))

# ---------------------------------------------------------------------------
# PHASE 5 — IC emit method probe (all 16 emit paths)
# ---------------------------------------------------------------------------
print("\nPHASE 5: IC Emit Method Probe (all 16 paths)")
print("-"*40)

today = date.today()
uid = uuid4()

IC_PROBES = [
    ("IC-01", lambda: bus.emit_ic_01(IC01Payload(
        participant_id=uid, intake_questionnaire_ref=uid,
        fracture_map_ref=uid, facilitator_id=uid, assessment_date=today))),
    ("IC-02", lambda: bus.emit_ic_02(IC02Payload(
        fracture_profile_id=uid, participant_id=uid,
        active_domains=["IDENTITY"], severity_per_domain={"IDENTITY": "L1"},
        recommended_entry_stage="STAGE_1", hub_id=uid, facilitator_id=uid))),
    ("IC-03", lambda: bus.emit_ic_03(IC03Payload(
        participant_id=uid, current_stage="STAGE_1",
        milestones_completed=[], milestones_pending=[],
        facilitator_attestation_ids=[], last_assessment_date=today,
        milestone_threshold_met=False, completion_percentage=0.0))),
    ("IC-04 Hold", lambda: bus.emit_ic_04_hold(IC04HoldPayload(
        participant_id=uid, blockage_id=uid,
        blockage_type="FORMATION", blockage_severity="MODERATE",
        detection_trigger="Milestone-stall", facilitator_id=uid,
        detection_date=today))),
    ("IC-04 Clear", lambda: bus.emit_ic_04_clear(IC04ClearPayload(
        participant_id=uid, blockage_id=uid,
        resolved_by=uid, resolution_date=today,
        resolution_documentation="Resolved."))),
    ("IC-05", lambda: bus.emit_ic_05(IC05Payload(
        pathway_id=uid, participant_id=uid, assigned_stage="STAGE_1",
        domain_sequence=["IDENTITY"], hub_id=uid,
        session_type_requirements=["individual"], facilitator_id=uid))),
    ("IC-06 Governance", lambda: bus.emit_ic_06_governance(IC06GovernancePayload(
        report_id=uid, reporting_period_start=today, reporting_period_end=today,
        authorization_ref=uid, total_participants=0,
        stage_distribution={}, domain_prevalence={},
        blockage_frequency={}, milestone_completion_rate=0.0))),
    ("IC-06 Capital", lambda: bus.emit_ic_06_capital(IC06CapitalPayload(
        report_id=uid, reporting_period_start=today, reporting_period_end=today,
        authorization_ref=uid, participant_count=0,
        stage_completion_count={}, program_utilization_rate=0.0))),
    ("IC-07", lambda: bus.emit_ic_07(IC07Payload(
        requesting_module="CLU-01.1", content_type="Document",
        content_ref=uid, asset_content_summary="Test",
        submitted_date=today))),
    ("IC-08", lambda: bus.emit_ic_08(IC08Payload(
        ruling_id=uid, ruling_type="Directive",
        affected_documents=[], affected_clusters=["CLU-01"],
        ruling_text="Test", scriptural_basis="Test",
        effective_date=today, vote_record={}))),
    ("IC-09", lambda: bus.emit_ic_09(IC09Payload(
        clearance_id=uid, source_id=uid, source_name="Test",
        source_type="Individual-donor", integrity_status="Cleared",
        clearance_date=today, expiry_date=today,
        donor_id=uid, amount_category="Small"))),
    ("IC-10", lambda: bus.emit_ic_10(IC10Payload(
        disbursement_authorization_id=uid, allocation_id=uid,
        allocation_type="Deployment", destination_id=uid,
        council_authorization_ref=uid, sufficiency_compliance_ref=uid,
        effective_date=today, authorized_amount_category="Medium"))),
    ("IC-11", lambda: bus.emit_ic_11(IC11Payload(
        clearance_id=uid, content_ref=uid, requesting_cluster="CLU-01",
        compliance_status="Cleared", clearance_date=today))),
    ("IC-12 New-entry", lambda: bus.emit_ic_12(IC12Payload(
        propagation_id=uid, update_id=uid, update_type="New-entry",
        term="test-term", updated_entry_ref=uid,
        council_ruling_ref=uid, effective_date=today))),
    ("IC-12 Disqualification", lambda: bus.emit_ic_12(IC12Payload(
        propagation_id=uid, update_id=uid, update_type="Disqualification",
        term="disq-term", updated_entry_ref=uid,
        council_ruling_ref=uid, effective_date=today))),
    ("IC-13", lambda: bus.emit_ic_13(IC13Payload(
        health_assessment_id=uid, hub_id=uid, health_score=65.0,
        consecutive_below_threshold=2, risk_areas=["formation_outcomes"],
        hub_leader_id=uid, assessment_date=today))),
    ("IC-14", lambda: bus.emit_ic_14(IC14Payload(
        funding_authorization_id=uid, deployment_request_id=uid,
        hub_id=uid, authorized_amount_category="Large",
        funding_status="Authorized", deployment_template_ref="DT-01",
        council_authorization_ref=uid, authorization_date=today,
        expiry_date=today))),
]

for ic_name, probe in IC_PROBES:
    try:
        probe()
        record(ic_name, "OK")
    except Exception as e:
        record(ic_name, "FAIL", str(e))

# ---------------------------------------------------------------------------
# PHASE 6 — Heartbeat
# ---------------------------------------------------------------------------
print("\nPHASE 6: System Heartbeat")
print("-"*40)

components = [
    "CLU-01 RestorationOS",
    "CLU-02 CouncilOfMetanoia",
    "CLU-03 SpikenardFoundation",
    "CLU-04 EmmausRoad",
    "CLU-05 LinguisticDiffusionEngine",
    "CLU-06 CapitalAccessEngine",
    "ICBus",
    "PlatformLogger",
]
for comp in components:
    logger.heartbeat(comp)
record("All cluster heartbeats emitted", "OK")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n" + "="*70)
print("  STEP 11 ACTIVATION SUMMARY")
print("="*70)

ok = sum(1 for v in results.values() if v["status"] == "OK")
fail = sum(1 for v in results.values() if v["status"] == "FAIL")
total = ok + fail

print(f"\n  Total checks : {total}")
print(f"  Passed       : {ok}")
print(f"  Failed       : {fail}")

if fail == 0:
    print("\n  STATUS: ACTIVATION COMPLETE — Ready for STEP 12\n")
else:
    print("\n  STATUS: ACTIVATION INCOMPLETE — Failures listed above\n")
    sys.exit(1)
