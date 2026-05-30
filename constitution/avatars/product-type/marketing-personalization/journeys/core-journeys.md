# Marketing Personalization — Core Journeys

**Avatar:** `avatar-product-marketing-personalization`
**Domain:** Customer Offer Targeting & Campaign Management

---

## Journey 1: Offer Targeting & Personalization

**Trigger:** Scheduled campaign run or real-time channel request (app open, page load).

**Steps:**
1. Customer eligibility filter applied (loyalty tier, opt-out flag, offer expiry, recent purchase suppression) — `CPSRulesEngineResponse` checked via aa-ct-mobile-airship
2. Propensity model scores customer-offer pairs via TOP scoring API; `MMXOffersServiceImpl` (mobile-offers-bff) constructs ranked `MMXResponse`
3. Business rules applied: suppression list, fatigue guard, channel cap (max 3 emails/7-day window), deduplication
4. Highest-scoring eligible offer selected per channel slot; `MMXResponseBuilder` assembles `MMXOffersResponse` with `PassengerOffer` payloads
5. Offer payload dispatched to channel (EMFT → Marigold for email; `AirshipController` in aa-ct-mobile-airship for push; Cassandra for app; personalization API for web; Ventana for loyalty)
6. Delivery confirmation recorded; impression logged to `marketing.offer_decisions_audit`

**Success criteria:**
- App scoring response within 200ms p99; `OffersFallbackService` (mobile-offers-bff) served if > 500ms
- Opt-out filter applied to 100% of targeting queries (Unity Catalog row-level security + `CPSRulesEngineResponse` check)
- Every offer decision logged with `model_version` and `mlflow_run_id`

**Exception flows:**
- Scoring service timeout → `OffersFallbackHandler` serves cached fallback offer; alert on-call
- CHUB erasure event received → `KafkaConfig` consumer (aa-ct-mobile-airship) propagates suppression via `ChubErasureFlow`

---

## Journey 2: Campaign Creation & A/B Testing

**Trigger:** Marketing Strategist or Campaign Manager initiates a new campaign.

**Steps:**
1. Campaign intent defined: retention or acquisition; target persona and lifecycle stage identified
2. Experiment pre-registered: hypothesis, primary metric (90-day re-engagement rate or incremental LTV), guardrail metrics (opt-out rate, fatigue score, hard unsubscribes), sample size, planned duration
3. Holdout group structured: minimum 80/20 treatment/control; stratified by loyalty tier and recency band
4. Campaign approved against retention gate: if re-engagement rate < 8%, acquisition campaigns blocked
5. Campaign launched; daily guardrail monitoring active
6. Campaign ends per planned date (no early stopping without sequential testing approval)
7. Results computed: incremental conversion = treatment rate − holdout rate; incremental LTV calculated

**Success criteria:**
- Minimum 14-day run; minimum 10,000 customers per arm
- No peeking before planned end date
- Gate outcome documented in decision log (PRD-1.5 compliance)

---

## Journey 3: Customer Segment Management

**Trigger:** Weekly segment refresh or analyst-initiated segment definition update.

**Steps:**
1. Segment definition authored: eligibility predicates against Unity Catalog customer tables
2. Opt-out filter mandatory: `WHERE opted_out_at IS NULL` enforced at row-security level
3. Segment computed on Unity Catalog Delta tables; customer count validated
4. Segment published to TOP for targeting use; version and timestamp recorded
5. Segment used in eligibility filter for offer ranking

**Data governance requirements:**
- No protected class attributes in segment predicates
- `customer_id_hash` (SHA-256 of loyalty_id) used in all segment exports — never raw loyalty numbers
- Email addresses not stored in Unity Catalog; resolved at delivery time via EMFT

---

## Journey 4: Offer Attribution & Performance Reporting

**Trigger:** Campaign flight ends; 90-day attribution window closes.

**Steps:**
1. Clicks, conversions, and booking events joined to offer delivery records in `offer_decisions_audit`
2. Attribution window applied per model (click-to-conversion: 30 days; view-through: 1 day; loyalty redemption: 90 days)
3. Holdout comparison computed: treatment conversion rate vs. no-offer holdout conversion rate
4. Incrementality calculated: incremental lift in conversion rate and incremental revenue
5. Report generated: primary metric (re-engagement rate or LTV uplift), secondary metrics, leading indicators (CTR, open rate) clearly labelled as diagnostic
6. Results stored; roadmap gate assessment performed if applicable

**Reporting hierarchy (PRD-6.2):**
- North star first: 90-day re-engagement rate
- Secondary: incremental LTV uplift vs. holdout
- Tertiary (diagnostic only): CTR, open rate, impression count — never reported as primary outcomes
