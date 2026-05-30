# Code Quality Laws

**Purpose:** Master the complexity, immutability, and Law of Demeter requirements that ensure maintainable, AI-friendly code.

**Constitutional Reference:** Article III, Sections 3.2-3.4  
**Time to Read:** 25 minutes

---

## Overview

The Code Quality Laws ensure code is:
- **Readable** - Easy to understand
- **Maintainable** - Easy to change
- **Testable** - Easy to verify
- **AI-Friendly** - Easy for AI to work with

---

## Section 3.2: Complexity Limits and Metrics Law

### The Thresholds (Strictly Enforced)

| Metric | Limit | Build Action |
|--------|-------|--------------|
| Cyclomatic Complexity | ≤ 10 per method | Fail if exceeded |
| Cognitive Complexity | ≤ 7 per method | Fail if exceeded |
| Method Length | ≤ 50 lines | Warning |
| Class Length | ≤ 300 lines | Warning |
| Maximum Parameters | ≤ 4 | Warning |
| Nested Depth | ≤ 3 levels | Warning |
| Code Duplication | < 3% | Fail if exceeded |
| Dependencies per Class | ≤ 7 | Warning |

### Cyclomatic Complexity

**Definition:** Number of linearly independent paths through code.

```java
// Complexity = 1 (no branches)
public String getName() {
    return this.name;
}

// Complexity = 3 (if + else if + else)
public String getStatus(int code) {
    if (code == 200) {
        return "OK";
    } else if (code == 404) {
        return "Not Found";
    } else {
        return "Error";
    }
}

// Complexity = 12 (TOO HIGH - above 10 threshold)
public String processApplication(PalApplication application) {
    if (order == null) return "Error";
    if (application.getItems() == null) return "Error";
    if (application.getItems().isEmpty()) return "Error";
    if (application.getCustomer() == null) return "Error";
    if (application.getCustomer().getAddress() == null) return "Error";
    if (application.getPayment() == null) return "Error";
    if (!application.getPayment().isValid()) return "Error";
    if (application.getTotal().compareTo(BigDecimal.ZERO) <= 0) return "Error";
    // ... more conditions
    return "Success";
}
```

**How to Reduce Cyclomatic Complexity:**

1. **Extract methods:**
```java
// Before: Complexity = 12
public String processApplication(PalApplication application) {
    // ... 12 conditions
}

// After: Complexity = 4 in each method
public String processApplication(PalApplication application) {
    ValidationResult validation = validateOrder(order);
    if (!validation.isValid()) {
        return validation.getErrorMessage();
    }
    return executeOrder(order);
}

private ValidationResult validateOrder(PalApplication application) {
    // ... validation logic
}
```

2. **Use polymorphism:**
```java
// Before: switch with 10 cases
public BigDecimal calculateDiscount(String customerType) {
    switch (customerType) {
        case "GOLD": return new BigDecimal("0.20");
        case "SILVER": return new BigDecimal("0.10");
        // ... 8 more cases
    }
}

// After: Strategy pattern
public interface DiscountStrategy {
    BigDecimal calculate();
}

public BigDecimal calculateDiscount(DiscountStrategy strategy) {
    return strategy.calculate();
}
```

3. **Use early returns:**
```java
// Before: Nested if-else
public void process(PalApplication application) {
    if (order != null) {
        if (application.isValid()) {
            if (order.hasItems()) {
                // process
            }
        }
    }
}

// After: Guard clauses
public void process(PalApplication application) {
    if (order == null) return;
    if (!application.isValid()) return;
    if (!order.hasItems()) return;
    // process
}
```

### Cognitive Complexity

**Definition:** How difficult code is to understand (accounts for nesting and flow breaks).

```java
// Cognitive Complexity = 1
public boolean isAdult(int age) {
    return age >= 18;
}

// Cognitive Complexity = 8 (TOO HIGH - above 7 threshold)
public void processApplications(List<Order> orders) {
    for (PalApplication application : orders) {                      // +1
        if (application.isValid()) {                        // +2 (nesting)
            if (application.getType().equals("EXPRESS")) {  // +3 (nesting)
                if (application.getStatus() == PENDING) {   // +4 (nesting)
                    // process
                } else if (application.getStatus() == DRAFT) {// +1
                    // different process
                }
            }
        }
    }
}
```

**How to Reduce Cognitive Complexity:**

1. **Flatten nesting:**
```java
// Before: Deep nesting
for (PalApplication application : orders) {
    if (application.isValid()) {
        if (application.getType().equals("EXPRESS")) {
            if (application.getStatus() == PENDING) {
                process(order);
            }
        }
    }
}

// After: Flattened with continue
for (PalApplication application : orders) {
    if (!application.isValid()) continue;
    if (!application.getType().equals("EXPRESS")) continue;
    if (application.getStatus() != PENDING) continue;
    process(order);
}
```

2. **Extract to methods with clear names:**
```java
// Before: Complex condition in loop
for (PalApplication application : orders) {
    if (shouldProcessOrder(order)) {
        process(order);
    }
}

private boolean shouldProcessOrder(PalApplication application) {
    return application.isValid()
        && application.getType().equals("EXPRESS")
        && application.getStatus() == PENDING;
}
```

### Verification Commands

```bash
# Run PMD complexity check
mvn pmd:check -Dpmd.maxAllowedViolations=0

# Run CPD duplication check
mvn pmd:cpd-check -Dpmd.cpd.minimumTokens=50

# Generate complexity report
mvn javancss:report
```

---

## Section 3.3: Immutability Law

### The Law

> **Value Objects and DTOs SHALL be immutable.**

### What Must Be Immutable

- All **value objects** (Money, Address, DateRange)
- All **DTOs** used in API requests/responses
- All **configuration objects**
- All **domain events**

### Immutable Class Pattern

```java
// ✅ CORRECT: Immutable value object
public final class Money {
    private final BigDecimal amount;
    private final String currency;
    
    public Money(BigDecimal amount, String currency) {
        this.amount = amount;
        this.currency = currency;
    }
    
    // No setters - object cannot change after construction
    
    public BigDecimal getAmount() { 
        return amount; 
    }
    
    public String getCurrency() { 
        return currency; 
    }
    
    // Methods return NEW instances
    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new IllegalArgumentException("Currency mismatch");
        }
        return new Money(this.amount.add(other.amount), this.currency);
    }
    
    public Money multiply(int quantity) {
        return new Money(this.amount.multiply(BigDecimal.valueOf(quantity)), this.currency);
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Money money = (Money) o;
        return Objects.equals(amount, money.amount) && 
               Objects.equals(currency, money.currency);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(amount, currency);
    }
}
```

```java
// ❌ WRONG: Mutable object with setters
public class Money {
    private BigDecimal amount;
    private String currency;
    
    public void setAmount(BigDecimal amount) { 
        this.amount = amount;  // Can be changed anytime!
    }
    
    public void setCurrency(String currency) { 
        this.currency = currency;  // Can be changed anytime!
    }
}
```

### Benefits of Immutability

1. **Thread-safe by design** - No synchronization needed
2. **Easier to reason about** - State never changes unexpectedly
3. **Can be safely shared** - No defensive copying needed
4. **Enables caching** - Immutable objects can be cached freely
5. **Prevents bugs** - Accidental modification impossible

### What May Be Mutable

- **JPA entities** (Hibernate requires setters)
- **Builder classes** (but `build()` returns immutable)
- **Transient objects** with short lifecycles

### Using Records (Java 17+)

```java
// Immutable DTO with Java record
public record TariffRequest(
    String origin,
    String destination,
    BigDecimal weight,
    String commodity
) {
    // Validation in compact constructor
    public TariffRequest {
        if (origin == null || origin.length() != 3) {
            throw new IllegalArgumentException("Origin must be 3-letter code");
        }
        if (destination == null || destination.length() != 3) {
            throw new IllegalArgumentException("Destination must be 3-letter code");
        }
    }
}
```

---

## Section 3.4: Law of Demeter

### The Law

> **A method of an object should call methods only on:**
> 1. Itself
> 2. Objects passed as parameters
> 3. Objects it creates
> 4. Its direct component objects (fields)

### The Principle: "Talk to Friends, Not Strangers"

```java
// ❌ VIOLATION: Talking to strangers
public void processApplication(PalApplication application) {
    // Reaching through order → customer → address
    String city = application.getCustomer().getAddress().getCity();
    // We know too much about Order's internal structure!
}

// ✅ CORRECT: Talking to friends
public void processApplication(PalApplication application) {
    // Order exposes behavior, not structure
    String city = application.getShippingCity();
}
```

### How to Fix Violations

**1. Tell, Don't Ask**

```java
// ❌ ASK: Get data, make decision externally
if (application.getCustomer().getType().equals("VIP")) {
    applyDiscount(order, 0.20);
}

// ✅ TELL: Tell object what to do
order.applyVipDiscountIfEligible();
```

**2. Encapsulate Navigation**

```java
// ❌ Navigation exposed
public class PalApplication {
    private Applicant applicant;
    
    public Customer getCustomer() {
        return customer;
    }
}

// ✅ Behavior encapsulated
public class PalApplication {
    private Applicant applicant;
    
    public String getShippingCity() {
        return applicant.getShippingCity();
    }
    
    public boolean isVipCustomer() {
        return applicant.isVip();
    }
}

public class Customer {
    private Address address;
    private CustomerType type;
    
    public String getShippingCity() {
        return address.getCity();
    }
    
    public boolean isVip() {
        return type == CustomerType.VIP;
    }
}
```

**3. Create Facade Methods**

```java
// ❌ Exposed internal structure
application.getCustomer().getCompany().getAddress().getCountry();

// ✅ Facade method
application.getShippingCountry();
```

**4. Use DTOs at Boundaries**

```java
// ❌ Passing entity chains to external layers
return customerRepository.findById(id)
    .getOrders()
    .stream()
    .map(o -> o.getItems())
    .flatMap(List::stream)
    .collect(toList());

// ✅ Convert to DTO at boundary
return orderMapper.toOrderSummaryDTO(
    customerRepository.findById(id)
);
```

### Allowed Method Calls

```java
public class PalApplicationService {
    private final PalApplicationRepository repository;  // Field (allowed)
    private final GraphMailService graphMailService;   // Field (allowed)
    
    public void processApplication(PalApplication application) {    // Parameter (allowed)
        // 1. Call method on itself (allowed)
        validateOrder(order);
        
        // 2. Call method on parameter (allowed)
        application.markProcessed();
        
        // 3. Call method on created object (allowed)
        OrderConfirmation confirmation = new OrderConfirmation(order);
        confirmation.generate();
        
        // 4. Call method on field (allowed)
        repository.save(order);
        graphMailService.sendConfirmation(order);
    }
}
```

---

## Prompt Examples for AI Assistance

### Requesting Complexity Reduction

```
Prompt: "This method has cyclomatic complexity of 15. Help me reduce it 
         following Article III, Section 3.2."

AI Response: "I see several ways to reduce complexity while maintaining behavior:

             1. **Extract validation to guard clauses:**
                [shows code]
             
             2. **Extract complex conditions to named methods:**
                [shows code]
             
             3. **Use strategy pattern for type-based logic:**
                [shows code]
             
             After these changes, complexity is reduced to 6.
             
             Shall I apply these refactorings following the Atomic TDD cycle?"
```

### Requesting Immutability Fix

```
Prompt: "Make this DTO immutable according to Article III, Section 3.3."

AI Response: "Following the Immutability Law, I'll convert this to an immutable class:

             **Before (Mutable):**
             ```java
             public class TariffRequest {
                 private String origin;
                 public void setOrigin(String origin) { this.origin = origin; }
             }
             ```
             
             **After (Immutable):**
             ```java
             public final class TariffRequest {
                 private final String origin;
                 
                 public TariffRequest(String origin) {
                     this.origin = Objects.requireNonNull(origin);
                 }
                 
                 public String getOrigin() { return origin; }
             }
             ```
             
             Or using Java records:
             ```java
             public record TariffRequest(String origin) {
                 public TariffRequest {
                     Objects.requireNonNull(origin);
                 }
             }
             ```"
```

### Requesting Law of Demeter Fix

```
Prompt: "This code violates Law of Demeter. Fix it according to Section 3.4."

AI Response: "I see the violation:
             ```java
             application.getCustomer().getAddress().getCity()
             ```
             
             Following 'Tell, Don't Ask', I'll encapsulate this navigation:
             
             **Step 1: Add method to Order:**
             ```java
             public String getShippingCity() {
                 return applicant.getShippingCity();
             }
             ```
             
             **Step 2: Add method to Customer:**
             ```java
             public String getShippingCity() {
                 return address.getCity();
             }
             ```
             
             **Step 3: Update calling code:**
             ```java
             application.getShippingCity()
             ```
             
             Now each class only talks to its direct collaborators."
```

---

## Quality Tool Commands

```bash
# Check all quality metrics
mvn pmd:check                    # Complexity, best practices
mvn pmd:cpd-check               # Code duplication
mvn formatter:validate          # Code style
mvn checkstyle:check            # Additional style rules
mvn spotbugs:check              # Bug patterns

# Generate reports
mvn pmd:pmd                     # PMD report
mvn pmd:cpd                     # Duplication report
mvn site                        # Full site with all reports
```

---

## Refactoring Checklist

When you touch a file, verify:

- [ ] Cyclomatic complexity ≤ 10 for all methods
- [ ] Cognitive complexity ≤ 7 for all methods
- [ ] Methods ≤ 50 lines
- [ ] Classes ≤ 300 lines
- [ ] Parameters ≤ 4 per method
- [ ] Nesting ≤ 3 levels
- [ ] No Law of Demeter violations (no method chaining)
- [ ] Value objects are immutable
- [ ] DTOs are immutable
- [ ] Code duplication < 3%

---

## Related Guides

- [Continuous Refactoring Law](./continuous-refactoring-law.md) - When to apply these rules
- [Atomic TDD Law](./atomic-tdd-law.md) - REFACTOR step applies these rules
- [Domain-Driven Design Law](./ddd-law.md) - Entities and value objects
- [Testing Architecture](../testing/testing-architecture.md) - Testing refactored code

---

**Constitutional Reference:** Article III, Sections 3.2-3.4  
**Last Updated:** January 27, 2026
