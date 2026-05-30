---
law_id: ENG-3.3
avatar: python-fastapi
---

# ENG-3.3: Law of Demeter Examples for Python/FastAPI

## VIOLATION: Train Wreck Chain (reaching through objects)

```python
from dataclasses import dataclass


@dataclass
class City:
    name: str
    state: str


@dataclass
class Address:
    street: str
    city: City
    zip_code: str


@dataclass
class Customer:
    name: str
    address: Address


@dataclass
class Order:
    id: str
    customer: Customer
    total: float


# VIOLATION: navigating deep into the object graph
def get_shipping_label(order: Order) -> str:
    # "Train wreck" - reaching through 3 levels of collaborators
    city_name = order.customer.address.city.name
    state = order.customer.address.city.state
    street = order.customer.address.street
    zip_code = order.customer.address.zip_code

    return f"{order.customer.name}\n{street}\n{city_name}, {state} {zip_code}"
```

**Why violates ENG-3.3:** The `get_shipping_label` function knows the entire internal structure of `Order`, `Customer`, `Address`, and `City`. If any intermediate class changes its structure (e.g., `Address` wraps `City` inside a `Region`), this function and every other function that navigates the same chain must be updated. The function is coupled to four classes instead of one.

---

## COMPLIANT: Encapsulated Access via Direct Collaborator Methods

```python
from dataclasses import dataclass


@dataclass
class City:
    name: str
    state: str


@dataclass
class Address:
    street: str
    city: City
    zip_code: str

    def city_name(self) -> str:
        return self.city.name

    def formatted(self) -> str:
        return f"{self.street}\n{self.city.name}, {self.city.state} {self.zip_code}"


@dataclass
class Customer:
    name: str
    address: Address

    def shipping_address(self) -> str:
        return f"{self.name}\n{self.address.formatted()}"


@dataclass
class Order:
    id: str
    customer: Customer
    total: float

    def delivery_city(self) -> str:
        """Encapsulated access - callers don't need to know the internal structure."""
        return self.customer.address.city_name()

    def shipping_label(self) -> str:
        """Order knows how to produce its own shipping label."""
        return self.customer.shipping_address()


# COMPLIANT: only talks to direct collaborator
def get_shipping_label(order: Order) -> str:
    return order.shipping_label()


def get_delivery_city(order: Order) -> str:
    return order.delivery_city()
```

**Why compliant:** Each function only talks to its direct collaborator. `get_shipping_label` asks `Order` for its label; `Order` delegates to `Customer`; `Customer` delegates to `Address`. If `Address` restructures how it stores city information, only `Address` methods need to change. External callers are shielded.

---

## FastAPI Route Example

```python
from fastapi import APIRouter, Depends

router = APIRouter()


# VIOLATION: route handler reaches deep into domain objects
@router.get("/orders/{order_id}/city")
async def get_order_city_bad(
    order_id: str,
    order_service: OrderService = Depends(get_order_service),
):
    order = await order_service.get_order(order_id)
    # Reaching through the object graph
    return {"city": order.customer.address.city.name}


# COMPLIANT: route handler uses encapsulated method
@router.get("/orders/{order_id}/city")
async def get_order_city_good(
    order_id: str,
    order_service: OrderService = Depends(get_order_service),
):
    order = await order_service.get_order(order_id)
    # Only talks to direct collaborator
    return {"city": order.delivery_city()}
```

---

## Why It Matters

The Law of Demeter reduces **coupling between components**. When code reaches through chains like `order.customer.address.city.name`, it creates invisible dependencies on the internal structure of every object in that chain. This leads to:

- **Fragile code:** A structural change in any intermediate object breaks all callers
- **Hidden dependencies:** The function secretly depends on Customer, Address, and City, but only declares a dependency on Order
- **Difficult testing:** Tests must construct deep object graphs instead of simple mocks
- **Ripple effects:** Refactoring one class forces changes across many unrelated modules

---

## The Rule

A method `M` of object `O` should only call methods on:

1. **`O` itself** - the object's own methods
2. **Objects passed as parameters to `M`** - direct arguments
3. **Objects created within `M`** - locally instantiated objects
4. **`O`'s direct component objects** - attributes held by the object

Any other access (reaching through a collaborator to talk to a stranger) violates the law and should be refactored into a method on the direct collaborator.
