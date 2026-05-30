---
law_id: ENG-3.2
avatar: dotnet-core
---

# ENG-3.2: Immutability Law Examples for .NET/C#

## COMPLIANT: Immutable Value Object (C# Record)

```csharp
// C# record: immutable by default with value equality
public record Money(decimal Amount, string Currency)
{
    // Validation in constructor
    public Money(decimal Amount, string Currency) : this(Amount, Currency)
    {
        if (Amount < 0)
            throw new ArgumentException("Amount cannot be negative", nameof(Amount));
        if (string.IsNullOrWhiteSpace(Currency))
            throw new ArgumentException("Currency is required", nameof(Currency));
    }

    public static Money Zero(string currency = "USD") => new(0m, currency);

    /// Returns a new Money instance -- does not mutate.
    public Money Add(Money other)
    {
        ValidateSameCurrency(other);
        return this with { Amount = Amount + other.Amount };
    }

    /// Returns a new Money instance -- does not mutate.
    public Money Multiply(decimal factor) => this with { Amount = Amount * factor };

    private void ValidateSameCurrency(Money other)
    {
        if (Currency != other.Currency)
            throw new CurrencyMismatchException(Currency, other.Currency);
    }
}
```

### Init-Only Properties

```csharp
// Init-only properties prevent mutation after construction
public class FlightSearchCriteria
{
    public required string Origin { get; init; }
    public required string Destination { get; init; }
    public required DateOnly DepartureDate { get; init; }
    public int PassengerCount { get; init; } = 1;

    public FlightSearchCriteria WithDate(DateOnly newDate) =>
        new()
        {
            Origin = Origin,
            Destination = Destination,
            DepartureDate = newDate,
            PassengerCount = PassengerCount
        };
}
```

### ImmutableList for Collections

```csharp
using System.Collections.Immutable;

public record Order(string Id, ImmutableList<LineItem> Items, OrderStatus Status)
{
    public static Order Create(string id) =>
        new(id, ImmutableList<LineItem>.Empty, OrderStatus.Draft);

    public Order AddItem(LineItem item) =>
        this with { Items = Items.Add(item) };

    public Order RemoveItem(string itemId) =>
        this with { Items = Items.RemoveAll(i => i.Id == itemId) };

    public Order WithStatus(OrderStatus newStatus) =>
        this with { Status = newStatus };

    public Money Total => Items.Aggregate(
        Money.Zero(), (sum, item) => sum.Add(item.Total));
}
```

**Why compliant:** C# records provide immutability with value equality. `init` setters prevent mutation after construction. `ImmutableList<T>` ensures collections cannot be modified in place. The `with` expression creates modified copies without mutating the original.

---

## VIOLATION: Mutable Class with Setters

```csharp
// BAD: Mutable class with public setters
public class Money
{
    // VIOLATION: Public setters allow uncontrolled mutation
    public double Amount { get; set; }   // Also wrong: using double for money
    public string Currency { get; set; }

    public Money(double amount, string currency)
    {
        Amount = amount;
        Currency = currency;
    }

    // VIOLATION: Mutates internal state
    public void Add(Money other)
    {
        Amount += other.Amount;
    }
}

// Usage showing problems with mutability
var price = new Money(10.0, "USD");
var tax = new Money(1.0, "USD");
price.Add(tax); // price is now mutated -- other references see the change
price.Amount = -999; // No protection against invalid state

// VIOLATION: Mutable list exposed
public class Order
{
    // VIOLATION: Mutable list property
    public List<LineItem> Items { get; set; } = new();
    public OrderStatus Status { get; set; }

    public void AddItem(LineItem item)
    {
        Items.Add(item);
    }
}

var order = new Order();
order.Items.Clear();  // Bypasses business logic
order.Items = new List<LineItem>(); // Replaces entire list
order.Status = OrderStatus.Delivered; // No validation
```

**Why violates ENG-3.2:** Public setters allow any caller to mutate internal state without validation. Mutable collections exposed through properties can be modified or replaced externally. In-place mutation breaks thread safety and makes bugs difficult to trace when objects are shared across services.

---

## Quick Reference

| Pattern | Mutable (Avoid) | Immutable (Prefer) |
|---------|-----------------|---------------------|
| Value Object | `class` with `{ get; set; }` | `record` type |
| Properties | `{ get; set; }` | `{ get; init; }` |
| Collections | `List<T>` | `ImmutableList<T>` / `IReadOnlyList<T>` |
| Dictionary | `Dictionary<K,V>` | `ImmutableDictionary<K,V>` |
| State change | `obj.Prop = val` | `obj with { Prop = val }` |
