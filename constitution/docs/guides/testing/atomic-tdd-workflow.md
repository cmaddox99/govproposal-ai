# Atomic TDD Workflow Guide

**Purpose:** Learn the Atomic Test-Driven Development cycle for building high-quality code that aligns with the Constitution.

**Constitutional Reference:** Article IV, Section 4.1
**Time to Read:** 30 minutes

---

## What Is Atomic TDD?

> **Definition:** Writing code **one test at a time** in the 8-step cycle with MANDATORY verification and Constitutional compliance.

**"Atomic"** means:
- ONE test at a time (not batch tests)
- ONE behavior at a time (not multiple assertions)
- ONE commit per cycle (save progress frequently)

**Constitutional Requirement:** Article IV, Section 4.1

---

## The Eight-Step Atomic TDD Cycle

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│    ❶ RED        Write ONE failing test                       │
│        ↓                                                     │
│    ❷ GREEN      Write MINIMUM code to pass                   │
│        ↓                                                     │
│    ❸ REFACTOR   Improve code (AI teaches here)               │
│        ↓                                                     │
│    ❹ VERIFY     Run ./mvnw verify (coverage, complexity)     │
│        ↓                                                     │
│    ❺ DOCUMENT   Update AGENTS.md if patterns changed         │
│        ↓                                                     │
│    ❻ COMMIT     git commit with meaningful message           │
│        ↓                                                     │
│    ❼ PUSH       Share progress                               │
│        ↓                                                     │
│    ❽ REPEAT     Next test                                    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## The Three Laws of TDD

### Law #1: Write No Production Code
**Except to pass a failing test.**

You must write a test first, see it fail, *then* write code.

### Law #2: Write Only Enough Test
**To make it fail, including compile failures.**

Don't write the whole test suite. Write ONE test.

### Law #3: Write Only Enough Production Code
**To pass the ONE failing test.**

Don't implement extra features "just in case."

---

## Step-by-Step Walkthrough

### Example Task: Add PAL Application Submission

**Requirement:** Submit an order, changing status from DRAFT to SUBMITTED.

---

### Cycle 1: Test Status Change

#### ❶ RED - Write Failing Test

```java
@SpringBootTest
@Transactional
public class PalApplicationServiceTest {

    @Autowired
    private PalApplicationService orderService;

    @Autowired
    private PalApplicationRepository orderRepository;

    @Test
    public void submitApplication_validDraft_changesStatusToSubmitted() {
        // GIVEN - Create draft PAL application
        PalApplication draft = orderRepository.save(
            PalApplicationBuilder.aDraftOrder()
                .withAllRequiredFieldsFilled()
                .build()
        );

        // WHEN - Submit order
        PalApplication result = orderService.submitApplication(draft.getId());

        // THEN - Status should be SUBMITTED
        assertThat(result.getStatus()).isEqualTo(ApplicationStatus.SUBMITTED);
    }
}
```

**Run test:**
```bash
./mvnw test -Dtest=PalApplicationServiceTest
```

**Result:** ❌ FAILS
```
java.lang.NoSuchMethodError: com.aa.cargo.services.PalApplicationService.submitApplication
```

Good! We have a failing test (compile error counts as failure).

---

#### ❷ GREEN - Make It Pass

**Write minimal code:**

```java
@Service
public class PalApplicationServiceImpl implements PalApplicationService {

    @Autowired
    private PalApplicationRepository repository;

    // Add the method
    @Override
    public Order submitApplication(Long applicationId) {
        PalApplication application = repository.findById(applicationId)
            .orElseThrow(() -> new NotFoundException("Order not found"));

        // Minimal code to pass test
        order.setStatus(ApplicationStatus.SUBMITTED);

        return repository.save(order);
    }
}
```

**Run test again:**
```bash
./mvnw test -Dtest=PalApplicationServiceTest
```

**Result:** ✅ PASSES

---

#### ❸ REFACTOR - Improve Code

Tests are green. Now improve code quality (AI teaches here):

```java
@Override
public Order submitApplication(Long applicationId) {
    PalApplication application = findOrderById(applicationId);

    order.setStatus(ApplicationStatus.SUBMITTED);

    return repository.save(order);
}

// Extract method for reuse
private Order findOrderById(Long id) {
    return repository.findById(id)
        .orElseThrow(() -> new NotFoundException(
            "Order not found with id: " + id
        ));
}
```

**Run tests:**
```bash
./mvnw test
```

**Result:** ✅ Still green after refactoring!

---

#### ❹ VERIFY - Run Quality Checks

```bash
./mvnw verify
```

This runs:
- All tests
- Jacoco coverage check (90%+)
- PMD complexity check (≤10)
- Checkstyle formatting

---

#### ❺ DOCUMENT - Update If Needed

If you created a new pattern, update AGENTS.md:
```markdown
## Patterns
- `findXxxById()` - Standard pattern for loading entities
```

---

#### ❻ COMMIT - Save Progress

```bash
git add .
git commit -m "test(order): add submitApplication status change

- RED: Test submitApplication changes status to SUBMITTED
- GREEN: Implement minimal status change
- REFACTOR: Extract findOrderById method

Refs: #123"
```

---

#### ❼ PUSH - Share Progress

```bash
git push
```

---

#### ❽ REPEAT - Next Test

**One cycle complete!** Now repeat for next behavior.

---

### Cycle 2: Test Submission Timestamp

#### ❶ RED

```java
@Test
public void submitApplication_validDraft_recordsSubmissionTimestamp() {
    PalApplication draft = createValidDraft();
    LocalDateTime before = LocalDateTime.now();

    PalApplication result = orderService.submitApplication(draft.getId());

    LocalDateTime after = LocalDateTime.now();
    assertThat(result.getSubmittedAt())
        .isNotNull()
        .isAfter(before)
        .isBefore(after);
}
```

**Run:** ❌ FAILS (submittedAt is null)

---

#### ❷ GREEN

```java
@Override
public Order submitApplication(Long applicationId) {
    PalApplication application = findOrderById(applicationId);

    order.setStatus(ApplicationStatus.SUBMITTED);
    order.setSubmittedAt(LocalDateTime.now()); // Add this line

    return repository.save(order);
}
```

**Run:** ✅ PASSES

---

#### ❸ REFACTOR

Tests are green, but we can improve. Move business logic to entity:

```java
// Entity
@Entity
public class PalApplication {
    // ... fields

    public void submit() {
        this.status = ApplicationStatus.SUBMITTED;
        this.submittedAt = LocalDateTime.now();
    }
}

// Service (now simpler)
@Override
public Order submitApplication(Long applicationId) {
    PalApplication application = findOrderById(applicationId);

    application.submit(); // Business logic in entity

    return repository.save(order);
}
```

**Run:** ✅ Still green!

---

#### ❹ VERIFY

```bash
./mvnw verify
```

---

#### ❺-❽ DOCUMENT, COMMIT, PUSH, REPEAT

```bash
git commit -m "test(order): record submission timestamp

- RED: Test submittedAt is set
- GREEN: Set submittedAt on submit
- REFACTOR: Extract submit() method to entity (DDD)

Refs: #123"
git push
```

---

### Cycle 3: Test Validation

#### ❶ RED

```java
@Test
public void submitApplication_alreadySubmitted_throwsIllegalStateException() {
    Order submitted = orderRepository.save(
        PalApplicationBuilder.aSubmittedOrder().build()
    );

    assertThatThrownBy(() -> orderService.submitApplication(submitted.getId()))
        .isInstanceOf(IllegalStateException.class)
        .hasMessageContaining("Only DRAFT orders can be submitted");
}
```

**Run:** ❌ FAILS (no exception thrown)

---

#### ❷ GREEN

```java
// Entity
public void submit() {
    // Add validation
    if (this.status != ApplicationStatus.DRAFT) {
        throw new IllegalStateException(
            "Only DRAFT orders can be submitted. Current status: " + this.status
        );
    }

    this.status = ApplicationStatus.SUBMITTED;
    this.submittedAt = LocalDateTime.now();
}
```

**Run:** ✅ PASSES

---

#### ❸ REFACTOR

Extract validation to separate method:

```java
public void submit() {
    validateCanSubmit();

    this.status = ApplicationStatus.SUBMITTED;
    this.submittedAt = LocalDateTime.now();
}

private void validateCanSubmit() {
    if (this.status != ApplicationStatus.DRAFT) {
        throw new IllegalStateException(
            "Only DRAFT orders can be submitted. Current status: " + this.status
        );
    }
}
```

**Run:** ✅ Still green!

---

## Atomic TDD Principles

### Principle #1: Baby Steps

Take the smallest step possible:

```java
// ❌ BAD - Too big a step
@Test
public void submitApplication_completesWholeWorkflow() {
    // Test validates, submits, sends email, logs, notifies...
    // Too many behaviors at once!
}

// ✅ GOOD - One behavior
@Test
public void submitApplication_validDraft_changesStatusToSubmitted() {
    // Just test status change
}
```

### Principle #2: Test First, Always

```java
// ❌ BAD - Code first
// 1. Write submitApplication() method
// 2. Test it later

// ✅ GOOD - Test first
// 1. Write test for submitApplication()
// 2. See it fail (RED)
// 3. Write code to pass (GREEN)
```

### Principle #3: Fake It Till You Make It

Start with the simplest possible implementation:

```java
// Cycle 1: Fake it
public Order submitApplication(Long id) {
    return new Order(); // Just to compile
}

// Cycle 2: Make it real
public Order submitApplication(Long id) {
    PalApplication application = repository.findById(id).get();
    order.setStatus(SUBMITTED);
    return repository.save(order);
}

// Cycle 3: Make it right
public Order submitApplication(Long id) {
    PalApplication application = findOrderById(id); // Extracted
    application.submit(); // Domain logic
    return repository.save(order);
}
```

---

## Refactoring Rules

### When to Refactor?

**Only when tests are GREEN!** ✅

```
❌ RED ────→ Refactor ← DON'T DO THIS
           (Tests failing)

✅ GREEN ──→ Refactor ← DO THIS
           (Tests passing)
```

### What to Refactor?

Apply the Boy Scout Rule (Constitution Article I, Section 1.5):

- [ ] **Extract methods** - Reduce complexity
- [ ] **Improve naming** - Make intent clear
- [ ] **Remove duplication** - DRY principle
- [ ] **Apply Law of Demeter** - Reduce coupling
- [ ] **Add immutability** - Value objects
- [ ] **Move logic to domain** - Rich entities

### Refactoring Checklist

After each refactor:
- [ ] Tests still pass
- [ ] Coverage unchanged or improved
- [ ] Code is cleaner than before
- [ ] Complexity reduced
- [ ] No new violations introduced

---

## AI-Assisted TDD

### How AI Teaches During TDD

During the REFACTOR step, AI teaches Constitutional compliance:

```
Prompt: "I made the test pass. Now help me refactor."

AI Response: "Great! Now per Article I, Section 1.5 (Boy Scout Rule), let's
             improve this code.

             I notice:
             1. **Complexity** - Method is 15 lines, could extract helper
             2. **Law of Demeter** - `application.getCustomer().getEmail()` chains
             3. **DDD** - Business logic should move to entity

             Let me refactor step by step, keeping tests green..."
```

### Test Writing Assistance

```
Prompt: "What test should I write next for submitApplication?"

AI Response: "Following Article IV, Section 4.1 (Atomic TDD), let's identify
             the next behavior to test.

             **Tested so far:**
             ✅ Changes status to SUBMITTED
             ✅ Records submission timestamp
             ✅ Validates only DRAFT can be submitted

             **Next behaviors to test:**
             - Records submitting user
             - Validates required fields
             - Sends confirmation email (mock external I/O)
             - Throws NotFoundException for invalid ID

             Let's write the 'records submitting user' test next..."
```

---

## Common Mistakes

### Mistake #1: Writing Multiple Tests First

```java
// ❌ BAD - Writing 10 tests before any code
@Test public void test1() { }
@Test public void test2() { }
@Test public void test3() { }
// ... write all tests first

// ✅ GOOD - Write one test at a time
@Test public void test1() { }
// Write code for test1
// Refactor
// Commit
// Then write test2
```

### Mistake #2: Skipping Red Phase

```java
// ❌ BAD - Test passes immediately
@Test
public void existingFeature_alreadyWorks() {
    // This test passes without writing code
}

// ✅ GOOD - Test fails first
@Test
public void newFeature_notImplementedYet() {
    // This test MUST fail before you write code
}
```

### Mistake #3: Refactoring While Red

```
❌ Test fails → Let me refactor first → Test still fails
✅ Test fails → Make it pass → NOW refactor → Test passes
```

### Mistake #4: Not Committing Frequently

```java
// ❌ BAD - One commit after 20 tests
// ... 3 hours of work
git commit -m "Added submit feature"

// ✅ GOOD - Commit after each cycle
// RED-GREEN-REFACTOR
git commit -m "test(order): status change"
// RED-GREEN-REFACTOR
git commit -m "test(order): timestamp"
// RED-GREEN-REFACTOR
git commit -m "test(order): validation"
```

---

## Metrics for Success

### Cycle Time

**Target:** Each RED-GREEN-REFACTOR cycle takes **5-15 minutes**

If longer than 15 minutes, your test is too big. Break it down.

### Commit Frequency

**Target:** Commit every **10-20 minutes**

If less frequent, you're working in batches, not atomically.

### Test Count

**Target:** Write **10-20 tests per day** (one at a time)

More tests = smaller, focused behaviors = better design.

---

## Tools and Shortcuts

### Run One Test at a Time

```bash
# Run single test method
./mvnw test -Dtest=PalApplicationServiceTest#submitApplication_validDraft_changesStatusToSubmitted

# Or in IntelliJ: Click green arrow next to @Test
```

### Watch Mode

```bash
# Auto-run tests on file change
./mvnw test -Dwatch=true
```

### Coverage Tool

```bash
# See what's not tested yet
./mvnw test jacoco:report
open target/site/jacoco/index.html
```

### IntelliJ Shortcuts

- `Ctrl+Shift+R` - Run test under cursor
- `Ctrl+Shift+F10` - Run test class
- `Ctrl+Shift+T` - Jump between test and code
- `Alt+Enter` - Create test method

---

## Constitutional Compliance

Atomic TDD ensures compliance with:

✅ **Article IV, Section 4.1** - Atomic TDD Law
✅ **Article I, Section 1.5** - Boy Scout Rule (refactor each cycle)
✅ **Article IV, Section 4.3** - Coverage Law (95%+ with TDD)
✅ **Article III, Section 3.2** - Complexity Law (small methods via TDD)

---

## Practice Exercise

Try this yourself:

### Task: Implement Order Rejection

**Requirements:**
- Reject a submitted order
- Change status to REJECTED
- Record rejection reason
- Record rejection timestamp
- Send rejection email

**Your turn:**
1. Write test list (all behaviors)
2. Pick first test
3. RED - Write failing test
4. GREEN - Make it pass
5. REFACTOR - Improve code
6. VERIFY - Run quality checks
7. DOCUMENT - Update if needed
8. COMMIT - Save progress
9. Repeat for next test

---

## The Three Constitutions and TDD

Atomic TDD supports all three constitutions:

| Constitution | TDD Support |
|--------------|-------------|
| [Engineering](../../../laws/engineering/) | Article IV defines the 8-step TDD cycle, coverage requirements |
| [Product](../../../laws/product/) | Tests verify user journey acceptance criteria |
| [Business](../../../laws/business/) | Tests enforce compliance rules (DOT timelines, TSA vetting) |

### Aviation Compliance Testing

For aviation systems, tests must also verify compliance with the [Aviation/FAA Adoption](../../../avatars/industry/aviation-faa/ADOPTION.md):

```java
@Test
void vetApplicant_tsaCheckRequired_logsAuditTrail() {
    // GIVEN - PAL application requiring TSA vetting
    PalApplication application = PalApplicationBuilder.draft()
        .withApplicant(applicantRequiringTsaCheck())
        .build();

    // WHEN - Vetting is performed
    VettingResult result = vettingService.vet(application);

    // THEN - Audit trail is recorded (TSA compliance)
    assertThat(result.getAuditTrail()).isNotEmpty();
    assertThat(result.getAuditTrail().get(0).getTimestamp()).isNotNull();
}
```

---

## Related Guides

- [Atomic TDD Law](../constitution/atomic-tdd-law.md) - Constitutional reference
- [Characterization Testing](./characterization-testing.md) - For legacy code
- [Testing Architecture](./testing-architecture.md) - Test types and layers
- [Code Quality Laws](../constitution/code-quality-laws.md) - Complexity targets
- [Aviation/FAA Adoption](../../../avatars/industry/aviation-faa/ADOPTION.md) - Compliance testing

---

## References

**Books:**
- "Test Driven Development: By Example" by Kent Beck
- "Growing Object-Oriented Software, Guided by Tests" by Freeman & Pryce

**Videos:**
- https://www.youtube.com/watch?v=qkblc5WRn-U (Kent Beck TDD demo)

**Tools:**
- JUnit 5: https://junit.org/junit5/
- AssertJ: https://assertj.github.io/doc/

---

**Constitutional Reference:** Engineering Constitution, Article IV, Section 4.1 (Atomic TDD Law)
**Last Updated:** January 28, 2026
