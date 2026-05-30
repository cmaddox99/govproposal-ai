---
law_id: ENG-3.1
avatar: python-fastapi
---

# ENG-3.1: Complexity Limits Examples for Python/FastAPI

## COMPLIANT: Low Complexity Function

```python
from dataclasses import dataclass
from decimal import Decimal
from typing import Sequence

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "USD"

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)


def calculate_order_total(items: Sequence[LineItem]) -> OrderTotal:
    """Calculate order total from line items.

    Cyclomatic complexity: 2
    Cognitive complexity: 1
    """
    if not items:
        return OrderTotal.zero()

    subtotal = sum_line_items(items)
    tax = calculate_tax(subtotal)
    shipping = calculate_shipping(items)

    return OrderTotal(subtotal=subtotal, tax=tax, shipping=shipping)


def sum_line_items(items: Sequence[LineItem]) -> Money:
    """Sum all line item totals."""
    return reduce(
        lambda acc, item: acc.add(item.total),
        items,
        Money(Decimal("0"))
    )
```

**Why compliant:** Small focused functions, each does one thing, cyclomatic complexity ≤10.

---

## VIOLATION: High Complexity Function

```python
def calculate_order_total(order):
    """Cyclomatic complexity: 15+ (VIOLATION)"""
    total = 0

    if order is not None and order.items is not None:
        for item in order.items:
            if item.product is not None:
                if item.product.is_on_sale:
                    if item.quantity > 10:
                        total += item.price * item.quantity * 0.8
                    elif item.quantity > 5:
                        total += item.price * item.quantity * 0.9
                    else:
                        total += item.price * item.quantity * 0.95
                else:
                    if item.product.category == "Electronics":
                        total += item.price * item.quantity * 1.05
                    else:
                        total += item.price * item.quantity

    # ... more nested conditions ...
    return total
```

**Why violates ENG-3.1:** Deeply nested conditions, high cyclomatic complexity, hard to test and maintain.

---

## How to Fix

1. **Extract functions:** Move each pricing rule to its own function
2. **Use guard clauses:** Return early for edge cases
3. **Apply Strategy pattern:** Use polymorphism for different pricing rules

```python
# Fixed version using Strategy pattern
class PricingStrategy(Protocol):
    def calculate(self, item: LineItem) -> Money: ...

class SaleItemPricing(PricingStrategy):
    def calculate(self, item: LineItem) -> Money:
        discount = self._get_volume_discount(item.quantity)
        return item.unit_price.multiply(item.quantity).multiply(1 - discount)

    def _get_volume_discount(self, quantity: int) -> Decimal:
        if quantity > 10:
            return Decimal("0.20")
        if quantity > 5:
            return Decimal("0.10")
        return Decimal("0.05")
```
