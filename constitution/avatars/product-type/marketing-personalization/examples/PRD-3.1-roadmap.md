---
avatar: avatar-product-marketing-personalization
law_id: PRD-3.1
law_title: "Roadmap Planning"
file_type: example
---

# PRD-3.1 Roadmap Planning — Marketing Personalization

## Principles Applied

- **Retention-first:** Win-back and re-engagement campaigns precede acquisition in every quarter
- **Metrics gates:** Each phase does not launch until the prior phase's gate metric is achieved
- **Evidence-driven:** Each quarter's focus is backed by CTR analysis, NPS verbatims, and interview findings
- **Explicit investment ratio:** 70% retention / 30% acquisition maintained across the roadmap

---

## ✅ COMPLIANT Example — 2026 Roadmap

### Retention vs. Acquisition Ratio

**Target: 70% retention / 30% acquisition.** Acquisition investment does not increase above 30% until the Q1 re-engagement gate (≥ 8%) is met. Rationale: acquiring a new customer costs 5–7x more than retaining an existing one; AA's lapsed member base (34% of AAdvantage members) is a high-value addressable pool before spending on acquisition.

---

### Q1 2026 — Retention: Win-Back Campaign for Lapsed Customers

**Focus:** Reactivate lapsed high-propensity customers (last booking > 180 days, c_lpr score > 0.7)

**What we're building:** Rule-based win-back email campaign using top historical route per customer; 20% holdout for incrementality; full opt-out and communication cap enforcement.

**Target audience:** ~87,000 customers (validated by CRM Analyst)

**Discovery evidence:**
- Lapsed segment CTR: 0.4%—worst-performing segment
- Lapsed = 34% of send volume but only 8% of conversions
- 6/8 campaign managers cite stale audience data as top pain point

**What we are NOT building in Q1:** ML ranking model, real-time personalization, push notification channel.

**Q1 Metric Gate:**

| Metric | Gate Threshold | Gate Date |
|--------|---------------|-----------|
| 90-day re-engagement rate | ≥ 8% | 2026-04-15 |
| Opt-out rate | ≤ 0.4% | During Q1 flight |
| Incremental LTV uplift vs. holdout | ≥ $50/customer | 90-day measurement |

---

### Q2 2026 — Personalization: Offer Ranking Model v2

**Dependency:** Q1 gate met

**What we're building:** Propensity model v2 with destination affinity features; A/B test 80% model v2 vs. 20% rule-based; MLflow → Databricks Model Serving → TOP scoring API.

**Discovery evidence:** Destination-matched offers are 5.2x higher CTR; correlation analysis confirms signal strength (r = 0.52 > 0.4 threshold); both Delta and United use ML destination ranking.

**Q2 Gate:** Email CTR ≥ 1.5% and model AUC ≥ 0.80 before full deployment.

---

### Q3–Q4 2026 (Summary)

| Quarter | Theme | Gate Metric |
|---------|-------|-------------|
| Q3 2026 | Channel: push notifications for high-intent mobile sessions | App offer CTR ≥ 3.0% |
| Q4 2026 | Data foundation: consent management + unified opt-out (BUS-4.3) | All BUS-4.3 requirements met |

**Retention/Acquisition ratio maintained at 70/30 throughout all four quarters.**

---

## ❌ VIOLATION Example

> "Q1: Build ML recommendation engine with real-time scoring.
> Q2: Launch all channels simultaneously (email, app, web, Ventana).
> Q3: Expand to acquisition campaigns.
> Q4: Add gamification."

**Why this violates PRD-3.1:**

| PRD-3.1 Requirement | Violation |
|--------------------|-----------|
| Retention-first | Q3 expansion to acquisition before re-engagement gate is met |
| Metrics gates | No gate defined between phases; Q2 launches regardless of Q1 outcome |
| Evidence-driven prioritization | ML engine in Q1 without validating destination hypothesis first (PRD-1.2) |
| Explicit investment ratio | No retention/acquisition ratio stated or enforced |
| MVP approach | Full ML stack and all channels before any hypothesis is validated |

**Correct first step:** Q1 must be a rule-based win-back MVP (see `PRD-5.1-mvp.md`). Validate the 8% re-engagement gate before committing Q2 ML investment.
