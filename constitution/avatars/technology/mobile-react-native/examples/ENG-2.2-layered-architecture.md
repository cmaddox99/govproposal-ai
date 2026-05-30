---
laws: [ENG-2.2]
avatar: [mobile-react-native]
title: Layered Architecture — React Native
---

# ENG-2.2: Layered Architecture — mobile-react-native

Separate domain logic, application orchestration, and infrastructure concerns into distinct layers.
Domain layer must have zero framework dependencies.

## Example

```
// domain/booking.ts — plain TS, no RN
export const calculateTotal = (segments: Segment[]): Money => { ... }
// application/useBookingFlow.ts — React hook calling domain
// infrastructure/bookingApi.ts — fetch calls only
```

**Rule**: Dependencies flow inward only — infrastructure depends on application, application depends on domain.
