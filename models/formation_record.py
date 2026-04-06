"""
FORMATION INTELLIGENCE PLATFORM
OBJ-11 — Formation Record

Schema authority: DATA-SCHEMA-REGISTRY.md (DSR-01 / OBJ-11)
Owning cluster: CLU-01.6 — Restoration Record Keeper
Interface: IC-06 (Formation Record Feed → CLU-02.1, CLU-06.5)
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class StageTransitionEntry:
    """Single entry in the stage transition audit log."""
    from_stage: str = ""
    to_stage: str = ""
    transition_date: date = field(default_factory=date.today)
    facilitator_id: Optional[UUID] = None
    notes: Optional[str] = None


@dataclass
class FormationRecord:
    """
    Permanent, comprehensive formation record for one participant.
    Aggregates all formation activity. One record per participant — permanent.

    Constraints:
    - Exactly one formation record per participant_id (VR-11-01)
    - Stage transition log entries must include date, from/to stage, facilitator_id (VR-11-02)
    - stage_5_completion_ref requires all Stage 5 milestones Complete (VR-11-03)
    - Amendments append with audit trail — no field overwrite (VR-11-04)
    - No individual identifiers in any output to CLU-06 (VR-11-05)
    """

    # System-generated
    formation_record_id: UUID = field(default_factory=uuid4)
    created_date: date = field(default_factory=date.today)
    last_modified_date: date = field(default_factory=date.today)

    # Ownership — 1:1 with participant
    participant_id: Optional[UUID] = None

    # Formation history — all records aggregated here
    fracture_profile_history: list[UUID] = field(default_factory=list)     # OBJ-05 refs
    pathway_history: list[UUID] = field(default_factory=list)              # OBJ-06 refs
    milestone_history: list[UUID] = field(default_factory=list)            # OBJ-07 refs
    blockage_history: list[UUID] = field(default_factory=list)             # OBJ-09 refs
    assessment_history: list[UUID] = field(default_factory=list)           # OBJ-26 refs

    # Stage transition audit log — permanent, append-only
    stage_transition_log: list[StageTransitionEntry] = field(default_factory=list)

    # Completion
    stage_5_completion_ref: Optional[str] = None   # Populated on Stage 5 milestone attestation

    # Session notes — facilitator only
    facilitator_session_notes: list[dict] = field(default_factory=list)

    def append_stage_transition(self, from_stage: str, to_stage: str, facilitator_id: UUID, notes: Optional[str] = None):
        """
        Append a stage transition entry to the audit log.
        Called by CLU-01.2 on every stage advancement or regression.
        TODO: Create StageTransitionEntry; append to log; update last_modified_date.
        """
        # TODO: Validate from_stage and to_stage are valid FormationStage values
        # TODO: Create StageTransitionEntry with all required fields
        # TODO: Append to stage_transition_log
        # TODO: Update last_modified_date
        # TODO: Log INFO event
        pass

    def get_governance_report_data(self, reporting_period_start: date, reporting_period_end: date) -> dict:
        """
        Returns anonymized governance report fields for OBJ-12 (IC-06).
        NO individual identifiers in output.
        TODO: Aggregate stage, domain, blockage, and milestone data — anonymized only.
        """
        # TODO: Filter records to reporting period
        # TODO: Return only: stage (enum value), domain counts, blockage type counts
        # TODO: No participant_id, facilitator_id, or hub_id in output
        pass

    def get_capital_report_data(self, reporting_period_start: date, reporting_period_end: date) -> dict:
        """
        Returns minimally anonymized capital report fields for OBJ-12 (IC-06, Capital type).
        Restricted to: stage completion indicator only.
        No domain, severity, or blockage data.
        TODO: Return only stage_completion indicator and utilization — fully anonymized.
        """
        # TODO: Return only permitted capital report fields (VR-12-02)
        # TODO: No domain_prevalence, no blockage_frequency in this output
        pass

    def amend(self, field_name: str, new_value, amended_by: UUID, reason: str):
        """
        Append-only amendment. Prior value is retained in audit trail.
        No field is ever overwritten without logging the prior value (VR-11-04).
        TODO: Implement append-only amendment pattern.
        """
        # TODO: Record prior value in amendment audit entry
        # TODO: Apply new value to field
        # TODO: Update last_modified_date
        # TODO: Log CRITICAL amendment event
        pass
