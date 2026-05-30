---
law: PRD-1.5
avatar: avatar-product-customer-service
title: "Evidence-Based: Self-Service IROP Rebooking Investment"
---

# PRD-1.5 Evidence-Based — Customer Service

## Law Summary

Investment decisions require quantified evidence. State the hypothesis, gather the data, then decide.

---

## ✅ COMPLIANT Example

### Decision

> Invest in self-service IROP rebooking capability for simple same-day domestic itinerary changes.

### Hypothesis

> If customers can rebook themselves during IROP events without calling an agent, we will deflect ≥ 15% of IROP call volume in the first 30 days, reducing agent staffing cost by ≥ $320K/day during major disruptions.

### Evidence Package

| Metric | Value | Source |
|--------|-------|--------|
| % of IROP call volume that is rebooking | 67% | Call recording analysis (n=2,400, 4 weeks) |
| Average calls per day during major IROP event | 40,000 | Call center operations data |
| Average handle time for IROP rebooking | 8 minutes | AHT system |
| Agent cost per minute | $1.00 (all-in loaded cost) | Finance |
| Agent cost for IROP rebooking calls per day | $320K/day | Calculated: 40K × 67% × 8 min × $1.00/min |
| % of rebooking customers who said they'd prefer self-serve | 73% | Post-interaction survey (n=1,800) |
| % of rebooking calls with no supervisor escalation | 89% | Call recording analysis |
| Simple domestic itineraries (no codeshare, no multi-city) | 78% of rebooking volume | Booking system analysis |

### Decision Tree

```
Self-service rebooking for simple domestic only (78% of rebooking volume)?
    │
    ▼
Addressable volume: 40,000 × 67% × 78% = ~20,900 calls/day
    │
    ▼
If 15% deflection achieved: 3,135 calls/day saved
    │
    ▼
Cost savings: 3,135 × 8 min × $1.00/min = $25,080/day
    │
    ▼
Annualized at 12 major IROP events/year (avg 2 days each): ~$600K/year
    │
    ▼
Build cost estimate: $280K (3 engineers, 12 weeks)
Payback period: ~6 months
```

### Investment Gate

Proceed if: 15% call deflection achieved in first 30-day pilot. Fail gate: < 8% deflection triggers pivot investigation (was it discoverability, UX friction, or eligibility scope?).

---

## ❌ VIOLATION Example

> "Self-service is obviously better for customers. Let's build it for all rebooking scenarios including refunds, IDB compensation, codeshare partners, and multi-city itineraries."

**Why this violates PRD-1.5:**
- No evidence cited for scope — codeshare and multi-city represent unknown complexity and edge-case volume.
- "Obviously better" is not quantified evidence.
- Refund and IDB compensation are legally complex; bundling them removes the ability to isolate what drives the investment outcome.
- Correct approach: prove the 78% simple-domestic hypothesis before extending scope.
