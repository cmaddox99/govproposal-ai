# Manage Trip — Avatar Guidance

## Domain Overview

Manage-Trip covers every post-booking reservation action a traveler takes before
the day of travel. The domain owns cancellation and refund flows, lap infant
addition, special service requests (SSRs), contact information updates, and
itinerary review. It operates on existing PNRs; it does not create bookings.

## What This Avatar Owns

- **Cancellation & Refund** — eligibility adjudication, DOT-compliant refund
  routing, PNR invalidation, and confirmation messaging
- **Lap Infant Addition** — eligibility check, infant data collection, PNR update
- **SSR Management** — wheelchair, dietary, and accessibility service requests
  on an existing reservation
- **Contact Update** — phone and email mutation on a live PNR so notification
  systems have current traveler data
- **Itinerary Review** — read-only trip details and segment status surfaced in
  the My Trips list

## What This Avatar Does NOT Own

- Initial ticket purchase (passenger-booking)
- Boarding pass issuance and day-of-travel gate updates (check-in-travel)
- Carrier-initiated schedule change rebooking (schedule-change-self-serve)
- Seat upgrades triggered at point of sale

## BFF Architecture

Three BFFs orchestrate manage-trip operations on mobile:

| BFF | Role |
|-----|------|
| `mobile-travelhub-bff` | Trip list aggregation and entry point routing |
| `aa-ct-mobile-manage-bff` | Cancellation, SSR, and lap infant mutation flows |
| `Mobile-Manage-Minilith` | Legacy orchestration layer bridging PSS and modern APIs |

`mobile-reservation-bff` and `aa-ct-mobile-reservationlist-bff` provide
reservation read endpoints used for eligibility checks and itinerary display.
`Mobile-Update-Reservation` handles contact-info write operations.

## Key Product Considerations

**Cancellation Eligibility** — Rules vary by fare class, purchase date, and
departure proximity. `CancelEligibilityEndpoint` must be consulted before
surfacing cancel options; never assume eligibility client-side.

**DOT Refund Rules** — Passengers are entitled to a full cash refund for
cancellations within 24 hours of purchase on flights 7+ days out. BUS-2.3
compliance requires explicit refund-method disclosure before confirmation.

**PNR Retention** — After a voluntary cancellation, the PNR must be retained in
a cancelled state per BUS-3.1. Downstream check-in and loyalty systems depend on
PNR history for dispute resolution.

**Audit Trail** — All reservation mutations log via `CancelTripViewModel_Metrics`
and equivalent analytics hooks. BUS-7.1 requires immutable audit records for
every cancellation and modification.

## When to Use This Avatar

Activate avatar-manage-trip when writing specs, journey maps, or acceptance
criteria for any feature that mutates or reads an existing reservation post-
purchase. Do not activate for initial booking or disruption-recovery flows.
