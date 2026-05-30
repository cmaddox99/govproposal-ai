# Characterization Testing Guide

**Purpose:** Learn how to write characterization tests that enable safe refactoring of legacy code.

**Constitutional Reference:** Article IV, Section 4.1 (Atomic TDD), Section 4.3 (Coverage Laws)
**Time to Read:** 25 minutes

---

## What Are Characterization Tests?

> **Definition:** Tests that capture and preserve the *current behavior* of existing code, providing a safety net for refactoring.

**Created by:** Michael Feathers in "Working Effectively with Legacy Code"

**Key Insight:** You don't need to understand *why* code works a certain way. You just need to document *that* it works that way.

---

## When to Use Characterization Tests

✅ **Use When:**
- Taking over legacy code with few or no tests
- Planning to refactor complex code
- Need 100% test coverage quickly
- Don't understand all the business rules yet
- Want to enable safe continuous refactoring

❌ **Don't Use When:**
- Writing new code from scratch (use TDD instead)
- Code already has comprehensive behavior tests
- You're throwing away the code

---

## The Golden Rules

### Rule #1: No Mocking

**Why?** Mocks test implementation, not behavior. When you refactor, mocked tests break.

```java
// ❌ BAD - Mocking internal structure
@Test
public void testSubmit_withMocks() {
    PalApplicationRepository mockRepo = mock(PalApplicationRepository.class);
    GraphMailService mockEmail = mock(GraphMailService.class);

    PalApplicationService service = new PalApplicationService(mockRepo, mockEmail);

    when(mockRepo.findById(1L)).thenReturn(Optional.of(draftOrder));
    when(mockRepo.save(any())).thenReturn(submittedOrder);

    service.submitApplication(1L);

    verify(mockRepo).save(any()); // Tests implementation
    verify(mockEmail).sendConfirmation(any()); // Tests structure
}

// ✅ GOOD - Real collaborators, test behavior
@Test
public void submitApplication_validDraft_changesStatusToSubmitted() {
    // Use real repository with H2 database
    PalApplication draft = orderRepository.save(
        PalApplicationBuilder.aDraftOrder().build()
    );

    PalApplication result = orderService.submitApplication(draft.getId());

    assertThat(result.getStatus()).isEqualTo(SUBMITTED); // Tests behavior
    assertThat(result.getSubmittedAt()).isNotNull();
}
```

**Exception:** Only mock external systems you don't control (e.g., third-party APIs, Email SMTP). Use WireMock for those.

### Rule #2: Test Behavior, Not Structure

**Behavior** = What the system does
**Structure** = How the system does it

```java
// ❌ BAD - Testing structure
@Test
public void testSubmit_callsSaveMethod() {
    service.submitApplication(1L);

    verify(repository).save(any()); // Who cares if it called save?
}

// ✅ GOOD - Testing behavior
@Test
public void submitApplication_validDraft_persistsSubmittedStatus() {
    PalApplication draft = createDraft();

    orderService.submitApplication(draft.getId());

    Order persisted = orderRepository.findById(draft.getId()).get();
    assertThat(persisted.getStatus()).isEqualTo(SUBMITTED);
    // This is what matters - data persisted correctly
}
```

### Rule #3: One Behavior Per Test

Keep tests small and focused:

```java
// ❌ BAD - Testing multiple behaviors
@Test
public void testSubmit() {
    PalApplication result = orderService.submitApplication(1L);

    assertThat(result.getStatus()).isEqualTo(SUBMITTED);
    assertThat(result.getSubmittedAt()).isNotNull();
    assertThat(result.getSubmittedBy()).isEqualTo("CURRENT_USER");
    // Email sent
    // Audit log created
    // Notification queued
    // ... too many concerns
}

// ✅ GOOD - One behavior per test
@Test
public void submitApplication_validDraft_changesStatusToSubmitted() {
    PalApplication result = orderService.submitApplication(draftId);
    assertThat(result.getStatus()).isEqualTo(SUBMITTED);
}

@Test
public void submitApplication_validDraft_recordsSubmissionTimestamp() {
    PalApplication result = orderService.submitApplication(draftId);
    assertThat(result.getSubmittedAt()).isNotNull();
}

@Test
public void submitApplication_validDraft_recordsSubmittingUser() {
    PalApplication result = orderService.submitApplication(draftId);
    assertThat(result.getSubmittedBy()).isEqualTo("CURRENT_USER");
}
```

---

## Step-by-Step Process

### Step 1: Identify the Method to Characterize

Start with public methods in the service layer:

```java
// Target: PalApplicationServiceImpl.java
public class PalApplicationServiceImpl implements PalApplicationService {

    // ← Start here
    public Order submitApplication(Long applicationId) {
        // ... complex logic we need to characterize
    }
}
```

### Step 2: Create Test Class

```java
@SpringBootTest
@Transactional
public class PalApplicationServiceCharacterizationTest {

    @Autowired
    private PalApplicationService orderService;

    @Autowired
    private PalApplicationRepository orderRepository;

    // Tests go here
}
```

### Step 3: Write a Failing Test

Start by asserting something (anything) to see what happens:

```java
@Test
public void submitApplication_withValidDraft_characterizesBehavior() {
    // GIVEN
    PalApplication draft = orderRepository.save(
        PalApplicationBuilder.aDraftOrder().build()
    );

    // WHEN
    PalApplication result = orderService.submitApplication(draft.getId());

    // THEN
    assertThat(result.getStatus()).isEqualTo(null); // Wrong on purpose
}
```

**Run the test. It fails:**
```
Expected: null
Actual: SUBMITTED
```

### Step 4: Record the Actual Behavior

Update assertion with the actual behavior:

```java
@Test
public void submitApplication_validDraft_changesStatusToSubmitted() {
    PalApplication draft = orderRepository.save(
        PalApplicationBuilder.aDraftOrder().build()
    );

    PalApplication result = orderService.submitApplication(draft.getId());

    assertThat(result.getStatus()).isEqualTo(SUBMITTED); // ✅ Now correct
}
```

### Step 5: Cover All Code Paths

Use coverage tool to find untested paths:

```bash
./mvnw test jacoco:report
open target/site/jacoco/index.html
```

Add tests for:
- Happy path
- Validation failures
- Edge cases
- Error conditions

```java
@Test
public void submitApplication_alreadySubmitted_throwsIllegalStateException() {
    Order submitted = createSubmittedOrder();

    assertThatThrownBy(() -> orderService.submitApplication(submitted.getId()))
        .isInstanceOf(IllegalStateException.class)
        .hasMessageContaining("already submitted");
}

@Test
public void submitApplication_missingRequiredFields_throwsValidationException() {
    Order incomplete = createIncompleteOrder();

    assertThatThrownBy(() -> orderService.submitApplication(incomplete.getId()))
        .isInstanceOf(ValidationException.class)
        .hasMessageContaining("Customer name required");
}
```

### Step 6: Verify 100% Coverage

```bash
./mvnw test jacoco:report
```

Look for `PalApplicationServiceImpl` - should show 100% line coverage.

---

## Test Data Builders

Make test setup readable with builders:

```java
public class PalApplicationBuilder {
    private Long id;
    private String customerName = "Default Customer";
    private ApplicationStatus status = ApplicationStatus.DRAFT;
    private String email = "default@example.com";
    private LocalDateTime createdAt = LocalDateTime.now();

    public static PalApplicationBuilder aDraftOrder() {
        return new PalApplicationBuilder()
            .withStatus(ApplicationStatus.DRAFT);
    }

    public static PalApplicationBuilder aSubmittedOrder() {
        return new PalApplicationBuilder()
            .withStatus(ApplicationStatus.SUBMITTED)
            .withSubmittedAt(LocalDateTime.now());
    }

    public PalApplicationBuilder withCustomerName(String name) {
        this.customerName = name;
        return this;
    }

    public PalApplicationBuilder withStatus(ApplicationStatus status) {
        this.status = status;
        return this;
    }

    public PalApplicationBuilder withAllRequiredFieldsFilled() {
        // Set all required fields to valid values
        return this;
    }

    public Order build() {
        PalApplication application = new Order();
        order.setId(id);
        order.setCustomerName(customerName);
        order.setStatus(status);
        order.setEmail(email);
        order.setCreatedAt(createdAt);
        return order;
    }
}
```

**Usage:**

```java
// Readable and concise
PalApplication draft = PalApplicationBuilder
    .aDraftOrder()
    .withCustomerName("Test Customer")
    .withAllRequiredFieldsFilled()
    .build();
```

---

## Complete Example

### Method to Characterize

```java
// From PalApplicationServiceImpl
public Order submitApplication(Long applicationId) {
    PalApplication application = repository.findById(applicationId)
        .orElseThrow(() -> new NotFoundException("Order not found"));

    // Validation
    if (application.getStatus() != ApplicationStatus.DRAFT) {
        throw new IllegalStateException("Only DRAFT orders can be submitted");
    }

    // Check required fields
    if (application.getCustomerName() == null ||
        application.getCustomerName().isEmpty()) {
        throw new ValidationException("Customer name is required");
    }

    // Update status
    order.setStatus(ApplicationStatus.SUBMITTED);
    order.setSubmittedAt(LocalDateTime.now());
    order.setSubmittedBy(getCurrentUser());

    // Save
    Order saved = repository.save(order);

    // Send email
    graphMailService.sendConfirmationEmail(saved);

    return saved;
}
```

### Characterization Tests

```java
@SpringBootTest
@Transactional
public class OrderSubmitCharacterizationTest {

    @Autowired
    private PalApplicationService orderService;

    @Autowired
    private PalApplicationRepository orderRepository;

    // Happy path - test main behavior
    @Test
    public void submitApplication_validDraft_changesStatusToSubmitted() {
        PalApplication draft = orderRepository.save(
            PalApplicationBuilder.aDraftOrder()
                .withAllRequiredFieldsFilled()
                .build()
        );

        PalApplication result = orderService.submitApplication(draft.getId());

        assertThat(result.getStatus()).isEqualTo(ApplicationStatus.SUBMITTED);
    }

    @Test
    public void submitApplication_validDraft_recordsSubmissionTimestamp() {
        PalApplication draft = createValidDraft();
        LocalDateTime before = LocalDateTime.now();

        PalApplication result = orderService.submitApplication(draft.getId());

        LocalDateTime after = LocalDateTime.now();
        assertThat(result.getSubmittedAt())
            .isAfter(before)
            .isBefore(after);
    }

    @Test
    public void submitApplication_validDraft_recordsSubmittingUser() {
        PalApplication draft = createValidDraft();

        PalApplication result = orderService.submitApplication(draft.getId());

        assertThat(result.getSubmittedBy()).isNotBlank();
    }

    @Test
    public void submitApplication_validDraft_persistsChanges() {
        PalApplication draft = createValidDraft();

        orderService.submitApplication(draft.getId());

        Order persisted = orderRepository.findById(draft.getId()).get();
        assertThat(persisted.getStatus()).isEqualTo(ApplicationStatus.SUBMITTED);
    }

    // Error cases - test validation
    @Test
    public void submitApplication_orderNotFound_throwsNotFoundException() {
        Long nonExistentId = 99999L;

        assertThatThrownBy(() -> orderService.submitApplication(nonExistentId))
            .isInstanceOf(NotFoundException.class)
            .hasMessageContaining("Order not found");
    }

    @Test
    public void submitApplication_alreadySubmitted_throwsIllegalStateException() {
        Order submitted = orderRepository.save(
            PalApplicationBuilder.aSubmittedOrder().build()
        );

        assertThatThrownBy(() -> orderService.submitApplication(submitted.getId()))
            .isInstanceOf(IllegalStateException.class)
            .hasMessageContaining("Only DRAFT orders can be submitted");
    }

    @Test
    public void submitApplication_missingCustomerName_throwsValidationException() {
        Order incomplete = orderRepository.save(
            PalApplicationBuilder.aDraftOrder()
                .withCustomerName(null)
                .build()
        );

        assertThatThrownBy(() -> orderService.submitApplication(incomplete.getId()))
            .isInstanceOf(ValidationException.class)
            .hasMessageContaining("Customer name is required");
    }

    @Test
    public void submitApplication_emptyCustomerName_throwsValidationException() {
        Order incomplete = orderRepository.save(
            PalApplicationBuilder.aDraftOrder()
                .withCustomerName("")
                .build()
        );

        assertThatThrownBy(() -> orderService.submitApplication(incomplete.getId()))
            .isInstanceOf(ValidationException.class)
            .hasMessageContaining("Customer name is required");
    }

    // Helper methods
    private Order createValidDraft() {
        return orderRepository.save(
            PalApplicationBuilder.aDraftOrder()
                .withAllRequiredFieldsFilled()
                .build()
        );
    }
}
```

---

## Verification Checklist

After writing characterization tests:

- [ ] **100% line coverage** for the method
- [ ] **No mocking** of internal collaborators
- [ ] **Test behavior** not structure
- [ ] **One assertion** per test (where possible)
- [ ] **All code paths** covered (happy path + errors)
- [ ] **Edge cases** tested (null, empty, invalid)
- [ ] **Tests are fast** (<100ms each)
- [ ] **Tests are independent** (can run in any order)
- [ ] **Test names** describe behavior clearly
- [ ] **Tests use** builders for readable setup

---

## AI Prompt Examples

### Starting with Legacy Code

```
Prompt: "I need to add tests to this legacy method before I refactor it."

AI Response: "Following Article IV (Testing Laws), I'll help you write
             characterization tests.

             **Step 1:** Let me analyze the method to identify all code paths:
             - Happy path
             - Validation branches
             - Exception handlers
             - Edge cases

             **Step 2:** I'll write a test that captures current behavior:
             ```java
             @Test
             void methodName_scenario_capturesCurrentBehavior() {
                 // We'll discover what this returns and update assertion
             }
             ```

             **Step 3:** Run it, record actual behavior, update assertion.

             **Step 4:** Repeat until 100% coverage.

             Shall I start with the happy path test?"
```

### Understanding Mysterious Behavior

```
Prompt: "This test captures weird behavior I don't understand. Should I fix it?"

AI Response: "**Don't fix it yet!** Characterization tests document WHAT
             code does, not WHAT it should do.

             **Options:**
             1. Document the behavior in a comment
             2. Ask business owner if it's intentional
             3. Create a ticket for future investigation

             **Then:**
             - If bug → file ticket, fix later with proper testing
             - If intentional → document why
             - If unclear → keep test, investigate later

             The important thing is: now you KNOW it does this."
```

---

## Now You Can Refactor Safely!

With 100% characterization test coverage:

✅ Refactor with confidence
✅ Tests stay green during refactoring
✅ Catch regressions immediately
✅ Enable continuous improvement
✅ Meet Constitutional requirements

**Next Steps:**
1. Run characterization tests (all green)
2. Refactor code (apply DDD, immutability, Law of Demeter)
3. Run tests again (still green)
4. Commit with Boy Scout Rule message

---

## Common Pitfalls

### Pitfall #1: Testing Implementation Details

```java
// ❌ BAD
verify(repository).findById(1L);
verify(graphMailService).sendEmail(any());
```

**Fix:** Test observable behavior instead.

### Pitfall #2: Too Many Assertions

```java
// ❌ BAD - Which behavior are we testing?
assertThat(result.getStatus()).isEqualTo(SUBMITTED);
assertThat(result.getSubmittedAt()).isNotNull();
assertThat(result.getSubmittedBy()).isEqualTo("USER");
```

**Fix:** Split into separate tests.

### Pitfall #3: Hard-Coded Test Data

```java
// ❌ BAD - Magic values
PalApplication application = new Order();
order.setCustomerName("Test");
order.setEmail("test@test.com");
// ... 20 more setters
```

**Fix:** Use test data builders.

### Pitfall #4: Tests That Are Too Slow

```java
// ❌ BAD - Hitting real database for every assertion
@Test
public void test1() { /* insert data, query, assert */ }
@Test
public void test2() { /* insert data, query, assert */ }
// ... 100 more tests = 30 seconds
```

**Fix:** Use `@Transactional` to rollback, or H2 in-memory database.

---

## References

**Books:**
- "Working Effectively with Legacy Code" by Michael Feathers
- "xUnit Test Patterns" by Gerard Meszaros

**Articles:**
- https://michaelfeathers.silvrback.com/characterization-testing
- https://martinfowler.com/bliki/CharacterizationTest.html

**Tools:**
- JUnit 5: https://junit.org/junit5/
- AssertJ: https://assertj.github.io/doc/
- Jacoco: https://www.jacoco.org/jacoco/

---

## Related Guides

- [Atomic TDD Workflow](./atomic-tdd-workflow.md) - For new code
- [Testing Architecture](./testing-architecture.md) - Test types and layers
- [Brownfield Adoption](../adoption/brownfield-adoption.md) - Legacy project strategy
- [Continuous Refactoring Law](../constitution/continuous-refactoring-law.md) - Safe refactoring
- [Constitution Overview](../constitution/constitution-overview.md) - All three constitutions

## Product Domain Testing Patterns

When characterizing legacy code, reference the relevant product domain:

| Domain | Key Entities to Characterize |
|--------|------------------------------|
| [Cargo & Freight](../../../avatars/product-type/cargo-freight/ADOPTION.md) | PalApplication, VettingAnswer, AWB |
| [Passenger Booking](../../../avatars/product-type/passenger-booking/ADOPTION.md) | Reservation, FlightSegment, Ancillary |
| [Loyalty](../../../avatars/product-type/loyalty-aadvantage/ADOPTION.md) | AAdvantageAccount, MilesTransaction |

---

**Constitutional Reference:** Engineering Constitution, Article IV, Section 4.1 (Atomic TDD), Section 4.3 (Coverage Laws)
**Last Updated:** January 28, 2026
