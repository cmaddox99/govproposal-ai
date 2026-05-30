# Use Case: Search and Book a Flight (Citizen Booking)
# Avatar: avatar-passenger-booking | Laws: PRD-1.2, PRD-2.3, PRD-3.2, BUS-3.6, BUS-2.3
# Grounded in: booking-ios analysis — FareMapSearchViewModel, BookingSearchCoordinator

use_case:
  id: uc-pax-search-and-book
  name: Search and Book a Flight
  jtbd: "When I need to get somewhere, I want to find the right fare quickly and pay without surprises."
  actor: Passenger (authenticated)
  laws: [PRD-1.2, PRD-2.3, PRD-3.2, BUS-3.6, BUS-2.3]

---

## Pre-conditions

- Passenger is authenticated (AAdvantage or guest)
- Booking is not disabled by feature toggle

## Main Flow

1. Passenger enters search parameters (OD pair, date, cabin, pax count)
2. `BookingSearchCoordinator` fetches fare matrix via `BookingSearchViewModel`
3. Fare Map displays lowest fare per date — data drives UI via Combine publisher
4. Passenger selects itinerary slice; coordinator advances state machine
5. Seat selection offered if available for market
6. Passenger info confirmed (frequent flyer pre-filled if AAdvantage)
7. `SummaryViewModel` renders full fare breakdown with taxes itemised (BUS-2.3)
8. Payment submitted; all monetary arithmetic via `Decimal` (BUS-3.6)
9. PNR issued; boarding pass deep-link prepared

## Alternate Flows

| Branch | Trigger | Resolution |
|--------|---------|------------|
| No availability | Zero fares returned | Show "no flights found" with alternate dates |
| Fare change during session | Server returns `PriceChangedError` | Prompt passenger to re-accept new fare before payment |
| Payment decline | Card auth fails | Surface decline code mapped to human error message |

## Architectural Notes (ENG-3.1)

**iOS:** `BookingSearchCoordinator` (461 lines, 6 responsibilities) is a god-class risk. Agents must not add to this file without first extracting at least one responsibility into its own type. Suggested first extraction: state management → `BookingFlowState` enum.

**Android:** `BookingViewModel.kt` (2,106 LOC) is the most critical god class in the androidapps codebase. It mixes 8 concerns (search orchestration, weekly pricing, itinerary mapping, summary, sorting, cobrand ads, analytics, UI state) across 3 reactive paradigms (RxJava + Coroutines + Compose State). Two confirmed memory leaks: nested `.subscribe()` calls at L403 and L662 never added to `CompositeDisposable` — subscriptions hold ViewModel references after `onCleared()`. **Do not add to `BookingViewModel.kt`.** Any new booking feature on Android requires a `PROPOSAL.md` decomposing the target responsibility out first (ENG-11.1).

---

## Module Reference (PRD-2.1 grounding)

| Module | Path | Lines | Role |
|--------|------|-------|------|
| `BookingSearchCoordinator` | `Sources/BookingSearch/` | 461 | Flow state machine, slice management |
| `BookingSearchViewController` | `Sources/BookingSearch/` | 430 | Search entry UI (UIKit) |
| `FareMapSearchViewModel` | `Sources/FareMap/` | 511 | Fare calendar, Combine publisher |
| `PassengerListViewModel` | `Sources/PassengerInfo/` | — | Passenger list management |
| `PassengerDetailsViewModel` | `Sources/PassengerInfo/` | — | Passenger detail entry |
| `AirfareSalesConnector` | `api/connector/` (BFF) | 174 | External fare API calls |
| `PassengerBuilder` | `api/builder/` (BFF) | 105 | Passenger request assembly |
| `ErrorExceptionHandler` | `exception/` (BFF) | 112 | Error mapping + decline codes |

BFF stack: Spring Boot 4.0.3, Java 25, JUnit 5, Jacoco 0.8.14, Checkstyle 12.1.2.
iOS stack: XCTest + XCUITest, Carthage (`businessui-ios ~> 39.0`), Fastlane.
