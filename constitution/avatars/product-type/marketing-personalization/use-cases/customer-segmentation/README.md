---
avatar: avatar-product-marketing-personalization
use_case: customer-segmentation
file_type: use-case-readme
---

# Use Case: Customer Segmentation & Targeting

**Avatar:** `avatar-product-marketing-personalization`
**Platform:** TOP (Targeted Offer Platform), Customer Data Platform (CDP), Unity Catalog
**Relevant Laws:** PRD-1.1, PRD-1.2, BUS-4.3, BUS-7.1

---

## Overview

This use case describes the workflow for building a targeting segment, validating its
quality, deploying it to the TOP platform, and maintaining it with appropriate governance.
Segments are the foundation of every offer campaign — a poorly built segment wastes
budget and degrades customer experience.

---

## Step 1 — Business Question

**Every segment starts with a specific, answerable business question.**

Do not start by choosing a segment; start by articulating the problem you are trying to solve.

**Example business question:**
> "Which customers are at high risk of churning in the next 90 days and have enough
> loyalty value to justify a targeted win-back offer?"

**Why this framing matters:**
- It constrains the segment to customers worth targeting (not all lapsed customers)
- It forces a loyalty value threshold (ROI consideration)
- It sets up measurable success: did we reduce churn in this specific population?

**Compliant framing (specific, actionable):**
> "Customers with last booking > 180 days, no offer engagement in 90 days, and AAdvantage Gold or higher tier"

**Non-compliant framing (too broad):**
> "All inactive customers"
→ This creates a massive, low-precision segment that wastes budget and fatigues customers.

---

## Step 2 — Data Sources

**Identify and validate data sources before writing segment logic.**

| Data Source | System | Latency | Quality Check Required |
|-------------|--------|---------|----------------------|
| AAdvantage booking history (recency/frequency) | Unity Catalog: `booking_history` | Near-real-time (< 4 hours) | Verify no duplicate bookings from data pipeline retries |
| Offer engagement history | Unity Catalog: `marketing.offer_decisions_audit` | < 1 hour (event-driven) | Verify impression/click tracking is active for recent campaigns |
| Loyalty tier | Unity Catalog: `customer_profile.loyalty_tier` | Near-real-time | Verify tier reflects last qualification cycle |
| Opt-out status | Unity Catalog: `customer_profile.opted_out_at` | < 24 hours (sync from Marigold) | CRITICAL: must be current before segment export |
| c_lpr score | Unity Catalog: `customer_profile.c_lpr_score` | Weekly refresh (Monday 2 AM CT) | Check `c_lpr_score_updated_at` — if > 7 days old, use with caution |

**Data freshness check (run before any campaign segment export):**

```sql
-- Verify data freshness of key fields
SELECT
  MAX(last_booking_at) AS most_recent_booking_event,
  MAX(opted_out_at) AS most_recent_opt_out,
  MAX(c_lpr_score_updated_at) AS most_recent_c_lpr_refresh,
  DATEDIFF(hour, MAX(last_booking_at), CURRENT_TIMESTAMP()) AS booking_data_age_hours,
  DATEDIFF(hour, MAX(c_lpr_score_updated_at), CURRENT_TIMESTAMP()) AS c_lpr_age_hours
FROM marketing.customer_profile;
-- Alert if booking_data_age_hours > 6 or c_lpr_age_hours > 168 (7 days)
```

---

## Step 3 — Segment Definition

**Churn Risk: High-Value Lapsed Customers (c_lpr)**

```sql
-- Segment: high-value lapsed customers for win-back campaign
-- Named: lapsed_gold_plus_winback_q1_2026
WITH base_segment AS (
  SELECT
    cp.customer_id_hash,
    cp.loyalty_tier,
    cp.c_lpr_score,
    cp.last_booking_at,
    cp.opted_out_at,
    cp.emails_sent_7d,
    -- Offer engagement: did they click or convert any offer in last 90 days?
    MAX(oda.click_at) AS last_offer_click_at
  FROM marketing.customer_profile cp
  LEFT JOIN marketing.offer_decisions_audit oda
    ON cp.customer_id_hash = oda.customer_id_hash
    AND oda.delivered_at >= DATEADD(day, -90, CURRENT_DATE())
  WHERE
    -- Core lapse criterion
    cp.last_booking_at < DATEADD(day, -180, CURRENT_DATE())
    -- Loyalty value threshold
    AND cp.loyalty_tier IN ('Gold', 'Platinum Pro', 'Executive Platinum')
    -- BUS-4.3: exclude opted-out customers
    AND cp.opted_out_at IS NULL
    -- Propensity filter: only worth targeting if propensity score is high enough
    AND cp.c_lpr_score > 0.7
    -- Communication cap
    AND cp.emails_sent_7d < 3
  GROUP BY
    cp.customer_id_hash, cp.loyalty_tier, cp.c_lpr_score,
    cp.last_booking_at, cp.opted_out_at, cp.emails_sent_7d
)
SELECT
  customer_id_hash,
  loyalty_tier,
  c_lpr_score,
  last_booking_at,
  DATEDIFF(day, last_booking_at, CURRENT_DATE()) AS days_since_last_booking,
  last_offer_click_at,
  -- No offer engagement in last 90 days = confirmed disengaged
  CASE WHEN last_offer_click_at IS NULL THEN true ELSE false END AS no_recent_offer_engagement
FROM base_segment
WHERE last_offer_click_at IS NULL  -- truly disengaged, not just lapsed
ORDER BY c_lpr_score DESC, days_since_last_booking DESC;
```

**Segment logic summary:**
- Last booking > 180 days ago
- No offer click in last 90 days
- AAdvantage Gold, Platinum Pro, or Executive Platinum tier
- c_lpr score > 0.7 (high propensity to respond if targeted)
- Not opted out (`opted_out_at IS NULL`)
- Not at communication cap (`emails_sent_7d < 3`)

---

## Step 4 — Validation

**Segment validation is mandatory before any campaign deployment.**

### Check 1: Segment Size

```sql
SELECT
  COUNT(*) AS total_segment_size,
  COUNT(*) >= 5000 AS meets_minimum_for_statistical_power
FROM lapsed_gold_plus_winback_q1_2026;
-- Minimum 5,000 for any campaign with a holdout group
-- Minimum 10,000 per arm if running an A/B test within the segment
```

### Check 2: Opt-Out Exclusion Verification

```sql
-- This MUST return 0 — any opted-out customer in segment is a BUS-4.3 violation
SELECT COUNT(*) AS opted_out_customers_in_segment
FROM lapsed_gold_plus_winback_q1_2026 s
JOIN marketing.customer_profile cp ON s.customer_id_hash = cp.customer_id_hash
WHERE cp.opted_out_at IS NOT NULL;
```

### Check 3: Overlap with Other Active Campaigns

```sql
-- Identify customers already in another active campaign this week
-- to prevent duplicate offers and channel conflicts
SELECT
  s.customer_id_hash,
  existing.campaign_id AS conflicting_campaign
FROM lapsed_gold_plus_winback_q1_2026 s
JOIN marketing.offer_decisions_audit existing
  ON s.customer_id_hash = existing.customer_id_hash
  AND existing.delivered_at >= DATEADD(day, -7, CURRENT_DATE())
  AND existing.campaign_id != 'CAMP-2026-Q1-WINBACK'
WHERE existing.customer_id_hash IS NOT NULL;
-- Review and deduplicate before campaign launch
```

### Check 4: Spot-Check 10 Customer Profiles

CRM Analyst (Marcus Williams) manually reviews 10 randomly sampled customer profiles
to verify the segment logic is producing expected results:

```sql
-- Sample 10 customers for manual validation
SELECT
  customer_id_hash,
  loyalty_tier,
  c_lpr_score,
  last_booking_at,
  days_since_last_booking,
  no_recent_offer_engagement
FROM lapsed_gold_plus_winback_q1_2026
ORDER BY RAND()
LIMIT 10;
```

For each sampled customer, verify in the CRM system:
- ✅ Last booking date matches — customer is genuinely lapsed
- ✅ Loyalty tier is correct
- ✅ Customer has not booked since the segment was built (recency check)
- ✅ No active opt-out in Marigold preference center

### Check 5: Distribution Sanity Check

```sql
-- Verify segment distribution looks reasonable
SELECT
  loyalty_tier,
  COUNT(*) AS count,
  ROUND(AVG(c_lpr_score), 3) AS avg_c_lpr_score,
  ROUND(AVG(days_since_last_booking), 0) AS avg_days_lapsed,
  MIN(days_since_last_booking) AS min_days_lapsed,
  MAX(days_since_last_booking) AS max_days_lapsed
FROM lapsed_gold_plus_winback_q1_2026
GROUP BY loyalty_tier
ORDER BY loyalty_tier;
-- Red flag: if avg_days_lapsed < 200 (something wrong with filter)
-- Red flag: if avg_c_lpr_score < 0.65 (score filter may not be working)
```

---

## Step 5 — Deployment to Campaigns

### Export Segment to TOP Targeting API

```sql
-- Export final segment to TOP targeting table
-- Refresh daily via Databricks job (maintains freshness)
CREATE OR REPLACE TABLE marketing.top_segments.lapsed_gold_plus_winback_q1_2026
AS SELECT
  customer_id_hash,
  loyalty_tier,
  c_lpr_score,
  'lapsed_gold_plus_winback_q1_2026' AS segment_id,
  CURRENT_TIMESTAMP() AS segment_built_at
FROM lapsed_gold_plus_winback_q1_2026;
```

### Refresh Cadence

| Setting | Value | Rationale |
|---------|-------|-----------|
| Refresh schedule | Daily at 2 AM CT | Opt-out sync completes by 1 AM; daily refresh ensures fresh opt-out exclusion |
| Refresh trigger | Databricks scheduled job + opt-out event trigger | Event trigger for urgent opt-outs |
| Staleness alert | Alert if `segment_built_at` > 28 hours before campaign delivery | Prevents stale segment deployment |

### Suppression Rules Applied at Delivery

Even after segment export, TOP applies these suppression rules at delivery time:
1. **Re-check opt-out:** `opted_out_at IS NULL` (defense-in-depth; catches opt-outs between segment refresh and delivery)
2. **Communication cap:** `emails_sent_7d < 3` (re-checked at delivery, not just at segment build)
3. **Channel deduplication:** customer not already receiving an offer via another channel in the last 24 hours

### Monitoring During Campaign Flight

| Metric | Check Frequency | Alert Threshold | Owner |
|--------|----------------|-----------------|-------|
| Segment size (daily refresh) | Daily | Drops > 20% from baseline | CRM Analyst |
| Opt-out rate | Daily | > 0.4% | Campaign Manager |
| Delivery failure rate | Per send | > 2% | Campaign Manager |
| Opted-out customers in delivered set | Per send | > 0 | CRM Analyst (BUS-4.3 critical) |
