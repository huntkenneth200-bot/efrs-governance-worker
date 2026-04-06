"""
FORMATION INTELLIGENCE PLATFORM
OBJ-20 — Language Compliance Clearance
OBJ-21 — Lexicon Entry
OBJ-22 — Lexicon Update Record

Schema authority: DATA-SCHEMA-REGISTRY.md (DSR-01 / OBJ-20 through OBJ-22)
Owning cluster: CLU-05 — Linguistic Diffusion Engine
Interfaces: IC-11, IC-12
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from .enumerations import ClearanceStatus, ContentType, LexiconUpdateType


@dataclass
class FlaggedTerm:
    """Sub-schema for a flagged term in a language compliance review."""
    term: str = ""
    context: str = ""
    lexicon_ref: Optional[str] = None   # DOC-03.1 entry reference
    correction_guidance: str = ""


@dataclass
class LanguageComplianceClearance:
    """
    OBJ-20 — Language compliance review outcome.
    Required before any document achieves platform status (VR-20-05).
    Required before any communication is released.

    Constraints:
    - Cleared requires flagged_terms and disqualified_terms to be empty (VR-20-01)
    - Disqualified requires at least one disqualified_terms entry (VR-20-02)
    - Flagged requires at least one flagged_terms entry (VR-20-03)
    - Resubmissions require resubmission_ref (VR-20-04)
    """

    clearance_id: UUID = field(default_factory=uuid4)
    submitted_date: date = field(default_factory=date.today)
    clearance_date: Optional[date] = None

    review_request_id: Optional[str] = None
    content_ref: Optional[str] = None
    content_type: Optional[ContentType] = None
    requesting_cluster: Optional[str] = None
    compliance_status: ClearanceStatus = ClearanceStatus.CONDITIONAL

    flagged_terms: list[FlaggedTerm] = field(default_factory=list)
    disqualified_terms: list[FlaggedTerm] = field(default_factory=list)
    correction_guidance: Optional[str] = None
    resubmission_ref: Optional[UUID] = None     # Required if prior review exists (VR-20-04)


@dataclass
class LexiconEntry:
    """
    OBJ-21 — Single authorized term entry in the Platform Lexicon (DOC-03.1).
    Every entry requires a Council ruling reference (VR-21-02).
    No entry is deleted — Disqualified or Superseded status only.

    Constraints:
    - term must be unique among Active entries (VR-21-01)
    - council_ruling_ref required (VR-21-02)
    - disqualified_uses must contain at least one entry (VR-21-03)
    - scriptural_anchor must cite at least one specific passage (VR-21-04)
    - Disqualified/Superseded entries may not revert to Active without Council ruling (VR-21-05)
    """

    entry_id: UUID = field(default_factory=uuid4)
    created_date: date = field(default_factory=date.today)
    last_amended_date: Optional[date] = None

    # Core content — all fields authority-governed
    term: str = ""
    domain: Optional[str] = None           # Identity / Formation / Community / Authority / Restoration / Mission
    definition: str = ""
    scriptural_anchor: str = ""            # Must cite at least one specific passage
    theological_context: str = ""
    disqualified_uses: list[str] = field(default_factory=list)  # Must contain at least one (VR-21-03)
    related_terms: list[UUID] = field(default_factory=list)

    # Governance
    entry_status: str = "ACTIVE"           # ACTIVE / DISQUALIFIED / SUPERSEDED
    council_ruling_ref: Optional[str] = None   # Required — no entry without this (VR-21-02)
    superseded_by: Optional[UUID] = None   # Must reference Active entry if populated (VR-21-06)


@dataclass
class LexiconUpdateRecord:
    """
    OBJ-22 — Single update event to the Platform Lexicon.
    All clusters must be notified. Disqualification triggers compliance audit.

    Constraints:
    - council_ruling_ref required — unilateral updates rejected (VR-22-01)
    - compliance_audit_triggered must be True when update_type = Disqualification (VR-22-02)
    - All clusters must appear in cluster_notification_log (VR-22-03)
    """

    update_id: UUID = field(default_factory=uuid4)
    propagation_date: date = field(default_factory=date.today)
    effective_date: Optional[date] = None

    update_type: Optional[LexiconUpdateType] = None
    term: str = ""
    updated_entry_ref: Optional[UUID] = None    # Links to OBJ-21
    council_ruling_ref: Optional[str] = None    # Required (VR-22-01)
    propagation_id: Optional[UUID] = None       # Links to OBJ-15 if applicable

    cluster_notification_log: dict[str, str] = field(default_factory=dict)  # ClusterID → status
    compliance_audit_triggered: bool = False    # Must be True on Disqualification (VR-22-02)
    audit_ref: Optional[str] = None             # CLU-05.3 audit record
