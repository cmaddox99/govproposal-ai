---
law_id: ENG-6.5
avatar: python-fastapi
---

# ENG-6.5: Input Validation Examples for Python/FastAPI

## COMPLIANT: Proper Validation with Pydantic

```python
from pydantic import BaseModel, Field, field_validator
from uuid import UUID


class LineItemRequest(BaseModel):
    """Validated line item in order request."""

    product_id: UUID
    quantity: int = Field(ge=1, le=1000, description="Quantity between 1 and 1000")

    @field_validator("product_id")
    @classmethod
    def validate_product_id(cls, v: UUID) -> UUID:
        if v == UUID(int=0):
            raise ValueError("Product ID cannot be nil UUID")
        return v


class CreateOrderRequest(BaseModel):
    """Validated order creation request."""

    customer_id: UUID
    items: list[LineItemRequest] = Field(
        min_length=1,
        max_length=100,
        description="Order items (1-100)",
    )

    model_config = {"extra": "forbid"}  # Reject unknown fields


# FastAPI automatically validates request body
@router.post("/")
async def create_order(request: CreateOrderRequest) -> OrderResponse:
    # request is guaranteed to be valid here
    ...


# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed",
            "details": exc.errors(),
        },
    )
```

**Why compliant:**
- Type-safe validation with Pydantic
- Constraints enforced at boundaries
- Unknown fields rejected
- Custom validators for complex rules

---

## VIOLATION: No Validation

```python
# BAD: No validation at all
@router.post("/orders")
async def create_order(request: dict):  # Untyped dict!
    # Trusting input blindly!
    customer_id = request["customer_id"]  # Could be missing, wrong type
    quantity = request["quantity"]  # Could be negative, huge, missing

    # SQL injection risk if used in raw query
    product_name = request["product_name"]

    # ...
```

**Why violates ENG-6.5:**
- No type checking
- No constraint validation
- Vulnerable to injection attacks
- Will crash on missing fields

---

## Common Validation Patterns

### Email Validation

```python
from pydantic import BaseModel, EmailStr

class UserRequest(BaseModel):
    email: EmailStr  # Built-in email validation
```

### String Constraints

```python
from pydantic import BaseModel, Field

class ProductRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    sku: str = Field(pattern=r"^[A-Z]{3}-\d{4}$")  # SKU format: ABC-1234
```

### Nested Validation

```python
class AddressRequest(BaseModel):
    street: str = Field(min_length=1)
    city: str = Field(min_length=1)
    postal_code: str = Field(pattern=r"^\d{5}(-\d{4})?$")  # US zip

class CustomerRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    shipping_address: AddressRequest  # Nested validation
    billing_address: AddressRequest | None = None  # Optional
```

### Custom Validators

```python
from pydantic import BaseModel, field_validator, model_validator

class DateRangeRequest(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_date_range(self) -> "DateRangeRequest":
        if self.end_date < self.start_date:
            raise ValueError("end_date must be after start_date")
        return self
```

---

## Query Parameter Validation

```python
from fastapi import Query

@router.get("/orders")
async def list_orders(
    page: int = Query(ge=1, default=1),
    per_page: int = Query(ge=1, le=100, default=20),
    status: OrderStatus | None = Query(default=None),
) -> list[OrderResponse]:
    # Parameters are validated before reaching handler
    ...
```
