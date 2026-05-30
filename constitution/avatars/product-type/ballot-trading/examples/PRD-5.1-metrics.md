---
avatar: avatar-product-ballot-trading
law: PRD-5.1
title: "MVP & Experimentation"
---

# PRD-5.1 — MVP & Experimentation: Ballot Trading Application

## What This Law Requires

Validate the smallest usable trade slice with real pilot traffic before building batch optimization or conversational layers. Define clear exit criteria before starting any experiment.

## Compliant Example

**MVP Slice: Real-Time Trade with Transparent Reason Codes**

```
Hypothesis:
  Transparent CBA ineligibility reason codes reduce scheduler escalation calls by 20%.

MVP scope (what IS included):
  - Real-time trade submission for eligible standard domestic pairings
  - CBA eligibility check result with specific reason code (e.g., "duty-time limit exceeded — Article 12.3")
  - CBA article reference displayed inline on rejection screen
  - Audit record per decision

MVP scope (what is NOT included):
  - Batch ballot period matching (Phase 2)
  - Conversational eligibility explanation via AI (Phase 3)
  - Multi-segment / codeshare pairing support (Phase 2)

Pilot cohort:
  - 10% of real-time trade traffic at 2 base domiciles (DFW, CLT)
  - Minimum 30-day observation window (covers one ballot period open/close)

Exit criteria (proceed to Phase 2):
  ✅ Self-serve trade success rate ≥ 85%
  ✅ Scheduler escalation calls for eligible rejections ↓ ≥ 20%
  ✅ Zero CBA compliance incidents (disputed awards)
  ✅ Audit record completeness ≥ 99.9% (BUS-7.1)

Exit criteria (do NOT proceed — revisit):
  ❌ Pilot abandonment rate at eligibility step > 30%
  ❌ Any award made without audit record
```

## Violation Example

```
❌ VIOLATION: Building full batch engine before validating real-time slice
   "Let's build batch matching first — it handles more volume"

   No validation that pilots understand real-time trade eligibility.
   No data on ineligibility reason code clarity.
   Batch engine built on unvalidated eligibility UX assumptions.
   If pilots don't understand rejections, batch awards won't help them.
```

## Success Metrics (Tier 1–3)

**Tier 1 — Customer Outcome**
- Self-serve trade success rate (real-time): ≥85%
- Time-to-award confirmation: <60 seconds (real-time path)
- Batch award cycle completion rate: ≥99%
- Pilot-reported clarity of ineligibility reason: ≥4.0/5.0 (post-MVP survey)

**Tier 2 — Operational**
- BTS RTT service p95 latency: <2,000ms
- CCA eligibility check p95: <500ms
- Batch run completion within SLA window: ≥99%
- Scheduler escalation rate (eligible rejections): ↓20% vs baseline

**Tier 3 — Risk & Compliance**
- Audit record completeness: ≥99.9% (BUS-7.1)
- CBA compliance incidents (disputed awards): 0
- Data classification violations (BUS-3.1): 0
- Failed audit trail retrievals during CBA disputes: 0
