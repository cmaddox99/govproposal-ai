# Atomic TDD Law

**Purpose:** Master the 8-step Atomic Test-Driven Development cycle that enables AI-human pairing with Constitutional compliance.

**Constitutional Reference:** Article IV, Section 4.1
**Time to Read:** 30 minutes

---

## The Law

> **TDD SHALL be practiced in atomic cycles - ONE test at a time with MANDATORY verification and complete Constitutional compliance.**

---

## Why "Atomic"?

**Atomic** means indivisible - the smallest unit of work that delivers value:

- **ONE test** at a time (not batch tests)
- **ONE behavior** at a time (not multiple assertions)
- **ONE commit** per cycle (save progress frequently)
- **ONE verification pass** (all compliance checks together)

---

## The 8-Step Cycle

```
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│  RED → GREEN → REFACTOR → VERIFY → DOCUMENT → COMMIT → PUSH → REPEAT                     │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 1: RED - Write ONE Failing Test

Write **ONE test** that specifies expected behavior.

```java
@Test
public void submitPalApplication_validDraft_changesStatusToSubmitted() {
    // GIVEN
    PalApplication draft = createDraftPalApplication();

    // WHEN
    PalApplication result = palApplicationService.submitPalApplication(draft.getId());

    // THEN
    assertThat(result.getStatus()).isEqualTo(SUBMITTED);
}
```

**Run the test:**
```bash
./mvnw test -Dtest=PalApplicationServiceTest#submitPalApplication_validDraft_changesStatusToSubmitted
```

**Result:** ❌ FAILS (for the right reason - missing behavior)

**Rules:**
- Test MUST fail for the right reason (missing behavior, not syntax error)
- NEVER write multiple tests before making them pass
- Keep the test small and focused

---

### Step 2: GREEN - Write Minimum Code to Pass

Write the **MINIMUM** production code to make that ONE test pass.

```java
@Override
public PalApplication submitPalApplication(Long applicationId) {
    PalApplication application = repository.findById(applicationId)
        .orElseThrow(() -> new NotFoundException("PalApplication not found"));

    application.setStatus(ApplicationStatus.SUBMITTED);

    return repository.save(application);
}
```

**Run the test:**
```bash
./mvnw test -Dtest=PalApplicationServiceTest#submitPalApplication_validDraft_changesStatusToSubmitted
```

**Result:** ✅ PASSES

**Rules:**
- Write ONLY what's needed to pass the test
- Resist adding "nice to have" features
- Don't worry about code quality yet - that's next

---

### Step 3: REFACTOR - Improve Code Quality

Now that tests are **GREEN**, improve the code:

```java
// Before refactoring
@Override
public PalApplication submitPalApplication(Long applicationId) {
    PalApplication application = repository.findById(applicationId)
        .orElseThrow(() -> new NotFoundException("PalApplication not found"));
    application.setStatus(ApplicationStatus.SUBMITTED);
    return repository.save(application);
}

// After refactoring - Extract method, move logic to domain
@Override
public PalApplication submitPalApplication(Long applicationId) {
    PalApplication application = findPalApplicationById(applicationId);
    application.submit();  // Business logic moved to entity
    return repository.save(application);
}

private PalApplication findPalApplicationById(Long id) {
    return repository.findById(id)
        .orElseThrow(() -> new NotFoundException("PalApplication not found: " + id));
}
```

**Run tests after EACH refactoring:**
```bash
./mvnw test
```

**Refactoring Checklist:**
- [ ] Apply Law of Demeter (no method chaining)
- [ ] Extract methods to reduce complexity
- [ ] Improve naming and readability
- [ ] Remove duplication
- [ ] Move business logic to domain entities
- [ ] Add missing documentation

---

### Step 4: VERIFY - Complete Constitutional Compliance

This step ensures compliance with **ALL** Constitutional laws in a single verification pass.

```bash
# Run ALL verification checks
./mvnw test jacoco:report              # Coverage ≥90%
./mvnw formatter:validate              # Code style
./mvnw pmd:check                       # Complexity ≤10
./mvnw pmd:cpd-check                   # Duplication <3%
```

**Verification Checklist:**

**Code Quality Tools:**
- [ ] Line coverage ≥90% for modified code
- [ ] Branch coverage ≥85% for modified code
- [ ] Code style enforced
- [ ] Cyclomatic complexity ≤10
- [ ] Code duplication <3%

**Code Quality Laws (Article III):**
- [ ] Immutability law followed for value objects/DTOs
- [ ] Law of Demeter enforced - no method chaining
- [ ] Method length ≤50 lines
- [ ] Class length ≤300 lines
- [ ] Maximum parameters ≤4

**Architectural Compliance (Article II):**
- [ ] Layered architecture preserved
- [ ] Dependencies point inward
- [ ] No architectural boundary violations

**Testing Laws (Article IV):**
- [ ] Test pyramid distribution maintained
- [ ] Test isolation verified
- [ ] No flaky tests introduced

**If ANY verification fails:** Return to step 3 (REFACTOR)
**If ALL verifications pass:** Proceed to step 5 (DOCUMENT)

---

### Step 5: DOCUMENT - Synchronize Hangar SDD Documentation

Update all relevant documentation:

```bash
# Update tasks.md - Mark completed task
vim hangar-ai-specs/changes/[change-id]/tasks.md
# Change [ ] to [x] for completed task

# Update proposal.md - Document findings
vim hangar-ai-specs/changes/[change-id]/PROPOSAL.md
# Add any decisions, deviations, or discoveries

# Update spec deltas if behavior changed
vim hangar-ai-specs/changes/[change-id]/specs/[capability]/spec.md
```

**Documentation Checklist:**
- [ ] Mark completed task in tasks.md with `[x]`
- [ ] Document findings in proposal.md
- [ ] Update spec deltas if behavior changed
- [ ] Track coverage metrics progression
- [ ] Run `` if spec changes made

---

### Step 6: COMMIT - Save Progress

Commit with a meaningful message following conventional commit format:

```bash
git add .
git commit -m "test(order): add submit order status change test

- RED: Test submitPalApplication changes status to SUBMITTED
- GREEN: Implement minimal status change
- REFACTOR: Extract findPalApplicationById, move submit() to entity

Constitutional compliance verified:
- Coverage: 92% (above 90% threshold)
- Complexity: 4 (below 10 threshold)

Refs: TICKET-123"
```

**Commit Message Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:** `test`, `feat`, `fix`, `refactor`, `docs`, `style`, `chore`

---

### Step 7: PUSH - Share Progress

Push commits to remote repository:

```bash
git push origin feature/order-submit
```

**Why Push After Each Cycle:**
- Enables CI/CD pipeline validation
- Makes work visible to team
- Enables early feedback
- Prevents lost work

---

### Step 8: REPEAT - Continue to Next Test

Return to **Step 1 (RED)** for the next test.

Continue until all tasks in `tasks.md` are complete.

---

## Complete Workflow Example

```bash
# ═══════════════════════════════════════════════════════════════
# CYCLE 1: Test status change
# ═══════════════════════════════════════════════════════════════

# 1. RED - Write failing test
vim src/test/java/.../PalApplicationServiceTest.java
./mvnw test  # Confirm test fails

# 2. GREEN - Write minimum code
vim src/main/java/.../PalApplicationServiceImpl.java
./mvnw test  # Confirm test passes

# 3. REFACTOR - Improve code quality
# - Extract method
# - Move logic to entity
./mvnw test  # Confirm still green

# 4. VERIFY - Complete Constitutional compliance
./mvnw test jacoco:report
./mvnw formatter:validate
./mvnw pmd:check
./mvnw pmd:cpd-check
# All checks pass ✅

# 5. DOCUMENT - Update Hangar SDD
vim hangar-ai-specs/changes/order-submit/tasks.md     # Mark [x]
vim hangar-ai-specs/changes/order-submit/PROPOSAL.md  # Add findings

# 6. COMMIT - Save progress
git add .
git commit -m "test(order): add submit status change test"

# 7. PUSH - Share with team
git push origin feature/order-submit

# 8. REPEAT - Next cycle
# ... start again with next test
```

---

## The Three Laws of TDD

### Law #1: Write No Production Code

> **Except to pass a failing test.**

You must write a test first, see it fail, THEN write code.

### Law #2: Write Only Enough Test

> **To make it fail, including compile failures.**

Don't write the whole test suite. Write ONE test.

### Law #3: Write Only Enough Production Code

> **To pass the ONE failing test.**

Don't implement extra features "just in case."

---

## Why 8 Steps Instead of 3?

Traditional TDD has 3 steps (Red-Green-Refactor). The Constitutional 8-step cycle adds:

| Step | Purpose | Constitutional Requirement |
|------|---------|---------------------------|
| RED | Write failing test | Section 4.1 |
| GREEN | Make it pass | Section 4.1 |
| REFACTOR | Clean code | Section 1.5 (Boy Scout Rule) |
| **VERIFY** | All compliance checks | All Articles |
| **DOCUMENT** | Keep specs synchronized | Hangar SDD workflow |
| **COMMIT** | Save verified progress | Section 3.6 (Git Workflow) |
| **PUSH** | Share with team | CI/CD integration |
| REPEAT | Continue cycle | Section 4.1 |

**Benefits:**
- **Unified Verification:** All compliance checks in one step
- **Auditability:** Every commit has proof of compliance
- **Living Documentation:** Specs stay synchronized
- **Team Visibility:** Progress is always visible

---

## Prompt Examples for AI-Assisted TDD

### Starting a New Test Cycle

```
Prompt: "I need to add email confirmation to PAL application submission.
         Let's follow the Atomic TDD cycle."

AI Response: "Following Article IV, Section 4.1 (Atomic TDD Law), let's start
             with Step 1: RED.

             First, let me write ONE failing test for email confirmation:

             [writes test]

             Please run this test to confirm it fails for the right reason."
```

### When Test Passes

```
Prompt: "The test passes now."

AI Response: "Step 2 (GREEN) complete. Now for Step 3: REFACTOR.

             Looking at the code, I see opportunities to:
             1. Extract the email sending logic to a separate method
             2. Apply Law of Demeter by not chaining through order object

             Let me refactor while keeping tests green..."
```

### After Refactoring

```
Prompt: "Refactoring done, tests still pass."

AI Response: "Step 3 (REFACTOR) complete. Now for Step 4: VERIFY.

             Please run these verification commands:

             ```bash
             ./mvnw test jacoco:report
             ./mvnw formatter:validate
             ./mvnw pmd:check
             ```

             I'll wait for the results to confirm Constitutional compliance
             before we proceed to DOCUMENT."
```

---

## Common Violations

### ❌ Writing Multiple Tests Before Implementation

```java
// WRONG - Batch testing
@Test void test1() { }
@Test void test2() { }
@Test void test3() { }
// Then write code for all three
```

**Fix:** Write ONE test, make it pass, then write the next.

### ❌ Skipping VERIFY Step

```
RED → GREEN → REFACTOR → COMMIT  // Missing VERIFY!
```

**Fix:** Always run all compliance checks before committing.

### ❌ Skipping DOCUMENT Step

```
RED → GREEN → REFACTOR → VERIFY → COMMIT  // Missing DOCUMENT!
```

**Fix:** Update tasks.md and proposal.md before committing.

### ❌ Committing with Violations

```bash
git commit -m "feat: add feature"
# But complexity is 15 (above threshold of 10)
```

**Fix:** Return to REFACTOR until VERIFY passes.

---

## Metrics for Success

### Cycle Time

**Target:** Each cycle takes **5-15 minutes**

If longer than 15 minutes, your test is too big. Break it down.

### Commit Frequency

**Target:** Commit every **10-20 minutes**

If less frequent, you're working in batches, not atomically.

### Test Count

**Target:** Write **10-20 tests per day** (one at a time)

More tests = smaller behaviors = better design.

---

## AI Agent Behavior

When working with AI on Atomic TDD, the AI will:

1. **Start with RED** - Write one failing test
2. **Wait for confirmation** - Ask you to run the test
3. **Write minimal GREEN code** - Only enough to pass
4. **Suggest refactorings** - Reference Article III laws
5. **List VERIFY commands** - All compliance checks
6. **Update documentation** - Propose tasks.md updates
7. **Format commit message** - Conventional commit format
8. **Prompt for next cycle** - Continue the loop

---

## Related Guides

- [Testing Architecture](../testing/testing-architecture.md) - Where tests go
- [Characterization Testing](../testing/characterization-testing.md) - Testing legacy code
- [Atomic TDD Workflow](../testing/atomic-tdd-workflow.md) - Detailed walkthrough
- [Code Quality Laws](./code-quality-laws.md) - Refactoring targets
- [Continuous Refactoring Law](./continuous-refactoring-law.md) - Boy Scout Rule

---

**Constitutional Reference:** Article IV, Section 4.1
**Last Updated:** January 2026
