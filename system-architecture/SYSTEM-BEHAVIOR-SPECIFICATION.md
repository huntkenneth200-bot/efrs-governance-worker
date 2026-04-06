# FORMATION INTELLIGENCE PLATFORM
## SYSTEM BEHAVIOR SPECIFICATION

**Document Reference:** SBS-01
**Version:** 1.0
**Status:** Active
**Owning Authority:** Council of Metanoia
**Prepared By:** Architect Mode — Claude Code
**Date:** 2026-03-30
**Review Cycle:** Upon structural amendment only

---

## PURPOSE

This specification defines the behavior of the Formation Intelligence Platform at the workflow and cross-module process level. For each major behavior: triggering conditions, state transitions, module interactions, data transformations, timing rules, escalation paths, and completion conditions.

This document governs what the platform does, in what sequence, under what conditions, and with what outcomes. It is the behavioral authority for all build, test, and operational work.

---

## GOVERNING PRINCIPLES

1. **Behavior is deterministic.** Given the same inputs and state, the platform produces the same outputs. No behavior is ambiguous.
2. **Theology governs process.** Any behavior that would require theological compromise to complete is halted, not worked around.
3. **State transitions are explicit.** No object changes state without a defined trigger, a valid prior state, and a logged record.
4. **Workflows are non-bypassable.** Completion conditions must be met in full. Partial completion does not advance a workflow.
5. **Human authorization is irreducible.** Certain state transitions (stage advancement, Council ruling ratification, hub launch) require human authorization — they are not system-automated regardless of data state.

---

## WORKFLOW INDEX

| ID | Workflow Name | Primary Cluster | Cross-Cluster |
|---|---|---|---|
| WF-01 | Participant Intake and Onboarding | CLU-01, CLU-04 | CLU-02, CLU-05 |
| WF-02 | Fracture Assessment and Profile Finalization | CLU-01 | CLU-04 |
| WF-03 | Formation Pathway Assignment and Activation | CLU-01 | CLU-04 |
| WF-04 | Milestone Tracking and Attestation | CLU-01 | CLU-04 |
| WF-05 | Stage Progression Evaluation and Advancement | CLU-01 | CLU-02, CLU-04 |
| WF-06 | Blockage Detection and Resolution | CLU-01 | CLU-02, CLU-04 |
| WF-07 | Participant Stage 5 Completion and Deployment | CLU-01 | CLU-02, CLU-04, CLU-05 |
| WF-08 | Hub Deployment and Launch | CLU-04 | CLU-02, CLU-06 |
| WF-09 | Hub Health Assessment and Escalation | CLU-04 | CLU-02 |
| WF-10 | Council Ruling Initiation and Propagation | CLU-02 | All Clusters |
| WF-11 | Theological Review Process | CLU-02 | All Clusters |
| WF-12 | Language Compliance Review | CLU-05 | All Clusters |
| WF-13 | Lexicon Entry Lifecycle | CLU-05 | CLU-02 |
| WF-14 | Capital Source Intake and Clearance | CLU-03 | CLU-02, CLU-06 |
| WF-15 | Fund Allocation and Disbursement | CLU-03, CLU-06 | CLU-02 |
| WF-16 | Aggregate Reporting | CLU-01 | CLU-02, CLU-06 |
| WF-17 | Facilitator Onboarding and Certification | CLU-02 | CLU-04, CLU-06 |
| WF-18 | Document Production and Platform Status | CLU-05 | CLU-02 |

---

---

# WF-01 — PARTICIPANT INTAKE AND ONBOARDING

## Behavior Description
A new individual is received into the platform, assigned a participant identity record, consented, assigned a facilitator and hub, and prepared for initial assessment. This is the entry gate for all formation activity.

## Triggering Conditions
- Hub Leader or Facilitator submits a new participant intake request
- Individual has been received through hub hospitality or local church referral
- Intake request includes preliminary identification information

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | No record | OBJ-01 Draft | Intake request submitted |
| 2 | OBJ-01 Draft | OBJ-01 Pending-consent | Facilitator assigned; hub confirmed |
| 3 | OBJ-01 Pending-consent | OBJ-01 Active | Consent document signed and consent_record_ref populated |
| 4 | OBJ-01 Active | OBJ-26 DOC_04_1 scheduled | Assessment scheduling initiated |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | CLU-04.1 (Hub Formation Protocol) | Confirms hub capacity and availability |
| 2 | CLU-01.6 (Restoration Record Keeper) | Creates OBJ-01 Participant Record and OBJ-11 Formation Record |
| 3 | CLU-02 (Council of Metanoia) | Validates facilitator standing and certification status |
| 4 | CLU-04.3 (Household Rhythm Scheduler) | Schedules initial intake session |
| 5 | CLU-05.1 (Semantic Authority Enforcer) | Validates any intake communication language before delivery |

## Data Transformations
- Intake request data → OBJ-01 Participant Record (status: Draft)
- Facilitator assignment confirmation → OBJ-01.facilitator_id populated
- Hub confirmation → OBJ-01.hub_id populated; OBJ-03.capacity_current incremented
- Signed consent → OBJ-01.consent_record_ref populated; status transitions to Active
- Active status → OBJ-11 Formation Record initialized (empty history arrays)

## Timing Rules
- Consent must be obtained before any assessment is scheduled
- OBJ-11 Formation Record must be created in the same session as OBJ-01
- Hub capacity check (COCC-04) runs on OBJ-03 before hub_id is assigned
- DOC-04.1 must be scheduled within defined intake window after record activation

## Escalation Paths
- Hub at capacity: route to CLU-01.5 for cross-hub evaluation (HB-001)
- Facilitator unavailable: escalate to Hub Leader for assignment (ESC-B)
- Consent not obtainable: record held in Pending-consent; Hub Leader notified after defined hold period

## Completion Conditions
- OBJ-01 status = Active
- consent_record_ref populated
- facilitator_id populated and references Certified facilitator
- hub_id populated and references Active hub
- OBJ-11 Formation Record created and linked
- DOC-04.1 assessment scheduled

---

# WF-02 — FRACTURE ASSESSMENT AND PROFILE FINALIZATION

## Behavior Description
A participant completes intake and fracture map assessment instruments. Results are processed by the Fracture Assessment Engine to produce a structured Fracture Domain Profile. L3 severity detections trigger mandatory facilitator review before the profile is finalized.

## Triggering Conditions
- OBJ-01 record status = Active
- DOC-04.1 (Intake Questionnaire) scheduled and session conducted
- Facilitator submits completed DOC-04.1 data to CLU-01.1

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | No assessment | OBJ-26 DOC_04_1 Partial | Session initiated |
| 2 | OBJ-26 DOC_04_1 Partial | OBJ-26 DOC_04_1 Complete | Facilitator verifies and submits |
| 3 | OBJ-26 DOC_04_1 Complete | OBJ-26 DOC_04_2 scheduled | CLU-01.1 initiates fracture map |
| 4 | OBJ-26 DOC_04_2 Complete | OBJ-05 Draft | CLU-01.1 generates profile |
| 5a | OBJ-05 Draft (no L3) | OBJ-05 Facilitator-reviewed | Facilitator reviews and approves |
| 5b | OBJ-05 Draft (L3 present) | OBJ-05 Draft — L3-review-required | System detects L3; sets l3_review_required = True |
| 6b | OBJ-05 Draft — L3-review-required | OBJ-05 Facilitator-reviewed | Facilitator conducts L3 review; l3_review_completed = True |
| 7 | OBJ-05 Facilitator-reviewed | OBJ-05 Finalized | Facilitator finalizes; system validates |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | CLU-01.1 (Fracture Assessment Engine) | Receives OBJ-26 records; generates OBJ-05 |
| 2 | CLU-01.6 (Restoration Record Keeper) | Stores OBJ-26 records and OBJ-05 in OBJ-11 |
| 3 | CLU-01.5 (Formation Pathway Router) | Receives finalized OBJ-05 via IC-02 |
| 4 | CLU-04.3 (Household Rhythm Scheduler) | Schedules DOC-04.2 session |

## Data Transformations
- DOC-04.1 responses → OBJ-26 (instrument_type = DOC_04_1)
- DOC-04.2 responses → OBJ-26 (instrument_type = DOC_04_2)
- Two OBJ-26 records + facilitator notes → OBJ-05 Draft:
  - active_domains derived from domain indicator pattern in assessment responses
  - severity_map assigned per domain based on indicator thresholds in DOC-03.2
  - origin_map assigned per domain based on origin indicator responses
  - recommended_entry_stage set to STAGE_1 by default
- L3 detection → l3_review_required = True; profile_status held at Draft
- L3 review completion → l3_review_completed = True; profile eligible for finalization
- Finalization → OBJ-05.profile_status = Finalized; OBJ-11 updated

## Timing Rules
- DOC-04.2 must be completed within defined interval after DOC-04.1 completion
- L3 review must occur before profile finalization — no time bypass
- If DOC-04.2 is not completed within interval: FP-014 warning issued; facilitator notified
- Profile must be finalized before WF-03 (pathway assignment) can begin

## Escalation Paths
- L3 severity in any domain: mandatory facilitator review (FP-002); no system bypass
- Conflicting domain indicators: profile held in Draft; facilitator manual review required
- Assessment voided by facilitator: new OBJ-26 record required; prior voided record retained

## Completion Conditions
- OBJ-26 records exist for both DOC_04_1 and DOC_04_2 with facilitator_verified = True
- OBJ-05.profile_status = Finalized
- l3_review_required = False OR (l3_review_required = True AND l3_review_completed = True)
- OBJ-05 stored in OBJ-11.fracture_profile_history
- IC-02 transmits finalized profile to CLU-01.5

---

# WF-03 — FORMATION PATHWAY ASSIGNMENT AND ACTIVATION

## Behavior Description
A finalized Fracture Domain Profile is translated into a specific formation pathway — identifying stage, domain sequence, facilitator, hub sessions, and hospitality integration. The participant's active pathway is initialized and hub routing is confirmed.

## Triggering Conditions
- OBJ-05 profile_status = Finalized (IC-02 signal received by CLU-01.5)
- Participant has Active OBJ-01 record with confirmed hub_id and facilitator_id
- No existing Active OBJ-06 pathway for participant (first assignment) or prior pathway is Complete/Transferred (reassignment)

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | No pathway | OBJ-06 Draft | CLU-01.5 receives finalized OBJ-05 |
| 2 | OBJ-06 Draft | OBJ-06 Active | Facilitator confirms pathway assignment |
| 3 | OBJ-06 Active | OBJ-10 Pending | CLU-01.5 initiates hub routing via IC-05 |
| 4 | OBJ-10 Pending | OBJ-10 Confirmed | Hub confirms capacity; Hub Leader notified |
| 5 | OBJ-10 Confirmed | OBJ-06 Active + session scheduled | CLU-04.3 creates session schedule entry |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | CLU-01.5 (Formation Pathway Router) | Generates OBJ-06 from OBJ-05 data |
| 2 | CLU-04 (Emmaus Road) | Confirms hub capacity and session availability |
| 3 | CLU-04.3 (Household Rhythm Scheduler) | Creates session schedule entry; returns session_schedule_ref |
| 4 | CLU-04.4 (Hospitality Operations) | Evaluates hospitality assignment appropriateness for stage |
| 5 | CLU-01.6 (Restoration Record Keeper) | Stores OBJ-06 in OBJ-11.pathway_history |

## Data Transformations
- OBJ-05.active_domains → OBJ-06.domain_sequence (ordered by severity, primary domain first)
- OBJ-05.recommended_entry_stage → OBJ-06.assigned_stage
- Hub confirmation → OBJ-10.routing_status = Confirmed; OBJ-03.capacity_current updated
- Session schedule creation → OBJ-06.hub_session_refs populated
- Hospitality evaluation → OBJ-10.hospitality_assignment_ref populated (if applicable)

## Timing Rules
- Pathway must be created within defined interval after profile finalization
- Hub routing confirmation must be received before pathway status advances to Active
- If hub at capacity: pathway held in Draft; routing set to Pending-capacity; reviewed at defined interval
- Cross-hub routing notification must be delivered before routing is confirmed

## Escalation Paths
- Hub at capacity: CLU-01.5 evaluates alternative hubs; Hub Leader notified (HB-001)
- No hub available within platform: escalated to Council for capacity planning (ESC-C)
- Facilitator unavailable: escalated to Hub Leader for alternative assignment (ESC-B)

## Completion Conditions
- OBJ-06.pathway_status = Active
- OBJ-10.routing_status = Confirmed
- OBJ-10.hub_leader_notified = True
- OBJ-06.hub_session_refs populated with at least one session entry
- OBJ-11.pathway_history updated
- OBJ-01.current_stage set to OBJ-06.assigned_stage

---

# WF-04 — MILESTONE TRACKING AND ATTESTATION

## Behavior Description
A participant engages in formation activities. Facilitators track and attest milestone completions within the participant's active stage. Overdue milestones are flagged. Completion data feeds stage progression evaluation.

## Triggering Conditions
- Participant has Active OBJ-06 pathway
- Facilitator submits a milestone completion attestation following a session or formation event
- Scheduled periodic check identifies overdue milestones (system-triggered)

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | No OBJ-07 record | OBJ-07 Pending | Pathway activated; milestones initialized from DOC-03.4 |
| 2 | OBJ-07 Pending | OBJ-07 Partial | Facilitator records partial progress |
| 3 | OBJ-07 Partial / Pending | OBJ-07 Complete | Facilitator submits attestation |
| 4 | OBJ-07 Pending (overdue threshold) | OBJ-07 Overdue | System sets overdue_flag = True |
| 5 | OBJ-07 Overdue | CLU-01.4 evaluated | Overdue milestone routed for blockage assessment |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | CLU-01.3 (Milestone Tracking System) | Initializes OBJ-07 records from DOC-03.4 for current stage |
| 2 | CLU-01.3 | Receives facilitator attestation; updates OBJ-07 status |
| 3 | CLU-01.4 (Blockage Detection Module) | Receives overdue flag for blockage evaluation |
| 4 | CLU-01.2 (Stage Progression Logic) | Receives milestone completion aggregate via IC-03 |
| 5 | CLU-01.6 (Restoration Record Keeper) | Updates OBJ-11.milestone_history |

## Data Transformations
- DOC-03.4 milestone list for current stage → Set of OBJ-07 records (status: Pending)
- Facilitator attestation submission → OBJ-07.completion_status = Complete; facilitator_attestation_id populated; attestation_date set
- Time threshold exceeded → OBJ-07.overdue_flag = True (system-calculated)
- Aggregate OBJ-07 status for stage → OBJ-08.completion_percentage (COCC-02 maintained)
- All milestones Complete → OBJ-08.milestone_threshold_met = True

## Timing Rules
- Milestone records for current stage are initialized on pathway activation — not on first session
- Overdue threshold per milestone is defined in DOC-03.4 — platform enforces; facilitator does not set
- Attestation must be submitted within defined post-session window
- Periodic overdue check runs at defined interval (minimum weekly per COCC-09 schedule)

## Escalation Paths
- Overdue milestone: facilitator notified; if not resolved within defined window, blockage evaluation initiated in CLU-01.4 (FP-014)
- Milestone not found in DOC-03.4: FP-007 error; routed to CLU-05.2 for registry review

## Completion Conditions (per stage)
- All OBJ-07 records for current stage have completion_status = Complete
- All OBJ-07 records have facilitator_attestation_id populated
- No OBJ-07 records for current stage have overdue_flag = True
- COCC-02 consistency check passes
- OBJ-08 milestone_threshold_met = True for current stage

---

# WF-05 — STAGE PROGRESSION EVALUATION AND ADVANCEMENT

## Behavior Description
When all milestones for a stage are complete and no active blockage exists, a stage progression evaluation is generated. If the evaluation is favorable and the facilitator authorizes, the participant advances to the next stage. The Stage 4 → Stage 5 transition requires additional facilitator assessment submission.

## Triggering Conditions
- All OBJ-07 records for current stage reach Complete status
- No active OBJ-09 Blockage Record exists for the participant
- CLU-01.3 transmits IC-03 signal to CLU-01.2 with milestone_threshold_met = True

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | Milestones complete; no blockage | OBJ-08 Created | IC-03 signal triggers evaluation creation |
| 2 | OBJ-08 Created | OBJ-08 Eligible | System confirms advancement_eligible = True |
| 3 | OBJ-08 Eligible | OBJ-08 Pending-facilitator | Facilitator review queue entry created |
| 4a (Stages 1–4) | OBJ-08 Pending-facilitator | OBJ-08 Authorized | Facilitator submits advancement authorization |
| 4b (Stage 4 → 5) | OBJ-08 Pending-facilitator | OBJ-08 Assessment-required | System detects Stage 4 → 5 and requires additional assessment |
| 5b | OBJ-08 Assessment-required | OBJ-08 Authorized | Facilitator submits Stage 4→5 assessment; authorizes |
| 6 | OBJ-08 Authorized | OBJ-01, OBJ-06 stage updated | Stage transition executed |
| 7 | Stage transition | OBJ-07 records initialized for new stage | New stage milestones loaded from DOC-03.4 |
| 8 | Stage transition | OBJ-11 stage_transition_log entry created | Audit record written |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | CLU-01.3 (Milestone Tracking System) | Confirms all milestones complete; sends IC-03 |
| 2 | CLU-01.4 (Blockage Detection Module) | Confirms no active blockage hold via IC-04 |
| 3 | CLU-01.2 (Stage Progression Logic) | Creates OBJ-08; evaluates advancement_eligible |
| 4 | CLU-01.2 | Routes to facilitator review queue |
| 5 | CLU-01.5 (Formation Pathway Router) | Updates OBJ-06.assigned_stage on advancement |
| 6 | CLU-01.3 | Initializes new stage OBJ-07 records |
| 7 | CLU-01.6 (Restoration Record Keeper) | Updates OBJ-11 stage_transition_log and pathway_history |
| 8 | CLU-04.3 (Household Rhythm Scheduler) | Updates session schedule for new stage requirements |

## Data Transformations
- OBJ-07 aggregate (all Complete) + OBJ-09 check (no Active) → OBJ-08.advancement_eligible = True
- OBJ-08 Authorized → OBJ-01.current_stage incremented by one stage
- OBJ-08 Authorized → OBJ-06.assigned_stage updated to new stage
- Stage transition → new OBJ-07 records initialized from DOC-03.4 for new stage
- Stage transition → OBJ-11.stage_transition_log appended with from_stage, to_stage, date, facilitator_id
- Stage regression → same process; regression_rationale required in OBJ-08.facilitator_assessment_ref

## Timing Rules
- OBJ-08 creation is event-triggered — not scheduled
- Facilitator review must occur within defined review window after evaluation creation
- Stage 4 → 5 assessment has no system-imposed time limit — but is required before advancement
- Stage advancement is never system-automated — human authorization is required in all cases

## Escalation Paths
- Stage 4 → 5 attempted without facilitator assessment: FP-008; blocked; facilitator notified
- Stage skipped in sequence: FP-005 CRITICAL error; CLU-02.1 notified
- Facilitator review window exceeded: Hub Leader notified; escalation if not resolved

## Completion Conditions
- OBJ-08.advancement_authorized = True
- OBJ-08.advancement_date populated
- OBJ-01.current_stage = new stage value
- OBJ-06.assigned_stage = new stage value
- OBJ-11.stage_transition_log entry created
- New stage OBJ-07 records initialized

---

# WF-06 — BLOCKAGE DETECTION AND RESOLUTION

## Behavior Description
Formation blockages are detected through milestone staleness, time-in-stage flags, facilitator observation, or assessment indicators. A blockage record is created, the appropriate escalation path is triggered, the participant's stage advancement is held, and resolution is tracked until cleared.

## Triggering Conditions
- OBJ-07 overdue_flag = True AND facilitator has not resolved within defined window
- Participant has exceeded maximum defined time-in-stage threshold
- Facilitator submits a blockage observation directly
- DOC-04.3 periodic assessment results indicate regression or stagnation indicators

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | No blockage | OBJ-09 Active | Detection trigger fires |
| 2 | OBJ-06 Active | OBJ-06 On-hold | OBJ-09 created with hold_status = Active |
| 3 | OBJ-09 Active | OBJ-09 Under-review | Facilitator acknowledges and initiates review |
| 4a (non-spiritual) | OBJ-09 Under-review | OBJ-09 Resolved | Facilitator documents resolution; submits clearance |
| 4b (spiritual) | OBJ-09 Active | OBJ-09 Under-review + Escalated | Escalation_required = True; routed to Council (ESC-C) |
| 5 | OBJ-09 Resolved | OBJ-06 Active | Hold released; stage progression re-eligible |
| 6 | OBJ-09 Resolved | OBJ-11 updated | Blockage history appended |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | CLU-01.4 (Blockage Detection Module) | Creates OBJ-09 on trigger |
| 2 | CLU-01.2 (Stage Progression Logic) | Receives IC-04 signal; holds advancement |
| 3 | CLU-01.4 | Routes spiritual blockages to CLU-02 for escalation |
| 4 | CLU-02.1 (Governing Authority Module) | Receives escalation for spiritual blockage; assigns elder or Council response |
| 5 | CLU-01.4 | Receives resolution documentation; updates OBJ-09 |
| 6 | CLU-01.2 | Clears hold on advancement when OBJ-09.hold_status = Resolved |
| 7 | CLU-01.6 (Restoration Record Keeper) | Updates OBJ-11.blockage_history |

## Data Transformations
- Detection trigger → OBJ-09 created: blockage_type, blockage_severity, detection_trigger, escalation_required populated
- OBJ-09 Active → OBJ-06.pathway_status = On-hold
- escalation_required = True → escalation_status = Pending; escalation_target populated
- Facilitator resolution submission → OBJ-09.resolution_documentation populated; hold_status = Resolved
- Resolved status → OBJ-06.pathway_status = Active; OBJ-08 re-evaluation eligible
- Resolved OBJ-09 → OBJ-11.blockage_history appended

## Timing Rules
- Blockage record is created immediately on detection trigger — not after facilitator confirmation
- Spiritual blockage escalation must occur immediately — no defined delay window
- Critical severity blockage requires Hub Leader notification within same session
- Resolution must include documentation — no time limit on resolution, but unclosed blockages are surfaced in Hub Health Assessment (OBJ-23)

## Escalation Paths
- SPIRITUAL type: immediate auto-escalation to Council (ESC-C) — FP-011
- CRITICAL severity: immediate Hub Leader notification (ESC-B)
- Blockage unresolved beyond defined threshold: surfaces in OBJ-23 Hub Health Assessment as risk area
- Duplicate blockage while hold Active: records merged; severity reviewed

## Completion Conditions
- OBJ-09.hold_status = Resolved
- OBJ-09.resolution_documentation populated
- OBJ-06.pathway_status = Active
- COCC-03 consistency check passes
- OBJ-11.blockage_history updated

---

# WF-07 — PARTICIPANT STAGE 5 COMPLETION AND DEPLOYMENT

## Behavior Description
A participant completes all Stage 5 (Deployment) milestones, receives facilitator attestation and advancement authorization, and is formally recognized as having completed the Restoration OS formation pathway. A stage completion record is created. Vocational and missional next steps are identified.

## Triggering Conditions
- All Stage 5 OBJ-07 milestone records reach Complete status
- No active OBJ-09 blockage exists
- OBJ-08 Stage 5 evaluation created with advancement_eligible = True
- Facilitator submits Stage 5 completion assessment and authorization

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | Stage 5 milestones all Complete | OBJ-08 Eligible (Stage 5) | IC-03 signal to CLU-01.2 |
| 2 | OBJ-08 Eligible | OBJ-08 Assessment-required | Stage 5 completion requires final facilitator assessment |
| 3 | OBJ-08 Assessment-required | OBJ-08 Authorized | Facilitator submits completion assessment and authorizes |
| 4 | OBJ-08 Authorized | OBJ-06.pathway_status = Complete | CLU-01.2 closes pathway |
| 5 | OBJ-06 Complete | OBJ-11.stage_5_completion_ref populated | CLU-01.6 records completion |
| 6 | OBJ-11 updated | OBJ-01.record_status = Completed (or Active for ongoing engagement) | Facilitator determines post-completion status |
| 7 | Completion | Vocational discernment process initiated | CLU-01.5 routes to post-formation resources |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | CLU-01.2 (Stage Progression Logic) | Creates and evaluates Stage 5 OBJ-08 |
| 2 | CLU-01.6 (Restoration Record Keeper) | Populates OBJ-11.stage_5_completion_ref; updates formation record |
| 3 | CLU-01.5 (Formation Pathway Router) | Routes to post-completion resources |
| 4 | CLU-04.2 (Covenant Community Engine) | Reviews covenant membership status post-completion |
| 5 | CLU-05.4 (Formation Narrative Generator) | Makes formation story framework available to participant and facilitator |
| 6 | CLU-02.1 (Governing Authority Module) | Receives aggregate completion data via IC-06 |

## Data Transformations
- All Stage 5 OBJ-07 Complete + facilitator assessment → OBJ-08 Authorized
- OBJ-08 Authorized → OBJ-06.pathway_status = Complete
- OBJ-06 Complete → OBJ-11.stage_5_completion_ref populated
- stage_transition_log entry appended: Stage 5 Completed with date and facilitator_id
- Aggregate formation data → OBJ-12 updated at next reporting cycle

## Timing Rules
- Stage 5 completion assessment has no system-imposed time limit — facilitator determines readiness
- stage_5_completion_ref must be populated within the same session as authorization
- Post-completion routing is initiated immediately on OBJ-06 status = Complete
- OBJ-01 status decision (Completed vs. Active) must be made within defined post-completion window

## Escalation Paths
- No escalation path — this is a positive completion workflow
- If formation reveals new fracture domains post-Stage 5: new OBJ-05 profile initiated; participant may re-enter at appropriate stage

## Completion Conditions
- OBJ-06.pathway_status = Complete
- OBJ-11.stage_5_completion_ref populated
- OBJ-11.stage_transition_log has final Stage 5 entry
- Participant post-completion status determined and recorded in OBJ-01

---

# WF-08 — HUB DEPLOYMENT AND LAUNCH

## Behavior Description
A new Emmaus Road hub is established — from Council authorization through formation protocol execution, funding authorization, Hub Leader assignment, covenant establishment, and launch. No hub becomes Active without completing all required steps in sequence.

## Triggering Conditions
- Hub launch request submitted to CLU-04.1 with site assessment and Hub Leader candidate
- Council authorization received from CLU-02.1
- Deployment template selected from Phase 9 inventory

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | No record | OBJ-03 Forming | Council authorization received; CLU-04.1 initiates |
| 2 | OBJ-03 Forming | Funding requested | CLU-04.1 submits to CLU-06.6 via IC-14 |
| 3 | OBJ-25 Pending | OBJ-25 Authorized | CLU-06.6 issues deployment funding authorization |
| 4 | OBJ-25 Authorized | Hub Leader qualified and assigned | OBJ-02 Hub Leader record confirmed |
| 5 | Hub Leader assigned | Hub covenant established | Hub covenant document created and signed |
| 6 | Covenant established | Formation infrastructure ready | CLU-01 submodules initialized for hub |
| 7 | Formation infrastructure ready | OBJ-03 Active | CLU-04.1 completes launch checklist; Hub Leader activates |
| 8 | OBJ-03 Active | Participant intake enabled | OBJ-03.capacity_current = 0; intake routing begins |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | CLU-02.1 (Governing Authority Module) | Issues Council authorization; records in OBJ-14 |
| 2 | CLU-04.1 (Hub Formation Protocol) | Drives entire deployment process; holds checklist |
| 3 | CLU-06.6 (Deployment Funding Logic) | Processes OBJ-25; issues funding authorization |
| 4 | CLU-03.5 (Fund Allocation Logic) | Provides capital via IC-10 to CLU-06.6 |
| 5 | CLU-02.5 (Member Accountability Module) | Validates Hub Leader qualification and standing |
| 6 | CLU-04.2 (Covenant Community Engine) | Establishes hub covenant record |
| 7 | CLU-04.3 (Household Rhythm Scheduler) | Initializes hub formation calendar |
| 8 | CLU-01 submodules | Prepared to receive first participant intake |

## Data Transformations
- Council authorization → OBJ-03 created with hub_status = Forming; council_authorization_ref populated
- Deployment template selection → OBJ-03.deployment_template_ref populated; OBJ-25 budget parameters set
- OBJ-25 Authorized → launch phase gates open
- Hub Leader assignment → OBJ-03.hub_leader_id populated; OBJ-02 hub_id updated
- Covenant signing → OBJ-03.covenant_ref populated
- Launch checklist complete → OBJ-03.hub_status = Active; OBJ-03.launch_date set
- OBJ-03 Active → OBJ-03.capacity_current initialized to 0; WF-01 routing enabled for this hub

## Timing Rules
- Each phase gate must be completed before the next opens — sequential, no parallel execution of dependent steps
- Funding authorization expiry (OBJ-25.expiry_date) governs launch deadline — hub must reach Active before expiry
- Hub Leader qualification must be confirmed by CLU-02.5 before covenant is established
- Formation infrastructure initialization must complete before OBJ-03 status advances to Active

## Escalation Paths
- Funding authorization denied: CLU-06.6 returns denial; CLU-04.1 and CLU-02.1 notified (CA-008)
- Funding authorization expired before launch: new authorization required (CA-010)
- Hub Leader qualification fails: Hub Leader candidate replaced; process returns to Step 4
- Council authorization not received: launch cannot proceed; no workaround path

## Completion Conditions
- OBJ-03.hub_status = Active
- OBJ-03.council_authorization_ref populated
- OBJ-03.hub_leader_id populated with qualified Hub Leader
- OBJ-03.covenant_ref populated
- OBJ-25.funding_status = Authorized (not Expired)
- OBJ-03.launch_date populated
- CLU-04.3 formation calendar initialized
- All COCC-07 consistency checks pass

---

# WF-09 — HUB HEALTH ASSESSMENT AND ESCALATION

## Behavior Description
Active hubs are evaluated on a periodic basis across five health dimensions. A health score is produced. If the score falls below threshold or a critical risk is present, mandatory escalation to Council is triggered. Council responds with an intervention type. The hub is monitored until escalation is resolved.

## Triggering Conditions
- Periodic assessment schedule reached (minimum defined interval per DOC-02.2)
- Hub Leader submits self-assessment
- Hub-level event triggers an ad hoc assessment (e.g., Hub Leader departure, significant participant departure)
- CLU-04.6 receives two consecutive below-threshold scores

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | No assessment | OBJ-23 Created | Scheduled trigger or event trigger |
| 2 | OBJ-23 Created | OBJ-23 Scored | Component data collected; health_score calculated |
| 3a | OBJ-23 Scored (above threshold) | Assessment complete; no escalation | Score recorded; OBJ-11 aggregate updated |
| 3b | OBJ-23 Scored (below threshold) | consecutive_below_threshold incremented | System updates count |
| 3c | OBJ-23 (critical risk present) | OBJ-24 created immediately | Mandatory escalation regardless of score |
| 4 | consecutive_below_threshold ≥ 2 | OBJ-24 Created | Mandatory escalation triggered |
| 5 | OBJ-24 Created | OBJ-24 Received | CLU-02.1 receives and acknowledges |
| 6 | OBJ-24 Received | OBJ-24 Under-review | Council initiates review |
| 7 | OBJ-24 Under-review | OBJ-24 Intervention-active | Council determines intervention_type |
| 8 | OBJ-24 Intervention-active | OBJ-24 Resolved | Intervention complete; resolution documented |
| 9 | OBJ-24 Resolved | OBJ-03 status reviewed | Hub status may change based on intervention outcome |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | CLU-04.6 (Hub Health Assessment) | Collects assessment components; calculates OBJ-23 |
| 2 | CLU-01.6 (Restoration Record Keeper) | Provides anonymized formation outcome data to CLU-04.6 |
| 3 | CLU-04.2 (Covenant Community Engine) | Provides covenant compliance data |
| 4 | CLU-04.3 (Household Rhythm Scheduler) | Provides rhythm adherence data |
| 5 | CLU-04.6 | Creates OBJ-24 when escalation_required = True; transmits via IC-13 |
| 6 | CLU-02.1 (Governing Authority Module) | Receives OBJ-24; determines intervention |
| 7 | CLU-02.3 (Council Operations Manager) | Schedules Council review session |
| 8 | CLU-02.4 (Amendment and Ruling Registry) | Stores OBJ-24 as governance record |

## Data Transformations
- Component data (formation outcomes + covenant compliance + rhythm adherence + leadership integrity + hospitality) → OBJ-23.health_score (weighted composite per DOC-02.2)
- health_score below threshold → OBJ-23.below_threshold = True; consecutive_below_threshold incremented
- consecutive_below_threshold ≥ 2 OR critical_risk_present = True → OBJ-23.escalation_required = True
- OBJ-23 escalation_required → OBJ-24 created; IC-13 transmits to CLU-02.1
- Council determination → OBJ-24.intervention_type populated; OBJ-03.hub_status updated if applicable
- Resolution → OBJ-24.resolution_documentation; OBJ-24.resolution_date; OBJ-24.escalation_status = Resolved

## Timing Rules
- Periodic assessments run on defined schedule — not ad hoc unless triggered
- Council acknowledgment of OBJ-24 must occur within required period per DOC-01.2
- Intervention type must be determined within Council session following acknowledgment
- Suspension and closure review interventions are time-sensitive — defined response windows apply

## Escalation Paths
- Missed mandatory escalation: system auto-creates OBJ-24; gap logged; CLU-02.3 notified (FP-017)
- Council acknowledgment overdue: escalated to CLU-02.3 for scheduling (GV-010)
- Unauthorized access to OBJ-24: access blocked; Council notified immediately (GV-011)
- Intervention without Council authorization: flagged; retroactive authorization required (GV-012)

## Completion Conditions
- OBJ-24.escalation_status = Resolved
- OBJ-24.resolution_documentation populated
- OBJ-24.resolution_date populated
- OBJ-03.hub_status reviewed and updated if applicable
- All actions logged and stored in CLU-02.4

---

# WF-10 — COUNCIL RULING INITIATION AND PROPAGATION

## Behavior Description
A matter is brought before the Council of Metanoia for a binding ruling — amendment, directive, disqualification, or doctrinal position. The Council deliberates, votes, ratifies, and the ruling is propagated to all affected clusters with mandatory acknowledgment tracking.

## Triggering Conditions
- Amendment request submitted by any cluster or Council member
- Theological review returns Disqualification requiring Council ratification
- Hub health escalation requires Council-level governance action
- Council member initiates a doctrinal position or directive

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | No ruling | OBJ-14 Draft | Matter submitted to CLU-02.1 |
| 2 | OBJ-14 Draft | Council session scheduled | CLU-02.3 receives agenda item |
| 3 | Session scheduled | Vote conducted | Council deliberates; vote submitted |
| 4a | Vote: quorum met | OBJ-14 Ratified | CLU-02.1 confirms quorum and ratification |
| 4b | Vote: quorum not met | OBJ-14 Draft — quorum failure | Session rescheduled; GV-001 logged |
| 5 | OBJ-14 Ratified | OBJ-15 Created | Propagation record initiated |
| 6 | OBJ-15 Created | Notification sent to all affected clusters | IC-08 propagation executed |
| 7 | Notifications sent | OBJ-15 Partial | Acknowledgments received from some clusters |
| 8 | All acknowledged | OBJ-15 Complete | Propagation complete |
| 9 | OBJ-15 Complete | Document amendments applied | Affected Tier documents updated by effective_date |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | CLU-02.1 (Governing Authority Module) | Receives matter; creates OBJ-14 Draft; assigns to agenda |
| 2 | CLU-02.3 (Council Operations Manager) | Schedules session; distributes materials |
| 3 | CLU-02.5 (Member Accountability Module) | Confirms eligible voter standing for quorum calculation |
| 4 | CLU-02.1 | Records vote; confirms quorum; ratifies ruling |
| 5 | CLU-02.4 (Amendment and Ruling Registry) | Receives ratified OBJ-14; creates permanent record |
| 6 | CLU-02.1 | Initiates IC-08 propagation |
| 7 | All affected clusters | Receive ruling; implement by effective_date; return acknowledgment |
| 8 | CLU-05.2 (Lexicon Management) | If ruling concerns lexicon: initiates OBJ-22 update via WF-13 |

## Data Transformations
- Matter submission → OBJ-14 Draft: ruling_type, ruling_text, affected_documents, affected_clusters populated
- Vote submission → OBJ-14.vote_record populated: votes_cast, votes_in_favor, quorum_confirmed
- Quorum confirmed → OBJ-14.ruling_status = Ratified; ratification_date populated
- Ratified ruling → OBJ-15 created: cluster_notification_log initialized for all affected clusters
- Cluster acknowledgment → OBJ-15.cluster_notification_log entry updated to Acknowledged
- All Acknowledged → OBJ-15.propagation_status = Complete
- Affected documents → amendment entries appended with ruling reference and effective_date

## Timing Rules
- effective_date governs implementation — not ratification_date or propagation_date
- Clusters must acknowledge by effective_date — overdue acknowledgments escalate to CLU-02.3
- Vote may not proceed without quorum per DOC-01.2 — session rescheduled if quorum fails
- Disqualification rulings take effect immediately on ratification — not deferred to effective_date

## Escalation Paths
- Quorum failure: session rescheduled; GV-001 logged; CLU-02.3 notified
- Cluster noncompliance (no acknowledgment): CLU-02.3 pursues; escalated to CLU-02.1 if persistent (GV-006)
- Conflicting ruling detected: propagation blocked; Council adjudication required before proceeding

## Completion Conditions
- OBJ-14.ruling_status = Ratified
- OBJ-14.quorum_confirmed = True
- OBJ-15.propagation_status = Complete
- All affected documents show amendment entries on or before effective_date
- OBJ-14 and OBJ-15 stored in CLU-02.4

---

# WF-11 — THEOLOGICAL REVIEW PROCESS

## Behavior Description
Any platform content — document, practice, communication, or proposed language — is submitted for theological review by the Council's Theological Review Engine. The review produces a clearance status with documented rationale. Clearance is required before any content achieves platform status.

## Triggering Conditions
- New Tier document submitted for platform status
- Amended document requires re-review
- Facilitator practice or hub activity referred for theological evaluation
- External content proposed for platform use
- Language audit (CLU-05.3) surfaces theologically complex flag requiring Council review

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | No review | OBJ-13 Submitted | Requesting module submits via IC-07 |
| 2 | OBJ-13 Submitted | OBJ-13 Assigned | CLU-02.3 assigns to available reviewer |
| 3 | OBJ-13 Assigned | OBJ-13 Under-review | Reviewing Council member begins evaluation |
| 4a | OBJ-13 Under-review | OBJ-13 Cleared | Reviewer approves; rationale documented |
| 4b | OBJ-13 Under-review | OBJ-13 Conditional | Reviewer approves with conditions; requirements listed |
| 4c | OBJ-13 Under-review | OBJ-13 Disqualified | Reviewer disqualifies; basis documented |
| 5a | OBJ-13 Cleared | Content achieves platform status | IC-11 clearance issued |
| 5b | OBJ-13 Conditional | Content held | Requesting module receives conditions; must resolve |
| 5c | OBJ-13 Disqualified | Disqualification routed to CLU-02.4 | Permanent record created; content blocked |
| 6b | Conditions resolved | Resubmit for re-review | New OBJ-13 created as resubmission |
| 6c | Dispute of disqualification | Full Council ruling initiated | WF-10 triggered for Council adjudication |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | Any cluster | Submits content via IC-07 |
| 2 | CLU-02.2 (Theological Review Engine) | Receives submission; creates OBJ-13 |
| 3 | CLU-02.3 (Council Operations Manager) | Assigns reviewer from available Council members |
| 4 | CLU-02.2 | Conducts review; records outcome in OBJ-13 |
| 5 | CLU-02.4 (Amendment and Ruling Registry) | Stores disqualification records |
| 6 | CLU-05.1 (Semantic Authority Enforcer) | Receives clearance notification; updates OBJ-20 status |
| 7 | Requesting cluster | Receives clearance status; implements or corrects |

## Data Transformations
- Content submission → OBJ-13: content_type, content_ref, requesting_module, review_priority populated
- Reviewer assignment → OBJ-13.reviewer_id populated
- Review completion → OBJ-13.clearance_status populated; theological_rationale required for all outcomes
- Cleared → IC-11 OBJ-20 updated to Cleared
- Conditional → IC-11 OBJ-20 status = Conditional; conditions returned to requesting module
- Disqualified → OBJ-13.disqualification_basis populated; OBJ-13 routed to CLU-02.4; IC-11 OBJ-20 = Disqualified

## Timing Rules
- Urgent priority requests must be assigned within defined accelerated window
- Routine priority requests assigned within standard review window
- Conditional review: requesting module has defined window to resolve conditions before re-review required
- Disqualification has no expiry — permanent unless reversed by full Council ruling (WF-10)

## Escalation Paths
- Reviewer unavailable: CLU-02.3 queues request; notifies Council (WARNING)
- Disqualification override attempt: GV-005 CRITICAL; deployment blocked; Council notified immediately
- Repeated conditional failure (same content repeatedly returns with conditions unresolved): escalated to CLU-02.1

## Completion Conditions
- OBJ-13.clearance_status populated (Cleared / Conditional / Disqualified)
- OBJ-13.theological_rationale populated
- OBJ-13.reviewer_id references Active Council member
- OBJ-13.review_date populated
- If Cleared: OBJ-20 compliance record updated; content may proceed
- If Disqualified: OBJ-13 stored in CLU-02.4; content blocked from platform use

---

# WF-12 — LANGUAGE COMPLIANCE REVIEW

## Behavior Description
Any platform document or communication passes through the Semantic Authority Enforcer before achieving platform status or being released. Language is checked against the Platform Lexicon and the Semantic Authority Hierarchy. Flagged content is returned for correction. Cleared content proceeds. Disqualified content is blocked and routed to the disqualified language registry.

## Triggering Conditions
- New or amended document submitted for platform status
- Communication ready for release from any cluster
- Training material or hub resource submitted for distribution
- External content proposed for platform use
- Scheduled or triggered language audit (CLU-05.3)

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | No review | OBJ-20 Submitted | Requesting module submits via IC-11 |
| 2 | OBJ-20 Submitted | OBJ-20 Under-review | CLU-05.1 begins evaluation |
| 3a | OBJ-20 Under-review | OBJ-20 Cleared | No flags or disqualifications detected |
| 3b | OBJ-20 Under-review | OBJ-20 Flagged | One or more terms flagged for correction |
| 3c | OBJ-20 Under-review | OBJ-20 Disqualified | One or more terms trigger disqualification |
| 4a | OBJ-20 Cleared | Content achieves platform / communication status | No further action |
| 4b | OBJ-20 Flagged | Content returned to owner for correction | Correction guidance provided |
| 4c | OBJ-20 Disqualified | Content blocked; routed to CLU-05.5 | Permanent disqualification record |
| 5b | Corrections made | Resubmission — new OBJ-20 with resubmission_ref | Review cycle repeats |
| 5c | Dispute of disqualification | Escalated to CLU-02.2 for theological review | WF-11 triggered |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | Any cluster | Submits content via IC-11 |
| 2 | CLU-05.1 (Semantic Authority Enforcer) | Evaluates content against DOC-03.1 lexicon and ENUM-08 standards |
| 3 | CLU-05.5 (Disqualified Language Filter) | Receives disqualified term records; issues removal directives |
| 4 | CLU-05.2 (Lexicon Management System) | Receives lexicon gap flags; initiates submission process if warranted |
| 5 | CLU-02.2 (Theological Review Engine) | Receives escalations for theologically complex flags |
| 6 | Requesting cluster | Receives OBJ-20 outcome; implements correction or proceeds |

## Data Transformations
- Content submission → OBJ-20: content_type, content_ref, requesting_cluster populated
- Evaluation → flagged_terms array populated (per term: term, context, lexicon_ref, correction_guidance)
- Evaluation → disqualified_terms array populated (per term: term, disqualification_basis)
- Cleared → OBJ-20.compliance_status = Cleared; flagged_terms and disqualified_terms empty
- Flagged → OBJ-20.compliance_status = Flagged; correction_guidance returned to owner
- Disqualified → OBJ-20.compliance_status = Disqualified; routed to CLU-05.5 for registry
- Lexicon gap → LG-004 warning; CLU-05.2 notified for potential submission

## Timing Rules
- Language review must complete before any document achieves platform status — no interim status
- Communication review must complete before release — no post-hoc review
- Resubmission review cycle restarts from beginning — prior Flagged status is reference only
- Disqualification takes effect immediately — no grace period for removal

## Escalation Paths
- Repeated flagging of same content without resolution: escalated to CLU-02.2 (LG-008)
- Disqualified content already in distribution: removal directive issued immediately; compliance tracked (LG-002)
- Lexicon gap on critical formation term: CLU-05.2 initiates emergency submission via WF-13

## Completion Conditions
- OBJ-20.compliance_status = Cleared
- OBJ-20.clearance_date populated
- Content achieves platform status or communication is released
- If Flagged: owner corrects; resubmits; new Cleared status obtained
- If Disqualified: CLU-05.5 registry updated; content blocked from all platform use

---

# WF-13 — LEXICON ENTRY LIFECYCLE

## Behavior Description
A new term is proposed for the Platform Lexicon, or an existing entry is amended or disqualified. The proposed change undergoes theological review, Council ruling, and propagation to all clusters. The lexicon remains the authoritative, Council-governed vocabulary of the platform.

## Triggering Conditions
- Language compliance review identifies a lexicon gap (LG-004)
- Facilitator or cluster submits a term proposal to CLU-05.2
- Council ruling requires a new doctrinal term or disqualification of an existing term
- Language audit (WF-12) surfaces systematic drift requiring lexicon amendment

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | No entry | OBJ-21 Proposed | Submission to CLU-05.2 |
| 2 | OBJ-21 Proposed | OBJ-13 Submitted | Theological review initiated (WF-11) |
| 3 | WF-11 Cleared | OBJ-14 Draft (lexicon ruling) | Council ruling required to add entry |
| 4 | OBJ-14 Ratified | OBJ-21 Active | Entry added to DOC-03.1 |
| 5 | OBJ-21 Active | OBJ-22 Created | Propagation record initiated |
| 6 | OBJ-22 Created | All clusters notified via IC-12 | Propagation executed |
| 7 | All acknowledged | OBJ-22 complete | Lexicon update implemented platform-wide |

**Amendment path:**
| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | OBJ-21 Active | OBJ-13 Submitted | Amendment proposal → theological review |
| 2 | WF-11 Cleared | OBJ-14 Draft (amendment ruling) | Council ruling for amendment |
| 3 | OBJ-14 Ratified | OBJ-21 Active (amended) | Entry updated; last_amended_date set |
| 4 | | OBJ-22 update_type = Amendment | Propagation initiated |

**Disqualification path:**
| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | OBJ-21 Active | OBJ-14 Ratified (disqualification) | Council ruling disqualifies term |
| 2 | OBJ-14 Ratified | OBJ-21 Disqualified | entry_status updated |
| 3 | OBJ-21 Disqualified | OBJ-22 update_type = Disqualification | Propagation with audit_triggered = True |
| 4 | Propagation | CLU-05.3 audit initiated | All platform documents checked for disqualified term |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | CLU-05.2 (Lexicon Management System) | Receives proposal; creates OBJ-21 Proposed; routes to WF-11 |
| 2 | CLU-02.2 (Theological Review Engine) | Reviews proposed entry (WF-11) |
| 3 | CLU-02.1 (Governing Authority Module) | Ratifies Council ruling on lexicon change (WF-10) |
| 4 | CLU-05.2 | Updates DOC-03.1 with ratified entry; creates OBJ-22 |
| 5 | All clusters | Receive IC-12 propagation; update internal references |
| 6 | CLU-05.3 (Language Audit Module) | On disqualification: initiates platform-wide audit |

## Data Transformations
- Proposal → OBJ-21: term, domain, definition, scriptural_anchor, theological_context, disqualified_uses populated
- Theological review Cleared → OBJ-13 Cleared; Council ruling initiated
- Council ruling Ratified → OBJ-21.entry_status = Active; council_ruling_ref populated; DOC-03.1 updated
- OBJ-21 Active → OBJ-22 created: update_type = New-entry; effective_date set
- Disqualification ruling → OBJ-21.entry_status = Disqualified; OBJ-22.update_type = Disqualification; compliance_audit_triggered = True
- CLU-05.3 audit → all OBJ-20 records for documents containing disqualified term invalidated; re-review required

## Timing Rules
- No lexicon entry is added, amended, or disqualified without completing theological review and Council ruling
- Disqualification propagation is immediate on ruling ratification
- Compliance audit on disqualification must be initiated on same date as propagation
- Clusters must implement lexicon updates by effective_date

## Escalation Paths
- Lexicon gap on urgent formation term: expedited theological review and Council ruling
- Cluster noncompliance with effective_date: escalated to CLU-02.1 (LG-009)
- Disqualification audit reveals widespread use: Council notified; remediation plan required

## Completion Conditions
- OBJ-21.entry_status = Active (new or amended) or Disqualified
- OBJ-21.council_ruling_ref populated
- OBJ-22 propagation record created
- IC-12 propagation complete with all clusters Acknowledged
- DOC-03.1 updated and OBJ-20 compliance status invalidated for affected content (disqualification only)

---

# WF-14 — CAPITAL SOURCE INTAKE AND CLEARANCE

## Behavior Description
An individual, organization, or institution is evaluated as a potential capital source. Source identity and affiliation are recorded. An integrity evaluation is conducted against DOC-01.4 standards. Cleared sources enter the capital pipeline; Conditional sources require acknowledgment; Disqualified sources are permanently blocked.

## Triggering Conditions
- Donor, grant, or institutional funding opportunity identified
- CLU-03.2 or CLU-06.2 refers a prospective source for integrity evaluation
- Existing source clearance has expired and re-evaluation is required

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | No record | OBJ-16 Created | Source identification and submission |
| 2 | OBJ-16 Created | OBJ-17 Under-evaluation | CLU-03.1 initiates integrity review |
| 3a | OBJ-17 Under-evaluation | OBJ-17 Cleared | No integrity concerns identified |
| 3b | OBJ-17 Under-evaluation | OBJ-17 Conditional | Concerns identified; conditions required |
| 3c | OBJ-17 Under-evaluation | OBJ-17 Disqualified | Integrity disqualification |
| 4a | OBJ-17 Cleared | Source enters CLU-03.2 and CLU-06.1 pipelines | Capital may be received |
| 4b | OBJ-17 Conditional | Source held pending acknowledgment | CLU-03.6 contacts source |
| 4c | OBJ-17 Disqualified | Source permanently blocked | Disqualification record created; CLU-03.4 notified |
| 5b | Conditions acknowledged | OBJ-17 Cleared | Pipeline entry enabled |
| 6 | OBJ-17.expiry_date reached | OBJ-17 Expired | Re-evaluation required; pipeline entry suspended |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | CLU-03.1 (Capital Source Integrity Filter) | Creates OBJ-16 and OBJ-17; conducts evaluation |
| 2 | CLU-02.2 (Theological Review Engine) | Receives escalations for complex integrity questions |
| 3 | CLU-03.6 (Donor Relations Interface) | Contacts source for condition acknowledgment |
| 4 | CLU-03.2 (Generative Giving Engine) | Receives Cleared source record |
| 5 | CLU-06.1 (Funding Stream Manager) | Receives Cleared source for pipeline entry |
| 6 | CLU-03.4 (Financial Integrity Reporting) | Receives disqualification records for reporting |

## Data Transformations
- Source identification → OBJ-16: source_name, source_type, source_affiliation, proposed_conditions populated
- Integrity evaluation → OBJ-17: integrity_status, disqualification_basis or conditional_requirements populated
- Cleared → OBJ-16.current_clearance_id = OBJ-17; expiry_date set; pipelines notified via IC-09
- Conditional → CLU-03.6 notified; conditions_acknowledged held False until source acknowledges
- Conditions acknowledged → OBJ-17.conditions_acknowledged = True; integrity_status = Cleared
- Disqualified → OBJ-17 permanent record; CLU-03.4 financial integrity report updated
- Expiry → OBJ-17 status = Expired; pipeline suspension triggered until re-evaluation

## Timing Rules
- Integrity evaluation must complete before any capital from the source enters the pipeline
- Clearance expiry is enforced at point of transaction — expired clearance does not block new submission, but does block pipeline
- Disqualification has no expiry — permanent unless Council ruling reverses
- Conditional acknowledgment must be received within defined window before clearance is granted

## Escalation Paths
- Complex affiliations requiring theological determination: escalated to CLU-02.2 (WF-11)
- Disqualified source attempting re-entry: CA-002 CRITICAL; CLU-02.1 notified
- Funds received from disqualified source: CA-001 CRITICAL; transaction blocked; reversal initiated

## Completion Conditions
- OBJ-16 record created and linked to OBJ-17
- OBJ-17.integrity_status = Cleared
- OBJ-17.expiry_date set
- Source accessible in CLU-03.2 and CLU-06.1 pipelines
- If Disqualified: OBJ-17 stored; CLU-03.4 updated; source blocked from all pipelines

---

# WF-15 — FUND ALLOCATION AND DISBURSEMENT

## Behavior Description
Approved capital is allocated by Council directive to platform operations, hub deployments, or training. Allocations are translated into disbursement authorizations. Funds are tracked from allocation through disbursement with sufficiency standard enforcement at every step.

## Triggering Conditions
- Council issues allocation directive for specific operational purpose
- Hub deployment request (CLU-04.1) triggers deployment funding request to CLU-06.6
- Operational budget cycle requires periodic allocation review

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | No allocation | OBJ-18 Created | Council authorization received |
| 2 | OBJ-18 Created | Sufficiency check | CLU-06.4 validates against sufficiency standard |
| 3a | Sufficiency compliant | OBJ-18 Active | Allocation confirmed |
| 3b | Sufficiency breach | OBJ-18 Blocked | CA-007; CLU-06.4 and CLU-02.1 notified |
| 4 | OBJ-18 Active | OBJ-19 Created | Disbursement authorization initiated |
| 5 | OBJ-19 Created | OBJ-19 Authorized | CLU-06.6 issues authorization |
| 6 | OBJ-19 Authorized | OBJ-19 Disbursed | Funds released; disbursement_date recorded |
| 7 | OBJ-19 Disbursed | CLU-06.5 reporting updated | Capital report record created |
| 8 | OBJ-25 (Deployment) | Hub launch gate opened | IC-14 transmits to CLU-04.1 |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | CLU-02.1 (Governing Authority Module) | Issues Council authorization; creates OBJ-14 ruling |
| 2 | CLU-03.5 (Fund Allocation Logic) | Creates OBJ-18; routes to CLU-06.4 for sufficiency check |
| 3 | CLU-06.4 (Sufficiency Standard Enforcer) | Validates allocation against sufficiency standard |
| 4 | CLU-06.6 (Deployment Funding Logic) | Creates OBJ-19 and OBJ-25 for deployment allocations |
| 5 | CLU-06.5 (Capital Reporting Interface) | Receives disbursement records for reporting |
| 6 | CLU-03.4 (Financial Integrity Reporting) | Receives allocation and disbursement data |
| 7 | CLU-04.1 (Hub Formation Protocol) | Receives OBJ-25 via IC-14 to unblock hub launch |

## Data Transformations
- Council authorization → OBJ-18: allocation_type, allocated_amount, destination_id, council_authorization_ref populated
- CLU-06.4 check → OBJ-18.sufficiency_compliance_ref populated
- OBJ-18 Active → OBJ-19 created: authorized_amount, expiry_date, disbursement_status = Authorized
- Disbursement execution → OBJ-19.disbursement_status = Disbursed; disbursement_date set
- OBJ-19 Disbursed → OBJ-18.allocation_status = Disbursed; OBJ-19.reporting_ref populated
- Deployment allocation → OBJ-25 created and transmitted via IC-14

## Timing Rules
- Sufficiency check must complete before allocation is Active
- Disbursement authorization expiry is enforced — expired authorizations require new Council ruling
- Deployment funding expiry (OBJ-25.expiry_date) enforced at hub launch gate
- Surplus identification: CLU-06.4 flags surplus continuously; Council must action within defined period

## Escalation Paths
- Sufficiency breach: CA-007 CRITICAL; CLU-06.4 and CLU-02.1 notified; allocation blocked until Council resolution
- Single source concentration exceeded: CA-011 ERROR; CLU-06.1 notified; diversification review required
- Deployment authorization expired: CA-010; hub launch held; CLU-06.6 and CLU-02.1 notified

## Completion Conditions
- OBJ-19.disbursement_status = Disbursed
- OBJ-19.disbursement_date populated
- OBJ-18.allocation_status = Disbursed
- OBJ-19.reporting_ref populated
- CLU-06.5 and CLU-03.4 reporting records updated

---

# WF-16 — AGGREGATE REPORTING

## Behavior Description
On schedule or Council request, the Restoration Record Keeper generates anonymized aggregate formation reports for Council governance review and capital reporting. Individual identifiers are never present. Report generation is logged. Unauthorized requests are blocked.

## Triggering Conditions
- Periodic reporting schedule reached
- CLU-02.1 submits governance report request
- CLU-06.5 submits capital report request
- Council-authorized ad hoc reporting request

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | Request submitted | Authorization validated | CLU-01.6 checks authorization_ref |
| 2 | Authorized | Report generated | CLU-01.6 aggregates OBJ-11 data |
| 3 | Report generated | OBJ-12 Created | Anonymized data packaged by report_type |
| 4 | OBJ-12 Created | Report delivered | Transmitted to requesting module |
| 5 | Report delivered | Log entry created | INFO log entry written |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | CLU-02.1 or CLU-06.5 | Submits authorized report request via IC-06 |
| 2 | CLU-01.6 (Restoration Record Keeper) | Validates authorization; aggregates OBJ-11 data |
| 3 | CLU-01.6 | Produces OBJ-12; applies report_type filters |
| 4 | CLU-02.1 | Receives Governance report; uses for platform oversight |
| 5 | CLU-06.5 | Receives Capital report; incorporates in capital reporting |

## Data Transformations
- OBJ-11 records (all participants in period) → OBJ-12 anonymized aggregate fields
- Governance report: total_participants, stage_distribution, domain_prevalence, blockage_frequency, milestone_completion_rate
- Capital report: participant_count, stage_completion_count, program_utilization_rate ONLY — no domain or severity data
- All individual identifiers removed before OBJ-12 is created — not filtered after

## Timing Rules
- Report generation follows defined periodic schedule; ad hoc requires Council authorization
- Governance and Capital reports may be generated independently on different schedules
- Log entry must be created within same session as report generation

## Escalation Paths
- Request without authorization_ref: DI-005 CRITICAL; request blocked
- Individual identifier detected in request: DI-002 CRITICAL; entire request rejected; logged for audit
- Unauthorized requesting module: DI-006 CRITICAL; blocked; Council notified

## Completion Conditions
- OBJ-12 created with correct report_type filters applied
- Report delivered to requesting module
- INFO log entry created referencing OBJ-12
- COCC-10 consistency check passes

---

# WF-17 — FACILITATOR ONBOARDING AND CERTIFICATION

## Behavior Description
A candidate is identified, assessed for formation background and theological alignment, completes the DOC-06.1 Facilitator Orientation Program, is reviewed by Council, and receives certification. Certification enables the facilitator to be assigned participants.

## Triggering Conditions
- Hub Leader identifies a facilitator candidate
- Council receives facilitator candidate nomination

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | No record | OBJ-02 Draft | Nomination received; record created |
| 2 | OBJ-02 Draft | OBJ-02 Provisional | Orientation enrollment confirmed |
| 3 | OBJ-02 Provisional | DOC-06.1 In-progress | Orientation program commenced |
| 4 | DOC-06.1 In-progress | DOC-06.1 Complete | Facilitator completes all orientation requirements |
| 5 | DOC-06.1 Complete | CLU-02.5 Review | Council accountability review |
| 6 | CLU-02.5 Review | OBJ-02 Certified | Council certifies; certification_ref populated |
| 7 | OBJ-02 Certified | Available for participant assignment | Facilitator appears in eligible roster |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | CLU-04 (Hub Leader) | Nominates candidate |
| 2 | CLU-02.5 (Member Accountability Module) | Creates OBJ-02; validates covenant; conducts review |
| 3 | CLU-06.1 (Facilitator Orientation) | Delivers DOC-06.1 program |
| 4 | CLU-02.2 (Theological Review Engine) | Reviews theological alignment as part of certification |
| 5 | CLU-01.5 (Formation Pathway Router) | Facilitator becomes available for pathway assignments |

## Data Transformations
- Nomination → OBJ-02: first_name, last_name, hub_id created in Draft status
- Orientation enrollment → OBJ-02.certification_status = Provisional
- DOC-06.1 completion → OBJ-26 equivalent orientation completion record; certification_ref populated
- Council review and approval → OBJ-02.certification_status = Certified; certification_date set
- Certified → OBJ-02 appears in eligible facilitator roster for CLU-01.5

## Timing Rules
- Provisional facilitators may not be assigned participants — only observe
- Certification review must include theological alignment assessment — not administrative only
- Covenant must be signed before certification is granted
- Lapsed covenant triggers standing review before any new assignments

## Escalation Paths
- Theological alignment concern during orientation: escalated to CLU-02.2 for review
- Certification denied: OBJ-02 held at Provisional; candidate may reapply after defined period
- Facilitator standing changes after certification: CLU-02.5 triggers participant reassignment protocol

## Completion Conditions
- OBJ-02.certification_status = Certified
- OBJ-02.certification_ref populated
- OBJ-02.covenant_ref populated
- OBJ-02.standing_status = Active
- Facilitator available for participant assignment in CLU-01.5 routing

---

# WF-18 — DOCUMENT PRODUCTION AND PLATFORM STATUS

## Behavior Description
A document is produced, passes through theological review and language compliance review, achieves platform status, and is distributed to the appropriate operational tier. Documents that fail review are corrected and resubmitted. Platform status is never granted without both clearances.

## Triggering Conditions
- Architect Mode or Council directive initiates document production
- Existing document requires amendment and re-review
- Deployment template or activation protocol requires formalization

## State Transitions

| Step | From State | To State | Trigger |
|---|---|---|---|
| 1 | No document | Document Draft | Production initiated |
| 2 | Document Draft | IC-07 submitted | Theological review requested (WF-11) |
| 3 | WF-11 Cleared | IC-11 submitted | Language compliance review requested (WF-12) |
| 4a | WF-12 Cleared | Document Platform-status | Both clearances obtained |
| 4b | WF-12 Flagged | Document returned for correction | Language revision required |
| 4c | WF-11 Disqualified | Document blocked | Permanent disqualification; no platform status |
| 5 | Document Platform-status | Document distributed to tier directory | Filed in correct tier subdirectory |
| 6 | Document distributed | Amendment log entry created | Initial amendment log populated |

## Module Interactions

| Sequence | Module | Action |
|---|---|---|
| 1 | Producing cluster or Architect Mode | Produces draft document |
| 2 | CLU-02.2 (Theological Review Engine) | Reviews via WF-11 |
| 3 | CLU-05.1 (Semantic Authority Enforcer) | Reviews via WF-12 |
| 4 | CLU-05.6 (External Communication Router) | Routes external-facing documents for additional review |
| 5 | CLU-01.6 or appropriate cluster | Stores document in correct directory |
| 6 | CLU-02.4 (Amendment and Ruling Registry) | Records initial amendment log entry |

## Data Transformations
- Draft document → OBJ-13 Theological Review Record created
- OBJ-13 Cleared → OBJ-20 Language Compliance Clearance created
- OBJ-20 Cleared → Document.platform_status = Active; clearance records linked
- Document Active → Filed in correct tier directory per SYSTEM-ARCHITECTURE-MANIFEST
- Filing → Document header populated: Reference, Version, Status = Active, Owning Authority, Date

## Timing Rules
- Theological review precedes language review — sequence is fixed
- Language review may not begin while theological review is pending
- External-facing documents require additional CLU-05.6 review before distribution
- Amendment log must be initialized on first platform-status grant

## Escalation Paths
- Theological disqualification: document blocked permanently; producing cluster notified; Council ruling required for any revival
- Repeated language flagging: escalated to CLU-02.2 for theological assessment of the language pattern
- Document distributed without clearance: LG-001 / GV-003 CRITICAL; platform status revoked; CLU-02.1 notified

## Completion Conditions
- OBJ-13.clearance_status = Cleared (theological review)
- OBJ-20.compliance_status = Cleared (language compliance)
- Document.platform_status = Active
- Document filed in correct tier directory
- Amendment log entry created with initial version record

---

---

# BEHAVIORAL CONSTRAINT SUMMARY

The following cross-workflow constraints govern all platform behavior and may not be relaxed by any single cluster, facilitator, or Hub Leader:

| Constraint ID | Statement |
|---|---|
| BC-01 | No stage advancement without completed milestones, active facilitator authorization, and no active blockage |
| BC-02 | No content achieves platform status without both theological review clearance and language compliance clearance |
| BC-03 | No hub becomes Active without Council authorization, qualified Hub Leader, signed covenant, and authorized deployment funding |
| BC-04 | No capital enters the platform pipeline without source integrity clearance |
| BC-05 | No Council ruling takes effect without quorum confirmation and documented scriptural basis |
| BC-06 | No escalation trigger is discretionary — all defined escalations execute automatically |
| BC-07 | No record is deleted — status transitions only, with permanent audit trail |
| BC-08 | No aggregate report contains individual identifiers under any circumstances |
| BC-09 | No lexicon entry is added, amended, or disqualified without Council ruling |
| BC-10 | Stage 4 → Stage 5 transition requires facilitator assessment submission — not milestone completion alone |
| BC-11 | Spiritual blockage requires Council referral — facilitator resolution is insufficient |
| BC-12 | Human authorization is required for all stage advancements, hub launches, Council rulings, and capital disbursements |

---

## AMENDMENT PROTOCOL

Amendments to this specification require:
1. Council of Metanoia review
2. Documented rationale referencing the affected workflow(s) and governing documents
3. Version increment and date update in document header
4. Notification to all clusters via IC-08

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
| 1.0 | 2026-03-30 | Initial specification created — 18 workflows, 12 behavioral constraints | Architect Mode |
