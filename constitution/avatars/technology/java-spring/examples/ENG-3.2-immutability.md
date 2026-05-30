---
law_id: ENG-3.2
avatar: java-spring
---

# ENG-3.2: Immutability Law Examples for Java/Spring

## COMPLIANT: Immutable Value Object (Java Record)

```java
import java.math.BigDecimal;
import java.util.List;

// Java record: immutable by default, auto-generates equals/hashCode/toString
public record Money(BigDecimal amount, String currency) {

    // Compact constructor for validation
    public Money {
        if (amount.compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
        if (currency == null || currency.isBlank()) {
            throw new IllegalArgumentException("Currency is required");
        }
    }

    public static Money zero(String currency) {
        return new Money(BigDecimal.ZERO, currency);
    }

    /** Returns a new Money instance -- does not mutate. */
    public Money add(Money other) {
        validateSameCurrency(other);
        return new Money(this.amount.add(other.amount), this.currency);
    }

    /** Returns a new Money instance -- does not mutate. */
    public Money multiply(BigDecimal factor) {
        return new Money(this.amount.multiply(factor), this.currency);
    }

    private void validateSameCurrency(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new CurrencyMismatchException(this.currency, other.currency);
        }
    }
}
```

### JPA @Embeddable with No Setters

```java
import jakarta.persistence.Embeddable;
import java.math.BigDecimal;

@Embeddable
public class MoneyVO {

    private BigDecimal amount;
    private String currency;

    // Required by JPA
    protected MoneyVO() {}

    public MoneyVO(BigDecimal amount, String currency) {
        this.amount = amount;
        this.currency = currency;
    }

    // Getters only -- no setters exposed
    public BigDecimal getAmount() { return amount; }
    public String getCurrency() { return currency; }

    public MoneyVO add(MoneyVO other) {
        return new MoneyVO(this.amount.add(other.amount), this.currency);
    }
}
```

### Immutable Collections

```java
import java.util.List;

public record Order(String id, List<LineItem> items, OrderStatus status) {

    // Defensive copy in compact constructor
    public Order {
        items = List.copyOf(items); // unmodifiable snapshot
    }

    public Order addItem(LineItem item) {
        var newItems = new java.util.ArrayList<>(items);
        newItems.add(item);
        return new Order(id, List.copyOf(newItems), status);
    }

    public Order withStatus(OrderStatus newStatus) {
        return new Order(id, items, newStatus);
    }
}
```

**Why compliant:** Java records are immutable by design with final fields. `List.copyOf()` produces unmodifiable collections. All state changes return new instances, making the objects safe to share across threads and domain boundaries.

---

## VIOLATION: Mutable Value Object with Setters

```java
// BAD: Mutable class with setters
public class Money {

    private double amount;   // VIOLATION: Using double for money (precision loss)
    private String currency;

    public Money(double amount, String currency) {
        this.amount = amount;
        this.currency = currency;
    }

    // VIOLATION: Setter allows external mutation
    public void setAmount(double amount) {
        this.amount = amount;
    }

    // VIOLATION: Setter allows external mutation
    public void setCurrency(String currency) {
        this.currency = currency;
    }

    public double getAmount() { return amount; }
    public String getCurrency() { return currency; }

    // VIOLATION: Mutates internal state instead of returning new instance
    public void add(Money other) {
        this.amount += other.amount;
    }
}

// Usage showing problems with mutability
Money price = new Money(10.0, "USD");
Money tax = new Money(1.0, "USD");
price.add(tax); // price is now mutated -- any other reference sees the change

// VIOLATION: Mutable list exposed directly
public class Order {
    private List<LineItem> items = new ArrayList<>();

    // Exposes internal mutable list
    public List<LineItem> getItems() { return items; }

    public void addItem(LineItem item) {
        items.add(item);
    }
}

Order order = new Order();
order.getItems().clear(); // Bypasses encapsulation entirely
```

**Why violates ENG-3.2:** Mutable value objects with setters allow any caller to change internal state, causing subtle bugs when objects are shared. Exposing mutable collections breaks encapsulation. In-place mutation makes the code thread-unsafe and harder to reason about.

---

## Quick Reference

| Pattern | Mutable (Avoid) | Immutable (Prefer) |
|---------|-----------------|---------------------|
| Value Object | `class` with setters | `record` type |
| JPA Value | `@Embeddable` with setters | `@Embeddable` with getters only |
| List field | `new ArrayList<>()` exposed via getter | `List.copyOf()` / `Collections.unmodifiableList()` |
| Map field | `new HashMap<>()` exposed via getter | `Map.copyOf()` / `Collections.unmodifiableMap()` |
| State change | `void setX(val)` | `Foo withX(val)` returning new instance |
