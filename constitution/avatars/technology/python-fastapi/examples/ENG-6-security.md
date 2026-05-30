---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [python-fastapi]
title: Security Laws — Python/FastAPI
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — python-fastapi

## ENG-6.1: Security by Design

Every route that handles passenger PII or payment data must require authentication via OAuth 2.0 bearer token.

```python
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/bookings/{booking_id}")
async def get_booking(booking_id: str, token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    return await booking_service.get_for_user(booking_id, user.id)
```

## ENG-6.4: Data Encryption

PII fields in transit: TLS 1.3 enforced via HTTPS-only. At rest: encrypt PAN/CVV before storage.

## ENG-6.7: Audit Trail with Correlation ID

Propagate X-Correlation-ID on every request and include in all log entries.

```python
@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid4()))
    with logger.contextualize(correlation_id=correlation_id):
        response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response
```
