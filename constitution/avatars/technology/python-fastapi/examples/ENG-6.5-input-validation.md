---
laws: [ENG-6.5]
avatar: [python-fastapi]
title: Input Validation — Python/FastAPI
---

# ENG-6.5: Input Validation — python-fastapi

All inputs must be validated at the boundary using Pydantic models. Never trust client-supplied data.

## Example

```python
from pydantic import BaseModel, Field, field_validator

class BookingRequest(BaseModel):
    origin: str = Field(min_length=3, max_length=3, pattern="^[A-Z]{3}$")
    destination: str = Field(min_length=3, max_length=3, pattern="^[A-Z]{3}$")
    passengers: int = Field(ge=1, le=9)

    @field_validator("destination")
    @classmethod
    def origin_ne_destination(cls, v, info):
        if "origin" in info.data and v == info.data["origin"]:
            raise ValueError("destination must differ from origin")
        return v
```

**Rule**: Pydantic validation is the single enforcement point. No manual `if/else` type checks in handlers.
