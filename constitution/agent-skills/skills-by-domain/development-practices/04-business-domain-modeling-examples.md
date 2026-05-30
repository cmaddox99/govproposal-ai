> Examples for: skill-04-business-domain-modeling  
> Parent skill: 04-business-domain-modeling.md  
> These are optional pedagogical supplements — not in governance scope.

---

## Good Examples

### Example 1: E-commerce Order Aggregate

**Context:** Order processing in a sales system

**Aggregate Design:**

```java
/**
 * Order Aggregate
 *
 * Invariants:
 * - Order total must equal sum of line totals
 * - Cannot modify order after shipping
 * - At least one item required to place order
 */
public class PalApplication {  // Aggregate Root
    private final OrderId id;
    private final CustomerId customerId;
    private final List<OrderLine> lines;  // Aggregate member
    private ApplicationStatus status;
    private Money total;

    // Factory method ensures valid creation
    public static Order create(CustomerId customerId) {
        return new Order(
            OrderId.generate(),
            customerId,
            new ArrayList<>(),
            ApplicationStatus.DRAFT,
            Money.ZERO
        );
    }

    // Behavior method, not setter
    public void addItem(Product product, Quantity quantity) {
        ensureModifiable();  // Invariant check

        OrderLine existingLine = findLineFor(product);
        if (existingLine != null) {
            existingLine.increaseQuantity(quantity);
        } else {
            lines.add(OrderLine.create(product, quantity));
        }

        recalculateTotal();  // Maintain invariant
    }

    public void removeItem(ProductId productId) {
        ensureModifiable();
        lines.removeIf(line -> line.isFor(productId));
        recalculateTotal();
    }

    public void place() {
        if (lines.isEmpty()) {
            throw new EmptyOrderException();
        }
        this.status = ApplicationStatus.PLACED;
        // Raise domain event
        DomainEvents.raise(new OrderPlaced(this.id, this.customerId, this.total));
    }

    private void ensureModifiable() {
        if (status != ApplicationStatus.DRAFT) {
            throw new OrderNotModifiableException(id, status);
        }
    }

    private void recalculateTotal() {
        this.total = lines.stream()
            .map(OrderLine::getLineTotal)
            .reduce(Money.ZERO, Money::add);
    }
}

/**
 * Value Object - immutable, no identity
 */
public final class Money {
    private final BigDecimal amount;
    private final Currency currency;

    public Money(BigDecimal amount, Currency currency) {
        if (amount.compareTo(BigDecimal.ZERO) < 0) {
            throw new NegativeMoneyException();
        }
        this.amount = amount;
        this.currency = currency;
    }

    public Money add(Money other) {
        ensureSameCurrency(other);
        return new Money(this.amount.add(other.amount), this.currency);
    }

    // Value objects: equality by value
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Money)) return false;
        Money money = (Money) o;
        return amount.equals(money.amount) && currency.equals(money.currency);
    }
}
```

**Why it's good:**
- Order (aggregate root) controls all access
- Invariants enforced in methods
- Behavior lives in the domain, not services
- Value objects are immutable
- Domain events capture significant occurrences

### Example 2: Subscription Domain

**Ubiquitous Language:**

| Term | Definition |
|------|------------|
| **Subscription** | A recurring arrangement for product delivery |
| **Billing Cycle** | The period between charges (monthly, annual) |
| **Pause** | Temporary suspension without cancellation |
| **Churn** | Customer ending their subscription |

**Aggregate:**

```java
public class Subscription {
    private final SubscriptionId id;
    private final CustomerId customerId;
    private Plan plan;
    private BillingCycle billingCycle;
    private SubscriptionStatus status;
    private LocalDate currentPeriodEnd;
    private int pauseCount;

    // Invariant: Cannot pause more than 3 times per year
    private static final int MAX_PAUSES_PER_YEAR = 3;

    public void pause(LocalDate until) {
        ensureActive();

        if (pauseCount >= MAX_PAUSES_PER_YEAR) {
            throw new PauseLimitExceededException(id, MAX_PAUSES_PER_YEAR);
        }

        if (until.isAfter(currentPeriodEnd.plusMonths(3))) {
            throw new PauseDurationExceededException();
        }

        this.status = SubscriptionStatus.PAUSED;
        this.pauseCount++;
        DomainEvents.raise(new SubscriptionPaused(id, until));
    }

    public void resume() {
        if (status != SubscriptionStatus.PAUSED) {
            throw new SubscriptionNotPausedException(id);
        }
        this.status = SubscriptionStatus.ACTIVE;
        DomainEvents.raise(new SubscriptionResumed(id));
    }

    public void changePlan(Plan newPlan) {
        ensureActive();
        if (newPlan.equals(this.plan)) {
            return;  // No change needed
        }

        Plan oldPlan = this.plan;
        this.plan = newPlan;
        DomainEvents.raise(new PlanChanged(id, oldPlan, newPlan));
    }

    public void cancel(CancellationReason reason) {
        ensureNotCancelled();
        this.status = SubscriptionStatus.CANCELLED;
        DomainEvents.raise(new SubscriptionCancelled(id, reason));
    }

    private void ensureActive() {
        if (status != SubscriptionStatus.ACTIVE) {
            throw new SubscriptionNotActiveException(id, status);
        }
    }
}
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: Anemic Domain Model

```java
// BAD - Data bag with no behavior

public class PalApplication {
    private Long id;
    private Long customerId;
    private List<OrderLine> lines;
    private String status;
    private BigDecimal total;

    // Only getters and setters - no behavior!
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    // ... more getters/setters
}

// All logic in service
public class PalApplicationService {
    public void addItem(PalApplication application, Product product, int quantity) {
        // Bypasses any invariant checking
        application.getLines().add(new OrderLine(product, quantity));

        // Manually recalculate - easy to forget
        BigDecimal total = BigDecimal.ZERO;
        for (OrderLine line : application.getLines()) {
            total = total.add(line.getTotal());
        }
        order.setTotal(total);
    }
}
```

**Why it's wrong:**
- Business logic scattered in services
- Invariants can be bypassed via setters
- No encapsulation of business rules
- Easy to corrupt object state
- "Object" is just a data structure

### Anti-Pattern 2: Primitive Obsession

```java
// BAD - Using primitives instead of domain concepts

public class PalApplication {
    private String customerId;  // Should be CustomerId
    private double total;       // Should be Money
    private String status;      // Should be ApplicationStatus enum/class
    private String email;       // Should be EmailAddress

    public void setTotal(double total) {
        this.total = total;  // No validation!
    }
}

// In service
order.setTotal(-100.50);  // Invalid but allowed
order.setStatus("INVALID_STATUS");  // Typo goes unnoticed
```

**Why it's wrong:**
- No domain concept validation
- Easy to pass wrong values
- Business rules not enforced
- Loses opportunity for behavior

**Correct approach:**
```java
// Value objects enforce rules
public final class Money {
    private final BigDecimal amount;
    private final Currency currency;

    public Money(BigDecimal amount, Currency currency) {
        if (amount.compareTo(BigDecimal.ZERO) < 0) {
            throw new InvalidMoneyException("Amount cannot be negative");
        }
        this.amount = amount;
        this.currency = currency;
    }
}
```

### Anti-Pattern 3: God Aggregate

```java
// BAD - Aggregate too large, too many responsibilities

public class Customer {
    // Customer info
    private String name;
    private String email;

    // All orders ever (unbounded!)
    private List<Order> orders;

    // All payments ever (unbounded!)
    private List<Payment> payments;

    // All support tickets (unbounded!)
    private List<Ticket> tickets;

    // All product reviews (unbounded!)
    private List<Review> reviews;

    // Methods for everything
    public void addOrder(PalApplication application) { ... }
    public void addPayment(Payment payment) { ... }
    public void addTicket(Ticket ticket) { ... }
    public void addReview(Review review) { ... }
}
```

**Why it's wrong:**
- Aggregate is huge (unbounded collections)
- Different consistency boundaries lumped together
- Performance problems loading entire aggregate
- Changes to orders require loading reviews

**Correct approach:** Separate aggregates with references by ID:
```java
public class Customer { /* just customer info */ }
public class PalApplication { private CustomerId customerId; }
public class Ticket { private CustomerId customerId; }
```

---

## Artifacts & Templates

### Template: Bounded Context Definition

```markdown
# Bounded Context: [Name]

## Purpose
[What this context is responsible for]

## Core Domain Concepts
- [Concept 1]: [Definition]
- [Concept 2]: [Definition]

## Aggregates
- [Aggregate 1] (root: [Entity])
- [Aggregate 2] (root: [Entity])

## Context Relationships
- **Upstream:** [Context that provides data to us]
- **Downstream:** [Context that consumes our data]
- **Partnership:** [Context we collaborate with as equals]

## Integration Patterns
- With [Context X]: [Pattern - Shared Kernel/Customer-Supplier/etc.]

## Team Ownership
[Team responsible for this context]
```

### Template: Aggregate Specification

```markdown
# Aggregate: [Name]

## Root Entity
**[Entity Name]**

## Members
- [Entity/Value Object 1]: [Purpose]
- [Entity/Value Object 2]: [Purpose]

## Invariants
1. [Invariant description]
2. [Invariant description]

## Behaviors
| Method | Purpose | Invariants Checked |
|--------|---------|-------------------|
| [method()] | [Purpose] | [Which invariants] |

## Domain Events Raised
- [EventName]: When [condition]

## Lifecycle
[Creation] → [State 1] → [State 2] → [Terminal State]
```

---

