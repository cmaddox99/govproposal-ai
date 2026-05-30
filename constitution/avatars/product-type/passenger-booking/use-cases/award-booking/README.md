# Use Case: Award Booking (AAdvantage Miles)
# Avatar: avatar-passenger-booking | Laws: PRD-1.2, PRD-2.3, BUS-3.6
# Grounded in: booking-ios analysis — AwardMVP1 feature toggle, DataModel/ award types

use_case:
  id: uc-pax-award-booking
  name: Book a Flight with AAdvantage Miles
  jtbd: "When I have miles, I want to use them to book a flight without navigating two different systems."
  actor: AAdvantage member (authenticated)
  laws: [PRD-1.2, PRD-2.3, BUS-3.6]

---

## Pre-conditions

- Passenger is authenticated as AAdvantage member
- `AwardMVP1` feature toggle is enabled
- Sufficient miles balance confirmed via `mobile-aadvantage-bff`

## Main Flow

1. Passenger selects "Use Miles" mode in booking entry
2. `BookingSearchViewModel` fetches award fare matrix (separate endpoint from cash fares)
3. Miles + copay cost displayed per itinerary cell
4. Passenger selects award itinerary; miles hold placed to prevent over-sell
5. Copay computed using `Decimal` arithmetic (BUS-3.6 — copay is a monetary value)
6. Miles deduction and copay payment processed atomically
7. Award PNR issued with MileagePlus award attributes

## Alternate Flows

| Branch | Trigger | Resolution |
|--------|---------|------------|
| Insufficient miles | Balance < required award | Offer points-plus-cash upgrade or block flow |
| Miles hold expires | Session times out before payment | Release hold; restart award search |
| Award seat no longer available | Race condition on hold | Retry once; surface "seat no longer available" if second attempt fails |

## Feature Toggle Contract

`AwardMVP1` gates the award search entry point only. If the toggle is off, the booking flow falls back to cash-only mode. No award logic should run outside this guard — confirm via feature flag inspection in `BookingSearchCoordinator.configure()`.
