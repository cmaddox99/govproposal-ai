---
laws: [ENG-2.2]
avatar: [mobile-native]
title: Layered Architecture — Swift/Kotlin
---

# ENG-2.2: Layered Architecture — mobile-native

Separate domain logic, application orchestration, and infrastructure concerns into distinct layers.
Domain layer must have zero framework dependencies.

## Example

```
// Domain layer: BookingUseCase.swift — no UIKit
class ConfirmBookingUseCase { func execute(_ b: Booking) -> Result<Receipt,Error> { } }
// Presentation: BookingViewModel.swift — calls use case, publishes state
```

**Rule**: Dependencies flow inward only — infrastructure depends on application, application depends on domain.
