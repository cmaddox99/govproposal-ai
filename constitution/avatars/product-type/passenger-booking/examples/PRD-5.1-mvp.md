---
law: PRD-5.1
avatar: avatar-product-passenger-booking
title: "MVP: All-In Price in Search Results (Direct Flights)"
---

# PRD-5.1 MVP Law — Passenger Booking

## Law Summary

The smallest experiment that validates the hypothesis is the correct first investment. Do not roll out price transparency to all flight types before proving the core hypothesis on the simplest case.

---

## ✅ COMPLIANT Example — MVP Canvas

### Hypothesis

> Displaying the all-in price (base fare + taxes + mandatory carrier fees) in search results for direct AA-operated domestic flights will reduce payment-step abandonment from 28% to ≤ 22% within 60 days of full launch.

### Riskiest Assumption

The all-in price calculation (base fare + all applicable taxes and mandatory fees) is accurate and consistent across all domestic routes at search time. If tax calculation has exceptions or errors, the displayed price will be wrong and trust will decrease.

### MVP Scope

**In scope:**
- All-in price display in search results for: direct AA-operated domestic flights only
- Price includes: base fare + all mandatory taxes + carrier-imposed fees (no optional fees)
- Displayed at: search results list view, fare selection screen
- Desktop (aa.com) and mobile web only (native app update deferred)

**Out of scope:**
- Codeshare partner flights (OneWorld, partner metal)
- Multi-city and connecting itineraries
- International routes (tax calculation complexity)
- Optional fee display (bags, seat upgrades, Wi-Fi)
- International tax breakdown views
- Native app (deferred to Phase 2)

### Acceptance Criteria

```gherkin
Scenario: Leisure traveler searches DFW→LAX and sees all-in price
  Given I search for a direct flight from DFW to LAX
  And the flight is operated by American Airlines (not a codeshare)
  When search results are displayed
  Then each fare option shows the total price including all taxes and mandatory fees
  And the price displayed in search matches the price shown at checkout exactly
  And no additional fees are revealed for the first time at the payment page
  And the price is labeled "Total price, all fees included"
```

### Success Criteria (60-Day Post-Launch)

| Metric | Baseline | Target | Fail Gate |
|--------|----------|--------|-----------|
| Payment-step abandonment (direct AA flights) | 28% | ≤ 22% | > 26% → investigate tax calculation accuracy |
| Price accuracy: search price = checkout price | N/A | 100% | Any discrepancy → immediate rollback |
| DOT 14 CFR Part 399 compliance (direct AA domestic) | Non-compliant | Compliant | Any violation → immediate fix |
| Booking completion rate (direct AA domestic) | 37% | ≥ 41% | No movement → investigate other friction sources |

### Codeshare Exclusion Rationale

Codeshare flights require partner tax data that is not available in real time from partner systems. Including codeshare in MVP would require 8+ weeks of partner API integration for 18% of search volume. Direct AA flights represent 82% of domestic search results; prove the hypothesis there first.

---

## ❌ VIOLATION Example

> "Show all-in price for all flights globally: domestic, international, codeshare, multi-city, and all optional fees in one view."

**Why this violates PRD-5.1:**
- International tax calculation requires country-specific tax tables — 6 months of compliance work.
- Codeshare partner tax data integration requires 3+ months of partner API work.
- Optional fee display is a separate product decision (ancillary attachment rate vs. conversion rate trade-off).
- Bundling all of this prevents isolating which change drove abandonment reduction.
- Correct approach: prove all-in price display on direct AA domestic (82% of volume) in 60 days. Then extend.
