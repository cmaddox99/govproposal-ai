# Proposal: Enrich Product Discovery Stage A–F Workflow

**Proposal ID:** `enrich-product-discovery-stage-a-f`
**Submitted:** 2026-04-14
**Revised:** 2026-04-15 — Gap 6 + human amendments incorporated after ensemble deliberation
**Status:** APPROVED WITH CONDITIONS
**Ensemble Deliberation:** `ensemble-pr31-gap6-2026-04-15` — APPROVED (5/5 roles; 2 conditional)
**Approved By:** adeel-ali-aa (human gate, 2026-04-15)
**Discovery Source:** `gate-mgmt` — disc-2026-001 Stage A test run
**Laws:** ENG-11.1 (NON-NEGOTIABLE), ENG-11.2, PRD-2.5 (NON-NEGOTIABLE), PRD-2.1, BUS-7.1 (NON-NEGOTIABLE), ENG-13.1 (elevated to NON-NEGOTIABLE by D17)

---

## Problem

A test run of the `product-discovery-stage-a-f` workflow against the `gate-mgmt` monorepo
(disc-2026-001) identified five structural gaps in the workflow and its orchestration skill.
A subsequent ensemble deliberation (2026-04-15) identified a sixth gap, added by adeel-ali-aa,
and two human amendments (Q4, Q5) that extend the scope to 23 deliverables.
These gaps create ambiguity, make audit compliance harder to verify, and allow inconsistent
execution across teams. All five gaps were observed during Stage A execution — the first and
most foundational stage of the discovery process.

---

### Gap 1 — No Discovery ID Format Standard

**Location:** `workflows/product-discovery-stage-a-f.md`, `agent-skills/…/product-discovery-orchestration.md`

The workflow references `[discovery-id]` as the folder name for all spec artifacts
(`hangar-ai-specs/changes/[discovery-id]/`) but provides no convention for what that ID
should look like. During disc-2026-001, the format `disc-YYYY-NNN` was invented ad hoc.

Without a standard:
- IDs will be inconsistent across teams and projects
- Automated tooling (lint, audit log parsers, RAG retrieval) cannot reliably address discovery artifacts
- Stage-gate audit trails (BUS-7.1) cannot be correlated across related discoveries

**Violated Laws:** PRD-2.5 (evidence traceability), BUS-7.1 (audit record correlation), ENG-11.1 (spec folder contract)

---

### Gap 2 — Avatar Activation Has No Verifiable Confirmation Mechanism

**Location:** `workflows/product-discovery-stage-a-f.md` Stage A entry, `agent-skills/…/product-discovery-orchestration.md` §Initialize Discovery

Stage A requires activating Product and Business avatars, but neither the workflow nor the
orchestration skill defines a confirmation artifact, checklist signal, or state record for
this activation. An agent executing Stage A cannot prove avatars were activated.

Without verification:
- A discovery can proceed without the correct constitutional context applied
- PRD-2.5 stage-gate transitions cannot confirm avatar compliance
- BUS-7.1 audit events cannot record which avatars were active and when
- Governance reviews have no evidence that avatar context was correct

**Violated Laws:** PRD-2.5 (evidence at transition), BUS-7.1 (audit who/what/when), ENG-11.2 (PROPOSAL must name participating avatars — but the workflow does not require this by spec)

---

### Gap 3 — Stakeholder Approval Not Bound to a Named Actor or Role

**Location:** `workflows/product-discovery-stage-a-f.md` Stage A exit gate

The Stage A exit gate is: *"Problem statement approved"* — but the workflow does not specify:
- Who is authorised to give that approval (Product Owner? Sponsor? Director?)
- How approval is captured (verbal? written? comment in PR? entry in PROPOSAL.md?)
- What constitutes a valid rejection and the remediation path

Without this:
- The exit gate is unenforceable — any team member could self-certify
- BUS-7.1 audit records cannot satisfy the *"who"* field for stage-gate events
- PRD-2.5 cannot be operationally non-negotiable if the gate itself is undefined

**Violated Laws:** PRD-2.5 (gate must be real, not nominal), PRD-2.1 (problem validation requires
an external, authorised approver), BUS-7.1 (audit trail: who approved, when, outcome)

---

### Gap 4 — Stage A Has No PROPOSAL.md Template

**Location:** `workflows/product-discovery-stage-a-f.md`, `agent-skills/…/product-discovery-orchestration.md`

The workflow directs agents to create `hangar-ai-specs/changes/[discovery-id]/PROPOSAL.md`
but provides no template for its structure. Stages B, C, E, and F all reference specific
artifact names and purposes; Stage A alone has no template.

The `skill-spec-governance` and `ENG-11.2` together define the general PROPOSAL.md contract
(problem, solution, deliverables, success criteria, law citations), but do not provide a
discovery-specific template covering:
- Discovery ID and naming
- Problem statement structured per PRD-2.1
- Scope in/out
- Participating avatars and activation record
- Stakeholder approval block with named approver and role
- BUS-7.1 audit event log table (see Gap 5)

Without this:
- Every team creating a discovery PROPOSAL.md starts from scratch
- ENG-11.2 compliance is inconsistent (proposals may omit required sections)
- Stage A artifact quality is untestable because there is no contract to test against

**Violated Laws:** ENG-11.2 (PROPOSAL.md must include all required sections — but what they
are for Stage A is unspecified), PRD-2.5 (exit gate evidence must be verifiable)

---

### Gap 5 — BUS-7.1 Audit Event Structure Not Scripted for Stage Transitions

**Location:** `workflows/product-discovery-stage-a-f.md` Governance Rules, `agent-skills/…/product-discovery-orchestration.md` §Gate Each Transition

The workflow and orchestration skill both cite BUS-7.1 and state that all stage transitions
"must be logged" — but neither document defines:
- The required fields for a discovery stage-gate audit event (who, what, when, where, why, outcome)
- The format of the audit record (YAML block? Table row in PROPOSAL.md? External system?)
- Where the audit record lives (in PROPOSAL.md, a separate audit.yaml, or an external log?)
- Whether stage A→B, B→C, … F→complete each need their own event record

BUS-7.1 requires audit events to capture: Who / What / When / Where / Why / Outcome.
Without a defined structure, audit events will be inconsistent, incomplete, and unverifiable.

**Violated Laws:** BUS-7.1 (audit trail must have defined structure — NON-NEGOTIABLE),
PRD-2.5 (each stage transition must be logged), ENG-11.1 (evidence artifacts must be verifiable)

---

## Proposed Solution

Five targeted changes to the workflow, skill, and a new templates directory. No existing law
text is changed. All changes are additive enrichment of the `product-discovery-stage-a-f`
workflow surface.

---

### Change 1 — Codify Discovery ID Naming Convention

**Files:** `workflows/product-discovery-stage-a-f.md`, `agent-skills/…/product-discovery-orchestration.md`

Add a **Discovery ID** section to both the workflow Stage A table and the orchestration skill
§Initialize procedure:

```
Format:  disc-{YYYY}-{NNN}
Example: disc-2026-001
Rules:
- YYYY = calendar year the discovery was initiated
- NNN  = zero-padded sequential number, restarting at 001 each year
- No other characters; lowercase only
- Must be globally unique within the organisation's hangar-ai-specs/ inventory
```

The workflow Stage A entry gate description shall be updated to include: *"Assign a Discovery ID
using the `disc-YYYY-NNN` format before creating the spec folder."*

---

### Change 2 — Define Avatar Activation Confirmation Record

**Files:** `workflows/product-discovery-stage-a-f.md` Stage A, `agent-skills/…/product-discovery-orchestration.md` §Initialize Discovery

Add a mandatory **Avatar Activation Record** to the Stage A activities:

1. The orchestration skill §Initialize procedure gains step 1a:
   *"Record avatar activation in PROPOSAL.md under `## Participating Avatars` with: avatar ID,
   load timestamp, constitutional context applied, and confirming agent."*

2. The workflow Stage A exit gate gains the additional condition:
   *"Avatar activation recorded in PROPOSAL.md — avatar IDs, context, and load timestamp present."*

3. The Stage A exit gate in the workflow table is updated from:
   > Problem statement approved; `hangar-ai-specs/changes/[discovery-id]/` scaffolded

   to:
   > Problem statement approved by named approver; `hangar-ai-specs/changes/[disc-id]/` scaffolded;
   > avatars activated and recorded; BUS-7.1 audit event filed

---

### Change 3 — Bind Stakeholder Approval to a Named Actor

**Files:** `workflows/product-discovery-stage-a-f.md` Stage A exit gate, `agent-skills/…/product-discovery-orchestration.md` §Initialize Discovery, Stage A PROPOSAL.md template

Add an **Approval Authority** specification to Stage A:

1. The workflow gains a **Governance** subsection under Stage A:
```
Approval Authority:
  Required role: Product Owner or Discovery Sponsor (Director level or above)
  Capture method: Signed entry in PROPOSAL.md ## Stakeholder Approval block
  Rejection path: Document blocker in PROPOSAL.md; resolve before advancing
  Self-certification: PROHIBITED — approver must be distinct from initiator
```

2. The PROPOSAL.md template (Change 4) gains a `## Stakeholder Approval` block
   with fields: approver name, role, approval date, approval form (in-person/async/PR review),
   and any conditions attached.

---

### Change 4 — Create Stage A PROPOSAL.md Template (D7 / extended by D18)

**Files:** Create `tools/templates/product-discovery/stage-a-proposal.md`

A complete, opinionated template for the Stage A `PROPOSAL.md` covering:
- YAML frontmatter (id, stage, status, created, branch, avatars, laws, workflow, **discovery_mode**, **tier**)
- **Mode Selection block** (Exploratory Discovery vs. Accelerated Discovery) with criteria and
  validation citation fields — required by ensemble deliberation condition (Jin / Q1)
- **Tier Complexity Rubric** (5 questions) — determines Tier 1 (simple, ≤1 service) vs.
  Tier 2 (complex, 3+ services) package; declared at Stage A (Marcus / Q2)
- `## Problem Statement` block structured per PRD-2.1 (exists / matters / solvable / users will pay)
- `## Scope` (in/out table)
- `## Participating Avatars` with activation record fields
- `## Stakeholder Approval` block with named approver, role, date, form, conditions
- `## Initial Findings` (open notes before Stage B)
- `## Exit Gate Checklist` (Stage A → B conditions, including HTML render + browser review)
- `## Audit Log` table for BUS-7.1 events

The orchestration skill §Initialize procedure gains: *"Use `tools/templates/product-discovery/stage-a-proposal.md`
as the starting point for PROPOSAL.md."*

---

### Change 5 — Script BUS-7.1 Audit Event Structure for Stage Transitions (D8 / extended by D15)

**Files:** `workflows/product-discovery-stage-a-f.md` Governance Rules section,
`agent-skills/…/product-discovery-orchestration.md` §Gate Each Transition,
Create `tools/templates/product-discovery/stage-transition-audit-event.yaml`

Add a **Audit Event Specification** for discovery stage transitions:

1. Define the canonical audit event record format (YAML):

```yaml
audit_event:
  discovery_id: disc-YYYY-NNN
  schema_version: "1.1"          # Added by D15
  discovery_mode: exploratory    # exploratory | accelerated — Added by D15
  from_stage: A
  to_stage: B
  timestamp: ISO-8601
  actor:
    name: "<full name>"
    role: "<role/title>"
    system: "GitHub Copilot CLI / manual"
  avatars_active:
    - product
    - business
  evidence_artifact: "hangar-ai-specs/changes/disc-YYYY-NNN/stage-a-evidence.md"
  human_browser_review:          # Added by D15 — Gap 6 requirement
    reviewer_name: "<full name>"
    reviewer_role: "<role>"
    review_timestamp: ISO-8601
    decision: APPROVE | REJECT | ENHANCE
    enhancement_round: 0         # 0 = first review; max 3 per stage
  exit_gate_conditions:
    - condition: "stage evidence artifact rendered as HTML and opened in browser"
      met: true
      evidence: "render-package.sh output"
    - condition: "Human reviewer APPROVED in browser"
      met: true
      evidence: "human_browser_review block above"
  outcome: APPROVED | REJECTED | DEFERRED
  blocker: null
  law_citations:
    - PRD-2.5
    - BUS-7.1
    - ENG-11.1
    - ENG-13.1
```

2. Audit events are stored as rows in the `## Audit Log` table in PROPOSAL.md (inline) AND
   optionally in a separate `audit.yaml` alongside PROPOSAL.md for machine-readable processing.

3. The orchestration skill §Gate Each Transition checklist gains:
   - `[ ] Audit event populated with all BUS-7.1 required fields (who/what/when/where/why/outcome)`
   - `[ ] Audit event filed in PROPOSAL.md §Audit Log before advancing stage`
   - `[ ] Audit event matches structure in tools/templates/product-discovery/stage-transition-audit-event.yaml`

4. The workflow Governance Rules section gains:
   > **Audit Event Contract:** Each stage transition MUST produce an audit event matching
   > the structure defined in `tools/templates/product-discovery/stage-transition-audit-event.yaml`.
   > Partial or unstructured audit notes do not satisfy BUS-7.1. (NON-NEGOTIABLE)

---

### Change 6 — Gap 6: Two-Mode Discovery and Mandatory HTML Evidence Gate (D11–D16)

**Proposed by:** adeel-ali-aa · **Approved by:** ensemble deliberation 2026-04-15

**Files:**
- `workflows/product-discovery-stage-a-f.md` — two-mode Stage A detail, per-stage reviewer role table, updated exit gates A–F
- `agent-skills/…/product-discovery-orchestration.md` — §Gate Each Transition updated, §HTML Render Gate added
- `tools/templates/product-discovery/stage-[b-f]-*.md` — five new per-stage evidence templates (D19–D23)
- `tools/templates/product-discovery/discovery-package-index.md` (D13)
- `tools/templates/product-discovery/render-package.sh` (D16)

#### Two Discovery Modes

Every discovery declares its mode in the Stage A PROPOSAL.md frontmatter:

| Mode | When to use | Stage A Evidence |
|------|-------------|-----------------|
| **Exploratory** | No existing validated problem statement; full PRD-2.1 problem validation from scratch | Full problem validation exercise; all 4 PRD-2.1 dimensions completed from evidence |
| **Accelerated** | Pre-validated problem statement exists (cited by source + date) | Problem statement block cites prior source; agent flags if source was NOT PRD-2.1-validated and recommends dropping to Exploratory mode for Stage A |

Mode selection is self-evidenced by criteria checklist in Stage A PROPOSAL.md template.
Agent actively guides Accelerated mode validation citation and flags non-compliant sources.

#### Mandatory HTML Evidence Gate (ENG-13.1 NON-NEGOTIABLE)

All six stages (A–F) MUST produce a named evidence artifact rendered as HTML via
`aa-artifact-render` before the stage exit gate can pass. This is NON-NEGOTIABLE (ENG-13.1
elevated globally by D17).

Named evidence artifacts follow the convention `stage-[X]-evidence.md` (D11):
- Stage A: `stage-a-evidence.md` (rendered from `stage-a-proposal.md` template, D18)
- Stage B: `stage-b-evidence.md` (rendered from `stage-b-field-study.md` template, D19)
- Stage C: `stage-c-evidence.md` (rendered from `stage-c-code-evidence.md` template, D20)
- Stage D: `stage-d-evidence.md` (rendered from `stage-d-validation.md` template, D21)
- Stage E: `stage-e-evidence.md` (rendered from `stage-e-metrics.md` template, D22)
- Stage F: `stage-f-evidence.md` (rendered from `stage-f-roadmap.md` template, D23)

#### Human Browser Review Gate

Agent workflow per stage transition:
1. Render the stage evidence artifact: `bash tools/templates/product-discovery/render-package.sh [stage]`
2. Open HTML in user's browser (`open` on macOS / `xdg-open` on Linux)
3. Prompt: **APPROVE / REJECT / ENHANCE**
4. **ENHANCE** path: agent produces structured checklist of missing items → actively guides
   remediation → re-renders → re-presents. Maximum 3 enhancement rounds per stage.
   Each round logged as a separate entry in the BUS-7.1 audit event (`enhancement_round: 1/2/3`).
5. Record reviewer name, role, decision, timestamp in `human_browser_review` block of audit event.
6. Stage does NOT advance until decision = APPROVE.

#### Per-Stage Reviewer Role Table (both modes)

| Stage | Exploratory | Accelerated |
|-------|-------------|-------------|
| A | Discovery Sponsor (Director+) | Problem Statement Author + Discovery Sponsor (Director+) |
| B | Product Owner + ≥1 domain expert interviewed | Product Owner + ≥1 domain expert interviewed |
| C | Engineering Lead + Product Owner | Engineering Lead + Product Owner |
| D | Full DVFT stakeholder group | Full DVFT stakeholder group |
| E | Product Owner + Finance/Analytics representative | Product Owner + Finance/Analytics representative |
| F | Executive Sponsor + Product Owner | Executive Sponsor + Product Owner |

#### Discovery Package Structure (Tier 1 / Tier 2)

Declared in Stage A PROPOSAL.md frontmatter via complexity rubric (5 questions):

| Tier | When | Artifacts |
|------|------|-----------|
| **Tier 1** | Simple, ≤1 service | discovery-guide + worksheets 01–03 + forward-roadmap + slice-1-ready-brief |
| **Tier 2** | Complex, 3+ services | Full service-recovery model: all worksheets 01–05 + executive-briefing-deck + discovery-guide + forward-roadmap + slice-1-ready-brief + ado-gap-analysis-brief (optional) + discovery-prompt-guide (optional) |

Reference package (Tier 2):
`/aa-hangar-labs/discovery-packages/service-recovery/complex-disruption-scenarios/`

Package manifest declared at Stage A (required / optional / deferred per artifact).
`tools/templates/product-discovery/discovery-package-index.md` contains both Tier 1 and Tier 2
manifests as templates (D13).

---

## Human Amendments (Ensemble Deliberation 2026-04-15)

### Q4 — ENG-13.1 Global Elevation (D17)

The human reviewer directed ENG-13.1 be elevated **globally** (not domain-scoped).

> D17: Amend `laws/engineering/artifact-rendering.md` — change ENG-13.1 status from RECOMMENDED
> to NON-NEGOTIABLE; remove the 30-day adoption window clause. All workflows (adoption, greenfield,
> legacy rescue, product discovery) are bound immediately upon merge.

This is the highest-priority deliverable per Elena (Constitutional-Judge).

### Q5 — Six Dedicated Per-Stage Evidence Templates (D18–D23)

The human reviewer directed 6 dedicated per-stage evidence templates (NOT a generic template).
Each template includes: stage-specific YAML frontmatter, entry gate checklist, constitutional law
citations for that stage, artifact body sections, exit gate checklist, BUS-7.1 audit event block,
and `aa-artifact-render` invocation command.

| Deliverable | File | Extends |
|-------------|------|---------|
| D18 | `tools/templates/product-discovery/stage-a-proposal.md` | Gap 4 template + mode selection, Tier rubric, per-stage reviewer roles |
| D19 | `tools/templates/product-discovery/stage-b-field-study.md` | `docs/templates/enrichment/02-persona-validation.md` + `04-domain-model-inventory.md` |
| D20 | `tools/templates/product-discovery/stage-c-code-evidence.md` | `docs/templates/enrichment/03-codebase-assessment.md` |
| D21 | `tools/templates/product-discovery/stage-d-validation.md` | New — DVFT matrix + blocker resolution |
| D22 | `tools/templates/product-discovery/stage-e-metrics.md` | `docs/templates/enrichment/01-metrics-collection.md` |
| D23 | `tools/templates/product-discovery/stage-f-roadmap.md` | `docs/templates/enrichment/05-agentic-workflow-discovery.md` + roadmap |

The enrichment worksheets (`docs/templates/enrichment/01–05`) remain the source material for
worksheet artifacts within the discovery package. The stage evidence templates are the gate
artifacts — the constitutional record of stage completion. They are distinct from the worksheets.

---

## Deliverables

| # | Deliverable | File | Type |
|---|---|---|---|
| D1 | Discovery ID naming convention | `workflows/product-discovery-stage-a-f.md` | Workflow amendment |
| D2 | Discovery ID naming convention | `agent-skills/…/product-discovery-orchestration.md` | Skill amendment |
| D3 | Avatar activation record specification | `workflows/product-discovery-stage-a-f.md` | Workflow amendment |
| D4 | Avatar activation record specification | `agent-skills/…/product-discovery-orchestration.md` | Skill amendment |
| D5 | Stakeholder approval authority specification | `workflows/product-discovery-stage-a-f.md` | Workflow amendment |
| D6 | Stakeholder approval authority specification | `agent-skills/…/product-discovery-orchestration.md` | Skill amendment |
| D7 | Stage A PROPOSAL.md template (base — superseded by D18) | `tools/templates/product-discovery/stage-a-proposal.md` | NEW FILE (created in PR) |
| D8 | Stage transition audit event template (base — extended by D15) | `tools/templates/product-discovery/stage-transition-audit-event.yaml` | NEW FILE (created in PR) |
| D9 | Updated Stage A exit gate (workflow table row) | `workflows/product-discovery-stage-a-f.md` | Workflow amendment |
| D10 | Audit event contract in Governance Rules | `workflows/product-discovery-stage-a-f.md` | Workflow amendment |
| D11 | Per-stage evidence artifact naming convention (`stage-[X]-evidence.md`) | `workflows/product-discovery-stage-a-f.md` | Workflow amendment |
| D12 | Updated exit gates A–F (HTML render + human browser review confirmed) | `workflows/product-discovery-stage-a-f.md` | Workflow amendment |
| D13 | Discovery package index (Tier 1 + Tier 2 manifests) | `tools/templates/product-discovery/discovery-package-index.md` | **NEW FILE** |
| D14 | Updated §Gate Each Transition checklist | `agent-skills/…/product-discovery-orchestration.md` | Skill amendment |
| D15 | Stage transition audit event — add `human_browser_review` block, `schema_version`, `discovery_mode` | `tools/templates/product-discovery/stage-transition-audit-event.yaml` | File update |
| D16 | Package render script | `tools/templates/product-discovery/render-package.sh` | **NEW FILE** |
| D17 | ENG-13.1 global elevation to NON-NEGOTIABLE; 30-day adoption window removed | `laws/engineering/artifact-rendering.md` | **LAW AMENDMENT** |
| D18 | Stage A evidence template (mode selection + Tier rubric + reviewer roles) | `tools/templates/product-discovery/stage-a-proposal.md` | File update (extends D7) |
| D19 | Stage B field study evidence template | `tools/templates/product-discovery/stage-b-field-study.md` | **NEW FILE** |
| D20 | Stage C code evidence template | `tools/templates/product-discovery/stage-c-code-evidence.md` | **NEW FILE** |
| D21 | Stage D validation template (DVFT matrix) | `tools/templates/product-discovery/stage-d-validation.md` | **NEW FILE** |
| D22 | Stage E metrics evidence template | `tools/templates/product-discovery/stage-e-metrics.md` | **NEW FILE** |
| D23 | Stage F roadmap evidence template | `tools/templates/product-discovery/stage-f-roadmap.md` | **NEW FILE** |

---

## Success Criteria

| Criterion | Measure | Target |
|---|---|---|
| Discovery ID standard adopted | No discovery PROPOSAL.md in `hangar-ai-specs/` uses an ad-hoc ID format | 100% compliance |
| Avatar activation verifiable | Stage A PROPOSAL.md template includes activation record block | Template exists and is used |
| Approval authority unambiguous | Stage A exit gate specifies required role + capture method | No self-certification possible |
| PROPOSAL.md template complete | Template satisfies all ENG-11.2 required sections + mode selection + Tier rubric | 0 missing sections |
| Audit event structured | `stage-transition-audit-event.yaml` covers all 6 BUS-7.1 fields + schema_version + discovery_mode + human_browser_review | 100% field coverage |
| ENG-13.1 global elevation | `laws/engineering/artifact-rendering.md` marks ENG-13.1 as NON-NEGOTIABLE; 30-day window removed | D17 merged |
| Two modes operative | Stage A PROPOSAL.md template includes mode selection block with Exploratory and Accelerated criteria | Both modes testable |
| HTML gate enforced | All 6 stage exit gates require HTML render + human browser APPROVE before advancing | 0 skipped gates |
| ENHANCE loop bounded | Max 3 enhancement rounds per stage; each round logged as audit entry | Enforced in skill |
| Per-stage templates complete | D18–D23 all exist with stage-specific frontmatter, gate checklists, law citations, BUS-7.1 audit block | 6/6 templates |
| Package structure declared | D13 discovery-package-index.md covers Tier 1 and Tier 2 manifests | Both tiers documented |
| Render script operative | `render-package.sh` renders full discovery package and opens stage artifact in browser on macOS and Linux | Tested end-to-end |
| Workflow lint | `aa-constitution-lint .` passes with no regressions | 0 new failures |
| RAG eval | Workflow routing scores for product-discovery queries do not regress | ≥ baseline pass rate |
| disc-2026-001 retro | Re-running Stage A against disc-2026-001 produces no new workflow gaps | 0 new gaps |

---

## Files To Create / Modify

### Modify (existing files)

| File | Change | Laws |
|------|--------|------|
| `workflows/product-discovery-stage-a-f.md` | D1–D6, D9–D12: ID format, avatar activation, approval authority, updated Stage A–F exit gates, Stage A Detail section, per-stage reviewer role table, audit event contract, evidence naming convention | PRD-2.5, BUS-7.1, ENG-11.1, ENG-13.1 |
| `agent-skills/…/product-discovery-orchestration.md` | D2, D4, D6, D14: §ID Naming Convention, §Avatar Activation Record, §Approval Authority, §HTML Render Gate, updated §Gate Each Transition, updated §Initialize Discovery | PRD-2.5, BUS-7.1, ENG-11.2, ENG-13.1 |
| `laws/engineering/artifact-rendering.md` | D17: ENG-13.1 status → NON-NEGOTIABLE; remove 30-day adoption window | ENG-13.1 |
| `tools/templates/product-discovery/stage-a-proposal.md` | D8/D18: Add mode selection block, Tier complexity rubric, per-stage reviewer role table (Exploratory + Accelerated columns) | ENG-11.2, PRD-2.1, BUS-7.1, ENG-13.1 |
| `tools/templates/product-discovery/stage-transition-audit-event.yaml` | D15: Add schema_version, discovery_mode, human_browser_review block (reviewer_name, reviewer_role, review_timestamp, decision, enhancement_round) | BUS-7.1, PRD-2.5 |

### Create (new files)

| File | Deliverable | Laws |
|------|-------------|------|
| `tools/templates/product-discovery/stage-b-field-study.md` | D19 | PRD-2.3, PRD-2.4, PRD-3.1, PRD-3.2, BUS-7.1, ENG-13.1 |
| `tools/templates/product-discovery/stage-c-code-evidence.md` | D20 | ENG-3.1, ENG-6.7, BUS-7.1, ENG-13.1 |
| `tools/templates/product-discovery/stage-d-validation.md` | D21 | PRD-2.2, PRD-2.1, BUS-7.1, ENG-13.1 |
| `tools/templates/product-discovery/stage-e-metrics.md` | D22 | PRD-6.1, ENG-10.1, BUS-7.1, ENG-13.1 |
| `tools/templates/product-discovery/stage-f-roadmap.md` | D23 | PRD-4.1, PRD-4.2, ENG-11.1, BUS-7.1, ENG-13.1 |
| `tools/templates/product-discovery/discovery-package-index.md` | D13 | ENG-11.1, PRD-2.5 |
| `tools/templates/product-discovery/render-package.sh` | D16 | ENG-13.1, BUS-7.1 |

---

## What Is Out of Scope

- Changes to laws other than ENG-13.1 (D17 is the sole law text amendment in this proposal)
- Product discovery content changes unrelated to workflow mechanics (e.g. adding new market
  research techniques to Stage B)
- `product-discovery-stage-a-f.md` full enrichment to `adoption.md`-level richness — this
  proposal targets the six structural gaps; full prompt enrichment is a separate proposal
- Migration of pre-existing discovery packages to the new Tier structure (teams opt in)

---

## Constitutional Compliance

| Law | How Satisfied |
|-----|--------------|
| ENG-11.1 ⛔ NON-NEG | This document is the SDD PROPOSAL artifact; `tasks.md` governs implementation; archive on completion |
| ENG-11.2 | PROPOSAL includes: Problem, Solution, Deliverables, Success Criteria, Law Citations — all sections present |
| PRD-2.5 ⛔ NON-NEG | Proposal directly addresses the operationalisability of PRD-2.5's NON-NEGOTIABLE stage gates |
| PRD-2.1 | Problem validated with evidence from disc-2026-001 test run before solution design |
| BUS-7.1 ⛔ NON-NEG | Proposal directly addresses the structural gap preventing BUS-7.1 compliance in Stage A transitions; audit event schema extended with human_browser_review |
| ENG-13.1 | D17 elevates ENG-13.1 globally to NON-NEGOTIABLE; all 23 deliverables are compliant with this elevation |
| ENG-4.1 | All workflow and template changes authored with RED→GREEN→REFACTOR on lint/RAG gates per tasks.md |
| ENG-1.2 | Human browser review gate operationalises ENG-1.2 AI-Engineer Pairing Law at every stage transition |

---

## Evidence Source

All gaps documented in:
- `gate-mgmt/hangar-ai-specs/artifacts/stage-a-initialize.html` — §Workflow Validation section
- `gate-mgmt/hangar-ai-specs/changes/disc-2026-001/PROPOSAL.md` — §Workflow Gaps Identified
- Discovery: `disc-2026-001` · Branch: `product-discovery` · Repo: `gate-mgmt`
- Ensemble Deliberation: `ensemble-pr31-gap6-2026-04-15` · Approved: 2026-04-15
