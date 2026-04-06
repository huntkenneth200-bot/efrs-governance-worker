# FORMATION INTELLIGENCE PLATFORM
## SYSTEM ARCHITECTURE MANIFEST

**Document Reference:** MANIFEST-01
**Version:** 1.0
**Status:** Active
**Owning Authority:** Council of Metanoia
**Prepared By:** Architect Mode — Claude Code
**Date:** 2026-03-30
**Review Cycle:** Upon structural amendment only

---

## PURPOSE

This manifest is the authoritative reference for the Formation Intelligence Platform file system. It defines the purpose of every top-level directory, its relationship to the platform architecture, governing constraints, and the types of files or modules that will reside within it.

All contributors, builders, and deployers must orient to this manifest before creating, moving, or modifying any file within the platform.

---

## ROOT DIRECTORY

**Path:** `Formation-Intelligence-Platform/`

**Purpose:** Root container for all platform assets. Every document, schema, assessment, training module, and architectural artifact produced under the Formation Intelligence Platform governing sequence resides within this root.

**Governing Constraint:** No files are created directly in the root except this manifest and the project index. All content belongs in a designated subdirectory.

**Authority:** Council of Metanoia — Platform Governing Charter (DOC-01.1)

---

## TOP-LEVEL DIRECTORY DEFINITIONS

---

### 1. `system-architecture/`

**Purpose:** Contains all architectural phase outputs produced during the initial 9-phase build sequence. These are the governing blueprints from which every operational document, assessment, and training module derives.

**Platform Relationship:** Foundational layer. All Tier documents trace authority to outputs housed here. No Tier document may contradict an architectural phase output without a Council ruling.

**Subdirectories and Contents:**

| Subdirectory | Phase | Contents |
|---|---|---|
| `phase-02-platform-map/` | Phase 2 | Top-level platform map; 6-cluster architecture diagram and narrative |
| `phase-03-module-clusters/` | Phase 3 | 6 cluster specification documents |
| `phase-04-submodules/` | Phase 4 | 36 submodule specification documents (6 per cluster) |
| `phase-05-interface-contracts/` | Phase 5 | 14 interface contracts (IC-01 through IC-14) |
| `phase-06-documentation-layer/` | Phase 6 | Documentation layer definition; 44-document registry |
| `phase-07-diffusion-layer/` | Phase 7 | 6 diffusion modules (07.1 through 07.6) |
| `phase-08-activation-protocols/` | Phase 8 | 6 activation protocol documents (AP-01 through AP-06) |
| `phase-09-deployment-templates/` | Phase 9 | 8 deployment templates (DT-01 through DT-08) |

**File Types Expected:** Markdown (.md) — one file per architectural component

---

### 2. `tier-01-governing/`

**Purpose:** Houses all Tier 1 governing documents. These are the theological, constitutional, and doctrinal foundations of the platform. No platform operation, document, or formation activity may contradict a Tier 1 document.

**Platform Relationship:** Supreme governing layer, second only to Scripture. All Tier 2–6 documents are subordinate to Tier 1.

**Authority Hierarchy Position:** Scripture → Tier 1 Documents → All Other Platform Assets

**Contents:**

| File | Document |
|---|---|
| `DOC-01-1-platform-governing-charter.md` | Platform Governing Charter |
| `DOC-01-2-council-constitutional-charter.md` | Council Constitutional Charter |
| `DOC-01-3-household-theology-reference.md` | Household Theology Reference Document |
| `DOC-01-4-stewardship-theology-reference.md` | Stewardship Theology Reference Document |
| `DOC-01-5-language-authority-reference.md` | Language Authority Reference Document |
| `DOC-01-6-scriptural-anthropology-position-paper.md` | Scriptural Anthropology Position Paper |

**File Types Expected:** Markdown (.md) — one file per document, no subdirectories required

---

### 3. `tier-02-operations/`

**Purpose:** Houses all operational manuals and deployment guides used by Facilitators, Hub Leaders, and deployment teams. These documents translate platform architecture into executable field instructions.

**Platform Relationship:** Operational translation layer. Tier 2 documents operationalize Tier 1 theology and Phase 2–9 architecture into human-executable processes.

**Governing Constraint:** All procedural instructions must align with DOC-01.1 (Governing Charter), DOC-01.2 (Council Charter), and DOC-01.6 (Anthropology Position Paper).

**Subdirectories and Contents:**

| Subdirectory | Document | Description |
|---|---|---|
| `DOC-02-1-facilitator-operations-manual/` | DOC-02.1 | Full operational manual for formation facilitators |
| `DOC-02-1B-facilitator-field-guide/` | DOC-02.1B | Condensed field reference for active facilitation use |
| `DOC-02-2-hub-leader-operations-manual/` | DOC-02.2 | Full operational manual for Emmaus Road Hub leaders |
| `DOC-02-5-hub-deployment-protocol-guide/` | DOC-02.5 | Step-by-step protocol for launching a new hub site |

**Note:** DOC-02.3 and DOC-02.4 are not required. Those registry entries are undefined and excluded from the build.

**File Types Expected:** Markdown (.md) primary document per subdirectory; supporting appendices or reference sheets as needed

---

### 4. `tier-03-schemas/`

**Purpose:** Houses all structural schemas, taxonomies, and reference definitions that govern how the platform categorizes, classifies, and processes formation data. These schemas are the semantic and diagnostic backbone of the platform.

**Platform Relationship:** Definitional infrastructure layer. All assessments (Tier 4), operations (Tier 2), and training (Tier 6) depend on Tier 3 schemas for consistency of terminology and classification.

**Governing Constraint:** All terms used in platform documents must resolve to an entry in DOC-03.1 (Platform Lexicon) or be submitted for Council ruling.

**Subdirectories and Contents:**

| Subdirectory | Document | Description |
|---|---|---|
| `DOC-03-1-platform-lexicon/` | DOC-03.1 | Master reference for all authorized platform terminology (27 entries, 6 domains) |
| `DOC-03-2-fracture-domain-taxonomy/` | DOC-03.2 | Classification system for the five fracture domains with severity and origin markers |
| `DOC-03-3-stage-schema-reference/` | DOC-03.3 | Definitive schema for the five Restoration OS formation stages |
| `DOC-03-4-milestone-definition-registry/` | DOC-03.4 | Registry of all formation milestones mapped to stages and domains |

**File Types Expected:** Markdown (.md) primary schema document; supporting tables or cross-reference indexes as needed

---

### 5. `tier-04-assessments/`

**Purpose:** Houses all assessment instruments used to evaluate, diagnose, and track the formation status of individuals. These instruments are the primary data collection tools of the platform.

**Platform Relationship:** Diagnostic layer. Assessment outputs feed directly into facilitator decision-making, stage assignment, fracture mapping, and milestone tracking. All instruments must align with Tier 3 schemas.

**Governing Constraint:** No assessment question or scoring rubric may contradict DOC-01.6 (Scriptural Anthropology), DOC-03.2 (Fracture Domain Taxonomy), or DOC-03.3 (Stage Schema Reference).

**Subdirectories and Contents:**

| Subdirectory | Document | Description |
|---|---|---|
| `DOC-04-1-intake-questionnaire/` | DOC-04.1 | Initial intake instrument for new formation participants |
| `DOC-04-2-fracture-map-assessment/` | DOC-04.2 | Diagnostic instrument for mapping fracture domain and severity |
| `DOC-04-3-periodic-formation-assessment/` | DOC-04.3 | Recurring instrument for tracking formation progress across stages |

**File Types Expected:** Markdown (.md) primary instrument; scoring guides, response rubrics, and facilitator instructions as supporting files within subdirectory

---

### 6. `tier-06-training/`

**Purpose:** Houses all training and orientation programs that prepare Facilitators, Hub Leaders, and Council members for platform service. Training must produce formation-aligned, theologically grounded practitioners.

**Platform Relationship:** Equipping layer. Tier 6 training outputs are downstream of all Tier 1–4 documents. Trainees are formed according to the same schemas, lexicon, and anthropology that govern participant formation.

**Governing Constraint:** No training content may contradict any Tier 1 governing document. All training must align with DOC-02.1 (Facilitator Operations Manual) for facilitator-track content.

**Subdirectories and Contents:**

| Subdirectory | Document | Description |
|---|---|---|
| `DOC-06-1-facilitator-orientation-program/` | DOC-06.1 | Full orientation curriculum for new platform facilitators |

**Note:** Additional DOC-06.x entries are not required at this time. This tier remains open for future expansion under Council directive.

**File Types Expected:** Markdown (.md) primary curriculum document; session outlines, resource lists, and facilitator notes as supporting files within subdirectory

---

## EXCLUDED SERIES

| Series | Status | Reason |
|---|---|---|
| DOC-02.3 | UNDEFINED / NOT REQUIRED | Not defined in governing sequence |
| DOC-02.4 | UNDEFINED / NOT REQUIRED | Not defined in governing sequence |
| DOC-05.x (entire series) | NOT REQUIRED | Tracking and reporting tier excluded from Claude Code build-out |

---

## FILE NAMING CONVENTION

All files within this platform follow this convention:

```
DOC-[TIER]-[NUMBER]-[descriptor].md
```

Examples:
- `DOC-01-1-platform-governing-charter.md`
- `DOC-03-2-fracture-domain-taxonomy.md`
- `DOC-04-1-intake-questionnaire.md`

Supporting files within a subdirectory use the parent document ID as prefix:
```
DOC-02-1-appendix-A-session-templates.md
DOC-04-2-scoring-rubric.md
```

---

## AMENDMENT PROTOCOL

Amendments to this manifest require:
1. Council of Metanoia review
2. Documented rationale referencing a governing document or architectural phase output
3. Version increment and date update in document header

No directory may be added, renamed, or removed without an updated manifest entry.

---

## AUTHORIZATION RECORD

| Role | Name | Status |
|---|---|---|
| Architect | — | Pending Council signature |
| Council Chair | — | Pending |
| Documentation Lead | — | Pending |

**Amendment Log:**

| Version | Date | Change | Authority |
|---|---|---|---|
| 1.0 | 2026-03-30 | Initial manifest created — directory scaffold complete | Architect Mode |
