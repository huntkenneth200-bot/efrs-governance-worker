"""
FORMATION INTELLIGENCE PLATFORM
IC Payload Schemas

Dataclass definitions for all 14 Interface Contract payloads.
Each dataclass reflects the Input Schema defined in INTERFACE-CONTRACT-MATRIX (ICM-01).

Authority: ICM-01
Version: 1.0
Status: WIRED — Step 10 IC Integration

No payload class may be amended without a corresponding ICM-01 amendment
under Council ruling (DOC-01.2).
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import date


# ---------------------------------------------------------------------------
# IC-01 — Assessment-to-Fracture Profile
# Producer: CLU-01.1 | Consumers: CLU-01.2, CLU-01.5
# ---------------------------------------------------------------------------

@dataclass
class IC01Payload:
    """Input to FractureAssessmentEngine.receive_assessment()."""
    participant_id: UUID
    intake_questionnaire_ref: UUID          # DOC-04.1 completion record
    fracture_map_ref: UUID                  # DOC-04.2 completion record
    facilitator_id: UUID
    assessment_date: date
    facilitator_notes: str = ""


# ---------------------------------------------------------------------------
# IC-02 — Fracture Profile-to-Pathway Assignment
# Producer: CLU-01.1 (finalized profile) | Consumer: CLU-01.5
# ---------------------------------------------------------------------------

@dataclass
class IC02Payload:
    """Output of FractureAssessmentEngine.finalize_profile(); input to FormationPathwayRouter."""
    fracture_profile_id: UUID
    participant_id: UUID
    active_domains: List[str]               # e.g. ["Identity", "Authority"]
    severity_per_domain: Dict[str, str]     # e.g. {"Identity": "L2"}
    recommended_entry_stage: str            # e.g. "STAGE_1"
    hub_id: UUID
    facilitator_id: UUID


# ---------------------------------------------------------------------------
# IC-03 — Milestone-to-Stage Progression
# Producer: CLU-01.3 | Consumer: CLU-01.2
# ---------------------------------------------------------------------------

@dataclass
class IC03Payload:
    """Output of MilestoneTrackingSystem.check_stage_threshold(); input to StageProgressionLogic."""
    participant_id: UUID
    current_stage: str
    milestones_completed: List[UUID]
    milestones_pending: List[UUID]
    facilitator_attestation_ids: List[UUID]
    last_assessment_date: date
    milestone_threshold_met: bool
    completion_percentage: float
    evaluation_data: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# IC-04 — Blockage-to-Stage Hold  (hold signal and clear signal share this module)
# Producer: CLU-01.4 | Consumer: CLU-01.2
# ---------------------------------------------------------------------------

@dataclass
class IC04HoldPayload:
    """Emitted by BlockageDetectionModule on blockage creation."""
    participant_id: UUID
    blockage_id: UUID
    blockage_type: str                      # Formation / Relational / Spiritual / External
    blockage_severity: str                  # Moderate / Significant / Critical
    detection_trigger: str                  # Milestone-stall / Time-in-stage / Facilitator-submitted / Assessment-flag
    facilitator_id: UUID
    detection_date: date
    escalation_required: bool = False


@dataclass
class IC04ClearPayload:
    """Emitted by BlockageDetectionModule.resolve_blockage()."""
    participant_id: UUID
    blockage_id: UUID
    resolved_by: UUID
    resolution_date: date
    resolution_documentation: str


# ---------------------------------------------------------------------------
# IC-05 — Pathway-to-Hub Routing
# Producer: CLU-01.5 | Consumers: CLU-04.1, CLU-04.3
# ---------------------------------------------------------------------------

@dataclass
class IC05Payload:
    """Emitted by FormationPathwayRouter.route_to_hub()."""
    pathway_id: UUID
    participant_id: UUID
    assigned_stage: str
    domain_sequence: List[str]
    hub_id: UUID
    session_type_requirements: List[str]
    facilitator_id: UUID


# ---------------------------------------------------------------------------
# IC-06 — Formation Record Feed
# Producer: CLU-01.6 | Consumers: CLU-02.1 (governance), CLU-06.5 (capital)
# ---------------------------------------------------------------------------

@dataclass
class IC06GovernancePayload:
    """AggregateFormationReport routed to CLU-02.1."""
    report_id: UUID
    reporting_period_start: date
    reporting_period_end: date
    authorization_ref: UUID
    total_participants: int
    stage_distribution: Dict[str, int]
    domain_prevalence: Dict[str, int]
    blockage_frequency: Dict[str, int]
    milestone_completion_rate: float


@dataclass
class IC06CapitalPayload:
    """Anonymized AggregateFormationReport routed to CLU-06.5."""
    report_id: UUID
    reporting_period_start: date
    reporting_period_end: date
    authorization_ref: UUID
    participant_count: int
    stage_completion_count: Dict[str, int]
    program_utilization_rate: float


# ---------------------------------------------------------------------------
# IC-07 — Theological Review Request
# Producer: Any cluster | Consumer: CLU-02.2
# ---------------------------------------------------------------------------

@dataclass
class IC07Payload:
    """Emitted by any cluster; received by TheologicalReviewEngine.receive_review_request()."""
    requesting_module: str                  # e.g. "CLU-03.1"
    content_type: str                       # Document / Language / Practice / External-content / Lexicon-entry
    content_ref: UUID
    asset_content_summary: str
    review_priority: str = "Routine"        # Routine / Urgent
    submitted_date: Optional[date] = None


# ---------------------------------------------------------------------------
# IC-08 — Council Ruling Propagation  (broadcast)
# Producer: CLU-02.1 | Consumers: CLU-02.4 + all clusters
# ---------------------------------------------------------------------------

@dataclass
class IC08Payload:
    """Emitted by GoverningAuthorityModule.ratify_ruling() / issue_governance_directive()."""
    ruling_id: UUID
    ruling_type: str                        # Amendment / Directive / Disqualification / Doctrinal-position
    affected_documents: List[str]
    affected_clusters: List[str]
    ruling_text: str
    scriptural_basis: str
    effective_date: date
    vote_record: Dict[str, Any]
    propagation_record: Any = None          # RulingPropagationRecord — set by bus before dispatch


# ---------------------------------------------------------------------------
# IC-09 — Capital Source Integrity Clearance
# Producer: CLU-03.1 | Consumers: CLU-03.2, CLU-06.1
# ---------------------------------------------------------------------------

@dataclass
class IC09Payload:
    """Emitted by CapitalSourceIntegrityFilter.evaluate_source() on Approved/Conditional."""
    clearance_id: UUID
    source_id: UUID
    source_name: str
    source_type: str                        # Individual-donor / Foundation / Grant / Corporate / Other
    integrity_status: str                   # Cleared / Conditional
    clearance_date: date
    expiry_date: date
    donor_id: Optional[UUID] = None         # Populated if source is an individual donor
    amount_category: str = ""
    conditional_requirements: str = ""


# ---------------------------------------------------------------------------
# IC-10 — Fund Allocation Authorization
# Producer: CLU-03.5 | Consumer: CLU-06.6
# ---------------------------------------------------------------------------

@dataclass
class IC10Payload:
    """Emitted by FundAllocationLogic.authorize_deployment_funding()."""
    disbursement_authorization_id: UUID
    allocation_id: UUID
    allocation_type: str                    # Deployment / Operations / Training / Reserve
    destination_id: UUID                    # Hub or operational unit ID
    council_authorization_ref: UUID
    sufficiency_compliance_ref: UUID
    effective_date: date
    authorized_amount_category: str


# ---------------------------------------------------------------------------
# IC-11 — Language Compliance Clearance  (broadcast)
# Producer: CLU-05.1 | Consumers: all document-producing modules
# ---------------------------------------------------------------------------

@dataclass
class IC11Payload:
    """Emitted by SemanticAuthorityEnforcer.issue_compliance_clearance()."""
    clearance_id: UUID
    content_ref: UUID
    requesting_cluster: str
    compliance_status: str                  # Cleared / Flagged / Disqualified
    flagged_terms: List[str] = field(default_factory=list)
    disqualified_terms: List[str] = field(default_factory=list)
    correction_guidance: str = ""
    clearance_date: Optional[date] = None


# ---------------------------------------------------------------------------
# IC-12 — Lexicon Update Propagation  (broadcast)
# Producer: CLU-05.2 | Consumers: all clusters + CLU-05.3 on disqualification
# ---------------------------------------------------------------------------

@dataclass
class IC12Payload:
    """Emitted by LexiconManagementSystem.publish_lexicon_update()."""
    propagation_id: UUID
    update_id: UUID
    update_type: str                        # New-entry / Amendment / Disqualification
    term: str
    updated_entry_ref: UUID
    council_ruling_ref: UUID
    effective_date: date


# ---------------------------------------------------------------------------
# IC-13 — Hub Health Escalation
# Producer: CLU-04.6 | Consumer: CLU-02.1
# ---------------------------------------------------------------------------

@dataclass
class IC13Payload:
    """Emitted by HubHealthAssessmentModule.emit_hub_health_escalation()."""
    health_assessment_id: UUID
    hub_id: UUID
    health_score: float
    consecutive_below_threshold: int
    risk_areas: List[str]
    hub_leader_id: UUID
    assessment_date: date


# ---------------------------------------------------------------------------
# IC-14 — Deployment Funding Authorization
# Producer: CLU-06.6 | Consumer: CLU-04.1
# ---------------------------------------------------------------------------

@dataclass
class IC14Payload:
    """Emitted by DeploymentFundingLogic.authorize_deployment_budget()."""
    funding_authorization_id: UUID
    deployment_request_id: UUID
    hub_id: UUID
    authorized_amount_category: str
    funding_status: str                     # Authorized / Contingent / Denied
    deployment_template_ref: str
    council_authorization_ref: UUID
    authorization_date: date
    expiry_date: date
    contingency_conditions: str = ""
    denial_basis: str = ""
