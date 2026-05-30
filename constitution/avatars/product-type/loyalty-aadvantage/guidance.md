# AAdvantage Loyalty — Guidance

> **Program scale:** 180M+ members worldwide. Every product decision affects earning, redemption, elite status, or retention for a material segment of AA's customer base.

## Core Laws

| Law | Application |
|-----|-------------|
| **PRD-1.1** Continuous Discovery | Survey member redemption desires; analyze earning by cohort; track elite retention drivers |
| **PRD-2.1** User Journey | Map enrollment → earning → redemption → retention. Document each touchpoint. |
| **PRD-3.1** Roadmap | Rank features by member lifetime value impact + retention signal |
| **PRD-4.1** MVP | Test new redemption options with small cohort before full rollout |
| **PRD-5.1** Metrics | Earning rate, redemption rate, churn rate, member lifetime value, NPS |
| **ENG-6.4** PII/GDPR | EU members: Article 6(1)(b) contract basis; right to erasure limited by financial retention obligations |
| **BUS-4.3** Data Retention | Points ledger: lifetime + 7 years. Transaction history: 7 years. Inactive member PII: review at 3 years. |
| **ENG-11.1** SDD | PROPOSAL.md required before any new loyalty feature implementation |

## AAdvantage BFF Intelligence (Mobile)

**Loyalty BFF repos:** `aa-ct-fly-mobile-loyalty-bff` (5.3/10) and `mobile-aadvantage-bff` (5.6/10). Both in Yellow tier. Key issue: AAdvantage data aggregated from Member Database + Points Ledger + Partner Integration APIs — coordination bugs surface at seam boundaries.

> Full discovery patterns in `guidance-detail.md`. Member personas in `examples/personas-detail.md`.
