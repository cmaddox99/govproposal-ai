# Prompt Patterns for Spec-Driven Development

**Purpose:** Learn effective prompt patterns for AI-assisted development following Constitutional practices.

**Time to Read:** 25 minutes

---

## Why Prompt Patterns Matter

Effective prompts:
- Guide AI to produce Constitutional code
- Reduce back-and-forth iterations
- Teach AI your project context
- Ensure consistent quality

Poor prompts:
- Get generic responses
- Miss Constitutional requirements
- Require extensive rework
- Waste time

---

## Core Prompt Patterns

### Pattern 1: Context-First

**Always provide context before asking for code.**

```
❌ BAD - No context
"Write a submit method"

✅ GOOD - Context first
"I'm working on PalApplicationService. Following Article IV (Atomic TDD),
I need a submit method that:
- Changes status from DRAFT to SUBMITTED
- Records submission timestamp
- Validates the order is in DRAFT status

What's the first test I should write?"
```

**Template:**
```
Context: [Where you're working, what exists]
Constitutional Reference: [Relevant Article/Section]
Requirement: [What you need]
Question: [Specific ask]
```

---

### Pattern 2: TDD-Guided

**Ask for tests before implementation.**

```
❌ BAD - Ask for implementation
"Implement the rejection workflow for orders"

✅ GOOD - TDD approach
"I need to implement order rejection.
Following Article IV, Section 4.1 (Atomic TDD), help me:
1. List the behaviors I should test
2. Write the first failing test
3. Guide me through RED-GREEN-REFACTOR"
```

**Template:**
```
Feature: [What you're building]
Following Atomic TDD, help me:
1. Identify behaviors to test
2. Write one failing test
3. Guide through the cycle
```

---

### Pattern 3: Refactoring Request

**Ask for improvements after tests pass.**

```
❌ BAD - Vague refactoring
"Make this code better"

✅ GOOD - Specific refactoring
"My test passes. Following Article I, Section 1.5 (Boy Scout Rule),
help me refactor this method:
- Current complexity is 12 (target ≤10)
- Uses `applicant.getAddress().getCity()` (Law of Demeter violation)
- Has a 45-line method

What's the safest first refactoring step?"
```

**Template:**
```
Tests are GREEN. Following [Article/Section], help me refactor:
- Issue 1: [Specific problem]
- Issue 2: [Specific problem]
Keep tests passing. What's the first safe step?
```

---

### Pattern 4: Code Review Request

**Ask AI to review against Constitution.**

```
❌ BAD - Generic review
"Review this code"

✅ GOOD - Constitutional review
"Review this service method against the Constitution:
- Article III: Complexity ≤10, Cognitive ≤7
- Article II: Law of Demeter
- Article IV: Is it testable?

```java
public void processApplication(Long id) {
    // ... code ...
}
```

What violations do you see?"
```

**Template:**
```
Review this code against:
- [Article/Section]: [Requirement]
- [Article/Section]: [Requirement]

[Code block]

What violations exist and how do I fix them?
```

---

### Pattern 5: Hangar SDD Proposal Help

**Get help structuring proposals.**

```
❌ BAD - Vague feature request
"Help me plan the email notification feature"

✅ GOOD - Hangar SDD-structured
"Help me create a Hangar SDD proposal for email notifications.
Following Article V (Vertical Slice Development):
1. What vertical slices should I define?
2. What should Slice 1 include (minimal working feature)?
3. What tests define 'done' for each slice?"
```

**Template:**
```
Feature: [Description]
Help me create a Hangar SDD proposal:
1. Define vertical slices (per Article V)
2. List files for Slice 1
3. Define acceptance criteria
4. Identify what's out of scope
```

---

### Pattern 6: Error Resolution

**Get help fixing test failures or errors.**

```
❌ BAD - Just paste error
"I'm getting this error: NullPointerException"

✅ GOOD - Full context
"My test is failing with NullPointerException.

Test:
```java
@Test
void submitApplication_validDraft_changesStatus() {
    PalApplication application = orderService.submitApplication(1L);
    assertThat(application.getStatus()).isEqualTo(SUBMITTED);
}
```

Error:
```
NullPointerException at PalApplicationService.submitApplication(line 42)
```

Following TDD, what's the minimum fix to make this pass?"
```

**Template:**
```
Test failing with [Error type]

Test code: [test]
Error message: [full error]
Code under test (if relevant): [code]

Following TDD, what's the minimum fix?
```

---

### Pattern 7: Domain Design Help

**Get DDD guidance.**

```
❌ BAD - Generic design question
"How should I design the PalApplication entity?"

✅ GOOD - DDD-focused
"Following Article II (DDD Law), help me design Order:
1. Is this an Entity or Value Object?
2. What behaviors should live in the entity?
3. What's the aggregate boundary?
4. Show me a rich domain model implementation"
```

**Template:**
```
Following Article II (DDD), help me design [Concept]:
1. Entity or Value Object?
2. What behaviors belong here?
3. What's the aggregate boundary?
4. Show example with business methods
```

---

### Pattern 8: Legacy Code Help

**Get safe approaches for brownfield work.**

```
❌ BAD - Just ask to change it
"Refactor this legacy method"

✅ GOOD - Safe approach
"This legacy method has no tests (120 lines, complexity 18).
Following Article I, Section 1.5 (Continuous Refactoring):
1. Help me write characterization tests first
2. Then guide me through safe refactoring
3. Keep tests green throughout"
```

**Template:**
```
Legacy code with no tests. Following safe refactoring:
1. Write characterization tests (capture current behavior)
2. Guide incremental refactoring
3. Keep tests green

[Code block]

What should my first characterization test capture?
```

---

## Domain-Specific Prompts

### PAL Application Processing Prompts

```
"I'm adding email confirmation to PAL application submission.
Following Article IV (Atomic TDD):
1. The email service is external I/O (should be mocked)
2. Need to verify email is sent after successful submit
Write a test that mocks the email service"
```

### Price Calculation Prompts

```
"The price calculation has multiple rates and discounts.
Following Article III, Section 3.2 (Complexity ≤10):
- Current complexity is 15
- Multiple nested if-else for discount tiers
Help me refactor using the Strategy pattern"
```

### External API Integration Prompts

```
"I need to add WireMock tests for the iCargo service integration.
Following Article IV, Section 4.2 (Test Pyramid):
- This is a contract test (15-25% of tests)
- Should test happy path and error scenarios
Help me create the WireMock stub and test"
```

---

## Anti-Patterns to Avoid

### ❌ Asking for Complete Features

```
BAD: "Implement the entire user registration system"
GOOD: "What's the first vertical slice for user registration?"
```

### ❌ Skipping the Test Step

```
BAD: "Write the submit method"
GOOD: "Write a failing test for the submit method's first behavior"
```

### ❌ Vague Requirements

```
BAD: "Make this better"
GOOD: "This has complexity 15 (target ≤10). What's the first extraction?"
```

### ❌ Ignoring Constitutional Context

```
BAD: "How do I structure this service?"
GOOD: "Following Article II (DDD) and Article III (Complexity), how should I structure this service?"
```

### ❌ Mixing Concerns

```
BAD: "Add email sending to the submit method"
GOOD: "I've tested status change. Now I need to add email (external I/O).
       Should I mock the email service in my test?"
```

---

## Prompt Chaining

Use a series of prompts to build incrementally:

### Chain 1: Feature Planning
```
Prompt 1: "Help me create vertical slices for [feature]"
Prompt 2: "What files do I need for Slice 1?"
Prompt 3: "Write a Hangar SDD proposal for this"
```

### Chain 2: TDD Implementation
```
Prompt 1: "What behaviors should I test for [method]?"
Prompt 2: "Write the first failing test"
Prompt 3: "What's the minimum code to pass?"
Prompt 4: "How should I refactor? (tests are green)"
```

### Chain 3: Code Quality
```
Prompt 1: "Review this against Article III (complexity)"
Prompt 2: "How do I extract [identified section]?"
Prompt 3: "Review the extracted method"
```

---

## Context Maintenance

### Keep AI Informed

Update AI about:
- What's already been done
- Current test status (RED/GREEN)
- Files you've changed
- Patterns established

```
"Continuing from last cycle:
- Status change test passes ✅
- Timestamp test passes ✅
Now writing validation test (RED phase).
Here's the test that fails..."
```

### Reference AGENTS.md

```
"Per our AGENTS.md, we use:
- `findXxxById()` pattern for entity loading
- PalApplicationBuilder for test data
- @Transactional on integration tests

Following these patterns, help me write..."
```

---

## Prompt Templates Library

### New Feature Template
```
Feature: [Name]
Context: [What exists, where to add]
Constitutional Requirements:
- Article IV: TDD, 90% coverage
- Article III: Complexity ≤10
- Article II: DDD patterns

Help me:
1. Define vertical slices
2. Write first failing test
3. Guide through implementation
```

### Bug Fix Template
```
Bug: [Description]
Reproduction: [How to see it]
Failing test (if exists): [Test code]
Code under test: [Code]

Following TDD:
1. Write a failing test that exposes this bug
2. Guide me to the minimum fix
```

### Refactoring Template
```
Code to refactor: [Code block]
Tests: ✅ All passing
Issues:
- [Issue 1]
- [Issue 2]

Following Article I, Section 1.5 (Boy Scout Rule):
What's the safest first step?
```

---

## The Three Constitutions

When referencing Constitutional articles, specify which constitution:

| Constitution | When to Reference | Example Articles |
|--------------|-------------------|------------------|
| [Engineering](../../../laws/engineering/) | Code quality, testing, architecture | Article IV (TDD), Article III (Complexity) |
| [Product](../../../laws/product/) | User journeys, metrics, accessibility | Article III (User Journey Laws) |
| [Business](../../../laws/business/) | Compliance, domain rules | Article XII (Aviation Compliance) |

### Aviation Compliance Prompts

When working on aviation-related features, reference the [Aviation/FAA Adoption](../../../avatars/industry/aviation-faa/ADOPTION.md):

```
"Following the Aviation/FAA adoption (DO-178C requirements),
this cargo vetting function needs:
- Full requirements traceability
- TSA compliance validation
- Audit trail for all decisions

Help me design the test coverage approach."
```

---

## Product Domain Prompts

Reference the relevant product domain when working on specific AA systems:

| Domain | Example Prompt |
|--------|----------------|
| [Passenger Booking](../../../avatars/product-type/passenger-booking/ADOPTION.md) | "Following the Booking adoption, implement fare validation with DOT transparency requirements" |
| [Cargo & Freight](../../../avatars/product-type/cargo-freight/ADOPTION.md) | "Following the Cargo adoption, implement PAL application vetting with TSA compliance" |
| [Loyalty](../../../avatars/product-type/loyalty-aadvantage/ADOPTION.md) | "Following the Loyalty adoption, implement miles earning with audit trail requirements" |
| [Airport Operations](../../../avatars/product-type/airport-operations/ADOPTION.md) | "Following the Operations adoption, implement crew scheduling with FAR Part 117 legality checks" |
| [Customer Service](../../../avatars/product-type/customer-service/ADOPTION.md) | "Following the Service adoption, implement rebooking with DOT refund timeline compliance" |

---

## Related Guides

- [Agent Response Patterns](./agent-response-patterns.md) - How AI responds
- [AI-Engineer Pairing Law](../constitution/ai-engineer-pairing-law.md) - Teaching feedback loop
- [Atomic TDD Law](../constitution/atomic-tdd-law.md) - TDD requirements
- [Constitution Overview](../constitution/constitution-overview.md) - All three constitutions

---

**Last Updated:** January 28, 2026
