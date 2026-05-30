---
law: PRD-1.1
avatar: avatar-passenger-booking
title: "Continuous Discovery — Booking Funnel Abandonment Research"
---

# PRD-1.1 Continuous Discovery — Passenger Booking

## Context

Booking is AA's primary revenue funnel. Discovery work focuses on funnel abandonment,
price opacity, and payment friction using real signals from `booking-ios` and
`aa-ct-mobile-booking-bff` instrumentation.

---

## ✅ COMPLIANT Example

### Weekly Funnel Analysis (booking-ios + BFF telemetry)

| Step | Entry | Drop-off | Abandonment Rate |
|------|-------|----------|-----------------|
| Search → Fare display | 100% | 12% | 12% |
| Fare select → Seat | 88% | 8% | 9% |
| Seat → Passenger info | 80% | 4% | 5% |
| Passenger info → Payment | 76% | 28% | 37% |
| Payment → Confirm | 48% | 2% | 4% |

**Insight:** Payment step is the primary abandonment vector. Root cause investigation:
1. Total-cost shock: taxes + fees revealed at payment (base fare shown at search)
2. Card form friction: 4-field layout on 375px screens has 3× error rate vs. saved cards
3. Auth timeouts: `AirfareSalesConnector` p95 latency = 4.2s; passengers abandon at >3s

### Monthly Passenger Interviews (N=24, 30-day cohort)

| Theme | Frequency | Evidence Source |
|-------|-----------|----------------|
| "Price is different at checkout" | 19/24 | Funnel analytics + interview |
| "Payment timed out" | 11/24 | BFF error logs, `ErrorExceptionHandler` |
| "Couldn't find multi-city easily" | 9/24 | `AAFeatureMultiCityRecentSearches` feature flag |

### Discovery Output → PRD-1.2 Problem Statement

> **Validated problem:** All-in price opacity drives 28% abandonment at payment.
> **Evidence:** 19/24 interviews + funnel analytics confirm total-cost surprise.
> **Next step:** Define smallest MVP per PRD-5.1 (all-in price on direct flights first).

---

## ❌ NON-COMPLIANT Example

> "Let's redesign the booking flow to feel more modern."

**Violation:** No problem statement, no abandonment data, no passenger evidence.
Booking flow redesigns without funnel instrumentation violate PRD-1.1.
