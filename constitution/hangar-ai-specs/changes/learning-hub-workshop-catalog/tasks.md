# Tasks: learning-hub-workshop-catalog

> **Status:** In Progress — Phase 1 (Ensemble Deliberation)
> **Spec ID:** LHW-001
> **Baseline:** `aa-constitution-lint .` — 17/17 PASS (confirmed before Phase 0 began)
> **Laws governing this work:** ENG-13.1, ENG-11.1, ENG-10.1, BUS-7.1, PRD-2.5

---

## Progress Summary

| Phase | Total Tasks | Done | Remaining |
|-------|-------------|------|-----------|
| 0 — Governance Foundation | 5 | 3 | 2 |
| 1 — Ensemble Deliberation | 4 | 0 | 4 |
| 2 — Workshop Repository Readiness | 6 | 0 | 6 |
| 3 — Learning Hub Publication | 8 | 0 | 8 |
| 4 — Self-Service Verification | 5 | 0 | 5 |
| 5 — Artifact Rendering + Archive | 5 | 0 | 5 |
| **Total** | **33** | **3** | **30** |

---

## Phase 0 — Governance Foundation

> Establish the constitutional spec artifacts (PROPOSAL, slideware, tasks) before any implementation begins. All three must be committed together before Phase 1 begins.

- [x] 0.1 Create `hangar-ai-specs/changes/learning-hub-workshop-catalog/PROPOSAL.md` — full 4-workshop catalog proposal (LHW-001): problem statement, course details (HAW-GF-001, HAW-LR-001, HAW-AW-001, HAW-PD-001), sequencing, self-service mechanics, laws applied, acceptance criteria, 5 open questions for ensemble deliberation
- [x] 0.2 Create `hangar-ai-specs/changes/learning-hub-workshop-catalog/workshop-program-slides.html` — 10-slide AA-branded self-contained presentation for stakeholder review; keyboard navigable (←/→/Space/Home/End); AA design system (blue `#072c66`, red `#c8102e`, gold `#c79b2c`); no external dependencies
- [ ] 0.3 Create `hangar-ai-specs/changes/learning-hub-workshop-catalog/tasks.md` — this file
- [ ] 0.4 VERIFY — run `aa-constitution-lint .` → 0 failures
- [ ] 0.5 Commit: `feat(learning-hub): add workshop catalog PROPOSAL.md + slideware + tasks.md (LHW-001)`

---

## Phase 1 — Ensemble Deliberation

> Convene ensemble deliberation on the 5 open questions from LHW-001 PROPOSAL before any Learning Hub publication. Ensemble verdict must be APPROVED (all roles at partial approval or above) before Phase 2 begins.

- [ ] 1.1 Draft `hangar-ai-specs/changes/learning-hub-workshop-catalog/ensemble-deliberation.md` — 5 open questions deliberated by standard ensemble roster (Clara / Marcus / Sarah / David / Jin); each persona reviews the full proposal and addresses the questions in scope for their role; composite verdict recorded as YAML block
- [ ] 1.2 Resolve any open conditions from ensemble verdict that require PROPOSAL.md updates before publication (e.g., audience reframes, structural decisions on enrollment model, certification scope)
- [ ] 1.3 VERIFY — run `aa-constitution-lint .` → 0 failures
- [ ] 1.4 Commit: `feat(learning-hub): ensemble deliberation complete — LHW-001 APPROVED (BUS-7.1)`

---

## Phase 2 — Workshop Repository Readiness

> Verify that each of the four workshop repositories is in a publication-ready state before course pages are built. Document any gaps as blocked tasks with remediation path.

- [ ] 2.1 Audit `hangar-ai-constitution-greenfield` — confirm: bootstrap prompt present, WORKSHOP-GUIDE.md current, session-output isolation in place, constitution lint passes, `aa-constitution-lint` install step present for participants
- [ ] 2.2 Audit `hangar-ai-constitution-workflows` (Legacy Rescue) — confirm: both Part 1 and Part 2 lab guides present, sample codebase `loyalty-service-legacy` realistic and complete, participant gate checklists include linter install step
- [ ] 2.3 Audit `hangar-ai-constitution-avatars` (Avatar Workflow) — confirm: workshop guide present, avatar generation exercises functional, workshop is in a state that can be completed without instructor support
- [ ] 2.4 Audit Product Discovery workshop — confirm whether a dedicated workshop repository exists; if not, document as gap and record blocker with remediation scope for a future spec (HAW-PD-001 requires its own workshop repo before publication)
- [ ] 2.5 VERIFY — run `aa-constitution-lint .` → 0 failures
- [ ] 2.6 Commit: `feat(learning-hub): workshop readiness audit complete — gaps documented (LHW-001)`

---

## Phase 3 — Learning Hub Publication

> Build and publish all course pages. Each workshop must have a single-URL entry point covering title, description, duration, audience, outcomes, and link to the workshop repository. Ensemble verdict must be APPROVED before this phase begins.

- [ ] 3.1 Create Learning Hub course page for **HAW-GF-001** (Greenfield Development: Agentic SDLC in Practice) — title, description, 1-part / 3 hours, audience, outcomes table, link to `hangar-ai-constitution-greenfield`
- [ ] 3.2 Create Learning Hub course page for **HAW-LR-001** (Legacy Rescue: Governed Transformation) — title, description, 2-part / 6 hours, enrollment model per ensemble verdict, audience, outcomes table, link to `hangar-ai-constitution-workflows`
- [ ] 3.3 Create Learning Hub course page for **HAW-AW-001** (Avatar Workflow) — title, description, duration, audience sections per ensemble verdict (builders vs consumers), outcomes table, link to `hangar-ai-constitution-avatars`
- [ ] 3.4 Create Learning Hub course page for **HAW-PD-001** (Product Discovery) — title, description, audience reframe per ensemble verdict, outcomes table; publish only if Phase 2.4 audit confirms readiness, otherwise defer
- [ ] 3.5 Update Learning Hub landing page (`docs/workshops/index.html` or equivalent) — surface all four workshop cards, recommended learning path diagram, total time investment (12 hours), and link to `workshop-program-slides.html` for stakeholder preview
- [ ] 3.6 Add certification pathway section to landing page — per ensemble verdict on Question 5 (Hangar AI Constitutional Fluency badge on completion of all 4 workshops)
- [ ] 3.7 VERIFY — each published workshop accessible via single URL; run `aa-constitution-lint .` → 0 failures
- [ ] 3.8 Commit: `feat(learning-hub): publish 4-workshop catalog on Learning Hub (LHW-001, ENG-13.1)`

---

## Phase 4 — Self-Service Verification

> Verify that each published workshop can be completed by an AI agent without instructor support. Agent reads workshop guide, executes each phase, and produces all defined evidence artifacts. Document results as evidence.

- [ ] 4.1 Self-service dry-run for **HAW-GF-001** — AI agent given bootstrap prompt; verify it completes all phases, produces `AGENTS.md`, `PROPOSAL.md`, working implementation with 90%+ coverage, and `adoption-verified.md`; record PASS/FAIL
- [ ] 4.2 Self-service dry-run for **HAW-LR-001 Part 1** — AI agent completes characterization test phase; verify characterization tests committed and constitutional gate passes
- [ ] 4.3 Self-service dry-run for **HAW-LR-001 Part 2** — AI agent completes refactor or rewrite track; verify `refactor-plan.md` and test delta artifacts produced
- [ ] 4.4 Document self-service verification results as `evidence/self-service-verification.md` — PASS/FAIL per workshop, any gaps found, remediation applied; commit alongside Phase 4 tasks
- [ ] 4.5 VERIFY — run `aa-constitution-lint .` → 0 failures; commit: `feat(learning-hub): self-service verification evidence — all workshops PASS (LHW-001, BUS-7.1)`

---

## Phase 5 — Artifact Rendering + Archive

> Render all governance artifacts as HTML using `aa-artifact-render` (ENG-13.1). Archive the spec. Close LHW-001.

- [ ] 5.1 Render `PROPOSAL.md` as HTML: `aa-artifact-render hangar-ai-specs/changes/learning-hub-workshop-catalog/PROPOSAL.md --output PROPOSAL.html`
- [ ] 5.2 Render `ensemble-deliberation.md` as HTML: `aa-artifact-render hangar-ai-specs/changes/learning-hub-workshop-catalog/ensemble-deliberation.md --output ensemble-deliberation.html`
- [ ] 5.3 VERIFY — rendered HTML files open correctly in browser; run `aa-constitution-lint .` → 0 failures
- [ ] 5.4 Archive: `mv hangar-ai-specs/changes/learning-hub-workshop-catalog hangar-ai-specs/archive/$(date +%Y-%m-%d)-learning-hub-workshop-catalog`
- [ ] 5.5 Commit: `feat(archive): learning-hub-workshop-catalog complete — 4 workshops published to Learning Hub (LHW-001, BUS-7.1)`
