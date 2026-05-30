---
avatar: avatar-product-marketing-personalization
use_case: campaign-attribution
file_type: use-case-readme
---

# Use Case: Campaign Attribution

**Avatar:** `avatar-product-marketing-personalization`
**Platform:** TOP (Targeted Offer Platform), Unity Catalog, Databricks
**Relevant Laws:** PRD-1.5, PRD-6.2, BUS-7.1

---

## Overview

Campaign attribution answers the question: **did this offer cause this booking?**
Without a rigorous attribution methodology, teams mistake organic demand for campaign
impact — overstating ROI, misdirecting investment, and making strategy decisions based
on noise rather than signal.

This use case describes the workflow for attributing bookings to offer campaigns, from
defining attribution windows through to incremental lift reporting and LTV impact measurement.

---

## Step 1 — Define Attribution Windows

Attribution windows define how long after an offer interaction a booking can be credited
to that offer. Different channels and offer types warrant different windows.

**Attribution window configuration:**

| Channel | Interaction Type | Attribution Window | Rationale |
|---------|-----------------|-------------------|-----------|
| Email | Click | 30 days | Leisure travel research-to-book cycle averages 21 days |
| Email | Last-touch | 7 days | Conservative window for last email in a sequence |
| App | Click | 30 days | Same booking cycle; high-intent context |
| Web | Click | 30 days | Same booking cycle |
| Loyalty (Ventana) | Any interaction | 90 days | Loyalty offers have longer consideration cycles |
| View-through (app banner) | Impression (no click) | 1 day | Only for high-confidence session-context impressions |

**Window selection principle:** Use the longest window supported by evidence of causal
relationship. Do not use short windows to inflate conversion counts (cherry-picking) or
long windows that capture organic demand (false attribution).

---

## Step 2 — Link Delivery to Conversion

**Join offer delivery events to booking events using customer_id_hash and timestamp window.**

```sql
-- Attribution join: link offer clicks to bookings within the attribution window
WITH offer_clicks AS (
  SELECT
    oda.audit_id,
    oda.customer_id_hash,
    oda.offer_id,
    oda.campaign_id,
    oda.channel,
    oda.model_version,
    oda.click_at,
    oda.experiment_group,  -- from decision_reason field, parsed
    -- Attribution window end date by channel
    CASE oda.channel
      WHEN 'loyalty' THEN DATEADD(day, 90, oda.click_at)
      ELSE DATEADD(day, 30, oda.click_at)
    END AS attribution_window_end
  FROM marketing.offer_decisions_audit oda
  WHERE oda.click_at IS NOT NULL
    AND oda.campaign_id = :campaign_id  -- parameterized
),
attributed_bookings AS (
  SELECT
    oc.audit_id,
    oc.customer_id_hash,
    oc.offer_id,
    oc.campaign_id,
    oc.channel,
    oc.model_version,
    oc.click_at,
    oc.experiment_group,
    b.booking_id,
    b.booked_at,
    b.revenue,
    b.origin_airport,
    b.destination_airport,
    DATEDIFF(day, oc.click_at, b.booked_at) AS days_click_to_booking
  FROM offer_clicks oc
  -- Last-touch attribution: take the booking closest to (but after) the click
  LEFT JOIN booking_events b
    ON oc.customer_id_hash = b.customer_id_hash
    AND b.booked_at > oc.click_at
    AND b.booked_at <= oc.attribution_window_end
  -- For customers with multiple clicks on the same campaign, take most recent click
  QUALIFY ROW_NUMBER() OVER (
    PARTITION BY oc.customer_id_hash, oc.campaign_id, b.booking_id
    ORDER BY oc.click_at DESC
  ) = 1
)
SELECT * FROM attributed_bookings;
```

**Important:** A booking attributed to a campaign must NOT also be attributed to another
campaign in the same time window. Deduplication logic:

```sql
-- Deduplication: if a booking is within the attribution window of multiple campaigns,
-- assign to the campaign with the click closest to the booking date (last-touch)
SELECT
  booking_id,
  FIRST_VALUE(campaign_id) OVER (
    PARTITION BY booking_id
    ORDER BY days_click_to_booking ASC
  ) AS attributed_campaign_id
FROM attributed_bookings
WHERE booking_id IS NOT NULL;
```

---

## Step 3 — Calculate Incremental Lift

**Raw conversion rate is not an acceptable attribution metric. Incrementality requires a holdout group.**

### Why Raw Conversion Rate Is Misleading

If 8.6% of lapsed customers who received an offer booked within 90 days, that sounds
like a strong campaign result. But if 4.0% of lapsed customers would have booked anyway
(natural re-engagement), then the campaign's incremental impact is only 4.6pp — not 8.6pp.
Reporting 8.6% without a holdout overstates campaign ROI by 2.15x.

### Holdout-Based Incrementality Calculation

```sql
-- Incremental lift: treatment vs. holdout (no-offer) group
WITH cohort_summary AS (
  SELECT
    experiment_group,
    COUNT(DISTINCT customer_id_hash) AS customers_in_group,
    COUNTIF(conversion_at IS NOT NULL) AS customers_who_converted,
    SUM(revenue_attributed) AS total_attributed_revenue,
    AVG(revenue_attributed) AS avg_revenue_per_customer
  FROM marketing.offer_decisions_audit
  WHERE campaign_id = :campaign_id
    AND experiment_group IN ('treatment', 'holdout')
  GROUP BY experiment_group
),
treatment AS (SELECT * FROM cohort_summary WHERE experiment_group = 'treatment'),
holdout AS (SELECT * FROM cohort_summary WHERE experiment_group = 'holdout')
SELECT
  treatment.customers_in_group AS treatment_n,
  holdout.customers_in_group AS holdout_n,
  ROUND(treatment.customers_who_converted * 100.0 / treatment.customers_in_group, 2) AS treatment_conversion_rate_pct,
  ROUND(holdout.customers_who_converted * 100.0 / holdout.customers_in_group, 2) AS holdout_conversion_rate_pct,
  ROUND(
    (treatment.customers_who_converted * 1.0 / treatment.customers_in_group)
    - (holdout.customers_who_converted * 1.0 / holdout.customers_in_group),
    4
  ) AS incremental_conversion_rate,
  ROUND(
    ((treatment.customers_who_converted * 1.0 / treatment.customers_in_group)
    - (holdout.customers_who_converted * 1.0 / holdout.customers_in_group))
    * treatment.customers_in_group,
    0
  ) AS incremental_bookings,
  ROUND(treatment.avg_revenue_per_customer - holdout.avg_revenue_per_customer, 2) AS incremental_revenue_per_customer,
  ROUND(
    ((treatment.customers_who_converted * 1.0 / treatment.customers_in_group)
    - (holdout.customers_who_converted * 1.0 / holdout.customers_in_group))
    * treatment.customers_in_group
    * (treatment.avg_revenue_per_customer - holdout.avg_revenue_per_customer),
    0
  ) AS incremental_total_revenue
FROM treatment, holdout;
```

### 90-Day Re-Engagement Rate (PRD-6.2 North Star)

```sql
-- 90-day re-engagement: % of lapsed customers who book within 90 days
-- (requires 90-day wait from campaign launch before measurement)
SELECT
  experiment_group,
  COUNT(DISTINCT oda.customer_id_hash) AS customers,
  COUNTIF(b.booking_id IS NOT NULL) AS customers_who_rebooked,
  ROUND(COUNTIF(b.booking_id IS NOT NULL) * 100.0 / COUNT(DISTINCT oda.customer_id_hash), 2) AS re_engagement_rate_pct
FROM marketing.offer_decisions_audit oda
LEFT JOIN booking_events b
  ON oda.customer_id_hash = b.customer_id_hash
  AND b.booked_at > oda.delivered_at
  AND b.booked_at <= DATEADD(day, 90, oda.delivered_at)
WHERE oda.campaign_id = :campaign_id
GROUP BY experiment_group;
```

---

## Step 4 — Report to Stakeholders

**Attribution report must separate incremental metrics from raw totals.**

### Campaign Attribution Report Template

**Campaign:** `CAMP-2026-Q1-WINBACK`
**Measurement date:** 90 days post-launch
**Prepared by:** Dr. Priya Patel (Data Scientist)
**For:** Sarah Kim (Marketing Strategist), Alex Chen (Campaign Manager), Finance

---

#### Primary Outcome (PRD-6.2 North Star)

| Metric | Treatment | Holdout | Incremental |
|--------|-----------|---------|-------------|
| 90-day re-engagement rate | 8.6% | 3.9% | **+4.7pp** |
| Customers re-engaged | 356 | 8 (of 207) | ~310 incremental |

**Gate check:** 8.6% ≥ 8% threshold → **Q1 gate MET**. Q2 campaigns approved.

---

#### Secondary Outcome (LTV Uplift)

| Metric | Treatment | Holdout | Incremental |
|--------|-----------|---------|-------------|
| 90-day avg revenue/customer | $491 | $298 | **+$193** |
| Total incremental revenue | — | — | **$2,343,600** |

---

#### Campaign Cost and ROI

| Metric | Value |
|--------|-------|
| Campaign cost (email delivery + offer discount) | $187,000 |
| Incremental revenue | $2,343,600 |
| **ROI** | **12.5x** |
| Cost per incremental booking | $603 |

---

#### Leading Indicators (Tertiary — context only, NOT success metrics)

| Metric | Value | Note |
|--------|-------|------|
| Email CTR | 1.7% | Exceeded 1.5% target — positive signal |
| Email open rate | 18.4% | Above industry average (14–16%) |
| Total impressions | 4,143 | Treatment group size |

**Note to stakeholders:** CTR and open rate indicate the offer creative and subject
line were effective. They are reported as context, not as campaign success criteria.
The success criteria are the 90-day re-engagement rate and incremental LTV above.

---

#### Opt-Out Rate (Guardrail)

| Metric | Treatment | Control | Δ | Status |
|--------|-----------|---------|---|--------|
| Opt-out rate | 0.29% | 0.38% | -0.09pp | ✅ Improved |

---

### Attribution Limitations Disclosure

Include in every report:

1. **Last-touch attribution:** This report uses last-touch attribution (30-day window for email). Customers who were influenced by multiple campaigns before booking are attributed to the last campaign they clicked. Multi-touch attribution is not currently implemented.

2. **View-through not included:** Only click-attributed bookings are counted. Impression-only influence (customer saw the offer, didn't click, but later booked) is not measured.

3. **Holdout group size:** The holdout group (n = 207) is small relative to the treatment group (n = 4,143). The incremental conversion rate estimate has a margin of error of ±1.2pp at 90% confidence. Interpret incremental figures as approximate.

4. **Seasonal confounds:** Q1 2026 included Presidents' Day and Valentine's Day, both high-travel periods. The holdout group controls for this, but any unequal distribution of high-season bookers between groups could affect results.
