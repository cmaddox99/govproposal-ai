> Examples for: skill-12-api-design  
> Parent skill: 12-api-design.md  
> These are optional pedagogical supplements — not in governance scope.

---

## RESTful API Design Principles

### Resource Naming

**Use nouns, not verbs:**
```
# GOOD
GET    /users
GET    /users/{id}
POST   /users
PUT    /users/{id}
DELETE /users/{id}

# BAD
GET    /getUsers
POST   /createUser
POST   /deleteUser/{id}
```

**Use plural nouns:**
```
# GOOD
/users
/orders
/products

# BAD
/user
/order
/product
```

**Use kebab-case for multi-word resources:**
```
# GOOD
/user-profiles
/order-items

# BAD
/userProfiles
/order_items
```

### HTTP Methods

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Retrieve resource(s) | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Partial update | No | No |
| DELETE | Remove resource | Yes | No |

### Status Codes

```
# Success
200 OK           - Successful GET, PUT, PATCH, DELETE
201 Created      - Successful POST (return Location header)
204 No Content   - Successful DELETE (no body)

# Client Errors
400 Bad Request  - Invalid input, validation failed
401 Unauthorized - Not authenticated
403 Forbidden    - Authenticated but not authorized
404 Not Found    - Resource doesn't exist
409 Conflict     - State conflict (e.g., duplicate)
422 Unprocessable Entity - Valid JSON, invalid semantics

# Server Errors
500 Internal Server Error - Unexpected error
502 Bad Gateway  - Upstream service failure
503 Service Unavailable - Temporarily unavailable
```

---

## Request/Response Design

### Request Body

```json
// POST /orders
{
  "customer_id": "cust_123",
  "items": [
    {
      "product_id": "prod_456",
      "quantity": 2
    }
  ],
  "shipping_address": {
    "street": "123 Main St",
    "city": "Boston",
    "state": "MA",
    "zip": "02101"
  }
}
```

**Conventions:**
- Use `snake_case` for JSON properties
- Include only what's needed for the operation
- Validate all input on the server

### Response Body

```json
// 201 Created
{
  "id": "ord_789",
  "customer_id": "cust_123",
  "status": "pending",
  "items": [
    {
      "product_id": "prod_456",
      "product_name": "Widget",
      "quantity": 2,
      "unit_price": 19.99,
      "total": 39.98
    }
  ],
  "subtotal": 39.98,
  "tax": 2.50,
  "total": 42.48,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Conventions:**
- Include resource ID in response
- Use ISO 8601 for timestamps
- Include computed fields
- Use `null` for missing optional fields, omit or use `null`

### Error Response

```json
// 400 Bad Request
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "items[0].quantity",
        "message": "Quantity must be positive",
        "code": "POSITIVE_NUMBER_REQUIRED"
      }
    ]
  },
  "request_id": "req_abc123"
}
```

**Error conventions:**
- Consistent error structure
- Machine-readable error codes
- Human-readable messages
- Field-level details for validation errors
- Request ID for debugging

---

## Pagination

### Offset-Based Pagination

```
GET /users?page=2&per_page=20

{
  "data": [...],
  "pagination": {
    "page": 2,
    "per_page": 20,
    "total_pages": 5,
    "total_count": 100
  }
}
```

**Use when:** Random access needed, moderate dataset size.

### Cursor-Based Pagination

```
GET /users?cursor=eyJpZCI6MTAwfQ&limit=20

{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTIwfQ",
    "has_more": true
  }
}
```

**Use when:** Large datasets, real-time data, no random access needed.

---

## Filtering, Sorting, and Fields

### Filtering

```
GET /orders?status=pending&created_after=2024-01-01

GET /products?category=electronics&price_min=100&price_max=500
```

### Sorting

```
GET /users?sort=created_at:desc

GET /products?sort=price:asc,name:desc
```

### Sparse Fields

```
GET /users?fields=id,name,email

GET /orders?fields=id,status&expand=customer
```

---

## Versioning

### URI Versioning (Recommended)

```
/v1/users
/v2/users
```

**Pros:** Explicit, easy to route, cache-friendly
**Cons:** Clutters URI

### Header Versioning

```
GET /users
Accept: application/vnd.api+json; version=2
```

**Pros:** Clean URIs
**Cons:** Harder to test, less visible

### Version Lifecycle

```
v1 - Deprecated (sunset date announced)
v2 - Stable (current)
v3 - Beta (not for production)
```

---

## API Security

### Authentication

```python
# Bearer token authentication
@app.get("/users/me")
async def get_current_user(
    authorization: str = Header(...)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid authorization header")

    token = authorization[7:]
    user = verify_token(token)
    return user
```

### Authorization

```python
# Role-based access control
@app.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    if not current_user.has_role("admin"):
        raise HTTPException(403, "Admin access required")

    # Delete user...
```

### Rate Limiting

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.get("/search")
@limiter.limit("10/minute")
async def search(query: str):
    return perform_search(query)
```

**Rate limit headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

---

## OpenAPI Specification

```yaml
openapi: 3.0.3
info:
  title: Order API
  version: 1.0.0
  description: API for managing orders

paths:
  /orders:
    post:
      summary: Create an order
      operationId: createOrder
      tags:
        - Orders
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
      responses:
        '201':
          description: Order created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '400':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

components:
  schemas:
    CreateOrderRequest:
      type: object
      required:
        - customer_id
        - items
      properties:
        customer_id:
          type: string
          example: "cust_123"
        items:
          type: array
          items:
            $ref: '#/components/schemas/OrderItem'

    Order:
      type: object
      properties:
        id:
          type: string
        status:
          type: string
          enum: [pending, confirmed, shipped, delivered]
        total:
          type: number
          format: decimal
```

---

## Contract Testing

```python
# Test API contract
class TestOrderAPI:

    def test_create_order_returns_201(self, client):
        response = client.post("/orders", json={
            "customer_id": "cust_123",
            "items": [{"product_id": "prod_1", "quantity": 1}]
        })

        assert response.status_code == 201
        assert "id" in response.json()
        assert response.json()["status"] == "pending"

    def test_create_order_validates_required_fields(self, client):
        response = client.post("/orders", json={})

        assert response.status_code == 400
        assert response.json()["error"]["code"] == "VALIDATION_ERROR"

    def test_get_order_returns_404_for_missing(self, client):
        response = client.get("/orders/nonexistent")

        assert response.status_code == 404
```

---

## Good Examples

### Example 1: Well-Designed Resource API

```yaml
# User management API

# List users with filtering and pagination
GET /v1/users?status=active&sort=created_at:desc&page=1&per_page=20
Response: 200 OK
{
  "data": [
    {
      "id": "usr_123",
      "email": "user@example.com",
      "name": "John Doe",
      "status": "active",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_count": 150
  }
}

# Get single user
GET /v1/users/usr_123
Response: 200 OK
{
  "id": "usr_123",
  "email": "user@example.com",
  "name": "John Doe",
  "status": "active",
  "profile": {
    "avatar_url": "...",
    "bio": "..."
  },
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}

# Create user
POST /v1/users
Request: { "email": "new@example.com", "name": "Jane", "password": "..." }
Response: 201 Created
Location: /v1/users/usr_456

# Update user (partial)
PATCH /v1/users/usr_123
Request: { "name": "John Smith" }
Response: 200 OK

# Delete user
DELETE /v1/users/usr_123
Response: 204 No Content
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: RPC-Style Endpoints

```
# BAD - Verbs in URLs
POST /createUser
POST /getUser
POST /updateUser
POST /deleteUser

# GOOD - Resource-oriented
POST   /users
GET    /users/{id}
PUT    /users/{id}
DELETE /users/{id}
```

---

### Anti-Pattern 2: Inconsistent Responses

```json
// BAD - Different structures for similar endpoints

// GET /users
{ "users": [...] }

// GET /orders
{ "data": [...], "count": 10 }

// GET /products
[...]
```

**Correct approach:** Consistent envelope structure across all endpoints.

---

### Anti-Pattern 3: Breaking Changes Without Versioning

```json
// v1 response
{ "name": "John Doe" }

// "Updated" response (BREAKING!)
{ "first_name": "John", "last_name": "Doe" }
```

**Correct approach:** New version for breaking changes, deprecation period for old version.

---

