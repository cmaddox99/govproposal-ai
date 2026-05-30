---
avatar: avatar-product-ballot-trading
law: PRD-1.1
title: "Continuous Discovery"
---

# PRD-1.1 — Continuous Discovery: Ballot Trading Application

## What This Law Requires

Continuously surface pilot pain points in trade submission, CBA rule interpretation, and ballot period experience — before and during every feature iteration.

## Compliant Example

**Discovery Sprint: Ballot Period Observation**

```
Research Questions (validated before ballot period opens):
  1. Where do pilots abandon trade requests — eligibility check or submission form?
  2. Which ineligibility reason codes generate the most scheduler calls?
  3. How do pilots compare ballot trading UX to industry peers (e.g., United FLICA, FOS)?

Methods:
  - Contextual interviews: 6–8 line pilots across base domiciles
  - Scheduler call-log analysis: tag calls by reason code (duty-time, seniority, pairing conflict)
  - Session replay review on DOTC Portal trade-submission flow
  - Competitor benchmark: FLICA ballot UX vs DOTC Portal — feature parity gaps

Output: Opportunity backlog ranked by ineligibility frequency × pilot frustration score

Signal metrics tracked per ballot period:
  - Ineligibility rate by reason code
  - Abandonment rate at step: availability check → eligibility → submission
  - Scheduler escalation rate post-rejection
```

**What Continuous Looks Like**
- Debrief with 2 pilots after every ballot period close
- Monthly review of top-5 ineligibility reason codes with Product + CBA team
- Discovery backlog item created for any reason code triggering >5% of rejections

## Violation Example

```
❌ VIOLATION: Feature shipped based on scheduler request alone
   "Schedulers asked for bulk trade approval — we built it"

   No pilot interviews conducted.
   No data on whether bulk approval addresses actual pilot frustration.
   Missing: what do pilots do when their trade is caught in a batch queue?
```

## Edge Cases & Warnings

- **CBA interpretation gaps are discovery signals** — when pilots misunderstand eligibility rules, that is a product gap, not a pilot error.
- **Ballot period discovery is time-boxed** — schedule interviews within the first 3 days of a ballot period; do not wait until disputes emerge.
- **Seniority bias in interviews** — junior pilots experience more ineligibility. Ensure sample includes pilots across seniority quintiles.
