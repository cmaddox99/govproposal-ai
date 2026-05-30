# Proposal: Hangar AI Constitution Workflows — Practical Exercises & Workshops

**Proposal ID:** hangar-ai-constitution-workflows  
**Submitted:** March 31, 2026  
**Status:** DRAFT — Awaiting Governance Review  
**Execution Order:** Phase 2 of 2 (execute after `constitution-workflow-governance-evolution` lands)  
**Dependency:** Requires `constitution-workflow-governance-evolution` completion + SonarQube integration (Phase 9)

---

## Problem

The Hangar AI Constitution now defines three governed workflows for this workshop: legacy decision track, refactor, and rewrite. These address how engineering teams assess, decide, and transform legacy codebases. Teams can then apply the **Feature Development Workflow** to build new features in their rescued codebases. (Note: Standalone new projects and product discovery workflows are covered in separate workshops.)

**Current gaps:**
1. **No exercises codebase** — Workflows exist in the constitution but lack small, incremental, reproducible exercises that teach *how to apply* them
2. **No incremental learning arc** — Teams cannot progress from "understand workflow concepts" → "execute workflows on sample code" → "apply workflows to production codebases"
3. **No facilitated learning** — Workflows are documented but not taught with slideware, facilitator guides, or learner prompts
4. **Decision track not contextualized** — The decision track workflow (refactor vs. rewrite determination) lacks practical guidance on *when to decide*, *what to evaluate*, and *how to execute the chosen path*
5. **Avatar/law/skill/gate integration not visible** — Learners cannot see how avatar enrichment, constitutional laws, skill compositions, and SonarQube gates work together in a real workflow execution
6. **No hands-on SonarQube integration** — Teams cannot see how SonarQube compliance gates enforce laws in practice

---

## Solution

Create **hangar-ai-constitution-workflows**: a new exercises codebase + workshop program spanning **two 3-hour sessions** (Part 1 & Part 2, 6 hours total) that teaches constitutional workflow adoption through **interactive scenario-based learning with ensemble governance**, hands-on exercises, slideware, facilitator guides, and learner prompts.

**Key insight:** Anchor everything — exercises, slides, prompts, facilitator guides — in the constitution's **laws, skills, workflows, avatar enrichment, and SonarQube gates**. Every exercise teaches a constitutional concept. Ground all examples in **real American Airlines operational systems and FAA/TSA compliance requirements** to maximize relevance and authenticity.

### Interactive Scenario-Based Learning with Ensemble Governance

Rather than abstract exercises, participants engage with **realistic American Airlines scenarios** that demonstrate each workflow:

**Part 1 scenarios (provided sample systems):**
- **Scenario 1: Crew Scheduling System Assessment** — 12-year-old Node.js system with regulatory debt (FAA duty time tracking violations, accessibility issues)
- **Scenario 2: Maintenance Records Refactor** — Legacy monolith with test debt; learners refactor via atomic TDD while maintaining FAA audit trail integrity
- **Scenario 3: Flight Dispatch Feature Addition** — Participants add a new compliance feature to a rescued legacy system
- **Scenario 4: Full Governance in Flight Management** — End-to-end: assess a legacy flight rebooking system → decide refactor vs. rewrite → execute chosen path → add regulatory feature → enforce SonarQube gates

**Key pedagogical approach:**
1. **Ensemble governance during workshops** — Participants take on roles (architect, reviewer, sentinel, implementor) and vote on governance decisions using constitutional laws
2. **Law-cited traceability** — Every decision links back to specific laws (e.g., "Why refactor? Because ENG-3.1 + FAA Part 121 requires technical debt governance")
3. **Governance artifacts as outputs** — Each exercise produces DECISION.md, ASSESSMENT.md, GATES.md files that learners take away
4. **Multi-phase progression** — Discovery → Adoption → Assessment → Remediation → Execution → Certification (mirrors real-world transformation)
5. **Role-based deliberation** — Participants experience how governance trade-offs are resolved through constitutional ensemble voting, not unilateral decisions

### Part 1: Learn Workflows on Sample Legacy Codebases (Controlled Environment)

**Duration:** 3 hours  
**Format:** Self-paced hands-on exercises on provided sample codebases + facilitator-led demos + group discussion  
**Goal:** Master the legacy rescue workflows (decision track, refactor, rewrite) and feature development workflow through guided, predictable exercises
**Learning outcomes:**
- Understand the legacy rescue workflows (decision track, refactor, rewrite)
- Practice decision track criteria (refactor vs. rewrite assessment)
- Execute atomic TDD in refactor workflow
- Implement feature development workflow on a rescued codebase
- See SonarQube gates enforce constitutional laws
- Understand avatar enrichment (business, tech, product context)

**Exercises:** 4 progressive exercises using provided sample legacy codebases
- All participants work the same code examples
- Exercises guide the full cycle: assess → decide → execute (refactor/rewrite) → add feature
- Facilitator demonstrates each workflow; learners practice with confidence in controlled environment

| Exercise | Workflow | American Airlines Scenario | Duration | Law/Skill Focus |
|----------|----------|-------|----------|---|
| Ex 1: Crew Scheduling Assessment | Decision Track | Legacy crew duty-time tracking system (FAA Part 121 compliance); assess refactor vs. rewrite feasibility | 30 min | `ENG-3.1` (Technical Debt), `ENG-14` (Technical Debt Governance), `skill-14-technical-debt`, FAA Part 121 duty time rules |
| Ex 2: Maintenance Records Refactor | Refactor | Maintenance tracking monolith with test debt; refactor via atomic TDD with **mutation testing to kill mutants** (RED → GREEN → REFACTOR); verify ≥70% mutation score before merge | 45 min | `ENG-4.1` (Atomic TDD), `ENG-4.11` (Mutation Testing), `skill-06-atomic-tdd`, `skill-NN-mutation-testing`, SonarQube gate (RED validation + mutation score), FAA Part 147 maintenance documentation |
| Ex 3: Flight Dispatch Rescue Path | Refactor or Rewrite | Choose legacy rescue path for flight rebooking dispatch system; execute refactor vs. rewrite based on decision track assessment; validate with mutation testing (≥85% for TSA-critical functions) | 60 min | `ENG-3.1` (Technical Debt), `ENG-14` (Technical Debt Governance), `ENG-4.11` (Mutation Testing), `skill-16-refactor`, `skill-17-rewrite`, `skill-NN-mutation-testing`, TSA security compliance |
| Ex 4: Full Governance in Flight Management | All legacy rescue workflows + avatars + gates | Realistic AA flight management system: assess legacy code → decide path → execute (refactor/rewrite) → add TSA regulatory feature → enforce SonarQube gates including mutation score (≥70% general, ≥85% critical); role-based ensemble voting | 105 min | All legacy rescue laws/skills; `ENG-4.11`; avatar enrichment; SonarQube gates with mutation testing; FAA/TSA compliance requirements |

**Materials to create:**
- ✅ **Part 1 Slideware** — 4 decks (one per exercise) covering:
  - Workflow overview
  - Decision track criteria + assessment framework
  - Atomic TDD in practice with **mutation testing to verify test strength**
  - Feature Development Workflow lifecycle
  - Avatar enrichment (how business/tech/product context shapes workflow choices)
  - SonarQube gate checkpoints (coverage + **mutation score gates**)
  - Mutation testing concepts: killing mutants, interpreting scores, equivalent mutants
  - Law citations for each exercise (including `ENG-4.11`)
- ✅ **Exercise Codebase** — 4 self-contained airline-specific exercises:
  - Exercise 1: `exercises/ex1-crew-scheduling-assessment/` (FAA duty-time tracking system; assessment template)
  - Exercise 2: `exercises/ex2-maintenance-records-refactor/` (maintenance tracking monolith; RED test failing; learners execute TDD refactor)
  - Exercise 3: `exercises/ex3-flight-dispatch-path/` (flight rebooking system; learners choose and execute rescue path)
  - Exercise 4: `exercises/ex4-flight-management-full-workflow/` (realistic legacy AA system; learners apply full workflow with ensemble roles)
- ✅ **Facilitator Guide — Part 1** — Per-exercise guidance:
  - Learning objectives & time allocation
  - Common stumbling blocks + solutions
  - Facilitation talking points
  - Key law/skill callouts
  - SonarQube gate timing + expected violations/gates
  - Group discussion prompts (e.g., "When would you choose refactor over rewrite?")
- ✅ **Learner Prompts — Part 1** — In-exercise guidance:
  - "What law is this exercise testing?" (with link to constitution)
  - "What should this test do?" (RED validation)
  - "What's the minimal code to pass?" (GREEN minimalism)
  - "How does this improve the design?" (REFACTOR intent)
  - "What avatar context applies here?" (business, tech, product)
  - SonarQube violations: "What does this gate tell you?" (HARD_BLOCK, PHASE_GATE, WARNING)

### Part 2: Apply Workflows to Participant's Real Legacy Codebases (Real-World Application)

**Duration:** 3 hours  
**Format:** Participants bring their own legacy codebases; apply same workflows from Part 1 with facilitator + peer support  
**Goal:** Execute legacy rescue and feature development workflows on real production codebases with governance gates
**Learning outcomes:**
- Apply decision track assessment to own legacy codebase (same criteria as Part 1, but real code)
- Execute chosen workflow (refactor, rewrite, or feature development) on own codebase
- Generate SonarQube compliance evidence for real code
- Experience avatar enrichment with real product/business context specific to their team
- Navigate real governance trade-offs: technical debt vs. timeline vs. risk
- See full constitution-governed execution in a production-like scenario

**Execution model:**
1. **Setup (30 min):** Participants provision own repos in shared AA SonarQube instance
2. **Assess (30 min):** Apply decision track to own codebase (same Ex 4 assessment pattern from Part 1, now on real code)
3. **Choose & Execute (60 min):** Refactor, rewrite, or add feature to own codebase (same workflows practiced in Part 1)
4. **Gate Check (15 min):** Run SonarQube gates; address HARD_BLOCK violations in own code
5. **Debrief (15 min):** Group discussion on how governance trade-offs played out in their specific contexts

**Materials to create:**
- ✅ **Part 2 Slideware** — 2 decks:
  - Deck 1: Bringing real codebases; SonarQube project setup; avatar enrichment from real product context
  - Deck 2: Workflow decision flowchart; contingency planning (what if SonarQube blocks you?)
- ✅ **Facilitator Guide — Part 2** — Covers:
  - Repo provisioning + SonarQube setup
  - Coaching questions for decision track assessment
  - How to handle real-world complexity (partial refactors, tech stack mismatches, etc.)
  - Handling SonarQube violations (when to fix, when to document exception per ENG-6.1)
  - Avatar context extraction from participant repos
- ✅ **Learner Guide — Part 2** — Worksheet format:
  - "Assess your codebase" (decision track checklist)
  - "Choose your workflow" (decision matrix)
  - "Document your avatar context" (business goals, tech constraints, product roadmap)
  - "Track SonarQube gates" (log HARD_BLOCK/PHASE_GATE violations + resolutions)
  - "Reflect on constitution alignment" (what laws applied? where did governance help/hinder?)

### Exercises Codebase: `hangar-ai-constitution-workflows`

**Repository structure:**
```
hangar-ai-constitution-workflows/
├── README.md                       # Orientation: workflow overview, how to use this repo
├── SETUP.md                        # SonarQube setup; Prerequisites (Node? Python? Lang-agnostic?)
│
├── exercises/
│   ├── ex1-crew-scheduling-assessment/        # FAA duty-time tracking system assessment
│   │   ├── README.md
│   │   ├── legacy.js               # Crew scheduling legacy function (FAA debt markers)
│   │   ├── assessment-template.md  # Decision track assessment (refactor vs. rewrite)
│   │   └── solution/               # Reference: completed assessment
│   │
│   ├── ex2-maintenance-records-refactor/      # Maintenance tracking monolith refactor via TDD
│   │   ├── README.md
│   │   ├── tests/
│   │   │   └── maintenance.test.js    # Tests for learners to pass (RED state)
│   │   ├── src/
│   │   │   └── maintenance.js         # Skeleton (learners refactor via atomic TDD)
│   │   └── solution/               # Reference solution
│   │
│   ├── ex3-flight-dispatch-path/               # Flight rebooking system: refactor vs. rewrite
│   │   ├── README.md
│   │   ├── scenario.md             # Flight dispatch legacy challenge
│   │   ├── tests/
│   │   │   └── dispatch.test.js     # Behavior tests
│   │   ├── src/
│   │   │   └── dispatch.js          # Skeleton (learners choose and execute path)
│   │   └── solution/
│   │
│   └── ex4-flight-management-full-workflow/   # Realistic AA flight management system (end-to-end)
│       ├── README.md
│       ├── codebase/                # Mini-app with technical debt + new TSA compliance feature request
│       ├── WORKFLOW-GUIDE.md        # Step-by-step execution guide (assess → decide → execute → test → gate)
│       ├── ENSEMBLE-ROLES.md        # Role descriptions for governance deliberation (architect, reviewer, sentinel, implementor)
│       └── solutions/
│
├── slideware/
│   ├── part-1/
│   │   ├── 01-workflows-overview.md
│   │   ├── 02-decision-track-criteria.md
│   │   ├── 03-atomic-tdd-practice.md
│   │   └── 04-feature-dev-avatars-gates.md
│   │
│   └── part-2/
│       ├── 01-real-codebases-sonarqube-setup.md
│       └── 02-workflow-decision-flowchart.md
│
├── facilitator-guides/
│   ├── FACILITATOR-MASTER.md       # Overview + facilitation strategy
│   ├── part-1/
│   │   ├── ex1-facilitator-guide.md
│   │   ├── ex2-facilitator-guide.md
│   │   ├── ex3-facilitator-guide.md
│   │   └── ex4-facilitator-guide.md
│   │
│   └── part-2/
│       └── real-codebases-facilitator-guide.md
│
├── learner-guides/
│   ├── LEARNER-MASTER.md           # How to use this workshop
│   ├── part-1/
│   │   ├── ex1-learner-guide.md    # Includes embedded prompts
│   │   ├── ex2-learner-guide.md
│   │   ├── ex3-learner-guide.md
│   │   └── ex4-learner-guide.md
│   │
│   └── part-2/
│       └── real-codebases-learner-guide.md  # Assessment + execution worksheets
│
├── hangar-ai-specs/
│   └── changes/
│       └── hangar-ai-constitution-workflows/  # This proposal
│           ├── PROPOSAL.md
│           ├── tasks.md
│           └── PROGRESS.md
│
└── docs/
    ├── constitution-law-index.md            # Quick ref: laws cited in each exercise
    ├── skill-index.md                       # Quick ref: skills activated per exercise
    ├── workflow-index.md                    # Quick ref: workflow phases per exercise
    ├── avatar-enrichment-guide.md           # How to extract avatar context from a codebase
    └── sonarqube-setup-troubleshooting.md   # Common issues + fixes
```

---

## Exercise Acceptance Criteria (Detailed)

### Exercise 1: Code Assessment (Decision Track)

**Behavioral Specification:**
- Learner receives a 25–30 LOC legacy function with ≥3 debt markers
- Learner completes decision track assessment worksheet
- Assessment evaluates: code smell patterns, complexity metrics, team capacity, SonarQube violations

**Acceptance Criteria (PASS):**
- ✅ Correctly identifies ≥2 refactor blockers (documented with constitution law refs)
- ✅ Correctly identifies ≥1 rewrite indicator (documented with constitution law refs)
- ✅ Decision recommendation (refactor vs. rewrite) is justified with ENG-3.1/ENG-14/BUS-7.1 citations
- ✅ Assessment template is completed with ≥80% detail (all sections filled, law refs included)

**Assessment Method:** Facilitator review + learner self-check (guided)  
**Time:** 30 minutes (5 min intro, 20 min work, 5 min debrief)

---

### Exercise 2: Refactor via Atomic TDD

**Behavioral Specification:**
- Learner receives failing test suite (RED state)
- Learner implements minimal code to pass (GREEN state)
- Learner refactors while keeping tests green (REFACTOR state)

**Acceptance Criteria (PASS):**
- ✅ All tests pass (GREEN phase complete)
- ✅ Code complexity decreased (cyclomatic complexity, lines per function, etc.)
- ✅ SonarQube HARD_BLOCK gate passes (ENG-6.1, ENG-6.4, ENG-6.7)
- ✅ At least one refactoring technique applied (extract function, remove duplication, improve naming)
- ✅ Commits follow atomic TDD pattern: RED → GREEN → REFACTOR
- ✅ Test pyramid targets met: 80–90% unit tests, 10–20% integration

**Assessment Method:** Automated (tests + SonarQube gates) + Facilitator code review  
**Time:** 45 minutes (5 min intro, 30 min work, 10 min review)

---

### Exercise 3: Refactor or Rewrite (Legacy Rescue Path)

**Behavioral Specification:**
- Learner receives specification document
- Learner writes failing test (RED) that validates the spec
- Learner implements feature to pass test (GREEN)
- Learner refactors while keeping tests green (REFACTOR)

**Acceptance Criteria (PASS):**
- ✅ Spec is understood (learner articulates feature behavior in own words)
- ✅ Tests verify specification compliance (RED → GREEN → REFACTOR cycle)
- ✅ Feature builds & compiles without errors
- ✅ All tests pass
- ✅ SonarQube HARD_BLOCK gate passes (ENG-6.1, ENG-6.4, ENG-6.7)
- ✅ Contract test included (API signatures match spec, ENG-4.6)
- ✅ Code follows style guidelines (no lint violations)
- ✅ Test pyramid targets met: 70–80% unit, 15–25% integration (contract tests required)

**Assessment Method:** Automated (tests + SonarQube gates) + Facilitator integration test review  
**Time:** 60 minutes (5 min intro, 45 min work, 10 min review)

---

### Exercise 4: Full Workflow Execution

**Behavioral Specification:**
- Learner receives realistic legacy codebase with:
  - Existing code with ≥5 technical debt markers
  - ≥1 new feature request
  - SonarQube baseline scan (pre-refactor state)
- Learner applies decision track assessment
- Learner chooses workflow: refactor existing code OR rewrite OR implement feature development
- Learner executes chosen workflow
- Learner validates with SonarQube gates

**Acceptance Criteria (PASS) — Decision Track:**
- ✅ Assessment worksheet complete (same rubric as Ex 1)
- ✅ Justification for chosen workflow (refactor/rewrite/feature development)
- ✅ Constitutional law citations (ENG-3.1, ENG-14, BUS-7.1)

**Acceptance Criteria (PASS) — Refactor Path:**
- ✅ All Ex 2 criteria apply (TDD, complexity reduction, SonarQube gates)
- ✅ ≥2 code sections refactored
- ✅ Pre/post SonarQube scans compared (improvement in non-negotiable laws)

**Acceptance Criteria (PASS) — Rewrite Path:**
- ✅ Identifies code sections for rewrite (with justification)
- ✅ Implements feature development replacement code
- ✅ Replaces old code with new code + passes tests
- ✅ SonarQube gates pass on new code

**Acceptance Criteria (PASS) — Feature Development Path:**
- ✅ Feature specification written
- ✅ New feature passes Ex 3 criteria (spec-driven, tests, SonarQube gates)
- ✅ Feature integrates with existing codebase (no conflicts)

**Assessment Method:** Facilitator review of decision + code review of implementation  
**Time:** 105 minutes (15 min setup, 15 min assessment, 60 min implementation, 15 min review)  
**Audit Trail Requirement:** Git commits + SonarQube evidence

---

## Phase Acceptance Criteria

### Phase 1: Exercise Codebase Scaffolding & Content
- [ ] `hangar-ai-constitution-workflows` repo created with README, SETUP, exercises/ structure
- [ ] Ex 1–4 skeleton + instructions created with per-exercise acceptance criteria (detailed above)
- [ ] 4 SonarQube projects created on sonarqube.aa.com (ex1, ex2, ex3, ex4)
- [ ] HARD_BLOCK gates configured per SonarQube Gate Configuration section (thresholds verified)
- [ ] Exercise validation scripts created (each exercise has a `validate.sh` or `pytest` check)
- [ ] All exercises tested with reference solution; time estimates validated (within budgets)
- [ ] SonarQube token management documented; secure distribution plan in place

### Phase 2: Part 1 Materials
- [ ] 4 Part 1 slideware decks created (workflows, decision track, atomic TDD, feature development + avatars + gates)
- [ ] Part 1 facilitator guide created with learning objectives, talking points, stumbling blocks, law/skill callouts
- [ ] Part 1 learner guides embedded in exercise READMEs with prompts (constitutional callouts, RED/GREEN/REFACTOR guidance, avatar context questions)
- [ ] Facilitator validation rubric created (0–4 scoring per exercise)
- [ ] All law IDs verified against constitution (ENG-3.1, ENG-4.1, ENG-4.2, ENG-4.6, ENG-6.1/6.4/6.7, ENG-7.x, ENG-11.1, ENG-14, PRD-2.x, BUS-7.1)
- [ ] All skill IDs verified against constitution
- [ ] Test pyramid targets documented (unit/integration/E2E per exercise)
- [ ] 50% token savings applied vs. constitution originals (or justified exceptions)

### Phase 3: Part 2 Materials
- [ ] Part 2 slideware decks created (real codebase setup, SonarQube provisioning, decision flowchart, avatar enrichment)
- [ ] Part 2 facilitator guide created (codebase eligibility checklist, repo provisioning, contingency handling, recovery paths)
- [ ] Part 2 learner worksheets created (assessment checklist, decision matrix, avatar context template, SonarQube gate tracker, audit trail template)
- [ ] Avatar enrichment guide created (how to extract business/tech/product context from codebase)
- [ ] SonarQube project provisioning template created for Part 2 participants
- [ ] Shared AA SonarQube projects provisioned with role-based access (facilitators: admin, participants: analyst)
- [ ] Fallback sample codebase prepared (Ex 4 mini-app for participants whose codebases fail eligibility)

### Phase 4: Integration & Governance Review
- [ ] All materials linked from constitution README (exercises discoverable from workflows)
- [ ] Constitution linter clean (100% law/skill/workflow citations verified)
- [ ] Audit trail templates created + storage location documented
- [ ] Governance review session completed (architect + critic + test-architect roles; all 12 conditions addressed)
- [ ] All non-negotiable laws (ENG-4.1, ENG-6.1/6.4/6.7, BUS-7.1) have explicit enforcement evidence in exercises
- [ ] Decision track exercise (Ex 1 & 4) demonstrates all three paths (refactor, rewrite, feature development)
- [ ] Success metrics baseline established (workshop targeting ≥80% participant success rate)

---

## Success Metrics

### Participant Success Metrics

| Metric | Target | Measurement | Rationale |
|--------|--------|-------------|-----------|
| **Part 1 Completion Rate** | ≥90% of participants finish all 4 exercises | Facilitator checklist + exercise validation logs | Baseline: Can learners complete exercises in time? |
| **SonarQube Gate Pass Rate** | ≥85% of participants pass HARD_BLOCK gates on non-negotiable laws (ENG-4.1, ENG-6.1/6.4/6.7, BUS-7.1) | SonarQube project reports + facilitator logs | Core competency: Can learners meet compliance? |
| **Exercise Acceptance Rate** | ≥80% of participants achieve PASS status on Ex 1, 2, 3 per acceptance criteria | Facilitator rubric scoring | Learning validation: Do they understand workflows? |
| **Part 2 Application Rate** | ≥75% of participants bring real codebases to Part 2 | Participant registration + SonarQube project provisioning | Real-world relevance: Will they apply this? |
| **Part 2 Completion Rate** | ≥85% of participants complete assessment + choose + execute workflow | Facilitator logs + SonarQube gate reports | Engagement: Do they stay through Part 2? |
| **Decision Track Accuracy** | ≥80% of participants justify workflow choice with ≥1 constitutional law reference | Assessment worksheet review | Governance understanding: Do they cite laws? |
| **Post-Workshop Survey** | ≥80% "strongly agree": "I can now apply one of the 5 workflows to my own codebase" | Post-workshop survey (5-point scale) | Practical utility: Did they learn? |

### Facilitator Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Facilitator Readiness** | Facilitator passes dry-run with ≥90% slide accuracy + ≤5% timing variance | Dry-run + time logs |
| **Facilitator Intervention Rate** | ≤2 interventions per participant during Part 1; ≤3 during Part 2 | Facilitator notes |
| **Material Clarity** | Part 1 & Part 2 slideware scored ≥4/5 on clarity by 2 independent reviewers | Expert review rubric |

### Workshop Success Criteria

**SUCCESS THRESHOLD:** ≥80% of participants pass ≥5 of 7 participant metrics above.  
**FAILURE THRESHOLD:** <60% of participants pass ≥5 metrics → workshop requires revision before next delivery.

---

## Law Coverage

**Non-negotiable laws (must have enforcement in exercises):**
- `ENG-4.1` (Atomic TDD) — Ex 2, Ex 3, Ex 4 (RED → GREEN → REFACTOR explicitly practiced)
- `ENG-6.1` (Audit Trail) — Ex 4 (git commits + SonarQube evidence tracked)
- `BUS-7.1` (Decision Governance) — Ex 1 (decision track assessment), Ex 4 (path choice documented)

**Phase-gate laws:**
- `ENG-4.6` (Integration Testing) — Ex 3, Ex 4
- `ENG-11.1` (Spec-Driven Development) — Ex 3, Ex 4 (specs guide code)

**Engineering laws:**
- `ENG-3.1` (Technical Debt) — Ex 1, Ex 2, Ex 4
- `ENG-7.x` (API Design) — Ex 3, Ex 4
- `ENG-14` (Technical Debt Governance) — Ex 1, Ex 4

**Product laws:**
- `PRD-2.x` (Problem Framing) — Ex 4 (avatar context extraction)
- `PRD-3.x` (User Research) — Discussion prompts in Ex 4

**Avatar enrichment:**
- **Ex 1:** No avatar context (pure code assessment)
- **Ex 2:** Tech avatar (refactor constraints, design patterns)
- **Ex 3:** Tech + Product avatars (feature spec, API design for product goals)
- **Ex 4:** Business + Tech + Product avatars (full context from learner's own codebase)

---

## Facilitator Validation Rubric

**Per-Exercise Scoring (0–4 points each):**

| Criterion | 0 (Incorrect) | 1 (Partial) | 2 (Approaching) | 3 (Proficient) | 4 (Advanced) |
|-----------|---|---|---|---|---|
| **Exercise Understanding** | Learner cannot explain learning objective | Learner articulates objective vaguely | Learner explains objective but misses 1 key concept | Learner clearly explains objective + 1 supporting concept | Learner explains objective + 2+ supporting concepts with examples |
| **Law/Skill Citation** | No law/skill cited | 1 law/skill cited correctly | 2 laws/skills cited correctly | 3+ laws/skills cited correctly with explanation | 3+ laws/skills cited with explanation + connections between them |
| **Acceptance Criteria** | Does not meet any criteria | Meets 1 of 3+ criteria | Meets 2 of 3+ criteria | Meets 3–4 of 3+ criteria | Meets all criteria + exceeds in ≥1 area |
| **SonarQube Gate Status** | HARD_BLOCK violations remain | 1 gate passed, violations in 2+ gates | 2 gates passed, 1 violation remains | All HARD_BLOCK gates passed | All gates passed + quality metrics improved |

**Scoring Scale:**
- **16–20 points:** PASS (meets proficiency)
- **12–15 points:** CONDITIONAL PASS (meets minimum, needs follow-up)
- **<12 points:** FAIL (does not meet proficiency; recommend remediation)

**Facilitator Scoring:** Completed immediately after each exercise, shared with learner as formative feedback.

---

## Part 2: Real Codebase Specification

### Codebase Eligibility Criteria

**Required Properties:**
- ✅ **Size:** ≥500 LOC (demonstrable scope for decision track + workflow execution)
- ✅ **Complexity:** ≥1 existing SonarQube violation in non-negotiable laws (ENG-4.1, ENG-6.1/6.4/6.7, BUS-7.1)
  - Rationale: Learners must see real governance challenges, not toy code
- ✅ **Maturity:** ≥1 existing test suite (demonstrates refactor/feature development familiarity)
- ✅ **Language:** Supported by SonarQube (Java, Python, JavaScript, C#, Go, etc.)
- ✅ **Source Control:** Git repository with ≥5 commits (demonstrable history)

**Optional (Nice to Have):**
- Existing technical debt markers (comments like `// TODO`, `// HACK`, `// FIXME`)
- Mixed paradigm code (procedural + OO + functional) for refactor motivation
- Multiple modules/files (for scaling decisions)

**Disqualifying Factors:**
- ❌ <500 LOC (too simple for meaningful assessment)
- ❌ 0 SonarQube violations in non-negotiable laws (no governance learning)
- ❌ No tests (prevents safe refactoring)
- ❌ Unsupported language (SonarQube cannot scan)
- ❌ Proprietary/confidential code (security risk on shared SonarQube instance)

---

### Part 2 SonarQube Onboarding Workflow

**Timeline:** Part 2 onboarding occurs **48 hours before workshop session** (allows time for SonarQube scan)

**Step 1: Codebase Eligibility Check (Participant)**
- Participant completes eligibility checklist (size, complexity, language, source control)
- Facilitator reviews submission; confirms eligibility or suggests fallback codebase

**Step 2: SonarQube Project Provisioning (Facilitator)**
- Facilitator creates SonarQube project: `hangar-ai-constitution-workflows-part2-{participant-id}`
- Assigns participant as "analyst" role (can view results, not modify gates)
- Assigns facilitators as "admin" role (can modify gates, document exceptions)

**Step 3: Initial Scan (Participant)**
- Participant pushes codebase to SonarQube via sonar-scanner CLI
- Command template provided: `sonar-scanner -Dsonar.projectKey=... -Dsonar.token=$SONARQUBE_TOKEN`
- Token distributed securely (env var, not in script)
- Scan results available within 10 minutes

**Step 4: Baseline Assessment (Facilitator)**
- Facilitator reviews SonarQube baseline report
- Documents HARD_BLOCK violations in non-negotiable laws
- Confirms participant is ready for Part 2 (or identifies pre-work if needed)

---

### Part 2 Failure Recovery Path

**Scenario 1: Codebase fails HARD_BLOCK gates before workshop**
- **Recovery:** Participant has two options:
  1. **Remediate:** Fix HARD_BLOCK violations before Part 2 (with facilitator guidance)
  2. **Fallback:** Use provided sample codebase (same Ex 4 mini-app from Part 1) + add custom feature
- **Timing:** Remediation must complete ≥24 hours before Part 2 start

**Scenario 2: Codebase is too small (<500 LOC)**
- **Recovery:** Combine multiple repos into monorepo OR use fallback sample codebase

**Scenario 3: Codebase is proprietary/confidential**
- **Recovery:** Use fallback sample codebase (no IP risk)

**Scenario 4: Language unsupported by SonarQube**
- **Recovery:** Facilitate port to supported language (Python/JavaScript) OR use fallback codebase

---

### Facilitator Support Model (Part 2)

**1:1 Pairing Ratio:** 1 facilitator : 4–6 participants (adjusted based on codebase complexity)

**Support Phases:**

| Phase | Duration | Activity | Support Type |
|-------|----------|----------|---|
| **Setup** | 30 min | SonarQube provisioning + baseline scan | Synchronous (facilitator-led) |
| **Assess** | 30 min | Decision track assessment on own codebase | Pair support (facilitator observes, coaches on law interpretation) |
| **Execute** | 60 min | Workflow execution (refactor/rewrite/feature development) | On-demand coaching (facilitator available for questions; asynchronous Slack channel for pairing support) |
| **Gate Check** | 15 min | SonarQube gate validation + exception documentation | Synchronous (facilitator approves HARD_BLOCK exceptions per ENG-6.1) |
| **Debrief** | 15 min | Group reflection on governance trade-offs | Synchronous (facilitator-led discussion) |

**Escalation Triggers:**
- Participant blocks on language/tooling issue → facilitator 1:1 call
- Participant rejects SonarQube HARD_BLOCK verdict → facilitator + law review (cite ENG-6.1 exception process)
- Participant abandons workflow execution → facilitator check-in + support reset

---

## SonarQube Gate Configuration

### HARD_BLOCK Gate Definitions

**For Exercises 1–3 (ENG-6.1, ENG-6.4, ENG-6.7):**

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| **Code Smells (ENG-6.4)** | BLOCK if > 5 major, any critical | Maintainability gate |
| **Security Hotspots (ENG-6.7)** | BLOCK if any critical, >3 major | Security gate |
| **Duplicated Lines (ENG-6.1)** | BLOCK if > 20% duplication | Auditability gate |
| **Cognitive Complexity per Function** | BLOCK if > 10 | Testability gate |
| **Test Coverage** | BLOCK if < 70% (Ex 2) or < 80% (Ex 3) | Confidence gate |

**For Exercise 4 (ENG-4.6, ENG-11.1):**

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| **Integration Tests** | BLOCK if < 15% of test count | Contract fulfillment gate |
| **Spec Compliance** | BLOCK if spec not implemented | Behavioral specification gate |

---

### Gate Sequence (Workflow Execution)

**Ex 2 Refactor Sequence:**
1. RED: Write failing test (manual check: test fails before implementation)
2. GREEN: Implement minimal code (SonarQube gate runs; must pass)
3. REFACTOR: Improve design (SonarQube gate runs; must pass)

**Ex 3 Feature Development Sequence:**
1. RED: Write failing test against spec (manual check: test fails before implementation)
2. GREEN: Implement feature (SonarQube gate runs; must pass)
3. REFACTOR: Improve design (SonarQube gate runs; must pass)

**Ex 4 Workflow Sequence (depends on chosen path):**
- **Refactor path:** Follow Ex 2 sequence
- **Feature development path:** Follow Ex 3 sequence
- **Rewrite path:** Same as feature development (new code must satisfy gates)

---

## Audit Trail Design

### Audit Trail Logging Requirements

**Per-Exercise Audit Trail Template:**

```markdown
## Exercise 1 Audit Trail — Code Assessment

**Learner:** [Name]  
**Date/Time:** [Start time] → [End time] (duration: XX min)  
**Facilitator:** [Name]  

### Assessment Worksheet
- Debt markers identified: [count] ✅
- Law citations (ENG-3.1, ENG-14): [count] ✅
- Decision recommendation: [refactor/rewrite/hybrid] ✅
- Justification quality (facilitator rubric): [0–4 points] ✅

### Outcome
- Status: PASS / CONDITIONAL PASS / FAIL
- Feedback: [Facilitator notes]
- Learner signature: [Acknowledgment]

### Governance Compliance
- BUS-7.1 (Decision Governance): ✅ Decision documented & justified
- ENG-3.1 (Technical Debt): ✅ Debt assessed per law
- ENG-14 (Technical Debt Governance): ✅ Governance applied
```

**For Exercises 2–4:**

```markdown
## Exercise [N] Audit Trail

**Learner:** [Name]  
**Date/Time:** [Start] → [End] (duration: XX min)  
**Facilitator:** [Name]  

### Execution Summary
- Test count (initial): [N]
- Commits (RED → GREEN → REFACTOR): [commit hashes]
- SonarQube scan (pre-refactor): [violations]
- SonarQube scan (post-refactor): [violations]
- HARD_BLOCK gates passed: ✅ [gate names]

### Test Pyramid Verification
- Unit tests: [count] ([%] of total)
- Integration tests: [count] ([%] of total)
- Coverage: [X%]
- Target met: ✅ YES / ❌ NO

### Code Quality
- Complexity reduced: [before] → [after] ✅
- Duplication removed: [before] → [after] ✅
- Maintainability improved: [assessment] ✅

### Governance Compliance
- ENG-4.1 (Atomic TDD): ✅ RED/GREEN/REFACTOR cycle evident
- ENG-4.2 (Test Pyramid): ✅ Targets met
- ENG-6.1/6.4/6.7 (Audit/Compliance): ✅ Gates passed
- Audit trail complete: ✅ All steps logged

### Outcome
- Status: PASS / CONDITIONAL PASS / FAIL
- Feedback: [Facilitator notes]
- Learner signature: [Acknowledgment]
```

**Storage:** Audit trails stored in workshop repo `hangar-ai-constitution-workflows/audit-logs/` (one file per learner per exercise)

**Retention:** Audit trails retained for 12 months (governance + learning analytics)

**Compliance Check:** Pre-workshop review confirms audit trail template + storage location are ready

---

## Decision Track Framework

### Decision Track Assessment Criteria

| Category | Refactor Indicator | Rewrite Indicator | Neutral |
|----------|---|---|---|
| **Code Complexity** | <10 cyclomatic complexity per function; <50 lines per function | >20 cyclomatic complexity; >100 lines per function | 10–20 complexity; 50–100 lines |
| **Test Coverage** | ≥70% existing coverage | <30% existing coverage | 30–70% coverage |
| **Code Smell Density** | <10 SonarQube violations in non-negotiable laws | >50 SonarQube violations in non-negotiable laws | 10–50 violations |
| **Tech Debt Concentration** | Debt scattered across multiple functions | Debt concentrated in 1–2 large functions | Moderate distribution |
| **Refactor Feasibility** | ≥3 refactor patterns applicable (extract method, remove duplication, improve naming) | <1 applicable pattern; structure fundamentally flawed | 1–2 patterns applicable |
| **Team Capacity** | Team ≥3 engineers, >1 year tenure | Team <2 engineers, <3 months tenure | Team 2–3 engineers, 3–12 months tenure |
| **Timeline** | Can refactor in <2 sprints | Requires >3 sprints or new hire | 2–3 sprint estimate |
| **Risk Tolerance** | Low-risk changes (< 10% change surface area) | High-risk rewrite (>50% change surface area) | Medium risk (10–50%) |

### Decision Matrix Template (Learner Worksheet)

```markdown
## Decision Track Assessment — Refactor vs. Rewrite

### Codebase: [Name]  
### Assessed by: [Learner name]  
### Date: [Date]  

### Scoring (1 = Refactor, 5 = Rewrite)

| Criterion | Score (1–5) | Justification | Law Reference |
|-----------|-----------|---|---|
| Complexity | [1–5] | [Why?] | ENG-3.1 |
| Test Coverage | [1–5] | [Why?] | ENG-4.2 |
| Violations | [1–5] | [Why?] | ENG-6.1/6.4/6.7 |
| Pattern Density | [1–5] | [Why?] | ENG-14 |
| Feasibility | [1–5] | [Why?] | BUS-7.1 |
| Team Capacity | [1–5] | [Why?] | BUS-2.2 |
| Timeline | [1–5] | [Why?] | PRD-2.2 |
| Risk | [1–5] | [Why?] | BUS-7.1 |

**Total Score:** [Sum] / 40  
**Average:** [Sum / 8] / 5  

### Recommendation

**If average 1–2.5:** REFACTOR ✅  
**If average 2.5–3.5:** HYBRID (refactor + feature development) ⚠️  
**If average 3.5–5:** REWRITE 🔄  

### Decision Justification

[Learner writes: Why did you choose refactor/rewrite?]
- Strongest indicator: [which criterion most influenced decision?]
- Risk mitigation: [how would you reduce risk?]
- Law alignment: [which laws guide this decision?]

### Facilitator Review
- Assessment completeness: ✅
- Law citations: ✅
- Decision justified: ✅
- Facilitator signature: ___________
```

---

## Test Pyramid Targets

### Exercise 2: Refactor via TDD

**Test Pyramid Target:**
- Unit tests: 80–90% (isolated function tests)
- Integration tests: 10–20% (module interaction tests)
- E2E tests: 0–5% (not required for refactor of single function)

**Validation:** After Ex 2 completion, run test coverage tool (e.g., `nyc` for JavaScript, `coverage.py` for Python) and verify distribution.

---

### Exercise 3: Feature Development Workflow

**Test Pyramid Target:**
- Unit tests: 70–80% (feature logic, edge cases)
- Integration tests: 15–25% (feature + existing code interaction, API contract tests)
- E2E tests: 5–10% (feature end-to-end flow, if applicable)

**Contract Test Requirement:** ≥1 contract test verifying API surface (function signature, parameters, return type) matches specification.

**Example Contract Test:**
```javascript
// Example: ES6 feature contract test
describe('getUser contract', () => {
  it('returns user object with id, name, email', () => {
    const result = getUser(123);
    expect(result).toHaveProperty('id');
    expect(result).toHaveProperty('name');
    expect(result).toHaveProperty('email');
    expect(result.id).toBe(123);
  });
});
```

**Validation:** Contract test included in Ex 3 skeleton; learner must implement feature to satisfy contract + other tests.

---

### Exercise 4: Full Workflow Execution

**Test Pyramid Target Depends on Chosen Path:**
- **Refactor path:** Follow Ex 2 targets (80–90% unit, 10–20% integration)
- **Rewrite path:** Follow Ex 3 targets (70–80% unit, 15–25% integration, 5–10% E2E)
- **Feature development path:** Follow Ex 3 targets (same as rewrite)

---

## Blockers / Risks

### Blocker 1: Phase 9 Dependency Verification

**Risk:** `constitution-workflow-governance-evolution` Phase 9 (SonarQube integration) must be merged before Phase 1 kickoff.

**Mitigation:**
- **Action:** Verify Phase 9 merge status **before March 31, 2026** (today)
- **Confirmation checklist:**
  - [ ] Branch is merged to main
  - [ ] 4 test SonarQube projects created: ex1, ex2, ex3, ex4
  - [ ] HARD_BLOCK gates configured per law mapping
  - [ ] Token access tested (sonar-scanner CLI works with env var)

**Contingency Plan (If Phase 9 is Delayed):**

**Option A: Delay hangar-ai-constitution-workflows Phase 1 by 1 week** (RECOMMENDED)
- Add 1-week buffer to timeline
- New timeline: 5–7 weeks (instead of 4–6)
- Proceed once Phase 9 is confirmed merged

**Option B: Manual SonarQube Setup (Temporary)**
- Facilitators manually provision SonarQube projects without Phase 9 automation
- Create gate definitions from Phase 9 PROPOSAL.md (if needed)
- Extra work for facilitators; no impact to learner experience
- Plan to migrate to Phase 9 automation before Part 2 begins

**Preferred:** Option A (delay + ensure Phase 9 quality)

---

### Blocker 2: SonarQube Token Access

**Risk:** Shared AA SonarQube instance requires token for CI/local execution; distribution must be secure.

**Mitigation:** 
- Use `.env.example` in repo (token placeholder; never committed)
- Document secure setup in SETUP.md (env var-based access)
- Facilitators distribute token pre-workshop via secure channel (1Password, email with short TTL, etc.)
- Token rotated after workshop completion

---

### Blocker 3: Language Choice for Exercises

**Risk:** Exercises must be language-agnostic OR pick a canonical language.

**Decision:** Start with **Node.js** (quick, accessible, modern JavaScript)
- Rationale: Low barrier to entry, no installation complexity, works on all OSes
- Mitigation: Provide porting guides (Python, Java) in docs for teams with different stacks
- Framework: Vanilla Node.js + Jest (no heavy frameworks; pure TDD/governance practice)

---

### Blocker 4: Exercise Complexity Balance

**Risk:** Too simple → learners don't see real governance challenges; too complex → time overruns.

**Mitigation:**
- Time-box each exercise rigorously (Ex 1: 30 min, Ex 2: 45 min, Ex 3: 60 min, Ex 4: 105 min)
- Facilitator guide includes "stretch goals" for fast learners
- Reference solutions provided for context + time recovery

---

### Blocker 5: Avatar Enrichment Mechanics

**Issue:** How are avatars assigned? What triggers progression? How does avatar level affect exercises?

**Resolution:**

**Avatar Enrichment Model:**

| Exercise | Avatar Context | How It's Introduced | Impact on Exercise |
|----------|---|---|---|
| **Ex 1** | None | Pure code assessment (no business/product context) | Decision is code-driven only |
| **Ex 2** | **Tech Avatar** | Facilitator provides: "This codebase runs on Node.js; legacy patterns are callback-heavy" | Refactor strategy considers tech constraints (async/await vs. callbacks) |
| **Ex 3** | **Tech + Product Avatars** | Facilitator provides spec including business goal ("improve performance for mobile users") + tech constraint | Feature development implementation considers both user needs + platform constraints |
| **Ex 4** | **Business + Tech + Product** | Learners extract from own codebase: business goals, tech stack, user needs | Decision track assessment + workflow choice consider full context |

**Why This Matters:**
- Learners see how different stakeholder perspectives (business, tech, product) influence workflow decisions
- Real-world codebase decisions are never code-only; context matters
- Avatar enrichment anchors decisions to constitution's BUS-7.1 (Decision Governance) and PRD-2.x (Problem Framing)

---

### Blocker 6: Real Codebase Scope (Part 2)

**Risk:** Participant codebases vary wildly (monoliths vs. microservices, legacy vs. modern).

**Mitigation:** See **Part 2: Real Codebase Specification** section above (eligibility criteria + recovery paths).

---

## Success Metrics

- ✅ All exercises executable in ≤ time budgets (Ex 1: 30 min, Ex 2: 45 min, Ex 3: 60 min, Ex 4: 105 min)
- ✅ 100% of law/skill citations verified against constitution
- ✅ SonarQube gates enforce 2+ non-negotiable laws per exercise
- ✅ Facilitator guide covers decision track with ≥5 real-world scenarios (when to refactor, when to rewrite, etc.)
- ✅ Learner worksheets (Part 2) capture ≥80% of participant assessments + SonarQube gate results
- ✅ Post-workshop survey: "I can now apply one of the 5 workflows to my own codebase" — ≥80% "strongly agree"

---

## Phase Breakdown

| Phase | Deliverable | Owner | Duration | Gate | Blockers |
|-------|-------------|-------|----------|------|----------|
| 1 | Exercise scaffolding, skeleton code, SonarQube setup | Engineering | 1 week | Exercise validation (all 4 run successfully) | SonarQube token access |
| 2 | Part 1 slideware + facilitator guide + learner prompts | Content | 1 week | Content review (all laws/skills verified) | Language/exercise complexity decisions |
| 3 | Part 2 slideware + facilitator guide + worksheets | Content | 1 week | Content review + SonarQube project setup | Real codebase scope clarity |
| 4 | Governance review + constitution integration | Governance | 3 days | Gov review (ENG-4.x, BUS-7.1, PRD-2.x pass) | Completion of Phases 1–3 |

---

## Dependency Chain

```
constitution-workflow-governance-evolution
  ↓ (must complete + merge first)
hangar-ai-constitution-workflows
  ├─ Phase 1: Exercise scaffolding (can start before governance evolution lands)
  │   └─ Depends on: SonarQube token, language decision
  ├─ Phase 2: Part 1 materials (depends on Phase 1 + workflows defined)
  ├─ Phase 3: Part 2 materials (depends on Phase 1 + SonarQube setup)
  └─ Phase 4: Governance review (depends on Phases 1–3)
```

---

## Open Questions for Governance Review

1. **Language canonical choice:** Should exercises be Node.js-first with porting guides, or language-agnostic from day one?
2. **SonarQube exception handling:** How much detail on "when to document exception" per ENG-6.1? (decision tree in facilitator guide?)
3. **Avatar enrichment depth:** Should learners extract avatars from their own codebases in Part 2, or is facilitator-provided avatar context sufficient?
4. **Token optimization:** Should this codebase follow the token-optimization practices from the governance evolution proposal (limit example sizes)?
5. **Feature development build scope:** Should Ex 3 ask learners to build a feature, or just spec it out? (Time implications?)

---

## Next Steps if Approved

1. Request governance review session with architect + sentinel roles
2. Create repo: `hangar-ai-constitution-workflows` in governance folder
3. Begin Phase 1 implementation (exercise scaffolding)
4. Proceed with phased rollout (1–2 weeks per phase)
5. Target first workshop delivery after Phase 4 completion + team manual testing

