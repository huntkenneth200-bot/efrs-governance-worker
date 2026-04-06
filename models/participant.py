"""
FORMATION INTELLIGENCE PLATFORM
OBJ-01 — Participant Record

Schema authority: DATA-SCHEMA-REGISTRY.md (DSR-01 / OBJ-01)
Owning cluster: CLU-01.6 — Restoration Record Keeper
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from .enumerations import FormationStage, ParticipantStatus


@dataclass
class ParticipantRecord:
    """
    Root identity record for every individual in the formation platform.
    All other participant-related objects reference this record.

    Constraints:
    - Records may not be deleted — status changes only (VR-01)
    - Access restricted to assigned facilitator, Hub Leader, Council (aggregate only)
    - consent_record_ref must be populated before status may be Active
    """

    # System-generated
    participant_id: UUID = field(default_factory=uuid4)
    created_date: date = field(default_factory=date.today)
    last_modified_date: date = field(default_factory=date.today)

    # Identity
    first_name: str = ""
    last_name: str = ""

    # Assignments — validated on creation (VR-01-02, VR-01-03)
    hub_id: Optional[UUID] = None           # Must reference Active or Forming hub
    facilitator_id: Optional[UUID] = None   # Must reference Certified, Active facilitator

    # Formation state
    current_stage: FormationStage = FormationStage.STAGE_1
    record_status: ParticipantStatus = ParticipantStatus.ACTIVE

    # Consent — required before Active status (VR-01-06)
    intake_date: Optional[date] = None
    consent_record_ref: Optional[str] = None

    # Narrative — facilitator only, confidential
    notes: Optional[str] = None

    def validate(self) -> list[str]:
        """
        Run all VR-01 validation rules.
        Returns list of error codes for any violations.
        TODO: Implement validation logic per VR-01-01 through VR-01-08.
        """
        # TODO: VR-01-01 — participant_id uniqueness (enforced at storage layer)
        # TODO: VR-01-02 — hub_id references Active or Forming hub
        # TODO: VR-01-03 — facilitator_id references Certified, Active facilitator
        # TODO: VR-01-04 — intake_date on or before created_date
        # TODO: VR-01-05 — current_stage is valid FormationStage value
        # TODO: VR-01-06 — consent_record_ref present before Active status
        # TODO: VR-01-07 — status transition rules enforced
        # TODO: VR-01-08 — no required field null
        errors = []
        return errors

    def can_advance_status(self, new_status: ParticipantStatus) -> bool:
        """
        Validate status transition rules (VR-01-07).
        Permitted: Active → Inactive, Active → Transferred, Active → Completed.
        TODO: Implement transition matrix.
        """
        # TODO: Implement transition validation
        pass

    def to_anonymized(self) -> dict:
        """
        Return anonymized representation for aggregate reporting (IC-06).
        No identifying fields included.
        TODO: Implement anonymization — current_stage only, no name/ID.
        """
        # TODO: Return only non-identifying fields for OBJ-12 aggregate
        pass
