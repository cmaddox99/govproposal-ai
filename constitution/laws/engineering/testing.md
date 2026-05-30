---
domain: engineering
article: IV
title: Testing Laws
laws:
  - id: ENG-4.1
    title: Atomic TDD Law
    non_negotiable: true
    summary: TDD SHALL be practiced in atomic cycles - ONE test at a time
  - id: ENG-4.2
    title: Test Pyramid Law
    summary: Test suites SHALL maintain proper distribution (Unit 70-80%, Integration 15-25%, E2E 5-10%)
  - id: ENG-4.3
    title: Test Quality Law
    summary: Tests SHALL be Fast, Isolated, Repeatable, Self-validating, and Timely (FIRST)
  - id: ENG-4.4
    title: Test Structure Law
    summary: Every test SHALL follow Given-When-Then / Arrange-Act-Assert structure
  - id: ENG-4.5
    title: Test Naming Convention
    summary: Test names SHALL follow methodName_stateUnderTest_expectedBehavior format
  - id: ENG-4.6
    title: Coverage Requirements
    summary: Code coverage SHALL meet minimum thresholds (80% overall, 90% new code, 100% critical paths)
  - id: ENG-4.7
    title: Test Isolation Law
    summary: Tests MUST be independent with no shared mutable state
  - id: ENG-4.8
    title: Mock Boundaries Law
    summary: Mocking SHALL only occur at I/O boundaries
  - id: ENG-4.9
    title: Contract Testing Law
    summary: Service interfaces SHALL have contract tests
  - id: ENG-4.10
    title: Test Evolution Law
    summary: Characterization tests are transitional scaffolding — as code is refactored toward better design, tests MUST evolve alongside it; over-mocking is a design smell, not a testing solution
  - id: ENG-4.11
    title: Mutation Testing Law
    summary: Tests MUST be strong enough to catch real bugs — NOT just achieve coverage. Mutation score SHALL meet 70% baseline and 85% for critical paths (crew scheduling, dispatch, maintenance).
  - id: ENG-4.12
    title: Legacy Rescue Mutation Hardening Law
    non_negotiable: true
    summary: In the Legacy Rescue workflow Phase 7 (Harden), the mutation score MUST reach ≥90% before the workflow is certified complete. A surviving mutant is an untested assumption and is treated as a latent defect. This gate is a HARD_BLOCK — no override is permitted.
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article IV: Testing Laws

## Coverage Gate

## Test Traceability

## Unit Tests

## Link C++ Unit Tests

## DO-178C Aviation

## Requirements Apply to Avionics

## Apply to Avionics

## Section 4.1: Atomic Test-Driven Development Law

**Law ID:** `ENG-4.1` | **Status:** NON-NEGOTIABLE

TDD SHALL be practiced in atomic cycles - ONE test at a time.

### The Atomic TDD Cycle

```
1. RED      → Write ONE failing test (specifies expected behavior)
2. GREEN   → Write MINIMUM code to pass (no more than necessary)
3. REFACTOR → Improve code quality (while tests stay green)
4. VERIFY   → Run quality gates (tests, coverage, complexity, constitution-lint)
5. COMMIT   → Save progress at green state (atomic, focused commit)
6. REPEAT   → Start next test (never batch tests)
```

### Requirements

1. **ONE test at a time** - Never write multiple tests before making them pass
2. **Minimum code** - Only write enough code to pass the current test
3. **Refactor continuously** - Improve design while tests are green
4. **Commit frequently** - Each green state is a valid commit point

### Prohibited Anti-Patterns

- Writing multiple tests before implementation
- Writing production code without a failing test first
- Skipping the refactor step
- Testing implementation details instead of behavior
- Writing tests after the code (test-after development)

---

## Section 4.2: Test Pyramid Law

**Law ID:** `ENG-4.2`

Test suites SHALL maintain this distribution:

```
       /\
      /E2E\        5-10%  (Slow, expensive, few)
     /──────\
    /Integr- \    15-25% (Medium speed, real I/O)
   /──────────\
  /    Unit    \  70-80% (Fast, isolated, many)
 /──────────────\
```

| Level | Speed | Scope | I/O | Purpose |
|-------|-------|-------|-----|---------|
| **Unit** | <10ms | Single function/class | None | Verify logic in isolation |
| **Integration** | <5s | Component boundaries | Real DB, mocked externals | Verify integration points |
| **E2E** | <60s | Full user workflows | All real | Verify critical paths work |

### Anti-Pattern: Ice Cream Cone (Inverted Pyramid)

- Too many slow E2E tests
- Tests take hours to run
- Developers stop running tests
- Defects found late

---

## Section 4.3: Test Quality Law

**Law ID:** `ENG-4.3`

Tests SHALL be (FIRST principles):

1. **Fast** - Unit tests < 10ms, total suite < 5 minutes
2. **Isolated** - No test depends on another test's state
3. **Repeatable** - Same result every time, any environment
4. **Self-validating** - Pass or fail, no manual inspection
5. **Timely** - Written before or with production code

---

## Section 4.4: Test Structure Law

**Law ID:** `ENG-4.4`

Every test SHALL follow this structure:

```
test "behavior under test" {
    // GIVEN (Arrange) - Setup preconditions
    setup test fixtures and dependencies

    // WHEN (Act) - Execute the behavior
    invoke the method/function under test

    // THEN (Assert) - Verify outcomes
    assert expected results and side effects
}
```

---

## Section 4.5: Test Naming Convention

**Law ID:** `ENG-4.5`

Test names SHALL follow format: `methodName_stateUnderTest_expectedBehavior`

### Compliant Examples

```
calculateTotal_withEmptyCart_returnsZero
validateEmail_withInvalidFormat_throwsValidationError
createOrder_whenInventoryInsufficient_returnsBackorderStatus
```

### Violations

```
testCalculate
test1
testCreateOrderWorks
```

---

## Section 4.6: Coverage Requirements

**Law ID:** `ENG-4.6`

| Scope | Minimum | Notes |
|-------|---------|-------|
| **Overall** | 80% line coverage | Measured on each build |
| **New Code** | 90% line coverage | No merging below threshold |
| **Critical Paths** | 100% coverage | Authentication, payments, calculations |
| **Mutation Score** | 70% for changed code | Tests must catch mutations |

---

## Section 4.7: Test Isolation Law

**Law ID:** `ENG-4.7`

Tests MUST be independent:

- No shared mutable state between tests
- Each test sets up its own fixtures
- Each test cleans up after itself
- Execution order must not matter
- Parallel execution must be safe

---

## Section 4.8: Mock Boundaries Law

**Law ID:** `ENG-4.8`

Mock ONLY at I/O boundaries.

### DO Mock

- External APIs (third-party services)
- Databases (for unit tests)
- File systems
- Network calls
- Time/clock
- Random number generators

### DON'T Mock

- Domain objects
- Value objects
- Internal services (prefer integration tests)
- Data structures

---

## Section 4.9: Contract Testing Law

**Law ID:** `ENG-4.9`

Service interfaces SHALL have contract tests:

- Consumer-driven contracts where applicable
- Schema validation for all events/messages
- Backward compatibility verification
- Version compatibility matrix maintained

---

## Section 4.10: Test Evolution Law

**Law ID:** `ENG-4.10`

Tests MUST evolve alongside the production code they cover. A test that was valid for legacy code is not automatically valid after that code is refactored.

### Characterization Tests Are Transitional Scaffolding

Characterization tests — broad tests written to capture the current behavior of poorly-designed or legacy code — are a legitimate **starting point** for safe refactoring. They are **not** a destination.

- A characterization test is a safety net, not a quality signal
- Passing characterization tests do NOT indicate good design or adequate test coverage
- Each characterization test SHALL be retired and replaced by targeted unit tests as the code it covers is refactored into well-designed, testable units

### Over-Mocking Is a Design Smell

A unit test that mocks all of a class's dependencies is not a unit test of behavior — it is a **snapshot of current structure**. When internal collaborators change, the mocks become stale while the tests continue to pass, creating false confidence.

> If a class requires many mocks to test, the class has too many dependencies. Fix the design; don't normalize the mocks.

Signs that mocking has replaced design:
- A single test requires 3 or more mock collaborators
- Mocks assert on internal method calls rather than observable outcomes
- Tests break when internal implementation changes but observable behavior does not

The correct response to heavy mock usage is **not** more mocks — it is refactoring the production code toward a design that is testable without them (see `ENG-3.4`, `ENG-3.8`).

### Test Evolution Checklist

Apply this checklist whenever production code is refactored:

| Code Change | Required Test Action |
|---|---|
| Extract pure function/method | Add a focused unit test; no mocks needed |
| Separate I/O from logic | Test logic with no mocks; test I/O boundary with one mock |
| Reduce dependencies on a class | Remove corresponding mock setup from existing tests |
| Decompose a large class | Replace the broad characterization test with granular unit tests per sub-unit |
| Improve design testability | Eliminate mocks of internal collaborators; keep only I/O boundary mocks (see `ENG-4.8`) |

### Relationship to Coverage Targets

Coverage thresholds (see `ENG-4.6`) MUST be met by tests that reflect the **current design**, not tests that snapshot a legacy design. Coverage earned through characterization tests with over-mocked dependencies SHALL NOT be counted as meeting quality thresholds for refactored code.

### Anti-Patterns

- Treating characterization tests as proof of correctness after the code they covered has been redesigned
- Mocking internal services or domain objects to avoid refactoring the design (violates `ENG-4.8`)
- Counting coverage from tests that would pass even if the core business logic were deleted (because the mocks define the behavior)
- Claiming "the AI wrote it" as justification — AI-generated tests reflect the design they were given; a poor design produces poor tests regardless of the tool that wrote them

---

## Section 4.11: Mutation Testing Law

**Law ID:** `ENG-4.11`

Tests must not only achieve coverage targets; they must be strong enough to **catch real bugs**. A mutation score <70% indicates tests are too brittle or incomplete to provide confidence in code correctness.

### The Three Dimensions of Test Quality

| Dimension | ENG Law | Measures | Purpose |
|-----------|---------|----------|---------|
| **Coverage** | ENG-4.6 | Which lines are tested? | Quantity |
| **Pyramid** | ENG-4.2 | What type of tests? | Distribution |
| **Mutation** | ENG-4.11 | Do tests catch bugs? | Effectiveness |

A test that passes with buggy code fails all three dimensions of quality.

### Mutation Score Definition

```
Mutation Score = (Killed Mutants / Total Mutants Generated) × 100%
```

### Mandatory Thresholds

- **General Code:** ≥70% mutation score
- **Critical Paths:** ≥85% (crew-scheduling, dispatch, maintenance)

### Scope: Unit Tests Only

Mutation testing is MANDATORY for unit tests in the atomic TDD cycle (ENG-4.1).

Integration & E2E tests are EXEMPT (tool maturity, cost-benefit, test pyramid alignment).

### Integration with Atomic TDD Cycle

**RED Phase:** Write failing test. No mutation testing.

**GREEN Phase (MANDATORY):**
1. Write minimum code
2. Run coverage check: ≥70%/≥90%?
3. Run mutation testing
4. Score ≥70%/≥85%? → REFACTOR : RE-TEST

**REFACTOR Phase (MANDATORY):**
1. Improve code quality
2. Re-run mutation testing
3. Score stable/improved? → Merge : Investigate

### Tool Selection

Use the mutation testing tool and command designated for your language/platform in the
Mutation Testing Skill (`agent-skills/skills-by-domain/development-practices/11-mutation-testing.md`,
section *Running Mutation Testing → Select Tool by Language*). The skill is the canonical source of
truth (SSOT) for approved mutation tools and commands. If any workflow table conflicts with the skill,
follow the skill.

### SonarQube Enforcement

- **HARD_BLOCK:** Critical path <85% (non-waivable)
- **PHASE_GATE:** General code <70% (override with audit trail)
- **ADVISORY:** Equivalent mutants >10% (code review)

### Non-Negotiable

1. Critical paths MUST NOT merge with <85% (HARD_BLOCK)
2. General code <70% requires explanation (PHASE_GATE)
3. Equivalent mutants >10% require review (ADVISORY)
4. Mutation testing MUST run on all new code (GREEN phase)

### Relationship to Other Laws

- **ENG-4.1:** Mutation testing in GREEN/REFACTOR phases
- **ENG-4.2:** Unit tests only (pyramid base)
- **ENG-4.6:** Both score AND coverage required
- **BUS-7.1:** Audit trail for overrides
- **ENG-2.3:** Bounded to unit tests

---

## Section 4.12: Legacy Rescue Mutation Hardening Law

**Law ID:** `ENG-4.12` — **NON-NEGOTIABLE**

In the **Legacy Rescue workflow Phase 7 (Harden — Mutation)**, the mutation score MUST reach ≥90% before the workflow is certified complete.

This threshold is stricter than the general ENG-4.11 baseline (70%/85%) because:
- The codebase was untested before Phase 3
- Characterization tests are transitional scaffolding (ENG-4.10), not quality evidence
- Phase 7 is the final quality gate; no subsequent phase exists to catch gaps

### Hard Block Conditions

| Condition | Threshold | Disposition |
|-----------|-----------|-------------|
| Mutation score | ≥ 90% | HARD_BLOCK — no override permitted |
| Line coverage (PIT input) | ≥ 95% | HARD_BLOCK — PIT must not run on uncovered code |
| Surviving mutant review | 100% reviewed | Lead sign-off required |

### Surviving Mutant Protocol

Each surviving mutant MUST be one of:
1. **Killed** — new test added that catches the mutation
2. **Accepted** — law citation in surviving-mutant register explaining why the case cannot be tested (e.g., equivalent mutant, dead code path)

A surviving mutant that is neither killed nor accepted is a compliance violation.

### Evidence Required

- PIT HTML report committed to `hangar-ai-specs/evidence/mutation-report/`
- Surviving-mutant register reviewed and signed off by lead
- Final SonarQube scan confirming coverage ≥ 95%

### Relationship to Other Laws

- **ENG-4.11:** Base mutation law (70%/85%); ENG-4.12 supersedes it in Legacy Rescue context
- **ENG-4.10:** Characterization tests are transitional — mutation hardening retires them
- **BUS-7.1:** Surviving-mutant register is part of the audit evidence package

---

## Section 4.14: Legacy Rescue Commit Rhythm Law

**Law ID:** `ENG-4.14`

Legacy rescue refactoring SHALL follow an **explicit commit cycle** with verification checkpoints to ensure atomic, cohesive commits. The rhythm encodes WHEN to commit (not just HOW MUCH), preventing violations through structure rather than guidelines.

### Substrate Engineering Principle

This law applies **substrate engineering**: encoding the commit rhythm as explicit workflow steps, not advisory rules. Compare to Greenfield TDD (ENG-4.1), which has an 8-step cycle ending with "Commit checkpoint" — naturally producing 50-200 line commits WITHOUT line-count rules. Legacy Rescue lacked this substrate, leading to violations (e.g., 14,373-line commits in iOS workshop, 348-line contaminated commits in constitution Slice 1).

**Teaching beats policing.** The workflow teaches WHEN to commit through cycle structure, making atomic commits the natural outcome.

### Required Commit Cycles

#### Characterization Cycle (7 steps)

Use when adding characterization tests for untested legacy code:

1. **Identify Behavior:** Select one specific behavior to characterize (e.g., "calculateMileage returns 0 for null input")
2. **Write Test:** Create characterization test capturing current behavior (not ideal behavior)
3. **Verify Current Behavior:** Run test, confirm it passes against existing code
4. **Stage Test Only:** `git add <test-file>` (NO `git add -A` or `git add .`)
5. **Verify Staging:** `git diff --cached --stat` → confirm ONLY test file staged
6. **Commit Test:** Message format: `test(char): capture <behavior> in <component>`
7. **Verify Commit:** `git show --stat HEAD` → confirm no unexpected files

**Checkpoint:** Step 7. If unexpected files present, `git reset HEAD~1` and restart from Step 4.

**Rhythm Output:** One characterization test per commit. Typical size: 20-80 lines.

#### Refactor Cycle (8 steps)

Use when refactoring code with test coverage:

1. **Select Violation:** Identify one SOLID/code-quality violation to fix (e.g., "God class with 5 responsibilities")
2. **Plan Refactor:** Document approach (extract class, move method, etc.)
3. **Apply Refactor:** Make the change (preserve behavior, tests still green)
4. **Verify Tests Green:** Run full test suite → all tests pass
5. **Stage Changes:** `git add <files-modified-by-refactor>` (specific files only)
6. **Verify Staging:** `git diff --cached --stat` → confirm file count matches plan
7. **Commit Refactor:** Message format: `refactor(<violation-id>): <what-changed>`
8. **Verify Commit:** `git show --stat HEAD` → confirm atomicity

**Checkpoint:** Step 8. If commit includes unrelated changes, `git reset HEAD~1` and restart from Step 5.

**Rhythm Output:** One violation remediation per commit. Typical size: 50-300 lines.

### Verification Checkpoints (Critical)

**Why checkpoints matter:** Slice 1 substrate hardening demonstrated that good intentions ("I'll make atomic commits") fail without verification. Commit `e9d7cdf` was contaminated (348 lines, 3 concerns) due to missing checkpoints.

**Step 5 (Verify Staging):**  
Prevents accidentally staging unrelated changes. Catches `git add -A` mistakes BEFORE commit.

**Step 7/8 (Verify Commit):**  
Confirms commit atomicity AFTER commit. If contamination detected, rollback is cheap (one commit back).

**Failure Mode Without Checkpoints:**  
Developer stages everything (`git add -A`), commits contaminated changeset, discovers problem 3 commits later, expensive to fix.

**Failure Mode With Checkpoints:**  
Developer stages everything, Step 5 catches extra files, restages correctly, Step 7/8 confirms clean commit, advances confidently.

### Commit Message Format

**Characterization Test:**
```
test(char): capture <behavior> in <component>

Characterization test for legacy code before refactoring.
Captures CURRENT behavior (not ideal).

Component: <file/class>
Behavior: <specific case>
```

**Refactor:**
```
refactor(<violation-id>): <what-changed>

Fix <SOLID principle / code smell> violation.

Before: <problem description>
After: <solution description>
Tests: <N> green
```

### Violations

- Committing multiple characterization tests in one commit (should be one test per cycle)
- Committing refactor + new test together (should be separate cycles)
- Skipping verification checkpoints (Steps 5, 7/8)
- Using `git add -A` or `git add .` in legacy rescue context (too broad)
- Commit messages without violation ID or behavior description

### Relationship to Other Laws

- **ENG-4.1 (Atomic TDD Law):** Establishes 8-step TDD cycle for Greenfield; ENG-4.14 mirrors this for Legacy Rescue
- **ENG-3.4 (Single Responsibility Principle):** One violation per commit enforces SRP at commit level
- **ENG-3.9 (Open/Closed Principle):** Refactor cycles preserve existing behavior (closed for modification during refactor)
- **ENG-12.1 (Agentic Phase Gate Law):** Commit rhythm is enforced at phase gates (jury reviews commit atomicity)
- **ENG-10.1 (Constitution Metrics):** Commit hygiene is a measurable metric (avg lines/commit, commits/violation)

### Success Criteria

**Atomic Commit:**
- ✅ One concern (one test, one violation)
- ✅ 1-3 files changed
- ✅ 20-300 lines (characterization: 20-80, refactor: 50-300)
- ✅ Tests green before and after
- ✅ Reviewable in < 5 minutes

**Contaminated Commit (VIOLATION):**
- ❌ Multiple unrelated changes
- ❌ > 5 files changed
- ❌ > 500 lines
- ❌ Unrelated files from other work
- ❌ Requires > 10 minutes to review

### Evidence from Substrate Hardening

**iOS Workshop (Jason's Feedback):**  
> "Phase 5 bundled 3 separate refactors and 40 new tests into one [commit]."

**Problem:** No commit rhythm. Advisory rule "one violation per commit" was bypassed.

**Constitution Slice 1 (e9d7cdf contamination):**  
Commit intended for ENG-3.10 (LSP law, 139 lines) was contaminated with phase-8 corrections (207 lines) due to `git add -A` without verification. Total: 348 lines, 3 concerns.

**Lesson:** Verification checkpoints (Steps 5, 7/8) are non-negotiable. They catch contamination before it enters history.

**For detailed workflow integration, IDE guides, and troubleshooting:** See `skill-12-legacy-refactor-rhythm`


