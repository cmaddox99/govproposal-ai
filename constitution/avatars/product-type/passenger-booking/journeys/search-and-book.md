# Journey: Search & Book a Flight
# Avatar: avatar-passenger-booking | Law: PRD-3.2 Journey Mapping Law
# Grounded in: booking-ios analysis (2025-07-16) — 428 Swift files, 800 test methods
# Source modules: BookingSearch/, NativeBooking/, FareMap/, PassengerInfo/, DataModel/

journey:
  id: journey-search-and-book
  name: Search & Book a Flight
  persona: Leisure and business traveller booking via AA iOS app
  laws: [PRD-3.2, PRD-1.2, BUS-3.6, BUS-2.3, ENG-6.1, ENG-6.4]
  source_evidence: booking-ios code-quality-analysis.md (2025-07-16)

---

## Journey Map

| Step | What the passenger does | iOS module | Key law |
|------|------------------------|------------|---------|
| 1. Search | Enters origin, destination, date, cabin, passengers | `BookingSearchViewController` (430 lines, UIKit) | PRD-3.2 |
| 2. Fare Map | Browses lowest fares by date on a calendar map | `FareMapSearchViewModel` (470 lines, Combine) | PRD-1.2 |
| 3. Select flight | Chooses outbound (and return) itinerary slice | `BookingSearchCoordinator` — `setSlices()` | PRD-3.2 |
| 4. Seat selection | Picks seat from interactive map | `seats-ios` module (separate submodule) | ENG-6.4 |
| 5. Passenger info | Enters / confirms traveller details | `PassengerInfo/` module | ENG-6.4 |
| 6. Payment | Enters card or uses saved payment; DOT fare breakdown shown | `payments-ios`, `SummaryViewModel` | BUS-3.6, BUS-2.3 |
| 7. Confirmation | PNR issued; boarding pass deep-link offered | `BookingFinish/` module | ENG-6.7 |

## Pain Points (from codebase evidence)

- `BookingSearchCoordinator` (461 lines) manages 6 responsibilities simultaneously — state, network, error, metrics, slice processing, user preferences. Agent should flag god-class risk per ENG-3.1.
- `SummaryViewDescriber` protocol has 13 properties + 4 methods mixing UI state and business logic — ISP violation.
- Feature toggle branching in `SummaryViewModel` creates competing code paths that make testing the full booking confirmation non-deterministic.

## DOT Fare Transparency (BUS-2.3)

Full fare breakdown must be displayed before payment confirmation — taxes, carrier fees, and base fare itemised. `SummaryViewModel` owns this surface.

## Monetary Precision (BUS-3.6)

All fare amounts, fees, and totals must use `Decimal` (not `Double` or `Float`). Rounding mode: `HALF_EVEN`. No floating-point arithmetic on any monetary field.

---

## AAdvantage Loyalty Touchpoints (PRD-2.1)

| Step | Touchpoint | Module |
|------|-----------|--------|
| Step 5: Passenger info | AAdvantage number pre-filled from profile | `PassengerListViewModel` + `PassengerProfileFetcher` |
| Step 6: Payment | Elite status displayed with fare class earn rate | `SummaryViewModel` |
| Step 7: Post-confirm | Miles earn confirmation shown in-app | `BookingFinish/` |

AAdvantage pre-fill adoption: 67% of authenticated AAdvantage members (BFF telemetry).
Loyalty touchpoints must not be removed or reordered without PRD-6.2 retention impact assessment.

## PRD-2.1 Journey Law Alignment

This journey map fulfils PRD-2.1 (User Journey Mapping) for the app-native booking path.
Companion paths (mobile web, agent-assisted) are covered in `use-cases/search-and-book/README.md`.
Fare transparency gate at Step 3 satisfies DOT 14 CFR Part 260 requirement.
PNR audit event at Step 7 satisfies BUS-7.1 append-only audit trail requirement.

