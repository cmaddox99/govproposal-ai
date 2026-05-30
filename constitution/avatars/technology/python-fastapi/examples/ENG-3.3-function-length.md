---
laws: [ENG-3.3]
avatar: [python-fastapi]
title: Function Length — Python/FastAPI
---

# ENG-3.3: Function Length — python-fastapi

Route handler functions must be ≤ 20 lines. Delegate logic to service classes.

## Example

```python
@router.post("/bookings", response_model=BookingResponse)
async def create_booking(req: BookingRequest, svc: BookingService = Depends()):
    return await svc.create(req)  # handler is 1 line
```

**Rule**: Handlers only validate, delegate, and return. No business logic in route functions.
