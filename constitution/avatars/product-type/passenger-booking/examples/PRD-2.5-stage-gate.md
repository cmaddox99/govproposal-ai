---
law: PRD-2.5
avatar: avatar-product-passenger-booking
title: "Stage-Gate: PCI-Compliant Payment Redesign Discovery"
---

# PRD-2.5 Stage-Gate — Passenger Booking

## Law Summary

Discovery proceeds through defined stages. Each stage has a required evidence output. Do not redesign the payment flow before validating which friction point drives the most abandonment.

---

## ✅ COMPLIANT Example

### Initiative

Payment Flow Redesign — reduce abandonment at the checkout step to increase booking completion rate.

---

### Stage A — Conversion Killer Identification Gate

**Question to answer:** Is price opacity (total price not shown until payment) the top conversion driver, or is it something else (seat selection complexity, bag fee discovery, payment method friction)?

**This matters because:** If seat selection is the #1 conversion killer, investing in all-in price transparency will not move the primary metric. Each hypothesis requires different engineering investment.

**Required evidence before Stage B:**

| Evidence Required | Method | Sample | Owner | Deadline |
|------------------|--------|--------|-------|----------|
| Funnel abandonment by step | Funnel analytics, 3-month lookback | 4M+ sessions | Analytics | Week 2 |
| Step-level abandonment root cause | Session recording review with abandonment tagging | 200 sessions at highest-abandonment step | UX Researcher | Week 3 |
| Usability test: top friction moments | Moderated usability sessions with 5-question protocol | 20 sessions (leisure + business travelers) | UX Researcher | Week 3 |
| DOT compliance gap assessment | Legal review of current price display vs. 14 CFR Part 399 | Legal + Compliance | Week 2 |
| PCI-DSS scope assessment | Current payment flow PCI scope review | Compliance Engineer | Week 2 |

**Stage A Acceptance Thresholds:**

| Hypothesis | Confirmed If |
|-----------|-------------|
| Price opacity is #1 | Payment step has highest abandonment AND ≥ 50% of session recordings show price-related hesitation |
| Seat selection is #1 | Seat selection step has highest abandonment AND usability tests confirm fee confusion |
| Payment method friction | Card entry step has highest abandonment AND ≥ 30% cite payment method unavailability |

**Stage A Gate Decision (Week 4):**
- ✅ Proceed to Stage B on the validated #1 hypothesis.
- ❌ If tied: run 2-week A/B test on the top 2 hypotheses (price display vs. seat selection clarity) before Stage B design begins.

---

### Stage B — Solution Design Gate (If Price Opacity Confirmed)

**Required before engineering starts:**
- All-in price calculation validated with Finance and Tax (correct fee inclusion)
- PCI-DSS impact assessment: does showing all-in earlier change tokenization flow?
- Prototype of all-in search results tested with 8 booking completers
- Legal sign-off: DOT 14 CFR Part 399 compliance achieved with proposed display

---

## ❌ VIOLATION Example

> "The payment page looks outdated. Let's redesign it with a new layout, add Apple Pay and Google Pay, show a fee breakdown, and add a progress bar. That should improve conversion."

**Why this violates PRD-2.5:**
- No Stage A: is the payment page the highest-abandonment step? What is the root cause?
- Apple Pay and Google Pay are solutions to a payment method friction hypothesis that hasn't been tested.
- Fee breakdown shown at payment (not search) does not fix price opacity.
- Progress bar addresses navigation anxiety — unvalidated as a conversion driver.
- Correct first step: funnel analysis to confirm payment step is the problem, then session recordings to identify root cause.
