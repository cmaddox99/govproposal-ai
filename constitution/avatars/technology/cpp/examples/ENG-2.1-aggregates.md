---
law_id: ENG-2.1
cpp_version_min: 11
avatar: cpp
---

# [ENG-2.1](laws/engineering/eng-2-architecture.md): Aggregate Design — C++ Examples

## The Rule

Aggregates enforce transactional consistency: every mutation goes through the aggregate root, which guarantees invariants hold before and after each operation. Children are never modified directly.

## When to Use

- **Booking aggregate** — `Booking` root owns `Segment`, `Ticket`, and `Payment` children; adding a segment must revalidate the itinerary.
- **Crew roster aggregate** — `CrewRoster` root owns `Assignment` children; swapping a pilot must re-check rest rules (FAR Part 117).
- Any domain object where two or more child entities must stay mutually consistent.

## COMPLIANT: Aggregate Root with Encapsulated Children

```cpp
class Order {
public:
    static Order create(CustomerId customer_id) {
        return Order{OrderId::generate(), std::move(customer_id)};
    }

    void add_item(const Product& product, int quantity) {
        Expects(quantity > 0);
        items_.emplace_back(product, quantity);
        recalculate_total();
    }

    const std::vector<OrderItem>& items() const { return items_; }
    Money total() const { return total_; }

private:
    Order(OrderId id, CustomerId cid) : id_(std::move(id)), customer_id_(std::move(cid)) {}
    void recalculate_total() {
        total_ = Money::zero();
        for (const auto& item : items_) total_ = total_ + item.subtotal();
    }
    OrderId id_;
    CustomerId customer_id_;
    std::vector<OrderItem> items_;
    Money total_{Money::zero()};
};
```

**Why compliant:** Root entity owns children (`items_`). State changes go through root methods. Invariants enforced internally.

## NON-COMPLIANT: Exposed Internal Collection

```cpp
struct Order {
    std::vector<OrderItem> items;  // Public — anyone can mutate
    Money total;                    // Can become inconsistent with items
};
```

**Why non-compliant:** No encapsulation. External code can modify items without updating total. Aggregate invariants not enforced.

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Aggregate too large (hundreds of children) | Hydration takes >50 ms; memory spikes on every domain operation | Split on performance boundary — children over a certain count connect by ID reference; load on demand |
| Cross-aggregate transaction needed | Two aggregates must change atomically; distributed transaction is complex and fragile | Re-examine aggregate boundaries; use domain events for eventual consistency between aggregates instead |
| Aggregate root bypassed to mutate a child directly | Child state changes without the root re-validating invariants; domain rules silently broken | Only expose children via root methods; never return a mutable reference to a child from the root |
