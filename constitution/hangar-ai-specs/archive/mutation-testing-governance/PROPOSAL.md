# Proposal: Mutation Testing Governance — ENG-4.11 Law & Skill Implementation

**Proposal ID:** mutation-testing-governance  
**Submitted:** March 31, 2026  
**Status:** REVISION 2 — Governance Review Remediation Complete  
**Governance Session:** gov-390e7895ee2a (BLOCKED → all 6 conditions remediated)  
**Depends On:** constitution-workflow-governance-evolution (Phase 9 SonarQube integration)  
**Blocks:** hangar-ai-constitution-workflows (will reference ENG-4.11 in exercises)

---

## Problem

The Hangar AI Constitution defines **ENG-4.6 (Coverage Requirements)** which mentions a "70% mutation score for changed code," but **lacks comprehensive guidance on mutation testing itself**. This creates three gaps:

1. **No law definition** — Mutation testing is mentioned as a metric, not governed as a practice
2. **No skill implementation** — Engineers lack guidance on *how* to apply mutation testing in the atomic TDD cycle
3. **No tool/threshold specifications** — Which mutation tools? What do thresholds mean? How to interpret results?

**For aviation safety**, this is critical: 100% test coverage means nothing if tests don't catch real bugs. A crew scheduling system with 100% coverage but 40% mutation score could ship broken code that passes all tests.

---

## Solution

Create **ENG-4.11: Mutation Testing Law** as an extension of Article IV (Testing Laws), with:

1. **ENG-4.11 Law** — Comprehensive mutation testing governance
2. **skill-NN-mutation-testing Skill** — Practical implementation guidance for atomic TDD cycle
3. **Tool specifications** — Pitest (Java), Stryker (TypeScript/JS), mutmut (Python), etc.
4. **Threshold definitions** — 70% baseline, 85% critical paths (matching ENG-4.6 spirit)
5. **SonarQube gate configuration** — Enforce mutation scores as PHASE_GATE (strong recommendation)

---

## Law Content: ENG-4.11 — Mutation Testing Law

### Title
**Mutation Testing Governance: Verify Tests Catch Real Bugs**

### Summary
Tests must not only achieve coverage targets; they must be strong enough to catch mutations (intentional code changes). A mutation score <70% indicates tests are too brittle or incomplete to provide confidence in code correctness.

### Rationale

**Test quality has three dimensions:**
- **Coverage (ENG-4.6):** Which lines are tested? (quantity)
- **Pyramid (ENG-4.2):** What type of tests? (distribution)
- **Mutation (ENG-4.11):** Do tests actually catch bugs? (effectiveness) ← **NEW**

A test that passes with buggy code fails all three dimensions of quality. Mutation testing forces engineers to write **specific, sensitive tests** that validate behavior, not just code paths.

**Aviation Context:** A crew duty-time calculator tested at 100% coverage but with only 50% mutation score could miss:
- Off-by-one errors in accumulated hours
- Rounding bugs in time calculations
- Boundary condition failures (exactly 8.0 hours vs. 8.001)

These bugs would pass all traditional tests but fail in production.

### Requirements

#### 0. **REMEDIATION: Critical Paths Definition (Architect Condition 1)**

**Critical Paths — ≥85% Mutation Score Required:**
- `crew-scheduling/core/assignment.ts` — Crew legality determination, conflict detection (FAA Part 121 duty time rules)
- `crew-scheduling/core/time-calculations.ts` — Duty hour accumulation, reset logic, boundary calculations
- `dispatch/core/safety-constraints.ts` — Fuel calculations, weight-and-balance verification
- `maintenance/core/compliance-tracking.ts` — Regulatory compliance state management, audit trail integrity

**General Paths — ≥70% Mutation Score Required:**
- All other business logic functions (crew availability, schedule display, report generation, etc.)
- UI/presentation layer functions
- Data formatting, transformation, and utility functions
- Logging, monitoring, and diagnostic code

**Verification:** Code review must classify functions as critical or general; SonarQube gates enforced accordingly.

---

#### 1. **Mutation Testing is Mandatory for Changed Code (Strong Recommendation)**
- **Scope:** All code changes in RED/GREEN/REFACTOR cycle (ENG-4.1)
- **Threshold:** ≥70% mutation score for changed code
- **Critical Paths:** ≥85% mutation score for safety-critical functions (crew scheduling, maintenance records, fuel calculations)
- **Enforcement:** SonarQube PHASE_GATE (blocks merge if violated, but can be waived with architect approval)

#### 4. **Mutation Score Definition**
```
Mutation Score = (Killed Mutants / Total Mutants Generated) × 100%

- Killed Mutant: Test fails when mutation applied (desired)
- Survived Mutant: Test passes with mutation applied (problem — test is weak)
- Equivalent Mutant: Mutation produces identical behavior (ignore)
  └─ See Section 7 for decision tree on equivalent mutant handling
  └─ See BEHAVIORAL-EXAMPLES.md for concrete examples from crew-scheduling and dispatch
```

#### 3. **REMEDIATION: Tool Selection Criteria & Mutation Operators (Test Architect Condition 2)**

**Tool Selection by Language:**

| Language | Primary Tool | Configuration File | Mutation Operators | Notes |
|----------|--------------|----------|---|---|
| **TypeScript / JavaScript** | Stryker | `.stryker-config.json` | ArithmeticOperator, ConditionalOperator, LogicalOperator | Exclude: string literals, constant replacements in logging |
| **Python** | mutmut | `setup.py` or `.mutmut.ini` | arithmetic, boolean, constants | Exclude: docstring mutations, comment mutations |
| **Java** | Pitest | `pom.xml` (Maven plugin) | INVERT_NEGATION, RETURN_VALS, MATH, CONDITIONALS | Exclude: constructor mutations in dependency injection |
| **Go** | cosmic-ray | Build-system integration | arithmetic, boolean, conditionals | Verify cosmic-ray stability for Go 1.20+ |
| **C#** | Stryker.NET | Visual Studio / `.dotnet mutate` | Standard operators (arithmetic, logical, conditional) | Visual Studio integration provides UI |

**Excluded Mutation Operators (All Languages):**
- String literal replacements (unless testing string validation logic)
- Comment deletions
- Constant assignments in non-logic code (magic numbers in logging, timeouts, buffer sizes)
- Constructor mutations in dependency injection patterns
- Logging-only methods

**Justification:** Excluded operators reduce false positives and keep mutation testing focused on *behavior-critical* code logic.

---

#### 5. **REMEDIATION: Mutation Testing in Atomic TDD Cycle with Behavioral Workflows (Test Architect Condition 3)**

**Scope Clarification:** Mutation testing applies to **UNIT TESTS ONLY**. Integration and E2E tests are exempt from mutation score gates due to tool maturity limitations and cost-benefit analysis. This does not change overall test pyramid targets (ENG-4.2); mutation testing is a quality enforcement mechanism within the unit test tier.

**Atomic TDD Cycle Integration (ENG-4.1):**

```
RED Phase:
├─ Write test that will fail on current code
└─ No mutation testing (test not yet validated)

GREEN Phase (MANDATORY mutation testing checkpoint):
├─ Write minimal code to pass test
├─ (MANDATORY) Run coverage check: Code coverage ≥70%? (or ≥90% if critical path)
├─ (MANDATORY) Run mutation testing on GREEN code
└─ Decision gateway:
   ├─ Mutation score ≥70% (general) / ≥85% (critical): PASS → proceed to REFACTOR
   ├─ Mutation score <70%: FAIL → Either:
   │  ├─ Strengthen test (add more specific assertions)
   │  ├─ Simplify code (reduce complexity → fewer valid mutations to kill)
   │  └─ Document equivalent mutants if >5% of mutations are equivalent
   └─ Note: If coverage ≥ but mutation < threshold, test is brittle (likely over-mocking)

REFACTOR Phase (MANDATORY mutation verification):
├─ Improve code quality while maintaining test passage
├─ (MANDATORY) Re-run mutation testing on refactored code
├─ Mutation score must remain stable or improve
└─ If score drops: Refactoring introduced a bug; revert and investigate

**Integration & E2E Tests (Out of Scope):**

Integration and end-to-end (E2E) tests are **explicitly excluded** from mutation score gates. Rationale:
- **Tool maturity:** Mutation testing tools (Stryker, Pitest, mutmut) are optimized for unit tests; integration/E2E mutations introduce excessive false positives
- **Cost-benefit:** Mutation testing infrastructure for integration/E2E adds 3–5× execution time with limited signal gain
- **Behavioral validation:** Integration/E2E tests validate cross-system interactions, not code logic robustness; traditional coverage ≥80% adequately gates these
- **Test pyramid alignment:** Unit tests form the narrow base (high mutation rigor); integration tests add breadth (traditional coverage gates); E2E tests validate user workflows (manual or scripted smoke tests)

Teams may **voluntarily** apply mutation testing to critical integration behaviors, but this is not mandated and requires architecture review to justify infrastructure costs.

**SonarQube Gate Behavior:**
- PHASE_GATE (70% general code): Blocks merge; reviewer can override with comment explanation
- HARD_BLOCK (85% critical paths): Blocks merge; requires architect approval + BUS-7.1 audit trail entry
- All waivers logged in PR audit trail for compliance and learning
```

**Behavioral Specification:**
- Mutation testing is **mandatory** for all changed code in GREEN and REFACTOR phases
- Scope: **New code only** (existing code is not retroactively subject to mutation testing; teams may voluntarily apply during refactoring)
- Enforcement: Automatic via SonarQube CI/CD gate; no merge proceeds until gates pass or architect waives (with audit)
- Reviewer Checklist (ENG-3.5 Code Review Law):
  - [ ] Does PR include mutation testing results?
  - [ ] Is mutation score ≥70% for changed code?
  - [ ] For critical paths: Is mutation score ≥85%?
  - [ ] Are equivalent mutants (if any) documented in code comments?
  - [ ] Did test suite strengthen or weaken during refactor?

---

#### 6. **Supported Tools (Language-Specific)**

```
RED Phase:
├─ Write test that will fail on current code
└─ Run mutation testing on test itself
   → Verify test would catch seeded mutations
   → If no mutations killed by test, strengthen test before GREEN

GREEN Phase:
├─ Write minimal code to pass test
└─ Run mutation testing on implementation
   → Generate N mutations in GREEN code
   → Verify test kills ≥70% of mutations
   → If mutation score <70%, either:
      a) Strengthen test (add assertions)
      b) Simplify code (reduce complexity → fewer valid mutations)

REFACTOR Phase:
├─ Improve code quality while maintaining test passage
└─ Re-run mutation testing
   → Mutation score should remain stable or improve
   → If score drops, refactoring introduced a bug
```

#### 5. **Interpreting Mutation Scores**

| Score | Interpretation | Action |
|-------|---|---|
| **85–100%** | Tests are strong, code behavior well-validated | PASS: Proceed to production |
| **70–85%** | Tests are adequate but brittle in some areas | PASS with caution: Code merge allowed, but flag weak areas for next sprint |
| **50–70%** | Tests miss important behavior variants | FAIL: Strengthen tests before merge |
| **<50%** | Tests are superficial (likely high coverage, low quality) | FAIL: Tests do not provide confidence; rewrite entire test suite |

#### 7. **REMEDIATION: Equivalent Mutant Handling & Decision Tree (Test Architect Condition 5)**

**Definition:** Equivalent mutants are code mutations that don't change behavior (e.g., `i > 0` vs. `i >= 0` in loop starting at 1). They're not test failures; they're mutations the test *can't* distinguish.

**Handling Process:**

1. **Tool Auto-Detection (Primary):**
   - Most tools (Stryker, Pitest) automatically detect and exclude simple equivalent mutants
   - Stryker: Use "compatible mutants" option to reduce false positives
   - Pitest: Built-in detection for common equivalents (e.g., removing no-ops)

2. **Manual Documentation (Secondary):**
   ```javascript
   // ENG-4.11: Equivalent mutation — crew-scheduling/core/time-calculations.ts:87
   // Mutation: `if (hoursAccumulated > 8.0)` → `if (hoursAccumulated >= 8.0)`
   // Reason: Equivalent because inputs are floats with 0.5-hour granularity; boundary is irrelevant
   // Tool: Stryker marks as "equivalent mutation"
   ```

3. **SonarQube Scoring:**
   - **Equivalent mutants are EXCLUDED from mutation score calculation**
   - Only non-equivalent killed/survived mutants count toward ≥70%/≥85% thresholds
   - If >10% of mutations are equivalent, notify architect (possible code clarity issue)

4. **REMEDIATION: Equivalent Mutant Decision Tree (Architect Condition — REVISION 3)**

   **Decision Logic:**
   ```
   IF mutation_report.equivalent_mutant_count > 0 THEN:
     ├─ IF equivalent_count / total_mutants > 10% THEN:
     │  ├─ ACTION: Notify architect (possible code clarity issue)
     │  ├─ DECISION: Can code be simplified to reduce equivalent mutations?
     │  ├─ If YES → Refactor code for clarity; re-run mutation testing
     │  └─ If NO → Document justification; proceed with waiver (requires architect approval)
     │
     ├─ IF equivalent_count / total_mutants <= 10% THEN:
     │  ├─ ACTION: Auto-exclude from score calculation
     │  ├─ DECISION: Are equivalent mutations tool-detected or manually documented?
     │  ├─ If tool-detected → Trust tool exclusion; include in SonarQube report with "excluded" tag
     │  └─ If manually documented → Reviewer must verify documentation is accurate; flag any discrepancies
     │
     └─ IF equivalent_count == 0 THEN:
        ├─ ACTION: All mutations are non-equivalent (good code clarity)
        └─ DECISION: Proceed to score threshold evaluation
   ```

   **SonarQube Enforcement:**
   - Mutation report shows: `Killed: X | Survived: Y | Equivalent: Z | Score: X/(X+Y) × 100%`
   - Equivalent mutants (Z) appear in report with `[EXCLUDED]` tag but do NOT affect score denominator
   - If Z > 10%, SonarQube gate triggers ADVISORY to reviewer: "High equivalent mutant rate; consider simplifying code"
   - Architect can override ADVISORY (logs override reason in PR)

5. **Do NOT Artificially Inflate Score:**
   - Do NOT write overly complex tests to catch equivalent mutants
   - Do NOT over-specify assertions (e.g., exact float values) to chase false positives
   - Aim for ≥70% on *non-equivalent* mutants naturally

**See Also:** BEHAVIORAL-EXAMPLES.md for concrete examples of equivalent mutant detection in crew scheduling and dispatch code.

---

#### 8. **Mutation Testing as Part of Code Review (ENG-3.5)**

**Reviewer checklist:**
- [ ] Does PR include mutation testing results?
- [ ] Is mutation score ≥70% for changed code?
- [ ] For critical paths: Is mutation score ≥85%?
- [ ] Are equivalent mutants documented in code comments (if any)?
- [ ] Did the test suite strengthen or weaken during refactor?
- [ ] Are excluded mutation operators justified (e.g., logging constants)?

#### 9. **Integration with SonarQube Gates**

**Gate Configuration** (SonarQube quality gate named `mutation-testing-gate`):
```
- Condition 1: Mutation Score (new code) ≥ 70% → PASS
- Condition 2: Mutation Score (critical paths) ≥ 85% → HARD_BLOCK if violated
- Condition 3: Mutation Score (overall) ≥ 60% → WARNING if violated
```

**Gate Behavior:**
- PHASE_GATE (70% general code): Blocks merge; reviewer can override with comment explanation
- HARD_BLOCK (85% critical paths): Blocks merge; requires architect approval + written justification
- All waivers logged in PR audit trail (BUS-7.1 Decision Governance)
- Merge proceeds only when gates pass OR architect waiver is recorded

#### 10. **Mutation Testing Does NOT Replace Coverage**

- ENG-4.6 (Coverage Requirements) remains in effect: ≥80% overall, ≥90% new code
- Mutation testing is a **complement**, not a replacement
- A test suite can have 100% coverage but 40% mutation score (bad tests)
- A test suite can have 70% coverage but 90% mutation score (strong tests)
- **Both metrics required** for high-quality code

#### 10. **Anti-Patterns & What NOT to Do**

**Anti-Pattern 1: Over-Mocking to Achieve Mutation Score**
```javascript
// BAD: Test mocks everything; mutation score inflated
describe('calculateCrewDuty', () => {
  it('should calculate hours', () => {
    const mockLogger = jest.fn();
    const mockDB = jest.fn();
    const result = calculateCrewDuty([], mockDB, mockLogger);
    expect(result).toBe(0);
  });
});
// Problem: Test passes mutations because no real logic is tested
```

**Anti-Pattern 2: Brittle Assertions to Catch Mutations**
```javascript
// BAD: Assertions are too specific; tests break on refactor
expect(result).toBe(16.25); // Exact float value
expect(result).toBe(16.25000000000001); // Machine-specific
```

#### 11. **REMEDIATION: FIRST Principle Alignment & Performance SLA (Test Architect Condition 6)**

**FIRST Principle Validation (ENG-4.3 Test Quality Law):**

| FIRST Principle | Mutation Testing Impact | Status | Requirement |
|---|---|---|---|
| **Fast** | Mutation testing adds 2–5x runtime to test suite | ⚠️ ACCEPTABLE | Unit test mutation testing must complete <5 min for 1000 LOC; >10 min triggers optimization |
| **Isolated** | Mutations are isolated to single code units; tests run independently | ✅ MET | No shared state; mutations applied to one function at a time |
| **Repeatable** | Mutation tool output is deterministic; same code → same score | ✅ MET | All mutation tools produce consistent scores |
| **Self-validating** | Mutation score is automatically calculated and gated in SonarQube | ✅ MET | No manual assessment; SonarQube gate passes/fails automatically |
| **Timely** | Mutation testing must fit within development cycle feedback loop | ✅ MET w/ SLA | Runs async in CI; does not block developer (see Performance SLA below) |

**Performance SLA (ENG-4.3 Timely requirement):**
- **Mutation testing target:** <5 minutes for unit tests on typical project (1000 LOC)
- **Failure threshold:** >10 minutes → optimization required (reduce mutation operators, split test suite, parallelize)
- **Execution context:** Async CI/CD job; runs in parallel with other gates; does not block developer feedback
- **Acceptable delays:** Mutation testing may be async/deferred; final SonarQube gate must pass before merge

---

#### 12. **REMEDIATION: Tool & SonarQube Verification Checklist (Critic Condition 4)**

**Pre-Implementation Verification Checklist:**

See **CODEBASE-AUDIT.md** for comprehensive pre-implementation verification checklist covering:

- [ ] **Part A: SonarQube Infrastructure** — Version, custom metrics, webhook integration, mutation score import
- [ ] **Part B: Mutation Testing Tools** — Stryker.js, Pitest, mutmut, cosmic-ray availability testing
- [ ] **Part C: CI/CD Pipeline Integration** — Async execution, artifact upload, performance validation
- [ ] **Part D: Team Readiness** — Tool documentation, pilot project selection
- [ ] **Part E: Risk Mitigation** — Performance degradation, equivalent mutant false positives, integration failure fallbacks

**Quick Checklist (14 critical items):**
- [ ] SonarQube version supports mutation score custom metrics (v9.2+)
- [ ] SonarQube PHASE_GATE and HARD_BLOCK custom rules can be configured
- [ ] Stryker.js installed and tested in AA's TypeScript ecosystem (verify npm registry access)
- [ ] Pitest Maven plugin available for Java projects (verify Maven central access)
- [ ] mutmut installed and tested for Python projects (verify pip/pypi access)
- [ ] cosmic-ray available for Go projects (verify module access)
- [ ] Stryker.NET available for C# projects (verify NuGet access)
- [ ] Sample SonarQube quality gate configuration tested end-to-end
- [ ] CI/CD pipeline (GitHub Actions) can invoke mutation testing and upload results
- [ ] Mutation score data successfully imported to SonarQube dashboard
- [ ] Team trained on mutation testing tool usage (workshop or documentation)
- [ ] Pilot project teams identified (crew-scheduling, dispatch, maintenance)
- [ ] Performance SLA validated (<5 min for 1000 LOC; <20% CI/CD overhead)
- [ ] Risk mitigation procedures documented (tool failure fallbacks, performance degradation response)

**Post-Implementation Rollout:**
- Phase 1: Pilot in 1–2 projects (crew-scheduling, dispatch)
- Phase 2: Gather feedback, refine thresholds if needed
- Phase 3: Rollout to all engineering teams
- Timeline: 2–3 weeks (pilot) + 1 week (feedback) + 2 weeks (rollout)

---



**Skill Name:** Mutation Testing & Killing Mutants  
**Category:** Development  
**Implements:** ENG-4.11 (primary), ENG-4.1, ENG-4.3  
**Triggers:** "mutation", "mutant", "mutation score", "test effectiveness"

### Checklist

**Pre-Test (Does my test catch mutations in the implementation?)**
- [ ] Test runs and passes with current code (GREEN)
- [ ] Run mutation testing tool on implementation
- [ ] Review generated mutations (what bugs could exist?)
- [ ] Verify ≥70% of mutations are killed by test (or ≥85% for critical code)
- [ ] Document any equivalent mutants

**During Refactor (Does refactoring maintain mutation score?)**
- [ ] After refactoring, re-run mutation testing
- [ ] Mutation score should stay same or improve
- [ ] If score drops, debug refactoring for bugs

**Code Review (Does PR have strong mutations?)**
- [ ] Ask author: "What mutations do these tests catch?"
- [ ] Verify mutation score in SonarQube report
- [ ] Flag if score <70% and request strengthening
- [ ] Confirm critical paths are ≥85% mutation score

### Hands-On Exercise (Using Stryker for TypeScript)

**Prerequisite:** Review BEHAVIORAL-EXAMPLES.md for concrete examples of mutation testing in aviation-critical code (crew duty calculations, fuel verification, weight-and-balance, compliance tracking).

```bash
# 1. Install Stryker
npm install --save-dev @stryker-mutator/core @stryker-mutator/typescript-checker

# 2. Create stryker.conf.json
cat > stryker.conf.json << 'EOF'
{
  "testRunner": "jest",
  "reporters": ["html", "clear-text", "json"],
  "mutate": ["src/**/*.ts"],
  "mutator": "typescript",
  "thresholds": { "high": 85, "medium": 70, "low": 60 }
}
EOF

# 3. Run mutation testing
npx stryker run

# 4. Open HTML report
open reports/mutation/index.html

# 5. Kill the mutants:
# ├─ Red text = survived mutations (tests too weak)
# ├─ Green text = killed mutations (tests are strong)
# └─ Yellow text = equivalent mutations (ignore, but see Section 7 decision tree)

# 6. For each survived mutation, strengthen test with specific assertion
# Example: If crew duty accumulation test shows survived += → = mutation,
#          strengthen test to check multi-shift accumulation (see BEHAVIORAL-EXAMPLES.md)
```

**Learning Objectives:**
1. Understand the difference between code coverage and mutation score
2. Write tests that distinguish boundary conditions (crew duty at exactly 8.0 hours, fuel exactly meeting requirement, CG at min/max)
3. Recognize brittle tests that don't catch realistic mutations
4. Apply mutation testing to aviation-critical code (crew scheduling, dispatch, maintenance)
5. Calculate mutation score and interpret results in code review

---

## Acceptance Criteria

**Proposal is READY for governance approval when:**
- [ ] ENG-4.11 law defined with rationale, thresholds, tool specs, anti-patterns
- [ ] skill-NN-mutation-testing skill created with checklist and hands-on example
- [ ] SonarQube gate configuration specified (PHASE_GATE for 70%, HARD_BLOCK for critical paths)
- [ ] Aviation-specific examples added (crew scheduling, maintenance records, fuel calculations)
- [ ] Integration with ENG-4.1 (Atomic TDD) documented
- [ ] Anti-patterns documented (over-mocking, brittle assertions, E2E confusion)
- [ ] Governance session confirms alignment with test quality principles (ENG-4.3 FIRST)
- [ ] hangar-ai-constitution-workflows proposal updated to reference ENG-4.11

---

## Law Status

**Recommendation:** ENG-4.11 should be **STRONGLY ENFORCED** (not NON-NEGOTIABLE) because:
- ✅ Validates test quality (prevents false confidence from coverage metrics)
- ✅ Applied to changed code only (doesn't require retrofitting existing code)
- ✅ Supports all languages (tools exist for every major language)
- ⚠️ **Slightly lower strictness than ENG-4.1** because mutation testing interpretation is newer; architects can waive for justified cases

---

## Integration with hangar-ai-constitution-workflows

This proposal creates the foundation for **mutation testing in the workshop:**

1. **Exercise 2 (Refactor TDD):** Learners kill mutants during RED/GREEN/REFACTOR
2. **Exercise 3 & 4:** Mutation score gates alongside coverage gates
3. **Part 2 Real Codebases:** Participants run mutation testing on their own code
4. **SonarQube Dashboard:** Mutation score tracked per exercise

**Cross-Reference:** hangar-ai-constitution-workflows PROPOSAL.md will be updated to state:
> "Exercise X includes mutation testing (ENG-4.11). Participants achieve ≥70% mutation score for all changed code, ≥85% for crew/maintenance/dispatch safety-critical functions."

---

## Files to Create

1. **Constitution Law File:** `/laws/eng/eng-4-11-mutation-testing.md`
2. **Skill File:** `/skills/skill-NN-mutation-testing.md`
3. **SonarQube Configuration:** `/sonarqube-gates/mutation-testing-gate.json`
4. **Aviation Examples:** `/examples/mutation-testing-crew-scheduling.md`

---

## Timeline

- **Governance Review:** 1–2 days (small, focused proposal)
- **Implementation:** 1 week (add law, skill, SonarQube gate, examples)
- **Integration with hangar-ai-constitution-workflows:** Parallel (reference ENG-4.11 in exercises)

---

## References

- **ENG-4.1:** Atomic TDD Law (mutation testing is part of the cycle)
- **ENG-4.2:** Test Pyramid Law (mutation testing applies to all pyramid levels)
- **ENG-4.3:** Test Quality Law (FIRST principles; mutation testing validates "Timely")
- **ENG-4.6:** Coverage Requirements (mentions 70% mutation score; this law clarifies)
- **ENG-3.5:** Code Review Law (mutation score added to review checklist)

