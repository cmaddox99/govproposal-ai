# Continuous Refactoring Law

**Purpose:** Understand how to apply the Boy Scout Rule and refactor continuously without breaking functionality.

**Constitutional Reference:** Article I, Section 1.5  
**Time to Read:** 20 minutes

---

## The Law

> **Engineers SHALL leave code better than they found it. Refactoring MUST be done in small, safe steps with tests protecting every change.**

---

## The Boy Scout Rule

> "Always leave the campground cleaner than you found it."

Applied to code: Every time you touch code, improve it slightly.

### What "Better" Means

| Area | Before | After |
|------|--------|-------|
| **Names** | `process()`, `doIt()` | `calculateTariff()`, `submitApplication()` |
| **Methods** | 50+ lines | 10-15 lines, single purpose |
| **Complexity** | Nested if/else 5 deep | Guard clauses, early returns |
| **Duplication** | Copy-pasted blocks | Extracted helper methods |
| **Tests** | Missing | Added for changed code |

---

## Safe Refactoring Process

### Step 1: Ensure Test Coverage

**Never refactor without tests.** If tests don't exist, write characterization tests first:

```java
// Step 1: Characterization test - captures current behavior
@Test
void legacyMethod_captureCurrentBehavior() {
    // Given - existing state
    LegacyService service = new LegacyService(dependencies);
    
    // When - call method as-is
    Result result = service.mysteryMethod(input);
    
    // Then - capture what it returns (even if "wrong")
    assertThat(result.getCode()).isEqualTo("XYZ");  // Document current behavior
    assertThat(result.getTotal()).isEqualTo(BigDecimal.valueOf(100.50));
}
```

### Step 2: Make Small Changes

One refactoring at a time:

```java
// Original
public void process(Request r) {
    if (r != null) {
        if (r.getType() != null) {
            if (r.getType().equals("A")) {
                // do A stuff
            } else if (r.getType().equals("B")) {
                // do B stuff
            }
        }
    }
}

// Refactoring 1: Guard clause for null
public void process(Request r) {
    if (r == null || r.getType() == null) {
        return;  // Guard clause
    }
    if (r.getType().equals("A")) {
        // do A stuff
    } else if (r.getType().equals("B")) {
        // do B stuff
    }
}
// ✅ Run tests

// Refactoring 2: Extract method for type A
public void process(Request r) {
    if (r == null || r.getType() == null) {
        return;
    }
    if (r.getType().equals("A")) {
        processTypeA(r);
    } else if (r.getType().equals("B")) {
        // do B stuff
    }
}

private void processTypeA(Request r) {
    // do A stuff
}
// ✅ Run tests

// Refactoring 3: Extract method for type B
// ✅ Run tests

// Refactoring 4: Replace if-else with polymorphism or switch
// ✅ Run tests
```

### Step 3: Run Tests After EVERY Change

```bash
# After each micro-refactoring
./mvnw test -Dtest=AffectedClassTest

# Before committing
./mvnw verify
```

---

## Common Refactoring Patterns

### Extract Method

**When:** Method is too long, or has comments explaining sections

```java
// Before
public void processApplication(PalApplication application) {
    // Validate order
    if (application.getCustomerName() == null) {
        throw new ValidationException("Customer name required");
    }
    if (application.getEmail() == null) {
        throw new ValidationException("Email required");
    }

    // Save to database
    repository.save(order);

    // Send notification
    graphMailService.sendConfirmation(application.getEmail());
}

// After - Each comment becomes a method
public void processApplication(PalApplication application) {
    validateOrder(order);
    saveOrder(order);
    sendConfirmationEmail(order);
}

private void validateOrder(PalApplication application) {
    if (application.getCustomerName() == null) {
        throw new ValidationException("Customer name required");
    }
    if (application.getEmail() == null) {
        throw new ValidationException("Email required");
    }
}

private void saveOrder(PalApplication application) {
    repository.save(order);
}

private void sendConfirmationEmail(PalApplication application) {
    graphMailService.sendConfirmation(application.getEmail());
}
```

### Replace Conditional with Guard Clauses

**When:** Deep nesting makes code hard to follow

```java
// Before - Arrow code
public Money calculateTariff(Shipment shipment) {
    Money result = Money.ZERO;
    if (shipment != null) {
        if (shipment.getItems() != null) {
            if (!shipment.getItems().isEmpty()) {
                for (Item item : shipment.getItems()) {
                    if (item.getWeight() != null) {
                        result = result.add(calculateItemTariff(item));
                    }
                }
            }
        }
    }
    return result;
}

// After - Guard clauses, flat structure
public Money calculateTariff(Shipment shipment) {
    if (shipment == null) {
        return Money.ZERO;
    }
    if (shipment.getItems() == null || shipment.getItems().isEmpty()) {
        return Money.ZERO;
    }
    
    return shipment.getItems().stream()
        .filter(item -> item.getWeight() != null)
        .map(this::calculateItemTariff)
        .reduce(Money.ZERO, Money::add);
}
```

### Replace Temp with Query

**When:** Temporary variables are used only once

```java
// Before
public Money calculateTotal(PalApplication application) {
    Money basePrice = application.getBasePrice();
    Money taxAmount = basePrice.multiply(TAX_RATE);
    Money shippingCost = calculateShipping(order);
    Money total = basePrice.add(taxAmount).add(shippingCost);
    return total;
}

// After - Method calls replace temps
public Money calculateTotal(PalApplication application) {
    return application.getBasePrice()
        .add(calculateTax(order))
        .add(calculateShipping(order));
}

private Money calculateTax(PalApplication application) {
    return application.getBasePrice().multiply(TAX_RATE);
}
```

### Replace Magic Numbers with Constants

**When:** Literal values appear in code

```java
// Before
if (password.length() < 8) {
    throw new ValidationException("Password too short");
}
if (retryCount > 3) {
    throw new LockedException("Account locked");
}

// After
private static final int MINIMUM_PASSWORD_LENGTH = 8;
private static final int MAXIMUM_RETRY_ATTEMPTS = 3;

if (password.length() < MINIMUM_PASSWORD_LENGTH) {
    throw new ValidationException("Password too short");
}
if (retryCount > MAXIMUM_RETRY_ATTEMPTS) {
    throw new LockedException("Account locked");
}
```

### Move Logic to Entity (Anemic → Rich Domain)

**When:** Service manipulates entity internals

```java
// Before - Logic in service
public class PalApplicationService {
    public void rejectApplication(PalApplication application) {
        if (application.getStatus() == ApplicationStatus.SHIPPED) {
            throw new IllegalStateException("Cannot cancel shipped order");
        }
        order.setStatus(ApplicationStatus.CANCELLED);
        order.setCancelledAt(LocalDateTime.now());
        order.setCancelReason("User requested");
    }
}

// After - Logic in entity
public class PalApplication {
    public void cancel(String reason) {
        if (this.status == ApplicationStatus.SHIPPED) {
            throw new IllegalStateException("Cannot cancel shipped order");
        }
        this.status = ApplicationStatus.CANCELLED;
        this.cancelledAt = LocalDateTime.now();
        this.cancelReason = reason;
    }
}

public class PalApplicationService {
    public void rejectApplication(Long applicationId, String reason) {
        PalApplication application = repository.findById(applicationId)
            .orElseThrow(() -> new NotFoundException("Order not found"));
        order.cancel(reason);  // Entity handles its own logic
        repository.save(order);
    }
}
```

---

## When NOT to Refactor

### ❌ Without Tests

```java
// STOP! No tests = no safety net
// Write characterization tests FIRST
```

### ❌ During Feature Work

```java
// Don't mix refactoring with features
// Commit 1: Refactoring only (separate PR)
// Commit 2: Feature work
```

### ❌ Big Bang Refactoring

```java
// Don't rewrite entire classes at once
// Small steps, tested at each step
```

### ❌ Premature Optimization

```java
// Don't optimize unless there's a measured problem
// "Premature optimization is the root of all evil" - Knuth
```

---

## Refactoring with AI Assistance

### Prompt Pattern: Safe Refactoring

```
Prompt: "This method is 80 lines. Help me refactor safely."

AI Response: "Following Article I, Section 1.5 (Continuous Refactoring Law), 
             I'll guide you through safe, incremental refactoring.
             
             **Step 1: Test Coverage Check**
             First, let's verify test coverage exists:
             ```bash
             ./mvnw jacoco:check -Djacoco.file=target/jacoco.exec
             ```
             
             **Step 2: Characterization Test (if needed)**
             If tests are missing, we add them first to capture current behavior.
             
             **Step 3: Identify Extract Candidates**
             I see these logical sections:
             - Lines 10-25: Validation logic
             - Lines 26-45: Database operations  
             - Lines 46-70: Email formatting
             - Lines 71-80: Notification sending
             
             **Step 4: Refactor One at a Time**
             Let's start with extracting validation..."
```

### Prompt Pattern: Complexity Reduction

```
Prompt: "This method has complexity 15, need to reduce to ≤10"

AI Response: "Per Article III, Section 3.2 (Cyclomatic Complexity ≤10), I'll 
             reduce complexity safely.
             
             **Current Complexity Sources:**
             - 5 if/else branches
             - 3 nested loops
             - 7 early returns
             
             **Refactoring Strategy:**
             1. Replace nested conditionals with guard clauses
             2. Extract loop bodies to separate methods
             3. Use polymorphism for type-based branching
             
             Let me start with the guard clauses..."
```

---

## Refactoring Metrics

### Track Improvement Over Time

```
Before Refactoring:
- Cyclomatic Complexity: 15
- Cognitive Complexity: 12
- Method Length: 80 lines
- Test Coverage: 45%

After Refactoring:
- Cyclomatic Complexity: 7 ✅
- Cognitive Complexity: 5 ✅
- Method Length: 15 lines ✅
- Test Coverage: 95% ✅
```

### Verification Commands

```bash
# Check complexity
./mvnw pmd:check

# Check coverage
./mvnw jacoco:check

# Run all tests
./mvnw verify
```

---

## Integrating with Atomic TDD

Refactoring is built into the TDD cycle:

```
┌─────────────────────────────────────────────────────────┐
│                    ATOMIC TDD CYCLE                     │
│                                                         │
│    RED → GREEN → ⭐ REFACTOR → VERIFY → COMMIT         │
│                       ↑                                 │
│                       │                                 │
│        Continuous Refactoring Law Applied Here          │
│                                                         │
│    - Extract methods                                    │
│    - Improve names                                      │
│    - Reduce duplication                                 │
│    - Apply patterns                                     │
│    - Clean up test code too                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Common Violations

### ❌ "I'll refactor later"

```
// Later never comes
// Technical debt accumulates
// Refactor NOW, in small steps
```

### ❌ Skipping the test check

```
// Refactoring without tests = breaking things
// ALWAYS verify coverage before refactoring
```

### ❌ Big refactoring PRs

```
// 500+ line refactoring PRs are:
// - Hard to review
// - Risky to merge
// - Likely to break things

// Keep refactoring PRs small and focused
```

---

## Related Guides

- [Atomic TDD Law](./atomic-tdd-law.md) - Refactoring as part of TDD
- [Code Quality Laws](./code-quality-laws.md) - Complexity targets
- [Characterization Testing](../testing/characterization-testing.md) - Tests for legacy code
- [Brownfield Adoption](../adoption/brownfield-adoption.md) - Refactoring existing projects

---

**Constitutional Reference:** Article I, Section 1.5  
**Last Updated:** January 27, 2026
