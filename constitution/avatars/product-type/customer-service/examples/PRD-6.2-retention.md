---
law: PRD-6.2
avatar: avatar-product-customer-service
title: "Retention: Post-IROP Customer Rebook Rate by Channel"
---

# PRD-6.2 Retention Law — Customer Service

## Law Summary

Retention is the north-star metric. Acquisition spend is gated on retention performance. Measure 90-day behavior, not immediate satisfaction.

---

## ✅ COMPLIANT Example

### Context

After a major IROP event at ORD (weather cancellation affecting 420 flights, 38,000 passengers), the product team wants to understand whether self-service rebooking produces better long-term outcomes than agent-assisted rebooking.

### Retention Study Design

**Cohort:** All passengers who experienced a flight cancellation at ORD during the December 2025 winter storm event (n=38,000).

**Segmentation by recovery channel:**

| Channel | n | Recovery Time (avg) |
|---------|---|-------------------|
| Self-service rebook (app/web) | 12,400 | 11 minutes |
| Agent-assisted (phone) | 18,200 | 34 minutes |
| Agent-assisted (gate) | 7,400 | 28 minutes |

**90-Day Rebook Rate (primary retention metric):**

| Channel | 90-Day Rebook Rate | vs. Pre-IROP Baseline |
|---------|--------------------|----------------------|
| Self-service rebook | 68% | +2pp |
| Agent-assisted (phone) | 34% | −32pp |
| Agent-assisted (gate) | 41% | −25pp |
| No rebooking (abandoned) | 18% | −48pp |

**Finding:** Customers who successfully self-rebook during IROP are **2× more likely to rebook** within 90 days compared to those who reached a phone agent. The hypothesis is confirmed.

### Retention Metric (North Star)

**90-day rebook rate post-IROP by channel.** Tracked monthly; segmented by: self-serve vs. agent, AAdvantage status, domestic vs. international.

### Investment Gate

Self-service IROP rebooking expansion to connecting itineraries proceeds only when: self-serve 90-day rebook rate ≥ 65% sustained over 3 consecutive IROP events. Current: 68% ✅.

### What This Blocks

If self-serve 90-day rebook rate drops below 55%: pause expansion and investigate. Do not expand scope based on short-term CSAT alone.

---

## ❌ VIOLATION Example

> "CSAT scores during IROP were 3.8/5.0 for self-serve vs. 3.4/5.0 for phone. Self-serve is better. Let's expand."

**Why this violates PRD-6.2:**
- CSAT at the interaction moment is a leading indicator, not a retention outcome.
- A customer can rate self-serve 4.5/5.0 and never fly AA again.
- A customer can rate phone support 3.0/5.0 and become a loyal AAdvantage Gold member.
- The correct metric is 90-day rebook rate — measure it, gate expansion on it.
