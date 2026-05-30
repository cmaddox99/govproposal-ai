---
law: PRD-1.2
avatar: avatar-product-passenger-booking
title: "Problem-First: Payment Step Abandonment"
---

# PRD-1.2 Problem-First — Passenger Booking

## Law Summary

Validate the real problem before proposing a solution. Aesthetic requests often mask validated functional failures.

---

## ✅ COMPLIANT Example

### Stated Request

> "Redesign the booking flow with new animations and a modern visual design to improve conversion."

### Research Conducted

Funnel analytics (3-month dataset, 4.2M booking sessions), session recording review (n=200 sessions at payment step), 20 usability test sessions with travel shoppers.

| Finding | Value | Source |
|---------|-------|--------|
| Overall booking abandonment rate | 61% | Funnel analytics |
| Step with highest single-step abandonment | Payment page (28%) | Funnel analytics |
| % of users who abandon at payment after entering card details | 19% | Funnel analytics |
| #1 reason cited in usability tests for payment abandonment | "Total price was higher than expected" | Usability tests (20 sessions) |
| Gap between search-page price shown and payment-page total | $34–$89 (taxes + carrier fees) | Price audit (100 routes) |
| % of users who said they would have continued if total shown earlier | 71% | Post-session survey (usability tests) |
| DOT 14 CFR Part 399 compliance status | Non-compliant — total price not shown at search | Compliance audit |

**Session recording finding:** In 84% of sessions that abandoned at payment, the user paused ≥ 8 seconds after the final price was revealed and then navigated away.

### Validated Problem Statement

> 28% of users abandon the booking flow at the payment step. Root cause: total cost (base fare + taxes + mandatory carrier fees) is not displayed until the payment page. The gap between the price shown at search ($189) and the all-in total at payment ($247) causes price shock and abandonment. This is also a DOT 14 CFR Part 399 compliance violation. New animations will not fix price shock.

### Correct Solution Direction

Display all-in price (base fare + taxes + mandatory fees) in search results, before checkout. Start with direct AA flights (no codeshare). Target: reduce payment-step abandonment from 28% to 22%.

---

## ❌ VIOLATION Example

> "Our competitors have a cleaner booking UI. We should redesign the entire flow with new animations, a progress indicator, and a new color scheme. That will improve conversion."

**Why this violates PRD-1.2:**
- Competitor UI comparison is not evidence of root cause.
- Animations and color schemes do not address price opacity.
- No funnel data cited: where exactly does conversion fail?
- DOT compliance risk unaddressed.
- Correct first step: funnel analytics to identify the highest-abandonment step, then session recordings to identify the root cause at that step.
