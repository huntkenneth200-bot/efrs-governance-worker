"""
FORMATION INTELLIGENCE PLATFORM
OBJ-06 — Formation Pathway Assignment
OBJ-07 — Milestone Completion Record
OBJ-08 — Stage Progression Evaluation
OBJ-10 — Hub Routing Record
OBJ-12 — Aggregate Formation Report
OBJ-13 — Theological Review Record

Schema authority: DATA-SCHEMA-REGISTRY.md (DSR-01)
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from .enumerations import (
    FormationStage, FractureDomain, PathwayStatus, MilestoneStatus,
    RoutingStatus, ClearanceStatus, ContentType, ReviewPriority
)


@dataclass
class FormationPathwayAssignment:
    """OBJ-06 — Active formation pathway for one participant. See DSR-01 OBJ-06."""
    pathway_id: UUID = field(default_factory=uuid4)
    assignment_date: date = field(default_factory=date.today)
    last_modified_date: date = field(default_factory=date.today)
    participant_id: Optional[UUID] = None
    fracture_profile_id: Optional[UUID] = None  # Must be Finalized (VR-06-01)
    assigned_stage: Optional[FormationStage] = None
    domain_sequence: list[FractureDomain] = field(default_factory=list)
    assigned_facilitator_id: Optional[UUID] = None
    hub_id: Optional[UUID] = None               # Must be Active hub (VR-06-03)
    hub_session_refs: list[str] = field(default_factory=list)
    pathway_status: PathwayStatus = PathwayStatus.DRAFT
    modification_trigger: Optional[str] = None  # Required on update (VR-06-08)
    pathway_notes: Optional[str] = None


@dataclass
class MilestoneCompletionRecord:
    """OBJ-07 — Single formation milestone completion record. See DSR-01 OBJ-07."""
    milestone_record_id: UUID = field(default_factory=uuid4)
    created_date: date = field(default_factory=date.today)
    last_modified_date: date = field(default_factory=date.today)
    participant_id: Optional[UUID] = None
    milestone_ref: Optional[str] = None        # Must resolve to active DOC-03.4 entry (VR-07-02)
    stage: Optional[FormationStage] = None
    domain: Optional[FractureDomain] = None
    completion_status: MilestoneStatus = MilestoneStatus.PENDING
    facilitator_attestation_id: Optional[UUID] = None  # Required for Complete (VR-07-01)
    attestation_date: Optional[date] = None
    assessment_ref: Optional[UUID] = None
    overdue_flag: bool = False                  # System-calculated — not manually set (VR-07-04)


@dataclass
class StageProgressionEvaluation:
    """OBJ-08 — Stage advancement eligibility evaluation. See DSR-01 OBJ-08."""
    evaluation_id: UUID = field(default_factory=uuid4)
    evaluation_date: date = field(default_factory=date.today)
    advancement_date: Optional[date] = None
    participant_id: Optional[UUID] = None
    current_stage: Optional[FormationStage] = None
    milestone_threshold_met: bool = False
    completion_percentage: float = 0.0          # System-calculated (VR-08-03)
    outstanding_milestones: list[UUID] = field(default_factory=list)
    active_blockage_id: Optional[UUID] = None
    advancement_eligible: bool = False          # False while any active blockage (VR-08-01)
    facilitator_assessment_submitted: bool = False  # Required for Stage 4→5 (VR-08-04)
    facilitator_assessment_ref: Optional[str] = None
    advancement_authorized: bool = False        # Human-set — never system-automated (VR-08-05)


@dataclass
class HubRoutingRecord:
    """OBJ-10 — Hub routing assignment for a participant. See DSR-01 OBJ-10."""
    routing_record_id: UUID = field(default_factory=uuid4)
    routing_date: date = field(default_factory=date.today)
    last_modified_date: date = field(default_factory=date.today)
    participant_id: Optional[UUID] = None
    pathway_id: Optional[UUID] = None
    hub_id: Optional[UUID] = None
    session_schedule_ref: Optional[str] = None
    hospitality_assignment_ref: Optional[str] = None
    routing_status: RoutingStatus = RoutingStatus.PENDING_CAPACITY
    hub_leader_notified: bool = False           # Must be True before routing complete (VR-10-03)
    cross_hub_notification_sent: bool = False   # Required when Cross-hub (VR-10-04)


@dataclass
class AggregateFormationReport:
    """OBJ-12 — Anonymized aggregate formation report. See DSR-01 OBJ-12. No individual identifiers."""
    report_id: UUID = field(default_factory=uuid4)
    generated_date: date = field(default_factory=date.today)
    report_type: str = "GOVERNANCE"         # GOVERNANCE / CAPITAL
    requesting_module: Optional[str] = None # Must be CLU-02.1 or CLU-06.5 (VR-12-04)
    authorization_ref: Optional[str] = None # Required (VR-12-01)
    reporting_period_start: Optional[date] = None
    reporting_period_end: Optional[date] = None
    total_participants: int = 0
    stage_distribution: dict = field(default_factory=dict)
    domain_prevalence: dict = field(default_factory=dict)   # Governance only (VR-12-02)
    blockage_frequency: dict = field(default_factory=dict)  # Governance only
    milestone_completion_rate: float = 0.0
    stage_completion_count: dict = field(default_factory=dict)  # Capital only
    program_utilization_rate: float = 0.0                       # Capital only


@dataclass
class TheologicalReviewRecord:
    """OBJ-13 — Theological review request and outcome. See DSR-01 OBJ-13."""
    review_id: UUID = field(default_factory=uuid4)
    submitted_date: date = field(default_factory=date.today)
    review_date: Optional[date] = None
    review_request_id: Optional[str] = None
    requesting_module: Optional[str] = None
    content_type: Optional[ContentType] = None
    content_ref: Optional[str] = None
    review_priority: ReviewPriority = ReviewPriority.ROUTINE
    clearance_status: Optional[ClearanceStatus] = None
    theological_rationale: str = ""             # Required for ALL outcomes (VR-13-01)
    conditional_requirements: list[str] = field(default_factory=list)
    conditional_resolved: bool = False
    disqualification_basis: Optional[str] = None   # Required if Disqualified (VR-13-02)
    reviewer_id: Optional[UUID] = None             # Must be Active Council member (VR-13-04)
    registry_entry_ref: Optional[str] = None       # CLU-02.4 reference if disqualification
