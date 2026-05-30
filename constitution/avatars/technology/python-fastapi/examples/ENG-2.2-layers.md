---
law_id: ENG-2.2
avatar: python-fastapi
---

# ENG-2.2: Layered Architecture Examples for Python/FastAPI

## COMPLIANT: Clean Layers

```python
# api/routes/orders.py - PRESENTATION LAYER (Request/Response only)
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    request: CreateOrderRequest,
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    """Create a new order."""
    order = await service.create_order(
        customer_id=request.customer_id,
        items=request.to_line_items(),
    )
    return OrderResponse.from_domain(order)


# application/order_service.py - APPLICATION LAYER (Orchestration)
class OrderService:
    def __init__(
        self,
        repository: OrderRepository,
        inventory_client: InventoryClient,
        event_publisher: EventPublisher,
    ) -> None:
        self._repository = repository
        self._inventory = inventory_client
        self._events = event_publisher

    async def create_order(
        self,
        customer_id: UUID,
        items: list[LineItemCommand],
    ) -> Order:
        """Orchestrate order creation - no business logic here."""
        order = Order(customer_id=customer_id)

        for item in items:
            order.add_item(item.product_id, item.quantity, item.price)

        await self._inventory.reserve(order.items)
        await self._repository.save(order)
        await self._events.publish_all(order.collect_events())

        return order


# infrastructure/repositories/order_repository.py - INFRASTRUCTURE LAYER
class MongoOrderRepository(OrderRepository):
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self._collection = database["orders"]

    async def save(self, order: Order) -> None:
        document = self._to_document(order)
        await self._collection.replace_one(
            {"_id": order.id},
            document,
            upsert=True,
        )

    async def find_by_id(self, order_id: UUID) -> Order | None:
        document = await self._collection.find_one({"_id": order_id})
        return self._to_domain(document) if document else None
```

**Why compliant:**
- Each layer has a single responsibility
- Dependencies point inward (infrastructure → application → domain)
- Domain layer has no external dependencies

---

## VIOLATION: Business Logic in Route Handler

```python
# BAD: Route handler doing business logic
@router.post("/orders")
async def create_order(request: dict, db: Database = Depends(get_db)):
    # Business logic in route handler!
    order = {"id": uuid4(), "customer_id": request["customer_id"], "items": []}

    for item in request["items"]:
        if item["quantity"] > 100:  # Business rule in handler!
            raise HTTPException(400, "Max 100 items")
        order["items"].append(item)

    # Direct database access (skipping service layer)
    await db.orders.insert_one(order)
    return order
```

**Why violates ENG-2.2:**
- Business rules scattered in presentation layer
- No separation of concerns
- Hard to test business logic independently
- Database details leak into API layer

---

## Layer Responsibilities

| Layer | Responsibility | Dependencies |
|-------|----------------|--------------|
| **Presentation (API)** | HTTP, serialization, validation | Application |
| **Application** | Use case orchestration, transactions | Domain, Infrastructure (via ports) |
| **Domain** | Business rules, entities, value objects | None |
| **Infrastructure** | Database, external services, messaging | Domain (implements ports) |

---

## Dependency Inversion

```python
# Domain layer defines the PORT (interface)
class OrderRepository(ABC):
    @abstractmethod
    async def save(self, order: Order) -> None: ...

    @abstractmethod
    async def find_by_id(self, order_id: UUID) -> Order | None: ...


# Infrastructure layer provides the ADAPTER (implementation)
class PostgresOrderRepository(OrderRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, order: Order) -> None:
        # PostgreSQL-specific implementation
        ...
```

**Key principle:** Domain defines interfaces, infrastructure implements them.
