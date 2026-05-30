---
avatar: avatar-product-marketing-personalization
law_id: PRD-1.1
law_title: "Continuous Discovery"
file_type: example
---

# PRD-1.1 Continuous Discovery — Marketing Personalization

## Context

TOP (Targeted Offer Platform) powers all personalized offers delivered to AA customers
across email (EMFT/Marigold), app (Cassandra), web, and loyalty (Ventana) channels.
The discovery work below was conducted to understand why offer relevance is declining
and what the highest-leverage improvements would be.

---

## Research Approach

### Weekly Customer Interviews (8 sessions)

| Theme | Frequency | Representative Quote |
|-------|-----------|----------------------|
| No real-time visibility during campaign flight | 7/8 | "I find out the CTR is bad after the campaign is over" |
| Audience data stale at delivery | 6/8 | "Someone who booked yesterday is still in my 'lapsed' segment" |
| A/B test setup takes 3 weeks minimum | 5/8 | "By the time the test is ready, the sale is over" |
| Destination-customer mismatch | 5/8 | "We send Miami deals to customers who only fly to London" |

### Historical CTR Analysis (12-month, 2.4M delivery events)

| Offer Type | Audience | CTR | Opt-Out Rate |
|------------|----------|-----|--------------|
| Domestic leisure (generic) | All AAdvantage members | 0.6% | 0.41% |
| Domestic leisure (generic) | Last booking > 180 days | 0.4% | 0.58% |
| Transatlantic (destination-matched) | Historical intl bookers | 3.1% | 0.12% |
| Upgrade upsell | Elite tiers only | 4.8% | 0.08% |

**Headline finding:** 67% of all email offers achieved CTR < 1.0%. Destination-matched offers outperform generic by 5.2x CTR (3.1% vs. 0.6%).

### NPS Verbatim Review (214 offer-related verbatims)

| Theme | % of offer verbatims |
|-------|---------------------|
| "Offers not relevant to where I want to go" | 42% |
| "Too many emails" | 30% |
| "Hard to redeem / confusing terms" | 18% |

---

## BFF Module Signal Sources

| Module | Signal | Location |
|--------|--------|----------|
| `MMXOffersController` (mobile-offers-bff) | Offer request latency, cache hit rate | Spring Boot actuator metrics |
| `OffersConnector` (mobile-offers-bff) | Upstream DCF response time, fallback rate | `OffersFallbackService` logs |
| `AirshipController` (aa-ct-mobile-airship) | Push notification delivery status, CPS preference check | Airship webhook response |
| `KafkaConfig` (aa-ct-mobile-airship) | PNR feed lag, ACS event processing backlog | Kafka consumer lag metrics |
| `DestinationsController` (ai-inspiration-service) | AI destination recommendation latency, AiFoundry model version | `AiServiceConnector` trace |

**Discovery signal:** `OffersFallbackService` invocation rate > 2% is a leading indicator of
upstream DCF instability — surfaces before customer-visible CTR degradation.

---

## How Findings Drive Roadmap Decisions

**Evidence threshold:** A roadmap investment requires at least one quantitative data point AND one qualitative signal supporting the same problem.

**Q1 2026 prioritization:** Win-back campaign—lapsed segment CTR 0.4% (worst performer); 34% of send volume but only 8% of conversions; 6/8 campaign managers cite stale audience data as top pain point.

**Q2 2026 prioritization:** Offer ranking model v2—destination-matched offers are 5.2x higher CTR; both Delta and United use ML ranking; 89 NPS verbatims cite destination irrelevance.

**Deprioritized items require documented rationale:** Real-time web personalization deprioritized Q1 due to BUS-4.3 consent management dependency; push notification offers deprioritized Q2 because app CTR baseline not yet established.

---

## ✅ COMPLIANT Pattern

> "We interviewed 8 campaign managers, analyzed 12 months of CTR data by segment,
> benchmarked Delta and United, and reviewed 214 NPS verbatims. We found that 67%
> of offers achieve <1% CTR, with destination mismatch as the primary cause (5.2x
> CTR gap between matched and unmatched offers). This evidence drives Q2 investment
> in offer ranking model v2."

## ❌ VIOLATION Pattern

> "Let's improve offer personalization. We should build an ML recommendation engine."

**Why this violates PRD-1.1:**
- No research conducted before proposing a solution
- No quantitative data cited (no CTR analysis, no segment breakdown)
- No qualitative signal (no interviews, no NPS review)
- Solution proposed before problem is validated
- No competitive context and no ongoing discovery cadence established
