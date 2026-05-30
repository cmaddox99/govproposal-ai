---
laws: [ENG-4.1]
avatar: [mobile-native]
title: Atomic TDD — Swift/Kotlin Native
---

# ENG-4.1: Atomic TDD — mobile-native

Every production behaviour must be covered by a unit test written **before** the implementation.
Tests must run without network, database, or file-system dependencies.

## Example

```
func testBookingViewModel_confirmBooking_emitsConfirmationState() {
    let vm = BookingViewModel(service: MockBookingService())
    vm.confirm(booking: .stub())
    XCTAssertEqual(vm.state, .confirmed)
}
```

**Rule**: Each test verifies exactly one behaviour. No shared mutable state between tests.
