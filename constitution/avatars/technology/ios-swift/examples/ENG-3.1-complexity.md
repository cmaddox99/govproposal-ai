---
law_id: ENG-3.1
avatar: ios-swift
---

# ENG-3.1: Complexity Limits Examples for iOS (Swift)

> **Law:** Cyclomatic complexity SHALL NOT exceed 10 per method/function. Functions exceeding the limit MUST be decomposed. High complexity is a defect, not a style preference.

---

## iOS Complexity Limits

| Target | Limit | Enforcement |
|--------|-------|-------------|
| Any Swift function or method | ≤ 10 | SwiftLint `cyclomatic_complexity` rule |
| ViewModel action method | ≤ 5 (preferred) | Triggers use-case extraction |
| UI event handler | ≤ 3 | Delegates to ViewModel/use case |
| SwiftUI View `body` | Decompose into sub-views | No complexity metric; use judgment |

Configure SwiftLint:

```yaml
# .swiftlint.yml
cyclomatic_complexity:
  warning: 8
  error: 10
```

---

## COMPLIANT: Low-Complexity ViewModel Action

```swift
// Complexity: 2 — simple guard + async call
@MainActor
final class FlightSearchViewModel: ObservableObject {
    @Published private(set) var results: [FlightResult] = []
    @Published private(set) var errorMessage: String?

    private let searchFlights: SearchFlightsUseCase

    init(searchFlights: SearchFlightsUseCase) {
        self.searchFlights = searchFlights
    }

    func search(origin: Airport, destination: Airport, date: Date) async {
        guard origin != destination else {
            errorMessage = "Origin and destination cannot be the same"
            return
        }
        do {
            results = try await searchFlights(origin: origin, destination: destination, date: date)
            errorMessage = nil
        } catch {
            errorMessage = error.localizedDescription
            results = []
        }
    }
}
```

---

## COMPLIANT: Complex Logic Extracted to Use Case

When booking validation becomes complex, extract it to a dedicated, tested use case type rather than growing the ViewModel.

```swift
// ValidateBookingUseCase owns the complexity (well-tested in isolation)
struct ValidateBookingUseCase {
    // Complexity: 5 — each guard is +1
    func callAsFunction(_ booking: Booking) throws {
        guard !booking.passengerName.isEmpty else {
            throw BookingError.missingPassengerName
        }
        guard booking.departureDate > .now else {
            throw BookingError.departureDateInPast
        }
        guard booking.origin != booking.destination else {
            throw BookingError.sameOriginDestination
        }
        guard booking.passengerCount >= 1 else {
            throw BookingError.invalidPassengerCount
        }
        guard booking.passengerCount <= 9 else {
            throw BookingError.tooManyPassengers
        }
    }
}

// ViewModel delegates — complexity stays low
@MainActor
final class BookingViewModel: ObservableObject {
    @Published private(set) var isBookingValid = false

    private let validateBooking: ValidateBookingUseCase

    init(validateBooking: ValidateBookingUseCase = ValidateBookingUseCase()) {
        self.validateBooking = validateBooking
    }

    // Complexity: 2
    func validate(_ booking: Booking) {
        do {
            try validateBooking(booking)
            isBookingValid = true
        } catch {
            isBookingValid = false
        }
    }
}
```

---

## VIOLATION: Over-Complex Method

```swift
// Complexity: 13 — each if/guard/case/catch is +1; EXCEEDS LIMIT OF 10
func processBooking(_ booking: Booking, user: User, context: AppContext) -> BookingResult {
    if booking.passengerName.isEmpty {           // +1
        return .failure(.missingName)
    }
    if booking.departureDate <= .now {           // +1
        return .failure(.invalidDate)
    }
    if booking.origin == booking.destination {   // +1
        return .failure(.sameOriginDestination)
    }
    switch user.loyaltyTier {                    // +1
    case .platinum:
        if booking.seatClass == .economy {       // +1 (nested)
            applyUpgrade(&booking)
        }
    case .gold:
        if booking.passengerCount == 1 {         // +1
            applyGoldBenefit(&booking)
        }
    default: break
    }
    if context.isInternational {                 // +1
        if booking.requiresVisa {               // +1 (nested)
            try? validateVisa(booking)
        }
    }
    if booking.paymentMethod == .miles {        // +1
        if user.milesBalance < booking.mileCost { // +1 (nested)
            return .failure(.insufficientMiles)
        }
    }
    do {
        let confirmation = try api.submit(booking) // +1
        return .success(confirmation)
    } catch {
        return .failure(.networkError)
    }
}
```

**Why ENG-3.1 violated:** 13 branches create 13+ distinct code paths. Any change risks unexpected interaction between branches. Testing requires combinatorial coverage. Extract to `ValidateBookingUseCase`, `ApplyLoyaltyBenefitsUseCase`, and `SubmitBookingUseCase`.

---

## Real Codebase Evidence (booking-ios + checkin-ios, 2025-07-17)

These are documented violations in the Wave 4 mobile codebase — agents must not make them worse.

| Class | Lines | Responsibility count | Action required |
|-------|-------|---------------------|----------------|
| `BookingSearchCoordinator` | 461 | 6 (state, network, error, metrics, slice processing, user prefs) | Do not add to this file; extract `BookingFlowState` first |
| `FareMapSearchViewModel` | 470 | 3 (search, UI state, analytics) | Extract analytics to a side-effect wrapper |
| `TravelerContactInfoViewController` | 918 | 4 (UI, validation, network, state) | Migrate to MVVM before adding contact field |
| `CheckInManager` | 1,186 | 5+ (state machine, server, UI presentation, analytics, notifications) | Highest-priority refactor in check-in; extension split already started |

`CheckInManager` at 1,186 lines is the largest known god class in the iOS portfolio. The team has already applied the right first step (extension decomposition: `CheckInManager_Analytics.swift`, `CheckInManager_Notifications.swift`). Continue until each extension can become its own type.

### The Rule for These Files

> An agent must not add a single line of logic to any of these files without first extracting at least one existing responsibility. Adding to a god class is a complexity debt payment, not a feature.



---

## SwiftLint Setup

```bash
# Install SwiftLint via Homebrew or SPM
brew install swiftlint

# Or add to Package.swift as a build tool plugin (Xcode 14+)
# Then run:
swiftlint lint --config .swiftlint.yml

# Or via fastlane:
lane :lint do
  swiftlint(
    mode: :lint,
    config_file: ".swiftlint.yml",
    strict: true,
    reporter: "emoji"
  )
end
```
