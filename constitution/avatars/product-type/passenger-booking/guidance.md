---
avatar: avatar-passenger-booking
domain: Flight Search, Fare Display (DOT Transparency), PCI-DSS Payment, Itinerary Management
laws: [BUS-2.3, BUS-4.3, PRD-1.2, PRD-5.1, PRD-6.2, ENG-6.1, ENG-6.4]
skills: [06-atomic-tdd, 25-ux-design, 22-decision-support]
---

# Passenger Booking — Agent Guidance

Booking is AA's primary revenue funnel. The validated #1 conversion failure is **price opacity** — total-cost not shown until payment, driving 28% abandonment and DOT 14 CFR Part 399 violations.

## Core Laws (one-liner)

| Law | Rule |
|-----|------|
| BUS-2.3 | Display all-in price (base + taxes + fees) at search results — not at checkout |
| BUS-4.3 | No raw card data in logs; AAdvantage number never in URL params |
| PRD-1.2 | Validate abandonment root cause with funnel analytics before redesigning the flow |
| PRD-5.1 | MVP = all-in price on direct AA domestic flights only; codeshare out of scope |
| PRD-6.2 | AAdvantage status members have 3× completion rate — prioritise their flow first |
| ENG-6.1 | Security by design: no API keys in code or Info.plist |
| ENG-6.4 | PII (passport, DOB) encrypted at rest and in transit |

## Key Patterns

- **All-in price at search** — server-side fee calculation at search time, never deferred.
- **PCI masking at ingestion** — mask card data at the logging framework, not downstream.
- **Funnel-first** — instrument abandonment funnel before any redesign work starts.
- **Status cohort** — segment metrics by AAdvantage status; retention signal lives there.

## Anti-Patterns

- ❌ Base fare in search results, fees revealed at payment (DOT violation + 28% abandonment).
- ❌ Raw card numbers or full PANs in debug logs.
- ❌ Booking flow redesign without validated funnel abandonment data.
- ❌ Codeshare / multi-city in the all-in price MVP.

See `guidance-detail.md` for full law breakdowns, journey tables, and competitor benchmarks.
