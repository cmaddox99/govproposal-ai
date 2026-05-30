---
avatar: avatar-product-marketing-personalization
law_id: PRD-6.2
law_title: "Retention Over Acquisition"
file_type: example
---

# PRD-6.2 Retention Over Acquisition — Marketing Personalization

## Law Summary

Retaining existing customers is the primary mission of the offer platform. Acquisition
campaigns are a secondary investment, gated on retention performance. The north star
metric is 90-day re-engagement rate, not email open rate or impression count.

---

## ✅ COMPLIANT Example — KPI Hierarchy and Roadmap Gate

### KPI Hierarchy

| Tier | KPI | Definition | Target | Reporting Cadence |
|------|-----|------------|--------|-------------------|
| **Primary (North Star)** | 90-day re-engagement rate | % of lapsed customers (no booking in 180+ days) who complete a booking within 90 days of receiving a win-back offer | ≥ 8% | Monthly (requires 90-day lag) |
| **Secondary** | Incremental LTV uplift vs. holdout | (Avg 90-day revenue per customer, treatment) − (Avg 90-day revenue per customer, no-offer holdout) | ≥ $50/customer | Quarterly |
| **Tertiary** | Email CTR | Clicks / delivered offers | ≥ 1.5% (leading indicator) | Weekly during campaign flight |
| **Tertiary** | Email open rate | Opens / delivered offers | Diagnostic only | Weekly during campaign flight |
| **Tertiary** | Impression count | Raw offer impressions | Volume metric only | Weekly during campaign flight |

**Hierarchy enforcement rules:**

1. **CTR and open rate are NEVER reported to the exec team as primary success metrics.**
   They are useful for diagnosing delivery or creative issues mid-flight, but they do
   not measure whether the offer platform is creating business value.

2. **A campaign with high CTR but flat 90-day re-engagement is NOT a success.**
   Click-through is a leading indicator, not an outcome.

3. **Impression count is not a success metric.** Sending more offers to drive up impression
   count reduces margin and increases fatigue risk.

---

### Roadmap Gate: Acquisition Gated on Retention

**Gate definition:**
> Q2 2026 acquisition campaigns do NOT launch until the Q1 win-back campaign achieves
> 90-day re-engagement rate ≥ 8% as measured 90 days after the first Q1 campaign send.

**Gate measurement date:** 2026-04-15 (90 days after 2026-01-14 Q1 launch)

**Gate logic:** If re-engagement ≥ 8% → Q2 acquisition campaigns approved. If < 8% → Q2 acquisition BLOCKED; root cause analysis required (offer relevance, channel mix, timing); iterate on retention.

**Who enforces the gate:** Marketing Strategist (Sarah Kim). Gate outcome documented in decision log (PRD-1.5 compliance).

---

### Example: Q1 Gate Measurement

| Cohort | Group | Customers | 90-Day Bookings | Re-Engagement Rate | Avg Revenue |
|--------|-------|-----------|-----------------|-------------------|-------------|
| Lapsed (180+ days) | Treatment | 4,143 | 356 | 8.6% | $491 |
| Lapsed (180+ days) | No-offer holdout | 207 | 8 | 3.9% | $298 |

**Gate result:** 8.6% ≥ 8% → **GATE MET**. Incremental LTV: $491 − $298 = $193/customer.
**Decision:** Q2 acquisition campaigns approved.

---

### Correct Reporting Template (exec summary)

> **Q1 2026 Win-Back Campaign Results**
>
> Primary outcome: 90-day re-engagement rate = **8.6%** (gate threshold: 8%) ✅
> Secondary outcome: Incremental LTV = **$193/customer** vs. holdout ✅
> Leading indicators (FYI): CTR = 1.7%, open rate = 18.4%
>
> Gate met. Q2 acquisition campaigns approved per roadmap.

---

## ❌ VIOLATION Example

### Violation 1 — Optimizing for Open Rate as Primary KPI

> "Our Q1 campaign was a huge success! Open rate hit 22%, our best ever.
> We're going to double down and send more emails to drive more opens."

**Why this violates PRD-6.2:**

| PRD-6.2 Requirement | Violation |
|--------------------|-----------|
| 90-day re-engagement is the north star | Open rate reported as primary success metric |
| LTV uplift is secondary | No LTV measurement |
| CTR and open rate are tertiary | Open rate used as decision driver |
| No strategy change without evidence | "Double down on more emails" without re-engagement data |

**Risk:** High open rate may reflect a compelling subject line, not offer relevance.
Doubling frequency without re-engagement data will increase opt-out rates and destroy LTV.

---

### Violation 2 — Running Acquisition While Re-Engagement Declines

> "Our lapsed re-engagement rate is at 4% (below the 8% gate), but we have a spring
> acquisition sale ready and don't want to miss the season. Let's run both simultaneously."

**Why this violates PRD-6.2:**

| PRD-6.2 Requirement | Violation |
|--------------------|-----------|
| Retention must hit gate before acquisition launches | Gate not met (4% < 8%) |
| Retention investment prioritized over acquisition | Acquisition launched despite gate failure |
| Evidence-based decision | "Don't want to miss the season" is calendar-driven, not evidence-driven |

---

### Violation 3 — No Holdout Group

> "We ran the Q1 win-back campaign and got 8.6% of lapsed customers booking within
> 90 days. Great result — the campaign worked!"

**Why this is incomplete (PRD-6.2 and PRD-1.5):**

Without a holdout group, we cannot separate campaign-driven from organic re-engagement.
If 4% would have booked anyway, the incremental impact is only 4.6pp — not 8.6pp.

**Measurement:** treatment rate − holdout rate = 8.6% − 3.9% = **4.7pp incremental**.

This distinction determines true ROI and whether to invest further.
