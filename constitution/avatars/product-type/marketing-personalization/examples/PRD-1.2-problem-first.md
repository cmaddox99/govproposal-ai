---
avatar: avatar-product-marketing-personalization
law_id: PRD-1.2
law_title: "Problem-First Development"
file_type: example
---

# PRD-1.2 Problem-First Development — Marketing Personalization

## Law Summary

Before committing any engineering resources to a solution, validate that the problem
is real, quantified, and well-understood. For offer personalization: the problem must
be demonstrated with CTR, opt-out, or engagement data before proposing a model rebuild.

---

## ✅ COMPLIANT Example

### Problem Statement

> We observe that 67% of email offers sent through TOP in the last 12 months achieved
> CTR < 1.0%. We hypothesize that the primary root cause is destination-customer
> mismatch: customers receive offers for routes they have no demonstrated interest in.
> We will validate this hypothesis by analyzing the correlation between offer destination
> and customer historical booking destinations before committing to any ML investment.

---

### Step 1 — Evidence (What We Observe)

**Data source:** `marketing.offer_decisions_audit`, 12-month lookback, 2.4M delivery events

| Metric | Value |
|--------|-------|
| Total offers delivered | 2,400,000 |
| Offers with CTR < 1.0% | 1,608,000 (67%) |
| Average CTR, all offers | 0.74% |
| Average CTR, destination-matched offers | 3.1% |
| Average opt-out rate | 0.38% |
| Opt-out rate for lapsed segment | 0.58% |

**NPS signal:** 89 of 214 offer-related NPS verbatims cite destination irrelevance (42%).

---

### Step 2 — Hypothesis (Root Cause)

**Primary hypothesis:** Customers are assigned to broad segments (e.g., "all AAdvantage members in Northeast US") rather than segments built on demonstrated destination affinity. A customer who has booked JFK–LHR four times in two years continues to receive DFW–MIA leisure offers.

**Alternative hypotheses (to rule out if primary is validated):**
1. **Timing:** Offers sent when customers are unlikely to convert
2. **Frequency:** Email fatigue from 3+ weekly communications suppresses engagement
3. **Value:** Discount depth insufficient regardless of destination

**Priority order:** Destination mismatch → Timing → Frequency → Value

---

### Step 3 — Minimum Validation Experiment (SQL Analysis, NOT ML)

**What we build:** A SQL correlation analysis in Databricks—not an ML model, not a new API, not infrastructure.

**Goal:** Determine whether offer destination correlates with customer historical booking destination strongly enough to justify a recommendation model investment.

```sql
WITH customer_top_destinations AS (
  SELECT customer_id_hash, destination_airport,
    ROW_NUMBER() OVER (PARTITION BY customer_id_hash ORDER BY COUNT(*) DESC) AS destination_rank
  FROM booking_history
  WHERE booked_at >= DATEADD(year, -2, CURRENT_DATE())
  GROUP BY customer_id_hash, destination_airport
),
offer_destination_match AS (
  SELECT o.customer_id_hash, o.offer_id,
    CASE WHEN o.offer_destination = t.destination_airport THEN 1 ELSE 0 END AS destination_matched,
    CASE WHEN o.click_at IS NOT NULL THEN 1 ELSE 0 END AS clicked
  FROM marketing.offer_decisions_audit o
  LEFT JOIN customer_top_destinations t
    ON o.customer_id_hash = t.customer_id_hash AND t.destination_rank = 1
  WHERE o.delivered_at >= DATEADD(month, -6, CURRENT_DATE())
)
SELECT destination_matched, COUNT(*) AS offers_delivered,
  ROUND(SUM(clicked) * 100.0 / COUNT(*), 2) AS ctr_pct,
  CORR(destination_matched, clicked) AS point_biserial_correlation
FROM offer_destination_match
GROUP BY destination_matched;
```

**Expected runtime:** 20–40 minutes. Required by: Data Scientist, 1 week. Zero new infrastructure.

---

### Step 4 — Decision

If `correlation(destination_matched, clicked) > 0.4`: invest in destination recommendation model (Q2 2026).
If `< 0.4`: investigate timing or frequency hypothesis instead.

**Threshold rationale:** A correlation above 0.4 indicates a practically significant relationship yielding meaningful CTR lift. Below 0.4, a recommendation model is unlikely to recover its build cost within 2 quarters.

**Engineering gate:** Zero engineering resources committed before the analysis is complete and documented.

---

## ❌ VIOLATION Example

> "We should build an ML recommendation engine with real-time personalization.
> The system needs: a new feature store, a real-time scoring API, A/B testing
> infrastructure, a campaign management UI update, and a Databricks serving
> cluster. Estimated: 6 months, 4 engineers."

**Why this violates PRD-1.2:**

| PRD-1.2 Requirement | Violation |
|--------------------|-----------|
| State the problem before the solution | No problem statement. No CTR data cited. |
| Quantify the evidence | No data referenced. We don't know the problem exists at scale. |
| Form a falsifiable hypothesis | No hypothesis. Root cause is assumed. |
| Design a minimum validation experiment | Jumps directly to a 6-month, 4-engineer build. |
| Decision tree: validate before building | No validation step or stopping criteria. |

**Correct first step:** Run the SQL correlation analysis. 1 week, 0 new infrastructure, 1 data scientist. Then decide.
