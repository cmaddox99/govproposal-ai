---
laws: [ENG-4.1]
avatar: [python-fastapi]
title: Atomic TDD — Python/FastAPI
---

# ENG-4.1: Atomic TDD — python-fastapi

Use `httpx.AsyncClient` with `app` as transport — no live server, no database.

## Example

```python
from httpx import AsyncClient
import pytest

@pytest.mark.asyncio
async def test_health_check_returns_200():
    async with AsyncClient(app=app, base_url="http://test") as client:
        resp = await client.get("/health")
    assert resp.status_code == 200

@pytest.mark.asyncio
async def test_booking_endpoint_validates_pax_count():
    async with AsyncClient(app=app, base_url="http://test") as client:
        resp = await client.post("/bookings", json={"passengers": 0})
    assert resp.status_code == 422
```

**Rule**: Each test covers one endpoint behaviour. Dependency injection via `app.dependency_overrides`.
