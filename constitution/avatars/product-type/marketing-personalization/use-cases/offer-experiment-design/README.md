---
avatar: avatar-product-marketing-personalization
use_case: offer-experiment-design
file_type: use-case-readme
---

# Use Case: Offer Experiment Design (A/B Testing)

**Avatar:** `avatar-product-marketing-personalization`
**Platform:** TOP (Targeted Offer Platform)
**Relevant Laws:** PRD-1.2, PRD-1.5, PRD-5.1
**BFF Modules:** `MMXOffersController` / `MMXOffersServiceImpl` (mobile-offers-bff), `AirshipController` (aa-ct-mobile-airship)

---

## Overview

This use case describes the end-to-end workflow for designing, launching, analyzing,
and acting on a campaign A/B test in the TOP platform. Every offer strategy change
that affects targeting, ranking, or content must be validated through a pre-registered
experiment before full rollout.

---

## Step 1 — Problem Definition

**Before designing any experiment, state the hypothesis clearly.**

A well-formed offer hypothesis has three parts:
1. **Observation (evidence):** What data shows there is a problem or opportunity?
2. **Cause (assumption):** What do we believe is driving the observation?
3. **Solution (treatment):** What change do we propose to test?

**Example hypothesis:**
> "We observe that email offers for generic category deals (e.g., 'Save on flights this week')
> achieve CTR of 0.8% on average. We believe destination-specific offers matched to each
> customer's top historical route will outperform generic offers because the offer is
> directly relevant to demonstrated travel intent. We will test destination-matched offers
> against the current generic category offers to validate this hypothesis."

**Document in experiment registry before proceeding to Step 2.**

---

## Step 2 — Experiment Design

### Treatment and Control Definition

| Group | Description | Offer Type |
|-------|-------------|------------|
| **Treatment (80%)** | Destination-matched offers: top 3 routes by customer's booking history in last 24 months | "Save 15% to London — your favorite route" |
| **Control (20%)** | Current rule-based system: generic category offers by loyalty tier | "Save on international flights this week" |

**Why 80/20 (not 50/50)?**
- The treatment is expected to be superior (based on prior correlation analysis: 5.2x CTR gap)
- 80/20 maximizes learning while minimizing exposure to the (expected inferior) control experience
- For high-risk or uncertain experiments, use 50/50 split

### Randomization

- **Unit:** `customer_id_hash` (not session, not email address)
- **Method:** Deterministic hash-based assignment to prevent re-randomization on each run

```sql
-- Deterministic group assignment (stable across runs)
SELECT
  customer_id_hash,
  offer_id,
  CASE
    WHEN MOD(ABS(HASH(customer_id_hash || 'exp-destination-q2-2026')), 100) < 20
    THEN 'control'
    ELSE 'treatment'
  END AS experiment_group
FROM eligible_customers;
```

### Stratification

Stratify by loyalty tier and recency band to ensure balanced arms:

| Strata | Treatment Count | Control Count | Balance Check |
|--------|----------------|---------------|---------------|
| Executive Platinum | ~1,200 | ~300 | ≥ 95% of tier proportion |
| Platinum Pro | ~3,400 | ~850 | ≥ 95% of tier proportion |
| Gold | ~22,000 | ~5,500 | ≥ 95% of tier proportion |
| AAdvantage member | ~53,400 | ~13,350 | ≥ 95% of tier proportion |

### Pre-Registration Checklist

The following must be documented in the experiment registry **before** the experiment launches:

| Field | Value |
|-------|-------|
| Experiment ID | `EXP-2026-0401-DESTINATION-MATCH` |
| Hypothesis | (as stated in Step 1) |
| Primary success metric | Email CTR |
| Secondary success metric | 90-day re-engagement rate |
| Guardrail metrics | Opt-out rate (must not increase), hard unsubscribe rate |
| Minimum detectable effect (primary) | +0.4pp absolute CTR lift (0.8% → 1.2%) |
| Sample size (per arm) | Minimum 10,000 customers |
| Statistical power | 80% |
| α threshold | 0.05 (two-tailed) |
| Planned duration | 14 days minimum |
| Decision criteria (go) | CTR ≥ 1.2% AND p < 0.05 AND guardrails not breached |
| Decision criteria (no-go) | CTR < 1.2% OR p ≥ 0.05 OR any guardrail breached |
| Experiment owner | Alex Chen (Campaign Manager) |
| Analysis owner | Dr. Priya Patel (Data Scientist) |

**No-peeking rule:** Do not evaluate results before the planned end date.
If early stopping is needed for business reasons, apply sequential testing
(O'Brien-Fleming or Pocock correction) to preserve α.

---

## Step 3 — Implementation

### Audience Segment Creation (CDP)

1. In the Customer Data Platform, create segment: `lapsed_high_propensity_q2_2026`
   - Filter: `last_booking_at < DATEADD(day, -90, CURRENT_DATE())`
   - Filter: `c_lpr_score > 0.6`
   - Filter: `opted_out_at IS NULL`
   - Filter: `emails_sent_7d < 3`
   - Expected size: ~80,000 customers
2. Validate segment: spot-check 10 random customer profiles for correctness
3. Export to TOP targeting API with `segment_id = 'lapsed_high_propensity_q2_2026'`

### Offer Variant Configuration (TOP + mobile-offers-bff)

| Variant | Offer Source | Personalization | BFF Entrypoint |
|---------|-------------|-----------------|----------------|
| Treatment | TOP scoring API (model v2) returns top offer by destination affinity score | Subject: "Save [X]% to [DESTINATION]" | `MMXOffersController.getOffers()` → `MMXOffersServiceImpl.rankOffers()` |
| Control | Current rule engine: best offer by loyalty tier and category | Subject: "Save on international flights" | `MMXOffersController.getOffers()` → rule-based `MMXResponseBuilder` |

### Attribution Tracking

- Ensure `campaign_id = 'EXP-2026-0401-DESTINATION-MATCH'` is set on all offer delivery events
- Ensure `experiment_group` (treatment/control) is recorded in `offer_decisions_audit` via `decision_reason` field
- Confirm `click_at` and `conversion_at` tracking is active in Marigold webhook
- For push notifications: verify `AirshipAction` (aa-ct-mobile-airship) includes `campaign_id` in `StatusChangeRequest` payload sent to CHUB

---

## Step 4 — Analysis

Run analysis after minimum 14-day run and minimum 10,000 per arm are reached.

### Primary Metric: CTR

```sql
SELECT
  experiment_group,
  COUNT(*) AS offers_delivered,
  COUNTIF(click_at IS NOT NULL) AS clicks,
  ROUND(COUNTIF(click_at IS NOT NULL) * 100.0 / COUNT(*), 2) AS ctr_pct
FROM marketing.offer_decisions_audit
WHERE campaign_id = 'EXP-2026-0401-DESTINATION-MATCH'
  AND delivered_at BETWEEN '2026-04-01' AND '2026-04-15'
GROUP BY experiment_group;
```

### Statistical Significance (Two-Proportion Z-Test)

```python
from scipy import stats
import numpy as np

control_n = 13_000
control_clicks = 104       # 0.8% CTR
treatment_n = 52_000
treatment_clicks = 988     # 1.9% CTR

p_control = control_clicks / control_n
p_treatment = treatment_clicks / treatment_n
p_pooled = (control_clicks + treatment_clicks) / (control_n + treatment_n)

z = (p_treatment - p_control) / np.sqrt(p_pooled * (1 - p_pooled) * (1/control_n + 1/treatment_n))
p_value = 2 * (1 - stats.norm.cdf(abs(z)))

print(f"CTR Control: {p_control:.3%}")
print(f"CTR Treatment: {p_treatment:.3%}")
print(f"Absolute lift: {(p_treatment - p_control):.3%}")
print(f"p-value: {p_value:.4f}")
print(f"Significant: {p_value < 0.05}")
```

### Guardrail Metric Check

```sql
SELECT
  experiment_group,
  ROUND(COUNTIF(opt_out_triggered_at IS NOT NULL) * 100.0 / COUNT(*), 3) AS opt_out_rate_pct
FROM marketing.offer_decisions_audit
WHERE campaign_id = 'EXP-2026-0401-DESTINATION-MATCH'
GROUP BY experiment_group;
-- STOP EXPERIMENT if treatment opt_out_rate > control opt_out_rate + 0.1pp
```

---

## Step 5 — Decision

### Go/No-Go Documentation

Create a Decision Log entry (PRD-1.5 compliance) with:

| Field | Value |
|-------|-------|
| Decision ID | `DEC-2026-0415-DESTINATION-MATCH` |
| Decision | Go / No-Go (fill in after analysis) |
| Evidence | A/B test results table (CTR, p-value, n), guardrail check results |
| Decision date | Date of analysis completion |
| Decision maker | Marketing Strategist + Campaign Manager |
| Next action | If Go: roll out to 50% of campaigns; if No-Go: document pivot hypothesis |

### Rollout Plan (if Go)

1. Increase treatment allocation from 80% to 100% of targeted campaigns
2. Maintain 20% holdout group on a separate, permanent basis for ongoing incrementality measurement
3. Monitor CTR and opt-out rate weekly for 4 weeks post-rollout
4. Trigger 90-day re-engagement cohort analysis at day 90

### Pivot Plan (if No-Go)

If CTR < 1.2% or guardrails breached:
1. Document the failed hypothesis and evidence in the decision log
2. Investigate next hypothesis per PRD-1.2 decision tree (timing? frequency? offer value?)
3. Do NOT invest in ML model rebuild until a validated hypothesis exists (PRD-5.1)
