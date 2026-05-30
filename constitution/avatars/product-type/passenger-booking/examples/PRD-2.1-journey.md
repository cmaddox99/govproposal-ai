---
law: PRD-2.1
avatar: avatar-passenger-booking
title: "User Journey — Search to PNR (App-Native Path)"
---

# PRD-2.1 User Journey — Passenger Booking

## Journey: App-Native Booking (Primary Path)

Grounded in `booking-ios` module analysis:
`BookingSearchCoordinator` → `FareMapSearchViewModel` → `PassengerInfo/` → `BookingFinish/`

| Step | Module | Action | Key Law | Compliance Gate |
|------|--------|--------|---------|----------------|
| 1. Search | `BookingSearchViewController` | Enter OD pair, date, cabin, pax | PRD-1.1 | Instrumented for abandonment |
| 2. Fare Calendar | `FareMapSearchViewModel` (Combine) | Browse lowest fares by date | PRD-2.1 | Fare displayed inclusive of taxes? |
| 3. Select flight | `BookingSearchCoordinator.setSlices()` | Choose outbound + return slices | PRD-2.1 | DOT fare transparency gate |
| 4. Seat selection | `seats-ios` submodule | Pick seat from interactive map | ENG-6.4 | PII in seat assignment masked |
| 5. Passenger info | `PassengerListViewModel` | Confirm/enter traveller details | ENG-6.4 | AAdvantage pre-fill eligible |
| 6. Payment | `SummaryViewModel` | View full fare breakdown + pay | BUS-2.3 | All-in price before payment required |
| 7. Confirmation | `BookingFinish/` | PNR issued; boarding pass deep-link | ENG-6.7 | Audit event emitted |

## Loyalty Touchpoints

- Step 5: AAdvantage number pre-filled from profile (`PassengerProfileFetcher`)
- Step 6: Elite status shown with fare class earn rate
- Post-confirm: miles credited to account, earn confirmation in-app

## Exception Flows

| Scenario | Handling |
|----------|----------|
| Fare changed during session | `PriceChangedError` → re-accept modal before payment |
| Payment declined | Card decline code → human-readable error (`ErrorExceptionHandler`) |
| Session timeout | AirfareSalesConnector timeout → offer retry with saved card |

## Journey Metrics (from BFF telemetry)

- Median time search→confirm: 4.2 min
- Payment step p95 latency: 4.2s (target: <2s)
- Loyalty pre-fill adoption: 67% of AAdvantage members
