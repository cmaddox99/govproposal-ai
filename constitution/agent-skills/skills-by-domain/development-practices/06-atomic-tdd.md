---
skill:
  id: skill-06-atomic-tdd
  name: Atomic TDD
  category: development
  version: "2.0.0"

laws:
  implements:
    - id: ENG-4.1
      title: Atomic TDD Law (NON-NEGOTIABLE)
    - id: ENG-4.2
      title: Test Pyramid Law
    - id: ENG-4.3
      title: Test Quality Law
    - id: ENG-4.4
      title: Test Structure Law
  references:
    - id: ENG-4.5
      title: Test Naming Convention
    - id: ENG-4.6
      title: Coverage Requirements
    - id: ENG-4.7
      title: Test Isolation Law
    - id: ENG-4.11
      title: Mutation Testing Law

triggers:
  phrases:
    - "Write tests first"
    - "TDD cycle"
    - "Red-green-refactor"
    - "Implement with tests"

followed_by:
  - skill-08-code-review
  - skill-09-refactoring
  - skill-11-mutation-testing
---

# Skill: Atomic TDD

> **Purpose:** Implement software through disciplined test-first development, one small step at a time.
> **Workflow:** See `workflows/legacy-rescue-rewrite.md` for the full governed rewrite sequence with golden-file parity contracts.

---

## Purpose

Atomic TDD (Test-Driven Development) is the disciplined practice of writing software in the smallest possible increments, always starting with a failing test. This skill ensures:

1. **Design emerges from tests** - Tests drive the interface and structure
2. **Every line of code is justified** - No code exists without a test requiring it
3. **Continuous verification** - Always know the code works
4. **Refactoring confidence** - Tests enable fearless improvement
5. **Balanced test pyramid** - Proper distribution of unit, integration, and E2E tests
6. **Traceable progress** - All tests tracked as tasks in Hangar SDD

The "atomic" modifier emphasizes: **one test at a time, no batching, no skipping steps**.

**Test Pyramid Integration:** Before starting TDD cycles, analyze each slice to determine required tests at each pyramid level and create corresponding tasks in the Hangar SDD task file. This ensures proper coverage distribution (70-80% unit, 15-25% integration, 5-10% E2E).

---

## When to Invoke

Invoke this skill when:

- Implementing any new functionality
- Fixing bugs (reproduce with test first)
- Refactoring existing code (ensure tests exist first)
- Adding features to existing code
- Any time code needs to be written

**Trigger phrases:**
- "Let's implement this feature"
- "Time to write the code"
- "How should I build this?"
- "Let's fix this bug"

**First action:** Verify test pyramid tasks exist in Hangar SDD task file, then pick the first uncompleted task.

---

## Constitutional Foundation

### Engineering Constitution
- **Article IV, Section 4.1** - Test-First Development: "No production code without a failing test"
- **Article IV, Section 4.2** - Test Pyramid Law: Unit 70-80%, Integration 15-25%, E2E 5-10%
- **Article IV, Section 4.3** - Behavior Focus: "Test behavior, not implementation"
- **Article III, Section 3.1** - Simplicity: "The simplest code that passes the test"

### Product Constitution
- **ENG-11.1** - Traceability: Tests connect to user stories and Hangar SDD tasks

### Business Constitution
- **Article II, Section 2.1** - Business Rules: Tests encode business rules

---

## Prerequisite: Test Pyramid Tasks

Before starting TDD, test pyramid tasks must exist in the Hangar SDD task file.

**Location:** `hangar-ai-specs/changes/<feature-name>/tasks.md`

**Created during:** Planning phase (see skill-spec-governance)

| Level | Coverage Target | Focus |
|-------|-----------------|-------|
| **Unit** | 70-80% | Domain logic, validation, calculations |
| **Integration** | 15-25% | API endpoints, database, service boundaries |
| **E2E** | 5-10% | Critical user journeys only |

Work through tasks in order: **Unit → Integration → E2E**, following the TDD cycle for each.

---

## Method: The 8-Step Atomic TDD Cycle

### Step 1: Identify the Next Behavior

**Guiding Questions:**
- What is the smallest piece of behavior we can add?
- What would the user see or experience?
- What's the next logical step in the acceptance criteria?

**Socratic Prompt:**
> "Looking at our acceptance criteria, what's the simplest behavior we haven't implemented yet? Think about it from the user's perspective - what would they try to do next?"

### Step 2: Write a Failing Test (RED)

Write exactly ONE test that:
- Describes the expected behavior
- Uses the public interface
- Fails for the right reason
- Is named descriptively

**Test Structure (Arrange-Act-Assert):**
```
// Arrange: Set up the test context
// Act: Perform the action being tested
// Assert: Verify the expected outcome
```

**Verification Checkpoint:**
- [ ] Test is written
- [ ] Test fails (RED)
- [ ] Test fails for the expected reason (not syntax error, not wrong assertion)

### Step 3: Verify the Test Fails

Run the test and confirm:
- It fails (not passes accidentally)
- It fails for the RIGHT reason
- The failure message is clear

**If test passes:** You either tested existing behavior or the test is wrong.

### Step 4: Write Minimal Code to Pass (GREEN)

Write the **simplest possible code** that makes the test pass:
- Don't anticipate future requirements
- Don't add "nice to have" features
- Don't refactor yet
- It's okay if the code is ugly

**Guiding Questions:**
- What is the absolute minimum to make this test pass?
- Am I adding anything the test doesn't require?

**Verification Checkpoint:**
- [ ] Code is written
- [ ] Test passes (GREEN)
- [ ] No code beyond what the test requires

### Step 5: Verify All Tests Pass

Run the ENTIRE test suite:
- The new test passes
- All previous tests still pass
- No regressions introduced

**If any test fails:** Fix before proceeding. Never move forward with failing tests.

### Step 6: Refactor (REFACTOR)

Now improve the code while keeping tests green:

**Refactoring Opportunities:**
- Remove duplication (DRY)
- Improve naming
- Extract methods/classes
- Simplify conditionals
- Apply design patterns

**Refactoring Rules:**
- Tests must stay green throughout
- Make small changes, run tests frequently
- Don't add new behavior during refactoring

**Verification Checkpoint:**
- [ ] Code is improved
- [ ] All tests still pass
- [ ] No new behavior added

### Step 7: Verify Tests Still Pass

Run the full test suite again after refactoring:
- All tests pass
- Code is cleaner
- Ready for next behavior

### Step 8: Commit or Continue

**If behavior is complete:** Commit with a clear message
**If more behavior needed:** Return to Step 1

**Note:** Test pyramid tasks should already exist in the Hangar SDD task file (created during proposal phase). Mark tasks complete as you finish each TDD cycle.

---

## Quality Checklist

Before considering the TDD cycle complete:

### Test Pyramid Compliance
- [ ] **Pyramid Planned:** Hangar SDD task file includes tests categorized by pyramid level
- [ ] **Unit Coverage:** 70-80% of tests are unit tests
- [ ] **Integration Coverage:** 15-25% of tests are integration tests
- [ ] **E2E Coverage:** 5-10% of tests are E2E tests (critical paths only)
- [ ] **Tasks Updated:** Hangar SDD task file reflects completed tests

### TDD Discipline
- [ ] **Test First:** Every piece of production code has a test that preceded it
- [ ] **Single Behavior:** Each test verifies exactly one behavior
- [ ] **Clear Names:** Test names describe the expected behavior
- [ ] **Arrange-Act-Assert:** Tests follow AAA structure
- [ ] **No Duplication:** Common setup is extracted appropriately
- [ ] **Fast:** Tests run quickly (milliseconds, not seconds)
- [ ] **Independent:** Tests can run in any order
- [ ] **Behavior Focus:** Tests verify behavior, not implementation

### Test Effectiveness (ENG-4.11)
- [ ] **Mutation Score Ready:** Unit tests prepared for mutation testing tool integration
- [ ] **General Code Threshold:** Mutation score ≥ 70% on general code paths (PHASE_GATE at SonarQube gate)
- [ ] **Critical Paths Threshold:** Mutation score ≥ 85% on critical paths (crew scheduling, dispatch, maintenance — HARD_BLOCK at final Certify phase)
- [ ] **Equivalent Mutant Review:** Reviewed equivalent mutants; documented decisions (≤ 10% of total mutants acceptable without override)
- [ ] **Test Strengthening:** Tests kill majority of mutations; weak mutation detections resolved (see skill-11-mutation-testing for improvement tactics)

---

## Skill Interactions

### Preceded By
- **03-Executable Spec** - Provides acceptance criteria to implement
- **07-Vertical Slice Dev** - Defines the slice being implemented

### Followed By
- **08-Code Review** - Reviews the implemented code
- **11-Mutation Testing** - Verifies test effectiveness; strengthens weak test cases during REFACTOR phase (ENG-4.11)

### Related Skills
- **04-Business Domain Modeling** - Domain model emerges through TDD
- **05-Business Rules** - Rules are encoded through tests

> 📎 Examples: See 06-atomic-tdd-examples.md
