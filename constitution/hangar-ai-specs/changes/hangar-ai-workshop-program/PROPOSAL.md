# Proposal: Hangar AI Constitution Workshop Program

**Proposal ID:** hangar-ai-workshop-program  
**Submitted:** March 22, 2026  
**Last Updated:** March 22, 2026  
**Status:** DRAFT — Pending Review  
**Execution Order:** Phase 2 of 2 (execute after `constitution-workflow-governance-evolution`)  
**Dependency:** `constitution-workflow-governance-evolution` must be complete before implementation (Session 1 references greenfield workflow; Session 2 references legacy rescue workflows)

---

## Problem

The AA Hangar AI Constitution has robust laws, skills, workshops, and real-world examples — but no comprehensive instructor-led training program to bring engineers and product managers up to speed. Four specific gaps:

**1. The existing workshops are not structured as a teachable curriculum.**  
The Agentic SDLC Workshop (`WORKSHOP-GUIDE.md`) and Constitution Adoption Test are self-directed lab environments, not a sequenced two-session program. There is no arc that takes someone from *"What is this?"* through *"I can apply this to my own codebase today."*

**2. Engineers consistently report confusion on the same topics:**  
- What good tests actually look like — and how to identify bad ones  
- What good code structure looks like — clean vs. complex, with real before/after examples  
- How governance works in practice — laws as lived experience, not just written rules

**3. There is no visual learning layer.**  
People learn through diagrams — activity flows, user journeys, before/after comparisons. Participants have specifically requested visual explanations of the what/why/how behind TDD, code structure, constitution compliance, and the governed workflows.

**4. The Agentic SDLC Workshop carries stale infrastructure.**  
The pre-built Weather Dashboard (`backend/`, `frontend/`) and the Fast Track exist as a demo path that is no longer used. These add noise and confusion. The Hangar SDD is listed as a prerequisite — it must be replaced with the tool-independent `hangar-ai-specs/` approach from `constitution-workflow-governance-evolution`.

---

## Solution

Design, build, and deliver a two-session workshop program (2 × 3 hours) that teaches the constitution through doing, not through lecture. Academic concepts are introduced *in context* as participants encounter them during the lab — not front-loaded.

**Session 1 — Agentic SDLC: Self-Service Track (Greenfield)**  
Participants build a domain-rich application of their choice, step by step, following the Greenfield workflow. Constitution laws are surfaced at the moment they become relevant.

**Session 2 — Legacy Adoption: Characterization Tests & Rescue**  
Participants deep-dive into a brownfield codebase, surface architectural and code quality violations with law citations, and produce a characterization test proposal that kicks off rescue work on a real codebase — theirs or the provided `loyalty-service-legacy`.

The program:
- Uses and enhances **existing workshop material** (Agentic SDLC Workshop Step-by-Step track, Adoption Test Workshop)
- **Strips the Weather Dashboard** and Fast Track from the Agentic SDLC Workshop — no longer needed
- **Removes the Hangar SDD prerequisite** — replaced with `hangar-ai-specs/` (tool-independent)
- References the **new workflows** from `constitution-workflow-governance-evolution`
- **Produces PDF artifacts** using the same HTML/CSS toolchain as discovery and adoption packages, with the AA visual theme
- **Stores all material** in `docs/workshops/` inside the Hangar AI Constitution

---

## Class Description

**Course:** *Hangar AI Constitution: Governance, Testing, and Agentic Workflows in Practice*  
**Audience:** Software engineers, technical leads, and product managers adopting the Hangar AI Constitution  
**Format:** 2 sessions × 3 hours each; ~25% contextual teaching, ~75% hands-on practice  
**Pedagogy:** Learning by doing — constitutional concepts surface as participants encounter them, not as upfront lectures  
**Prerequisites:** Familiarity with at least one language (Python or Java); no prior constitution knowledge required

### Session 1 — Agentic SDLC: Self-Service Track (3 hours)
*Build a domain-rich application from scratch under constitutional governance. Every phase introduces the relevant laws and skills exactly when you need them.*

### Session 2 — Legacy Adoption: Characterization Tests & Rescue (3 hours)
*Go deep on a brownfield codebase — identify architectural, security, and code quality violations, understand why they matter (with law citations), and produce the characterization test proposal that starts the rescue.*

---

## What Will Be Delivered

---

### Phase 1: Session 1 — Agentic SDLC Self-Service Track

Session 1 IS the Agentic SDLC Workshop Step-by-Step track, redesigned as a facilitated class experience with contextual teaching woven in at each phase. Each phase opens with a brief "Why this matters" frame (2–3 min) before participants do the work.

#### Overview

Participants pick a domain they care about (aviation operations, loyalty, a personal project, anything) and build a real, tested, constitutionally-governed vertical slice from scratch in 3 hours. By the end they have working code, a characterization of the Greenfield workflow, and muscle memory for the TDD cycle.

#### Phase-by-Phase Flow

**Phase 1: Constitution Adoption** *(20 min)*  
*What participants do:* Clone the constitution, walk through the law/skill/avatar structure, create `AGENTS.md`, scaffold `hangar-ai-specs/changes/[their-project]/`, run the constitution linter.  
*Laws introduced contextually:* `ENG-1.2` (AI as teaching partner, not code generator) — *introduced when they see the AGENTS.md for the first time*; `ENG-11.1` (Hangar SDD Law) — *introduced when they scaffold `hangar-ai-specs/`*  
*Visual:* `diagram-01-constitution-overview.svg` — Laws → Skills → Avatars → Workflows, displayed as a reference card throughout the session

**Phase 2: Avatar Selection** *(15 min)*  
*What participants do:* Pick a product avatar (their domain) and a technology avatar (their stack). Read the avatar manifest to see which laws activate.  
*Laws introduced contextually:* `PRD-2.1` (Problem Validation) — *introduced when they frame their domain problem*; `ENG-1.1` (Priority Hierarchy) — *introduced when they scan the avatar's law specializations*

**Phase 3: Specification Generation** *(25 min)*  
*What participants do:* Use the constitution agent to generate a `PROPOSAL.md`, `design.md`, BDD specifications, and a vertical-slice `tasks.md` for their domain.  
*Laws introduced contextually:* `ENG-1.5` (API-First Design) — *when they see the API contract in `design.md`*; `ENG-4.4` (Test Structure: Given-When-Then) — *when they see the BDD scenarios*  
*Visual:* `diagram-02-hangar-ai-specs-lifecycle.svg` — PROPOSE → IMPLEMENT → ARCHIVE flow with folder structure

**Phase 4: Proposal Review** *(10 min)*  
*What participants do:* Review generated artifacts with the AI agent. Challenge the design choices. Understand why each spec element exists.  
*Laws introduced contextually:* `ENG-2.3` (Vertical Slice) — *when they see the slice definition*; `ENG-11.2` (Proposal Completeness) — *when they verify their PROPOSAL.md cites laws*

**Phase 5: Implementation with Atomic TDD** *(60 min — the core of the session)*  
*What participants do:* Execute 2–3 full TDD cycles on their first vertical slice: RED → GREEN → REFACTOR → VERIFY → COMMIT → REPEAT.  
*Laws introduced contextually:*
- `ENG-4.1` NON-NEGOTIABLE — *introduced at the first RED step, with the full cycle on the wall*
- `ENG-4.3` (FIRST principles) — *introduced when their first test takes too long*
- `ENG-4.5` (Test Naming) — *introduced when a participant names a test `test1()`*
- `ENG-3.1` (Complexity ≤10) — *introduced during REFACTOR step*
- `ENG-4.6` (Coverage ≥90% new code) — *introduced at VERIFY gate*

*Visual:* `diagram-03-tdd-cycle.svg` — The six-step atomic cycle displayed prominently; anti-patterns listed alongside each step  
*Visual:* `diagram-04-test-pyramid.svg` — Reference card showing 70/20/10 distribution

**Wrap-Up** *(10 min)*  
Archive the proposal to `hangar-ai-specs/archive/`. Debrief: which laws did they cite? Which violations did the linter catch? What would they do differently?

#### Agentic SDLC Workshop Updates (required before Session 1 can run)

| Change | Detail |
|---|---|
| **Remove Fast Track** | Delete the `## Fast Track` section and all references to it |
| **Remove Weather Dashboard** | Delete `backend/` and `frontend/` directories; remove all references to "Weather Dashboard" from `WORKSHOP-GUIDE.md`, `README.md`, and any supporting docs |
| **Remove Hangar SDD prerequisite** | Replace `ls hangar-ai-specs/` check with a plain `hangar-ai-specs/` scaffold instruction; remove `` |
| **Update references to `hangar-ai-specs/`** | All occurrences in the guide, workspace compliance section, and reference section |
| **Add Greenfield Workflow context header** | Add a "Workflow Context" callout at the top of the Step-by-Step section linking to `workflows/greenfield-development.md` and mapping each phase to its workflow phase number |
| **Add contextual law introductions** | Insert 2–3 line "Why this matters" callouts at each phase (see above), replacing the current front-loaded prerequisite list |
| **Update `session-output/` scaffold** | Use `hangar-ai-specs/` in the compliance section workspace diagram |

---

### Phase 2: Session 2 — Legacy Adoption: Characterization Tests & Rescue

Session 2 uses and significantly enhances the Adoption Test Workshop. It is structured as a deep investigation: participants go into a codebase looking for trouble, name what they find with law citations, and leave with a characterization test proposal ready to execute on their own work.

#### Overview

Participants work on `loyalty-service-legacy/` (provided) OR bring their own codebase. They surface violations, understand the architectural and design principles being broken, write characterization tests to lock existing behavior, and produce a PROPOSAL.md for rescue work. The session ends with participants having a concrete next step for their real codebase.

#### Phase-by-Phase Flow

**Phase 1: Domain Archaeology** *(25 min)*  
*What participants do:* Open the codebase cold. Read the code as an investigator. Map what the application does, who the domain objects are, what the data flows look like.  
*Laws introduced contextually:* `ENG-2.1` (DDD: entities, value objects, aggregates) — *introduced when they find financial logic sitting in a controller*; `ENG-2.4` (Bounded Contexts) — *introduced when they see unrelated concerns tangled together*  
*Visual:* `diagram-05-good-bad-architecture.svg` — Side-by-side: 270-line controller vs. domain objects + vertical slices; violation callouts with law IDs

**Phase 2: Violation Inventory** *(30 min)*  
*What participants do:* Produce a structured violation list — each item names the code location, the law violated, and the risk. Work in pairs. Share findings.  
*Laws introduced contextually (as violations are surfaced):*

| Violation found in `loyalty-service-legacy` | Law | Teaching moment |
|---|---|---|
| 270-line controller, cyclomatic complexity ~18 | `ENG-3.1` | How to measure complexity; what ≤10 looks like |
| Financial miles calculation with no domain object | `ENG-3.4` (Single Responsibility) | One class, one reason to change |
| 0% test coverage on critical financial paths | `ENG-4.6` (Coverage ≥90% new, 100% critical) | The risk of untested financial logic |
| No test names describe behavior | `ENG-4.5` (Naming Convention) | `test1()` vs. `calculateMiles_goldStatus_appliesMultiplier()` |
| Mocking the domain in unit tests | `ENG-4.8` (Mock Boundaries) | What to mock, what not to |
| PII passed through unsanitized | `ENG-6.5` (Input Validation) | Where validation belongs |
| No audit logging on loyalty transactions | `ENG-6.7`, `BUS-7.1` | Real vs. fake audit trail |

*Visual:* `diagram-06-violation-types.svg` — Taxonomy of violations by law domain (Engineering, Business, Product) with severity indicators

**Phase 3: Good Code Deep Dive** *(20 min)*  
*What participants do:* Side-by-side comparison of the violated code vs. the constitutionally-compliant version. Discussion: what changed, why, which law it satisfies.  
*Format:* Slide deck `slides-good-bad-code.html` — one violation per slide, bad code on left (red callouts), good code on right (law badge), explanation below  

**Examples covered:**

| Bad code | Law | Good code |
|---|---|---|
| `float milesEarned = baseMiles * 1.5;` | `ENG-3.2` | Domain object `MilesCalculation` with `BigDecimal` and rounding law cited |
| `public void processEverything(Customer c)` 270 lines | `ENG-3.1`, `ENG-3.4` | `MilesService`, `TierService`, `AuditService` — each ≤50 lines |
| `if (status.equals("GOLD")) { if (flight.isDomestic()) { if ...` | `ENG-3.1` | Strategy pattern; cyclomatic complexity = 2 |
| `logger.info("Processing customer " + id)` | `ENG-6.7`, `BUS-7.1` | `AuditLog.record(WHO, WHAT, WHEN, WHERE, RESULT)` |
| `@Test public void test1()` | `ENG-4.5` | `calculateMiles_goldStatusDomestic_applies15xMultiplier()` |
| `Mockito.mock(LoyaltyService.class)` in unit test | `ENG-4.8` | Mock `LoyaltyRepository` (I/O boundary only) |

**Phase 4: Characterization Tests** *(45 min — the core of the session)*  
*What participants do:* Write characterization tests that lock the existing (broken) behavior before touching anything. This is the entry point to any legacy rescue.  
*Laws introduced contextually:* `ENG-4.1` NON-NEGOTIABLE — *RED step: the test will be RED if behavior is already wrong, and that's the point*; `ENG-4.3` (FIRST principles) — *introduced when a test has external dependencies*  

*Lab steps:*

| Step | Activity | Law |
|---|---|---|
| 1 | Create `AGENTS.md` for the legacy project with law citations | `ENG-11.1`, `ENG-1.2` |
| 2 | Scaffold `hangar-ai-specs/changes/loyalty-rescue/PROPOSAL.md` | `ENG-11.1`, `ENG-11.2` |
| 3 | Write characterization test for `calculateMiles()` — assert what it currently does, not what it should do | `ENG-4.1`, `ENG-4.3` |
| 4 | Write characterization test for tier status progression logic | `ENG-4.1`, `ENG-4.4` |
| 5 | Run both tests — they should pass (we're locking current behavior) | `ENG-4.6` |
| 6 | Add a third test that *exposes* a known violation (it will fail) | `ENG-4.1` (RED step — intentional) |
| 7 | Determine: refactor, rewrite, or hybrid? Cite laws for the decision | `legacy-rescue-decision-track` workflow |

*Visual:* `diagram-07-characterization-test-flow.svg` — User journey: developer opening a legacy codebase → violation discovery → characterization → safe refactor entry

**Wrap-Up & Handoff** *(10 min)*  
Participants update their `PROPOSAL.md` with findings from today's session. The proposal now has: violation inventory, characterization tests written, rescue track decision with law citations, and a first slice defined. This is their homework — run it against their real codebase.

#### Adoption Test Workshop Updates (required before Session 2 can run)

| File | Enhancement |
|---|---|
| `docs/adoption-prompt.md` | Expand into a full participant guide: violation inventory template, characterization test walkthrough, PROPOSAL.md template with required law citation fields |
| `docs/lab-guide-instructor.md` (new) | Timing guide, common misconceptions per phase, what to watch for, suggested discussion questions |
| `docs/lab-guide-participant.md` (new) | Self-contained participant guide: step-by-step with worked examples, law reference sidebar |
| `loyalty-service-legacy/VIOLATION-INVENTORY.md` (new) | Pre-computed violation list for instructor reference (spoilers — instructor only) |
| `loyalty-service-legacy/sample-characterization-tests/` (new) | Worked examples of characterization tests (reference only, not in test suite) |
| `README.md` | Link to `legacy-rescue-refactor.md` workflow; use `hangar-ai-specs/` |
| Updated AI verification checklist | See below |

**Updated AI verification checklist:**
```
After AI-assisted adoption, verify:
  ✅ AGENTS.md cites specific law IDs (not generic boilerplate)
  ✅ hangar-ai-specs/changes/[id]/PROPOSAL.md exists with law references
  ✅ Characterization test proposal present with test names following ENG-4.5
  ✅ Violation inventory cites specific law IDs and code locations
  ✅ Rescue track selected (refactor / rewrite / decision) with constitutional rationale
  ✅ No reference to openspec/ folder — uses hangar-ai-specs/
```

---

### Phase 3: Visual Artifacts

All diagrams created as SVG (scalable for slides, PDF, print) with AA theme colors. Each diagram is self-contained — law IDs annotated directly on the diagram so participants can reference them without looking up text.

| File | Type | Session | Purpose |
|---|---|---|---|
| `diagram-01-constitution-overview.svg` | Architecture overview | S1 | Laws → Skills → Avatars → Workflows composition |
| `diagram-02-hangar-ai-specs-lifecycle.svg` | Process flow | S1 | PROPOSE → IMPLEMENT → ARCHIVE with folder structure |
| `diagram-03-tdd-cycle.svg` | Cycle diagram | S1 | RED→GREEN→REFACTOR→VERIFY→COMMIT→REPEAT with anti-patterns |
| `diagram-04-test-pyramid.svg` | Pyramid chart | S1 | 70/20/10 with real test-count examples |
| `diagram-05-good-bad-architecture.svg` | Side-by-side | S2 | 270-line controller vs. domain objects (annotated violations) |
| `diagram-06-violation-types.svg` | Taxonomy tree | S2 | Violation categories by law domain with severity |
| `diagram-07-characterization-test-flow.svg` | User journey | S2 | Developer journey: open legacy codebase → rescue proposal |
| `diagram-08-rescue-track-decision.svg` | Decision flowchart | S2 | Refactor vs. Rewrite vs. Hybrid decision tree with law citations |
| `diagram-09-greenfield-workflow.svg` | Activity diagram | Reference | 8-phase greenfield with entry/exit gates per phase |

---

### Phase 4: PDF Generation (HTML/CSS with AA Theme)

Generate workshop materials using the same HTML/CSS toolchain as discovery packages and adoption packages. AA visual identity throughout.

**Artifacts generated:**

| File | Description |
|---|---|
| `workshop-session-1-participant-guide.html` | S1 workbook: phase reference cards, TDD cycle cheat sheet, law callout index |
| `workshop-session-2-participant-guide.html` | S2 workbook: violation inventory template, characterization test guide, PROPOSAL.md template |
| `workshop-facilitator-guide.html` | Instructor guide: timing, talking points, facilitation notes, common questions |
| `workshop-quick-reference-card.html` | 2-page card: most-cited laws, TDD cycle, `hangar-ai-specs/` structure, rescue track decision criteria |
| `workshop-slides-session-1.html` | S1 slide deck: constitution overview, phase-by-phase reference (HTML, printable) |
| `workshop-slides-session-2.html` | S2 slide deck: good/bad code pairs, violation taxonomy, characterization flow |

**AA Theme (consistent with existing packages):**
- Typography: AA fonts; headers in AA blue (`#0078D2`); body sans-serif
- `NON-NEGOTIABLE` law callouts: red left-border with law ID badge
- `REQUIRED` callouts: amber left-border
- Code blocks: dark background, violation annotations in red inline, law ID badges on compliant lines
- Layout: same grid/card system as `docs-common.css` from `aa-hangar-labs/`

**Location:**
```
docs/workshops/
  session-1/
    lab-guide.md                              ← instructor
    lab-participant.md                        ← participant
    workshop-session-1-participant-guide.html
    slides-session-1.html
  session-2/
    lab-guide.md
    lab-participant.md
    workshop-session-2-participant-guide.html
    slides-session-2.html
    slides-good-bad-code.html
  shared/
    facilitator-guide.html
    quick-reference-card.html
    workshop-common.css                       ← AA-themed styles
    diagrams/                                 ← all 9 SVGs
```

---

## Session Plan Summary

### Session 1: Agentic SDLC — Self-Service Track (3 hours)

| Time | Phase | Activity | Laws surfaced in context |
|---|---|---|---|
| 0:00–0:20 | Phase 1 | Constitution Adoption: AGENTS.md + `hangar-ai-specs/` | `ENG-1.2`, `ENG-11.1` |
| 0:20–0:35 | Phase 2 | Avatar Selection | `PRD-2.1`, `ENG-1.1` |
| 0:35–1:00 | Phase 3 | Spec Generation: PROPOSAL + design + BDD + tasks | `ENG-1.5`, `ENG-4.4`, `ENG-11.2` |
| 1:00–1:10 | Phase 4 | Proposal Review with AI agent | `ENG-2.3`, `ENG-11.2` |
| 1:10–2:10 | Phase 5 | Atomic TDD: 2–3 full cycles | `ENG-4.1`, `ENG-4.3`, `ENG-4.5`, `ENG-3.1`, `ENG-4.6` |
| 2:10–2:20 | Wrap-Up | Archive proposal; debrief | `ENG-11.1` |
| 2:20–2:30 | Buffer | Questions; environment issues | — |

### Session 2: Legacy Adoption — Characterization Tests & Rescue (3 hours)

| Time | Phase | Activity | Laws surfaced in context |
|---|---|---|---|
| 0:00–0:25 | Phase 1 | Domain Archaeology: map the codebase | `ENG-2.1`, `ENG-2.4` |
| 0:25–0:55 | Phase 2 | Violation Inventory (pairs) | `ENG-3.1`, `ENG-3.4`, `ENG-4.5`, `ENG-4.6`, `ENG-4.8`, `ENG-6.5`, `ENG-6.7`, `BUS-7.1` |
| 0:55–1:15 | Phase 3 | Good Code Deep Dive (slides) | All above — visual side-by-side |
| 1:15–2:00 | Phase 4 | Characterization Tests + PROPOSAL.md | `ENG-4.1`, `ENG-4.3`, `ENG-11.1`, `ENG-11.2` |
| 2:00–2:10 | Wrap-Up | Rescue track decision; handoff to real codebase | `legacy-rescue-*` workflows |
| 2:10–2:20 | Buffer | Questions; next steps | — |

---

## Greenfield Workflow Integration (Scope Addition — March 2026)

**Problem observed:** In the previous Agentic SDLC workshop delivery, participants produced inconsistent results because they lacked **prompt maturity** — each person's AI coding agent responded differently because every participant was winging their prompts without a shared pattern. The root cause was no structured prompt guide and no explicit workflow backbone to orient the session.

**Solution:** Wire Session 1 directly to the `greenfield-development` workflow as its phase backbone, and produce a **Learner Prompt Guide** — a printed/shareable card that gives participants copy-pasteable, structured prompts for each workflow phase. This establishes a consistent **token-optimized context** across all participants' agents from the first message.

### What Changes

**1. WORKSHOP-GUIDE.md backbone becomes the Greenfield Workflow**

Each Session 1 phase maps 1:1 to a `greenfield-development` workflow phase. The guide explicitly names the workflow phase, the skills activated, the laws enforced, and the avatar in use at each step. This means the AI agent running the workshop and the participant's AI coding agent share the same constitutional context.

| Session 1 Phase | Greenfield Workflow Phase | Skills Activated | Laws Enforced |
|---|---|---|---|
| Constitution Adoption | Phase 1: Capture | `skill-spec-governance` | `ENG-11.1`, `ENG-1.2` |
| Avatar Selection | Phase 2: Discover | `skill-04-business-domain-modeling` | `PRD-2.1`, `ENG-1.1` |
| Spec Generation | Phase 3: Define | `skill-02-user-journey-mapping`, `skill-03-executable-spec` | `ENG-1.5`, `ENG-4.4`, `ENG-11.2` |
| Proposal Review | Phase 4: Design | `skill-spec-governance` | `ENG-2.3`, `ENG-11.2` |
| Atomic TDD | Phases 5+6: Plan → Build | `skill-06-atomic-tdd`, `skill-07-vertical-slice-dev` | `ENG-4.1` (NON-NEGOTIABLE), `ENG-4.3`, `ENG-4.6` |
| Archive + Debrief | Phase 8: Ship | `skill-spec-governance` | `ENG-11.1` |

**2. Learner Prompt Guide (`learner-prompt-guide.md` + HTML print artifact)**

A structured prompt guide that participants use throughout the session. Each prompt is:
- **Token-optimized** — loads only the context needed for the current phase (avatar ID, workflow phase ID, skill ID, law IDs). No wall of prose.
- **Consistent** — every participant starts from the same context bootstrap, eliminating the divergence seen last time.
- **Teachable** — the prompt structure itself teaches the constitutional pattern: Avatar → Workflow → Skill → Law. Participants leave knowing how to construct their own prompts.

The guide covers:
- **Session Bootstrap Prompt** — activates the engineering avatar, loads the greenfield workflow, names the session domain
- **Phase-by-phase prompt cards** (Phases 1–8 of greenfield workflow)
- **Skill invocation patterns** — how to call a skill by name and what to expect
- **TDD prompt sequence** — RED prompt → GREEN prompt → REFACTOR prompt → VERIFY prompt
- **Recovery prompts** — what to say when the agent goes off-track, over-generates, or violates a law
- **Session 2 bootstrap** — activates legacy rescue context with the `legacy-rescue-refactor` workflow

### New Deliverables Added

| Artifact | Location | Format |
|---|---|---|
| `learner-prompt-guide.md` | `docs/workshops/session-1/` | Markdown (source) |
| `learner-prompt-guide.html` | `docs/workshops/session-1/` | HTML/CSS (AA theme, print-optimized) |

---

## Success Criteria

| Criteria | Target |
|---|---|
| Weather Dashboard and Fast Track removed from Agentic SDLC Workshop | ✅ |
| Hangar SDD prerequisite removed; `hangar-ai-specs/` used throughout | ✅ |
| Session 1 materials complete (guide, slides, participant workbook) | ✅ |
| Session 2 materials complete | ✅ |
| All 9 visual diagrams created with law annotations | 9 |
| PDF/HTML artifacts generated with AA theme | 6 |
| Adoption Test enhanced with lab guides, violation inventory, sample tests | ✅ |
| Agentic SDLC Workshop updated with workflow context + `hangar-ai-specs/` | ✅ |
| All workshop material in `docs/workshops/` inside the constitution | ✅ |
| Laws introduced contextually — no standalone lecture blocks > 10 min | ✅ |
| Participant leaves Session 2 with a PROPOSAL.md for their real codebase | Target |
| WORKSHOP-GUIDE.md phases map 1:1 to `greenfield-development` workflow phases | ✅ |
| Each WORKSHOP-GUIDE.md phase cites workflow phase ID, skill IDs, law IDs, avatar | ✅ |
| Learner Prompt Guide delivered (md + HTML print artifact) | ✅ |
| Session bootstrap prompt is token-optimized (avatar+workflow+skill+law IDs, no prose bloat) | ✅ |
| Recovery prompts included for common agent drift patterns | ✅ |

---

## Decisions

| # | Question | Decision |
|---|---|---|
| 1 | Delivery format | **In-person** — lab guides written for side-by-side pairing; no virtual facilitation accommodations needed |
| 2 | AI assistant | **GitHub Copilot** — all lab instructions, prompts, and guardrail references are written for Copilot specifically |
| 3 | Language parity | **Java only** — `loyalty-service-legacy` stays Java; violations and constitutional principles are universal; no Python equivalent needed |
| 4 | Codebase for Session 2 | **`loyalty-service-legacy` in class; own codebase as take-home** — a pre-screening checklist is provided so participants can apply the characterization test proposal to their real codebase after the session |

---

## References

- [Proposal 1 (prerequisite)](../constitution-workflow-governance-evolution/PROPOSAL.md)
- [Agentic SDLC Workshop Guide](../../hangar-ai-constitution-greenfield/WORKSHOP-GUIDE.md)
- [Adoption Test Workshop](../../hangar-ai-constitution-brownfield/)
- [Greenfield Workflow (post Proposal 1)](../../workflows/greenfield-development.md)
- [Legacy Rescue Workflows (post Proposal 1)](../../workflows/legacy-rescue-refactor.md)
- [Testing Laws](../../laws/engineering/testing.md)
- [Code Quality Laws](../../laws/engineering/quality.md)
- [Discovery Laws](../../laws/product/discovery.md)
- [Audit Laws](../../laws/business/audit.md)
- [Discovery Package HTML/CSS Toolchain](../../../aa-hangar-labs/discovery-packages/)
- [Adoption Package HTML/CSS Toolchain](../../../aa-hangar-labs/adoption-packages/)
