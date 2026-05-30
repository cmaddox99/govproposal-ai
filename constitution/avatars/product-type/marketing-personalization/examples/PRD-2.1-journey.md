---
avatar: avatar-product-marketing-personalization
law_id: PRD-2.1
law_title: "User Journey Mapping"
file_type: example
---

# PRD-2.1 User Journey Mapping — Marketing Personalization

## Context

This map traces the lifecycle of a personalized offer from trigger through delivery,
customer interaction, conversion, and attribution. Email is the primary channel; app and
web divergences are noted.

**Platforms:** TOP, EMFT, Marigold, Cassandra, Ventana, Unity Catalog, MLflow/Databricks

---

## Campaign Manager Journey — Offer Delivery Flow

| Step | Actor | Module | Action | Compliance Gate |
|------|-------|--------|--------|----------------|
| 1. Segment | Campaign Mgr | Unity Catalog Delta tables | Define audience from customer behavior | CCPA opt-out suppression applied |
| 2. Score | Data Scientist | Propensity Model Service (TOP) | Run propensity scores per offer | Model version logged for audit |
| 3. Rank | TOP Platform | `MMXOffersController` → `MMXOffersServiceImpl` | Rank offers per customer-offer pair via mobile-offers-bff | Fatigue cap applied (max N offers/week) |
| 4. Deliver | System | EMFT/Marigold or `AirshipController` (aa-ct-mobile-airship) | Send email or serve in-app push offer | CAN-SPAM / GDPR consent verified via CPS |
| 5. Track | Analytics | Unity Catalog event tables | Capture opens, clicks, conversions | Attribution window defined |
| 6. Attribute | Analytics | MLflow / Databricks | Measure incremental lift vs. control | A/B test assignment logged |

## Customer Journey (Traveler)

| Step | Experience | Channel |
|------|-----------|---------|
| Receive offer | Email, push notification, or in-app banner | EMFT, `AirshipController`, Cassandra |
| Engage or ignore | Click, open, scroll past | Attribution tracked for all outcomes |
| Convert | Purchase, book, enroll | Revenue attributed to offer |
| Re-engage (lapsed) | Win-back campaign triggered | Loyalty Ventana channel |

## Exception Flows

| Scenario | Handling |
|----------|----------|
| Customer opts out | Suppress from all channels within CAN-SPAM 10-business-day window; `KafkaConfig` propagates CHUB erasure event |
| Propensity model stale | `OffersFallbackService` serves cached fallback; suppress offers using scores >24h old |
| A/B test assignment | Persist in Delta tables for attribution audit; `decision_reason` field in offer_decisions_audit |

---

## ✅ COMPLIANT Example — End-to-End Offer Journey

| Stage | System | Customer State | Key Pain Point |
|-------|--------|----------------|----------------|
| **1. Trigger** | TOP scheduler / CDP event bus | N/A | CDP event latency (2–6 hr): customer who booked today may still receive an offer |
| **2. Eligibility check** | TOP rules engine | N/A | Opt-out filter enforced at Unity Catalog; bypassing it is rejected at storage layer |
| **3. Offer ranking** | TOP scoring API → Databricks Model Serving | N/A | Model version + MLflow run ID written to audit log here (BUS-7.1 compliance) |
| **4. Suppression check** | TOP suppression service | N/A | CRM and Marigold suppression sync lag: customer who opted out 1 hr ago may still receive send |
| **5. Channel selection** | TOP routing logic | N/A | Cross-channel dedup is a Q4 2026 gap: same offer can arrive via email, app, and web simultaneously |
| **6. Delivery** | EMFT/Marigold (email); Cassandra (app); Ventana (loyalty) | Neutral | Marigold delivery webhook can lag up to 4 hr; `delivered_at` in audit log may lag actual delivery |
| **7. Impression** | Customer touchpoint | Relevant / Neutral / Fatigued | No real-time signal for relevance vs. fatigue; opt-out rate is the lagging proxy |
| **8. Click / Ignore** | Tracking → `offer_decisions_audit.click_at` | Intent / Neutral | 3–7% tracking gap in click-to-session handoff between Marigold and aa.com analytics |
| **9. Conversion** | aa.com / AA app | Satisfied / Frustrated | Offer discount does not auto-apply; customers must find and enter a promo code |
| **10. Attribution** | TOP attribution service | N/A | No multi-touch attribution; if customer clicked email then booked via app, only last-touch gets credit |
| **11. LTV impact** | Analytics / Finance | Positive / Neutral | 90-day lag before full measurement available |

### Key Rules Applied at Eligibility (Stage 2)

| Rule | Disqualification Condition |
|------|---------------------------|
| Opt-out | `opted_out_at IS NOT NULL` → skip entirely |
| Loyalty tier | Does not meet offer's `min_tier` |
| Recent purchase | `last_booking_at` < 7 days ago |
| Route relevance | `route_affinity_score` < 0.2 for destination-specific offers |

### Attribution Windows

| Channel | Window | Model |
|---------|--------|-------|
| Email | 30 days click-to-conversion | Last-touch |
| App | 30 days | Last-touch |
| Loyalty (Ventana) | 90 days | Any-touch |

---

## ❌ VIOLATION Example

### Missing Audit Trail at Ranking Stage

> An offer is scored and delivered but TOP does not record `model_version`,
> `mlflow_run_id`, or `score` in the audit log at Stage 3. Only `offer_id` and
> `customer_id_hash` are written. When a compliance investigation asks "why was
> this offer shown to this customer?", the answer is unrecoverable.

**Why this violates PRD-2.1 and BUS-7.1:**
- The "why" element of the audit trail (model, score, reasoning) is absent
- If the model produces a biased recommendation, no version can be identified or reproduced
- GDPR right-to-explanation (Article 22) cannot be fulfilled without `decision_reason`

**Remediation:** At Stage 3, TOP must write `model_version`, `mlflow_run_id`, `score`, and `decision_reason` to `offer_decisions_audit` before any delivery proceeds. See `BUS-7.1-audit-trail.md` for the full schema.
