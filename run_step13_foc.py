"""
FORMATION INTELLIGENCE PLATFORM
STEP 13 — First Operational Cycle (FOC)

Executes the platform's first full operational pass using a controlled test signal.
Injects a representative participant record at CLU-01.1 (FractureAssessmentEngine)
and traces the complete signal chain through all specified IC pathways.

Signal Pathway:
  Entry:   CLU-01.1 (FractureAssessmentEngine)
  IC-01 -> CLU-01.1 receive_assessment + CLU-01.2 stub + CLU-01.5 stub
  IC-02 -> CLU-01.5 receive_finalized_profile
  IC-07 -> CLU-02.2 receive_review_request (theological review of formation content)
  IC-11 -> All clusters (language compliance clearance)
  IC-05 -> CLU-04.1 + CLU-04.3 stub + CLU-04.4 stub
  IC-03 -> CLU-01.2 receive_milestone_signal
  IC-06 -> CLU-02.1 receive_formation_record_feed + CLU-06.5 stub
  IC-08 -> CLU-02.4 + all cluster stubs (council ruling propagation)
  IC-13 -> CLU-02.1 receive_hub_health_escalation
  IC-09 -> CLU-03.2 + CLU-06.1 (capital source clearance)
  IC-10 -> CLU-06.6 (fund allocation)
  IC-12 -> All clusters + CLU-05.3 (lexicon update)
  IC-14 -> CLU-04.1 (deployment funding)

Authority: STEP 13 FOC execution — no wiring or models modified.
"""

import sys
import io
import uuid
from datetime import date, timedelta
from contextlib import contextmanager

# ---------------------------------------------------------------------------
# Log capture context manager
# Wraps platform logger to capture lines into a list while also printing.
# ---------------------------------------------------------------------------

_foc_log: list[str] = []

def _make_capturing_logger(original_logger):
    """
    Wraps the original PlatformLogger so every .log() / .info() / .warning()
    / .error() / .critical() / .heartbeat() call is both printed and captured
    in _foc_log for post-run signal trace analysis.
    """
    original_log = original_logger.log

    def capturing_log(message: str, *args, **kwargs):
        _foc_log.append(message)
        return original_log(message, *args, **kwargs)

    original_logger.log = capturing_log
    return original_logger


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

WIDTH = 70

def section(title: str):
    print()
    print("=" * WIDTH)
    print(f"  {title}")
    print("=" * WIDTH)

def phase(label: str):
    print()
    print(f"  ── {label} {'─' * (WIDTH - 6 - len(label))}")

def ok(step: str, detail: str = ""):
    suffix = f" — {detail}" if detail else ""
    print(f"    [FIRE] {step}{suffix}")

def note(msg: str):
    print(f"    [NOTE] {msg}")

def warn(msg: str):
    print(f"    [WARN] {msg}")

def trace(msg: str):
    print(f"           {msg}")


# ---------------------------------------------------------------------------
# Signal trace collector
# ---------------------------------------------------------------------------

class SignalTrace:
    """Records each IC activation event for the final FOC report."""
    def __init__(self):
        self.events: list[dict] = []

    def record(self, ic: str, producer: str, consumers: list[str],
               payload_summary: str, status: str = "OK", notes: str = ""):
        self.events.append({
            "ic": ic,
            "producer": producer,
            "consumers": consumers,
            "payload_summary": payload_summary,
            "status": status,
            "notes": notes,
        })

    def activation_order(self) -> list[str]:
        return [e["ic"] for e in self.events]


# ---------------------------------------------------------------------------
# FOC Test Data (controlled test payload)
# Representative of a real participant entering the formation pathway.
# All IDs are deterministic UUIDs derived from a fixed namespace seed
# so the FOC run is fully reproducible.
# ---------------------------------------------------------------------------

NS = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")   # RFC 4122 DNS namespace

def foc_id(label: str) -> uuid.UUID:
    """Deterministic UUID for FOC test data."""
    return uuid.uuid5(NS, f"FOC-STEP13-{label}")

TODAY     = date(2026, 3, 31)
YESTERDAY = TODAY - timedelta(days=1)
NEXT_YEAR = TODAY + timedelta(days=365)

# Participant
PARTICIPANT_ID     = foc_id("participant-001")
FACILITATOR_ID     = foc_id("facilitator-001")
HUB_ID             = foc_id("hub-001")

# Formation documents
QUESTIONNAIRE_REF  = foc_id("doc-04-1-questionnaire")
FRACTURE_MAP_REF   = foc_id("doc-04-2-fracture-map")
FORMATION_CONTENT_REF = foc_id("doc-formation-content-001")

# Profile / routing
FRACTURE_PROFILE_ID = foc_id("fracture-profile-001")
PATHWAY_ID          = foc_id("pathway-001")

# Milestones
MILESTONE_A = foc_id("milestone-a")
MILESTONE_B = foc_id("milestone-b")
MILESTONE_C = foc_id("milestone-c")
ATTESTATION = foc_id("attestation-001")

# Council / governance
RULING_ID         = foc_id("ruling-001")
REPORT_ID         = foc_id("report-001")
AUTH_REF          = foc_id("authorization-001")
CLEARANCE_ID      = foc_id("lc-clearance-001")
LC_CONTENT_REF    = foc_id("lc-content-001")
LEXICON_UPDATE_ID = foc_id("lexicon-update-001")
LEXICON_PROP_ID   = foc_id("lexicon-propagation-001")
LEXICON_ENTRY_REF = foc_id("lexicon-entry-001")
RULING_REF        = foc_id("lexicon-ruling-ref")

# Capital
SOURCE_ID         = foc_id("capital-source-001")
DONOR_ID          = foc_id("donor-001")
CLEARANCE_CAP_ID  = foc_id("cap-clearance-001")
ALLOC_AUTH_ID     = foc_id("alloc-auth-001")
ALLOC_ID          = foc_id("allocation-001")
SUFFICIENCY_REF   = foc_id("sufficiency-ref-001")
COUNCIL_AUTH_REF  = foc_id("council-auth-ref-001")

# Deployment / hub health
DEPLOY_AUTH_ID    = foc_id("deploy-auth-001")
DEPLOY_REQ_ID     = foc_id("deploy-request-001")
HEALTH_ASSESS_ID  = foc_id("hub-health-assess-001")
HUB_LEADER_ID     = foc_id("hub-leader-001")


# ---------------------------------------------------------------------------
# Main FOC runner
# ---------------------------------------------------------------------------

def run_foc():
    from config import PlatformConfig
    from main import FormationIntelligencePlatform
    from ic_payloads import (
        IC01Payload, IC02Payload, IC03Payload,
        IC04HoldPayload, IC04ClearPayload,
        IC05Payload,
        IC06GovernancePayload, IC06CapitalPayload,
        IC07Payload, IC08Payload,
        IC09Payload, IC10Payload,
        IC11Payload, IC12Payload,
        IC13Payload, IC14Payload,
    )

    section("FORMATION INTELLIGENCE PLATFORM — STEP 13 FIRST OPERATIONAL CYCLE (FOC)")

    # -----------------------------------------------------------------------
    # Platform boot
    # -----------------------------------------------------------------------
    phase("Platform Boot")
    config  = PlatformConfig()
    platform = FormationIntelligencePlatform(config)
    bus     = platform.ic_bus
    _make_capturing_logger(platform.logger)
    ok("FormationIntelligencePlatform initialized — all 6 clusters + ICBus ready")

    sig = SignalTrace()
    warnings: list[str] = []
    errors:   list[str] = []

    # -----------------------------------------------------------------------
    # PHASE A — Assessment & Profile Intake
    # IC-01: CLU-01.1 → CLU-01.1 (receive_assessment) + CLU-01.2 stub + CLU-01.5 stub
    # -----------------------------------------------------------------------
    phase("PHASE A: Fracture Assessment Intake  [IC-01]")
    note("Participant: FOC-001 | Facilitator: FAC-001 | Date: 2026-03-31")
    note("Domains assessed: Identity, Authority, Relational")

    ic01 = IC01Payload(
        participant_id       = PARTICIPANT_ID,
        intake_questionnaire_ref = QUESTIONNAIRE_REF,
        fracture_map_ref     = FRACTURE_MAP_REF,
        facilitator_id       = FACILITATOR_ID,
        assessment_date      = TODAY,
        facilitator_notes    = (
            "Participant exhibits primary fracture in Identity domain "
            "with secondary presentation in Authority. Spiritual formation "
            "baseline established. Recommended STAGE_1 entry."
        ),
    )
    try:
        bus.emit_ic_01(ic01)
        ok("IC-01 fired", "CLU-01.1 receive_assessment + CLU-01.2 stub + CLU-01.5 stub")
        sig.record(
            ic="IC-01",
            producer="CLU-01.1 (FractureAssessmentEngine)",
            consumers=["CLU-01.1 receive_assessment", "CLU-01.2 stub (StageProgressionLogic)", "CLU-01.5 stub (FormationPathwayRouter)"],
            payload_summary=f"participant_id={PARTICIPANT_ID} | assessment_date={TODAY} | facilitator={FACILITATOR_ID}",
        )
    except Exception as e:
        errors.append(f"IC-01: {e}")
        ok("IC-01", f"ERROR — {e}")

    # -----------------------------------------------------------------------
    # PHASE B — Fracture Profile Finalization & Pathway Assignment
    # IC-02: CLU-01.1 → CLU-01.5 (FormationPathwayRouter.receive_finalized_profile)
    # -----------------------------------------------------------------------
    phase("PHASE B: Fracture Profile Finalization & Pathway Assignment  [IC-02]")
    note("Finalized profile: Identity=L3, Authority=L2 | Entry stage: STAGE_1")

    ic02 = IC02Payload(
        fracture_profile_id     = FRACTURE_PROFILE_ID,
        participant_id          = PARTICIPANT_ID,
        active_domains          = ["Identity", "Authority", "Relational"],
        severity_per_domain     = {"Identity": "L3", "Authority": "L2", "Relational": "L1"},
        recommended_entry_stage = "STAGE_1",
        hub_id                  = HUB_ID,
        facilitator_id          = FACILITATOR_ID,
    )
    try:
        bus.emit_ic_02(ic02)
        ok("IC-02 fired", "CLU-01.5 receive_finalized_profile — fracture profile transferred to pathway router")
        sig.record(
            ic="IC-02",
            producer="CLU-01.1 (FractureAssessmentEngine — finalize_profile)",
            consumers=["CLU-01.5 (FormationPathwayRouter.receive_finalized_profile)"],
            payload_summary=f"fracture_profile_id={FRACTURE_PROFILE_ID} | domains=Identity/Authority/Relational | stage=STAGE_1",
        )
    except Exception as e:
        errors.append(f"IC-02: {e}")
        ok("IC-02", f"ERROR — {e}")

    # -----------------------------------------------------------------------
    # PHASE C — Theological Review of Formation Content
    # IC-07: CLU-01.1 → CLU-02.2 (TheologicalReviewEngine.receive_review_request)
    # -----------------------------------------------------------------------
    phase("PHASE C: Theological Review Request  [IC-07]")
    note("Formation narrative document submitted for theological review from CLU-01.1")

    ic07 = IC07Payload(
        requesting_module   = "CLU-01.1",
        content_type        = "Document",
        content_ref         = FORMATION_CONTENT_REF,
        asset_content_summary = (
            "Initial formation narrative for participant FOC-001. "
            "Covers Identity fracture pathway and Scriptural re-anchoring "
            "framework. Requires theological review before use in Stage 1 "
            "formation sessions."
        ),
        review_priority     = "Routine",
        submitted_date      = TODAY,
    )
    try:
        bus.emit_ic_07(ic07)
        ok("IC-07 fired", "CLU-02.2 receive_review_request — formation document queued for theological review")
        sig.record(
            ic="IC-07",
            producer="CLU-01.1 (FractureAssessmentEngine)",
            consumers=["CLU-02.2 (TheologicalReviewEngine.receive_review_request)"],
            payload_summary=f"content_ref={FORMATION_CONTENT_REF} | type=Document | priority=Routine",
        )
    except Exception as e:
        errors.append(f"IC-07: {e}")
        ok("IC-07", f"ERROR — {e}")

    # -----------------------------------------------------------------------
    # PHASE D — Language Compliance Clearance
    # IC-11: CLU-05.1 → All clusters (broadcast)
    # -----------------------------------------------------------------------
    phase("PHASE D: Language Compliance Clearance  [IC-11]")
    note("Formation content cleared by SemanticAuthorityEnforcer — Cleared status broadcast")

    ic11 = IC11Payload(
        clearance_id        = CLEARANCE_ID,
        content_ref         = FORMATION_CONTENT_REF,
        requesting_cluster  = "CLU-01",
        compliance_status   = "Cleared",
        flagged_terms       = [],
        disqualified_terms  = [],
        correction_guidance = "",
        clearance_date      = TODAY,
    )
    try:
        bus.emit_ic_11(ic11)
        ok("IC-11 fired", "Broadcast to 6 cluster stubs — compliance status=Cleared")
        sig.record(
            ic="IC-11",
            producer="CLU-05.1 (SemanticAuthorityEnforcer)",
            consumers=["CLU-01 stub", "CLU-02 stub", "CLU-03 stub", "CLU-04 stub", "CLU-05 stub", "CLU-06 stub"],
            payload_summary=f"clearance_id={CLEARANCE_ID} | content_ref={FORMATION_CONTENT_REF} | status=Cleared",
        )
    except Exception as e:
        errors.append(f"IC-11: {e}")
        ok("IC-11", f"ERROR — {e}")

    # -----------------------------------------------------------------------
    # PHASE E — Pathway-to-Hub Routing
    # IC-05: CLU-01.5 → CLU-04.1 + CLU-04.3 stub + CLU-04.4 stub
    # -----------------------------------------------------------------------
    phase("PHASE E: Pathway-to-Hub Routing  [IC-05]")
    note("Formation pathway assigned — participant routed to hub for Stage 1 formation sessions")

    ic05 = IC05Payload(
        pathway_id              = PATHWAY_ID,
        participant_id          = PARTICIPANT_ID,
        assigned_stage          = "STAGE_1",
        domain_sequence         = ["Identity", "Authority", "Relational"],
        hub_id                  = HUB_ID,
        session_type_requirements = ["individual", "cohort", "household"],
        facilitator_id          = FACILITATOR_ID,
    )
    try:
        bus.emit_ic_05(ic05)
        ok("IC-05 fired",
           "CLU-04.1 receive_pathway_routing + CLU-04.3 inline stub + CLU-04.4 stub")
        sig.record(
            ic="IC-05",
            producer="CLU-01.5 (FormationPathwayRouter.route_to_hub)",
            consumers=[
                "CLU-04.1 (HubFormationProtocol.receive_pathway_routing)",
                "CLU-04.3 stub (HouseholdRhythmScheduler — inline log)",
                "CLU-04.4 stub (HospitalityOperationsModule)",
            ],
            payload_summary=f"pathway_id={PATHWAY_ID} | hub_id={HUB_ID} | stage=STAGE_1 | sessions=individual/cohort/household",
        )
    except Exception as e:
        errors.append(f"IC-05: {e}")
        ok("IC-05", f"ERROR — {e}")

    # -----------------------------------------------------------------------
    # PHASE F — Milestone Progress Signal
    # IC-03: CLU-01.3 → CLU-01.2 (StageProgressionLogic.receive_milestone_signal)
    # -----------------------------------------------------------------------
    phase("PHASE F: Milestone Progress Check  [IC-03]")
    note("Milestone A completed — threshold check triggered for Stage 1 advancement")

    ic03 = IC03Payload(
        participant_id          = PARTICIPANT_ID,
        current_stage           = "STAGE_1",
        milestones_completed    = [MILESTONE_A],
        milestones_pending      = [MILESTONE_B, MILESTONE_C],
        facilitator_attestation_ids = [ATTESTATION],
        last_assessment_date    = TODAY,
        milestone_threshold_met = False,
        completion_percentage   = 33.3,
        evaluation_data         = {"cohort_session_count": 3, "individual_session_count": 2},
    )
    try:
        bus.emit_ic_03(ic03)
        ok("IC-03 fired", "CLU-01.2 receive_milestone_signal — 1/3 milestones complete, stage hold maintained")
        sig.record(
            ic="IC-03",
            producer="CLU-01.3 (MilestoneTrackingSystem.check_stage_threshold)",
            consumers=["CLU-01.2 (StageProgressionLogic.receive_milestone_signal)"],
            payload_summary=f"participant_id={PARTICIPANT_ID} | stage=STAGE_1 | completion=33.3% | threshold_met=False",
        )
    except Exception as e:
        errors.append(f"IC-03: {e}")
        ok("IC-03", f"ERROR — {e}")

    # -----------------------------------------------------------------------
    # PHASE G — Formation Record Feed (Governance + Capital)
    # IC-06 Governance: CLU-01.6 → CLU-02.1
    # IC-06 Capital:    CLU-01.6 → CLU-06.5 stub
    # -----------------------------------------------------------------------
    phase("PHASE G: Formation Record Feed  [IC-06 Governance + Capital]")
    note("Aggregate formation report dispatched to Governance and Capital clusters")

    ic06_gov = IC06GovernancePayload(
        report_id               = REPORT_ID,
        reporting_period_start  = YESTERDAY,
        reporting_period_end    = TODAY,
        authorization_ref       = AUTH_REF,
        total_participants      = 1,
        stage_distribution      = {"STAGE_1": 1},
        domain_prevalence       = {"Identity": 1, "Authority": 1, "Relational": 1},
        blockage_frequency      = {},
        milestone_completion_rate = 33.3,
    )
    ic06_cap = IC06CapitalPayload(
        report_id               = REPORT_ID,
        reporting_period_start  = YESTERDAY,
        reporting_period_end    = TODAY,
        authorization_ref       = AUTH_REF,
        participant_count       = 1,
        stage_completion_count  = {"STAGE_1": 0},
        program_utilization_rate = 33.3,
    )
    try:
        bus.emit_ic_06_governance(ic06_gov)
        ok("IC-06 Governance fired", "CLU-02.1 receive_formation_record_feed — governance aggregate report received")
        bus.emit_ic_06_capital(ic06_cap)
        ok("IC-06 Capital fired", "CLU-06.5 stub — anonymized capital report dispatched")
        sig.record(
            ic="IC-06 (Governance)",
            producer="CLU-01.6 (RestorationRecordKeeper)",
            consumers=["CLU-02.1 (GoverningAuthorityModule.receive_formation_record_feed)"],
            payload_summary=f"report_id={REPORT_ID} | total_participants=1 | stage=STAGE_1 | completion=33.3%",
        )
        sig.record(
            ic="IC-06 (Capital)",
            producer="CLU-01.6 (RestorationRecordKeeper)",
            consumers=["CLU-06.5 stub (CapitalReportingInterface)"],
            payload_summary=f"report_id={REPORT_ID} | participant_count=1 | utilization=33.3%",
        )
    except Exception as e:
        errors.append(f"IC-06: {e}")
        ok("IC-06", f"ERROR — {e}")

    # -----------------------------------------------------------------------
    # PHASE H — Council Ruling Propagation (Broadcast)
    # IC-08: CLU-02.1 → CLU-02.4 (direct) + all cluster stubs
    # -----------------------------------------------------------------------
    phase("PHASE H: Council Ruling Propagation  [IC-08 Broadcast]")
    note("Council issues FOC Directive — Stage 1 formation standards confirmed")

    ic08 = IC08Payload(
        ruling_id           = RULING_ID,
        ruling_type         = "Directive",
        affected_documents  = ["DOC-04.1", "DOC-04.2"],
        affected_clusters   = ["CLU-01", "CLU-02", "CLU-03", "CLU-04", "CLU-05", "CLU-06"],
        ruling_text         = (
            "DIRECTIVE: Stage 1 formation standards are confirmed operative "
            "for the First Operational Cycle. All clusters are to implement "
            "Stage 1 protocols in accordance with ICM-01 and DSR-01."
        ),
        scriptural_basis    = "Romans 12:2 — transformation by the renewing of the mind",
        effective_date      = TODAY,
        vote_record         = {"unanimous": True, "members_present": 5},
    )
    try:
        bus.emit_ic_08(ic08)
        ok("IC-08 fired", "Broadcast to CLU-02.4 (direct) + 5 cluster stubs — council directive propagated")
        sig.record(
            ic="IC-08",
            producer="CLU-02.1 (GoverningAuthorityModule.ratify_ruling)",
            consumers=[
                "CLU-02.4 (AmendmentRulingRegistry.receive_ruling_propagation) [type mismatch tracked]",
                "CLU-01 stub", "CLU-03 stub", "CLU-04 stub", "CLU-05 stub", "CLU-06 stub",
            ],
            payload_summary=f"ruling_id={RULING_ID} | type=Directive | affected=all clusters",
            notes="IC-08 CLU-02.4 type contract mismatch tracked (non-blocking, stub=pass). See IMP-02.",
        )
    except Exception as e:
        errors.append(f"IC-08: {e}")
        ok("IC-08", f"ERROR — {e}")

    # -----------------------------------------------------------------------
    # PHASE I — Hub Health Escalation
    # IC-13: CLU-04.6 → CLU-02.1 (GoverningAuthorityModule.receive_hub_health_escalation)
    # -----------------------------------------------------------------------
    phase("PHASE I: Hub Health Escalation  [IC-13]")
    note("Hub FOC-001 health assessment — first cycle baseline reading")

    ic13 = IC13Payload(
        health_assessment_id       = HEALTH_ASSESS_ID,
        hub_id                     = HUB_ID,
        health_score               = 72.5,
        consecutive_below_threshold = 0,
        risk_areas                 = [],
        hub_leader_id              = HUB_LEADER_ID,
        assessment_date            = TODAY,
    )
    try:
        bus.emit_ic_13(ic13)
        ok("IC-13 fired", "CLU-02.1 receive_hub_health_escalation — hub health baseline registered (score=72.5, no risks)")
        sig.record(
            ic="IC-13",
            producer="CLU-04.6 (HubHealthAssessmentModule)",
            consumers=["CLU-02.1 (GoverningAuthorityModule.receive_hub_health_escalation)"],
            payload_summary=f"hub_id={HUB_ID} | health_score=72.5 | consecutive_below_threshold=0 | risk_areas=none",
        )
    except Exception as e:
        errors.append(f"IC-13: {e}")
        ok("IC-13", f"ERROR — {e}")

    # -----------------------------------------------------------------------
    # PHASE J — Capital Source Integrity Clearance
    # IC-09: CLU-03.1 → CLU-03.2 + CLU-06.1
    # -----------------------------------------------------------------------
    phase("PHASE J: Capital Source Integrity Clearance  [IC-09]")
    note("Foundation donor cleared — enters giving pipeline and funding stream inventory")

    ic09 = IC09Payload(
        clearance_id    = CLEARANCE_CAP_ID,
        source_id       = SOURCE_ID,
        source_name     = "Covenant Partners Foundation",
        source_type     = "Foundation",
        integrity_status = "Cleared",
        clearance_date  = TODAY,
        expiry_date     = NEXT_YEAR,
        donor_id        = DONOR_ID,
        amount_category = "Medium",
        conditional_requirements = "",
    )
    try:
        bus.emit_ic_09(ic09)
        ok("IC-09 fired", "CLU-03.2 receive_approved_donor + CLU-06.1 receive_approved_source")
        sig.record(
            ic="IC-09",
            producer="CLU-03.1 (CapitalSourceIntegrityFilter.evaluate_source)",
            consumers=[
                "CLU-03.2 (GenerativeGivingEngine.receive_approved_donor)",
                "CLU-06.1 (FundingStreamManager.receive_approved_source)",
            ],
            payload_summary=f"source=Covenant Partners Foundation | type=Foundation | status=Cleared | amount=Medium",
        )
    except Exception as e:
        errors.append(f"IC-09: {e}")
        ok("IC-09", f"ERROR — {e}")

    # -----------------------------------------------------------------------
    # PHASE K — Fund Allocation Authorization
    # IC-10: CLU-03.5 → CLU-06.6
    # -----------------------------------------------------------------------
    phase("PHASE K: Fund Allocation Authorization  [IC-10]")
    note("Hub deployment funding allocated and authorized for disbursement")

    ic10 = IC10Payload(
        disbursement_authorization_id = ALLOC_AUTH_ID,
        allocation_id               = ALLOC_ID,
        allocation_type             = "Deployment",
        destination_id              = HUB_ID,
        council_authorization_ref   = COUNCIL_AUTH_REF,
        sufficiency_compliance_ref  = SUFFICIENCY_REF,
        effective_date              = TODAY,
        authorized_amount_category  = "Medium",
    )
    try:
        bus.emit_ic_10(ic10)
        ok("IC-10 fired", "CLU-06.6 receive_fund_allocation_authorization — deployment funding cleared")
        sig.record(
            ic="IC-10",
            producer="CLU-03.5 (FundAllocationLogic.authorize_deployment_funding)",
            consumers=["CLU-06.6 (DeploymentFundingLogic.receive_fund_allocation_authorization)"],
            payload_summary=f"allocation_type=Deployment | destination=hub | amount=Medium | effective={TODAY}",
        )
    except Exception as e:
        errors.append(f"IC-10: {e}")
        ok("IC-10", f"ERROR — {e}")

    # -----------------------------------------------------------------------
    # PHASE L — Lexicon Update Propagation
    # IC-12: CLU-05.2 → All clusters + CLU-05.3 on Disqualification
    # -----------------------------------------------------------------------
    phase("PHASE L: Lexicon Update Propagation  [IC-12]")
    note("New formation term 'fracture-domain' published to all clusters")

    ic12_new = IC12Payload(
        propagation_id   = LEXICON_PROP_ID,
        update_id        = LEXICON_UPDATE_ID,
        update_type      = "New-entry",
        term             = "fracture-domain",
        updated_entry_ref = LEXICON_ENTRY_REF,
        council_ruling_ref = RULING_REF,
        effective_date   = TODAY,
    )
    try:
        bus.emit_ic_12(ic12_new)
        ok("IC-12 fired (New-entry)", "Broadcast to 6 cluster stubs — 'fracture-domain' published")
        sig.record(
            ic="IC-12 (New-entry)",
            producer="CLU-05.2 (LexiconManagementSystem.publish_lexicon_update)",
            consumers=["CLU-01 stub", "CLU-02 stub", "CLU-03 stub", "CLU-04 stub", "CLU-05 stub", "CLU-06 stub"],
            payload_summary=f"term='fracture-domain' | update_type=New-entry | effective={TODAY}",
        )
    except Exception as e:
        errors.append(f"IC-12 (New-entry): {e}")
        ok("IC-12 (New-entry)", f"ERROR — {e}")

    # -----------------------------------------------------------------------
    # PHASE M — Deployment Funding Authorization
    # IC-14: CLU-06.6 → CLU-04.1
    # -----------------------------------------------------------------------
    phase("PHASE M: Deployment Funding Authorization  [IC-14]")
    note("Hub deployment budget authorized — hub formation protocol may proceed")

    ic14 = IC14Payload(
        funding_authorization_id  = DEPLOY_AUTH_ID,
        deployment_request_id     = DEPLOY_REQ_ID,
        hub_id                    = HUB_ID,
        authorized_amount_category = "Medium",
        funding_status            = "Authorized",
        deployment_template_ref   = "TMPL-HUB-STAGE1-V1",
        council_authorization_ref = COUNCIL_AUTH_REF,
        authorization_date        = TODAY,
        expiry_date               = NEXT_YEAR,
        contingency_conditions    = "",
        denial_basis              = "",
    )
    try:
        bus.emit_ic_14(ic14)
        ok("IC-14 fired", "CLU-04.1 receive_deployment_funding_authorization — hub cleared for Stage 1 formation")
        sig.record(
            ic="IC-14",
            producer="CLU-06.6 (DeploymentFundingLogic.authorize_deployment_budget)",
            consumers=["CLU-04.1 (HubFormationProtocol.receive_deployment_funding_authorization)"],
            payload_summary=f"hub_id={HUB_ID} | status=Authorized | amount=Medium | expiry={NEXT_YEAR}",
        )
    except Exception as e:
        errors.append(f"IC-14: {e}")
        ok("IC-14", f"ERROR — {e}")

    # -----------------------------------------------------------------------
    # PHASE N — Final output coherence check
    # Verify the system returns without exception across the full chain
    # -----------------------------------------------------------------------
    phase("PHASE N: Final Output Coherence Check")
    ic_count  = len(sig.events)
    log_count = len(_foc_log)
    err_count = len(errors)

    ok(f"Total ICs activated: {ic_count}")
    ok(f"Total log lines emitted: {log_count}")
    if err_count == 0:
        ok("Exception check: CLEAN — no runtime exceptions across full chain")
    else:
        for err in errors:
            warn(f"Exception: {err}")

    # -----------------------------------------------------------------------
    # STEP 13 FOC REPORT
    # -----------------------------------------------------------------------
    section("STEP 13 FOC REPORT — Signal Trace")

    print(f"\n  {'IC':<22} {'Producer':<45} Status")
    print(f"  {'─'*22} {'─'*45} {'─'*6}")
    for ev in sig.events:
        status = "OK" if ev["status"] == "OK" else "WARN"
        print(f"  {ev['ic']:<22} {ev['producer'][:45]:<45} {status}")

    print()
    print("  IC Activation Order:")
    for i, ic in enumerate(sig.activation_order(), 1):
        print(f"    {i:>2}. {ic}")

    print()
    print("  Signal Trace — Cluster-by-Cluster:")
    for ev in sig.events:
        print(f"\n  [{ev['ic']}]")
        print(f"    Producer : {ev['producer']}")
        for c in ev["consumers"]:
            print(f"    Consumer : {c}")
        print(f"    Payload  : {ev['payload_summary']}")
        if ev["notes"]:
            print(f"    Note     : {ev['notes']}")

    section("STEP 13 FOC REPORT — Summary")

    print(f"\n  ICs activated   : {ic_count} / 13 pathways traced")
    print(f"  Log lines emitted: {log_count}")
    print(f"  Runtime errors  : {err_count}")

    print("\n  STANDING ISSUES (carried from STEP 12, non-blocking):")
    standing = [
        "IMP-01  platform_logger.py:53 — datetime.utcnow() deprecated; replace with datetime.now(datetime.UTC)",
        "IMP-02  IC-08 → CLU-02.4 type contract (IC08Payload vs RulingPropagationRecord) — resolve at CLU-02.4 implementation",
        "IMP-03  CLU-04.3 HouseholdRhythmScheduler.receive_participant_routing() missing — inline stub active",
        "IMP-04  CLU-06.5 CapitalReportingInterface.receive_formation_record_feed() missing — ic_06_capital_stub active",
        "IMP-05  CLU-05.3 LanguageAuditModule.receive_disqualification_trigger() missing — inline stub active",
    ]
    for s in standing:
        print(f"    {s}")

    print("\n  IC-04 NOTE: Blockage signal not triggered in FOC-001. Participant")
    print("  record is clean — no blockage at Stage 1 entry. IC-04 hold/clear")
    print("  pathway will be exercised at first milestone stall detection.")

    print()
    if err_count == 0:
        print("  ╔══════════════════════════════════════════════════════════════╗")
        print("  ║  FOC STATUS: COMPLETE — ALL SYSTEMS NOMINAL                 ║")
        print("  ║  READY FOR STEP 14 — CALIBRATION & TUNING                  ║")
        print("  ╚══════════════════════════════════════════════════════════════╝")
    else:
        print("  ╔══════════════════════════════════════════════════════════════╗")
        print("  ║  FOC STATUS: COMPLETED WITH ERRORS                          ║")
        print("  ║  RESOLVE ERRORS BEFORE STEP 14                              ║")
        print("  ╚══════════════════════════════════════════════════════════════╝")
    print()


if __name__ == "__main__":
    run_foc()
