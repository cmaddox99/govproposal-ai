---
law_id: ENG-3.5
avatar: python-fastapi
---

# ENG-3.5: Naming Conventions for Python/FastAPI

## Naming Convention Reference

| Element         | Convention            | Example                          |
|-----------------|-----------------------|----------------------------------|
| Classes         | PascalCase            | `OrderService`, `Money`          |
| Functions       | snake_case            | `calculate_total`, `validate_email` |
| Variables       | snake_case            | `customer_count`, `order_items`  |
| Constants       | SCREAMING_SNAKE_CASE  | `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT` |
| Private members | Leading underscore    | `_internal_method`, `_cache`     |
| Modules/files   | snake_case            | `order_service.py`, `cargo_manifest.py` |
| Packages        | lowercase (no underscores preferred) | `models`, `services` |
| Test files      | `test_` prefix        | `test_order_service.py`          |

---

## COMPLIANT: Idiomatic Python Naming

```python
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Sequence

# Constants: SCREAMING_SNAKE_CASE
MAX_RETRY_COUNT = 3
DEFAULT_CURRENCY = "USD"
BASE_TAX_RATE = Decimal("0.08")


# Classes: PascalCase
class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


@dataclass(frozen=True)
class Money:
    """Value object for monetary amounts."""
    amount: Decimal
    currency: str = DEFAULT_CURRENCY

    def add(self, other: "Money") -> "Money":
        self._validate_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def multiply(self, factor: int) -> "Money":
        return Money(self.amount * factor, self.currency)

    # Private method: leading underscore
    def _validate_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot operate on {self.currency} and {other.currency}"
            )


@dataclass(frozen=True)
class LineItem:
    product_name: str
    quantity: int
    unit_price: Money

    @property
    def line_total(self) -> Money:
        return self.unit_price.multiply(self.quantity)


class OrderService:
    """Application service for order operations."""

    def __init__(self, order_repository, tax_calculator) -> None:
        self._order_repository = order_repository
        self._tax_calculator = tax_calculator

    # Functions/methods: snake_case
    def calculate_total(self, items: Sequence[LineItem]) -> Money:
        """Calculate the total for a list of line items."""
        if not items:
            return Money(Decimal("0"))

        subtotal = self._sum_line_items(items)
        tax = self._tax_calculator.calculate_tax(subtotal)
        return subtotal.add(tax)

    def validate_email(self, email: str) -> bool:
        """Check whether the given email address is valid."""
        return "@" in email and "." in email.split("@")[-1]

    # Private helper: leading underscore
    def _sum_line_items(self, items: Sequence[LineItem]) -> Money:
        total = Money(Decimal("0"))
        for item in items:
            total = total.add(item.line_total)
        return total


# Variables: snake_case
def process_cargo_shipment(shipment_id: str) -> None:
    """Process a cargo shipment by its identifier."""
    customer_count = 0
    order_items = []
    retry_attempts = 0

    while retry_attempts < MAX_RETRY_COUNT:
        # processing logic
        retry_attempts += 1
```

```python
# test_order_service.py  (Test file: test_ prefix)
import pytest
from decimal import Decimal

from app.domain.money import Money
from app.services.order_service import OrderService


class TestOrderService:
    """Tests follow test_ file naming and descriptive method names."""

    def test_calculate_total_returns_zero_for_empty_items(self):
        service = OrderService(order_repository=..., tax_calculator=...)
        result = service.calculate_total([])
        assert result == Money(Decimal("0"))

    def test_calculate_total_includes_tax(self):
        # arrange, act, assert
        ...

    def test_validate_email_rejects_missing_at_sign(self):
        service = OrderService(order_repository=..., tax_calculator=...)
        assert service.validate_email("invalid-email") is False
```

**Why compliant:** Classes use PascalCase, functions and variables use snake_case, constants use SCREAMING_SNAKE_CASE, private members have a leading underscore, and test files follow the `test_*.py` convention. Every name communicates its purpose clearly.

---

## VIOLATION: Non-Idiomatic Naming

```python
from decimal import Decimal

# VIOLATION: Constants should be SCREAMING_SNAKE_CASE, not camelCase
maxRetryCount = 3
defaultCurrency = "USD"

# VIOLATION: Class name should be PascalCase, not snake_case
class order_service:

    def __init__(self, OrderRepository, TaxCalculator):
        # VIOLATION: Parameters should be snake_case, not PascalCase
        self.OrderRepository = OrderRepository
        self.TaxCalculator = TaxCalculator

    # VIOLATION: Method should be snake_case, not camelCase
    def calculateTotal(self, Items):
        # VIOLATION: Variable should be snake_case, not camelCase
        orderItems = Items
        customerCount = 0
        subTotal = Decimal("0")

        for Item in orderItems:
            # VIOLATION: Loop variable should be snake_case
            subTotal += Item.price * Item.quantity

        return subTotal

    # VIOLATION: Private method should use leading underscore
    def internalHelper(self):
        pass


# VIOLATION: Function should be snake_case, not PascalCase
def ProcessCargoShipment(ShipmentId: str) -> None:
    MaxAttempts = maxRetryCount  # VIOLATION: Variable should be snake_case
    pass
```

```python
# VIOLATION: Test file name should be test_order_service.py, not OrderServiceTest.py
# OrderServiceTest.py

class OrderServiceTest:
    # VIOLATION: Test method should be snake_case with test_ prefix
    def TestCalculateTotal(self):
        pass

    def shouldReturnZeroForEmptyItems(self):
        pass
```

**Why violates ENG-3.5:** This code uses camelCase for functions and variables (Java/JavaScript style), PascalCase for function names, missing leading underscores on private methods, uppercase parameter names, and non-standard test file naming. This violates Python community conventions (PEP 8) and makes the codebase feel foreign to Python developers.

---

## Quick Reference

```text
Classes/Exceptions    PascalCase          OrderService, ValueError
Functions/Methods     snake_case          calculate_total()
Variables             snake_case          customer_count
Constants             SCREAMING_SNAKE     MAX_RETRY_COUNT
Private               _leading_underscore _internal_cache
Dunder/Magic          __double_under__    __init__, __str__
Modules/Files         snake_case          order_service.py
Packages              lowercase           services, domain
Test Files            test_ prefix        test_order_service.py
```
