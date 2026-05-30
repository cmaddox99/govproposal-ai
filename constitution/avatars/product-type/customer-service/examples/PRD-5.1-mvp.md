---
law: PRD-5.1
avatar: avatar-product-customer-service
title: "MVP: IROP Self-Service Rebooking Pilot"
---

# PRD-5.1 MVP Law — Customer Service

## Law Summary

The smallest experiment that validates the hypothesis is the correct first investment. Do not build the full rebooking suite before testing whether self-service deflects the targeted call volume.

---

## ✅ COMPLIANT Example — MVP Canvas

### Hypothesis

> Customers with cancelled or significantly delayed domestic flights who have a simple same-day itinerary (single segment, no codeshare, no group booking) will self-rebook via the AA app at a rate that deflects ≥ 15% of IROP call volume within the first 30 days.

### Riskiest Assumption

Customers will discover and complete self-service rebooking during the stress of an IROP event. If discoverability or flow complexity causes abandonment, call deflection will be < 5%.

### MVP Scope

**In scope:**
- Self-service IROP rebooking for: domestic flights only, single-segment itineraries, no codeshare partners, no group bookings (< 10 passengers)
- Triggered by: flight cancelled or delayed ≥ 3 hours
- Rebooking options: same-day flights on AA-operated metal only
- Channels: AA mobile app and aa.com

**Out of scope:**
- Multi-city and connecting itineraries
- Codeshare partner flights (OneWorld)
- Refunds (separate compliance requirement)
- IDB compensation calculation
- Proactive hotel/meal voucher issuance
- Group booking modification

### Acceptance Criteria

```gherkin
Scenario: Customer with cancelled domestic flight self-rebooks
  Given my AA flight DFW→CLT AA1234 is cancelled
  And my itinerary has no connections or codeshare segments
  And I am not in a group booking
  When I open the AA app and tap "Rebook Now"
  Then I see available same-day AA flights to CLT
  And I can select and confirm a new flight in ≤ 4 taps
  And I receive a new boarding pass immediately
  And no agent interaction is required
```

### Success Criteria (30-Day Pilot)

| Metric | Target | Fail Gate |
|--------|--------|-----------|
| Call deflection rate (IROP rebooking calls) | ≥ 15% | < 8% → investigate discoverability |
| Self-service completion rate | ≥ 60% | < 40% → investigate UX friction |
| Customer satisfaction (post-rebook survey) | ≥ 4.0/5.0 | < 3.5 → pause and redesign |
| DOT compliance violations | 0 | > 0 → immediate halt |

### Out of Scope Rationale

Codeshare and multi-city are excluded because: (1) they represent < 22% of IROP rebooking volume, (2) they require partner system integration that adds 3 months of build time, and (3) bundling them prevents isolating what drives the deflection rate.

---

## ❌ VIOLATION Example

> "Build self-service rebooking for all scenarios: domestic, international, codeshare, multi-city, groups, and also include refund requests and IDB compensation."

**Why this violates PRD-5.1:**
- Bundles too many assumptions — if deflection rate is low, root cause is unknowable.
- 5× the build complexity to address 100% of scenarios before proving the 78% simple-domestic case.
- IDB compensation and refunds are legally distinct workflows requiring separate compliance review.
