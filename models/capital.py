"""
FORMATION INTELLIGENCE PLATFORM
OBJ-16 — Capital Source Record
OBJ-17 — Capital Source Clearance
OBJ-18 — Fund Allocation Record
OBJ-19 — Disbursement Authorization

Schema authority: DATA-SCHEMA-REGISTRY.md (DSR-01 / OBJ-16 through OBJ-19)
Owning clusters: CLU-03.1 (OBJ-16, OBJ-17), CLU-03.5 (OBJ-18), CLU-06.6 (OBJ-19)
Interfaces: IC-09, IC-10
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from .enumerations import CapitalSourceType, ClearanceStatus, FundingStatus, AllocationStatus


@dataclass
class CapitalSourceRecord:
    """
    OBJ-16 — Identity and affiliation record for a prospective capital source.
    No capital enters the pipeline without a linked Cleared OBJ-17 record.
    """

    source_id: UUID = field(default_factory=uuid4)
    first_submission_date: date = field(default_factory=date.today)
    last_evaluated_date: date = field(default_factory=date.today)

    source_name: str = ""
    source_type: Optional[CapitalSourceType] = None
    source_affiliation: Optional[str] = None   # Required if source_type = OTHER (VR-16-02)
    proposed_conditions: Optional[str] = None

    current_clearance_id: Optional[UUID] = None  # Links to most recent OBJ-17


@dataclass
class CapitalSourceClearance:
    """
    OBJ-17 — Integrity evaluation outcome for a capital source.
    Required before any funds from this source enter the platform pipeline.

    Constraints:
    - Cleared requires expiry_date to be set (VR-17-01)
    - Conditional may not enter pipeline without conditions_acknowledged (VR-17-02)
    - disqualification_basis required when Disqualified (VR-17-03)
    - Expired clearance is not active clearance (VR-17-04)
    """

    clearance_id: UUID = field(default_factory=uuid4)
    clearance_date: date = field(default_factory=date.today)
    expiry_date: Optional[date] = None     # Required on Cleared status

    source_id: Optional[UUID] = None
    integrity_status: ClearanceStatus = ClearanceStatus.CONDITIONAL
    disqualification_basis: Optional[str] = None    # Required if Disqualified
    conditional_requirements: Optional[str] = None  # Required if Conditional
    conditions_acknowledged: bool = False            # Required before Conditional → pipeline
    review_authority: Optional[str] = None
    evaluation_notes: Optional[str] = None

    def is_active_clearance(self) -> bool:
        """
        Returns True only if clearance is Cleared and not expired.
        Used at every pipeline entry point (CA-004 prevents expired clearance).
        TODO: Check integrity_status == CLEARED and expiry_date > today.
        """
        # TODO: Validate integrity_status == CLEARED
        # TODO: Validate expiry_date is not None and expiry_date > date.today()
        pass


@dataclass
class FundAllocationRecord:
    """
    OBJ-18 — Council-authorized allocation decision.
    No disbursement without council_authorization_ref (VR-18-01).

    Constraints:
    - council_authorization_ref must reference a Ratified ruling (VR-18-01)
    - allocated_amount must not breach sufficiency standard (VR-18-02)
    - destination_id must reference active hub or unit (VR-18-03)
    """

    allocation_id: UUID = field(default_factory=uuid4)
    created_date: date = field(default_factory=date.today)
    effective_date: Optional[date] = None

    allocation_type: Optional[str] = None   # Deployment / Operations / Training / Reserve
    allocated_amount: float = 0.0
    destination_id: Optional[str] = None
    council_authorization_ref: Optional[str] = None  # Must reference Ratified OBJ-14
    sufficiency_compliance_ref: Optional[str] = None  # CLU-06.4 compliance record
    allocation_status: AllocationStatus = AllocationStatus.PENDING


@dataclass
class DisbursementAuthorization:
    """
    OBJ-19 — Authorization record enabling actual fund disbursement.
    authorized_amount may not exceed OBJ-18.allocated_amount (VR-19-01).

    Constraints:
    - expiry_date must be set — no open-ended authorizations (VR-19-02)
    - Disbursed requires disbursement_date (VR-19-03)
    - Denied requires denial_basis (VR-19-04)
    """

    disbursement_authorization_id: UUID = field(default_factory=uuid4)
    authorization_date: date = field(default_factory=date.today)
    expiry_date: Optional[date] = None      # Required — no open-ended authorizations
    disbursement_date: Optional[date] = None

    allocation_id: Optional[UUID] = None
    destination_id: Optional[str] = None
    authorized_amount: float = 0.0
    disbursement_status: FundingStatus = FundingStatus.PENDING
    contingency_conditions: Optional[str] = None
    denial_basis: Optional[str] = None      # Required if Denied
    reporting_ref: Optional[str] = None     # CLU-06.5 reporting record

    def is_valid_for_disbursement(self) -> bool:
        """
        Returns True if authorization is current and has Authorized status.
        Checks expiry and status before any disbursement action.
        TODO: Implement expiry and status validation.
        """
        # TODO: Check disbursement_status == AUTHORIZED
        # TODO: Check expiry_date > date.today()
        pass
