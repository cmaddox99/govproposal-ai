# Agent Response Patterns

**Purpose:** Understand how AI agents respond to Constitutional laws and what to expect from AI-assisted development.

**Time to Read:** 20 minutes

---

## How AI Teaches Through Responses

The Constitution creates a **teaching feedback loop**:

```
┌─────────────────────────────────────────────────────────────┐
│                  AI TEACHING FEEDBACK LOOP                  │
│                                                             │
│    You Ask           AI Responds         You Learn          │
│    ─────────         ───────────         ─────────          │
│    "Write code"  →   "Per Article IV,    TDD is required   │
│                       let's write a                         │
│                       test first..."                        │
│                                                             │
│    "Add feature" →   "Following Atomic   Small steps,      │
│                       TDD, what's the    one test at time  │
│                       first behavior?"                      │
│                                                             │
│    "Review this" →   "Article III        Complexity rules, │
│                       violation:         how to fix        │
│                       complexity 15..."                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Pattern: TDD Enforcement

### When You Skip Tests

```
Your Prompt: "Write a method to submit the order"

AI Response: "I'd be happy to help with PAL application submission! Following
             Article IV, Section 4.1 (Atomic TDD Law), we need to start with
             a failing test.

             **What behavior should we test first?**
             - Status changes to SUBMITTED?
             - Timestamp is recorded?
             - Validation prevents non-DRAFT submission?

             Let's write the first test:

             ```java
             @Test
             void submitApplication_validDraft_changesStatusToSubmitted() {
                 // GIVEN
                 PalApplication draft = createDraftOrder();

                 // WHEN
                 PalApplication result = service.submitApplication(draft.getId());

                 // THEN
                 assertThat(result.getStatus()).isEqualTo(SUBMITTED);
             }
             ```

             Run this and confirm it fails, then I'll help with the implementation."
```

**What AI Teaches:**
- Tests come first (Article IV)
- One behavior at a time (Atomic)
- Test structure (Given-When-Then)

---

## Pattern: Complexity Correction

### When Code is Too Complex

```
Your Prompt: "Here's my method, any feedback?"

AI Response: "I see a Constitutional issue. Per Article III, Section 3.2,
             cyclomatic complexity must be ≤10. This method has complexity 14.

             **Sources of complexity:**
             - Lines 5-15: Nested if-else (4 branches)
             - Lines 20-35: Another nested block (3 branches)
             - Lines 40-50: Switch with 7 cases

             **Recommended fixes:**

             1. **Extract validation to separate method:**
             ```java
             private void validateForSubmission(PalApplication application) {
                 // Move lines 5-15 here
             }
             ```

             2. **Use early returns instead of nesting:**
             ```java
             if (order == null) return;
             if (!application.isDraft()) throw new IllegalStateException(...);
             // Continue with happy path
             ```

             3. **Replace switch with polymorphism or Map:**
             ```java
             private static final Map<Type, Handler> HANDLERS = Map.of(
                 TYPE_A, new TypeAHandler(),
                 TYPE_B, new TypeBHandler()
             );
             ```

             Shall I refactor one section at a time, keeping tests green?"
```

**What AI Teaches:**
- Complexity limits (Article III)
- How to measure and reduce complexity
- Safe refactoring patterns

---

## Pattern: Law of Demeter Fix

### When Chains Appear

```
Your Prompt: "Is this code okay?
             applicant.getAddress().getCity().toUpperCase()"

AI Response: "This violates the Law of Demeter (Article III, Section 3.4).
             You're reaching through multiple objects.

             **The Problem:**
             - Code knows internal structure of Customer and Address
             - If Address changes, this code breaks
             - Hard to mock in tests

             **The Fix:**

             Option 1: **Add behavior to Customer**
             ```java
             // In Customer class
             public String getCityUpperCase() {
                 return address != null && address.getCity() != null
                     ? address.getCity().toUpperCase()
                     : "";
             }

             // Usage
             applicant.getCityUpperCase();
             ```

             Option 2: **Pass what you need**
             ```java
             // Instead of passing Customer
             public void process(String city) {
                 String upper = city.toUpperCase();
             }

             // Caller extracts what's needed
             process(applicant.getAddress().getCity());
             ```

             Which approach fits your use case better?"
```

**What AI Teaches:**
- Law of Demeter principle
- Why it matters (maintainability, testability)
- Multiple solution patterns

---

## Pattern: DDD Guidance

### When Domain Modeling

```
Your Prompt: "Should Order be an entity or value object?"

AI Response: "Following Article II, Section 2.0 (DDD Law), let's analyze:

             **Entity Characteristics:**
             ✅ Has identity (order ID)
             ✅ Has lifecycle (DRAFT → SUBMITTED → SHIPPED → DELIVERED)
             ✅ Changes over time (status, dates)
             ✅ Needs to be tracked

             **Value Object Characteristics:**
             ❌ Not defined by attributes only
             ❌ Not interchangeable
             ❌ Needs to be unique, not equal by value

             **Conclusion: Order is an Entity**

             **Rich Domain Model:**
             ```java
             @Entity
             public class PalApplication {
                 @Id
                 private Long id;  // Identity

                 private ApplicationStatus status;

                 // Behavior belongs here
                 public void submit() {
                     validateCanSubmit();
                     this.status = SUBMITTED;
                     this.submittedAt = LocalDateTime.now();
                 }

                 public void ship() {
                     validateCanShip();
                     this.status = SHIPPED;
                 }

                 private void validateCanSubmit() {
                     if (this.status != DRAFT) {
                         throw new IllegalStateException(
                             \"Only DRAFT orders can be submitted\"
                         );
                     }
                 }
             }
             ```

             **Key points:**
             - Business logic in entity, not service
             - Validation inside entity methods
             - No public setters for status"
```

**What AI Teaches:**
- Entity vs Value Object distinction
- Rich domain model pattern
- Where business logic belongs

---

## Pattern: Test Architecture Guidance

### When Choosing Test Type

```
Your Prompt: "Should I use @SpringBootTest for this service test?"

AI Response: "Following Article IV, Section 4.2 (Test Pyramid Law):

             **Test Pyramid Distribution:**
             - 70-80%: Unit tests (fast, no Spring)
             - 15-25%: Integration tests (controller layer only)
             - 5-10%: E2E tests

             **For Service Layer:**
             Use **unit tests**, not integration tests.

             ❌ Don't do this:
             ```java
             @SpringBootTest  // Heavy, slow
             public class PalApplicationServiceTest {
                 @Autowired
                 private PalApplicationService service;
             }
             ```

             ✅ Do this:
             ```java
             @ExtendWith(MockitoExtension.class)  // Fast, no Spring
             public class PalApplicationServiceTest {
                 @InjectMocks
                 private PalApplicationServiceImpl service;

                 @Mock  // Only mock external I/O
                 private GraphMailService graphMailService;

                 // Use real domain objects, not mocks
             }
             ```

             **When to use @SpringBootTest:**
             - Controller integration tests
             - Testing full HTTP request/response cycle
             - Testing security configurations"
```

**What AI Teaches:**
- Test pyramid proportions
- Which test type for which layer
- Why fast tests matter

---

## Pattern: Refactoring Guidance

### During GREEN → REFACTOR

```
Your Prompt: "Test passes. How should I refactor?"

AI Response: "Great! Following Article I, Section 1.5 (Boy Scout Rule), let's
             improve this code while keeping tests green.

             **I see these opportunities:**

             1. **Extract Method** (Lines 10-25)
                These lines handle validation - extract to `validateRequest()`

             2. **Improve Names**
                - `x` → `applicationId`
                - `doProcess()` → `submitApplication()`

             3. **Remove Duplication**
                Lines 30-35 and 50-55 are nearly identical

             4. **Apply Immutability**
                `submittedDate` should be final after assignment

             **Safe Order:**
             1. Rename variables (low risk)
             2. Extract methods (medium risk)
             3. Remove duplication (verify behavior)

             Which would you like to start with? Remember: run tests after
             each change!"
```

**What AI Teaches:**
- Boy Scout Rule application
- Safe refactoring order
- Test-after-each-change discipline

---

## Pattern: Vertical Slice Planning

### When Planning Features

```
Your Prompt: "I need to add email notifications to the PAL application workflow"

AI Response: "Following Article V (Vertical Slice Development), let's plan
             this incrementally.

             **Vertical Slices (smallest working increments):**

             **Slice 1: Basic Email on Submit** (Day 1)
             - Send simple text email when order submitted
             - Email service integration (mocked in tests)
             - Template: 'Your order {id} has been submitted'

             **Slice 2: Rich Email Template** (Day 2)
             - HTML email with order details
             - Template engine integration
             - Responsive design for mobile

             **Slice 3: Shipping/Delivery Emails** (Day 3)
             - Different templates for different statuses
             - Include tracking information

             **Slice 4: Email Preferences** (Day 4)
             - User can opt-out
             - Preferences storage

             **Hangar SDD Proposal Structure:**
             ```markdown
             ## Slice 1: Basic Email on Submit

             Files:
             - EmailNotificationService.java
             - EmailNotificationServiceTest.java
             - PalApplicationService.java (update)

             Tests:
             - submitApplication_success_sendsEmail
             - submitApplication_emailFails_stillSubmits
             ```

             Start with Slice 1?"
```

**What AI Teaches:**
- Vertical slice thinking
- Incremental delivery
- Hangar SDD proposal structure

---

## What AI Will NOT Do

### Won't Skip Tests

```
You: "Just give me the implementation, I'll test later"
AI: "Per Article IV, Section 4.1, we need a failing test first..."
```

### Won't Ignore Complexity

```
You: "This works, ship it"
AI: "I notice complexity is 15 (Article III requires ≤10). Let me
     suggest some refactoring before we consider this complete..."
```

### Won't Write Untestable Code

```
You: "Add this static method"
AI: "Static methods are hard to test. Following Article IV, let me
     suggest an injectable service pattern instead..."
```

### Won't Create Technical Debt

```
You: "Quick hack, we'll fix later"
AI: "Per Article I, Section 1.5, 'later' rarely comes. Let me show
     you a clean approach that takes about the same time..."
```

---

## Interpreting AI Responses

### When AI Says "Following Article..."

**Meaning:** AI is teaching you a Constitutional principle.
**Action:** Learn the principle, apply it.

### When AI Suggests Tests First

**Meaning:** Article IV (TDD) requires test-first.
**Action:** Write the test, see it fail, then implement.

### When AI Offers Multiple Options

**Meaning:** There's a design decision to make.
**Action:** Understand trade-offs, choose based on context.

### When AI Points Out Violations

**Meaning:** Code doesn't meet Constitutional standards.
**Action:** Fix before proceeding or committing.

---

## The Three Constitutions in AI Responses

AI will reference different constitutions based on context:

| When AI Says... | It's Referencing... |
|-----------------|---------------------|
| "Per Engineering Constitution, Article IV..." | [Engineering Constitution](../../../laws/engineering/) - Testing, code quality |
| "Following Product Constitution, Article III..." | [Product Constitution](../../../laws/product/) - User journeys, metrics |
| "Per Business Constitution, Article XII..." | [Business Constitution](../../../laws/business/) - Compliance, aviation |

### Aviation Compliance Responses

When working on aviation systems, AI will enforce compliance:

```
Your Prompt: "Implement the TSA vetting check for PAL applications"

AI Response: "Following the Aviation/FAA Adoption (TSA Requirements section) and
             the Cargo & Freight product adoption:

             **Compliance Requirements:**
             - All vetting decisions must be auditable
             - VettingAnswer entities must be immutable once submitted
             - TSA response must be logged with timestamp

             **First test (Article IV - Atomic TDD):**
             ```java
             @Test
             void vetApplicant_validRequest_recordsAuditTrail() {
                 // GIVEN - PAL application with applicant details
                 ...
             }
             ```

             This ensures we meet TSA audit requirements while following TDD."
```

---

## Related Guides

- [Prompt Patterns](./prompt-patterns.md) - How to ask AI effectively
- [AI-Engineer Pairing Law](../constitution/ai-engineer-pairing-law.md) - The pairing model
- [Constitution Overview](../constitution/constitution-overview.md) - All three constitutions
- [Atomic TDD Law](../constitution/atomic-tdd-law.md) - TDD requirements
- [Aviation/FAA Adoption](../../../avatars/industry/aviation-faa/ADOPTION.md) - Aviation compliance

---

**Last Updated:** January 28, 2026
