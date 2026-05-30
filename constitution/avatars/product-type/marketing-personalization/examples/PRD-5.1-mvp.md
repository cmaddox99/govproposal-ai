---
avatar: avatar-product-marketing-personalization
law_id: PRD-5.1
law_title: "MVP Law"
file_type: example
---

# PRD-5.1 MVP Law — Marketing Personalization

## Law Summary

The smallest possible experiment that validates the offer hypothesis is the correct
first investment. Do not build the full ML stack before testing whether the hypothesis
is correct with a rule-based or manual approach.

---

## ✅ COMPLIANT Example — MVP Canvas: Win-Back Offer Experiment

### Hypothesis

> Lapsed c_lpr customers (no booking in 180+ days, c_lpr score > 0.7) will book
> within 90 days at a rate ≥ 8% if shown a destination-matched offer based on their
> top historical route, compared to the ~4% natural re-engagement baseline.

### Riskiest Assumption

> Destination matching is sufficient to drive re-engagement for lapsed customers.
> If destination-matched rule-based offers achieve ≥ 1.5% CTR, the signal is strong
> enough to justify a full propensity model. If CTR < 1.5%, the problem is not
> destination relevance—it may be offer value, timing, or channel.

---

### MVP Approach (Rule-Based SQL, NOT ML)

**What we build:** A SQL-based offer selection rule that assigns each lapsed c_lpr customer their top historical booking destination, then selects the best available offer for that destination from the active catalog.

**What we explicitly do NOT build:**
- Real-time ML scoring API or Databricks Model Serving endpoint
- Feature store integration or retraining pipeline
- A/B testing infrastructure beyond a simple SQL holdout split
- Campaign management UI changes or new EMFT/Marigold integration

**Total engineering time:** ~3 days (1 data scientist writing SQL + campaign manager config). No sprint tickets required for new infrastructure.

---

### Experiment Setup

| Parameter | Value |
|-----------|-------|
| Pilot audience | 5% of eligible lapsed c_lpr customers ≈ 4,350 customers |
| Treatment | Destination-matched offer via rule-based SQL assignment |
| Holdout | No offer (suppressed from this campaign) |
| Duration | 2 weeks from first email delivery |
| Channel | Email only (EMFT → Marigold, existing batch pipeline) |
| Re-engagement measurement | 90 days from first delivery date |

---

### Success Metrics

**Primary (validate hypothesis):**
- Email CTR ≥ 1.5% — indicates destination matching drives click intent

**Secondary (validate business case):**
- 90-day re-engagement rate ≥ 8% in treatment vs. ~4% in holdout

**Guardrail (must not worsen):**
- Opt-out rate ≤ 0.4%

---

### Decision Criteria

| Outcome | Evidence | Decision |
|---------|----------|----------|
| ✅ CTR ≥ 1.5% AND opt-out ≤ 0.4% | Destination hypothesis validated | Invest in propensity model v2 (Q2 2026) |
| ⚠️ CTR 1.0–1.4% AND opt-out ≤ 0.4% | Partial validation | Add recency/discount features to rule; re-test |
| ❌ CTR < 1.0% | Destination hypothesis not validated | Investigate timing/frequency; do NOT invest in ML |
| ❌ Opt-out > 0.4% | Campaign causing fatigue | Pause; reduce frequency; investigate offer value |

---

## ❌ VIOLATION Example

> "To properly test our personalization hypothesis we need to: rebuild the campaign pipeline,
> retrain all propensity models (3-month effort), implement a real-time scoring API,
> build A/B testing infrastructure with significance dashboards, and integrate all channels
> before running a single test. Estimated: 6 months, 5 engineers."

**Why this violates PRD-5.1:**

| PRD-5.1 Requirement | Violation |
|--------------------|-----------|
| Smallest experiment to validate hypothesis | 6-month build before any test |
| Rule-based MVP before ML investment | ML models rebuilt before hypothesis is validated |
| 5% traffic slice for initial experiment | Full pipeline rebuild affects 100% of campaigns |
| Success threshold defined upfront | No success threshold; cannot know when to stop building |
| Decision criteria at end | No gate defined; build continues regardless of outcome |

**Consequence:** If the destination-matching hypothesis is wrong, 6 months of infrastructure spend is wasted. The rule-based SQL approach in the compliant example costs 3 engineer-days and answers the same question.

**Correct first step:** Run the 2-week rule-based pilot. Invest in the ML stack only after the pilot confirms CTR ≥ 1.5%.
