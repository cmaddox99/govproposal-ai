# Python/FastAPI Guidance

> **Purpose:** Stack-specific agent behaviors and patterns for Python/FastAPI applications.

---

## Overview

This guidance provides patterns for AI agents working with Python and FastAPI applications. It covers testing with pytest, domain modeling with dataclasses and Pydantic, and async patterns.

---

## Testing Framework

**Primary Framework:** pytest + pytest-asyncio + httpx

### Test Structure

```python
import pytest
from httpx import AsyncClient
from app.domain.order import Order, OrderLine
from app.domain.value_objects import Money, CustomerId

class TestOrder:
    """Tests for Order aggregate."""

    def test_new_order_has_zero_total(self):
        # Arrange
        customer_id = CustomerId("cust-123")

        # Act
        order = Order.create(customer_id)

        # Assert
        assert order.total == Money.zero()

    def test_adding_item_updates_total(self):
        # Arrange
        order = Order.create(CustomerId("cust-123"))
        product = Product(sku="SKU-1", price=Money(100))

        # Act
        order.add_item(product, quantity=2)

        # Assert
        assert order.total == Money(200)


@pytest.mark.asyncio
class TestOrderAPI:
    """Integration tests for Order API."""

    async def test_create_order_returns_201(self, client: AsyncClient):
        # Arrange
        payload = {"customer_id": "cust-123", "items": []}

        # Act
        response = await client.post("/orders", json=payload)

        # Assert
        assert response.status_code == 201
        assert "id" in response.json()
```

### Testing Patterns

- Use class-based tests for grouping related tests
- Use `pytest.mark.asyncio` for async tests
- Use fixtures for common setup
- Use `httpx.AsyncClient` for API testing
- Use `pytest-cov` for coverage

---

## Domain Modeling

### Entity Pattern

```python
from dataclasses import dataclass, field
from typing import List
from uuid import uuid4

from .value_objects import OrderId, CustomerId, Money
from .events import OrderPlaced

@dataclass
class Order:
    """Order aggregate root."""

    id: OrderId
    customer_id: CustomerId
    lines: List[OrderLine] = field(default_factory=list)
    status: OrderStatus = OrderStatus.DRAFT
    _events: List[DomainEvent] = field(default_factory=list, repr=False)

    @classmethod
    def create(cls, customer_id: CustomerId) -> "Order":
        """Factory method for creating new orders."""
        return cls(
            id=OrderId(str(uuid4())),
            customer_id=customer_id,
        )

    def add_item(self, product: Product, quantity: int) -> None:
        """Add item to order. Raises if order is not modifiable."""
        self._ensure_modifiable()

        existing = self._find_line_for(product)
        if existing:
            existing.increase_quantity(quantity)
        else:
            self.lines.append(OrderLine(product, quantity))

    def place(self) -> None:
        """Place the order for fulfillment."""
        if not self.lines:
            raise EmptyOrderError(self.id)

        self.status = OrderStatus.PLACED
        self._events.append(OrderPlaced(self.id, self.total))

    @property
    def total(self) -> Money:
        """Calculate order total from line items."""
        return sum((line.total for line in self.lines), Money.zero())

    def _ensure_modifiable(self) -> None:
        if self.status != OrderStatus.DRAFT:
            raise OrderNotModifiableError(self.id, self.status)
```

### Value Object Pattern

```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)  # Immutable
class Money:
    """Value object representing monetary amount."""

    amount: Decimal
    currency: str = "USD"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")

    def __add__(self, other: "Money") -> "Money":
        self._ensure_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, multiplier: int | Decimal) -> "Money":
        return Money(self.amount * Decimal(multiplier), self.currency)

    @classmethod
    def zero(cls, currency: str = "USD") -> "Money":
        return cls(Decimal("0"), currency)

    def _ensure_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise CurrencyMismatchError(self.currency, other.currency)
```

### Pydantic for DTOs

```python
from pydantic import BaseModel, Field

class CreateOrderRequest(BaseModel):
    """Request DTO for creating orders."""

    customer_id: str = Field(..., min_length=1)
    items: list[OrderItemRequest] = Field(default_factory=list)

    class Config:
        extra = "forbid"  # Reject unknown fields


class OrderResponse(BaseModel):
    """Response DTO for order data."""

    id: str
    customer_id: str
    total: str
    status: str

    @classmethod
    def from_domain(cls, order: Order) -> "OrderResponse":
        return cls(
            id=str(order.id),
            customer_id=str(order.customer_id),
            total=str(order.total.amount),
            status=order.status.value,
        )
```

---

## Common Patterns

### Dependency Injection with FastAPI

```python
from fastapi import Depends
from typing import Annotated

def get_order_repository() -> OrderRepository:
    return SqlAlchemyOrderRepository(get_session())

def get_order_service(
    repo: Annotated[OrderRepository, Depends(get_order_repository)]
) -> OrderService:
    return OrderService(repo)

@router.post("/orders")
async def create_order(
    request: CreateOrderRequest,
    service: Annotated[OrderService, Depends(get_order_service)]
) -> OrderResponse:
    order = await service.create_order(request.customer_id)
    return OrderResponse.from_domain(order)
```

### Async Repository Pattern

```python
from abc import ABC, abstractmethod

class OrderRepository(ABC):
    @abstractmethod
    async def find_by_id(self, order_id: OrderId) -> Order | None:
        ...

    @abstractmethod
    async def save(self, order: Order) -> None:
        ...


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, order_id: OrderId) -> Order | None:
        result = await self._session.execute(
            select(OrderModel).where(OrderModel.id == str(order_id))
        )
        model = result.scalar_one_or_none()
        return model.to_domain() if model else None

    async def save(self, order: Order) -> None:
        model = OrderModel.from_domain(order)
        self._session.add(model)
        await self._session.commit()
```

### Test Fixtures

```python
# conftest.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def sample_order() -> Order:
    order = Order.create(CustomerId("cust-123"))
    order.add_item(Product(sku="SKU-1", price=Money(100)), quantity=1)
    return order
```

---

## Anti-Patterns to Avoid

### Business Logic in Routes

```python
# BAD - Logic in route handler
@router.post("/orders/{order_id}/discount")
async def apply_discount(order_id: str, discount: float):
    order = await repo.find_by_id(order_id)
    # Business logic in route!
    new_total = order.total.amount * (1 - discount)
    order.total = Money(new_total)
    await repo.save(order)
    return {"total": str(new_total)}
```

### Mutable Value Objects

```python
# BAD - Value object should be immutable
@dataclass
class Money:
    amount: Decimal

    def add(self, other: "Money") -> None:
        self.amount += other.amount  # Mutation!
```

### Not Using Type Hints

```python
# BAD - No type hints
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price * item.quantity
    return total

# GOOD - With type hints
def calculate_total(items: list[OrderLine]) -> Money:
    return sum((item.total for item in items), Money.zero())
```

---

## FastAPI Specific Guidance

### Error Handling

```python
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

class DomainException(Exception):
    """Base class for domain exceptions."""
    pass

class OrderNotFoundError(DomainException):
    def __init__(self, order_id: OrderId):
        self.order_id = order_id
        super().__init__(f"Order {order_id} not found")

# Exception handler
@app.exception_handler(OrderNotFoundError)
async def order_not_found_handler(request, exc: OrderNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "ORDER_NOT_FOUND", "message": str(exc)}
    )
```

### Testing Async Code

```python
@pytest.mark.asyncio
async def test_order_service_creates_order():
    # Arrange
    repo = InMemoryOrderRepository()
    service = OrderService(repo)

    # Act
    order = await service.create_order(CustomerId("cust-123"))

    # Assert
    saved = await repo.find_by_id(order.id)
    assert saved is not None
    assert saved.customer_id == CustomerId("cust-123")
```

### Background Tasks

```python
from fastapi import BackgroundTasks

@router.post("/orders/{order_id}/place")
async def place_order(
    order_id: str,
    background_tasks: BackgroundTasks,
    service: Annotated[OrderService, Depends(get_order_service)]
):
    order = await service.place_order(OrderId(order_id))

    # Async side effects
    background_tasks.add_task(send_confirmation_email, order)

    return OrderResponse.from_domain(order)
```

---

## Tools and Commands

### Development

```bash
# Start development server
uvicorn app.main:app --reload

# Start with specific host/port
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run with debugger
python -m debugpy --listen 5678 -m uvicorn app.main:app --reload
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run with HTML coverage report
pytest --cov=app --cov-report=html

# Run async tests only
pytest -m asyncio

# Run with verbose output
pytest -v

# Stop on first failure
pytest -x
```

### Code Quality

```bash
# Format
ruff format app tests

# Lint
ruff check app tests --fix

# Type check
mypy app --strict

# All in one (pre-commit)
pre-commit run --all-files
```
