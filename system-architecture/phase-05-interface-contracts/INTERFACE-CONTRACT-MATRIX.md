# FORMATION INTELLIGENCE PLATFORM
## INTERFACE CONTRACT MATRIX

**Document Reference:** ICM-01
**Version:** 1.0
**Status:** Active
**Owning Authority:** Council of Metanoia
**Prepared By:** Architect Mode — Claude Code
**Date:** 2026-03-30
**Review Cycle:** Upon structural amendment only

---

## PURPOSE

This matrix defines every interface contract governing data flow between clusters and submodules in the Formation Intelligence Platform. Each contract specifies: interface name, purpose, input schema, output schema, allowed operations, dependency rules, error conditions, and interacting modules.

No data may pass between modules outside a defined interface contract. All inter-module communication is governed by the contracts in this document.

---

## CONTRACT INDEX

| ID | Interface Name | Producer | Consumer |
|---|---|---|---|
| IC-01 | Assessment-to-Fracture Profile | CLU-01.1 | CLU-01.2, CLU-01.5 |
| IC-02 | Fracture Profile-to-Pathway Assignment | CLU-01.1 | CLU-01.5 |
| IC-03 | Milestone-to-Stage Progression | CLU-01.3 | CLU-01.2 |
| IC-04 | Blockage-to-Stage Hold | CLU-01.4 | CLU-01.2 |
| IC-05 | Pathway-to-Hub Routing | CLU-01.5 | CLU-04 |
| IC-06 | Formation Record Feed | CLU-01.6 | CLU-02, CLU-06 |
| IC-07 | Theological Review Request | All Clusters | CLU-02.2 |
| IC-08 | Council Ruling Propagation | CLU-02.1 | CLU-02.4, All Clusters |
| IC-09 | Capital Source Integrity Clearance | CLU-03.1 | CLU-03.2, CLU-06.1 |
| IC-10 | Fund Allocation Authorization | CLU-03.5 | CLU-06.6 |
| IC-11 | Language Compliance Clearance | CLU-05.1 | All Document-Producing Modules |
| IC-12 | Lexicon Update Propagation | CLU-05.2 | All Clusters |
| IC-13 | Hub Health Escalation | CLU-04.6 | CLU-02.1 |
| IC-14 | Deployment Funding Authorization | CLU-06.6 | CLU-04.1 |

---

---

## IC-01 — ASSESSMENT-TO-FRACTURE PROFILE

**Interface Name:** Assessment-to-Fracture Profile
**Version:** 1.0
**Status:** Active

### Purpose
Transfers completed assessment data from intake and fracture map instruments into a structured, actionable Fracture Domain Profile. This is the primary diagnostic intake interface of the platform.

### Producer
CLU-01.1 — Fracture Assessment Engine

### Consumers
- CLU-01.2 — Stage Progression Logic (entry stage determination)
- CLU-01.5 — Formation Pathway Router (pathway assignment)

### Input Schema

| Field | Type | Required | Source |
|---|---|---|---|
| participant_id | Identifier | Yes | DOC-04.1 completion record |
| intake_questionnaire_ref | Document reference | Yes | DOC-04.1 |
| fracture_map_ref | Document reference | Yes | DOC-04.2 |
| facilitator_id | Identifier | Yes | Assigned facilitator record |
| facilitator_notes | Text | No | Facilitator field submission |
| assessment_date | Date | Yes | System-generated |

### Output Schema

| Field | Type | Description |
|---|---|---|
| participant_id | Identifier | Links to formation record in CLU-01.6 |
| fracture_profile_id | Identifier | Unique profile record |
| active_domains | Array | One or more of: Identity / Authority / Relational / Vocational / Worldview |
| severity_per_domain | Map | L1 / L2 / L3 per active domain |
| origin_per_domain | Map | Self-generated / Externally inflicted / Systemic per active domain |
| recommended_entry_stage | Enum | Stage 1–5 (typically Stage 1) |
| profile_status | Enum | Draft / Facilitator-reviewed / Finalized |
| profile_date | Date | System-generated |

### Allowed Operations
- CREATE fracture profile (first assessment)
- UPDATE fracture profile (re-assessment trigger)
- READ by assigned facilitator, Hub Leader, Council (aggregate only)
- No DELETE operation permitted

### Dependency Rules
- DOC-04.2 must be completed before profile may be finalized
- L3 severity designation holds profile in Draft status until facilitator review
- Profile may not be finalized without facilitator_id present

### Error Conditions

| Error | Condition | Resolution |
|---|---|---|
| INCOMPLETE_ASSESSMENT | DOC-04.2 not completed | Hold profile in Draft; notify facilitator |
| L3_REVIEW_REQUIRED | L3 severity detected | Route to facilitator review queue; block finalization |
| MISSING_FACILITATOR | No facilitator_id on record | Block profile creation; require assignment first |
| DOMAIN_CONFLICT | Contradictory domain indicators | Flag for facilitator manual review |

### Interacting Modules
CLU-01.1 → CLU-01.2, CLU-01.5, CLU-01.6

---

## IC-02 — FRACTURE PROFILE-TO-PATHWAY ASSIGNMENT

**Interface Name:** Fracture Profile-to-Pathway Assignment
**Version:** 1.0
**Status:** Active

### Purpose
Translates a finalized Fracture Domain Profile into a specific formation pathway assignment — identifying which stage, domain sequence, resources, and facilitator configuration are appropriate for the individual.

### Producer
CLU-01.1 — Fracture Assessment Engine (finalized profile)

### Consumer
CLU-01.5 — Formation Pathway Router

### Input Schema

| Field | Type | Required | Source |
|---|---|---|---|
| fracture_profile_id | Identifier | Yes | IC-01 output |
| active_domains | Array | Yes | IC-01 output |
| severity_per_domain | Map | Yes | IC-01 output |
| recommended_entry_stage | Enum | Yes | IC-01 output |
| hub_id | Identifier | Yes | Participant hub assignment |
| facilitator_id | Identifier | Yes | Assigned facilitator |

### Output Schema

| Field | Type | Description |
|---|---|---|
| pathway_id | Identifier | Unique pathway record |
| participant_id | Identifier | Links to formation record |
| assigned_stage | Enum | Active formation stage (1–5) |
| domain_sequence | Array | Ordered domain focus sequence |
| assigned_facilitator_id | Identifier | Confirmed facilitator assignment |
| hub_session_refs | Array | Linked hub session schedule entries |
| pathway_status | Enum | Active / On-hold / Complete |
| assignment_date | Date | System-generated |

### Allowed Operations
- CREATE pathway (initial assignment)
- UPDATE pathway (re-assessment or stage transition)
- READ by assigned facilitator, Hub Leader
- No DELETE operation permitted

### Dependency Rules
- Fracture profile must be in Finalized status before pathway is created
- Hub must have active status in CLU-04 directory before routing
- Facilitator must be available per CLU-02 operational data

### Error Conditions

| Error | Condition | Resolution |
|---|---|---|
| PROFILE_NOT_FINALIZED | Profile still in Draft | Block pathway creation; return to IC-01 |
| HUB_UNAVAILABLE | Hub at capacity or inactive | Hold assignment; notify Hub Leader |
| FACILITATOR_UNAVAILABLE | No facilitator available | Escalate to Hub Leader for assignment |
| STAGE_CONFLICT | Recommended stage conflicts with prior record | Require facilitator adjudication |

### Interacting Modules
CLU-01.1 → CLU-01.5 → CLU-04, CLU-01.6

---

## IC-03 — MILESTONE-TO-STAGE PROGRESSION

**Interface Name:** Milestone-to-Stage Progression
**Version:** 1.0
**Status:** Active

### Purpose
Transfers milestone completion data from the Milestone Tracking System to the Stage Progression Logic module. Governs whether an individual has met the milestone threshold required for stage advancement evaluation.

### Producer
CLU-01.3 — Milestone Tracking System

### Consumer
CLU-01.2 — Stage Progression Logic

### Input Schema

| Field | Type | Required | Source |
|---|---|---|---|
| participant_id | Identifier | Yes | Formation record |
| current_stage | Enum | Yes | Active stage assignment |
| milestones_completed | Array | Yes | Facilitator-attested completions |
| milestones_pending | Array | Yes | Incomplete milestones for current stage |
| facilitator_attestation_ids | Array | Yes | Attestation records |
| last_assessment_date | Date | Yes | DOC-04.3 completion date |

### Output Schema

| Field | Type | Description |
|---|---|---|
| progression_evaluation_id | Identifier | Unique evaluation record |
| participant_id | Identifier | Links to formation record |
| milestone_threshold_met | Boolean | True if all required milestones complete |
| completion_percentage | Numeric | Percentage of stage milestones complete |
| outstanding_milestones | Array | Remaining required milestones |
| advancement_eligible | Boolean | Ready for Stage Progression Logic review |
| evaluation_date | Date | System-generated |

### Allowed Operations
- CREATE evaluation record (triggered by milestone completion event)
- READ by CLU-01.2, assigned facilitator
- UPDATE when milestone status changes
- No DELETE operation permitted

### Dependency Rules
- All milestones in DOC-03.4 for current stage must be evaluated (complete or pending)
- Facilitator attestation required for each completed milestone
- Evaluation record must reference last completed DOC-04.3 assessment

### Error Conditions

| Error | Condition | Resolution |
|---|---|---|
| MISSING_ATTESTATION | Milestone marked complete without facilitator attestation | Revert to pending; notify facilitator |
| ASSESSMENT_OVERDUE | DOC-04.3 not completed within required interval | Flag for facilitator; hold evaluation |
| REGISTRY_MISMATCH | Milestone not found in DOC-03.4 | Reject; route to CLU-05 for lexicon/registry check |
| INCOMPLETE_STAGE_DATA | Current stage milestones not fully evaluated | Block evaluation record creation |

### Interacting Modules
CLU-01.3 → CLU-01.2 → CLU-01.6

---

## IC-04 — BLOCKAGE-TO-STAGE HOLD

**Interface Name:** Blockage-to-Stage Hold
**Version:** 1.0
**Status:** Active

### Purpose
Communicates active blockage flags from the Blockage Detection Module to Stage Progression Logic, preventing stage advancement until blockage is resolved.

### Producer
CLU-01.4 — Blockage Detection Module

### Consumer
CLU-01.2 — Stage Progression Logic

### Input Schema

| Field | Type | Required | Source |
|---|---|---|---|
| participant_id | Identifier | Yes | Formation record |
| blockage_id | Identifier | Yes | Blockage flag record |
| blockage_type | Enum | Yes | Formation / Relational / Spiritual / External |
| blockage_severity | Enum | Yes | Moderate / Significant / Critical |
| detection_trigger | Enum | Yes | Milestone-stall / Time-in-stage / Facilitator-submitted / Assessment-flag |
| facilitator_id | Identifier | Yes | Detecting facilitator |
| detection_date | Date | Yes | System-generated |

### Output Schema

| Field | Type | Description |
|---|---|---|
| hold_record_id | Identifier | Unique hold record |
| participant_id | Identifier | Links to formation record |
| hold_status | Enum | Active / Under-review / Resolved |
| advancement_blocked | Boolean | Always True while hold_status is Active |
| recommended_response | Text | Protocol from DOC-02.1 |
| escalation_required | Boolean | True if blockage_type is Spiritual or severity is Critical |
| hold_opened_date | Date | System-generated |
| hold_resolved_date | Date | Populated on resolution |

### Allowed Operations
- CREATE hold record (on blockage detection)
- UPDATE hold record (facilitator review actions, resolution)
- READ by assigned facilitator, Hub Leader; escalation cases by Council
- RESOLVE hold (requires documented facilitator clearance)
- No DELETE operation permitted

### Dependency Rules
- Spiritual blockage type automatically triggers escalation_required = True
- Critical severity automatically triggers escalation to Hub Leader
- Stage advancement in CLU-01.2 is blocked while any Active hold exists for participant

### Error Conditions

| Error | Condition | Resolution |
|---|---|---|
| UNRESOLVED_HOLD_ADVANCE | Advancement attempted with Active hold | Block advancement; return error to CLU-01.2 |
| SPIRITUAL_ESCALATION_MISSED | Spiritual blockage not escalated | System auto-escalates; notify Hub Leader |
| CLEARANCE_WITHOUT_DOCUMENTATION | Hold resolved without documented facilitator review | Reject resolution; require documentation |
| DUPLICATE_BLOCKAGE | Same blockage type re-flagged while hold Active | Merge records; update severity if escalated |

### Interacting Modules
CLU-01.4 → CLU-01.2, CLU-01.6, CLU-02 (Spiritual/Critical escalations)

---

## IC-05 — PATHWAY-TO-HUB ROUTING

**Interface Name:** Pathway-to-Hub Routing
**Version:** 1.0
**Status:** Active

### Purpose
Routes an individual's formation pathway assignment to the appropriate Emmaus Road hub, triggering session scheduling, facilitator confirmation, and hospitality integration.

### Producer
CLU-01.5 — Formation Pathway Router

### Consumer
CLU-04 — Emmaus Road (specifically 04.3 Household Rhythm Scheduler and 04.4 Hospitality Operations)

### Input Schema

| Field | Type | Required | Source |
|---|---|---|---|
| pathway_id | Identifier | Yes | IC-02 output |
| participant_id | Identifier | Yes | Formation record |
| assigned_stage | Enum | Yes | IC-02 output |
| domain_sequence | Array | Yes | IC-02 output |
| hub_id | Identifier | Yes | Assigned hub |
| session_type_requirements | Array | Yes | Stage-specific session types |
| facilitator_id | Identifier | Yes | Assigned facilitator |

### Output Schema

| Field | Type | Description |
|---|---|---|
| routing_record_id | Identifier | Unique routing record |
| hub_id | Identifier | Confirmed hub assignment |
| session_schedule_ref | Identifier | Links to CLU-04.3 schedule entry |
| hospitality_assignment_ref | Identifier | Links to CLU-04.4 hospitality record (if applicable) |
| routing_status | Enum | Confirmed / Pending-capacity / Cross-hub |
| hub_leader_notified | Boolean | Notification sent to Hub Leader |
| routing_date | Date | System-generated |

### Allowed Operations
- CREATE routing record (on pathway assignment)
- UPDATE routing record (on pathway adjustment or hub change)
- READ by facilitator, Hub Leader, CLU-04 operations
- No DELETE operation permitted

### Dependency Rules
- Hub must have Active status in CLU-04 directory
- Hub capacity must be confirmed available before routing_status = Confirmed
- Cross-hub routing requires Hub Leader notification on both hubs

### Error Conditions

| Error | Condition | Resolution |
|---|---|---|
| HUB_AT_CAPACITY | Hub cannot accept new participants | Set routing_status = Pending-capacity; notify Hub Leader |
| HUB_INACTIVE | Assigned hub is inactive or closed | Escalate to CLU-04.1 and CLU-01.5 for reassignment |
| CROSS_HUB_NOTIFICATION_FAILED | Notification not delivered | Retry; escalate to Hub Leader manually if unresolved |
| SESSION_TYPE_UNAVAILABLE | Required session type not offered at hub | Flag for Hub Leader to schedule or route cross-hub |

### Interacting Modules
CLU-01.5 → CLU-04.3, CLU-04.4, CLU-01.6

---

## IC-06 — FORMATION RECORD FEED

**Interface Name:** Formation Record Feed
**Version:** 1.0
**Status:** Active

### Purpose
Provides authorized read access to formation records from the Restoration Record Keeper to Council governance (aggregate only) and Capital Access Engine (anonymized aggregate only). No individual-level data crosses this interface to CLU-06.

### Producer
CLU-01.6 — Restoration Record Keeper

### Consumers
- CLU-02.1 — Governing Authority Module (aggregate governance reporting)
- CLU-06.5 — Capital Reporting Interface (anonymized aggregate only)

### Input Schema

| Field | Type | Required | Source |
|---|---|---|---|
| report_request_id | Identifier | Yes | Requesting module |
| requesting_module | Identifier | Yes | CLU-02.1 or CLU-06.5 |
| report_type | Enum | Yes | Governance / Capital |
| reporting_period | DateRange | Yes | Defined period |
| authorization_ref | Identifier | Yes | Council authorization record |

### Output Schema — Governance Report (CLU-02.1)

| Field | Type | Description |
|---|---|---|
| report_id | Identifier | Unique report record |
| reporting_period | DateRange | Covered period |
| total_participants | Numeric | Count only — no identifiers |
| stage_distribution | Map | Count per stage |
| domain_prevalence | Map | Count per fracture domain |
| blockage_frequency | Map | Count per blockage type |
| milestone_completion_rate | Numeric | Aggregate percentage |

### Output Schema — Capital Report (CLU-06.5)

| Field | Type | Description |
|---|---|---|
| report_id | Identifier | Unique report record |
| reporting_period | DateRange | Covered period |
| participant_count | Numeric | Count only — fully anonymized |
| stage_completion_count | Numeric | Participants completing each stage |
| program_utilization_rate | Numeric | Aggregate capacity utilization |

### Allowed Operations
- READ (report generation only — no write access across this interface)
- Reports are generated on schedule or Council request
- No individual record identifiers cross this interface

### Dependency Rules
- All reports require authorization_ref from an active Council authorization
- CLU-06.5 receives only anonymized aggregate — no domain or severity breakdowns
- Report generation triggers audit log entry in CLU-01.6

### Error Conditions

| Error | Condition | Resolution |
|---|---|---|
| MISSING_AUTHORIZATION | No valid Council authorization_ref | Block report generation; return error |
| PERIOD_EXCEEDS_RECORD | Requested period predates records | Return available data only; note gap |
| INDIVIDUAL_DATA_REQUEST | Request includes individual identifiers | Reject entire request; log attempt |
| UNAUTHORIZED_CONSUMER | Requesting module not CLU-02.1 or CLU-06.5 | Block; log; escalate to CLU-02.1 |

### Interacting Modules
CLU-01.6 → CLU-02.1, CLU-06.5

---

## IC-07 — THEOLOGICAL REVIEW REQUEST

**Interface Name:** Theological Review Request
**Version:** 1.0
**Status:** Active

### Purpose
Routes any platform document, content, language sample, or practice for theological review to CLU-02.2. Any cluster may initiate a review request. All new Tier documents must pass through this interface before platform status is granted.

### Producer
Any cluster — CLU-01 through CLU-06

### Consumer
CLU-02.2 — Theological Review Engine

### Input Schema

| Field | Type | Required | Source |
|---|---|---|---|
| review_request_id | Identifier | Yes | Requesting module |
| requesting_module | Identifier | Yes | Any cluster submodule |
| content_type | Enum | Yes | Document / Language / Practice / External-content |
| content_ref | Identifier or Text | Yes | Reference to content under review |
| review_priority | Enum | No | Routine / Urgent |
| submitted_date | Date | Yes | System-generated |

### Output Schema

| Field | Type | Description |
|---|---|---|
| review_id | Identifier | Unique review record |
| content_ref | Identifier | Links to reviewed content |
| clearance_status | Enum | Approved / Conditional / Disqualified |
| theological_rationale | Text | Scripture or Tier 1 document basis |
| conditional_requirements | Array | If Conditional — required modifications |
| disqualification_basis | Text | If Disqualified — full theological basis |
| review_date | Date | System-generated |
| reviewer_id | Identifier | Reviewing Council member |

### Allowed Operations
- CREATE review request (any module)
- READ clearance status by requesting module
- UPDATE status by CLU-02.2 only
- No DELETE operation permitted

### Dependency Rules
- All new Tier documents require Approved or Conditional status before deployment
- Conditional approvals must have requirements resolved before full platform status
- Disqualification records automatically route to CLU-02.4 (Amendment and Ruling Registry)

### Error Conditions

| Error | Condition | Resolution |
|---|---|---|
| CONTENT_NOT_SUBMITTED | Review requested without content_ref | Reject; require complete submission |
| REVIEWER_UNAVAILABLE | No Council member available for review | Queue request; notify Council Operations (02.3) |
| DISQUALIFICATION_OVERRIDE_ATTEMPT | Attempt to deploy disqualified content | Block deployment; log attempt; escalate to 02.1 |
| CONDITIONAL_UNRESOLVED | Conditional status with no resolution timeline | Escalate to 02.3 for scheduling |

### Interacting Modules
All Clusters → CLU-02.2 → CLU-02.4, CLU-05.1

---

## IC-08 — COUNCIL RULING PROPAGATION

**Interface Name:** Council Ruling Propagation
**Version:** 1.0
**Status:** Active

### Purpose
Distributes ratified Council rulings, amendments, and directives from the Governing Authority Module to all affected clusters and the Amendment and Ruling Registry. Ensures all platform components operate on current Council-authorized versions.

### Producer
CLU-02.1 — Governing Authority Module

### Consumers
- CLU-02.4 — Amendment and Ruling Registry (permanent record)
- All clusters — operational implementation of rulings

### Input Schema

| Field | Type | Required | Source |
|---|---|---|---|
| ruling_id | Identifier | Yes | Council session record |
| ruling_type | Enum | Yes | Amendment / Directive / Disqualification / Doctrinal-position |
| affected_documents | Array | Yes | Document references affected |
| affected_clusters | Array | Yes | Cluster IDs required to implement |
| ruling_text | Text | Yes | Full ruling with rationale |
| scriptural_basis | Text | Yes | Scripture or Tier 1 document citation |
| effective_date | Date | Yes | Date ruling takes effect |
| vote_record | Object | Yes | Member votes and quorum confirmation |

### Output Schema

| Field | Type | Description |
|---|---|---|
| propagation_id | Identifier | Unique propagation record |
| ruling_id | Identifier | Links to source ruling |
| registry_entry_ref | Identifier | CLU-02.4 registry entry |
| cluster_notification_log | Map | Notification status per affected cluster |
| document_amendment_refs | Array | Amendment records created in affected documents |
| propagation_status | Enum | Complete / Partial / Failed |
| propagation_date | Date | System-generated |

### Allowed Operations
- CREATE propagation record (on ruling ratification)
- READ by all clusters (their own notification records)
- Full read by CLU-02.4
- No UPDATE or DELETE on ruling text once propagated

### Dependency Rules
- Ruling may not propagate without confirmed quorum in vote_record
- Effective_date governs when clusters must implement — not propagation date
- All affected clusters must acknowledge receipt

### Error Conditions

| Error | Condition | Resolution |
|---|---|---|
| QUORUM_NOT_MET | Vote record does not show required quorum | Block propagation; return to Council session |
| CLUSTER_NOTIFICATION_FAILED | Acknowledgment not received from affected cluster | Retry; escalate to 02.3 if unresolved |
| CONFLICTING_RULING | New ruling conflicts with existing active ruling | Flag conflict; require Council adjudication before propagation |
| MISSING_SCRIPTURAL_BASIS | Ruling submitted without citation | Block propagation; return to 02.1 for completion |

### Interacting Modules
CLU-02.1 → CLU-02.4, All Clusters

---

## IC-09 — CAPITAL SOURCE INTEGRITY CLEARANCE

**Interface Name:** Capital Source Integrity Clearance
**Version:** 1.0
**Status:** Active

### Purpose
Communicates capital source integrity status from CLU-03.1 to downstream capital processing modules. No funds enter the platform pipeline without a Cleared status from this interface.

### Producer
CLU-03.1 — Capital Source Integrity Filter

### Consumers
- CLU-03.2 — Generative Giving Engine
- CLU-06.1 — Funding Stream Manager

### Input Schema

| Field | Type | Required | Source |
|---|---|---|---|
| source_id | Identifier | Yes | Donor or grant source record |
| source_type | Enum | Yes | Individual-donor / Foundation / Grant / Corporate / Other |
| source_affiliation | Text | No | Known organizational affiliations |
| proposed_conditions | Text | No | Any attached conditions on funds |
| evaluation_date | Date | Yes | System-generated |

### Output Schema

| Field | Type | Description |
|---|---|---|
| clearance_id | Identifier | Unique clearance record |
| source_id | Identifier | Links to source record |
| integrity_status | Enum | Cleared / Conditional / Disqualified |
| disqualification_basis | Text | If Disqualified — full stated reason |
| conditional_requirements | Text | If Conditional — required modifications |
| review_authority | Identifier | Reviewing module or Council referral |
| clearance_date | Date | System-generated |
| expiry_date | Date | Date clearance requires re-evaluation |

### Allowed Operations
- CREATE clearance record (on source submission)
- READ by CLU-03.2, CLU-06.1
- UPDATE on re-evaluation or conditional resolution
- No DELETE operation permitted

### Dependency Rules
- No capital may enter CLU-03.2 or CLU-06.1 pipeline without Cleared status
- Conditional sources require donor acknowledgment before Cleared status issued
- Disqualification records automatically route to CLU-03.4 for financial integrity reporting

### Error Conditions

| Error | Condition | Resolution |
|---|---|---|
| FUNDS_ENTERED_WITHOUT_CLEARANCE | Capital processed without Cleared status | Block; reverse transaction; log violation |
| DISQUALIFIED_SOURCE_RESUBMITTED | Previously disqualified source resubmitted | Reject; reference prior disqualification record |
| CONDITIONAL_UNACKNOWLEDGED | Donor has not acknowledged conditions | Hold Cleared status; notify CLU-03.6 |
| CLEARANCE_EXPIRED | Clearance past expiry_date | Require re-evaluation before further processing |

### Interacting Modules
CLU-03.1 → CLU-03.2, CLU-06.1, CLU-03.4

---

## IC-10 — FUND ALLOCATION AUTHORIZATION

**Interface Name:** Fund Allocation Authorization
**Version:** 1.0
**Status:** Active

### Purpose
Authorizes and transfers fund allocation decisions from CLU-03.5 to CLU-06.6 for deployment funding execution. Ensures all deployment capital has Council-authorized allocation backing before disbursement.

### Producer
CLU-03.5 — Fund Allocation Logic

### Consumer
CLU-06.6 — Deployment Funding Logic

### Input Schema

| Field | Type | Required | Source |
|---|---|---|---|
| allocation_id | Identifier | Yes | CLU-03.5 allocation record |
| allocation_type | Enum | Yes | Deployment / Operations / Training / Reserve |
| allocated_amount | Numeric | Yes | Authorized amount |
| destination_id | Identifier | Yes | Hub or operational unit ID |
| council_authorization_ref | Identifier | Yes | CLU-02.1 authorization record |
| effective_date | Date | Yes | Date funds available |
| sufficiency_compliance_ref | Identifier | Yes | CLU-06.4 compliance record |

### Output Schema

| Field | Type | Description |
|---|---|---|
| disbursement_authorization_id | Identifier | Unique disbursement record |
| allocation_id | Identifier | Links to CLU-03.5 record |
| destination_id | Identifier | Receiving hub or unit |
| authorized_amount | Numeric | Confirmed disbursement amount |
| disbursement_status | Enum | Authorized / Pending / Disbursed / Held |
| disbursement_date | Date | Actual disbursement date |
| reporting_ref | Identifier | Links to CLU-06.5 reporting record |

### Allowed Operations
- CREATE disbursement authorization (on allocation decision)
- UPDATE status through disbursement lifecycle
- READ by CLU-06.6, CLU-03.4, CLU-06.5
- No DELETE operation permitted

### Dependency Rules
- All allocations require council_authorization_ref from CLU-02.1
- Sufficiency compliance must be confirmed before authorization issued
- Deployment allocations must reference an active hub deployment record in CLU-04.1

### Error Conditions

| Error | Condition | Resolution |
|---|---|---|
| MISSING_COUNCIL_AUTHORIZATION | No CLU-02.1 authorization reference | Block disbursement; return to CLU-03.5 |
| SUFFICIENCY_VIOLATION | Allocation would breach sufficiency standard | Block; route to CLU-06.4 for review |
| DESTINATION_INACTIVE | Receiving hub or unit not active | Hold disbursement; notify CLU-04 and CLU-02.1 |
| AMOUNT_EXCEEDS_AUTHORIZATION | Disbursement amount exceeds authorized amount | Block; require new Council authorization |

### Interacting Modules
CLU-03.5 → CLU-06.6 → CLU-06.5, CLU-03.4

---

## IC-11 — LANGUAGE COMPLIANCE CLEARANCE

**Interface Name:** Language Compliance Clearance
**Version:** 1.0
**Status:** Active

### Purpose
Issues language compliance clearance to any platform document or communication that has passed semantic review. No document receives platform status and no communication is released without this clearance.

### Producer
CLU-05.1 — Semantic Authority Enforcer

### Consumers
All document-producing and communication-releasing modules across all clusters.

### Input Schema

| Field | Type | Required | Source |
|---|---|---|---|
| review_request_id | Identifier | Yes | Requesting module |
| content_type | Enum | Yes | Document / Communication / Training-material / External |
| content_ref | Identifier | Yes | Reference to content under review |
| requesting_cluster | Identifier | Yes | Originating cluster |
| submitted_date | Date | Yes | System-generated |

### Output Schema

| Field | Type | Description |
|---|---|---|
| clearance_id | Identifier | Unique clearance record |
| content_ref | Identifier | Links to reviewed content |
| compliance_status | Enum | Cleared / Flagged / Disqualified |
| flagged_terms | Array | Terms requiring correction (if Flagged) |
| disqualified_terms | Array | Terms triggering disqualification (if Disqualified) |
| correction_guidance | Text | Authorized alternative language |
| clearance_date | Date | System-generated |

### Allowed Operations
- CREATE clearance request (any document-producing module)
- READ by requesting module and CLU-05.2
- UPDATE on resubmission after corrections
- Disqualified records route to CLU-05.5 automatically

### Dependency Rules
- All Tier documents require Cleared status before platform deployment
- Facilitator communications require Cleared status before distribution
- External communications require Cleared status before release (per IC external routing)
- Resubmission after Flagged status requires documented corrections

### Error Conditions

| Error | Condition | Resolution |
|---|---|---|
| DEPLOYMENT_WITHOUT_CLEARANCE | Document deployed without Cleared status | Block; revoke platform status; require review |
| DISQUALIFIED_TERM_IN_USE | Active disqualification applied to in-use content | Issue removal directive; set compliance hold |
| REPEATED_FLAGGING | Same content flagged multiple times without resolution | Escalate to CLU-02.2 for theological review |
| LEXICON_GAP | Term in content not found in DOC-03.1 | Flag for CLU-05.2 lexicon submission process |

### Interacting Modules
All Clusters → CLU-05.1 → CLU-05.2, CLU-05.5, CLU-02.2 (escalations)

---

## IC-12 — LEXICON UPDATE PROPAGATION

**Interface Name:** Lexicon Update Propagation
**Version:** 1.0
**Status:** Active

### Purpose
Distributes approved lexicon additions, amendments, and disqualifications from CLU-05.2 to all clusters, ensuring all platform modules operate on the current authorized lexicon version.

### Producer
CLU-05.2 — Lexicon Management System

### Consumers
All clusters — CLU-01 through CLU-06

### Input Schema

| Field | Type | Required | Source |
|---|---|---|---|
| update_id | Identifier | Yes | CLU-05.2 update record |
| update_type | Enum | Yes | New-entry / Amendment / Disqualification |
| term | Text | Yes | Affected lexicon term |
| updated_entry_ref | Identifier | Yes | Links to DOC-03.1 updated entry |
| council_ruling_ref | Identifier | Yes | CLU-02.4 ruling authorizing the update |
| effective_date | Date | Yes | Date update takes effect |

### Output Schema

| Field | Type | Description |
|---|---|---|
| propagation_id | Identifier | Unique propagation record |
| update_id | Identifier | Links to CLU-05.2 record |
| cluster_notification_log | Map | Notification status per cluster |
| compliance_review_triggered | Boolean | True if disqualification requires audit |
| propagation_date | Date | System-generated |

### Allowed Operations
- CREATE propagation record (on lexicon update approval)
- READ by all clusters
- Disqualification updates automatically trigger CLU-05.3 audit
- No UPDATE or DELETE on propagated term records

### Dependency Rules
- All lexicon updates require council_ruling_ref — no unilateral updates
- Disqualification propagation automatically initiates CLU-05.3 audit of corpus
- Clusters must implement updates by effective_date

### Error Conditions

| Error | Condition | Resolution |
|---|---|---|
| MISSING_COUNCIL_RULING | Update submitted without ruling reference | Block propagation; return to CLU-05.2 |
| CLUSTER_NONCOMPLIANCE | Cluster fails to implement by effective_date | Escalate to CLU-02.1 |
| TERM_CONFLICT | New term conflicts with existing entry | Block; require CLU-05.2 adjudication |
| DISQUALIFICATION_AUDIT_FAILED | CLU-05.3 audit not initiated on disqualification | System auto-triggers; log failure |

### Interacting Modules
CLU-05.2 → All Clusters, CLU-05.3

---

## IC-13 — HUB HEALTH ESCALATION

**Interface Name:** Hub Health Escalation
**Version:** 1.0
**Status:** Active

### Purpose
Routes hub health assessment findings from CLU-04.6 to CLU-02.1 when health thresholds indicate systemic concern requiring Council-level intervention.

### Producer
CLU-04.6 — Hub Health Assessment

### Consumer
CLU-02.1 — Governing Authority Module

### Input Schema

| Field | Type | Required | Source |
|---|---|---|---|
| health_assessment_id | Identifier | Yes | CLU-04.6 assessment record |
| hub_id | Identifier | Yes | Assessed hub |
| health_score | Numeric | Yes | Composite health score |
| consecutive_below_threshold | Numeric | Yes | Count of consecutive below-threshold assessments |
| risk_areas | Array | Yes | Identified risk categories |
| hub_leader_id | Identifier | Yes | Current Hub Leader |
| assessment_date | Date | Yes | System-generated |

### Output Schema

| Field | Type | Description |
|---|---|---|
| escalation_id | Identifier | Unique escalation record |
| hub_id | Identifier | Links to hub record |
| escalation_status | Enum | Received / Under-review / Intervention-active / Resolved |
| council_response_record | Text | Council action taken |
| intervention_type | Enum | Advisory / Oversight / Suspension / Closure-review |
| escalation_date | Date | System-generated |
| resolution_date | Date | Populated on resolution |

### Allowed Operations
- CREATE escalation record (automatic on threshold breach)
- UPDATE status through intervention lifecycle
- READ by CLU-02.1, Hub Leader (own hub only)
- No DELETE operation permitted

### Dependency Rules
- Two consecutive below-threshold assessments trigger mandatory escalation (per MDI-01 constraint)
- Single Critical-severity risk area triggers immediate escalation regardless of score
- Council must acknowledge escalation within defined period per DOC-01.2

### Error Conditions

| Error | Condition | Resolution |
|---|---|---|
| MANDATORY_ESCALATION_MISSED | Threshold breached without escalation created | System auto-creates; flags gap to CLU-02.3 |
| COUNCIL_ACKNOWLEDGMENT_OVERDUE | No Council response within required period | Escalate to 02.3 for scheduling |
| HUB_LEADER_ACCESS_VIOLATION | Escalation accessed by unauthorized party | Block; log; notify Council |
| INTERVENTION_WITHOUT_AUTHORIZATION | Intervention action taken without Council authorization | Flag; require retroactive authorization |

### Interacting Modules
CLU-04.6 → CLU-02.1 → CLU-02.3, CLU-02.4

---

## IC-14 — DEPLOYMENT FUNDING AUTHORIZATION

**Interface Name:** Deployment Funding Authorization
**Version:** 1.0
**Status:** Active

### Purpose
Transfers deployment funding authorizations from CLU-06.6 to CLU-04.1, enabling a hub formation protocol to proceed once financial authorization is confirmed. No hub formation process may advance to launch without this clearance.

### Producer
CLU-06.6 — Deployment Funding Logic

### Consumer
CLU-04.1 — Hub Formation Protocol

### Input Schema

| Field | Type | Required | Source |
|---|---|---|---|
| deployment_request_id | Identifier | Yes | CLU-04.1 deployment record |
| hub_id | Identifier | Yes | Hub being deployed |
| requested_amount | Numeric | Yes | Budget from deployment template |
| deployment_template_ref | Identifier | Yes | Phase 9 template reference |
| council_authorization_ref | Identifier | Yes | CLU-02.1 authorization record |
| allocation_id | Identifier | Yes | CLU-03.5 allocation record |

### Output Schema

| Field | Type | Description |
|---|---|---|
| funding_authorization_id | Identifier | Unique funding authorization record |
| deployment_request_id | Identifier | Links to CLU-04.1 deployment record |
| hub_id | Identifier | Receiving hub |
| authorized_amount | Numeric | Confirmed deployment budget |
| funding_status | Enum | Authorized / Contingent / Denied |
| contingency_conditions | Text | If Contingent — required conditions |
| denial_basis | Text | If Denied — stated reason |
| authorization_date | Date | System-generated |
| expiry_date | Date | Date authorization lapses if unused |

### Allowed Operations
- CREATE authorization record (on deployment funding approval)
- READ by CLU-04.1, CLU-06.5
- UPDATE status on contingency resolution
- No DELETE operation permitted; Denied records are permanent

### Dependency Rules
- Hub formation protocol (CLU-04.1) is blocked from launch phase until Authorized status confirmed
- Authorization expires if deployment not initiated within defined period
- Contingent authorizations require CLU-04.1 acknowledgment of conditions

### Error Conditions

| Error | Condition | Resolution |
|---|---|---|
| LAUNCH_WITHOUT_AUTHORIZATION | Hub formation attempts launch phase without Authorized status | Block; return to pending-funding state |
| AUTHORIZATION_EXPIRED | Deployment not initiated before expiry_date | Require new authorization from CLU-06.6 |
| AMOUNT_INSUFFICIENT | Authorized amount below deployment template minimum | Flag to CLU-06.6 and CLU-02.1; hold launch |
| TEMPLATE_MISMATCH | Deployment template ref not matching authorized scope | Require reconciliation before launch |

### Interacting Modules
CLU-06.6 → CLU-04.1, CLU-06.5, CLU-03.4

---

## CROSS-REFERENCE MATRIX

The following table shows which clusters are connected by at least one interface contract.

|  | CLU-01 | CLU-02 | CLU-03 | CLU-04 | CLU-05 | CLU-06 |
|---|---|---|---|---|---|---|
| **CLU-01** | Internal (IC-01–04) | IC-06 | — | IC-05 | IC-11 | IC-06 |
| **CLU-02** | IC-08 | Internal (IC-07–08) | IC-09 | IC-13 | IC-07, IC-11 | IC-10 |
| **CLU-03** | — | IC-09 | Internal | — | IC-11 | IC-09, IC-10 |
| **CLU-04** | IC-05 | IC-13 | — | Internal (IC-13) | IC-11 | IC-14 |
| **CLU-05** | IC-11, IC-12 | IC-07, IC-08 | IC-11 | IC-11 | Internal (IC-11–12) | IC-11 |
| **CLU-06** | IC-06 | IC-08 | IC-09, IC-10 | IC-14 | IC-11 | Internal (IC-10, IC-14) |

---

## AMENDMENT PROTOCOL

Amendments to any interface contract require:
1. Council of Metanoia review
2. Documented rationale referencing the affected module definitions (MDI-01)
3. Version increment on the specific contract and this matrix document
4. Notification to all affected clusters via IC-08

---

## AUTHORIZATION RECORD

| Role | Name | Status |
|---|---|---|
| Architect | — | Pending Council signature |
| Systems Engineer | — | Pending |
| Council Chair | — | Pending |

**Amendment Log:**

| Version | Date | Change | Authority |
|---|---|---|---|
| 1.0 | 2026-03-30 | Initial matrix created — 14 contracts defined | Architect Mode |
