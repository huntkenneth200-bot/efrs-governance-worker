"""
FORMATION INTELLIGENCE PLATFORM
OBJ-04 — Council Member Record

Schema authority: DATA-SCHEMA-REGISTRY.md (DSR-01 / OBJ-04)
Owning cluster: CLU-02.5 — Member Accountability Module
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from .enumerations import MemberStandingStatus


@dataclass
class CouncilMemberRecord:
    """
    Identity, standing, and accountability record for every Council member.

    Constraints:
    - Disqualification is immediate — no grace period (VR-04-03)
    - Suspended members excluded from vote counts and quorum (VR-04-04)
    - disqualification_record_ref required if Disqualified (VR-04-05)
    - Under-review requires active accountability record (VR-04-06)
    - Records are permanent — status changes only
    """

    member_id: UUID = field(default_factory=uuid4)
    created_date: date = field(default_factory=date.today)

    first_name: str = ""
    last_name: str = ""
    role: str = ""          # Council role per DOC-01.2

    standing_status: MemberStandingStatus = MemberStandingStatus.ACTIVE
    appointment_date: Optional[date] = None
    covenant_ref: Optional[str] = None
    covenant_renewal_date: Optional[date] = None    # Must be within renewal interval (VR-04-02)

    accountability_record_refs: list[str] = field(default_factory=list)
    disqualification_record_ref: Optional[str] = None  # Required if Disqualified (VR-04-05)

    def is_eligible_to_vote(self) -> bool:
        """
        Returns True only if member may participate in Council votes.
        Suspended and Disqualified members are excluded from quorum calculation.
        TODO: Implement per VR-04-04.
        """
        # TODO: Return True only if standing_status == ACTIVE
        pass

    def disqualify(self, disqualification_record_ref: str):
        """
        Immediately set standing_status = DISQUALIFIED.
        No grace period — takes effect at time of call (VR-04-03).
        TODO: Implement immediate disqualification; log; route to CLU-02.4.
        """
        # TODO: Set standing_status = DISQUALIFIED immediately
        # TODO: Set disqualification_record_ref
        # TODO: Remove from eligible voter list
        # TODO: Log CRITICAL event
        pass
