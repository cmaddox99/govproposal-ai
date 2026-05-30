# Marketing Personalization & Targeted Offers — Avatar Guidance

**Avatar:** `avatar-product-marketing-personalization`
**Domain:** Customer Offer Targeting & Campaign Management
**Platform:** TOP (Targeted Offer Platform)

## Purpose

This avatar guides product development for the TOP (Targeted Offer Platform) — selecting, ranking, and delivering personalized offers across email (EMFT/Marigold), app (Cassandra), web (aa.com), and loyalty (Ventana) channels.

## Core Offer Decisioning Stack

Every offer decision passes four ordered gates before delivery:

1. **Eligibility Filter** — Hard disqualification: loyalty tier, route relevance, opt-out flag, offer expiry.
2. **Propensity Score** — ML model (TOP scoring API, 0.0–1.0); ties broken by recency of last booking.
3. **Business Rules** — Suppression, fatigue guard, channel cap (max 3 emails/7-day window), deduplication.
4. **Final Selection** — Highest-scoring eligible, non-suppressed offer wins per channel slot.

## Retention-First Principles

- **North star metric:** 90-day re-engagement rate — not CTR, not open rate, not impressions.
- **Acquisition gate:** Acquisition campaigns are blocked until retention 90-day re-engagement rate ≥ 8%.
- **Holdout required:** Every campaign must have a holdout group (minimum 20%) to measure incremental lift.
- **Incremental LTV uplift** vs. holdout is the secondary success metric.

## Session Setup Scaffold

When starting a new campaign or feature:

1. Define retention or acquisition intent (persona, lifecycle stage).
2. Specify eligibility rules and propensity model version.
3. Document holdout structure before any sends.
4. Pre-register hypothesis, primary metric, and guardrail metrics in experiment registry.
5. Confirm PII handling: `customer_id_hash` in all audit logs; email resolved at delivery only via EMFT.
6. Confirm opt-out filter (`opted_out_at IS NULL`) applied at Unity Catalog row-security level.

## Compliance Reminders

- Opt-out propagation SLA: 24 hours from preference store to Unity Catalog row filter.
- Model features: No protected class attributes (race, gender, national origin, religion, disability).
- Consent fields required per record: `consent_given_at`, `consent_type`, `consent_source`, `consent_version`.
- Audit trail: Every offer decision logged with `model_version` and `mlflow_run_id`.

## Reference Files

- `guidance-detail.md` — Full decisioning patterns, A/B design, model lifecycle, channel delivery, attribution windows.
- `examples/PRD-6.2-retention.md` — Retention-over-acquisition compliant and violation examples.
- `examples/PRD-5.1-metrics.md` — TOP platform KPI definitions.
- `use-cases/` — Campaign scenario walkthroughs.
