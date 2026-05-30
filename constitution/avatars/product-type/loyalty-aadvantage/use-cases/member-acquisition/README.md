# Use Case: Member Acquisition (AAdvantage Loyalty)

**Avatar:** avatar-loyalty-aadvantage  
**Laws:** PRD-1.1 (Continuous Discovery), PRD-4.1 (MVP), PRD-5.1 (Metrics), BUS-4.3 (Data Retention)  
**Scope:** New member enrollment via app, web, airport, and partner channels

## Acquisition Context

AAdvantage is AA's most valuable retention asset. Acquisition economics:
- Credit card co-brand enrollments have 3-4× higher 12-month retention than travel-only enrollments
- Airport kiosk enrollments have the highest earn-in-first-30-days rate
- App enrollments that trigger a booking within 7 days have near-zero 90-day churn

## Enrollment Channels

| Channel | Quality of Acquire | BFF Dependency |
|---------|-------------------|----------------|
| In-booking (AA app) | Highest LTV | `aa-ct-mobile-booking-bff` (7.4/10 ✅) |
| Post-flight notification | High intent | `aa-ct-mobile-airship` (4.5/10 🟡 — ClassCastException confirmed) |
| Airport kiosk | High earn velocity | Not mobile BFF — separate system |
| Partner landing page | Variable | `mobile-aadvantage-bff` (5.6/10 🟡) |

**Note on airship:** `aa-ct-mobile-airship` (4.5/10) has a confirmed `ClassCastException` in `CuratedFlightEvent.unpackNestedBookingDetails()` — push notification enrichment fails silently for certain booking types. Post-flight enrollment notifications may silently fail for this member segment.

## Enrollment MVP Requirements

Per PRD-4.1:
1. Instrument enrollment funnel **before launch** — capture drop-off at each step
2. ENG-11.1 gate: any new enrollment path that modifies BFF contracts requires PROPOSAL.md
3. BUS-4.3 compliance: enrolled member PII must route through compliant data retention pipeline from day 1

## Enrollment Funnel Metrics (PRD-5.1)

```
Step 1: Enrollment prompt shown
Step 2: Enrollment form opened          ← drop-off #1 (friction)
Step 3: Form submitted
Step 4: Email verified                  ← drop-off #2 (email bounce / deliverability)
Step 5: First earning event             ← activation signal
```

- **Activation rate target:** ≥ 40% of enrolled members earn at least 1 point within 30 days
- **Form completion rate:** ≥ 70% (if < 70%, form has too many required fields)
- **Email verification rate:** ≥ 85% (if < 85%, deliverability or UX issue)

## Data Retention (BUS-4.3)

Member PII collected at enrollment:
- **Retention:** Lifetime of membership + 7 years post-closure
- **EU members:** GDPR Article 6(1)(b) contract basis — explicit consent required for marketing communications
- **Incomplete enrollments (abandoned):** PII must not be retained beyond 30 days without explicit consent

> Full acquisition analysis, channel benchmarks, and A/B testing framework in `README-detail.md`.
