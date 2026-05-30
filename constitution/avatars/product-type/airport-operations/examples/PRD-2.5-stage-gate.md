---
law: PRD-2.5
avatar: avatar-product-airport-operations
title: "Stage-Gate: IROP Recovery Discovery"
---

# PRD-2.5 Stage-Gate — Airport Operations

## Law Summary

Discovery proceeds through defined stages. Each stage has a required evidence output. Stage B does not begin until Stage A evidence is accepted.

---

## ✅ COMPLIANT Example

### Initiative

IROP Recovery Optimization — improve passenger recovery time during major weather disruptions at hub stations.

---

### Stage A — Problem Validation Gate

**Question to answer:** Is delay notification timing the #1 passenger pain point during IROP, or is it something else (rebooking options, hotel vouchers, communication quality)?

**Required evidence before Stage B proceeds:**

| Evidence Required | Method | Owner | Deadline |
|------------------|--------|-------|----------|
| NPS driver analysis: top 3 drivers of IROP NPS score | Regression on post-IROP survey data (n ≥ 500) | Data Analyst | Week 2 |
| Passenger verbatim coding: top complaint themes | Code 200 IROP complaint verbatims by theme | UX Researcher | Week 2 |
| Agent workflow observation: where do passengers get blocked? | Shadow 3 IROP events at DFW, CLT, ORD | Product Manager | Week 3 |
| Quantified impact: cost of current recovery time | Ops Finance analysis of hotel, meal, rebook costs | Finance Partner | Week 3 |

**Stage A Gate Decision (Week 4):**
- ✅ Proceed to Stage B if: delay notification timing is confirmed as top-3 NPS driver in regression AND appears in ≥ 30% of complaint verbatims.
- ❌ Pivot if: rebooking options or hotel vouchers rank higher — redirect scope to the validated top driver.

---

### Stage B — Solution Design Gate (If Stage A Passes)

**Question to answer:** What is the minimum intervention that reduces notification latency for the top passenger pain point?

**Required evidence before build:**
- Prototype of push notification flow tested with 8 stranded passengers in simulated IROP
- Operations Controller confirmation that notification trigger data is available in real time
- Legal review: DOT tarmac delay timer integration requirements

---

## ❌ VIOLATION Example

> "We know IROP is a bad experience. Let's design the full recovery suite: automated rebooking, push notifications, hotel voucher integration, and meal credit system. We'll figure out what passengers care most about as we build."

**Why this violates PRD-2.5:**
- No Stage A evidence gate: what is the #1 pain point?
- "We'll figure it out as we build" = building without validated problem direction.
- Full recovery suite is Stage C or D work, not the discovery starting point.
- If hotel vouchers are the #1 pain point, notification investment is wasted.
