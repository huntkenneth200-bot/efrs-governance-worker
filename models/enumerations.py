"""
FORMATION INTELLIGENCE PLATFORM
Global Enumerations

Reference: DSR-01 / ENUM-01 through ENUM-14
Version: 0.1-scaffold

All enum values are Council-governed. No value may be added, changed, or
removed without a Council ruling (DOC-01.2). See DATA-SCHEMA-REGISTRY.md.
"""

from enum import Enum


# ENUM-01 — Formation Stage (DOC-03.3)
class FormationStage(str, Enum):
    STAGE_1 = "STAGE_1"   # Stabilization
    STAGE_2 = "STAGE_2"   # Deconstruction
    STAGE_3 = "STAGE_3"   # Reconstruction
    STAGE_4 = "STAGE_4"   # Integration
    STAGE_5 = "STAGE_5"   # Deployment


# ENUM-02 — Fracture Domain (DOC-03.2)
class FractureDomain(str, Enum):
    IDENTITY   = "IDENTITY"
    AUTHORITY  = "AUTHORITY"
    RELATIONAL = "RELATIONAL"
    VOCATIONAL = "VOCATIONAL"
    WORLDVIEW  = "WORLDVIEW"


# ENUM-03 — Fracture Severity (DOC-03.2)
class FractureSeverity(str, Enum):
    L1 = "L1"   # Surface
    L2 = "L2"   # Structural
    L3 = "L3"   # Root — requires facilitator review before finalization


# ENUM-04 — Fracture Origin (DOC-03.2)
class FractureOrigin(str, Enum):
    SELF_GENERATED      = "SELF_GENERATED"
    EXTERNALLY_INFLICTED = "EXTERNALLY_INFLICTED"
    SYSTEMIC            = "SYSTEMIC"


# ENUM-05 — Blockage Type (DOC-02.1)
class BlockageType(str, Enum):
    FORMATION  = "FORMATION"
    RELATIONAL = "RELATIONAL"
    SPIRITUAL  = "SPIRITUAL"   # Auto-escalates to Council
    EXTERNAL   = "EXTERNAL"


# ENUM-06 — Blockage Severity
class BlockageSeverity(str, Enum):
    MODERATE    = "MODERATE"
    SIGNIFICANT = "SIGNIFICANT"
    CRITICAL    = "CRITICAL"    # Auto-notifies Hub Leader


# ENUM-07 — Clearance Status (theological, capital, language)
class ClearanceStatus(str, Enum):
    CLEARED      = "CLEARED"
    CONDITIONAL  = "CONDITIONAL"
    DISQUALIFIED = "DISQUALIFIED"   # Permanent — Council ruling required to reverse


# ENUM-08 — Content Type
class ContentType(str, Enum):
    TIER_1_DOCUMENT         = "TIER_1_DOCUMENT"
    TIER_2_DOCUMENT         = "TIER_2_DOCUMENT"
    TIER_3_SCHEMA           = "TIER_3_SCHEMA"
    TIER_4_ASSESSMENT       = "TIER_4_ASSESSMENT"
    TIER_6_TRAINING         = "TIER_6_TRAINING"
    FACILITATOR_COMMUNICATION = "FACILITATOR_COMMUNICATION"
    HUB_MATERIAL            = "HUB_MATERIAL"
    EXTERNAL_CONTENT        = "EXTERNAL_CONTENT"
    TRAINING_MATERIAL       = "TRAINING_MATERIAL"
    PUBLIC_COMMUNICATION    = "PUBLIC_COMMUNICATION"


# ENUM-09 — Council Ruling Type
class RulingType(str, Enum):
    AMENDMENT          = "AMENDMENT"
    DIRECTIVE          = "DIRECTIVE"
    DISQUALIFICATION   = "DISQUALIFICATION"
    DOCTRINAL_POSITION = "DOCTRINAL_POSITION"
    MEMBERSHIP_ACTION  = "MEMBERSHIP_ACTION"
    PARTNERSHIP_APPROVAL = "PARTNERSHIP_APPROVAL"


# ENUM-10 — Hub Status
class HubStatus(str, Enum):
    FORMING        = "FORMING"
    ACTIVE         = "ACTIVE"
    AT_CAPACITY    = "AT_CAPACITY"
    UNDER_REVIEW   = "UNDER_REVIEW"
    SUSPENDED      = "SUSPENDED"
    CLOSED         = "CLOSED"    # Permanent — records preserved


# ENUM-11 — Intervention Type (Hub Health)
class InterventionType(str, Enum):
    ADVISORY       = "ADVISORY"
    OVERSIGHT      = "OVERSIGHT"
    SUSPENSION     = "SUSPENSION"
    CLOSURE_REVIEW = "CLOSURE_REVIEW"


# ENUM-12 — Lexicon Update Type
class LexiconUpdateType(str, Enum):
    NEW_ENTRY      = "NEW_ENTRY"
    AMENDMENT      = "AMENDMENT"
    DISQUALIFICATION = "DISQUALIFICATION"


# ENUM-13 — Capital Source Type
class CapitalSourceType(str, Enum):
    INDIVIDUAL_DONOR = "INDIVIDUAL_DONOR"
    FOUNDATION       = "FOUNDATION"
    GRANT            = "GRANT"
    CORPORATE        = "CORPORATE"
    CHURCH_PARTNER   = "CHURCH_PARTNER"
    OTHER            = "OTHER"    # Requires affiliation description


# ENUM-14 — Funding Status
class FundingStatus(str, Enum):
    AUTHORIZED  = "AUTHORIZED"
    CONTINGENT  = "CONTINGENT"
    DENIED      = "DENIED"       # Permanent record
    PENDING     = "PENDING"
    DISBURSED   = "DISBURSED"
    HELD        = "HELD"


# --- Record Status Enumerations ---

class ParticipantStatus(str, Enum):
    ACTIVE      = "ACTIVE"
    INACTIVE    = "INACTIVE"
    COMPLETED   = "COMPLETED"
    TRANSFERRED = "TRANSFERRED"


class FacilitatorCertificationStatus(str, Enum):
    CERTIFIED   = "CERTIFIED"
    PROVISIONAL = "PROVISIONAL"
    SUSPENDED   = "SUSPENDED"
    REVOKED     = "REVOKED"


class MemberStandingStatus(str, Enum):
    ACTIVE        = "ACTIVE"
    UNDER_REVIEW  = "UNDER_REVIEW"
    SUSPENDED     = "SUSPENDED"
    DISQUALIFIED  = "DISQUALIFIED"


class FractureProfileStatus(str, Enum):
    DRAFT              = "DRAFT"
    L3_REVIEW_REQUIRED = "L3_REVIEW_REQUIRED"
    FACILITATOR_REVIEWED = "FACILITATOR_REVIEWED"
    FINALIZED          = "FINALIZED"


class PathwayStatus(str, Enum):
    DRAFT       = "DRAFT"
    ACTIVE      = "ACTIVE"
    ON_HOLD     = "ON_HOLD"
    COMPLETE    = "COMPLETE"
    TRANSFERRED = "TRANSFERRED"


class MilestoneStatus(str, Enum):
    PENDING  = "PENDING"
    PARTIAL  = "PARTIAL"
    COMPLETE = "COMPLETE"
    OVERDUE  = "OVERDUE"


class BlockageHoldStatus(str, Enum):
    ACTIVE       = "ACTIVE"
    UNDER_REVIEW = "UNDER_REVIEW"
    RESOLVED     = "RESOLVED"


class RoutingStatus(str, Enum):
    CONFIRMED        = "CONFIRMED"
    PENDING_CAPACITY = "PENDING_CAPACITY"
    CROSS_HUB        = "CROSS_HUB"


class AssessmentInstrumentType(str, Enum):
    DOC_04_1 = "DOC_04_1"   # Intake Questionnaire
    DOC_04_2 = "DOC_04_2"   # Fracture Map Assessment
    DOC_04_3 = "DOC_04_3"   # Periodic Formation Assessment


class CovenantStatus(str, Enum):
    ACTIVE       = "ACTIVE"
    RENEWAL_DUE  = "RENEWAL_DUE"
    UNDER_REVIEW = "UNDER_REVIEW"
    RELEASED     = "RELEASED"


class EscalationStatus(str, Enum):
    NOT_ESCALATED = "NOT_ESCALATED"
    PENDING       = "PENDING"
    ACTIVE        = "ACTIVE"
    RESOLVED      = "RESOLVED"


class PropagationStatus(str, Enum):
    COMPLETE = "COMPLETE"
    PARTIAL  = "PARTIAL"
    FAILED   = "FAILED"


class AllocationStatus(str, Enum):
    PENDING   = "PENDING"
    ACTIVE    = "ACTIVE"
    DISBURSED = "DISBURSED"
    CLOSED    = "CLOSED"


class RulingStatus(str, Enum):
    DRAFT      = "DRAFT"
    RATIFIED   = "RATIFIED"
    SUPERSEDED = "SUPERSEDED"


class ReviewPriority(str, Enum):
    ROUTINE = "ROUTINE"
    URGENT  = "URGENT"
