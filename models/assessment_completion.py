"""
FORMATION INTELLIGENCE PLATFORM
OBJ-26 — Assessment Completion Record
OBJ-27 — Covenant Member Record

Schema authority: DATA-SCHEMA-REGISTRY.md (DSR-01 / OBJ-26, OBJ-27)
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from .enumerations import AssessmentInstrumentType, FormationStage, CovenantStatus


@dataclass
class AssessmentCompletionRecord:
    """
    OBJ-26 — Completion record for a single assessment instrument.
    facilitator_verified must be True before feeding into OBJ-05 or OBJ-07 (VR-26-01).

    Constraints:
    - Partial may not finalize OBJ-05 (VR-26-02)
    - Voided requires voided_reason (VR-26-03)
    - DOC_04_3 must be completed within required interval (VR-26-04)
    """

    assessment_completion_id: UUID = field(default_factory=uuid4)
    created_date: date = field(default_factory=date.today)
    completion_date: Optional[date] = None

    participant_id: Optional[UUID] = None
    facilitator_id: Optional[UUID] = None
    instrument_type: Optional[AssessmentInstrumentType] = None
    instrument_ref: Optional[str] = None    # Reference to specific instrument document

    completion_status: str = "PARTIAL"      # COMPLETE / PARTIAL / VOIDED
    current_stage_at_completion: Optional[FormationStage] = None
    facilitator_verified: bool = False      # Required before feeding downstream (VR-26-01)
    voided_reason: Optional[str] = None     # Required if VOIDED (VR-26-03)


@dataclass
class CovenantMemberRecord:
    """
    OBJ-27 — Covenant membership status within an Emmaus Road hub community.
    Release documentation required regardless of release_type (VR-27-03).

    Constraints:
    - covenant_ref must reference valid covenant document (VR-27-01)
    - renewal_due_date must be future-dated on creation (VR-27-02)
    - release_documentation required on release (VR-27-03)
    - Under-review requires active accountability_action_ref (VR-27-04)
    """

    covenant_member_id: UUID = field(default_factory=uuid4)

    participant_id: Optional[UUID] = None
    hub_id: Optional[UUID] = None
    covenant_ref: Optional[str] = None          # Required (VR-27-01)

    covenant_status: CovenantStatus = CovenantStatus.ACTIVE
    covenant_start_date: Optional[date] = None
    last_renewal_date: Optional[date] = None
    renewal_due_date: Optional[date] = None     # Must be future-dated on creation (VR-27-02)

    accountability_action_refs: list[str] = field(default_factory=list)
    breach_record_refs: list[str] = field(default_factory=list)

    release_date: Optional[date] = None
    release_type: Optional[str] = None          # Voluntary / Facilitated / Required
    release_documentation: Optional[str] = None  # Required on release (VR-27-03)
