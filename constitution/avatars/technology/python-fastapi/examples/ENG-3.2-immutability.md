---
law_id: ENG-3.2
avatar: python-fastapi
---

# ENG-3.2: Immutability Law Examples for Python/FastAPI

## COMPLIANT: Immutable Value Object (frozen dataclass)

```python
from dataclasses import dataclass
from decimal import Decimal
from typing import Self


@dataclass(frozen=True)  # frozen=True makes it immutable
class Money:
    """Immutable value object representing monetary amount."""

    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        # Validation runs after initialization
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if not self.currency:
            raise ValueError("Currency is required")

    @classmethod
    def zero(cls, currency: str = "USD") -> Self:
        return cls(Decimal("0"), currency)

    def add(self, other: "Money") -> "Money":
        """Return new Money instance (immutable)."""
        self._validate_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def multiply(self, factor: Decimal) -> "Money":
        """Return new Money instance (immutable)."""
        return Money(self.amount * factor, self.currency)

    def _validate_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise CurrencyMismatchError(self.currency, other.currency)
```

**Why compliant:** `frozen=True` prevents mutation, all operations return new instances.

---

## VIOLATION: Mutable Data Class

```python
from dataclasses import dataclass


@dataclass  # Missing frozen=True - MUTABLE!
class Money:
    amount: float  # Using float for money is also wrong
    currency: str

    def add(self, other: "Money") -> None:
        # Mutating in place - BAD!
        self.amount += other.amount


# This causes bugs:
price = Money(10.0, "USD")
tax = Money(1.0, "USD")
price.add(tax)  # price is now mutated! Other code holding reference is affected
```

**Why violates ENG-3.2:** Mutable value objects cause subtle bugs when shared across different parts of the code. Changes in one place unexpectedly affect others.

---

## Pydantic Alternative

```python
from pydantic import BaseModel, Field


class Money(BaseModel):
    """Immutable value object using Pydantic."""

    amount: Decimal = Field(ge=0)
    currency: str = Field(min_length=3, max_length=3)

    model_config = {"frozen": True}  # Makes it immutable

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(amount=self.amount + other.amount, currency=self.currency)
```

**Why compliant:** Pydantic's `frozen=True` config prevents mutation, plus built-in validation.

---

## Quick Reference

| Pattern | Mutable | Immutable |
|---------|---------|-----------|
| dataclass | `@dataclass` | `@dataclass(frozen=True)` |
| Pydantic | default | `model_config = {"frozen": True}` |
| NamedTuple | N/A | Always immutable |
