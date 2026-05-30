# Use Case: Retention & Engagement (AAdvantage Loyalty)

**Avatar:** avatar-loyalty-aadvantage  
**Laws:** PRD-1.1 (Continuous Discovery), PRD-3.1 (Roadmap), PRD-5.1 (Metrics), BUS-2.1 (Regulatory Mapping)  
**Scope:** Members at churn risk — no earning or redemption activity in 60–90 days

## The Retention Problem

180M+ enrolled members. Churn is silent — members don't cancel, they just stop. The product signal is: no earning event, no redemption, no app open in 90 days.

**AA fleet context:** The loyalty BFF tier — `aa-ct-fly-mobile-loyalty-bff` (5.3/10) and `mobile-aadvantage-bff` (5.6/10) — are both Yellow. Retention campaigns that require personalized real-time member data depend on these services being reliable. Their current quality tier means feature velocity is constrained.

## Retention Funnel

```
All members (180M)
  → Active in last 12 months (~40%)
    → Earned in last 6 months (~25%)
      → Redeemed in last 12 months (~15%)
        → Renewing elite (~5%)
```

Retention work targets the 15% who've earned but not redeemed — highest recovery value.

## Proven Retention Plays

| Play | Mechanism | Metric |
|------|-----------|--------|
| Points expiry alert | Push via `mobile-aadvantage-bff` 60 days before expiry | Open rate ≥ 40%, earn activity ≥ 5% |
| Threshold bonus | Extra miles offer to close the gap to next tier | Elite upgrade rate in targeted segment |
| Partner earn reminder | "Earn miles at hotels you already book" | Partner earning activation rate |
| Win-back campaign | Email with bonus + flight offer at 90-day inactivity | Reactivation rate ≥ 3% |

## Discovery Requirements (PRD-1.1)

Before building any retention feature, answer:
1. What is the leading behavioral indicator 30 days before churn? (data from `mobile-aadvantage-bff`)
2. Which cohort has the highest LTV-weighted recovery potential?
3. Does the target BFF service have the data needed, or does it require upstream dependency?

## BFF Contract Gate

Any retention feature that modifies BFF response contracts requires a PROPOSAL.md before implementation. `mobile-aadvantage-bff` (Spring Boot 4.0.5 / Java 25) is stable but requires careful review for new paths that touch points ledger queries or GraphQL schema changes. `aa-ct-fly-mobile-loyalty-bff` handles enrollment-side data via CHUB — changes to member profile fields require CHUB contract coordination.

## Success Metrics (PRD-5.1)

- Reactivation rate: ≥ 3% of targeted churned members resume activity within 30 days  
- Earning event count: ≥ 1 qualifying event within 30 days of campaign contact  
- NPS delta: ≥ +2 points for reactivated members at 90-day survey

> Full retention playbook, A/B testing templates, and cohort analysis framework in `README-detail.md`.
