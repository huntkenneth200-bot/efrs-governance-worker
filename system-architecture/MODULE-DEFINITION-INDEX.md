# FORMATION INTELLIGENCE PLATFORM
## MODULE DEFINITION INDEX

**Document Reference:** MDI-01
**Version:** 1.0
**Status:** Active
**Owning Authority:** Council of Metanoia
**Prepared By:** Architect Mode — Claude Code
**Date:** 2026-03-30
**Review Cycle:** Upon architectural amendment only

---

## PURPOSE

This index defines every module and submodule in the Formation Intelligence Platform. For each entry it provides: module name, purpose, inputs, outputs, dependencies, constraints, and directory location. This document is the authoritative structural map for all build and integration work.

No module may be built, modified, or retired without a corresponding update to this index under Council review.

---

## INDEX STRUCTURE

The platform contains 6 top-level clusters. Each cluster contains 6 submodules. Total: 36 submodules across 6 clusters.

| Cluster ID | Cluster Name | Submodules |
|---|---|---|
| CLU-01 | Restoration OS | 01.1 – 01.6 |
| CLU-02 | Council of Metanoia | 02.1 – 02.6 |
| CLU-03 | Spikenard Foundation | 03.1 – 03.6 |
| CLU-04 | Emmaus Road | 04.1 – 04.6 |
| CLU-05 | Linguistic Diffusion Engine | 05.1 – 05.6 |
| CLU-06 | Capital Access Engine | 06.1 – 06.6 |

---

---

# CLUSTER 01 — RESTORATION OS

**Cluster Purpose:** Core formation operating system. Governs all individual fracture assessment, stage progression, milestone tracking, blockage detection, pathway routing, and restoration record management. All formation activity in the platform passes through or is governed by this cluster.

**Directory:** `system-architecture/phase-03-module-clusters/`
**Cluster Authority Doc:** DOC-01.6 (Scriptural Anthropology), DOC-03.2 (Fracture Domain Taxonomy), DOC-03.3 (Stage Schema Reference)

---

## 01.1 — Fracture Assessment Engine

**Purpose:** Receives raw intake and assessment data and produces a structured fracture profile for each individual. Determines which fracture domains are active, at what severity level, and from which origin type.

**Inputs:**
- Completed DOC-04.1 (Intake Questionnaire)
- Completed DOC-04.2 (Fracture Map Assessment Instrument)
- Facilitator observation notes (if applicable)

**Outputs:**
- Fracture Domain Profile (domains active: Identity / Authority / Relational / Vocational / Worldview)
- Severity classification per domain (L1 / L2 / L3)
- Origin markers per domain (Self-generated / Externally inflicted / Systemic)
- Recommended pathway entry point

**Dependencies:**
- DOC-03.2 (Fracture Domain Taxonomy) — classification logic
- DOC-03.3 (Stage Schema Reference) — entry stage alignment
- DOC-04.1, DOC-04.2 — data source instruments

**Constraints:**
- Must not assign severity without completed DOC-04.2 data
- Must not contradict Scriptural Anthropology (DOC-01.6) tripartite framework
- L3 severity designation requires Facilitator review before finalizing

**Directory:** `system-architecture/phase-04-submodules/`

---

## 01.2 — Stage Progression Logic

**Purpose:** Governs movement of individuals through the five Restoration OS formation stages. Evaluates milestone completion, blockage status, and Facilitator input to determine readiness for stage advancement.

**Inputs:**
- Current formation stage assignment
- Milestone completion records from 01.3
- Blockage flags from 01.4
- Facilitator stage-readiness assessment

**Outputs:**
- Stage advancement authorization or hold status
- Transition record with date and authorizing facilitator
- Updated stage assignment routed to 01.6

**Dependencies:**
- 01.3 (Milestone Tracking System) — completion data required
- 01.4 (Blockage Detection Module) — must be clear before advancement
- DOC-03.3 (Stage Schema Reference) — governs stage criteria
- DOC-03.4 (Milestone Definition Registry) — governs milestone thresholds

**Constraints:**
- Stage regression is permitted; must be documented with rationale
- No stage may be skipped
- Facilitator authorization required for all Stage 4 → 5 transitions
- Stage 1 (Stabilization) cannot be bypassed regardless of prior history

**Directory:** `system-architecture/phase-04-submodules/`

---

## 01.3 — Milestone Tracking System

**Purpose:** Tracks individual progress against defined formation milestones within each stage. Records milestone completion dates, partial completions, and facilitator attestations.

**Inputs:**
- Milestone registry from DOC-03.4
- Facilitator milestone attestation entries
- Periodic assessment data from DOC-04.3
- Current stage assignment from 01.2

**Outputs:**
- Milestone completion record per individual per stage
- Percentage completion indicator per stage
- Overdue milestone alerts
- Milestone data feed to 01.2 for stage progression evaluation

**Dependencies:**
- DOC-03.4 (Milestone Definition Registry) — authoritative milestone list
- DOC-04.3 (Periodic Formation Assessment) — data source
- 01.2 (Stage Progression Logic) — downstream consumer
- 01.4 (Blockage Detection Module) — stalled milestones may indicate blockage

**Constraints:**
- Milestone completion may not be self-reported by participants without Facilitator attestation
- Milestone definitions may not be modified within this module — amendments require DOC-03.4 update
- Records must be date-stamped and Facilitator-attributed

**Directory:** `system-architecture/phase-04-submodules/`

---

## 01.4 — Blockage Detection Module

**Purpose:** Identifies when an individual's formation progress has stalled or regressed. Flags specific blockage types, routes them to facilitator review, and tracks resolution.

**Inputs:**
- Milestone completion data from 01.3
- Stage duration flags (time-in-stage exceeding defined threshold)
- Periodic assessment data from DOC-04.3
- Facilitator-submitted blockage observations

**Outputs:**
- Blockage flag with type classification (formation / relational / spiritual / external)
- Severity indicator
- Recommended facilitator response protocol
- Blockage resolution record upon clearance

**Dependencies:**
- 01.3 (Milestone Tracking System) — stalled milestone data
- 01.2 (Stage Progression Logic) — blockage holds advancement
- DOC-03.2 (Fracture Domain Taxonomy) — blockage may indicate unaddressed fracture domain
- DOC-02.1 (Facilitator Operations Manual) — facilitator response protocols

**Constraints:**
- Blockage flags may not be cleared without documented facilitator review
- Spiritual blockage classification requires elder or Council referral
- Blockage data is confidential — not surfaced to participant without facilitator discretion

**Directory:** `system-architecture/phase-04-submodules/`

---

## 01.5 — Formation Pathway Router

**Purpose:** Assigns and manages each individual's formation pathway — the specific sequence of resources, sessions, and interventions prescribed based on their fracture profile and current stage. Routes individuals to appropriate hub programming, facilitator assignments, and supplemental resources.

**Inputs:**
- Fracture Domain Profile from 01.1
- Current stage assignment from 01.2
- Hub capacity and programming data from CLU-04
- Facilitator availability data from CLU-02

**Outputs:**
- Assigned formation pathway (stage + domain-specific sequence)
- Facilitator assignment
- Hub session schedule
- Pathway adjustment records upon re-assessment

**Dependencies:**
- 01.1 (Fracture Assessment Engine) — profile data
- 01.2 (Stage Progression Logic) — stage assignment
- CLU-04 (Emmaus Road) — hub programming inventory
- DOC-03.3 (Stage Schema Reference) — pathway logic anchored to stage definitions

**Constraints:**
- Pathway assignment may not override participant's active stage
- Pathway adjustments require documented re-assessment trigger
- Cross-hub routing requires Hub Leader notification

**Directory:** `system-architecture/phase-04-submodules/`

---

## 01.6 — Restoration Record Keeper

**Purpose:** Maintains the permanent, authoritative formation record for each individual. Stores all fracture profiles, stage assignments, milestone completions, blockage events, pathway assignments, and facilitator notes in a single auditable record.

**Inputs:**
- Outputs from all other CLU-01 submodules (01.1–01.5)
- Facilitator session notes
- Assessment instrument completions (DOC-04.1, 04.2, 04.3)

**Outputs:**
- Complete individual formation record
- Formation history summary (for facilitator review)
- Stage completion certificate data (upon Stage 5 completion)
- Anonymized aggregate data feed to CLU-02 for platform governance review

**Dependencies:**
- All CLU-01 submodules — primary data sources
- DOC-04.x assessment instruments
- CLU-02 (Council of Metanoia) — governance reporting consumer

**Constraints:**
- Records are permanent and may not be deleted — only amended with audit trail
- Access restricted to assigned facilitator, Hub Leader, and Council (aggregate only)
- Data handling must comply with DOC-01.1 confidentiality provisions
- Anonymized aggregate reports only to CLU-06 capital reporting

**Directory:** `system-architecture/phase-04-submodules/`

---
---

# CLUSTER 02 — COUNCIL OF METANOIA

**Cluster Purpose:** Supreme governing body of the platform. Holds theological review authority, constitutional governance, operational oversight, amendment power, member accountability, and external relationship management. All platform clusters are accountable to this cluster.

**Directory:** `system-architecture/phase-03-module-clusters/`
**Cluster Authority Doc:** DOC-01.1 (Platform Governing Charter), DOC-01.2 (Council Constitutional Charter)

---

## 02.1 — Governing Authority Module

**Purpose:** Executes the Council's constitutional authority over all platform operations. Processes platform-wide decisions, governance rulings, and policy amendments. Maintains the authoritative record of all Council actions.

**Inputs:**
- Proposed amendments from any cluster
- Governance escalations from Facilitators or Hub Leaders
- Platform health reports from CLU-01.6
- Theological review requests from 02.2

**Outputs:**
- Ratified Council rulings
- Amendment authorizations (routed to affected documents)
- Governance directives to cluster leads
- Council action log

**Dependencies:**
- DOC-01.2 (Council Constitutional Charter) — governs all Council operations
- DOC-01.1 (Platform Governing Charter) — governs amendment authority
- 02.4 (Amendment and Ruling Registry) — all rulings logged here

**Constraints:**
- No ruling may contradict Scripture or a Tier 1 governing document
- Quorum required for all binding rulings (per DOC-01.2 Article III)
- All rulings require written record with scriptural or doctrinal basis

**Directory:** `system-architecture/phase-04-submodules/`

---

## 02.2 — Theological Review Engine

**Purpose:** Evaluates all platform content, language, documents, and practices for theological integrity. Issues theological clearance, flags, or disqualification on any platform asset under review.

**Inputs:**
- New or amended documents submitted for review
- Language audit reports from CLU-05
- Facilitator practice reports flagged for review
- External content proposals

**Outputs:**
- Theological clearance status (approved / conditional / disqualified)
- Written theological rationale with scriptural basis
- Conditional approval requirements (if applicable)
- Disqualification records routed to 02.4

**Dependencies:**
- DOC-01.6 (Scriptural Anthropology Position Paper) — primary review standard
- DOC-01.5 (Language Authority Reference) — language evaluation standard
- DOC-01.3 (Household Theology) — community practice standard
- DOC-01.4 (Stewardship Theology) — financial practice standard
- CLU-05 (Linguistic Diffusion Engine) — language audit source

**Constraints:**
- Cannot grant clearance to content that contradicts any Tier 1 document
- Review must cite Scripture or Tier 1 document — opinion alone is insufficient
- Theological disqualification is non-negotiable without full Council reversal

**Directory:** `system-architecture/phase-04-submodules/`

---

## 02.3 — Council Operations Manager

**Purpose:** Manages the internal operational rhythms of the Council — meeting scheduling, agenda production, decision documentation, member communication, and administrative logistics.

**Inputs:**
- Member availability and scheduling data
- Pending agenda items from 02.1 and 02.2
- External communication requests from 02.6
- Administrative submissions from platform clusters

**Outputs:**
- Meeting schedules and agendas
- Decision documentation packages
- Member communication records
- Administrative action logs

**Dependencies:**
- DOC-01.2 (Council Constitutional Charter) — operational rules
- 02.1 (Governing Authority Module) — agenda items
- 02.5 (Member Accountability Module) — member status data

**Constraints:**
- Meetings must be convened per DOC-01.2 quorum and frequency requirements
- Agenda items must be submitted with governing document reference
- Records are permanent and Council-access only unless published by Council directive

**Directory:** `system-architecture/phase-04-submodules/`

---

## 02.4 — Amendment and Ruling Registry

**Purpose:** Maintains the permanent, authoritative log of all Council rulings, doctrinal positions, platform amendments, theological disqualifications, and governance decisions. Functions as the platform's legal and doctrinal memory.

**Inputs:**
- Ratified rulings from 02.1
- Theological review outcomes from 02.2
- Amendment authorizations affecting Tier 1–6 documents
- Disqualification records from CLU-05

**Outputs:**
- Indexed ruling registry (searchable by document, date, topic)
- Amendment logs appended to affected documents
- Disqualification register
- Ruling precedent reports for future Council review

**Dependencies:**
- 02.1 (Governing Authority Module) — source of rulings
- 02.2 (Theological Review Engine) — source of theological records
- All Tier 1 documents — amendment logs reference these documents

**Constraints:**
- Registry is immutable — entries may be superseded but not deleted
- All entries must include date, Council vote record, and scriptural/doctrinal basis
- Public access to this registry is at Council discretion

**Directory:** `system-architecture/phase-04-submodules/`

---

## 02.5 — Member Accountability Module

**Purpose:** Tracks Council member standing, covenant compliance, accountability actions, and disqualification events. Ensures all Council members remain qualified to exercise governing authority per DOC-01.2.

**Inputs:**
- Member covenant submissions and renewals
- Accountability review requests
- Disqualification triggers (per DOC-01.2 Article V)
- Reinstatement petitions

**Outputs:**
- Member standing status (active / under review / suspended / disqualified)
- Accountability action records
- Disqualification records routed to 02.4
- Reinstatement review records

**Dependencies:**
- DOC-01.2 (Council Constitutional Charter) — membership and accountability standards
- 02.4 (Amendment and Ruling Registry) — disqualification records stored here
- 02.3 (Council Operations Manager) — member status affects quorum calculation

**Constraints:**
- Disqualification is immediate upon trigger events defined in DOC-01.2
- Reinstatement requires full Council vote
- Member records are Council-confidential

**Directory:** `system-architecture/phase-04-submodules/`

---

## 02.6 — External Relations Interface

**Purpose:** Manages all Council-level communication with entities external to the platform — local churches, denominational bodies, partner organizations, and the public. Governs what platform information is shared externally and under what conditions.

**Inputs:**
- External partnership requests
- Public inquiry routing from CLU-05
- Inter-organization communication requests
- Council-approved public statements from 02.1

**Outputs:**
- Official Council correspondence
- Partnership agreement records
- Public statement releases
- External relations log

**Dependencies:**
- DOC-01.1 (Platform Governing Charter) — external relationship constraints (Article VIII)
- DOC-01.3 (Household Theology) — local church relationship posture
- 02.1 (Governing Authority Module) — all external communications require Council authorization

**Constraints:**
- No external representation may commit the platform without Council ratification
- All partnership agreements must be reviewed by 02.2 (Theological Review Engine)
- Platform architecture documents are not shared externally without Council directive

**Directory:** `system-architecture/phase-04-submodules/`

---
---

# CLUSTER 03 — SPIKENARD FOUNDATION

**Cluster Purpose:** Financial and stewardship governance layer. Manages capital source integrity, generative giving theology, fund allocation, financial integrity reporting, stewardship formation integration, and donor relations. All financial operations are subordinate to DOC-01.4 (Stewardship Theology).

**Directory:** `system-architecture/phase-03-module-clusters/`
**Cluster Authority Doc:** DOC-01.4 (Stewardship Theology Reference Document)

---

## 03.1 — Capital Source Integrity Filter

**Purpose:** Evaluates all incoming capital sources for theological and ethical compliance before funds are accepted. Disqualifies sources that violate DOC-01.4 capital source standards.

**Inputs:**
- Donor or grant source identification
- Source background and affiliation data
- Attached conditions or restrictions on proposed funds

**Outputs:**
- Source integrity status (approved / conditional / disqualified)
- Disqualification record with stated reason
- Conditional approval with required modifications
- Approved source routed to 03.2

**Dependencies:**
- DOC-01.4 (Stewardship Theology) — governing standard for capital source integrity
- 02.2 (Theological Review Engine) — escalation path for complex integrity questions
- 03.5 (Fund Allocation Logic) — approved sources enter allocation pipeline

**Constraints:**
- No funds accepted from disqualified sources regardless of amount
- Conditional approvals require donor acknowledgment of conditions before receipt
- Disqualification records are permanent

**Directory:** `system-architecture/phase-04-submodules/`

---

## 03.2 — Generative Giving Engine

**Purpose:** Manages and cultivates the generative giving culture of the platform — teaching, equipping, and sustaining a community of givers aligned with Kingdom Economics theology. Connects giving activity to formation outcomes.

**Inputs:**
- Approved donor records from 03.1
- Giving history and engagement data
- Formation stage data from CLU-01 (anonymized)
- Stewardship formation content from 03.3

**Outputs:**
- Donor stewardship communications
- Giving trend reports
- Formation-giving integration reports (anonymized)
- Generative giving community engagement records

**Dependencies:**
- DOC-01.4 (Stewardship Theology) — theological framework
- 03.1 (Capital Source Integrity Filter) — approved donors only
- 03.3 (Stewardship Formation Module) — content source

**Constraints:**
- Giving must never be instrumentalized as a formation incentive or requirement
- Communications must align with DOC-01.5 (Language Authority) and CLU-05
- Sufficiency standard governs all giving communications — wealth accumulation language disqualified

**Directory:** `system-architecture/phase-04-submodules/`

---

## 03.3 — Stewardship Formation Module

**Purpose:** Integrates stewardship theology into individual formation pathways. Provides formation content, teaching frameworks, and facilitator resources for stewardship as a formation domain.

**Inputs:**
- Formation pathway assignments from CLU-01.5
- DOC-01.4 stewardship theology content
- Facilitator requests for stewardship formation resources

**Outputs:**
- Stage-specific stewardship formation content
- Facilitator stewardship teaching guides
- Stewardship milestone definitions (fed to DOC-03.4)
- Integration records linking stewardship formation to fracture domain progress

**Dependencies:**
- DOC-01.4 (Stewardship Theology) — content authority
- CLU-01.5 (Formation Pathway Router) — integration into individual pathways
- DOC-03.4 (Milestone Definition Registry) — stewardship milestones registered here

**Constraints:**
- Content must not promote wealth accumulation theology
- Stewardship formation is integrated into existing stage pathway — not a separate track
- All content requires 02.2 (Theological Review) clearance

**Directory:** `system-architecture/phase-04-submodules/`

---

## 03.4 — Financial Integrity Reporting

**Purpose:** Produces all internal financial reports, stewardship accountability records, and governance reporting required by DOC-01.4. Ensures the platform's financial operations are fully transparent to the Council.

**Inputs:**
- Fund allocation records from 03.5
- Donor and source data from 03.1 and 03.2
- Expenditure records from all clusters
- Audit requests from CLU-02

**Outputs:**
- Periodic financial integrity reports to Council
- Expenditure accountability records
- Stewardship witness reports (for external stakeholder reporting, Council-authorized)
- Audit response packages

**Dependencies:**
- DOC-01.4 (Stewardship Theology) — reporting standard
- 02.1 (Governing Authority Module) — Council reporting recipient
- 03.5 (Fund Allocation Logic) — expenditure data source
- 03.1 (Capital Source Integrity Filter) — source integrity records

**Constraints:**
- All financial reports are Council-access by default
- No financial data shared externally without Council authorization
- Reports must reflect sufficiency standard — surplus handling must be documented

**Directory:** `system-architecture/phase-04-submodules/`

---

## 03.5 — Fund Allocation Logic

**Purpose:** Governs how approved capital is allocated across platform operations, hub deployments, facilitator support, and training resources. Applies sufficiency standard to all allocation decisions.

**Inputs:**
- Approved capital from 03.1
- Platform operational budget requirements from all clusters
- Deployment funding requests from CLU-06
- Council-approved allocation priorities from 02.1

**Outputs:**
- Allocation decisions with rationale
- Budget distribution records per cluster
- Deployment funding authorizations to CLU-06
- Sufficiency compliance record

**Dependencies:**
- DOC-01.4 (Stewardship Theology) — sufficiency standard governs all allocations
- 02.1 (Governing Authority Module) — allocation priorities set by Council
- CLU-06 (Capital Access Engine) — deployment funding pipeline
- 03.4 (Financial Integrity Reporting) — allocation records feed reporting

**Constraints:**
- Allocations may not create dependency on any single funding source
- Surplus beyond operational sufficiency must be redirected per DOC-01.4 protocols
- No allocation to theologically disqualified purposes

**Directory:** `system-architecture/phase-04-submodules/`

---

## 03.6 — Donor Relations Interface

**Purpose:** Manages all relational touchpoints with donors — communication, appreciation, formation integration, and boundary-setting. Ensures donor relationships are formed according to platform theology rather than transactional fundraising norms.

**Inputs:**
- Approved donor records from 03.1
- Generative giving engagement data from 03.2
- Council-authorized communication templates from CLU-05
- Donor inquiries and correspondence

**Outputs:**
- Donor communication records
- Relationship health indicators
- Formation integration reports (where donors are also participants)
- Escalation requests to 02.6 (External Relations) for complex donor relationships

**Dependencies:**
- DOC-01.4 (Stewardship Theology) — relational framework
- CLU-05 (Linguistic Diffusion Engine) — communication language standards
- 03.2 (Generative Giving Engine) — engagement data
- 02.6 (External Relations Interface) — escalation path

**Constraints:**
- Donor relationships may not be structured around giving-level tiers or preferential access
- Communication must not use manipulation, scarcity, or urgency tactics
- Donors who are also formation participants have their formation records treated separately

**Directory:** `system-architecture/phase-04-submodules/`

---
---

# CLUSTER 04 — EMMAUS ROAD

**Cluster Purpose:** Covenant community and hub operations layer. Governs hub formation, covenant community life, household rhythms, hospitality operations, local church relationships, and hub health. The Emmaus Road cluster is the primary deployment unit of the platform.

**Directory:** `system-architecture/phase-03-module-clusters/`
**Cluster Authority Doc:** DOC-01.3 (Household Theology Reference Document), DOC-02.2 (Hub Leader Operations Manual)

---

## 04.1 — Hub Formation Protocol

**Purpose:** Governs the process of establishing a new Emmaus Road hub site — from initial assessment through covenant community launch. Operationalizes DOC-02.5 (Hub Deployment Protocol Guide).

**Inputs:**
- Hub launch request with site assessment data
- Council authorization from 02.1
- Deployment template selection from Phase 9
- Hub Leader identification and qualification records

**Outputs:**
- Hub formation checklist and progress record
- Hub covenant document (site-specific)
- Hub Leader assignment record
- Hub registration in platform directory
- Launch readiness authorization

**Dependencies:**
- DOC-02.5 (Hub Deployment Protocol Guide) — process authority
- DOC-02.2 (Hub Leader Operations Manual) — leader qualification standards
- 02.1 (Governing Authority Module) — authorization required
- CLU-01 (Restoration OS) — formation infrastructure must be ready before launch

**Constraints:**
- No hub may launch without Council authorization
- Hub Leader must be qualified per DOC-02.2 standards
- All hubs operate under the Emmaus Road Hub Model (Luke 24 anchored)

**Directory:** `system-architecture/phase-04-submodules/`

---

## 04.2 — Covenant Community Engine

**Purpose:** Manages the ongoing covenant life of an active hub — covenant renewals, member accountability, community rhythm adherence, and covenant breach processes.

**Inputs:**
- Hub member covenant records
- Community rhythm compliance data from 04.3
- Accountability events from Hub Leader submissions
- Covenant renewal schedules

**Outputs:**
- Covenant status per member (active / renewal due / under review / released)
- Accountability action records
- Covenant breach documentation and resolution records
- Covenant renewal records

**Dependencies:**
- DOC-01.3 (Household Theology) — covenant community standard
- DOC-02.2 (Hub Leader Operations Manual) — Hub Leader accountability role
- 04.3 (Household Rhythm Scheduler) — rhythm data source
- CLU-01.3 (Milestone Tracking) — covenant milestones tracked here

**Constraints:**
- Covenant membership is voluntary but governed once entered
- Breach processes must be restorative in posture (per DOC-01.6 anthropology)
- Covenant release is not punitive — records remain respectful and accurate

**Directory:** `system-architecture/phase-04-submodules/`

---

## 04.3 — Household Rhythm Scheduler

**Purpose:** Manages the recurring formation rhythms of the hub community — gathering schedules, formation sessions, hospitality rotations, sabbath practices, and seasonal rhythms.

**Inputs:**
- Hub formation calendar
- Participant availability and session assignments from CLU-01.5
- Facilitator schedules from CLU-02
- Hospitality rotation assignments from 04.4

**Outputs:**
- Published hub formation calendar
- Session attendance records
- Rhythm compliance reports to 04.2
- Schedule conflict alerts

**Dependencies:**
- DOC-01.3 (Household Theology) — rhythm theology
- DOC-02.2 (Hub Leader Operations Manual) — scheduling authority
- CLU-01.5 (Formation Pathway Router) — session assignments
- 04.4 (Hospitality Operations Module) — hospitality integration

**Constraints:**
- Sabbath rhythms may not be scheduled over
- Formation sessions must align with stage-appropriate content
- Calendar is Hub Leader-controlled; CLU-01 may recommend but not override

**Directory:** `system-architecture/phase-04-submodules/`

---

## 04.4 — Hospitality Operations Module

**Purpose:** Governs the hospitality life of the hub — meal schedules, hosting assignments, guest integration, and household hospitality practices. Anchors hospitality as a formation practice, not a program.

**Inputs:**
- Hub member household availability
- Guest and newcomer intake requests
- Formation stage data (to assign hospitality role appropriately)
- Household rhythm schedule from 04.3

**Outputs:**
- Hospitality assignment records
- Guest intake and follow-up records
- Hospitality formation integration reports
- Newcomer to covenant pathway handoff records

**Dependencies:**
- DOC-01.3 (Household Theology) — hospitality theology
- 04.3 (Household Rhythm Scheduler) — scheduling integration
- CLU-01.5 (Formation Pathway Router) — appropriate hospitality role per stage

**Constraints:**
- Hospitality may not be assigned as a requirement before formation readiness
- Guest intake must not bypass CLU-01 intake process if formation is sought
- Hospitality records involving non-members are handled with confidentiality

**Directory:** `system-architecture/phase-04-submodules/`

---

## 04.5 — Local Church Interface

**Purpose:** Manages the relationship between the Emmaus Road hub and local church bodies in the hub's geographic context. Governs referral, partnership, non-competition posture, and pastoral coordination.

**Inputs:**
- Local church identification and relationship records
- Pastoral referral requests (inbound and outbound)
- Partnership proposals from local church leaders
- Council external relations data from 02.6

**Outputs:**
- Local church relationship records
- Referral coordination records
- Partnership agreements (pending 02.6 authorization)
- Pastoral coordination logs

**Dependencies:**
- DOC-01.3 (Household Theology) — local church relationship theology
- 02.6 (External Relations Interface) — Council-level partnership oversight
- DOC-01.1 (Platform Governing Charter) — Article VIII external relationships

**Constraints:**
- Platform does not position itself as a church substitute
- All formal partnerships require 02.6 and 02.2 clearance
- Referrals to local churches are encouraged; referrals from churches are received with intake protocol

**Directory:** `system-architecture/phase-04-submodules/`

---

## 04.6 — Hub Health Assessment

**Purpose:** Evaluates the ongoing health of an active hub across formation outcomes, covenant community vitality, hospitality practice, rhythm adherence, and leadership integrity.

**Inputs:**
- Formation outcome data from CLU-01 (anonymized aggregate)
- Covenant compliance data from 04.2
- Rhythm adherence data from 04.3
- Hub Leader self-assessment submission
- Facilitator field observations

**Outputs:**
- Hub health score and narrative report
- Identified risk areas with recommended interventions
- Escalation to Council (02.1) if health thresholds indicate systemic concern
- Hub health history record

**Dependencies:**
- All CLU-04 submodules — data sources
- CLU-01.6 (Restoration Record Keeper) — formation outcome data
- 02.1 (Governing Authority Module) — escalation recipient
- DOC-02.2 (Hub Leader Operations Manual) — health standard reference

**Constraints:**
- Hub health assessments are Council and Hub Leader access only
- Escalation to Council is mandatory if two consecutive assessments are below threshold
- Hub health data may not be used punitively against individual participants

**Directory:** `system-architecture/phase-04-submodules/`

---
---

# CLUSTER 05 — LINGUISTIC DIFFUSION ENGINE

**Cluster Purpose:** Language governance and formation communication layer. Enforces semantic authority, manages the platform lexicon, audits language usage, generates formation narrative, filters disqualified language, and routes all external communication. All language used in the platform is subject to this cluster.

**Directory:** `system-architecture/phase-03-module-clusters/`
**Cluster Authority Doc:** DOC-01.5 (Language Authority Reference Document), DOC-03.1 (Platform Lexicon)

---

## 05.1 — Semantic Authority Enforcer

**Purpose:** Governs the application of the Semantic Authority Hierarchy across all platform documents and communications. Ensures all language resolves to its correct authority level: Scripture → Council Rulings → Platform Lexicon → Editorial Standards → Facilitator Language.

**Inputs:**
- New or amended platform documents submitted for language review
- Facilitator communication samples
- External content proposed for platform use
- Language audit reports from 05.3

**Outputs:**
- Semantic compliance status (approved / flagged / disqualified)
- Flagged terms with correction recommendations
- Disqualification records routed to 05.5 and 02.4
- Compliance clearance for approved content

**Dependencies:**
- DOC-01.5 (Language Authority Reference) — governing standard
- DOC-03.1 (Platform Lexicon) — authorized term definitions
- 05.3 (Language Audit Module) — audit data
- 02.2 (Theological Review Engine) — escalation path for theologically complex language flags

**Constraints:**
- No document may receive platform status without semantic compliance clearance
- Facilitator language deviations are correctable; repeated violations require 02.5 review
- Scripture remains supreme — no platform term may redefine a Scriptural concept

**Directory:** `system-architecture/phase-04-submodules/`

---

## 05.2 — Lexicon Management System

**Purpose:** Manages the lifecycle of all Platform Lexicon entries — creation, amendment, disqualification, and cross-referencing. Ensures DOC-03.1 remains current, accurate, and authoritatively maintained.

**Inputs:**
- New term submission requests (from any cluster)
- Amendment proposals for existing entries
- Disqualification requests from 05.1 or 02.2
- Cross-reference update requirements

**Outputs:**
- Updated DOC-03.1 entries
- New entry records with Council approval status
- Disqualified term records
- Lexicon version history

**Dependencies:**
- DOC-03.1 (Platform Lexicon) — the document being managed
- 02.2 (Theological Review Engine) — all new entries require theological clearance
- 05.1 (Semantic Authority Enforcer) — new terms must pass semantic review
- 02.4 (Amendment and Ruling Registry) — all lexicon changes are Council-ruled amendments

**Constraints:**
- No new term added to DOC-03.1 without Council ruling
- Existing entries may not be modified without documented theological rationale
- Disqualified terms are logged permanently — not deleted

**Directory:** `system-architecture/phase-04-submodules/`

---

## 05.3 — Language Audit Module

**Purpose:** Conducts periodic and triggered audits of language usage across platform documents, facilitator communications, hub materials, and external-facing content. Identifies drift, unauthorized terms, and disqualified language in active use.

**Inputs:**
- Platform document corpus (all Tier documents)
- Facilitator communication samples
- Hub-produced materials
- External communications from 02.6

**Outputs:**
- Language audit reports with flagged instances
- Drift trend analysis (language shifting from authorized definitions)
- Urgent disqualification alerts to 05.1
- Remediation recommendations

**Dependencies:**
- DOC-03.1 (Platform Lexicon) — authorized term reference
- DOC-01.5 (Language Authority Reference) — audit standard
- 05.1 (Semantic Authority Enforcer) — flag routing
- 02.4 (Amendment and Ruling Registry) — historical ruling reference

**Constraints:**
- Audits must be conducted at minimum annually; triggered audits as needed
- Audit findings are not punitive — remediation-focused
- Systemic drift findings escalate to Council via 02.1

**Directory:** `system-architecture/phase-04-submodules/`

---

## 05.4 — Formation Narrative Generator

**Purpose:** Produces authorized narrative content — testimonials frameworks, formation story structures, platform communication templates, and formative language guides for facilitators and hub leaders.

**Inputs:**
- Authorized formation stage and milestone language from DOC-03.3 and DOC-03.4
- Lexicon entries from DOC-03.1
- Council-approved narrative frameworks
- Facilitator communication requests

**Outputs:**
- Formation story structure templates
- Facilitator communication scripts and guides
- Hub-level narrative resources
- Platform-wide communication templates

**Dependencies:**
- DOC-03.1 (Platform Lexicon) — all narrative uses authorized terms only
- DOC-01.5 (Language Authority Reference) — narrative language standard
- DOC-03.3 (Stage Schema Reference) — stage-specific language
- 05.1 (Semantic Authority Enforcer) — all outputs pass semantic review

**Constraints:**
- Narrative templates may not be modified by facilitators without CLU-05 review
- Participant formation stories are not platform property — participant consent governs usage
- All templates must reflect Scriptural anthropology (DOC-01.6)

**Directory:** `system-architecture/phase-04-submodules/`

---

## 05.5 — Disqualified Language Filter

**Purpose:** Maintains the authoritative registry of disqualified terms, phrases, frameworks, and language patterns. Enforces removal of disqualified language from all platform assets.

**Inputs:**
- Disqualification records from 05.1 and 02.2
- Audit flags from 05.3
- Council rulings from 02.4
- New disqualification requests from any cluster

**Outputs:**
- Disqualified language registry (indexed, searchable)
- Removal directives to affected documents
- Replacement recommendations using authorized alternatives
- Compliance record upon remediation

**Dependencies:**
- DOC-01.5 (Language Authority Reference) — disqualification authority
- DOC-03.1 (Platform Lexicon) — disqualified uses section of each entry
- 02.4 (Amendment and Ruling Registry) — Council ruling basis for disqualifications
- 05.1 (Semantic Authority Enforcer) — enforcement pipeline

**Constraints:**
- Disqualified terms list is Council-ratified — no unilateral additions
- Registry is permanent — disqualified status is not reversed without Council ruling
- Removal directives apply to all platform documents retroactively

**Directory:** `system-architecture/phase-04-submodules/`

---

## 05.6 — External Communication Router

**Purpose:** Governs all outbound platform communication to external audiences — public-facing language, partner communications, media responses, and digital presence content. Ensures all external language meets platform standards before release.

**Inputs:**
- Communication requests from any cluster
- Council-authorized statements from 02.1
- External partnership communications from 02.6
- Digital and media content requests

**Outputs:**
- Reviewed and cleared external communications
- Published communication records
- Language compliance certificates for external content
- Rejected communication records with remediation guidance

**Dependencies:**
- DOC-01.5 (Language Authority Reference) — external communication standard
- 05.1 (Semantic Authority Enforcer) — semantic review
- 02.6 (External Relations Interface) — authorization source for external comms
- 02.1 (Governing Authority Module) — Council-level statement authorization

**Constraints:**
- No external communication released without CLU-05 review
- Platform architecture details not shared externally without Council directive
- All public language must be accessible to non-platform audiences without theological distortion

**Directory:** `system-architecture/phase-04-submodules/`

---
---

# CLUSTER 06 — CAPITAL ACCESS ENGINE

**Cluster Purpose:** Funding and capital development layer. Manages all funding streams, grant and donor pipelines, Kingdom Economics application, sufficiency standard enforcement, capital reporting, and deployment funding. All capital activity is governed by DOC-01.4 (Stewardship Theology) and filtered through CLU-03 (Spikenard Foundation).

**Directory:** `system-architecture/phase-03-module-clusters/`
**Cluster Authority Doc:** DOC-01.4 (Stewardship Theology Reference Document)

---

## 06.1 — Funding Stream Manager

**Purpose:** Identifies, catalogs, and manages all active and potential funding streams available to the platform. Maintains a current funding stream inventory with source integrity status, stream health, and diversification indicators.

**Inputs:**
- Approved capital sources from CLU-03.1
- Grant and donor pipeline data from 06.2
- Funding stream performance reports
- Platform operational budget requirements from CLU-03.5

**Outputs:**
- Funding stream inventory (active, pending, closed)
- Stream health and diversification report
- At-risk stream alerts
- Funding gap analysis

**Dependencies:**
- CLU-03.1 (Capital Source Integrity Filter) — source approval prerequisite
- CLU-03.5 (Fund Allocation Logic) — allocation recipient
- DOC-01.4 (Stewardship Theology) — sufficiency and diversification standards

**Constraints:**
- No single stream may exceed Council-defined percentage of total operating budget
- All streams must maintain active CLU-03.1 integrity status
- Stream closure records are permanent

**Directory:** `system-architecture/phase-04-submodules/`

---

## 06.2 — Grant and Donor Pipeline

**Purpose:** Manages the development, tracking, and cultivation of grant opportunities and donor relationships from initial identification through receipt. Coordinates with CLU-03 for source integrity and CLU-05 for communication language.

**Inputs:**
- Grant opportunity identification data
- Donor cultivation records from CLU-03.6
- Source integrity clearance from CLU-03.1
- Proposal development requests

**Outputs:**
- Grant proposal records and submission history
- Donor cultivation pipeline status
- Funding received records
- Pipeline health report

**Dependencies:**
- CLU-03.1 (Capital Source Integrity Filter) — all pipeline entries require approval
- CLU-03.6 (Donor Relations Interface) — donor relationship data
- CLU-05 (Linguistic Diffusion Engine) — proposal language compliance
- 06.1 (Funding Stream Manager) — pipeline feeds stream inventory

**Constraints:**
- Proposals may not include theological compromise as a condition of funding
- All grant applications require 02.2 (Theological Review) for ideological alignment
- Donor pipeline must reflect generative giving theology — not transactional fundraising

**Directory:** `system-architecture/phase-04-submodules/`

---

## 06.3 — Kingdom Economics Module

**Purpose:** Applies Kingdom Economics theology (from DOC-01.4) to all capital access decisions. Evaluates funding strategies, economic structures, and financial practices for alignment with Biblical economic principles.

**Inputs:**
- Funding strategy proposals from 06.1 and 06.2
- Financial practice questions escalated from CLU-03
- Platform economic model review requests from Council

**Outputs:**
- Kingdom Economics compliance assessment
- Theological economic guidance documents
- Disqualified economic practice records
- Kingdom Economics formation content for CLU-03.3

**Dependencies:**
- DOC-01.4 (Stewardship Theology) — primary theological standard
- 02.2 (Theological Review Engine) — escalation path
- CLU-03.3 (Stewardship Formation Module) — content integration

**Constraints:**
- Debt-based financing requires Council ruling before adoption
- Investment strategies must comply with sufficiency standard
- Profit motive disqualified as a platform economic principle

**Directory:** `system-architecture/phase-04-submodules/`

---

## 06.4 — Sufficiency Standard Enforcer

**Purpose:** Applies the sufficiency standard from DOC-01.4 to all capital access and allocation decisions. Ensures the platform does not accumulate beyond operational sufficiency and that surplus is redirected per theological protocol.

**Inputs:**
- Funding stream inventory from 06.1
- Allocation records from CLU-03.5
- Operating budget data
- Reserve fund levels

**Outputs:**
- Sufficiency compliance status
- Surplus identification and redirection records
- Accumulation risk alerts
- Sufficiency standard audit reports to CLU-03.4

**Dependencies:**
- DOC-01.4 (Stewardship Theology) — sufficiency standard definition
- CLU-03.5 (Fund Allocation Logic) — allocation data
- CLU-03.4 (Financial Integrity Reporting) — reporting recipient
- 02.1 (Governing Authority Module) — surplus redirection decisions

**Constraints:**
- Surplus redirection decisions require Council authorization
- Reserve funds may not exceed Council-defined operational threshold
- Sufficiency standard applies to all platform entities, not only headquarters

**Directory:** `system-architecture/phase-04-submodules/`

---

## 06.5 — Capital Reporting Interface

**Purpose:** Produces all capital-related reports for Council review, platform governance, and authorized external disclosure. Aggregates data from all capital activity into auditable reporting packages.

**Inputs:**
- Funding stream data from 06.1
- Pipeline data from 06.2
- Sufficiency compliance records from 06.4
- Allocation records from CLU-03.5
- Financial integrity records from CLU-03.4

**Outputs:**
- Periodic capital reports to Council
- Deployment funding status reports
- External stewardship reports (Council-authorized)
- Audit-ready capital record packages

**Dependencies:**
- All CLU-06 submodules — data sources
- CLU-03.4 (Financial Integrity Reporting) — consolidated with financial reports
- 02.1 (Governing Authority Module) — Council report recipient
- DOC-01.4 (Stewardship Theology) — reporting standard

**Constraints:**
- Capital reports are Council-access by default
- External reporting requires Council authorization per 02.6
- Reports must reflect actual activity — projections clearly labeled as such

**Directory:** `system-architecture/phase-04-submodules/`

---

## 06.6 — Deployment Funding Logic

**Purpose:** Manages the capital allocation process specifically for hub deployments — calculating funding requirements, authorizing deployment budgets, and tracking expenditure against deployment templates.

**Inputs:**
- Hub deployment requests from CLU-04.1
- Deployment template budget specifications from Phase 9
- Available capital from CLU-03.5 (Fund Allocation Logic)
- Council deployment authorization from 02.1

**Outputs:**
- Deployment funding authorization
- Deployment budget records
- Expenditure tracking reports per deployment
- Post-deployment financial reconciliation records

**Dependencies:**
- Phase 9 Deployment Templates (DT-01 through DT-08) — budget specifications
- CLU-03.5 (Fund Allocation Logic) — capital source
- CLU-04.1 (Hub Formation Protocol) — deployment trigger
- 02.1 (Governing Authority Module) — authorization required

**Constraints:**
- No deployment funded without Council authorization
- Deployment expenditure may not exceed template budget without Council amendment
- All deployment financial records route to 06.5 for consolidated reporting

**Directory:** `system-architecture/phase-04-submodules/`

---
---

## INDEX SUMMARY

| Cluster | Submodules | Directory |
|---|---|---|
| CLU-01 Restoration OS | 01.1 – 01.6 | `phase-04-submodules/` |
| CLU-02 Council of Metanoia | 02.1 – 02.6 | `phase-04-submodules/` |
| CLU-03 Spikenard Foundation | 03.1 – 03.6 | `phase-04-submodules/` |
| CLU-04 Emmaus Road | 04.1 – 04.6 | `phase-04-submodules/` |
| CLU-05 Linguistic Diffusion Engine | 05.1 – 05.6 | `phase-04-submodules/` |
| CLU-06 Capital Access Engine | 06.1 – 06.6 | `phase-04-submodules/` |
| **Total** | **36 submodules** | |

---

## AMENDMENT PROTOCOL

Amendments to this index require:
1. Council of Metanoia review
2. Documented rationale referencing the governing architectural phase output
3. Version increment and date update in document header
4. Corresponding update to SYSTEM-ARCHITECTURE-MANIFEST.md if directory structure changes

---

## AUTHORIZATION RECORD

| Role | Name | Status |
|---|---|---|
| Architect | — | Pending Council signature |
| Council Chair | — | Pending |
| Systems Engineer | — | Pending |

**Amendment Log:**

| Version | Date | Change | Authority |
|---|---|---|---|
| 1.0 | 2026-03-30 | Initial index created — all 36 submodules defined | Architect Mode |
