# Marketing Personalization & Targeted Offers — Avatar Guidance

**Avatar:** `avatar-product-marketing-personalization`
**Domain:** Customer Offer Targeting & Campaign Management
**Platform:** TOP (Targeted Offer Platform)

---

## 1. Offer Decisioning Patterns

### Ranking Stack

Every offer decision flows through four ordered gates before a final offer is selected:

1. **Eligibility Filter** — Hard rules that disqualify customers from an offer entirely.
   - Loyalty tier requirement (e.g., offer restricted to AAdvantage Gold and above)
   - Route relevance (e.g., customer has never searched or booked the offer destination)
   - Offer expiry (offer end date passed)
   - Active opt-out flag (`opted_out_at IS NOT NULL`)

2. **Propensity Score** — ML model output from TOP scoring API (backed by MLflow/Databricks).
   - Score range: 0.0–1.0, representing predicted probability of conversion
   - Scores computed per customer-offer pair using the latest registered model version
   - Ties broken by recency of last booking (more recent = higher priority)

3. **Business Rules (Suppression, Fatigue, Channel Cap)** — Post-scoring filters that protect customer experience:
   - **Suppression rules:**
     - Customer is on the global opt-out list (any channel)
     - Recent purchase: no upsell offer within 7 days of a completed booking
     - Communication cap: maximum 3 emails per customer per week (rolling 7-day window)
     - Channel-specific opt-out respected (e.g., opted out of push notifications)
   - **Fatigue guard:** customers with offer engagement score below threshold are rotated to a 48-hour cool-down
   - **Deduplication:** same offer not delivered via more than one channel in the same 24-hour window

4. **Final Offer Selection** — Highest-scoring eligible, non-suppressed offer wins per channel slot.
   - Ties at the same score fall back to business-priority ordering (retention offers > acquisition offers)

### Eligibility Reference

| Rule | Field | Condition |
|------|-------|-----------|
| Loyalty tier | `loyalty_tier` | Must satisfy offer's `min_tier` requirement |
| Route relevance | `route_affinity_score` | ≥ 0.2 for destination-specific offers |
| Offer expiry | `offer_expires_at` | Must be in the future |
| Opt-out | `opted_out_at` | Must be NULL |
| Recent purchase | `last_booking_at` | Must be > 7 days ago |
| Communication cap | `emails_sent_7d` | Must be < 3 |

---

## 2. A/B Experiment Design for Campaigns

### Holdout Group Structure

- **Allocation:** Minimum 80% treatment / 20% control. For high-risk experiments, use 50/50.
- **Randomization unit:** `customer_id_hash` (not session or device) to avoid cross-contamination.
- **Holdout integrity:** Holdout group receives no offer for the full duration — do not send them a different offer.
- **Stratification:** Stratify by loyalty tier and recency band to ensure balanced arms.

### Pre-Registration Requirements

Before any experiment goes live, document in the experiment registry:

| Field | Requirement |
|-------|-------------|
| Hypothesis | Written statement: "We believe X will cause Y because Z" |
| Success metric | Single primary metric (e.g., CTR, 90-day re-engagement rate) |
| Guardrail metrics | Opt-out rate must not increase; customer fatigue score must not degrade |
| Minimum detectable effect | e.g., CTR lift from 0.8% to 1.2% (0.4pp absolute) |
| Sample size | Calculated at 80% power, α = 0.05 |
| Planned duration | Minimum 2 weeks; must cover at least one full week-cycle twice |
| Decision criteria | Go/no-go thresholds defined before launch, not after |

### Statistical Significance Standards

- **p-value threshold:** p < 0.05 (two-tailed)
- **Minimum arm size:** 10,000 customers per arm
- **Minimum run time:** 14 days (to account for day-of-week effects)
- **No peeking:** Do not evaluate results before the planned end date; use sequential testing if early stopping is needed
- **Multiple comparisons:** Apply Bonferroni correction when testing more than one variant

### Guardrail Metrics

An experiment is automatically flagged for review if any guardrail is breached, regardless of primary metric performance:

| Guardrail | Threshold | Action |
|-----------|-----------|--------|
| Opt-out rate | Increases by > 0.1pp vs. baseline | Pause experiment, investigate |
| Customer fatigue score | Decreases by > 5% in treatment | Pause experiment |
| Hard unsubscribes | Increases by > 0.05pp | Pause experiment, legal review |

---

## 3. Propensity Model Lifecycle

### Training Data

- **Booking history:** last 24 months of flight bookings (origin, destination, cabin, price paid)
- **Offer history:** all offers delivered, impressions, clicks, conversions from `marketing.offer_decisions_audit`
- **Demographic features:** loyalty tier, account age, home airport — **no protected class features** (no race, gender, national origin, religion)
- **Behavioral signals:** search history (last 90 days), app session frequency

### Feature Engineering

| Feature | Description | Decay |
|---------|-------------|-------|
| `recency_score` | Days since last booking, normalized 0–1 | Fast (weekly) |
| `frequency_score` | Bookings per 90 days | Fast (weekly) |
| `route_preference_score` | Top-3 destination affinity by booking count | Slow (monthly) |
| `loyalty_tier_encoded` | Ordinal encoding of AAdvantage tier | Slow (monthly) |
| `offer_engagement_rate` | Clicks / impressions over last 60 days | Fast (weekly) |
| `price_sensitivity_index` | Average discount booked vs. offered | Slow (monthly) |

### Retraining Cadence

- **Fast-decay features** (recency, frequency, engagement rate): weekly retraining on rolling 90-day window
- **Structural features** (route preference, price sensitivity): monthly retraining on 24-month window
- **Trigger-based retraining:** if model AUC drops below 0.75 in production monitoring → immediate retrain

### Deployment Pipeline

```
MLflow experiment run
  → model registered in MLflow Model Registry (Unity Catalog)
  → staging validation: AUC ≥ 0.80, lift top-decile ≥ 3x
  → Databricks Model Serving endpoint promoted to production
  → TOP scoring API calls endpoint for real-time scoring
  → audit log records model_version and mlflow_run_id per decision
```

- **Rollback:** previous model version kept in registry; TOP can be reverted via feature flag within 15 minutes
- **Shadow mode:** new model runs in shadow (scores computed but not served) for 48 hours before cutover

---

## 4. Customer Data Governance

### PII Handling

- **customer_id_hash:** All audit logs, training datasets, and segment exports use SHA-256 hash of `loyalty_id`. Never log raw loyalty numbers.
- **Email address:** Stored only in EMFT/Marigold (not in Unity Catalog offer tables). Resolved at delivery time via secure lookup.
- **Model features:** No feature may be derived from a protected class attribute (race, religion, national origin, sex, disability status, age for discrimination purposes).

### Opt-Out Enforcement

All targeting queries against Unity Catalog must apply the row filter:

```sql
WHERE opted_out_at IS NULL
```

This filter is enforced at the Unity Catalog table level as a row-level security policy. Queries that bypass it will be rejected by the platform.

- **Opt-out propagation SLA:** Customer opt-out recorded in preference store → Unity Catalog row filter updated within 24 hours
- **Model training exclusion:** Opted-out customers excluded from training datasets within 30 days

### Consent Tracking

Every record in the customer preference store must carry:

| Field | Description |
|-------|-------------|
| `consent_given_at` | Timestamp when customer provided consent |
| `consent_type` | `explicit` / `implicit` / `legitimate_interest` |
| `consent_source` | `preference_center` / `account_creation` / `campaign_opt_in` |
| `consent_version` | Privacy policy version in effect at consent time |

---

## 5. Channel Delivery Patterns

### Email (EMFT → Marigold)

- **Flow:** TOP selects offer and customer list → TOP calls EMFT API with offer payload → EMFT routes to Marigold for rendering and delivery
- **Cap:** Maximum 3 emails per customer per rolling 7-day window (enforced in TOP before EMFT handoff)
- **Preference center:** Customers can opt out of individual offer categories (not just "unsubscribe all"); preferences respected within 24 hours
- **Tracking:** Opens, clicks, and unsubscribes reported back from Marigold to TOP via webhook → written to `offer_decisions_audit`

### App (Cassandra API)

- **Flow:** Customer opens AA app → app calls Cassandra offer API → Cassandra calls TOP scoring API → returns ranked offer for in-app banner
- **Cap:** Maximum 1 offer banner per app session
- **Real-time:** Scoring must complete within 200ms p99; cached fallback offer served if scoring exceeds 500ms
- **Personalization:** Offer selected based on real-time session context (current search destination overrides propensity model)

### Web (aa.com Personalization API)

- **Flow:** aa.com page load → personalization API called with session token → TOP returns offer for hero/module placement
- **Cookie consent:** Web personalization only activates if customer has accepted targeting cookies (IAB TCF consent framework)
- **Session linkage:** Anonymous sessions linked to AAdvantage account via cookie after login; pre-login sessions receive generic offers

### Loyalty (Ventana)

- **Flow:** Loyalty-triggered offer (e.g., tier upgrade incentive) → TOP selects offer parameters → Ventana attaches offer to AAdvantage account
- **Display:** Offer visible in AAdvantage account portal and AA app loyalty section
- **Expiry:** Ventana offers carry explicit expiry date; expired offers purged from account display automatically

---

## 6. Campaign Attribution

### Attribution Windows

| Attribution Model | Window | Use Case |
|-------------------|--------|----------|
| Click-to-conversion | 30 days | Standard email/app campaign attribution |
| Last-touch email | 7 days | Email-specific reporting |
| View-through | 1 day | App banner impression (no click required) |
| Loyalty redemption | 90 days | Ventana offer attribution |

### Incrementality Measurement

- **Holdout required:** Every campaign must have a holdout group (minimum 20%) to measure incrementality
- **Incremental lift calculation:**
  ```
  Incremental conversion rate = Conversion rate (treatment) − Conversion rate (holdout)
  Incremental bookings = Incremental conversion rate × Treatment group size
  Incremental revenue = Incremental bookings × Average order value
  ```
- **Do not report:** Raw conversion rate in treatment without comparing to holdout — this conflates organic demand with offer-driven demand

### LTV Impact

- **Window:** 90-day revenue comparison between treatment and control cohorts
- **Metric:** Average revenue per customer in treatment − average revenue per customer in holdout
- **Reported as:** Incremental LTV uplift per treated customer

---

## 7. Retention-First Metrics Framework

### KPI Hierarchy

| Tier | Metric | Definition | Threshold |
|------|--------|------------|-----------|
| **North Star** | 90-day re-engagement rate | % of lapsed customers (no booking in 180+ days) who book within 90 days of receiving a win-back offer | ≥ 8% for roadmap gate |
| **Secondary** | Incremental LTV uplift | (Avg 90-day revenue, treatment) − (Avg 90-day revenue, holdout) | ≥ 5% vs. holdout |
| **Tertiary** | CTR | Clicks / Impressions | Leading indicator only |
| **Tertiary** | Email open rate | Opens / Delivered | Leading indicator only |
| **Tertiary** | Impression count | Raw impressions | Volume metric, not outcome |

### Hierarchy Enforcement

- **CTR and open rate are never reported as primary success metrics.** They may be used as diagnostic signals when primary metrics are unavailable (e.g., early in a campaign flight).
- **Acquisition campaigns are gated on retention performance.** If 90-day re-engagement rate is below threshold, acquisition investment does not increase.
- **Roadmap gate:** Q2 features do not launch until Q1 re-engagement target is met. Documented in `examples/PRD-3.1-roadmap.md`.

### Reporting Cadence

| Metric | Frequency | Audience |
|--------|-----------|----------|
| 90-day re-engagement | Monthly (90-day lag required) | Exec, Marketing Strategist |
| Incremental LTV uplift | Quarterly | Exec, Finance |
| CTR / open rate | Weekly (campaign flight) | Campaign Manager, CRM Analyst |
| Model AUC / drift | Weekly | Data Scientist |
| Opt-out rate | Daily (guardrail) | Campaign Manager, Legal |
