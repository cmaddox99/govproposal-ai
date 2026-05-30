# PRD-1.1 — Continuous Discovery (AAdvantage Loyalty)

**Applies to:** Feature teams building earning, redemption, elite status, and retention experiences for 180M+ AAdvantage members.

## Discovery Cadence

| Cadence | Activity | Signal Sought |
|---------|----------|--------------|
| Weekly | Cohort earning/redemption analytics | Drop-off in earning = friction. Drop-off in redemption = catalog mismatch. |
| Monthly | Member NPS + verbatim review | Elite member churn signals surface here first |
| Per feature | 5-user prototype test | Validate redemption flow before build |
| Per quarter | Competitive loyalty program scan | Point valuation drift vs competitors |

## Key Discovery Questions

1. **Earning:** Where do members earn points but fail to redeem? That gap is retention risk.
2. **Redemption:** What redemption categories have lowest usage despite high availability? (catalog mismatch)
3. **Elite:** What is the drop-off rate at each tier threshold? (too hard vs too easy)
4. **Retention:** Which event in the 6 months before churn is the clearest leading indicator?

## AAdvantage-Specific Research Constraints

- Member PII in research outputs must comply with **ENG-6.4** (GDPR Article 6) — no EU member data in unencrypted analytics exports
- Research cohorts for elite members (EXP, PLT, GLD) must be segmented separately — their behavior is not representative of the general member population
- Points ledger data requires **BUS-4.3** retention compliance review before use in experiments

## Architecture Note: BFF-Heavy Discovery

This avatar has **no primary iOS or Android source repo** in the workspace. Discovery signals come from BFF API instrumentation:

- **`mobile-aadvantage-bff`** — primary telemetry source for earning/redemption flows; GraphQL query metrics reveal member drop-off patterns
- **`aa-ct-fly-mobile-loyalty-bff`** — enrollment funnel instrumentation via CHUB integration
- **`Mobile-Loyalty-Events-Qualifier`** — Kafka consumer metrics (PnrFeedReceiver, TailoredOffersReceiver) reveal real-time earning event volume

When running discovery analytics, instrument BFF endpoints rather than client-side SDKs. Log member cohort identifiers (hashed) at the BFF layer for privacy compliance with ENG-6.4.

> Full discovery framework in `PRD-1.1-discovery-detail.md`.
