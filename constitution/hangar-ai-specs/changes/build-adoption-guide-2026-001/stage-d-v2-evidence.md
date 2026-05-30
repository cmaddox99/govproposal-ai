# Stage D v2 — Amendment: Architect/Engineer Paths + Workflow Hub + Phase Gate Evidence
**Changeset:** `build-adoption-guide-2026-001`
**Amendment type:** PRD-2.5 ⛔ post-clearance amendment — new PO direction constitutes new evidence
**Author:** Adeel Ali — AI & Technical Coach, American Airlines Hangar
**Status:** v1.1 — 2026-05-07 — ✅ JURY-CLEARED 6/6 APPROVE (2 rounds). SC-OBL-2 WAIVED — Architect path UNBLOCKED. DC-08 through DC-12 binding on all workflow pages. IMPLEMENT may proceed: P3-SA, P3-ENG, P7, P8, P9-adopt, P9-lr, P9-gf, P9-av.
**Parent:** stage-d-evidence.md v1.2 (JURY-CLEARED 2026-05-06) — this document extends, does not replace
**Gate:** Stage D v1 — ✅ CLEARED | Stage D v2 — JURY PENDING

---

## §1 Amendment Trigger — New PO Direction (PRD-2.5 ⛔)

**Evidence type:** Product Owner strategic direction (PRD-2.5 ⛔ — new directional evidence from PO supersedes LATER/NEXT deferral).

**Direction received 2026-05-07 from Adeel Ali (PO + AA Tech Coach + Architect):**
> "Continue to build for architects and engineers. I want a lot of emphasis on the workflows and how, when to use them and how to tackle their non-deterministic nature to their advantage. Coaches, architects and engineers should be able to work with the workflows including agentic discovery, adoption, avatar, legacy rescue and greenfield development. They are the main interface. We need prompt-level guidance for them to execute all the workflows with GitHub Copilot. They should be able to understand the phase gate evidence artifacts, what they can have, how to interpret the information and be able to monitor, provide essential decisions, detect drift."

**Why this is PRD-2.5 ⛔ valid evidence:** PO has firsthand experience of all 5 workflows (14+ adoption runs across the AA Hangar programme). This is direct domain expertise from the product owner, not assumption. The direction reframes the guide's primary interface from *quick-start hub* to *workflow command centre*.

---

## §2 SC-OBL-2 Waiver — Architect Path Unblocking

**Original blocker:** SD-OBL-1 — Architect path blocked until SC-OBL-2 (≥2 architect/engineer interviews).

**Waiver justification:**
1. **PO direct expertise:** Adeel Ali is both a Technical Coach and a practising Solution Architect at AA Hangar. His firsthand architect perspective on adoption friction is equivalent to a structured interview. Evidence on file: session author identity + 2026-05-07 direction statement above.
2. **Stage B proxy evidence:** All 4 Stage B interviewees (Turpin, Fraser, Sutherland, Robinson) have conducted architect-level adoption sessions (C++, data science stacks, multi-repo). Architect concerns (adoption scope, SonarQube gate, law override) are documented in `stage-b-evidence.md §3`.
3. **Jury ratification required:** This waiver must be jury-approved by Tomás Reyes (Sr. Architect juror) and Alexandra Pierce before Architect path IMPLEMENT begins.

**SC-OBL-2 disposition:** WAIVED with PO justification — Architect path UNBLOCKED upon jury APPROVE of this document.

---

## §3 New Design Constraints DC-08 through DC-12

These constraints are BINDING on all workflow and evidence pages. DC-01–DC-07 remain binding on P3 and P1.

| ID | Constraint | Binding on |
|----|-----------|-----------|
| **DC-08** | Every workflow page MUST include a visible **"When to Use This Workflow"** decision section showing which persona uses it, what triggers it, and what precedes/follows it in the workflow chain | All workflow deep-dive pages |
| **DC-09** | Every workflow page MUST include a **per-phase prompt library** with copyable GitHub Copilot prompts for each phase. Each prompt must: (a) be usable as-is or scoped down — no abstract guidance without a concrete prompt; (b) be compatible with the GitHub Copilot CLI `gh copilot ask` command and GitHub Copilot IDE chat; (c) reference the correct workflow trigger phrase from the constitution workflow YAML front-matter | All workflow deep-dive pages |
| **DC-10** | Every workflow page MUST include a **Phase Gate Evidence** section showing: (a) what artifact is produced at each gate, (b) what the human reads in that artifact, (c) what decision the human makes, (d) signals of drift or AI misalignment | All workflow deep-dive pages + Phase Gate Evidence Guide |
| **DC-11** | **Non-determinism callout** MUST appear visible-by-default (not collapsed) on every workflow page, adjacent to or integrated within DC-08. Same visual treatment as DC-07 human agency section on P3. Content: same prompt ≠ same output; scope control; iteration is expected | All workflow deep-dive pages |
| **DC-12** | **Persona routing** — every workflow and evidence page MUST show a clear "Who uses this" indicator (Technical Coach / Senior Architect / Engineer) as a visible label. If a workflow applies to all 3, all 3 must be shown | All workflow pages |

---

## §4 Updated Information Architecture

### §4.1 Revised Page Structure

| Page | Name | Persona(s) | New/Updated | Status |
|------|------|-----------|-------------|--------|
| P1 | Landing Hub | All | Existing — add Architect/Engineer cards as active | ✅ Built, needs card activation |
| P2 | Constitutional AI Model Viz | Architect | Existing | ✅ Built |
| P3-TC | Technical Coach Quick Start | Coach | Existing | ✅ Built |
| P3-SA | Architect Quick Start | Architect | **NEW** — SC-OBL-2 WAIVED | ⏳ PENDING |
| P3-ENG | Engineer Quick Start | Engineer | **NEW** | ⏳ PENDING |
| P7 | Workflows Hub | All | **NEW** — replaces SDD Workflow Guide concept; primary workflow interface | ⏳ PENDING |
| P8 | Phase Gate Evidence Guide | All | **NEW** — replaces Compliance Checklist concept; artifact reading + decision-making + drift detection | ⏳ PENDING |
| P9-adopt | Adoption Workflow Deep-Dive | All | **NEW** — phases, prompts, evidence, non-determinism (DC-08 through DC-12) | ⏳ PENDING |
| P9-lr | Legacy Rescue Workflow Deep-Dive | All | **NEW** | ⏳ PENDING |
| P9-gf | Greenfield Workflow Deep-Dive | All | **NEW** | ⏳ PENDING |
| P9-av | Avatar + Product Discovery Workflow | All | **NEW** | ⏳ PENDING |
| P4 | Laws Reference | Engineer, Architect | Existing plan — unchanged | DEFERRED |
| P5 | Skills Catalog | Engineer, Coach | Existing plan — unchanged | DEFERRED |
| P6 | Avatar Selection Wizard | All | Existing plan — unchanged (partially covered by P9-av) | DEFERRED |
| P10 | Amendment Process | All | Existing plan — unchanged | DEFERRED |

### §4.2 Navigation Model

```
P1 (Landing Hub — persona selector)
├── Coach      → P3-TC (Coach Quick Start) → P7 (Workflows Hub) → P9-adopt / P9-lr / P9-gf / P9-av
├── Architect  → P3-SA (Architect Quick Start) → P7 → P8 (Phase Gate Evidence)
├── Engineer   → P3-ENG (Engineer Quick Start) → P7 → P9-adopt → P8
└── All        → P7 (Workflows Hub) — primary workflow command centre
                 └── Per-workflow: DC-08 trigger | DC-09 prompts | DC-10 phase gates | DC-11 non-determinism
```

---

## §5 Page Wireframes

### §5.1 P3-SA — Architect Quick Start

```
┌──────────────────────────────────────────────────────────┐
│  ← Adoption Guide | P3 — Senior Architect Quick Start    │
│  AA Navy header                                           │
├──────────────────────────────────────────────────────────┤
│  ACCOMPLISH BAR: "Evaluate constitutional fit, govern     │
│  architecture decisions, review phase gate evidence"      │
├──────────────────────────────────────────────────────────┤
│  ⚡ QUICK START PATH (DC-04 visual treatment)             │
│  3 steps: (1) Run architecture scan prompt               │
│           (2) Review AI model viz (P2 link)               │
│           (3) Open Workflow Hub for your next workflow     │
│  [Copy Architecture Scan Prompt] button                   │
├──────────────────────────────────────────────────────────┤
│  🧭 HUMAN AGENCY (DC-07 — visible, same as P3-TC)        │
│  Architect-specific framing: you decide scope and         │
│  batch size; agent proposes; you govern                   │
├──────────────────────────────────────────────────────────┤
│  📐 ARCHITECTURE REVIEW CHECKLIST (DC-01 direct steps)   │
│  Expandable step cards:                                   │
│  1. Understand the law precedence hierarchy               │
│     → prompt: ask agent to summarise applicable laws      │
│  2. Map your bounded context to the constitution          │
│     → prompt: DDD bounded context scan                    │
│  3. Review the phase gate artifact for your workflow      │
│     → link to P8 Phase Gate Evidence Guide                │
│  4. Handle law conflicts / propose amendments             │
│     → link to P10 Amendment Process                       │
├──────────────────────────────────────────────────────────┤
│  🔗 WORKFLOWS + EVIDENCE (visible links)                  │
│  → Workflows Hub (P7) — all 5 workflows                   │
│  → Phase Gate Evidence Guide (P8) — read any artifact     │
├──────────────────────────────────────────────────────────┤
│  ▼ Coaching Notes for Senior Architects (DC-06 collapsed) │
│  Socratic prompts for architect-level reflection           │
├──────────────────────────────────────────────────────────┤
│  FOOTER: v2.0.0 · DC-01 through DC-07 · ENG-13.1 ⛔      │
└──────────────────────────────────────────────────────────┘
```

### §5.2 P3-ENG — Engineer Quick Start

```
┌──────────────────────────────────────────────────────────┐
│  ← Adoption Guide | P3 — Engineer Quick Start             │
├──────────────────────────────────────────────────────────┤
│  ACCOMPLISH BAR: "Run your first governed task using      │
│  the PROPOSE → IMPLEMENT → ARCHIVE cycle"                 │
├──────────────────────────────────────────────────────────┤
│  ⚡ FIRST GOVERNED TASK (DC-04 visual treatment)          │
│  4 steps: (1) Adopt the constitution (link to P9-adopt)   │
│           (2) Pick your workflow (link to P7)             │
│           (3) Run the PROPOSE prompt                      │
│           (4) Review, approve, and IMPLEMENT              │
│  [Copy First Task Prompt] button                          │
├──────────────────────────────────────────────────────────┤
│  🤖 WHAT IS THE AGENT DOING? (DC-03)                      │
│  PROPOSE → wait for your review → IMPLEMENT → ARCHIVE     │
│  Engineer-specific: you write tests; agent writes code;   │
│  you review; TDD gate must pass before archive            │
├──────────────────────────────────────────────────────────┤
│  🧭 HUMAN AGENCY (DC-07 — visible)                        │
│  Engineer framing: scope your ticket to one class;        │
│  reject over-large proposals; run mutations               │
├──────────────────────────────────────────────────────────┤
│  📋 FULL ENGINEER WORKFLOW (DC-01 direct steps)           │
│  Step cards: adopt → propose → TDD gate → implement →    │
│  mutation test → sonarqube gate → archive → PR            │
├──────────────────────────────────────────────────────────┤
│  🔗 WORKFLOWS FOR ENGINEERS (link to P7)                  │
│  → Legacy Rescue · Greenfield · Adoption                  │
├──────────────────────────────────────────────────────────┤
│  ▼ Coaching Notes for Engineers (DC-06 collapsed)         │
└──────────────────────────────────────────────────────────┘
```

### §5.3 P7 — Workflows Hub

```
┌──────────────────────────────────────────────────────────┐
│  ← Adoption Guide | 🔀 Workflows Hub                     │
├──────────────────────────────────────────────────────────┤
│  "Workflows are the main interface to the constitution.   │
│  Choose the right workflow for your situation."           │
├──────────────────────────────────────────────────────────┤
│  🧭 NON-DETERMINISM REMINDER (DC-11 — visible)            │
│  Same workflow, different result each time — by design.   │
│  You review at every gate. This is the feature.           │
├──────────────────────────────────────────────────────────┤
│  DECISION TREE: Which workflow do I need?                  │
│  Q1: Is the repo adopted? No → Adoption first             │
│  Q2: New project? → Greenfield                            │
│  Q3: Existing code to improve? → Legacy Rescue            │
│  Q4: New product idea? → Product Discovery + Avatar       │
│  Q5: Need to set AI context for your tech stack? → Avatar │
├──────────────────────────────────────────────────────────┤
│  WORKFLOW CARDS (5 cards, all personas visible):          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │
│  │ ADOPTION    │ │LEGACY RESCUE│ │ GREENFIELD  │        │
│  │ All personas│ │ All personas│ │ All personas│        │
│  │ Phase 1–3   │ │ Phase 1–7   │ │ Phase 1–8   │        │
│  │ [Open →]    │ │ [Open →]    │ │ [Open →]    │        │
│  └─────────────┘ └─────────────┘ └─────────────┘        │
│  ┌─────────────┐ ┌─────────────────────────────┐        │
│  │   AVATAR    │ │   PRODUCT DISCOVERY         │        │
│  │ All personas│ │   (Agentic Discovery)        │        │
│  │ 1 session   │ │   Stage A–F                 │        │
│  │ [Open →]    │ │   [Open →]                  │        │
│  └─────────────┘ └─────────────────────────────┘        │
├──────────────────────────────────────────────────────────┤
│  🔗 Phase Gate Evidence Guide (P8) — "How to read any    │
│  workflow artifact and make the right decision"           │
└──────────────────────────────────────────────────────────┘
```

### §5.4 P8 — Phase Gate Evidence Guide

```
┌──────────────────────────────────────────────────────────┐
│  ← Workflows Hub | 📊 Phase Gate Evidence Guide          │
│  "Every constitutional workflow produces evidence.        │
│  Here's how to read it."                                  │
├──────────────────────────────────────────────────────────┤
│  WHO USES THIS: Coach ✅ Architect ✅ Engineer ✅          │
├──────────────────────────────────────────────────────────┤
│  §1 WHAT IS A PHASE GATE ARTIFACT?                        │
│  HTML file in hangar-ai-specs/changes/[spec-id]/          │
│  Contains: evidence produced, decisions made, status      │
│  ┌──────────────────────────────────────────────────┐    │
│  │ Anatomy of a phase artifact:                     │    │
│  │ • Header: workflow ID, phase number, status      │    │
│  │ • Evidence table: what was found                 │    │
│  │ • Decision row: what the human approved/objected │    │
│  │ • Gate status: PASS / FAIL / PENDING             │    │
│  │ • Commit hash: links to code change              │    │
│  └──────────────────────────────────────────────────┘    │
├──────────────────────────────────────────────────────────┤
│  §2 DECISIONS AT EACH GATE (expandable cards per gate)   │
│  Gate: PROPOSE — "Does this proposal match your intent?"  │
│  Gate: IMPLEMENT — "Did the agent execute correctly?"     │
│  Gate: ARCHIVE — "Is the governed trail complete?"        │
│  Gate: SONARQUBE — "No new debt introduced?"             │
│  Gate: MUTATION — "Are tests meaningful?"                 │
├──────────────────────────────────────────────────────────┤
│  §3 DETECTING DRIFT (visible callout box)                 │
│  Signs the AI has drifted from the constitution:          │
│  • Proposal cites no law IDs                              │
│  • Proposal scope grew between sessions                   │
│  • Archive step skipped                                   │
│  • SonarQube gate was not consulted                       │
│  What to do: OBJECT at the gate, ask for re-proposal      │
├──────────────────────────────────────────────────────────┤
│  §4 MONITORING ACROSS SESSIONS (for coaches + architects) │
│  Check: hangar-ai-specs/changes/ for open proposals       │
│  Check: hangar-ai-specs/archive/ for closed proposals     │
│  Check: PROGRESS.md for overall workflow health           │
│  Prompt: "Summarise all open proposals in this repo"      │
├──────────────────────────────────────────────────────────┤
│  §5 QUICK REFERENCE PROMPTS (DC-09 — copyable)           │
│  [Copy "Summarise open proposals"] button                  │
│  [Copy "Review this phase artifact for drift"] button     │
│  [Copy "Re-propose with reduced scope"] button            │
└──────────────────────────────────────────────────────────┘
```

### §5.5 P9-adopt — Adoption Workflow Deep-Dive

```
┌──────────────────────────────────────────────────────────┐
│  ← Workflows Hub | 🏛️ Adoption Workflow                  │
├──────────────────────────────────────────────────────────┤
│  DC-08: WHEN TO USE THIS WORKFLOW                         │
│  Use when: new repo, stale AGENTS.md, missing avatar      │
│  Precedes: Legacy Rescue, Greenfield, Discovery           │
│  Personas: Coach ✅ Architect ✅ Engineer ✅              │
│  DC-11: Non-determinism callout                           │
├──────────────────────────────────────────────────────────┤
│  PHASE TABLE: Phase 1 Check → Phase 2 Adopt →            │
│  Phase 2b Provision Gate → Phase 3 Verify                │
│  (expandable cards, 1 per phase)                          │
│  Each card: what agent does | what human does | gate     │
├──────────────────────────────────────────────────────────┤
│  DC-09: PROMPT LIBRARY (3 phases × 1 prompt each)        │
│  Phase 1: Check adoption state prompt                     │
│  Phase 2: Full adoption prompt (= P3-TC sprint prompt)    │
│  Phase 2b: Provision SonarQube gate prompt                │
│  Phase 3: Verify adoption prompt                          │
│  All copyable                                             │
├──────────────────────────────────────────────────────────┤
│  DC-10: PHASE GATE EVIDENCE                               │
│  adoption-check.md → what to look for → decision         │
│  adoption-verified.md → what to look for → decision       │
│  Drift signals: agent proposes avatar creation when       │
│  team said "setup only" → OBJECT and scope down           │
├──────────────────────────────────────────────────────────┤
│  🧭 COMPOSITIONAL ADOPTION (DC-07 link)                   │
│  You can stop at any phase and commit.                    │
│  Each phase outcome is a valid constitutional result.     │
└──────────────────────────────────────────────────────────┘
```

### §5.6 P9-lr — Legacy Rescue Workflow Deep-Dive

```
┌──────────────────────────────────────────────────────────┐
│  ← Workflows Hub | 🔧 Legacy Rescue Workflow             │
├──────────────────────────────────────────────────────────┤
│  DC-08: WHEN TO USE + DECISION TRACK                      │
│  "Refactor or Rewrite?" decision tree:                    │
│  Score low + high test coverage → Refactor Track          │
│  Score very low + no tests → Rewrite Track               │
│  Personas: Coach ✅ Architect ✅ Engineer ✅              │
│  DC-11: Non-determinism callout                           │
├──────────────────────────────────────────────────────────┤
│  PHASE TABLE (Refactor Track, 7 phases):                  │
│  1.Characterization → 2.Scan → 3.Tests → 4.Mutation →   │
│  5.Refactor → 6.Certify → 7.PR                           │
│  (expandable cards, 1 per phase)                          │
│  Each card: agent action | human decision | artifact name │
├──────────────────────────────────────────────────────────┤
│  DC-09: PROMPT LIBRARY                                    │
│  Phase 1: Characterization test prompt                    │
│  Phase 2: SonarQube scan + legacy rescue scan prompt      │
│  Phase 3: TDD / characterization test writing prompt      │
│  Phase 4: Mutation test run prompt                        │
│  Phase 5: Refactor with Feathers process prompt           │
│  Phase 6: Certification prompt                            │
│  All copyable                                             │
├──────────────────────────────────────────────────────────┤
│  DC-10: PHASE GATE EVIDENCE                               │
│  phase-N.html anatomy: what each section means           │
│  Decision at each gate: approve / scope down / re-propose │
│  Drift signals: mutation score dropped | scope grew |     │
│  tests not updated | characterization tests missing       │
├──────────────────────────────────────────────────────────┤
│  BOUNDED CONTEXT TIP (DC-07 link)                         │
│  Scope to com.aa.loyalty.mileage — not the whole app      │
└──────────────────────────────────────────────────────────┘
```

### §5.7 P9-gf — Greenfield Workflow Deep-Dive

```
┌──────────────────────────────────────────────────────────┐
│  ← Workflows Hub | 🌱 Greenfield Development             │
├──────────────────────────────────────────────────────────┤
│  DC-08: WHEN TO USE                                       │
│  Use for net-new services, APIs, modules from scratch     │
│  Precedes nothing; preceded by adoption                   │
│  Personas: Coach ✅ Architect ✅ Engineer ✅              │
│  DC-11: Non-determinism callout                           │
├──────────────────────────────────────────────────────────┤
│  PHASE TABLE (8 phases):                                  │
│  1.Domain → 2.Spec → 3.Slice → 4.TDD → 5.API →          │
│  6.Security → 7.Mutation → 8.PR                           │
│  (expandable cards)                                        │
├──────────────────────────────────────────────────────────┤
│  DC-09: PROMPT LIBRARY                                    │
│  1 prompt per phase, all copyable                         │
├──────────────────────────────────────────────────────────┤
│  DC-10: PHASE GATE EVIDENCE                               │
│  Per-phase artifact: what it contains | decision criteria │
│  Drift signals: vertical slice grew beyond one endpoint;  │
│  tests not written before implementation                  │
└──────────────────────────────────────────────────────────┘
```

### §5.8 P9-av — Avatar + Product Discovery Workflow

```
┌──────────────────────────────────────────────────────────┐
│  ← Workflows Hub | 🤖 Avatar + Product Discovery         │
├──────────────────────────────────────────────────────────┤
│  TWO RELATED WORKFLOWS EXPLAINED                          │
│  Avatar: sets the AI's domain context for your stack      │
│  Product Discovery: finds what to build (Stage A-F)       │
│  When to use which — decision section                     │
│  DC-11: Non-determinism callout                           │
├──────────────────────────────────────────────────────────┤
│  AVATAR CREATION (from avatar-workflow.md)                │
│  When: first adoption, or after tech stack change         │
│  Phases: analyse context → generate avatar → validate    │
│  DC-09: prompts for each phase                            │
│  DC-10: evidence artifact (avatar-validation.md)          │
├──────────────────────────────────────────────────────────┤
│  PRODUCT DISCOVERY / AGENTIC DISCOVERY (Stage A-F)        │
│  Stage A: Problem framing                                  │
│  Stage B: Assumption mapping + interviews                 │
│  Stage C: JTBD analysis                                   │
│  Stage D: IA design                                       │
│  Stage E: Validation                                      │
│  Stage F: Go/No-Go                                        │
│  DC-09: key prompt for each stage                         │
│  DC-10: stage evidence artifacts (what they contain)      │
└──────────────────────────────────────────────────────────┘
```

---

## §6 Page Contracts (DC-08 through DC-12 compliance)

| Page | DC-08 ✓ | DC-09 ✓ | DC-10 ✓ | DC-11 ✓ | DC-12 ✓ | ENG-13.1 ✓ |
|------|---------|---------|---------|---------|---------|-----------|
| P3-SA | N/A | ✅ arch scan + 4 step prompts | N/A | ✅ visible | ✅ Architect | ✅ zero deps |
| P3-ENG | N/A | ✅ first task + workflow prompts | N/A | ✅ visible | ✅ Engineer | ✅ zero deps |
| P7 (Workflows Hub) | ✅ decision tree | N/A (links to P9) | N/A (links to P8) | ✅ visible | ✅ All 3 | ✅ zero deps |
| P8 (Phase Gate Evidence) | N/A | ✅ 3 monitoring prompts | ✅ all gate types | ✅ visible | ✅ All 3 | ✅ zero deps |
| P9-adopt | ✅ triggers table | ✅ 4 prompts | ✅ 2 artifact types | ✅ visible | ✅ All 3 | ✅ zero deps |
| P9-lr | ✅ decision track | ✅ 6 prompts | ✅ phase-N.html anatomy | ✅ visible | ✅ All 3 | ✅ zero deps |
| P9-gf | ✅ triggers | ✅ 8 prompts | ✅ per-phase artifacts | ✅ visible | ✅ All 3 | ✅ zero deps |
| P9-av | ✅ decision (avatar vs discovery) | ✅ avatar + A-F prompts | ✅ avatar-validation + stage evidence | ✅ visible | ✅ All 3 | ✅ zero deps |

---

## §7 User Stories — New (US-TC-07 through US-TC-13)

| ID | As a… | I want to… | So that… | Acceptance Criteria |
|----|-------|-----------|---------|---------------------|
| **US-TC-07** | Architect | See my persona-specific quick start with architecture scan prompts | I can assess constitutional fit for my project in one session | P3-SA loads; architecture scan prompt is copyable; DC-07 visible; link to P2 and P8 present |
| **US-TC-08** | Engineer | See my persona-specific quick start with first governed task prompts | I can run PROPOSE→IMPLEMENT→ARCHIVE on my first ticket without coaching | P3-ENG loads; first task prompt copyable; TDD gate explained; DC-03 and DC-07 visible |
| **US-TC-09** | Any persona | Navigate to the right workflow for my situation using a decision tree | I don't have to guess which workflow to run | P7 loads; decision tree renders; all 5 workflow cards link to P9-* pages; decision tree reaches a unique workflow within 3 questions |
| **US-TC-10** | Any persona | Copy a ready-to-run GitHub Copilot prompt for every phase of every workflow | I can run the workflow without consulting external docs | Each P9-* page has ≥1 copyable prompt per workflow phase; prompts work in GitHub Copilot CLI and IDE chat |
| **US-TC-11** | Architect / Coach | Read a phase gate artifact and know exactly what decision to make | I can govern a workflow in progress without facilitator guidance | P8 has a gate decision section covering PROPOSE/IMPLEMENT/ARCHIVE/SONARQUBE/MUTATION gates; each gate has a named decision action |
| **US-TC-12** | Any persona | Identify signs of AI drift in a workflow artifact | I can detect when the agent has moved off-constitution and course-correct | P8 has a drift detection section listing ≥4 concrete drift signals and a correction action (OBJECT + re-propose) |
| **US-TC-13** | Any persona | Understand which workflow follows which and when adoption is required first | I can sequence multiple workflows in the right order | P7 workflow cards show preceded_by and followed_by links; adoption prerequisite is prominently noted |

---

## §8 Law Citation Crosswalk (amendment additions)

| Law ID | Application |
|--------|-------------|
| `ENG-11.1` | ⛔ — all new pages must be evolvable; section-based HTML per existing constraint |
| `ENG-13.1` | ⛔ — all new pages self-contained, zero external deps |
| `ENG-4.1` | ⛔ — P3-SA and P3-ENG TDD stubs required for any JS before IMPLEMENT |
| `PRD-2.5` | ⛔ — this amendment is valid under PRD-2.5 (new PO directional evidence) |
| `PRD-3.3` | US-TC-07 through US-TC-13 per PRD-3.3 user story law |
| `ENG-1.2` | ⛔ — workflow prompts must reference the correct workflow trigger phrases from constitution |
| `BUS-1.1` | ⛔ — new pages must maintain accessibility (WCAG 2.1 AA) — apply R-14/R-15 pattern from the start |
| `ENG-10.1` | ⛔ — all law IDs cited in workflow pages must be verified against laws/index.yaml |

---

## §9 Stage D v2 Jury Pre-Requisites

Before this document can enter jury:
- [x] Stage D v1 jury-cleared (2026-05-06)
- [x] IMPLEMENT complete (P1/P3/prompt-templates, commit `9c8b430`)
- [x] SD-OBL-4 cleared (commit `2ae750a`)
- [x] Stage E jury-cleared (commit `fd2e345`)
- [x] R-14/R-15 resolved (commit `7a1eb99`)
