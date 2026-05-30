---
avatar: avatar-product-passenger-booking
domain: Flight Search, Fare Display (DOT Transparency), PCI-DSS Payment, Itinerary Management
laws:
  - BUS-2.3
  - BUS-4.3
  - PRD-1.2
  - PRD-5.1
  - PRD-6.2
  - ENG-6.1
  - ENG-6.4
skills:
  - skill-06-atomic-tdd
  - skill-25-ux-design
  - skill-22-decision-support
---

# Passenger Booking — Implementation Guidance

## Overview

Passenger Booking tools serve leisure travelers, business travelers, family coordinators, and travel agents across flight search, booking, ancillary purchase, and reservation management. The primary conversion failure is **price opacity**: customers who reach the payment step without seeing total cost abandon at 28%. DOT 14 CFR Part 399 requires total cost disclosure before checkout — compliance and conversion improvement are the same fix.

---

## Core Journeys

| Journey | Persona | Success Metric |
|---------|---------|----------------|
| Flight Search | Leisure/Business Traveler | Search-to-book rate > 3% |
| Booking Flow | All | Booking completion rate > 65% |
| Ancillary Purchase | All | Ancillary attachment rate > 40% |
| Manage Reservation | All | Self-service completion rate > 80% |
| Price Alerts | Leisure Traveler | Alert-to-book conversion |

**Key personas:** Leisure Traveler, Business Traveler, Family Coordinator, Travel Agent.

---

## Non-Negotiable Laws

### BUS-2.3 — DOT Fare Transparency (14 CFR Part 399)
- **Total price must be displayed at search results** — not at checkout, not at seat selection. All-in price (base fare + taxes + mandatory fees) required on every fare option shown.
- Displaying a "base fare" in search results and revealing total cost only at payment is a DOT violation and a 28% abandonment driver.
- Implementation: total price calculation must run server-side at search time; no lazy-loading of fees at checkout.

### BUS-4.3 — PCI-DSS / Data Privacy
- **No payment card data in application logs** — mask card numbers in all logging frameworks at the ingestion point, not post-hoc.
- Passenger PII (passport numbers, DOB for international travel) must be encrypted at rest and in transit.
- AAdvantage number must not appear in URL parameters or browser history.

### PRD-1.2 — Problem-First
- Validate that payment-step abandonment is driven by price opacity before any booking flow redesign.
- Research: `booking_funnel_analytics`, `abandonment_rate_tracking`, `search_to_book_conversion`, `session_recordings`.
- A "new booking flow with animations" does not address the validated problem.

### PRD-5.1 — MVP
- Show all-in price in search results for **direct AA flights only** (not codeshare, not multi-city) as MVP.
- Success: reduce payment-step abandonment from 28% to 22%.
- Out of scope for MVP: codeshare partners, international tax breakdown, multi-city itineraries.

### PRD-6.2 — Retention Over Acquisition
- AAdvantage status members have 3× booking completion rate. Status member experience has higher ROI than new customer acquisition spend.
- North-star retention metric: AAdvantage active member 90-day rebook rate.

---

## Key Patterns

- **All-in price at search:** Server-side fee calculation at search time — not deferred to checkout.
- **PCI masking at ingestion:** Card data masking applied at the logging framework level, not filtered downstream.
- **Funnel instrumentation before redesign:** Every abandonment hypothesis must be validated with funnel analytics and session recordings before engineering starts.
- **Status member priority:** AAdvantage Gold/Platinum/Executive Platinum flows are tested first; their rebook rate is the leading retention indicator.

---

## Anti-Patterns

- ❌ Displaying base fare in search results and revealing fees only at payment (DOT 14 CFR Part 399 violation and 28% abandonment driver).
- ❌ Logging raw card numbers or full PANs in debug output — PCI-DSS violation with mandatory breach notification.
- ❌ Booking flow redesign without funnel data identifying the abandonment root cause.
- ❌ Codeshare and multi-city in the all-in price MVP — validate the hypothesis on direct AA flights first.
- ❌ Reporting booking completion rate without segmenting by AAdvantage status — the retention signal is in the status-member cohort.
