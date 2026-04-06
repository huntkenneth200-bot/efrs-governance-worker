# FORMATION INTELLIGENCE PLATFORM
## DATA SCHEMA REGISTRY

**Document Reference:** DSR-01
**Version:** 1.0
**Status:** Active
**Owning Authority:** Council of Metanoia
**Prepared By:** Architect Mode — Claude Code
**Date:** 2026-03-30
**Review Cycle:** Upon structural amendment only

---

## PURPOSE

This registry defines every data object referenced in the Interface Contract Matrix (ICM-01). For each object: field list, field types, required vs. optional, validation rules, enumerations, constraints, and relationships to other objects.

No data object may be implemented, modified, or retired without a corresponding update to this registry under Council review. This document is the authoritative schema reference for all platform build work.

---

## REGISTRY INDEX

| ID | Object Name | Primary Owner | Interface References |
|---|---|---|---|
| OBJ-01 | Participant Record | CLU-01.6 | IC-01, IC-02, IC-03, IC-04, IC-05, IC-06 |
| OBJ-02 | Facilitator Record | CLU-02 | IC-01, IC-02, IC-03, IC-04, IC-05 |
| OBJ-03 | Hub Record | CLU-04 | IC-05, IC-13, IC-14 |
| OBJ-04 | Council Member Record | CLU-02 | IC-07, IC-08 |
| OBJ-05 | Fracture Domain Profile | CLU-01.1 | IC-01, IC-02 |
| OBJ-06 | Formation Pathway Assignment | CLU-01.5 | IC-02, IC-05 |
| OBJ-07 | Milestone Completion Record | CLU-01.3 | IC-03 |
| OBJ-08 | Stage Progression Evaluation | CLU-01.2 | IC-03, IC-04 |
| OBJ-09 | Blockage Record | CLU-01.4 | IC-04 |
| OBJ-10 | Hub Routing Record | CLU-04.3 | IC-05 |
| OBJ-11 | Formation Record | CLU-01.6 | IC-06 |
| OBJ-12 | Aggregate Formation Report | CLU-01.6 | IC-06 |
| OBJ-13 | Theological Review Record | CLU-02.2 | IC-07 |
| OBJ-14 | Council Ruling Record | CLU-02.1 | IC-08 |
| OBJ-15 | Ruling Propagation Record | CLU-02.1 | IC-08 |
| OBJ-16 | Capital Source Record | CLU-03.1 | IC-09 |
| OBJ-17 | Capital Source Clearance | CLU-03.1 | IC-09 |
| OBJ-18 | Fund Allocation Record | CLU-03.5 | IC-10 |
| OBJ-19 | Disbursement Authorization | CLU-06.6 | IC-10 |
| OBJ-20 | Language Compliance Clearance | CLU-05.1 | IC-11 |
| OBJ-21 | Lexicon Entry | CLU-05.2 | IC-12 |
| OBJ-22 | Lexicon Update Record | CLU-05.2 | IC-12 |
| OBJ-23 | Hub Health Assessment | CLU-04.6 | IC-13 |
| OBJ-24 | Hub Health Escalation | CLU-04.6 | IC-13 |
| OBJ-25 | Deployment Funding Authorization | CLU-06.6 | IC-14 |
| OBJ-26 | Assessment Completion Record | CLU-01.1 | IC-01 |
| OBJ-27 | Covenant Member Record | CLU-04.2 | IC-05 |

---

## GLOBAL ENUMERATIONS

These enumerations are referenced across multiple objects. All objects using these fields must conform to the values defined here.

---

### ENUM-01 — Formation Stage

| Value | Label | Description |
|---|---|---|
| STAGE_1 | Stabilization | Initial grounding; safety and spiritual orientation established |
| STAGE_2 | Deconstruction | Fracture identification and acknowledgment |
| STAGE_3 | Reconstruction | Theological re-framing and identity rebuilding |
| STAGE_4 | Integration | Consolidation of formation gains into whole-person living |
| STAGE_5 | Deployment | Vocational and missional activation from restored identity |

**Authority:** DOC-03.3 (Stage Schema Reference)
**Constraint:** No custom values permitted. Stages are sequential and non-skippable.

---

### ENUM-02 — Fracture Domain

| Value | Label | Description |
|---|---|---|
| IDENTITY | Identity | Fractures in self-understanding as image-bearer |
| AUTHORITY | Authority | Fractures in relationship to legitimate authority structures |
| RELATIONAL | Relational | Fractures in capacity for covenant community and attachment |
| VOCATIONAL | Vocational | Fractures in calling, purpose, and productive contribution |
| WORLDVIEW | Worldview | Fractures in the interpretive framework through which life is understood |

**Authority:** DOC-03.2 (Fracture Domain Taxonomy)
**Constraint:** Multiple domains may be active simultaneously for one participant.

---

### ENUM-03 — Fracture Severity

| Value | Label | Description |
|---|---|---|
| L1 | Surface | Behavioral or symptomatic manifestation; no structural root identified |
| L2 | Structural | Persistent pattern with identifiable formative cause |
| L3 | Root | Deep-seated fracture with spiritual, developmental, or traumatic origin |

**Authority:** DOC-03.2 (Fracture Domain Taxonomy)
**Constraint:** L3 requires facilitator review before profile finalization (per IC-01).

---

### ENUM-04 — Fracture Origin

| Value | Label | Description |
|---|---|---|
| SELF_GENERATED | Self-generated | Fracture arising from individual choices, sin patterns, or self-protective responses |
| EXTERNALLY_INFLICTED | Externally inflicted | Fracture arising from harm done by another person or institution |
| SYSTEMIC | Systemic | Fracture arising from structural, cultural, or generational systems |

**Authority:** DOC-03.2 (Fracture Domain Taxonomy)
**Constraint:** Multiple origin types may apply to a single domain.

---

### ENUM-05 — Blockage Type

| Value | Label | Description |
|---|---|---|
| FORMATION | Formation | Stalled progress in formation activities or milestone engagement |
| RELATIONAL | Relational | Interpersonal conflict, isolation, or community withdrawal |
| SPIRITUAL | Spiritual | Unresolved spiritual warfare, unforgiveness, or theological resistance |
| EXTERNAL | External | Life circumstances preventing formation engagement |

**Authority:** DOC-02.1 (Facilitator Operations Manual)
**Constraint:** SPIRITUAL type automatically triggers escalation (per IC-04).

---

### ENUM-06 — Blockage Severity

| Value | Label | Description |
|---|---|---|
| MODERATE | Moderate | Progress slowed; engagement present |
| SIGNIFICANT | Significant | Progress halted; engagement intermittent |
| CRITICAL | Critical | Full disengagement or acute crisis indicators present |

**Constraint:** CRITICAL severity triggers Hub Leader notification regardless of blockage type.

---

### ENUM-07 — Clearance Status

| Value | Label | Description |
|---|---|---|
| CLEARED | Cleared | Fully approved; no conditions |
| CONDITIONAL | Conditional | Approved subject to stated modifications or acknowledgments |
| DISQUALIFIED | Disqualified | Rejected; permanent record; Council ruling required for reversal |

**Used in:** OBJ-13 (Theological Review), OBJ-17 (Capital Source Clearance), OBJ-20 (Language Compliance)

---

### ENUM-08 — Document / Content Type

| Value | Label |
|---|---|
| TIER_1_DOCUMENT | Tier 1 Governing Document |
| TIER_2_DOCUMENT | Tier 2 Operations Document |
| TIER_3_SCHEMA | Tier 3 Structural Schema |
| TIER_4_ASSESSMENT | Tier 4 Assessment Instrument |
| TIER_6_TRAINING | Tier 6 Training Document |
| FACILITATOR_COMMUNICATION | Facilitator Communication |
| HUB_MATERIAL | Hub-Produced Material |
| EXTERNAL_CONTENT | External Content Proposed for Platform Use |
| TRAINING_MATERIAL | Training or Curriculum Material |
| PUBLIC_COMMUNICATION | External / Public-Facing Communication |

---

### ENUM-09 — Council Ruling Type

| Value | Label |
|---|---|
| AMENDMENT | Document or policy amendment |
| DIRECTIVE | Operational directive to clusters |
| DISQUALIFICATION | Doctrinal or language disqualification |
| DOCTRINAL_POSITION | New or affirmed doctrinal position |
| MEMBERSHIP_ACTION | Council member standing action |
| PARTNERSHIP_APPROVAL | External partnership authorization |

---

### ENUM-10 — Hub Status

| Value | Label | Description |
|---|---|---|
| FORMING | Forming | Pre-launch; formation protocol in progress |
| ACTIVE | Active | Fully operational hub accepting participants |
| AT_CAPACITY | At Capacity | Active but not accepting new participants |
| UNDER_REVIEW | Under Review | Health assessment escalation in progress |
| SUSPENDED | Suspended | Operations paused by Council directive |
| CLOSED | Closed | Permanently closed; records preserved |

---

### ENUM-11 — Intervention Type (Hub Health)

| Value | Label | Description |
|---|---|---|
| ADVISORY | Advisory | Council guidance issued; Hub Leader to self-correct |
| OVERSIGHT | Oversight | Council assigns oversight liaison to hub |
| SUSPENSION | Suspension | Hub operations suspended pending review |
| CLOSURE_REVIEW | Closure Review | Council evaluating hub for permanent closure |

---

### ENUM-12 — Lexicon Update Type

| Value | Label |
|---|---|
| NEW_ENTRY | New authorized term added |
| AMENDMENT | Existing entry modified |
| DISQUALIFICATION | Term disqualified; added to disqualified register |

---

### ENUM-13 — Capital Source Type

| Value | Label |
|---|---|
| INDIVIDUAL_DONOR | Individual donor |
| FOUNDATION | Private or family foundation |
| GRANT | Institutional or government grant |
| CORPORATE | Corporate giving program |
| CHURCH_PARTNER | Church partnership contribution |
| OTHER | Other — requires description |

---

### ENUM-14 — Funding Status

| Value | Label |
|---|---|
| AUTHORIZED | Fully authorized; ready for disbursement |
| CONTINGENT | Authorized subject to stated conditions |
| DENIED | Not authorized; permanent record |
| PENDING | Under review; not yet determined |
| DISBURSED | Funds released to destination |
| HELD | Authorization active but disbursement paused |

---

---

## OBJECT DEFINITIONS

---

### OBJ-01 — PARTICIPANT RECORD

**Owner:** CLU-01.6 — Restoration Record Keeper
**Description:** The root identity record for every individual who enters the formation platform. All other participant-related objects reference this record.

| Field | Type | Required | Description |
|---|---|---|---|
| participant_id | UUID | Yes | System-generated unique identifier |
| first_name | String (50) | Yes | Legal or preferred first name |
| last_name | String (50) | Yes | Legal last name |
| hub_id | Foreign Key → OBJ-03 | Yes | Assigned Emmaus Road hub |
| facilitator_id | Foreign Key → OBJ-02 | Yes | Assigned facilitator |
| intake_date | Date | Yes | Date DOC-04.1 was completed |
| current_stage | Enum (ENUM-01) | Yes | Active formation stage |
| record_status | Enum | Yes | Active / Inactive / Completed / Transferred |
| consent_record_ref | Identifier | Yes | Signed consent document reference |
| created_date | Date | Yes | System-generated |
| last_modified_date | Date | Yes | System-generated |
| notes | Text | No | Facilitator narrative notes — confidential |

**Validation Rules:**
- participant_id must be unique across all records
- hub_id must reference an Active or Forming hub (ENUM-10)
- facilitator_id must reference an active facilitator record
- intake_date must be on or before created_date
- current_stage must be a valid ENUM-01 value

**Constraints:**
- Records may not be deleted — status changes only
- Access restricted to assigned facilitator, Hub Leader, Council (aggregate reporting only)
- Transferred records retain original hub history

**Relationships:**
- 1:1 with OBJ-11 (Formation Record) — every participant has one formation record
- 1:Many with OBJ-05 (Fracture Domain Profile) — may have multiple over time
- 1:Many with OBJ-07 (Milestone Completion Record)
- 1:Many with OBJ-09 (Blockage Record)
- 1:1 active with OBJ-06 (Formation Pathway Assignment)
- 1:Many with OBJ-26 (Assessment Completion Record)

---

### OBJ-02 — FACILITATOR RECORD

**Owner:** CLU-02 — Council of Metanoia
**Description:** Identity and operational record for every platform-certified facilitator.

| Field | Type | Required | Description |
|---|---|---|---|
| facilitator_id | UUID | Yes | System-generated unique identifier |
| first_name | String (50) | Yes | First name |
| last_name | String (50) | Yes | Last name |
| hub_id | Foreign Key → OBJ-03 | Yes | Primary hub assignment |
| certification_status | Enum | Yes | Certified / Provisional / Suspended / Revoked |
| certification_date | Date | Yes | Date of certification |
| certification_ref | Identifier | Yes | DOC-06.1 orientation completion record |
| active_participant_ids | Array [Foreign Key → OBJ-01] | No | Current participant caseload |
| max_caseload | Integer | Yes | Council-defined maximum caseload |
| standing_status | Enum | Yes | Active / Under-review / Inactive |
| covenant_ref | Identifier | Yes | Signed facilitator covenant record |
| created_date | Date | Yes | System-generated |

**Validation Rules:**
- certification_status must be Certified before facilitator is assigned participants
- active_participant_ids count may not exceed max_caseload
- standing_status is governed by CLU-02.5 (Member Accountability Module)
- covenant_ref must reference a current, signed covenant

**Constraints:**
- Suspended facilitators may not be assigned new participants
- Revoked facilitators trigger reassignment of all active participants
- Facilitator records are permanent — status changes only, no deletion

**Relationships:**
- 1:Many with OBJ-01 (Participant Record)
- 1:1 with OBJ-03 (Hub Record) — primary assignment
- Referenced in OBJ-05, OBJ-07, OBJ-08, OBJ-09

---

### OBJ-03 — HUB RECORD

**Owner:** CLU-04.1 — Hub Formation Protocol
**Description:** Identity and operational record for every Emmaus Road hub site.

| Field | Type | Required | Description |
|---|---|---|---|
| hub_id | UUID | Yes | System-generated unique identifier |
| hub_name | String (100) | Yes | Official hub name |
| hub_leader_id | Identifier | Yes | Assigned Hub Leader |
| geographic_location | String (200) | Yes | City, region, and context description |
| hub_status | Enum (ENUM-10) | Yes | Current operational status |
| launch_date | Date | No | Date hub achieved Active status |
| formation_date | Date | Yes | Date hub formation protocol initiated |
| capacity_max | Integer | Yes | Maximum participant capacity |
| capacity_current | Integer | Yes | Current active participant count |
| council_authorization_ref | Identifier | Yes | CLU-02.1 authorization record |
| deployment_template_ref | Identifier | Yes | Phase 9 template used for deployment |
| covenant_ref | Identifier | Yes | Hub covenant document reference |
| local_church_refs | Array [Identifier] | No | Associated local church relationships |
| created_date | Date | Yes | System-generated |
| last_modified_date | Date | Yes | System-generated |

**Validation Rules:**
- hub_status must be Active before participants may be routed (per IC-05)
- capacity_current may not exceed capacity_max
- council_authorization_ref must be present before hub_status advances beyond Forming
- hub_leader_id must reference a qualified Hub Leader record

**Constraints:**
- Hub status changes require Hub Leader or Council authorization
- Closed hubs retain all records — no deletion
- capacity_current is system-calculated from active participant routing records

**Relationships:**
- 1:Many with OBJ-01 (Participant Record)
- 1:Many with OBJ-02 (Facilitator Record)
- 1:Many with OBJ-23 (Hub Health Assessment)
- 1:1 with OBJ-25 (Deployment Funding Authorization) — per deployment event
- Referenced in IC-05, IC-13, IC-14

---

### OBJ-04 — COUNCIL MEMBER RECORD

**Owner:** CLU-02.5 — Member Accountability Module
**Description:** Identity, standing, and accountability record for every Council of Metanoia member.

| Field | Type | Required | Description |
|---|---|---|---|
| member_id | UUID | Yes | System-generated unique identifier |
| first_name | String (50) | Yes | First name |
| last_name | String (50) | Yes | Last name |
| role | String (100) | Yes | Council role/title per DOC-01.2 |
| standing_status | Enum | Yes | Active / Under-review / Suspended / Disqualified |
| appointment_date | Date | Yes | Date of appointment |
| covenant_ref | Identifier | Yes | Signed Council covenant reference |
| covenant_renewal_date | Date | Yes | Date of most recent renewal |
| accountability_record_refs | Array [Identifier] | No | Any accountability action records |
| disqualification_record_ref | Identifier | No | If applicable |
| created_date | Date | Yes | System-generated |

**Validation Rules:**
- standing_status governs voting rights and quorum calculation
- covenant_renewal_date must be within required renewal interval per DOC-01.2
- Disqualification is immediate on trigger — standing_status set without delay

**Constraints:**
- Suspended members cannot vote on Council rulings
- Disqualified members are permanently removed from quorum calculation
- Records are permanent — status changes only

**Relationships:**
- Referenced in OBJ-13 (Theological Review Record) as reviewer_id
- Referenced in OBJ-14 (Council Ruling Record) for vote records
- Governed by CLU-02.5 accountability processes

---

### OBJ-05 — FRACTURE DOMAIN PROFILE

**Owner:** CLU-01.1 — Fracture Assessment Engine
**Description:** Structured diagnostic output of the fracture assessment process for one participant. The primary input to pathway routing.

| Field | Type | Required | Description |
|---|---|---|---|
| fracture_profile_id | UUID | Yes | System-generated unique identifier |
| participant_id | Foreign Key → OBJ-01 | Yes | Owning participant |
| facilitator_id | Foreign Key → OBJ-02 | Yes | Assessing facilitator |
| assessment_refs | Array [Foreign Key → OBJ-26] | Yes | DOC-04.1 and DOC-04.2 completion records |
| active_domains | Array [Enum (ENUM-02)] | Yes | One or more active fracture domains |
| severity_map | Map [ENUM-02 → ENUM-03] | Yes | Severity per active domain |
| origin_map | Map [ENUM-02 → Array[ENUM-04]] | Yes | One or more origins per active domain |
| recommended_entry_stage | Enum (ENUM-01) | Yes | Suggested starting stage |
| profile_status | Enum | Yes | Draft / Facilitator-reviewed / Finalized |
| l3_review_required | Boolean | Yes | True if any domain is L3 severity |
| l3_review_completed | Boolean | No | Required before finalization if l3_review_required |
| profile_date | Date | Yes | System-generated on creation |
| finalized_date | Date | No | Populated when status = Finalized |
| facilitator_notes | Text | No | Narrative clinical notes |
| superseded_by | Foreign Key → OBJ-05 | No | Links to updated profile on re-assessment |

**Validation Rules:**
- active_domains must contain at least one value
- severity_map must have an entry for every domain in active_domains
- origin_map must have at least one entry for every domain in active_domains
- profile_status may not be set to Finalized if l3_review_required = True and l3_review_completed = False
- recommended_entry_stage must be STAGE_1 unless prior formation history justifies otherwise (requires facilitator note)

**Constraints:**
- Only one Finalized profile may be active per participant at a time
- Prior profiles are retained and linked via superseded_by
- L3 designation in any domain is non-negotiable without facilitator review

**Relationships:**
- Many:1 with OBJ-01 (Participant Record)
- References OBJ-26 (Assessment Completion Record) — both DOC-04.1 and DOC-04.2
- Consumed by OBJ-06 (Formation Pathway Assignment)
- Stored in OBJ-11 (Formation Record)

---

### OBJ-06 — FORMATION PATHWAY ASSIGNMENT

**Owner:** CLU-01.5 — Formation Pathway Router
**Description:** The active formation pathway for one participant — stage, domain focus sequence, facilitator, hub, and session schedule linkage.

| Field | Type | Required | Description |
|---|---|---|---|
| pathway_id | UUID | Yes | System-generated unique identifier |
| participant_id | Foreign Key → OBJ-01 | Yes | Owning participant |
| fracture_profile_id | Foreign Key → OBJ-05 | Yes | Finalized profile driving this pathway |
| assigned_stage | Enum (ENUM-01) | Yes | Current formation stage |
| domain_sequence | Array [Enum (ENUM-02)] | Yes | Ordered domain focus sequence |
| assigned_facilitator_id | Foreign Key → OBJ-02 | Yes | Confirmed facilitator |
| hub_id | Foreign Key → OBJ-03 | Yes | Assigned hub |
| hub_session_refs | Array [Identifier] | No | Linked session schedule entries in CLU-04.3 |
| pathway_status | Enum | Yes | Active / On-hold / Complete / Transferred |
| assignment_date | Date | Yes | System-generated |
| last_modified_date | Date | Yes | System-generated |
| modification_trigger | Enum | No | Re-assessment / Stage-transition / Facilitator-adjustment |
| pathway_notes | Text | No | Routing rationale notes |

**Validation Rules:**
- fracture_profile_id must reference a Finalized profile
- assigned_stage must match or follow recommended_entry_stage from OBJ-05
- hub_id must reference an Active hub (ENUM-10)
- domain_sequence must contain only values present in fracture_profile_id.active_domains
- pathway_status = Complete requires all Stage 5 milestones attested in OBJ-07

**Constraints:**
- Only one Active pathway per participant at a time
- On-hold status requires active OBJ-09 (Blockage Record) on file
- Pathway transfers retain full history

**Relationships:**
- Many:1 with OBJ-01 (Participant Record)
- 1:1 with OBJ-05 (Fracture Domain Profile)
- Drives OBJ-10 (Hub Routing Record)
- Stored in OBJ-11 (Formation Record)

---

### OBJ-07 — MILESTONE COMPLETION RECORD

**Owner:** CLU-01.3 — Milestone Tracking System
**Description:** Records the completion status of a single formation milestone for a single participant.

| Field | Type | Required | Description |
|---|---|---|---|
| milestone_record_id | UUID | Yes | System-generated unique identifier |
| participant_id | Foreign Key → OBJ-01 | Yes | Owning participant |
| milestone_ref | Identifier | Yes | Reference to milestone entry in DOC-03.4 |
| stage | Enum (ENUM-01) | Yes | Stage to which this milestone belongs |
| domain | Enum (ENUM-02) | No | Domain association (if domain-specific milestone) |
| completion_status | Enum | Yes | Pending / Partial / Complete / Overdue |
| facilitator_attestation_id | Foreign Key → OBJ-02 | No | Required for Complete status |
| attestation_date | Date | No | Date of facilitator attestation |
| assessment_ref | Foreign Key → OBJ-26 | No | Supporting assessment completion reference |
| overdue_flag | Boolean | Yes | True if completion_status = Overdue |
| created_date | Date | Yes | System-generated |
| last_modified_date | Date | Yes | System-generated |

**Validation Rules:**
- completion_status may not be set to Complete without facilitator_attestation_id
- milestone_ref must resolve to an active entry in DOC-03.4
- stage must match the stage field in the referenced DOC-03.4 entry
- overdue_flag is system-set based on time thresholds in DOC-03.4 — not manually overridden

**Constraints:**
- Milestone definitions may not be modified in this object — all definition changes go through DOC-03.4 and CLU-05.2
- Overdue milestones are routed to CLU-01.4 for blockage evaluation
- Records are permanent — status changes only

**Relationships:**
- Many:1 with OBJ-01 (Participant Record)
- References DOC-03.4 milestone registry entries
- Aggregated in OBJ-08 (Stage Progression Evaluation)
- Stored in OBJ-11 (Formation Record)

---

### OBJ-08 — STAGE PROGRESSION EVALUATION

**Owner:** CLU-01.2 — Stage Progression Logic
**Description:** Evaluation record assessing whether a participant is eligible for stage advancement. Produced by aggregating milestone completion data and blockage status.

| Field | Type | Required | Description |
|---|---|---|---|
| evaluation_id | UUID | Yes | System-generated unique identifier |
| participant_id | Foreign Key → OBJ-01 | Yes | Participant being evaluated |
| current_stage | Enum (ENUM-01) | Yes | Stage being evaluated for completion |
| milestone_threshold_met | Boolean | Yes | True if all required milestones complete |
| completion_percentage | Decimal (0–100) | Yes | Percentage of stage milestones complete |
| outstanding_milestones | Array [Foreign Key → OBJ-07] | No | Remaining incomplete milestone records |
| active_blockage_id | Foreign Key → OBJ-09 | No | Active blockage hold if present |
| advancement_eligible | Boolean | Yes | True if milestone_threshold_met = True AND no active blockage |
| facilitator_assessment_submitted | Boolean | Yes | Required for Stage 4 → 5 transition |
| facilitator_assessment_ref | Identifier | No | Facilitator stage-readiness submission reference |
| evaluation_date | Date | Yes | System-generated |
| advancement_authorized | Boolean | No | Set by facilitator after review |
| advancement_date | Date | No | Populated when advancement executed |

**Validation Rules:**
- advancement_eligible may only be True if milestone_threshold_met = True AND active_blockage_id is null
- Stage 4 → Stage 5 transition requires facilitator_assessment_submitted = True
- completion_percentage is system-calculated from OBJ-07 records — not manually entered
- advancement_authorized requires facilitator action — not system-automated

**Constraints:**
- Stages may not be skipped regardless of completion_percentage values
- Regression (moving to prior stage) is permitted with documented rationale
- Evaluations are triggered events — not scheduled — triggered by milestone completion

**Relationships:**
- Many:1 with OBJ-01 (Participant Record)
- Aggregates OBJ-07 (Milestone Completion Records)
- References OBJ-09 (Blockage Record) for hold status
- Outcomes update OBJ-06 (Formation Pathway Assignment) current stage

---

### OBJ-09 — BLOCKAGE RECORD

**Owner:** CLU-01.4 — Blockage Detection Module
**Description:** Records a detected formation blockage for one participant — type, severity, resolution tracking, and escalation status.

| Field | Type | Required | Description |
|---|---|---|---|
| blockage_id | UUID | Yes | System-generated unique identifier |
| participant_id | Foreign Key → OBJ-01 | Yes | Participant affected |
| facilitator_id | Foreign Key → OBJ-02 | Yes | Detecting facilitator |
| blockage_type | Enum (ENUM-05) | Yes | Type classification |
| blockage_severity | Enum (ENUM-06) | Yes | Severity level |
| detection_trigger | Enum | Yes | Milestone-stall / Time-in-stage / Facilitator-submitted / Assessment-flag |
| hold_status | Enum | Yes | Active / Under-review / Resolved |
| advancement_blocked | Boolean | Yes | Always True while hold_status = Active |
| recommended_response | Text | Yes | Protocol reference from DOC-02.1 |
| escalation_required | Boolean | Yes | True if SPIRITUAL type or CRITICAL severity |
| escalation_status | Enum | No | Not-escalated / Pending / Active / Resolved |
| escalation_target | Enum | No | Hub-leader / Council |
| facilitator_review_notes | Text | No | Documentation of review actions taken |
| resolution_documentation | Text | No | Required before hold_status = Resolved |
| detection_date | Date | Yes | System-generated |
| resolution_date | Date | No | Populated when hold_status = Resolved |

**Validation Rules:**
- hold_status may not be set to Resolved without resolution_documentation present
- escalation_required must be True when blockage_type = SPIRITUAL or blockage_severity = CRITICAL
- escalation_status must be updated when escalation_required = True
- advancement_blocked must remain True while hold_status = Active — not manually overridden

**Constraints:**
- Blockage clearance without documentation is a system error condition (per IC-04)
- Spiritual blockage requires elder or Council referral — not facilitator-only resolution
- Records are permanent; resolved records retained in OBJ-11 (Formation Record)

**Relationships:**
- Many:1 with OBJ-01 (Participant Record)
- References OBJ-02 (Facilitator Record)
- Blocks OBJ-08 (Stage Progression Evaluation) while Active
- Stored in OBJ-11 (Formation Record)

---

### OBJ-10 — HUB ROUTING RECORD

**Owner:** CLU-04.3 — Household Rhythm Scheduler
**Description:** Records the routing of a participant to a specific hub, linking their pathway assignment to hub session scheduling and hospitality integration.

| Field | Type | Required | Description |
|---|---|---|---|
| routing_record_id | UUID | Yes | System-generated unique identifier |
| participant_id | Foreign Key → OBJ-01 | Yes | Participant being routed |
| pathway_id | Foreign Key → OBJ-06 | Yes | Active pathway driving the routing |
| hub_id | Foreign Key → OBJ-03 | Yes | Assigned hub |
| session_schedule_ref | Identifier | No | CLU-04.3 schedule entry reference |
| hospitality_assignment_ref | Identifier | No | CLU-04.4 hospitality record reference |
| routing_status | Enum | Yes | Confirmed / Pending-capacity / Cross-hub |
| hub_leader_notified | Boolean | Yes | Notification delivery status |
| cross_hub_notification_sent | Boolean | No | Required if routing_status = Cross-hub |
| routing_date | Date | Yes | System-generated |
| last_modified_date | Date | Yes | System-generated |

**Validation Rules:**
- routing_status = Confirmed requires hub_id to reference an Active hub with available capacity
- hub_leader_notified must be True before routing is considered complete
- cross_hub_notification_sent required when routing_status = Cross-hub

**Constraints:**
- Hub at capacity triggers routing_status = Pending-capacity — not routing failure
- Inactive hub reference is an error condition requiring escalation
- Records are permanent

**Relationships:**
- Many:1 with OBJ-01 (Participant Record)
- 1:1 with OBJ-06 (Formation Pathway Assignment)
- References OBJ-03 (Hub Record)

---

### OBJ-11 — FORMATION RECORD

**Owner:** CLU-01.6 — Restoration Record Keeper
**Description:** The permanent, comprehensive formation record for one participant. Aggregates all formation activity — assessments, profiles, pathways, milestones, blockages, and session history.

| Field | Type | Required | Description |
|---|---|---|---|
| formation_record_id | UUID | Yes | System-generated unique identifier |
| participant_id | Foreign Key → OBJ-01 | Yes | 1:1 relationship — one record per participant |
| fracture_profile_history | Array [Foreign Key → OBJ-05] | Yes | All fracture profiles, chronological |
| pathway_history | Array [Foreign Key → OBJ-06] | Yes | All pathway assignments |
| milestone_history | Array [Foreign Key → OBJ-07] | Yes | All milestone records |
| blockage_history | Array [Foreign Key → OBJ-09] | Yes | All blockage records |
| assessment_history | Array [Foreign Key → OBJ-26] | Yes | All completed assessments |
| stage_transition_log | Array [Object] | Yes | Log of all stage transitions with dates and facilitator IDs |
| stage_5_completion_ref | Identifier | No | Populated upon Stage 5 milestone attestation |
| facilitator_session_notes | Array [Object] | No | Chronological facilitator session notes |
| created_date | Date | Yes | System-generated on participant intake |
| last_modified_date | Date | Yes | System-generated |

**Validation Rules:**
- One formation_record per participant_id — enforced at system level
- stage_transition_log entries must include date, from_stage, to_stage, and facilitator_id
- stage_5_completion_ref requires all Stage 5 milestones in milestone_history to have Complete status

**Constraints:**
- Formation records are permanent and immutable — amendments append with audit trail
- Access restricted: assigned facilitator (read/write notes), Hub Leader (read), Council (aggregate read only)
- Records do not travel to CLU-06 with individual identifiers — only anonymized aggregate via IC-06

**Relationships:**
- 1:1 with OBJ-01 (Participant Record)
- Aggregates OBJ-05, OBJ-06, OBJ-07, OBJ-09, OBJ-26
- Source for OBJ-12 (Aggregate Formation Report) — anonymized

---

### OBJ-12 — AGGREGATE FORMATION REPORT

**Owner:** CLU-01.6 — Restoration Record Keeper
**Description:** Anonymized aggregate output derived from formation records for Council governance reporting (CLU-02.1) and capital reporting (CLU-06.5). Contains no individual identifiers.

| Field | Type | Required | Description |
|---|---|---|---|
| report_id | UUID | Yes | System-generated unique identifier |
| report_type | Enum | Yes | Governance / Capital |
| requesting_module | Identifier | Yes | CLU-02.1 or CLU-06.5 |
| authorization_ref | Identifier | Yes | Council authorization record |
| reporting_period_start | Date | Yes | Start of reporting period |
| reporting_period_end | Date | Yes | End of reporting period |
| total_participants | Integer | Yes | Count only — no identifiers |
| stage_distribution | Map [ENUM-01 → Integer] | Yes | Count per stage |
| domain_prevalence | Map [ENUM-02 → Integer] | Yes | Governance reports only — omit from Capital |
| blockage_frequency | Map [ENUM-05 → Integer] | Yes | Governance reports only — omit from Capital |
| milestone_completion_rate | Decimal (0–100) | Yes | Aggregate percentage |
| stage_completion_count | Map [ENUM-01 → Integer] | No | Capital reports — count completing each stage |
| program_utilization_rate | Decimal (0–100) | No | Capital reports — capacity utilization |
| generated_date | Date | Yes | System-generated |

**Validation Rules:**
- No participant_id, facilitator_id, or hub_id included in Capital-type reports
- domain_prevalence and blockage_frequency omitted from Capital-type reports
- authorization_ref must be a valid, active Council authorization

**Constraints:**
- Report generation triggers audit log entry in CLU-01.6
- Reports are read-only outputs — no write-back
- Individual data requests are rejected as error conditions (per IC-06)

**Relationships:**
- Derived from OBJ-11 (Formation Record) — anonymized aggregate only
- Delivered to CLU-02.1 (Governance) and CLU-06.5 (Capital) via IC-06

---

### OBJ-13 — THEOLOGICAL REVIEW RECORD

**Owner:** CLU-02.2 — Theological Review Engine
**Description:** Records the request, process, and outcome of a theological review for any platform content.

| Field | Type | Required | Description |
|---|---|---|---|
| review_id | UUID | Yes | System-generated unique identifier |
| review_request_id | Identifier | Yes | Originating request reference |
| requesting_module | Identifier | Yes | Cluster and submodule submitting for review |
| content_type | Enum (ENUM-08) | Yes | Type of content under review |
| content_ref | Identifier | Yes | Reference to reviewed content |
| review_priority | Enum | Yes | Routine / Urgent |
| clearance_status | Enum (ENUM-07) | Yes | Cleared / Conditional / Disqualified |
| theological_rationale | Text | Yes | Required for all outcomes — Scripture or Tier 1 citation |
| conditional_requirements | Array [Text] | No | Required if clearance_status = Conditional |
| conditional_resolved | Boolean | No | True when all conditions satisfied |
| disqualification_basis | Text | No | Required if clearance_status = Disqualified |
| reviewer_id | Foreign Key → OBJ-04 | Yes | Reviewing Council member |
| submitted_date | Date | Yes | System-generated on submission |
| review_date | Date | No | Date review completed |
| registry_entry_ref | Identifier | No | CLU-02.4 ruling reference if disqualification |

**Validation Rules:**
- theological_rationale is required for all clearance_status values — including Cleared
- disqualification_basis required when clearance_status = Disqualified
- conditional_requirements required when clearance_status = Conditional
- reviewer_id must reference an Active Council member (OBJ-04)

**Constraints:**
- Disqualification records automatically route to CLU-02.4 (Amendment and Ruling Registry)
- Platform status may not be granted to any content without Cleared or Conditional (resolved) status
- Disqualification is not reversible without full Council ruling

**Relationships:**
- References OBJ-04 (Council Member Record) for reviewer
- Feeds OBJ-14 (Council Ruling Record) if ruling generated
- Stored in CLU-02.4 registry

---

### OBJ-14 — COUNCIL RULING RECORD

**Owner:** CLU-02.1 — Governing Authority Module
**Description:** The authoritative record of a single Council ruling — amendment, directive, disqualification, or doctrinal position.

| Field | Type | Required | Description |
|---|---|---|---|
| ruling_id | UUID | Yes | System-generated unique identifier |
| ruling_type | Enum (ENUM-09) | Yes | Type of ruling |
| ruling_title | String (200) | Yes | Short descriptive title |
| ruling_text | Text | Yes | Full ruling with rationale |
| scriptural_basis | Text | Yes | Scripture or Tier 1 document citation |
| affected_documents | Array [Identifier] | Yes | Document references affected |
| affected_clusters | Array [Identifier] | Yes | Cluster IDs required to implement |
| vote_record | Object | Yes | See Vote Record sub-schema |
| quorum_confirmed | Boolean | Yes | True if quorum met per DOC-01.2 |
| effective_date | Date | Yes | Date ruling takes effect |
| ratification_date | Date | Yes | Date Council vote completed |
| ruling_status | Enum | Yes | Draft / Ratified / Superseded |

**Vote Record Sub-Schema:**

| Field | Type | Required |
|---|---|---|
| total_eligible_voters | Integer | Yes |
| votes_cast | Integer | Yes |
| votes_in_favor | Integer | Yes |
| votes_opposed | Integer | Yes |
| abstentions | Integer | Yes |
| quorum_threshold | Integer | Yes |
| quorum_met | Boolean | Yes |

**Validation Rules:**
- quorum_confirmed must be True before ruling_status = Ratified
- scriptural_basis is required — opinion-only rulings are rejected
- vote_record.quorum_met must be True and consistent with DOC-01.2 quorum requirements
- effective_date may be same as or after ratification_date — never before

**Constraints:**
- Ruling text is immutable once ratified — supersession requires new ruling
- Ruled-superseded records are retained permanently
- All rulings propagate via IC-08 and are stored in CLU-02.4

**Relationships:**
- 1:1 with OBJ-15 (Ruling Propagation Record) — one propagation per ruling
- References OBJ-04 (Council Member Record) in vote record
- Stored in and retrieved from CLU-02.4 (Amendment and Ruling Registry)

---

### OBJ-15 — RULING PROPAGATION RECORD

**Owner:** CLU-02.1 — Governing Authority Module
**Description:** Tracks the distribution and acknowledgment of a ratified Council ruling to all affected clusters.

| Field | Type | Required | Description |
|---|---|---|---|
| propagation_id | UUID | Yes | System-generated unique identifier |
| ruling_id | Foreign Key → OBJ-14 | Yes | Source ruling |
| registry_entry_ref | Identifier | Yes | CLU-02.4 registry entry |
| cluster_notification_log | Map [ClusterID → Enum] | Yes | Acknowledged / Pending / Failed per cluster |
| document_amendment_refs | Array [Identifier] | No | Amendment records in affected documents |
| propagation_status | Enum | Yes | Complete / Partial / Failed |
| propagation_date | Date | Yes | System-generated |
| effective_date | Date | Yes | Copied from OBJ-14 |

**Validation Rules:**
- All entries in affected_clusters (from OBJ-14) must appear in cluster_notification_log
- propagation_status = Complete requires all clusters in log to show Acknowledged
- document_amendment_refs must reference actual document amendment entries

**Constraints:**
- Failed notifications trigger escalation to CLU-02.3
- Propagation records are permanent audit artifacts

**Relationships:**
- 1:1 with OBJ-14 (Council Ruling Record)
- Delivers to OBJ-22 (Lexicon Update Record) when ruling concerns lexicon
- Triggers document amendments in affected Tier documents

---

### OBJ-16 — CAPITAL SOURCE RECORD

**Owner:** CLU-03.1 — Capital Source Integrity Filter
**Description:** Identity and affiliation record for every individual, organization, or institution that proposes to provide capital to the platform.

| Field | Type | Required | Description |
|---|---|---|---|
| source_id | UUID | Yes | System-generated unique identifier |
| source_name | String (200) | Yes | Legal name of donor or institution |
| source_type | Enum (ENUM-13) | Yes | Source classification |
| source_affiliation | Text | No | Known organizational affiliations |
| proposed_conditions | Text | No | Any conditions attached to proposed funds |
| first_submission_date | Date | Yes | Date source first submitted for evaluation |
| last_evaluated_date | Date | Yes | System-generated on most recent evaluation |
| current_clearance_id | Foreign Key → OBJ-17 | No | Most recent clearance record |

**Validation Rules:**
- source_type = OTHER requires source_affiliation or description to be populated
- source_name must be unique per source record — duplicates are flagged for review

**Constraints:**
- All capital sources must have an OBJ-17 (Capital Source Clearance) before any funds enter pipeline
- Source records are permanent — no deletion

**Relationships:**
- 1:Many with OBJ-17 (Capital Source Clearance) — may have multiple evaluations over time
- Referenced in CLU-03.2 and CLU-06.1 pipelines after Cleared status

---

### OBJ-17 — CAPITAL SOURCE CLEARANCE

**Owner:** CLU-03.1 — Capital Source Integrity Filter
**Description:** The integrity evaluation outcome for a capital source. Required before any funds from that source enter the platform pipeline.

| Field | Type | Required | Description |
|---|---|---|---|
| clearance_id | UUID | Yes | System-generated unique identifier |
| source_id | Foreign Key → OBJ-16 | Yes | Evaluated source |
| integrity_status | Enum (ENUM-07) | Yes | Cleared / Conditional / Disqualified |
| disqualification_basis | Text | No | Required if Disqualified |
| conditional_requirements | Text | No | Required if Conditional |
| conditions_acknowledged | Boolean | No | Required for Conditional → Cleared transition |
| review_authority | Identifier | Yes | Reviewing module or Council referral |
| clearance_date | Date | Yes | System-generated |
| expiry_date | Date | Yes | Date clearance requires re-evaluation |
| evaluation_notes | Text | No | Internal review notes |

**Validation Rules:**
- integrity_status = Cleared requires expiry_date to be set
- Conditional status cannot advance to pipeline without conditions_acknowledged = True
- disqualification_basis required when integrity_status = Disqualified

**Constraints:**
- Disqualified sources may not be resubmitted without documented basis for reversal
- Clearance expiry requires re-evaluation — expired clearance is not active clearance
- All disqualifications route to CLU-03.4 for financial integrity reporting

**Relationships:**
- Many:1 with OBJ-16 (Capital Source Record)
- Cleared status enables entry to CLU-03.2 and CLU-06.1 pipelines

---

### OBJ-18 — FUND ALLOCATION RECORD

**Owner:** CLU-03.5 — Fund Allocation Logic
**Description:** Records a Council-authorized allocation decision — what funds go where and under what authority.

| Field | Type | Required | Description |
|---|---|---|---|
| allocation_id | UUID | Yes | System-generated unique identifier |
| allocation_type | Enum | Yes | Deployment / Operations / Training / Reserve |
| allocated_amount | Decimal | Yes | Authorized amount |
| destination_id | Identifier | Yes | Hub or operational unit receiving allocation |
| council_authorization_ref | Identifier | Yes | CLU-02.1 authorization record |
| sufficiency_compliance_ref | Identifier | Yes | CLU-06.4 compliance record |
| effective_date | Date | Yes | Date funds become available |
| allocation_status | Enum | Yes | Pending / Active / Disbursed / Closed |
| created_date | Date | Yes | System-generated |

**Validation Rules:**
- council_authorization_ref must reference a Ratified ruling (OBJ-14)
- allocated_amount must not breach sufficiency standard — validated against CLU-06.4
- destination_id must reference an active hub or operational unit

**Constraints:**
- No disbursement proceeds without council_authorization_ref
- Closed allocations are permanent records

**Relationships:**
- 1:1 with OBJ-19 (Disbursement Authorization) — per allocation event
- References OBJ-14 (Council Ruling Record) for authorization

---

### OBJ-19 — DISBURSEMENT AUTHORIZATION

**Owner:** CLU-06.6 — Deployment Funding Logic
**Description:** The authorization record enabling actual disbursement of funds from an approved allocation to a hub or operational unit.

| Field | Type | Required | Description |
|---|---|---|---|
| disbursement_authorization_id | UUID | Yes | System-generated unique identifier |
| allocation_id | Foreign Key → OBJ-18 | Yes | Source allocation record |
| destination_id | Identifier | Yes | Receiving hub or unit |
| authorized_amount | Decimal | Yes | Confirmed disbursement amount |
| disbursement_status | Enum (ENUM-14) | Yes | Current status |
| contingency_conditions | Text | No | If Contingent — required conditions |
| denial_basis | Text | No | If Denied — stated reason |
| authorization_date | Date | Yes | System-generated |
| expiry_date | Date | Yes | Date authorization lapses if unused |
| disbursement_date | Date | No | Populated when Disbursed |
| reporting_ref | Identifier | No | CLU-06.5 reporting record |

**Validation Rules:**
- authorized_amount may not exceed OBJ-18.allocated_amount
- expiry_date must be set — no open-ended authorizations
- disbursement_status = Disbursed requires disbursement_date to be populated
- Denied status requires denial_basis to be populated

**Constraints:**
- Expired authorizations require new authorization — no extension without CLU-06.6 action
- Denial records are permanent
- All disbursements feed CLU-06.5 reporting

**Relationships:**
- 1:1 with OBJ-18 (Fund Allocation Record)
- Consumed by OBJ-25 (Deployment Funding Authorization) for hub deployment
- Reported through CLU-06.5

---

### OBJ-20 — LANGUAGE COMPLIANCE CLEARANCE

**Owner:** CLU-05.1 — Semantic Authority Enforcer
**Description:** Records the language compliance review outcome for a platform document or communication. Required before any document achieves platform status or any communication is released.

| Field | Type | Required | Description |
|---|---|---|---|
| clearance_id | UUID | Yes | System-generated unique identifier |
| review_request_id | Identifier | Yes | Originating request |
| content_ref | Identifier | Yes | Reference to reviewed content |
| content_type | Enum (ENUM-08) | Yes | Type of content |
| requesting_cluster | Identifier | Yes | Originating cluster |
| compliance_status | Enum (ENUM-07) | Yes | Cleared / Flagged / Disqualified |
| flagged_terms | Array [Object] | No | Term + context + correction guidance per flag |
| disqualified_terms | Array [Object] | No | Term + disqualification basis per disqualification |
| correction_guidance | Text | No | Authorized alternative language |
| resubmission_ref | Identifier | No | Links to prior clearance if resubmission |
| submitted_date | Date | Yes | System-generated |
| clearance_date | Date | No | Date review completed |

**Flagged Term Sub-Schema:**

| Field | Type |
|---|---|
| term | String |
| context | Text |
| lexicon_ref | Identifier |
| correction_guidance | Text |

**Validation Rules:**
- Cleared status requires flagged_terms and disqualified_terms to be empty
- Disqualified status requires at least one entry in disqualified_terms
- Flagged status requires at least one entry in flagged_terms
- resubmission_ref required if prior review exists for same content_ref

**Constraints:**
- Disqualified terms automatically route to CLU-05.5 (Disqualified Language Filter)
- Documents may not achieve platform status without Cleared status on file
- Lexicon gap flags (term not in DOC-03.1) route to CLU-05.2 for submission

**Relationships:**
- References DOC-03.1 (Platform Lexicon) entries for each flagged or disqualified term
- Disqualifications feed OBJ-22 (Lexicon Update Record) via CLU-05.5
- All clusters produce requests; CLU-05.1 produces clearance records

---

### OBJ-21 — LEXICON ENTRY

**Owner:** CLU-05.2 — Lexicon Management System (authoritative content in DOC-03.1)
**Description:** A single authorized term entry in the Platform Lexicon. Defines what each term means, its authority, and its constraints.

| Field | Type | Required | Description |
|---|---|---|---|
| entry_id | UUID | Yes | System-generated unique identifier |
| term | String (100) | Yes | Authorized term — exact spelling and capitalization |
| domain | Enum | Yes | Identity / Formation / Community / Authority / Restoration / Mission |
| definition | Text | Yes | Authoritative definition |
| scriptural_anchor | Text | Yes | Primary Scripture reference(s) |
| theological_context | Text | Yes | Theological framework for the term |
| disqualified_uses | Array [Text] | Yes | Uses that are explicitly disallowed |
| related_terms | Array [Foreign Key → OBJ-21] | No | Cross-references to other lexicon entries |
| entry_status | Enum | Yes | Active / Disqualified / Superseded |
| council_ruling_ref | Identifier | Yes | CLU-02.4 ruling authorizing the entry |
| created_date | Date | Yes | System-generated |
| last_amended_date | Date | No | Populated on amendment |
| superseded_by | Foreign Key → OBJ-21 | No | Links to replacement entry if Superseded |

**Validation Rules:**
- term must be unique in the Active lexicon
- council_ruling_ref required — no entries without Council authorization
- disqualified_uses must contain at least one entry
- scriptural_anchor must cite at least one specific passage

**Constraints:**
- Entries may not be deleted — status changes to Disqualified or Superseded only
- Entry amendments require new council_ruling_ref
- All platform language resolves to an Active lexicon entry or is flagged

**Relationships:**
- Many:Many with itself via related_terms
- Referenced by OBJ-20 (Language Compliance Clearance) for flagging
- Updated via OBJ-22 (Lexicon Update Record)
- Authoritative content resides in DOC-03.1

---

### OBJ-22 — LEXICON UPDATE RECORD

**Owner:** CLU-05.2 — Lexicon Management System
**Description:** Records a single update event to the Platform Lexicon — new entry, amendment, or disqualification — and tracks its propagation to all clusters.

| Field | Type | Required | Description |
|---|---|---|---|
| update_id | UUID | Yes | System-generated unique identifier |
| update_type | Enum (ENUM-12) | Yes | New-entry / Amendment / Disqualification |
| term | String (100) | Yes | Affected term |
| updated_entry_ref | Foreign Key → OBJ-21 | Yes | Links to updated OBJ-21 entry |
| council_ruling_ref | Identifier | Yes | CLU-02.4 ruling authorizing the update |
| effective_date | Date | Yes | Date update takes effect |
| propagation_id | Foreign Key → OBJ-15 | No | Links to ruling propagation record |
| cluster_notification_log | Map [ClusterID → Enum] | Yes | Acknowledged / Pending / Failed |
| compliance_audit_triggered | Boolean | Yes | True if update_type = Disqualification |
| audit_ref | Identifier | No | CLU-05.3 audit record if triggered |
| propagation_date | Date | Yes | System-generated |

**Validation Rules:**
- council_ruling_ref required — no unilateral updates
- Disqualification updates must set compliance_audit_triggered = True
- All clusters must appear in cluster_notification_log

**Constraints:**
- Lexicon updates propagate to all clusters — no selective distribution
- Disqualification audit must be initiated on same date as propagation
- Update records are permanent

**Relationships:**
- 1:1 with OBJ-21 (Lexicon Entry) — per update event
- References OBJ-14 (Council Ruling Record) via council_ruling_ref
- Triggers CLU-05.3 audit when update_type = Disqualification

---

### OBJ-23 — HUB HEALTH ASSESSMENT

**Owner:** CLU-04.6 — Hub Health Assessment
**Description:** Periodic or triggered composite health evaluation of an active hub.

| Field | Type | Required | Description |
|---|---|---|---|
| health_assessment_id | UUID | Yes | System-generated unique identifier |
| hub_id | Foreign Key → OBJ-03 | Yes | Assessed hub |
| hub_leader_id | Identifier | Yes | Current Hub Leader |
| assessment_type | Enum | Yes | Periodic / Triggered |
| assessment_date | Date | Yes | System-generated |
| health_score | Decimal (0–100) | Yes | Composite health score |
| below_threshold | Boolean | Yes | True if health_score below defined minimum |
| consecutive_below_threshold | Integer | Yes | Running count of consecutive below-threshold assessments |
| risk_areas | Array [Enum] | Yes | Formation-outcomes / Covenant-vitality / Hospitality / Rhythm-adherence / Leadership-integrity |
| risk_area_details | Map [RiskArea → Text] | No | Narrative per flagged risk area |
| critical_risk_present | Boolean | Yes | True if any single risk area is Critical severity |
| hub_leader_self_assessment_ref | Identifier | No | Hub Leader submission reference |
| facilitator_observation_refs | Array [Identifier] | No | Facilitator field observation references |
| escalation_required | Boolean | Yes | True if consecutive_below_threshold ≥ 2 OR critical_risk_present |

**Validation Rules:**
- consecutive_below_threshold is system-calculated — not manually entered
- escalation_required must be True if consecutive_below_threshold ≥ 2 or critical_risk_present = True
- health_score is calculated from weighted component scores — algorithm governed by DOC-02.2

**Constraints:**
- Health assessments are conducted at minimum on defined periodic schedule
- Hub Leader and Council access only — not surfaced to individual participants
- Assessment records are permanent

**Relationships:**
- Many:1 with OBJ-03 (Hub Record)
- Triggers OBJ-24 (Hub Health Escalation) when escalation_required = True
- Feeds aggregate data to Council via IC-06

---

### OBJ-24 — HUB HEALTH ESCALATION

**Owner:** CLU-04.6 → CLU-02.1
**Description:** Formal escalation record created when a hub health assessment meets escalation threshold. Tracks Council response and intervention.

| Field | Type | Required | Description |
|---|---|---|---|
| escalation_id | UUID | Yes | System-generated unique identifier |
| health_assessment_id | Foreign Key → OBJ-23 | Yes | Triggering assessment |
| hub_id | Foreign Key → OBJ-03 | Yes | Escalated hub |
| hub_leader_id | Identifier | Yes | Current Hub Leader |
| escalation_trigger | Enum | Yes | Consecutive-threshold / Critical-risk / Council-initiated |
| escalation_status | Enum | Yes | Received / Under-review / Intervention-active / Resolved |
| intervention_type | Enum (ENUM-11) | No | Set when intervention determined |
| council_response_record | Text | No | Council action documentation |
| council_acknowledgment_date | Date | No | Date Council acknowledged escalation |
| intervention_start_date | Date | No | Date intervention began |
| resolution_date | Date | No | Date escalation resolved |
| resolution_documentation | Text | No | Required on resolution |

**Validation Rules:**
- escalation_status = Resolved requires resolution_documentation to be present
- intervention_type required when escalation_status = Intervention-active
- council_acknowledgment_date must be within required period per DOC-01.2

**Constraints:**
- Mandatory escalation on threshold breach — not discretionary
- Resolution does not delete the escalation record — retained in audit trail
- Escalation records are accessible to Hub Leader (own hub) and Council only

**Relationships:**
- 1:1 with OBJ-23 (Hub Health Assessment) — one escalation per triggering assessment
- References OBJ-03 (Hub Record)
- Received and acted upon by CLU-02.1 (Governing Authority Module)
- Stored in CLU-02.4 (Amendment and Ruling Registry) as governance record

---

### OBJ-25 — DEPLOYMENT FUNDING AUTHORIZATION

**Owner:** CLU-06.6 — Deployment Funding Logic
**Description:** Authorizes and records the financial clearance for a specific hub deployment event, enabling the Hub Formation Protocol to proceed to the launch phase.

| Field | Type | Required | Description |
|---|---|---|---|
| funding_authorization_id | UUID | Yes | System-generated unique identifier |
| deployment_request_id | Identifier | Yes | CLU-04.1 deployment record |
| hub_id | Foreign Key → OBJ-03 | Yes | Hub being funded for deployment |
| deployment_template_ref | Identifier | Yes | Phase 9 template reference |
| council_authorization_ref | Identifier | Yes | CLU-02.1 authorization record |
| allocation_id | Foreign Key → OBJ-18 | Yes | Source fund allocation |
| requested_amount | Decimal | Yes | Amount requested per deployment template |
| authorized_amount | Decimal | Yes | Confirmed authorization amount |
| funding_status | Enum (ENUM-14) | Yes | Authorized / Contingent / Denied / Held |
| contingency_conditions | Text | No | Required if Contingent |
| denial_basis | Text | No | Required if Denied |
| authorization_date | Date | Yes | System-generated |
| expiry_date | Date | Yes | Date authorization lapses if unused |
| initiation_deadline | Date | Yes | Date by which deployment must begin |

**Validation Rules:**
- authorized_amount may not exceed requested_amount without amended Council authorization
- funding_status = Authorized requires council_authorization_ref to reference a Ratified ruling
- expiry_date must be set and must be after authorization_date
- Denied status requires denial_basis

**Constraints:**
- Hub Formation Protocol (CLU-04.1) may not proceed to launch phase without Authorized status
- Expired authorizations are not revivable without new CLU-06.6 action
- Denied records are permanent

**Relationships:**
- References OBJ-03 (Hub Record)
- References OBJ-18 (Fund Allocation Record)
- Enables OBJ-03 hub_status progression from Forming to Active
- Reported through CLU-06.5 and CLU-03.4

---

### OBJ-26 — ASSESSMENT COMPLETION RECORD

**Owner:** CLU-01.1 — Fracture Assessment Engine
**Description:** Records the completion of a single assessment instrument (DOC-04.1, DOC-04.2, or DOC-04.3) for a single participant.

| Field | Type | Required | Description |
|---|---|---|---|
| assessment_completion_id | UUID | Yes | System-generated unique identifier |
| participant_id | Foreign Key → OBJ-01 | Yes | Assessed participant |
| facilitator_id | Foreign Key → OBJ-02 | Yes | Administering facilitator |
| instrument_type | Enum | Yes | DOC_04_1 / DOC_04_2 / DOC_04_3 |
| instrument_ref | Identifier | Yes | Reference to the specific instrument document |
| completion_status | Enum | Yes | Complete / Partial / Voided |
| completion_date | Date | Yes | Date instrument was completed |
| current_stage_at_completion | Enum (ENUM-01) | Yes | Participant's stage when assessment completed |
| facilitator_verified | Boolean | Yes | Facilitator has reviewed and accepted the assessment |
| voided_reason | Text | No | Required if completion_status = Voided |
| created_date | Date | Yes | System-generated |

**Validation Rules:**
- facilitator_verified must be True before assessment feeds into OBJ-05 or OBJ-07
- Voided assessments require voided_reason to be populated
- Partial assessments may not be used to finalize OBJ-05 (Fracture Domain Profile)
- DOC_04_3 assessments must be completed within required interval per DOC-03.4 thresholds

**Constraints:**
- Assessment data belongs to the participant — platform does not own the data
- Voided records are retained with voided status — not deleted
- Each instrument_type has its own completion criteria governed by the relevant DOC-04.x document

**Relationships:**
- Many:1 with OBJ-01 (Participant Record)
- Referenced by OBJ-05 (Fracture Domain Profile) as source data
- Referenced by OBJ-07 (Milestone Completion Record) for milestone support
- Stored in OBJ-11 (Formation Record)

---

### OBJ-27 — COVENANT MEMBER RECORD

**Owner:** CLU-04.2 — Covenant Community Engine
**Description:** Records the covenant membership status and accountability history of an individual within an Emmaus Road hub community.

| Field | Type | Required | Description |
|---|---|---|---|
| covenant_member_id | UUID | Yes | System-generated unique identifier |
| participant_id | Foreign Key → OBJ-01 | Yes | Linked participant record |
| hub_id | Foreign Key → OBJ-03 | Yes | Hub covenant membership |
| covenant_ref | Identifier | Yes | Signed covenant document reference |
| covenant_status | Enum | Yes | Active / Renewal-due / Under-review / Released |
| covenant_start_date | Date | Yes | Date covenant entered |
| last_renewal_date | Date | No | Date of most recent renewal |
| renewal_due_date | Date | Yes | Upcoming renewal date |
| accountability_action_refs | Array [Identifier] | No | Any accountability action records |
| breach_record_refs | Array [Identifier] | No | Any covenant breach records |
| release_date | Date | No | Populated if covenant_status = Released |
| release_type | Enum | No | Voluntary / Facilitated / Required |
| release_documentation | Text | No | Required on release |

**Validation Rules:**
- covenant_ref must reference a current, valid covenant document
- renewal_due_date must be future-dated on record creation
- Release requires release_documentation regardless of release_type
- covenant_status = Under-review requires an active accountability_action_ref

**Constraints:**
- Release is not punitive — documentation must reflect restorative posture
- Released members may reenter covenant process through standard intake
- Records are permanent — status changes only

**Relationships:**
- 1:1 with OBJ-01 (Participant Record) per hub
- References OBJ-03 (Hub Record)
- Feeds covenant compliance data to OBJ-23 (Hub Health Assessment)
- Informs OBJ-10 (Hub Routing Record) for appropriate hospitality assignment

---

## OBJECT RELATIONSHIP MAP

```
OBJ-01 Participant Record
    ├── 1:1  OBJ-11  Formation Record
    ├── 1:N  OBJ-05  Fracture Domain Profile
    ├── 1:1  OBJ-06  Formation Pathway Assignment (active)
    ├── 1:N  OBJ-07  Milestone Completion Record
    ├── 1:N  OBJ-09  Blockage Record
    ├── 1:N  OBJ-26  Assessment Completion Record
    ├── 1:1  OBJ-27  Covenant Member Record (per hub)
    └── N:1  OBJ-02  Facilitator Record
             └── N:1  OBJ-03  Hub Record
                          ├── 1:N  OBJ-23  Hub Health Assessment
                          │         └── 1:1  OBJ-24  Hub Health Escalation
                          └── 1:1  OBJ-25  Deployment Funding Authorization
                                   └── N:1  OBJ-18  Fund Allocation Record

OBJ-05 Fracture Domain Profile
    └── drives OBJ-06  Formation Pathway Assignment
              └── drives OBJ-10  Hub Routing Record

OBJ-07 Milestone Completion Record
    └── aggregates into OBJ-08  Stage Progression Evaluation
              └── checked against OBJ-09  Blockage Record

OBJ-13 Theological Review Record
    └── feeds OBJ-14  Council Ruling Record
              └── 1:1  OBJ-15  Ruling Propagation Record

OBJ-16 Capital Source Record
    └── 1:N  OBJ-17  Capital Source Clearance
              └── enables OBJ-18  Fund Allocation Record
                        └── 1:1  OBJ-19  Disbursement Authorization
                                 └── links to OBJ-25  Deployment Funding Auth

OBJ-21 Lexicon Entry
    └── managed via OBJ-22  Lexicon Update Record
    └── referenced by OBJ-20  Language Compliance Clearance

OBJ-11 Formation Record
    └── anonymized aggregate → OBJ-12  Aggregate Formation Report
```

---

## AMENDMENT PROTOCOL

Amendments to any object definition require:
1. Council of Metanoia review
2. Documented rationale referencing affected interface contracts (ICM-01)
3. Version increment on affected object definitions and this document
4. Notification to all affected clusters via IC-08

---

## AUTHORIZATION RECORD

| Role | Name | Status |
|---|---|---|
| Architect | — | Pending Council signature |
| Systems Engineer | — | Pending |
| Documentation Lead | — | Pending |

**Amendment Log:**

| Version | Date | Change | Authority |
|---|---|---|---|
| 1.0 | 2026-03-30 | Initial registry created — 27 objects, 14 enumerations defined | Architect Mode |
