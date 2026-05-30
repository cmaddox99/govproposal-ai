---
law_id: ENG-2.1
avatar: python-fastapi
---

# ENG-2.1: DDD Aggregate Root Examples for Python/FastAPI

## COMPLIANT: Proper Aggregate Root

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Self
from uuid import UUID, uuid4


@dataclass
class Order:
    """Order aggregate root - controls all mutations."""

    id: UUID = field(default_factory=uuid4)
    customer_id: UUID = field(default=None)
    items: list[LineItem] = field(default_factory=list)
    status: OrderStatus = field(default=OrderStatus.DRAFT)
    created_at: datetime = field(default_factory=datetime.utcnow)
    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    def add_item(self, product_id: UUID, quantity: int, price: Money) -> None:
        """Add item through aggregate root - enforces invariants."""
        self._validate_can_modify()
        self.items.append(LineItem(product_id=product_id, quantity=quantity, price=price))

    def submit(self) -> None:
        """Submit order - validates business rules."""
        self._validate_can_submit()
        self.status = OrderStatus.SUBMITTED
        self._events.append(OrderSubmittedEvent(order_id=self.id))

    def _validate_can_modify(self) -> None:
        if self.status != OrderStatus.DRAFT:
            raise OrderCannotBeModifiedError(self.id, self.status)

    def _validate_can_submit(self) -> None:
        if not self.items:
            raise EmptyOrderCannotBeSubmittedError(self.id)

    def collect_events(self) -> list[DomainEvent]:
        """Collect and clear domain events."""
        events = self._events.copy()
        self._events.clear()
        return events
```

**Why compliant:**
- All mutations go through aggregate root methods
- Invariants are enforced internally
- Domain events capture state changes
- Clear transactional boundary

---

## VIOLATION: Anemic Domain Model

```python
# BAD: Entity is just a data container
@dataclass
class Order:
    id: UUID
    customer_id: UUID
    items: list[LineItem]
    status: str  # String instead of enum


# Business logic in service (violation!)
class OrderService:
    def add_item(self, order_id: UUID, product_id: UUID, quantity: int) -> None:
        order = self.repository.find_by_id(order_id)
        if order.status != "DRAFT":  # Logic should be in Order
            raise Exception("Cannot modify")
        order.items.append(LineItem(...))  # Direct manipulation
        self.repository.save(order)
```

**Why violates ENG-2.1:**
- Order is just a data bag with no behavior
- Business rules scattered in services
- No encapsulation of invariants
- Easy to bypass rules by directly manipulating data

---

## Aggregate Boundaries

```python
# Order aggregate contains:
# - Order (root)
# - LineItem (entity within aggregate)
# - Money (value object)

@dataclass
class Order:
    """Aggregate root."""
    id: OrderId
    items: list[LineItem]  # Entities within same aggregate

    @property
    def total(self) -> Money:  # Value object
        return sum((item.total for item in self.items), Money.zero())


@dataclass
class LineItem:
    """Entity within Order aggregate - not accessed directly."""
    product_id: ProductId
    quantity: int
    unit_price: Money

    @property
    def total(self) -> Money:
        return self.unit_price.multiply(self.quantity)


# Customer is a SEPARATE aggregate - reference by ID only
@dataclass
class Order:
    customer_id: CustomerId  # Reference, not embedded
```

**Key principle:** Aggregates reference other aggregates by ID only, never by direct object reference.
