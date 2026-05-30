---
laws: [ENG-2.2]
avatar: [angular]
title: Layered Architecture — TypeScript/Angular
---

# ENG-2.2: Layered Architecture — angular

Separate domain logic, application orchestration, and infrastructure concerns into distinct layers.
Domain layer must have zero framework dependencies.

## Example

```
// domain/booking.ts — pure domain, no Angular deps
export class Booking { confirm(): void { this.status = 'CONFIRMED'; } }
// application/booking.facade.ts — orchestrates, no HTTP
export class BookingFacade { constructor(private api: BookingApi) {} }
// infrastructure/booking.api.ts — HTTP only
```

**Rule**: Dependencies flow inward only — infrastructure depends on application, application depends on domain.
