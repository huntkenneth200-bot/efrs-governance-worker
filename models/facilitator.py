"""
FORMATION INTELLIGENCE PLATFORM
OBJ-02 — Facilitator Record

Schema authority: DATA-SCHEMA-REGISTRY.md (DSR-01 / OBJ-02)
Owning cluster: CLU-02 — Council of Metanoia
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from .enumerations import FacilitatorCertificationStatus, MemberStandingStatus


@dataclass
class FacilitatorRecord:
    """
    Identity and operational record for every platform-certified facilitator.

    Constraints:
    - certification_status must be Certified before assigned to participants (VR-02-02)
    - active_participant count may not exceed max_caseload (VR-02-03)
    - Revoked status triggers reassignment of all active participants (VR-02-05)
    - Records are permanent — status changes only
    """

    # System-generated
    facilitator_id: UUID = field(default_factory=uuid4)
    created_date: date = field(default_factory=date.today)

    # Identity
    first_name: str = ""
    last_name: str = ""

    # Assignment
    hub_id: Optional[UUID] = None       # Primary hub assignment — must be Active (VR-02-07)

    # Certification — governed by DOC-06.1 orientation completion
    certification_status: FacilitatorCertificationStatus = FacilitatorCertificationStatus.PROVISIONAL
    certification_date: Optional[date] = None
    certification_ref: Optional[str] = None     # DOC-06.1 completion record reference

    # Caseload
    active_participant_ids: list[UUID] = field(default_factory=list)
    max_caseload: int = 0       # TODO: Council-defined per facilitator

    # Standing — governed by CLU-02.5
    standing_status: MemberStandingStatus = MemberStandingStatus.ACTIVE
    covenant_ref: Optional[str] = None     # Must reference current, signed covenant (VR-02-04)

    def validate(self) -> list[str]:
        """
        Run all VR-02 validation rules.
        Returns list of error codes for any violations.
        TODO: Implement per VR-02-01 through VR-02-07.
        """
        # TODO: VR-02-01 — unique facilitator_id
        # TODO: VR-02-02 — certification_status = Certified before participant assignment
        # TODO: VR-02-03 — caseload not exceeded
        # TODO: VR-02-04 — covenant_ref present and current
        # TODO: VR-02-05 — Revoked triggers reassignment
        # TODO: VR-02-06 — certification_ref references completed DOC-06.1
        # TODO: VR-02-07 — hub_id references Active hub
        errors = []
        return errors

    def is_eligible_for_assignment(self) -> bool:
        """
        Returns True only if facilitator may receive new participant assignments.
        Requires: Certified status, Active standing, caseload not full.
        TODO: Implement eligibility check.
        """
        # TODO: Check certification_status == CERTIFIED
        # TODO: Check standing_status == ACTIVE
        # TODO: Check len(active_participant_ids) < max_caseload
        pass

    def trigger_reassignment(self):
        """
        Called when facilitator standing changes to Suspended or Revoked.
        Initiates participant reassignment through CLU-01.5.
        TODO: Implement reassignment trigger — route to CLU-01.5 Formation Pathway Router.
        """
        # TODO: For each participant in active_participant_ids, trigger pathway reassignment
        pass
