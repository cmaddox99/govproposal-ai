# Use Case: Self-Serve Flight Rebooking

**Avatar:** schedule-change-self-serve  
**Law:** PRD-2.1 User Journey Mapping, PRD-3.1 Roadmap Planning  
**Slice:** 2 — Rebooking Success and Audit Completeness  
**Status:** Discovery — details require validation against BFF and reservation service code

---

## Overview

An eligible passenger selects a replacement flight, reviews the fare difference,
selects a seat, and receives atomic confirmation of the rebooking. The BFF
orchestrates eligibility → fare calculation → seat selection → reservation write
as a traceable, auditable transaction.

---

## Actors

- **Passenger** — self-serve (web or app)  
- **schedule-change-bff** — orchestration hub  
- **schedule-change-eligibility-service** — confirms eligibility before write  
- **drss-schedule-change-reservation-service** — executes rebooking  
- **schedule-change-ui** — flight selection, seat picker, confirmation screen

---

## Happy Path

1. Passenger selects replacement flight from available alternatives.
2. BFF re-validates eligibility (guard against stale eligibility check).
3. BFF requests fare difference from pricing service.
4. Passenger reviews fare difference and confirms.
5. Seat selection UI opens with loyalty preferences pre-applied.
6. Passenger selects seat and submits.
7. BFF calls drss-schedule-change-reservation-service to write rebooking atomically.
8. Confirmation returned — BFF emits audit event.
9. UI displays confirmation; push/email notification dispatched within 60 seconds.

---

## Exception Paths

| Scenario | Handling |
|----------|---------|
| Seat selected already taken between selection and write | Re-prompt seat selection; no partial booking left |
| Reservation write fails mid-transaction | BFF rolls back; original booking preserved; passenger shown retry option |
| Loyalty upgrade hold on original flight | UI prompts: "Your upgrade on {flight} will be released — continue?" |
| Fare calculation timeout | Hold selection; surface timeout message with retry CTA |

---

## Audit Requirements (BUS-3.1, ENG-6.4)

Every completed or attempted rebooking must emit:

- Eligibility result + rule match
- Fare difference accepted or declined
- Seat selection outcome
- Reservation write result (success / failure + reason)
- Timestamp and passenger identifier (anonymised for PII compliance)

---

## Acceptance Criteria (Slice 2)

- BFF p95 latency ≤1800ms for full orchestration chain
- Zero partial bookings (original not restored after write failure)
- Audit event coverage 100% on all change attempts
- Upgrade hold preserved in ≥95% of eligible rebookings after seat selection
