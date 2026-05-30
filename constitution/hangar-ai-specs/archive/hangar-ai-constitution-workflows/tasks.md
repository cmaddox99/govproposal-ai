# Tasks: Hangar AI Constitution Workflows — Practical Exercises & Workshops

**Proposal ID:** hangar-ai-constitution-workflows  
**Total Tasks:** 27  
**Status:** DRAFT — Awaiting Governance Approval

---

## Phase 1: Exercise Codebase Scaffolding & Content (7 tasks)

### 1.1: Create Exercise Repository Structure
- [ ] Create `hangar-ai-constitution-workflows` repository at governance root
- [ ] Initialize README.md with orientation & quick-start guide
- [ ] Initialize SETUP.md with SonarQube credentials setup & language prerequisites
- [ ] Create `exercises/` directory with ex1–4 subdirectories
- [ ] Create `.env.example` with SonarQube token placeholder
- [ ] Add `.gitignore` (exclude `.env`, `node_modules`, `__pycache__`)

**Acceptance:** Repo structure matches specification; all 4 exercise directories created with README placeholders

### 1.2: Exercise 1 — Code Assessment (Decision Track)
- [ ] Create `exercises/ex1-code-assessment/legacy.js` (20–30 LOC legacy function with debt markers)
- [ ] Create `exercises/ex1-code-assessment/assessment-template.md` (learner worksheet)
- [ ] Create `exercises/ex1-code-assessment/solution/assessment-complete.md` (reference solution)
- [ ] Create `exercises/ex1-code-assessment/README.md` with:
  - Learning objectives (decision track, ENG-3.1, ENG-14, skill-14-technical-debt)
  - Time estimate (30 min)
  - Step-by-step instructions
  - Law/skill citations

**Acceptance:** Exercise is clear; learner can complete assessment in ≤30 min; solution provided

### 1.3: Exercise 2 — Refactor via TDD (Atomic TDD)
- [ ] Create `exercises/ex2-refactor-tdd/tests/function.test.js` (complete test suite)
- [ ] Create `exercises/ex2-refactor-tdd/src/function.js` (skeleton; learners implement)
- [ ] Create `exercises/ex2-refactor-tdd/solution/function.js` (reference solution)
- [ ] Create `exercises/ex2-refactor-tdd/README.md` with:
  - Learning objectives (ENG-4.1, atomic TDD, skill-06-atomic-tdd)
  - Time estimate (45 min)
  - RED → GREEN → REFACTOR guidance
  - SonarQube RED gate expectations

**Acceptance:** Tests pass with reference solution; learner path is clear; RED validation is reproducible

### 1.4: Exercise 3 — Greenfield Feature (Spec-Driven)
- [ ] Create `exercises/ex3-greenfield-feature/spec.md` (feature specification)
- [ ] Create `exercises/ex3-greenfield-feature/tests/feature.test.js` (failing test scaffold)
- [ ] Create `exercises/ex3-greenfield-feature/src/feature.js` (skeleton)
- [ ] Create `exercises/ex3-greenfield-feature/solution/feature.js` (reference solution)
- [ ] Create `exercises/ex3-greenfield-feature/README.md` with:
  - Learning objectives (ENG-4.1, ENG-7.x, skill-12-api-design, skill-07-vertical-slice-dev)
  - Time estimate (60 min)
  - Spec-first development guidance
  - Integration testing expectations (ENG-4.6)

**Acceptance:** Feature compiles & tests pass; spec clearly guides implementation; learner path is intuitive

### 1.5: Exercise 4 — Full Workflow Execution (Integrated)
- [ ] Create `exercises/ex4-full-workflow/codebase/` (mini-app: legacy code + new feature request)
- [ ] Create `exercises/ex4-full-workflow/WORKFLOW-GUIDE.md` (step-by-step execution)
- [ ] Create `exercises/ex4-full-workflow/README.md` with:
  - Learning objectives (decision track, refactor, rewrite, greenfield)
  - Time estimate (105 min total; breakdown per step)
  - Three decision paths clearly marked (refactor path, rewrite path, greenfield feature path)
  - Avatar context extraction guidance
- [ ] Create `exercises/ex4-full-workflow/solutions/` (reference solutions for each path)

**Acceptance:** All three paths are executable & documented; time budget validated; solutions provided

### 1.6: SonarQube Project Setup
- [ ] Provision 4 SonarQube projects on sonarqube.aa.com:
  - `hangar-ai-constitution-workflows-ex1`
  - `hangar-ai-constitution-workflows-ex2`
  - `hangar-ai-constitution-workflows-ex3`
  - `hangar-ai-constitution-workflows-ex4`
- [ ] Configure HARD_BLOCK gates for ex1–3 (ENG-6.1, ENG-6.4, ENG-6.7)
- [ ] Configure HARD_BLOCK + PHASE_GATE for ex4 (ENG-4.6, ENG-11.1)
- [ ] Document SonarQube token management in SETUP.md (secure distribution)
- [ ] Test token access from local CLI (`sonar-scanner` with env var)

**Acceptance:** All 4 projects created & gates configured; token setup documented & tested

### 1.7: Exercise Validation Scripts
- [ ] Create `exercises/validate.sh` (master validation script for all 4 exercises)
- [ ] Create `exercises/ex1-code-assessment/validate.sh` (assessment completeness check)
- [ ] Create `exercises/ex2-refactor-tdd/validate.sh` (tests pass + SonarQube gate check)
- [ ] Create `exercises/ex3-greenfield-feature/validate.sh` (tests pass + integration test check)
- [ ] Create `exercises/ex4-full-workflow/validate.sh` (one of three paths executable + SonarQube gates pass)
- [ ] Test all validation scripts against reference solutions

**Acceptance:** All 4 validation scripts pass with reference solutions; errors are clear & actionable

---

## Phase 2: Part 1 Materials (10 tasks)

### 2.1: Slideware Deck 1 — Workflows Overview
- [ ] Create `slideware/part-1/01-workflows-overview.md`
- [ ] Include:
  - The 5 workflows (product discovery, greenfield, decision, refactor, rewrite)
  - Law citations for each workflow
  - Skill compositions for each workflow
  - Avatar context (business, tech, product)
  - Visual: workflow decision tree
- [ ] Embed law IDs with links to constitution
- [ ] Include 2–3 real-world scenarios (when to use each workflow)

**Acceptance:** Deck is presentable; all law/skill IDs verified; slides are clear & time-bounded (30 min presentation)

### 2.2: Slideware Deck 2 — Decision Track Criteria
- [ ] Create `slideware/part-1/02-decision-track-criteria.md`
- [ ] Include:
  - Decision track purpose (refactor vs. rewrite determination)
  - Assessment criteria (code smell patterns, complexity metrics, team capacity)
  - Skill: skill-14-technical-debt, skill-04-business-domain-modeling
  - SonarQube role (violations as input to decision)
  - 5+ real-world scenarios (when to refactor, when to rewrite)
- [ ] Cite ENG-3.1, ENG-14, BUS-7.1, PRD-2.2

**Acceptance:** Facilitators can teach decision track in 30 min; scenarios are realistic & diverse

### 2.3: Slideware Deck 3 — Atomic TDD in Practice
- [ ] Create `slideware/part-1/03-atomic-tdd-practice.md`
- [ ] Include:
  - RED phase: write ONE failing test (ENG-4.1)
  - GREEN phase: minimal code to pass (no more)
  - REFACTOR phase: improve design while tests stay green
  - VERIFY phase: SonarQube gate checks (skill-sonarqube-compliance-gate)
  - Common mistakes & fixes
- [ ] Visual: RED → GREEN → REFACTOR cycle diagram
- [ ] Example: Ex 2 refactor walkthrough

**Acceptance:** TDD cycle is clear; learners understand RED/GREEN/REFACTOR distinction; SonarQube role is explicit

### 2.4: Slideware Deck 4 — Greenfield, Avatars, & Gates
- [ ] Create `slideware/part-1/04-greenfield-to-avatars-to-gates.md`
- [ ] Include:
  - Greenfield workflow (spec → RED → GREEN)
  - Avatar enrichment: how business/tech/product context shapes code decisions
  - Skill: skill-12-api-design, skill-07-vertical-slice-dev
  - SonarQube gates as constitutional enforcement
  - Ex 3 & 4 walkthrough
- [ ] Cite ENG-4.1, ENG-7.x, ENG-11.1, PRD-2.1, PRD-3.1

**Acceptance:** Avatars concept is clear; learners see connection between avatars → workflow choices → code

### 2.5: Part 1 Facilitator Guide Overview
- [ ] Create `facilitator-guides/FACILITATOR-MASTER.md`
- [ ] Include:
  - 3-hour session structure (breakdown: setup, Ex 1–4, debrief)
  - Facilitation philosophy (discovery-driven; prompt learners to connect to laws)
  - Common stumbling blocks (language setup, test runner, SonarQube token)
  - Group discussion prompts (e.g., "When would you refuse to refactor?")
  - Success signals (learners can articulate decision criteria, RED/GREEN/REFACTOR cycle)

**Acceptance:** Facilitators feel confident teaching the workshop with this guide

### 2.6: Exercise 1 Facilitator Guide
- [ ] Create `facilitator-guides/part-1/ex1-facilitator-guide.md`
- [ ] Include:
  - Learning objectives (decision track, ENG-3.1, ENG-14)
  - Time allocation (5 min intro, 20 min guided assessment, 5 min debrief)
  - Common mistakes: overcomplicating assessment, missing debt markers, not citing laws
  - Talking points: "What makes code 'hard to refactor'?" "How does SonarQube help assess?"
  - Law/skill callouts with constitution links
  - Group discussion: "Would you refactor or rewrite this function?"

**Acceptance:** Facilitator can guide Ex 1 in 30 min; talking points feel natural & law-grounded

### 2.7: Exercises 2–4 Facilitator Guides
- [ ] Create `facilitator-guides/part-1/ex2-facilitator-guide.md` (Refactor via TDD)
- [ ] Create `facilitator-guides/part-1/ex3-facilitator-guide.md` (Greenfield Feature)
- [ ] Create `facilitator-guides/part-1/ex4-facilitator-guide.md` (Full Workflow)
- [ ] Each guide includes:
  - Detailed time allocation
  - Common errors & solutions
  - Law/skill callouts
  - Group prompts
  - SonarQube gate timing & expected violations

**Acceptance:** All 3 guides are detailed & consistent in structure; facilitators can teach all 4 exercises

### 2.8: Part 1 Learner Guides & Embedded Prompts
- [ ] Create `learner-guides/LEARNER-MASTER.md` (orientation to workshop)
- [ ] Create `learner-guides/part-1/ex1-learner-guide.md` with embedded prompts:
  - "What law is this testing?" (ENG-3.1, ENG-14, skill-14-technical-debt)
  - "What debt markers do you see?" (with examples)
  - "How would you describe the refactor/rewrite decision?" (guided assessment)
- [ ] Create `learner-guides/part-1/ex2-learner-guide.md` with:
  - "What should this test validate?" (RED phase)
  - "What's the minimal code to pass?" (GREEN phase)
  - "How would you improve the design?" (REFACTOR phase)
  - "What does SonarQube tell you?" (gate check)
- [ ] Create `learner-guides/part-1/ex3-learner-guide.md` & `ex4-learner-guide.md` (similar structure)

**Acceptance:** Learners can work through exercises independently with guides; prompts connect to constitution

### 2.9: Law & Skill Verification
- [ ] Audit all slideware, facilitator guides, learner guides for law/skill citations
- [ ] Verify against constitution:
  - ENG-3.1, ENG-4.1, ENG-4.6, ENG-6.1, ENG-6.4, ENG-6.7, ENG-7.x, ENG-11.1, ENG-14
  - PRD-2.1, PRD-2.2, PRD-3.1, PRD-4.1
  - BUS-7.1
  - Skills: skill-04-business-domain-modeling, skill-06-atomic-tdd, skill-07-vertical-slice-dev, skill-12-api-design, skill-14-technical-debt, skill-sonarqube-compliance-gate
- [ ] Create `docs/constitution-law-index.md` (quick ref: laws per exercise)
- [ ] Create `docs/skill-index.md` (quick ref: skills per exercise)

**Acceptance:** 100% of law/skill citations verified; index docs are accurate & useful

### 2.10: Token Optimization Review (Optional)
- [ ] Review slideware, facilitator guides, learner guides for token bloat
- [ ] Apply 50% token reduction targets (or document exceptions)
- [ ] Validate that cut content is still accessible (cross-references, links to constitution)

**Acceptance:** Token savings documented; no learning loss

---

## Phase 3: Part 2 Materials (7 tasks)

### 3.1: Slideware Deck 1 — Real Codebases & SonarQube Setup
- [ ] Create `slideware/part-2/01-real-codebases-sonarqube-setup.md`
- [ ] Include:
  - SonarQube project provisioning (team ID, token management)
  - Avatar enrichment from participant repos (extract business, tech, product context)
  - Decision track application to real code (checklist)
  - Common pitfalls (large codebases, multiple languages, unfamiliar tech stacks)
- [ ] Visual: SonarQube project setup flow

**Acceptance:** Participants understand SonarQube setup; facilitators can guide provisioning in 30 min

### 3.2: Slideware Deck 2 — Workflow Decision Flowchart & Contingencies
- [ ] Create `slideware/part-2/02-workflow-decision-flowchart.md`
- [ ] Include:
  - Decision tree: "Should I refactor or rewrite?" (links to decision track criteria)
  - Greenfield feature decision: "Is there a feature request?"
  - Contingencies: "What if SonarQube blocks me?" (exception documentation per ENG-6.1)
  - Real-world scenarios from Part 2 assessment phase
- [ ] Visual: large flowchart with decision branches

**Acceptance:** Participants can navigate flowchart to choose their workflow; facilitators can coach decisions

### 3.3: Part 2 Facilitator Guide
- [ ] Create `facilitator-guides/part-2/real-codebases-facilitator-guide.md`
- [ ] Include:
  - 3-hour session structure (30 min setup, 30 min assess, 60 min execute, 15 min gates, 15 min debrief)
  - SonarQube project provisioning (step-by-step with screenshots)
  - Coaching questions for decision track (e.g., "What does this test failure tell you?")
  - Handling real-world complexity:
    - Monoliths vs. microservices (scope decisions)
    - Multiple languages (SonarQube polyglot support)
    - Unfamiliar tech stacks (facilitator pairing)
  - Exception handling per ENG-6.1 (when to fix, when to document)
  - Avatar extraction guidance (what counts as business/tech/product context?)
  - Debrief prompts (what governance helped? what hindered?)

**Acceptance:** Facilitators feel prepared for diverse participant scenarios; guide covers edge cases

### 3.4: Part 2 Learner Worksheets — Assessment Phase
- [ ] Create `learner-guides/part-2/real-codebases-learner-guide.md`
- [ ] Include sections:
  - **Setup Worksheet:** SonarQube project creation checklist
  - **Assessment Worksheet:** Decision track checklist (code smell patterns, complexity, team capacity, SonarQube violations)
  - **Avatar Extraction Worksheet:** Business goals, tech constraints, product roadmap (template)
  - **Workflow Decision Matrix:** "Should I refactor, rewrite, or add feature?" (guided template)

**Acceptance:** Learners can complete assessment in 30 min; worksheets guide decision clearly

### 3.5: Part 2 Learner Worksheets — Execution & Gate Check
- [ ] Create `learner-guides/part-2/execution-tracking.md`
- [ ] Include sections:
  - **Execution Checklist:** Workflow-specific steps (refactor, rewrite, or greenfield)
  - **SonarQube Gate Tracker:** Log HARD_BLOCK, PHASE_GATE, WARNING violations; document resolutions
  - **Commit Tracker:** Log git commits (audit trail per BUS-7.1, ENG-6.1)
  - **Constitution Alignment Reflection:** "What laws applied?" "Where did governance help/hinder?"

**Acceptance:** Learners can track execution with worksheets; SonarQube gate results are documented

### 3.6: SonarQube Part 2 Project Provisioning
- [ ] Create template for Part 2 participant projects: `hangar-ai-constitution-workflows-part2-{participant-id}`
- [ ] Document:
  - Role-based access (facilitators: admin, participants: analyst)
  - Gate configuration (copy from ex1–4)
  - Token distribution securely (env vars, not committed)
- [ ] Create provisioning script (automated project creation + role assignment)

**Acceptance:** Script provisions projects quickly; security model is clear

### 3.7: Avatar Enrichment Guide
- [ ] Create `docs/avatar-enrichment-guide.md`
- [ ] Include:
  - How to extract business context (goals, constraints, roadmap)
  - How to extract tech context (stack, constraints, team capacity)
  - How to extract product context (user needs, success metrics)
  - Worksheet template (reusable for Part 2)
  - Real-world example (one of Part 1 exercises walkthrough)

**Acceptance:** Guide is clear; learners can extract avatars from any codebase

---

## Phase 4: Integration & Governance Review (3 tasks)

### 4.1: Constitution Integration
- [ ] Link hangar-ai-constitution-workflows from constitution README
- [ ] Add exercises codebase to `hangar-ai-specs/README.md` (orientation)
- [ ] Create `docs/sonarqube-setup-troubleshooting.md` (common issues + fixes)
- [ ] Verify all exercises are discoverable from constitution workflows

**Acceptance:** Constitution README updated; exercises are easy to find; troubleshooting guide covers 10+ scenarios

### 4.2: Linter & Citation Verification
- [ ] Run constitution linter on all materials (law/skill/workflow citations)
- [ ] Verify 100% of law IDs exist in constitution
- [ ] Verify 100% of skill IDs exist in constitution
- [ ] Verify all workflow references are correct (product-discovery-stage-a-f, greenfield-development, legacy-rescue-decision-track, legacy-rescue-refactor, legacy-rescue-rewrite)
- [ ] Create validation report

**Acceptance:** Linter passes 100%; validation report generated; no broken citations

### 4.3: Governance Review Session
- [ ] Request governance review (architect + sentinel roles)
- [ ] Review coverage:
  - ENG-4.1 (Atomic TDD) enforcement in exercises ✅
  - ENG-6.1, ENG-6.4, ENG-6.7 (Audit Trail, Compliance) enforcement in SonarQube gates ✅
  - BUS-7.1 (Decision Governance) enforcement in decision track exercise ✅
  - PRD-2.x (Problem Framing) enforcement in avatar enrichment ✅
  - All three decision track paths (refactor, rewrite, greenfield feature) demonstrated ✅
- [ ] Obtain governance approval to merge

**Acceptance:** Governance session completed; all non-negotiable laws have enforcement evidence; proposal approved

---

## Summary

**Total Tasks:** 27  
**Phase 1 (Engineering):** 7 tasks  
**Phase 2 (Content):** 10 tasks  
**Phase 3 (Content):** 7 tasks  
**Phase 4 (Governance):** 3 tasks  

**Timeline:** 4–6 weeks (1 week per phase, with parallel work possible in Phases 2–3)

