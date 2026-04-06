"""
FORMATION INTELLIGENCE PLATFORM
OBJ-25 — Deployment Funding Authorization

Schema authority: DATA-SCHEMA-REGISTRY.md (DSR-01 / OBJ-25)
Owning cluster: CLU-06.6 — Deployment Funding Logic
Interface: IC-14 (Deployment Funding Authorization → CLU-04.1)
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from .enumerations import FundingStatus


@dataclass
class DeploymentFundingAuthorization:
    """
    OBJ-25 — Financial clearance for a specific hub deployment event.
    Hub Formation Protocol (CLU-04.1) may not advance to launch without Authorized status.

    Constraints:
    - authorized_amount may not exceed requested_amount without amended Council authorization (VR-25-01)
    - Authorized requires council_authorization_ref referencing a Ratified ruling (VR-25-02)
    - expiry_date must be set — no open-ended authorizations (VR-25-03)
    - Denied requires denial_basis (VR-25-04)
    - Hub launch gate blocked without Authorized status (VR-25-05 / BC-03)
    """

    funding_authorization_id: UUID = field(default_factory=uuid4)
    authorization_date: date = field(default_factory=date.today)
    expiry_date: Optional[date] = None          # Required — open-ended rejected (VR-25-03)
    initiation_deadline: Optional[date] = None  # Hub must begin by this date

    deployment_request_id: Optional[str] = None    # CLU-04.1 deployment record
    hub_id: Optional[UUID] = None
    deployment_template_ref: Optional[str] = None  # Phase 9 template
    council_authorization_ref: Optional[str] = None
    allocation_id: Optional[UUID] = None            # OBJ-18 source allocation

    requested_amount: float = 0.0
    authorized_amount: float = 0.0          # May not exceed requested_amount (VR-25-01)
    funding_status: FundingStatus = FundingStatus.PENDING
    contingency_conditions: Optional[str] = None
    denial_basis: Optional[str] = None      # Required if Denied (VR-25-04)

    def is_launch_authorized(self) -> bool:
        """
        Returns True if hub formation protocol may proceed to launch phase.
        Checks: Authorized status AND not expired.
        Used as gate in WF-08 (Hub Deployment and Launch).
        TODO: Implement status and expiry check.
        """
        # TODO: Check funding_status == AUTHORIZED
        # TODO: Check expiry_date > date.today()
        # TODO: Return False with CA-009 error if either check fails
        pass
