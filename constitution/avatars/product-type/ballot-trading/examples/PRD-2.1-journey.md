---
avatar: avatar-product-ballot-trading
law: PRD-2.1
title: "User Journey Mapping"
---

# PRD-2.1 — User Journey Mapping: Ballot Trading Application

## What This Law Requires

Map the complete journey from pilot trade intent through CBA eligibility validation to award or batch queuing — for both real-time and batch paths.

## Compliant Example

**Journey: Line Pilot — Real-Time Trip Trade**

| Step | Action | System | CBA Gate | Success State |
|---|---|---|---|---|
| 1 | Pilot logs into DOTC Portal | DOTC Portal | — | Authenticated session |
| 2 | Views available pairings for trade | DOTC/RAS Cache | — | Pairing list rendered |
| 3 | Selects target pairing | DOTC Portal | — | Pairing selected |
| 4 | Submits trade request | PTTS/BTS (Apigee) | — | Request accepted |
| 5 | CBA eligibility check | CCA Rules Engine | Duty-time, seniority, rest minimums, OT limits | PASS or FAIL with reason code |
| 6a | **PASS:** Trade awarded | CCA → PTTS/BTS | — | Audit record written; pilot notified |
| 6b | **FAIL:** Reason code returned | CCA → DOTC Portal | — | Ineligibility reason displayed; escalation option offered |

**Journey: Reserve Pilot — Reserve Availability Check**

```
1. Pilot opens DOTC Portal → reserve status tab
2. System queries dotc_ras_cache (Redis) → upstream crew system
3. Reserve window displayed: start/end, contact obligation
4. Pilot views upcoming trade windows within reserve constraints
5. If reserve cleared: trade submission path (same as Line Pilot above)
```

**Journey: Batch Ballot Period Award**

```
1. Ballot period opens (trade window configured in pilottts_admin)
2. Pilots submit ballot preferences over N-day window
3. pilottts_batchrungenerator schedules batch run
4. ptts-batch-aks executes bulk matching:
   - Seniority-ordered evaluation
   - CCA eligibility check per candidate trade
   - OTL (overtime limit) check via pilottts_otlimitservice
5. Awards written; pilots notified
6. ptts_purge_adf executes post-processing / archival
```

## Violation Example

```
❌ VIOLATION: Journey map covers only real-time happy path
   "We mapped: select pairing → submit → awarded"

   Missing: batch ballot award path
   Missing: reserve pilot reserve-window constraint
   Missing: ineligibility escalation to crew scheduler
   Missing: CBA dispute path (audit retrieval)

   Result: batch and reserve pilots have no designed journey;
   scheduler escalation path built ad hoc.
```

## Edge Cases & Warnings

- **Real-time and batch are separate journeys with different SLAs** — real-time: <60s award; batch: multi-hour window. Design both explicitly.
- **CBA eligibility failure is a journey state, not an error** — the "FAIL with reason code" path is a first-class product outcome, not an edge case.
- **Codeshare and multi-segment pairings** add eligibility complexity — map these as variant journeys, not footnotes.
