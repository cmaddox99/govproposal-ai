# Governance Review Remediation — hangar-ai-constitution-workflows

**Session ID:** gov-5e6476f70cd2  
**Review Date:** March 31, 2026  
**Verdict:** CONDITIONAL (12 conditions to address)  
**Roles:** Architect, Critic, Test Architect

---

## Executive Summary

The proposal demonstrates **strong foundational design** (workflows, exercises, SonarQube integration, law coverage). However, three critical areas lack specificity:

1. **Exercise acceptance criteria** — what counts as "passing" each exercise?
2. **Workshop success metrics** — how do we measure learning outcomes?
3. **Part 2 real codebase specification** — what are the requirements for participant repos?

Additionally, four governance gaps require clarification:
- Avatar enrichment mechanics (unverified)
- Phase 9 dependency status (verification needed)
- SonarQube gate configuration (explicit thresholds needed)
- Audit trail design (non-negotiable law enforcement)

Below are responses to all 12 conditions, mapped to the three roles.

---

## ARCHITECT REMEDIATIONS (3 CONDITIONS)

### Condition 1: Exercise Acceptance Criteria (ENG-2.1)

**Issue:** Proposal describes what exercises teach, but not testable pass/fail criteria.

**Remediation:**

#### Exercise 1: Code Assessment (Decision Track)

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

#### Exercise 2: Refactor via Atomic TDD

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

**Assessment Method:** Automated (tests + SonarQube gates) + Facilitator code review

**Time:** 45 minutes (5 min intro, 30 min work, 10 min review)

**Test Pyramid Target:** 70–80% unit tests, 15–25% integration, 5–10% E2E (if applicable)

---

#### Exercise 3: Greenfield Feature (Spec-Driven)

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

**Assessment Method:** Automated (tests + SonarQube gates) + Facilitator integration test review

**Time:** 60 minutes (5 min intro, 45 min work, 10 min review)

**Test Pyramid Target:** 80% unit, 20% integration (contract tests required)

**Contract Test Requirement:** Ex 3 must include ≥1 contract test verifying API surface matches spec

---

#### Exercise 4: Full Workflow Execution

**Behavioral Specification:**
- Learner receives realistic legacy codebase with:
  - Existing code with ≥5 technical debt markers
  - ≥1 new feature request
  - SonarQube baseline scan (pre-refactor state)
- Learner applies decision track assessment
- Learner chooses workflow: refactor existing code OR rewrite OR implement greenfield feature
- Learner executes chosen workflow
- Learner validates with SonarQube gates

**Acceptance Criteria (PASS) — Decision Track:**
- ✅ Assessment worksheet complete (same rubric as Ex 1)
- ✅ Justification for chosen workflow (refactor/rewrite/greenfield)
- ✅ Constitutional law citations (ENG-3.1, ENG-14, BUS-7.1)

**Acceptance Criteria (PASS) — Refactor Path:**
- ✅ All Ex 2 criteria apply (TDD, complexity reduction, SonarQube gates)
- ✅ ≥2 code sections refactored
- ✅ Pre/post SonarQube scans compared (improvement in non-negotiable laws)

**Acceptance Criteria (PASS) — Rewrite Path:**
- ✅ Identifies code sections for rewrite (with justification)
- ✅ Implements greenfield replacement code
- ✅ Replaces old code with new code + passes tests
- ✅ SonarQube gates pass on new code

**Acceptance Criteria (PASS) — Greenfield Feature Path:**
- ✅ Feature specification written
- ✅ New feature passes Ex 3 criteria (spec-driven, tests, SonarQube gates)
- ✅ Feature integrates with existing codebase (no conflicts)

**Assessment Method:** Facilitator review of decision + code review of implementation

**Time:** 105 minutes (15 min setup, 15 min assessment, 60 min implementation, 15 min review)

**Test Pyramid Target:** Same as chosen path (refactor = Ex 2 targets; greenfield = Ex 3 targets)

**Audit Trail Requirement:** Git commits + SonarQube evidence (see Audit Trail Design section below)

---

### Condition 2: Workshop Success Metrics (PRD-1.2)

**Issue:** No quantitative targets for workshop outcomes.

**Remediation:**

#### Participant Success Metrics

| Metric | Target | Measurement | Rationale |
|--------|--------|-------------|-----------|
| **Part 1 Completion Rate** | ≥90% of participants finish all 4 exercises | Facilitator checklist + exercise validation logs | Baseline: Can learners complete exercises in time? |
| **SonarQube Gate Pass Rate** | ≥85% of participants pass HARD_BLOCK gates on non-negotiable laws (ENG-4.1, ENG-6.1/6.4/6.7, BUS-7.1) | SonarQube project reports + facilitator logs | Core competency: Can learners meet compliance? |
| **Exercise Acceptance Rate** | ≥80% of participants achieve PASS status on Ex 1, 2, 3 per acceptance criteria above | Facilitator rubric scoring | Learning validation: Do they understand workflows? |
| **Part 2 Application Rate** | ≥75% of participants bring real codebases to Part 2 | Participant registration + SonarQube project provisioning | Real-world relevance: Will they apply this? |
| **Part 2 Completion Rate** | ≥85% of participants complete assessment + choose + execute workflow (even if workflow incomplete) | Facilitator logs + SonarQube gate reports | Engagement: Do they stay through Part 2? |
| **Decision Track Accuracy** | ≥80% of participants justify workflow choice with ≥1 constitutional law reference | Assessment worksheet review | Governance understanding: Do they cite laws? |
| **Post-Workshop Survey** | ≥80% "strongly agree": "I can now apply one of the 5 workflows to my own codebase" | Post-workshop survey (5-point scale) | Practical utility: Did they learn? |

#### Facilitator Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Facilitator Readiness** | Facilitator passes dry-run with ≥90% slide accuracy + ≤5% timing variance | Dry-run + time logs |
| **Facilitator Intervention Rate** | ≤2 interventions per participant during Part 1; ≤3 during Part 2 | Facilitator notes |
| **Material Clarity** | Part 1 & Part 2 slideware scored ≥4/5 on clarity by 2 independent reviewers | Expert review rubric |

#### Workshop Success Criteria

**SUCCESS THRESHOLD:** ≥80% of participants pass ≥5 of 7 participant metrics above.

**FAILURE THRESHOLD:** <60% of participants pass ≥5 metrics → workshop requires revision before next delivery.

---

### Condition 3: Facilitator Validation Rubric (ENG-2.4)

**Issue:** "Facilitator validation" is subjective; no scoring framework.

**Remediation:**

#### Facilitator Validation Rubric

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

## CRITIC REMEDIATIONS (4 CRITICAL FINDINGS)

### Critical Finding 1: Workshop Success Criteria (PRD-1.2)

**Issue:** How do you measure participant competency, facilitator readiness, and material clarity?

**Remediation:** See **Architect Condition 2** above (Success Metrics) and **Condition 3** (Facilitator Validation Rubric).

---

### Critical Finding 2: Part 2 Real Codebase Specification (PRD-1.5)

**Issue:** Part 2 is underspecified. What counts as "valid"? How are projects onboarded? What's the support model?

**Remediation:**

#### Part 2 Codebase Eligibility Criteria

**Required Properties:**
- ✅ **Size:** ≥500 LOC (demonstrable scope for decision track + workflow execution)
- ✅ **Complexity:** ≥1 existing SonarQube violation in non-negotiable laws (ENG-4.1, ENG-6.1/6.4/6.7, BUS-7.1)
  - Rationale: Learners must see real governance challenges, not toy code
- ✅ **Maturity:** ≥1 existing test suite (demonstrates refactor/greenfield familiarity)
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

#### Part 2 SonarQube Onboarding Workflow

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

#### Part 2 Failure Recovery Path

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

#### Facilitator Support Model (Part 2)

**1:1 Pairing Ratio:** 1 facilitator : 4–6 participants (adjusted based on codebase complexity)

**Support Phases:**

| Phase | Duration | Activity | Support Type |
|-------|----------|----------|---|
| **Setup** | 30 min | SonarQube provisioning + baseline scan | Synchronous (facilitator-led) |
| **Assess** | 30 min | Decision track assessment on own codebase | Pair support (facilitator observes, coaches on law interpretation) |
| **Execute** | 60 min | Workflow execution (refactor/rewrite/greenfield) | On-demand coaching (facilitator available for questions; asynchronous Slack channel for pairing support) |
| **Gate Check** | 15 min | SonarQube gate validation + exception documentation | Synchronous (facilitator approves HARD_BLOCK exceptions per ENG-6.1) |
| **Debrief** | 15 min | Group reflection on governance trade-offs | Synchronous (facilitator-led discussion) |

**Escalation Triggers:**
- Participant blocks on language/tooling issue → facilitator 1:1 call
- Participant rejects SonarQube HARD_BLOCK verdict → facilitator + law review (cite ENG-6.1 exception process)
- Participant abandons workflow execution → facilitator check-in + support reset

---

### Critical Finding 3: Phase 9 Dependency Risk (ENG-12.1)

**Issue:** Phase 9 merge status unknown. If delayed, timeline collapses.

**Remediation:**

#### Phase 9 Status Verification Checklist

**BEFORE Phase 1 kickoff, confirm:**

- [ ] `constitution-workflow-governance-evolution` branch is merged to main
- [ ] Phase 9 commit(s) are in hangar-ai-constitution repo
- [ ] SonarQube integration (skill-sonarqube-compliance-gate) is active
- [ ] 4 test SonarQube projects created: ex1, ex2, ex3, ex4
- [ ] HARD_BLOCK gates configured per law mapping:
  - ENG-6.1, ENG-6.4, ENG-6.7 for ex1–3
  - ENG-4.6, ENG-11.1 for ex4
- [ ] Token access tested (sonar-scanner CLI works with env var)

**Contact:** hangar-ai-governance team (github.com/american-airlines/governance/AA-Hangar-AI-Constitution/issues)

---

#### Contingency Plan (If Phase 9 is Delayed)

**Scenario: Phase 9 merge slips past hangar-ai-constitution-workflows Phase 1 start**

**Option A: Delay hangar-ai-constitution-workflows Phase 1 by 1 week**
- Add 1-week buffer to timeline
- New timeline: 5–7 weeks (instead of 4–6)
- Proceed once Phase 9 is confirmed merged

**Option B: Manual SonarQube Setup (Temporary)**
- Facilitators manually provision SonarQube projects without Phase 9 automation
- Create gate definitions from Phase 9 PROPOSAL.md (if needed)
- Extra work for facilitators; no impact to learner experience
- Plan to migrate to Phase 9 automation before Part 2 begins

**Preferred:** Option A (delay + ensure Phase 9 quality) rather than Option B (workaround complexity)

**Decision Point:** March 31, 2026 (today) — confirm Phase 9 status to lock timeline

---

### Critical Finding 4: Avatar Enrichment Unverified (ENG-12.3)

**Issue:** Proposal claims "Progressive avatar enrichment" but does not specify mechanics.

**Remediation:**

**Decision:** Either specify OR remove from proposal.

#### Option A: Specify Avatar Enrichment (Recommended)

**Avatar Enrichment Model:**

| Exercise | Avatar Context | How It's Introduced | Impact on Exercise |
|----------|---|---|---|
| **Ex 1** | None | Pure code assessment (no business/product context) | Decision is code-driven only |
| **Ex 2** | **Tech Avatar** | Facilitator provides: "This codebase runs on Node.js; legacy patterns are callback-heavy" | Refactor strategy considers tech constraints (async/await vs. callbacks) |
| **Ex 3** | **Tech + Product Avatars** | Facilitator provides: spec includes business goal ("improve performance for mobile users") + tech constraint | Greenfield implementation considers both user needs + platform constraints |
| **Ex 4** | **Business + Tech + Product** | Learners extract from own codebase: business goals, tech stack, user needs | Decision track assessment + workflow choice consider full context |

**Avatar Extraction Template (Part 2, Ex 4):**

```markdown
## Avatar Context from Your Codebase

### Business Avatar
- Business goal: [what problem does this codebase solve?]
- Success metrics: [how is success measured?]
- Constraints: [what blocks investment?]

### Tech Avatar
- Tech stack: [languages, frameworks, platforms]
- Technical debt (if refactoring): [complexity pain points]
- Team capacity: [how large is the team? what's their skill level?]

### Product Avatar
- User needs: [who uses this code? what do they need?]
- Feature roadmap: [what's next?]
- Performance/scale constraints: [what's the load profile?]
```

**Why This Matters:**
- Learners see how different stakeholder perspectives (business, tech, product) influence workflow decisions
- Real-world codebase decisions are never code-only; context matters
- Avatar enrichment anchors decisions to constitution's BUS-7.1 (Decision Governance) and PRD-2.x (Problem Framing)

#### Option B: Remove Avatar Enrichment from Proposal

If Option A feels out of scope, remove from proposal and defer to future enhancement:
- Remove: "Progressive avatar enrichment (none → tech → tech+product → business+tech+product)"
- Simplify: "Exercises grounded in constitutional laws and skills; real codebase context introduced in Part 2"

**Recommendation:** Option A (keep + specify). Avatar enrichment is pedagogically powerful and aligns with constitution's emphasis on BUS/PRD laws.

---

## TEST ARCHITECT REMEDIATIONS (4 CONDITIONS)

### Condition 1: Test Pyramid Targets (ENG-4.2)

**Issue:** No test distribution targets specified (70–80% unit, 15–25% integration, 5–10% E2E).

**Remediation:**

#### Exercise 2: Refactor via TDD

**Test Pyramid Target:**
- Unit tests: 80–90% (isolated function tests)
- Integration tests: 10–20% (module interaction tests)
- E2E tests: 0–5% (not required for refactor of single function)

**Validation:** After Ex 2 completion, run test coverage tool (e.g., `nyc` for JavaScript, `coverage.py` for Python) and verify distribution.

---

#### Exercise 3: Greenfield Feature

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

#### Exercise 4: Full Workflow Execution

**Test Pyramid Target Depends on Chosen Path:**
- **Refactor path:** Follow Ex 2 targets (80–90% unit, 10–20% integration)
- **Rewrite path:** Follow Ex 3 targets (70–80% unit, 15–25% integration, 5–10% E2E)
- **Greenfield feature path:** Follow Ex 3 targets (same as rewrite)

---

### Condition 2: SonarQube Gate Configuration (ENG-4.9)

**Issue:** No explicit gate definitions (thresholds, blocking rules, sequence).

**Remediation:**

#### SonarQube HARD_BLOCK Gate Definitions

**For Exercises 1–3 (ENG-6.1, ENG-6.4, ENG-6.7):**

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| **Code Smells (ENG-6.4)** | BLOCK if > 5 major, any critical | Maintainability gate |
| **Security Hotspots (ENG-6.7)** | BLOCK if any critical, >3 major | Security gate |
| **Duplicated Lines (ENG-6.1)** | BLOCK if > 20% duplication | Auditability gate |
| **Cognitive Complexity per Function** | BLOCK if > 10 | Testability gate |
| **Test Coverage** | BLOCK if < 70% (Ex 2) or < 80% (Ex 3) | Confidence gate |

**For Exercise 4 (ENG-4.6, ENG-11.1):**

Add to above gates:
| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| **Integration Tests** | BLOCK if < 15% of test count | Contract fulfillment gate |
| **Spec Compliance** | BLOCK if spec not implemented | Behavioral specification gate |

---

#### Gate Sequence (Workflow Execution)

**Ex 2 Refactor Sequence:**
1. RED: Write failing test (manual check: test fails before implementation)
2. GREEN: Implement minimal code (SonarQube gate runs; must pass)
3. REFACTOR: Improve design (SonarQube gate runs; must pass)

**Ex 3 Greenfield Sequence:**
1. RED: Write failing test against spec (manual check: test fails before implementation)
2. GREEN: Implement feature (SonarQube gate runs; must pass)
3. REFACTOR: Improve design (SonarQube gate runs; must pass)

**Ex 4 Workflow Sequence (depends on chosen path):**
- **Refactor path:** Follow Ex 2 sequence
- **Greenfield path:** Follow Ex 3 sequence
- **Rewrite path:** Same as greenfield (new code must satisfy gates)

---

### Condition 3: Audit Trail Design (ENG-6.1, ENG-6.4, ENG-6.7 — NON-NEGOTIABLE)

**Issue:** How is compliance tracked? Who ran what exercise, when, with what results?

**Remediation:**

#### Audit Trail Logging Requirements

**Per-Exercise Audit Trail:**

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
## Exercise 2 Audit Trail — Refactor via TDD

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

### Condition 4: Decision Track Framework (BUS-7.1 — NON-NEGOTIABLE)

**Issue:** Decision track exercise (Ex 1) must include explicit decision criteria and trade-off templates.

**Remediation:**

#### Decision Track Framework for Exercise 1

**Decision Track Assessment Criteria:**

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

**Decision Matrix Template (Learner Worksheet):**

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
**If average 2.5–3.5:** HYBRID (refactor + greenfield feature) ⚠️  
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

## SUMMARY: REMEDIATION CHECKLIST

**Priority 1 (Blocking) — Complete before governance re-submission:**
- [ ] 1. Exercise acceptance criteria per exercise (with behavioral specs)
- [ ] 2. Workshop success metrics (quantitative targets)
- [ ] 3. Part 2 real codebase specification (eligibility + onboarding + recovery)
- [ ] 4. Phase 9 dependency verification (confirm merge status + contingency)
- [ ] 5. Avatar enrichment (specify OR remove)

**Priority 2 (High) — Complete before Phase 1 kickoff:**
- [ ] 6. Facilitator validation rubric (0–4 point scoring)
- [ ] 7. Test pyramid targets per exercise (unit/integration/E2E %)
- [ ] 8. SonarQube gate configuration (thresholds + gate sequence)
- [ ] 9. Audit trail design (logging + retention + compliance check)
- [ ] 10. Decision track framework (criteria matrix + decision template)
- [ ] 11. Contract test specifications (Ex 3 & Ex 4 templates)
- [ ] 12. Behavioral specs + acceptance criteria (in exercise READMEs)

---

## NEXT STEPS

1. **Add this REMEDIATION.md to the proposal directory**
2. **Update PROPOSAL.md** with remediation content (new sections + expanded acceptance criteria)
3. **Update tasks.md** with remediation-driven subtasks (gate configurations, audit trail setup, etc.)
4. **Confirm Phase 9 status** (merge date + SonarQube readiness)
5. **Re-submit for governance approval** with all 12 conditions addressed

**Timeline:** Remediation should take 1–2 weeks (mostly documentation + clarification, not implementation)

