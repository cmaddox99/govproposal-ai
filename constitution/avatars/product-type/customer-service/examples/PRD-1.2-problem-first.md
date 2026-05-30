---
law: PRD-1.2
avatar: avatar-product-customer-service
title: "Problem-First: IROP Rebooking vs. AI Chatbot"
---

# PRD-1.2 Problem-First — Customer Service

## Law Summary

Validate the real problem before committing to a solution. The stated request often reflects a solution bias, not a validated problem.

---

## ✅ COMPLIANT Example

### Stated Request

> "Build an AI chatbot to handle all customer service queries so we can reduce call center headcount."

### Research Conducted

4 weeks of call recording analysis (n=2,400 calls during 2 major IROP events at ORD and DFW) plus post-interaction surveys (n=1,800 responses).

| Finding | Value | Source |
|---------|-------|--------|
| % of IROP call volume that is rebooking requests | 67% | Call recording analysis |
| % of rebooking calls resolved without supervisor escalation | 89% | Call recording analysis |
| Average handle time for IROP rebooking | 8 minutes | AHT system |
| Average handle time for complaint resolution | 24 minutes | AHT system |
| % of customers who prefer self-service for simple rebooking | 73% | Post-interaction survey |
| % of customers who prefer human agent for complaint resolution | 81% | Post-interaction survey |

### Validated Problem Statement

> During major IROP events, 67% of call volume is same-day rebooking requests for simple domestic itineraries. These calls average 8 minutes and are resolved without escalation 89% of the time. This is a **self-service automation opportunity**, not an AI chatbot problem. An AI chatbot that handles "all queries" will not reduce this bottleneck — customers who need to rebook want to do so immediately, not converse with a bot.

### Correct Solution Direction

Self-service IROP rebooking for simple same-day domestic itinerary changes (no codeshare, no group, no multi-city). Estimated call deflection at 15%: 6,000 calls/day during major IROP events.

---

## ❌ VIOLATION Example

> "AI chatbots are the future of customer service. We should build a conversational AI that handles all inbound queries: flight status, baggage, rebooking, complaints, AAdvantage questions, and disability accommodation requests."

**Why this violates PRD-1.2:**
- No problem quantified: what % of volume is each category? What is the AHT by category?
- Solution (AI chatbot) proposed before problem is validated.
- "All queries" approach ignores that 81% of customers prefer a human for complaints.
- Complaint resolution and disability accommodation require judgment — AI chatbot will produce compliance failures.

**Correct first step:** Call recording analysis to quantify call mix. Then invest in the highest-volume, most automatable category (IROP rebooking at 67%) first.
