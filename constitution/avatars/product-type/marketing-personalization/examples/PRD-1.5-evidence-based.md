---
avatar: avatar-product-marketing-personalization
law_id: PRD-1.5
law_title: "Evidence-Based Decision Making"
file_type: example
---

# PRD-1.5 Evidence-Based Decision Making — Marketing Personalization

## Law Summary

Every significant offer strategy decision must be backed by cited data: A/B test results,
propensity model lift charts, cohort re-engagement analysis, or other quantitative evidence.
Opinion without data is not a valid input to strategy decisions.

---

## ✅ COMPLIANT Example — Decision Log Entry

### Decision: Launch Offer Ranking Model v2 to 50% of Email Campaigns

**Decision ID:** DEC-2026-0312
**Decision Date:** 2026-03-12
**Decision Maker:** Sarah Kim (Marketing Strategist), with sign-off from Alex Chen (Campaign Manager)
**Effective Date:** 2026-03-19 (next campaign flight)

---

### Evidence Table 1: A/B Test Results — Ranking Model v2 vs. Rule-Based System

**Experiment ID:** EXP-2026-0201 | **Run:** 2026-02-01 to 2026-02-28 | **Allocation:** 80% treatment, 20% holdout

| Metric | Control | Treatment (Model v2) | Lift | p-value |
|--------|---------|---------------------|------|---------|
| CTR | 0.8% | 1.9% | +137.5% | 0.02 |
| Conversion rate | 0.18% | 0.41% | +127.8% | 0.03 |
| Opt-out rate | 0.38% | 0.29% | -23.7% | 0.08 |
| Unsubscribe rate | 0.12% | 0.09% | -25.0% | 0.11 |

**Statistical validity:** p < 0.05 on primary metrics (CTR, conversion). Guardrail metrics show favorable direction. 50,000 per arm; duration exceeds 14-day minimum.

---

### Evidence Table 2: Propensity Model Lift Chart — Model v2

**Model:** `top_offer_ranking_v2` | **Holdout set:** 95,000 records

| Decile | Observed Conversion Rate | Lift vs. Random |
|--------|--------------------------|-----------------|
| 1 (top) | 3.78% | 4.2x |
| 2 | 2.91% | 3.2x |
| 3 | 2.14% | 2.4x |
| 4 | 1.42% | 1.6x |
| 5 | 0.93% | 1.0x |
| 6–10 | 0.41% | 0.5x |

**AUC on holdout set: 0.83** (exceeds 0.80 threshold). Serving offers only to top-4 deciles would improve CTR while reducing send volume by 60%.

---

### Evidence Table 3: 90-Day Re-Engagement Cohort Analysis

| Cohort | Group | Customers | 90-Day Re-Engagement | Avg Revenue |
|--------|-------|-----------|---------------------|-------------|
| Lapsed (180+ days) | Treatment (model v2) | 12,400 | 8.0% | $487 |
| Lapsed (180+ days) | Control (rule-based) | 3,100 | 6.0% | $391 |
| Lapsed (180+ days) | No-offer holdout | 3,100 | 4.0% | $298 |

**Incremental re-engagement:** +4.0pp (treatment vs. holdout)
**Incremental LTV per treated customer:** $189 | **Total incremental revenue (lapsed cohort):** $2.3M

---

### Decision Rationale

1. **A/B test confirms CTR improvement:** +137.5% at p = 0.02; guardrails not breached.
2. **Model quality validated:** AUC 0.83 > 0.80 threshold; top-decile 4.2x lift.
3. **Re-engagement target met:** 8.0% treatment vs. 4.0% no-offer holdout; Q1 gate achieved.

**Decision:** Launch model v2 to 50% of email traffic starting 2026-03-19. Remaining 50% continues on rule-based as ongoing holdout.

**Outcome tracking:** Weekly CTR comparison; monthly opt-out monitoring; 90-day cohort analysis to confirm results hold at scale.

---

## ❌ VIOLATION Example

### Decision: Switch All Campaigns to Destination-Based Offers

> "The CMO thinks destination-based offers will resonate better with customers.
> Let's switch all campaigns to destination-based offers for the spring sale."

**Why this violates PRD-1.5:**

| PRD-1.5 Requirement | Violation |
|--------------------|-----------|
| Decision backed by cited data | "The CMO thinks" is opinion, not evidence. |
| A/B test results or lift chart | No experiment conducted. No comparison group. |
| Quantified success metric | No metric defined. "Resonate better" is unmeasurable. |
| Outcome tracking plan | No plan to detect if the decision was wrong. |

**Risk:** Without a holdout group, opt-out rates could rise for 4+ weeks undetected—by which point the spring sale is over.

**Correct approach:** Run a 2-week A/B test with destination-based offers in treatment and current rule-based system in control before committing the strategy change.
