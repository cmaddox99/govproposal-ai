# Domain-Driven Design Law

**Purpose:** Understand how to apply DDD principles to create rich domain models that encapsulate business logic.

**Constitutional Reference:** Article II, Section 2.0  
**Time to Read:** 25 minutes

---

## The Law

> **The system SHALL adhere to Domain-Driven Design principles with ubiquitous language, rich domain models, and clear aggregate boundaries.**

---

## Core DDD Concepts

### Ubiquitous Language

Use domain terminology consistently in code, tests, and documentation:

```java
// ✅ GOOD - Business language
public class PalApplication {
    public void submit() { }
    public void confirm() { }
    public void cancel(String reason) { }
}

// ❌ BAD - Technical/generic language
public class OrderData {
    public void process() { }
    public void setStatus(int statusCode) { }
    public void updateState(String action) { }
}
```

**Rules:**
- Class names reflect business concepts (`Order`, `Customer`, `Payment`)
- Method names describe business operations (`submit()`, `calculateTotal()`)
- Avoid generic names (`Manager`, `Handler`, `Processor`, `Data`, `Info`)

---

## Entities vs Value Objects

### Entities

Have **identity** and **lifecycle** - tracked over time:

```java
// Entity - Has ID and lifecycle
@Entity
public class PalApplication {
    @Id
    private Long id;  // Identity

    private ApplicationStatus status;
    private LocalDateTime createdAt;
    private LocalDateTime submittedAt;

    // Lifecycle operations
    public void submit() {
        validateCanSubmit();
        this.status = ApplicationStatus.SUBMITTED;
        this.submittedAt = LocalDateTime.now();
    }
}
```

**Characteristics:**
- Unique identifier
- State changes over time
- Equality based on ID, not attributes

### Value Objects

Defined by **attributes**, not identity - immutable:

```java
// Value Object - Immutable, defined by attributes
public final class Money {
    private final BigDecimal amount;
    private final String currency;
    
    public Money(BigDecimal amount, String currency) {
        this.amount = amount;
        this.currency = currency;
    }
    
    // No setters - immutable
    
    // Operations return new instances
    public Money add(Money other) {
        return new Money(this.amount.add(other.amount), this.currency);
    }
    
    // Equality based on attributes
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Money money = (Money) o;
        return Objects.equals(amount, money.amount) && 
               Objects.equals(currency, money.currency);
    }
}
```

**Characteristics:**
- No identity
- Immutable
- Equality based on all attributes
- Interchangeable (two $100 bills are the same)

### Common Value Objects

| Value Object | Attributes | Why Value Object? |
|--------------|------------|-------------------|
| `Money` | amount, currency | $100 = $100 regardless of which bill |
| `Address` | street, city, country | Same address is same address |
| `DateRange` | start, end | Same period is same period |
| `EmailAddress` | email | Can validate format |
| `ProductCode` | code | SKU with format validation |

---

## Aggregates and Aggregate Roots

### What Is an Aggregate?

A cluster of entities and value objects treated as a single unit:

```
┌─────────────────────────────────────────────────────────┐
│                      ORDER AGGREGATE                     │
│                                                         │
│  ┌─────────────────────────────────────┐               │
│  │        Order (ROOT)                 │               │
│  │    - id                             │               │
│  │    - status                         │               │
│  │    - submit()                       │               │
│  │    - confirm()                      │               │
│  └───────────────┬─────────────────────┘               │
│                  │                                      │
│    ┌─────────────┴─────────────┐                       │
│    │                           │                        │
│    ▼                           ▼                        │
│  ┌───────────────┐   ┌─────────────────┐               │
│  │   Customer    │   │    VettingAnswer    │               │
│  │   - name      │   │  - productId    │               │
│  │   - email     │   │  - quantity     │               │
│  │   - address   │   │  - price        │               │
│  └───────────────┘   └─────────────────┘               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Aggregate Rules

**Rule 1: Access children ONLY through the root**

```java
// ✅ CORRECT - Through aggregate root
PalApplication application = orderRepository.findById(id);
application.addItem(productId, quantity, price);
orderRepository.save(order);

// ❌ WRONG - Directly accessing child
VettingAnswer item = orderItemRepository.findById(itemId);
item.setQuantity(newQuantity);  // Bypassing aggregate root!
```

**Rule 2: One repository per aggregate root**

```java
// ✅ CORRECT
@Repository
public interface PalApplicationRepository extends JpaRepository<Order, Long> { }

// ❌ WRONG - Repository for internal aggregate member
@Repository
public interface VettingAnswerRepository extends JpaRepository<VettingAnswer, Long> { }
```

**Rule 3: External references use IDs, not objects**

```java
// ✅ CORRECT - Reference by ID
public class PalApplication {
    private Long customerId;  // Reference to Customer aggregate
}

// ❌ WRONG - Direct object reference across aggregates
public class PalApplication {
    private Applicant applicant;  // Tight coupling between aggregates!
}
```

---

## Rich vs Anemic Domain Models

### The Problem: Anemic Domain Model

Entities with only getters/setters - all logic in services:

```java
// ❌ ANEMIC - Just data, no behavior
public class PalApplication {
    private ApplicationStatus status;

    public ApplicationStatus getStatus() { return status; }
    public void setStatus(ApplicationStatus status) { this.status = status; }
}

// ❌ Logic in service instead of entity
public class PalApplicationService {
    public void submit(Long applicationId) {
        PalApplication application = repository.findById(applicationId);

        // Business logic scattered in service
        if (application.getStatus() != ApplicationStatus.DRAFT) {
            throw new IllegalStateException("Only drafts can be submitted");
        }
        order.setStatus(ApplicationStatus.SUBMITTED);
        order.setSubmittedAt(LocalDateTime.now());

        repository.save(order);
    }
}
```

### The Solution: Rich Domain Model

Entities encapsulate their own business logic:

```java
// ✅ RICH - Behavior in the entity
public class PalApplication {
    private ApplicationStatus status;
    private LocalDateTime submittedAt;

    public void submit() {
        validateCanSubmit();
        this.status = ApplicationStatus.SUBMITTED;
        this.submittedAt = LocalDateTime.now();
    }

    private void validateCanSubmit() {
        if (this.status != ApplicationStatus.DRAFT) {
            throw new IllegalStateException(
                "Only DRAFT orders can be submitted. Current: " + status
            );
        }
    }

    public void confirm() {
        if (this.status != ApplicationStatus.SUBMITTED) {
            throw new IllegalStateException("Only submitted orders can be confirmed");
        }
        this.status = ApplicationStatus.CONFIRMED;
    }
}

// ✅ Service orchestrates, entity encapsulates
public class PalApplicationService {
    public Order submit(Long applicationId) {
        PalApplication application = repository.findById(applicationId)
            .orElseThrow(() -> new NotFoundException("Order not found"));

        application.submit();  // Entity knows how to submit itself

        return repository.save(order);
    }
}
```

### Benefits of Rich Domain Models

1. **Logic is where the data is** - No need to pass data around
2. **Easier to test** - Test entity directly without mocking
3. **Better encapsulation** - Internal state protected
4. **Self-documenting** - Entity shows what operations are valid
5. **Prevents invalid states** - Validation happens inside entity

---

## Domain Services

For operations that don't belong to a single entity:

```java
// Domain Service - Operation spans multiple aggregates
public class PricingService {

    public Money calculateOrderTotal(
            List<VettingAnswer> items,
            Applicant applicant,
            ShippingMethod shipping) {

        Money subtotal = calculateSubtotal(items);
        Money discount = calculateCustomerDiscount(customer, subtotal);
        Money shippingCost = calculateShippingCost(items, shipping);

        return subtotal.subtract(discount).add(shippingCost);
    }
}
```

**Use Domain Services when:**
- Operation doesn't naturally belong to one entity
- Operation requires multiple aggregates
- Operation is a pure domain calculation

**Don't use Domain Services for:**
- Logic that belongs in an entity (use rich domain model)
- Infrastructure concerns (use application services)

---

## Anti-Patterns to Avoid

### ❌ Generic Names

```java
// BAD
class DataManager { }
class ApplicationHandler { }
class OrderProcessor { }
class InfoHelper { }

// GOOD
class PricingCalculator { }
class OrderSubmissionService { }
class OrderFulfillmentService { }
class EmailTemplateGenerator { }
```

### ❌ Setters on Entities

```java
// BAD - Allows invalid state
public class PalApplication {
    public void setStatus(ApplicationStatus status) {
        this.status = status;  // No validation!
    }
}

// GOOD - Behavior methods with validation
public class PalApplication {
    public void confirm() {
        if (this.status != ApplicationStatus.PENDING) {
            throw new IllegalStateException("Only pending orders can be confirmed");
        }
        this.status = ApplicationStatus.CONFIRMED;
        this.confirmedAt = LocalDateTime.now();
    }
}
```

### ❌ Exposing Internal Structure

```java
// BAD - Exposes internal list
public class PalApplication {
    private List<VettingAnswer> items;
    
    public List<VettingAnswer> getItems() {
        return items;  // Can be modified externally!
    }
}

// GOOD - Encapsulated
public class PalApplication {
    private List<VettingAnswer> items = new ArrayList<>();
    
    public void addItem(VettingAnswer item) {
        items.add(item);
        recalculateTotal();
    }
    
    public List<VettingAnswer> getItems() {
        return Collections.unmodifiableList(items);
    }
}
```

---

## Testing Rich Domain Models

With rich domain models, tests become simpler:

```java
// Testing anemic model (complex, lots of mocking)
@Test
public void submit_validDraft_changesStatus() {
    when(repository.findById(1L)).thenReturn(Optional.of(draftOrder));
    when(repository.save(any())).thenReturn(submittedOrder);

    service.submit(1L);

    verify(repository).save(argThat(order ->
        application.getStatus() == ApplicationStatus.SUBMITTED
    ));
}

// Testing rich domain model (simple, no mocking)
@Test
public void submit_validDraft_changesStatus() {
    PalApplication application = PalApplication.createDraft();

    application.submit();

    assertThat(application.getStatus()).isEqualTo(ApplicationStatus.SUBMITTED);
    assertThat(application.getSubmittedAt()).isNotNull();
}
```

---

## Prompt Examples

### Creating a Rich Entity

```
Prompt: "Create an PalApplication entity following DDD principles"

AI Response: "Following Article II, Section 2.0 (Domain-Driven Design Law), I'll
             create a rich domain model with encapsulated behavior.

             ```java
             @Entity
             public class PalApplication {
                 @Id
                 @GeneratedValue
                 private Long id;

                 @Enumerated(EnumType.STRING)
                 private ApplicationStatus status;

                 @Embedded
                 private Applicant applicant;

                 @OneToMany(cascade = CascadeType.ALL)
                 private List<VettingAnswer> items = new ArrayList<>();

                 private LocalDateTime createdAt;
                 private LocalDateTime submittedAt;

                 // Factory method
                 public static Order create(Applicant applicant) {
                     PalApplication application = new Order();
                     order.customer = customer;
                     order.status = ApplicationStatus.DRAFT;
                     order.createdAt = LocalDateTime.now();
                     return order;
                 }

                 // Business behavior
                 public void submit() {
                     validateForSubmission();
                     this.status = ApplicationStatus.SUBMITTED;
                     this.submittedAt = LocalDateTime.now();
                 }

                 public void addItem(Long productId, int quantity, Money price) {
                     if (this.status != ApplicationStatus.DRAFT) {
                         throw new IllegalStateException(\"Cannot modify submitted order\");
                     }
                     this.items.add(new VettingAnswer(productId, quantity, price));
                 }

                 private void validateForSubmission() {
                     if (this.status != ApplicationStatus.DRAFT) {
                         throw new IllegalStateException(\"Only drafts can be submitted\");
                     }
                     if (this.items.isEmpty()) {
                         throw new ValidationException(\"Order must have at least one item\");
                     }
                 }
             }
             ```

             **DDD principles applied:**
             - Rich behavior (submit, addItem)
             - Validation inside entity
             - Aggregate boundary (VettingAnswer is internal)
             - Factory method for creation
             - No setters for status"
```

### Refactoring to Rich Domain

```
Prompt: "This service has too much logic. Help me move it to the entity."

AI Response: "Following DDD (Article II, Section 2.0), I'll identify logic that 
             belongs in the entity vs the service.
             
             **Move to Entity:**
             - Status transitions (draft → submitted → approved)
             - Validation rules
             - Date recording (submittedAt)
             
             **Keep in Service:**
             - Repository operations
             - Email sending (external I/O)
             - Transaction coordination
             
             Let me refactor step by step..."
```

---

## Related Guides

- [Code Quality Laws](./code-quality-laws.md) - Immutability, Law of Demeter
- [Continuous Refactoring Law](./continuous-refactoring-law.md) - Migrating to rich models
- [Testing Architecture](../testing/testing-architecture.md) - Testing domain models
- [Test Pyramid Law](./test-pyramid-law.md) - Domain tests vs integration tests

---

**Constitutional Reference:** Article II, Section 2.0  
**Last Updated:** January 27, 2026
