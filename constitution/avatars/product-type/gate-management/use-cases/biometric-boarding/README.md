# Use Case: Touchless Biometric Boarding

**Avatar:** gate-management
**Laws:** PRD-2.1, ENG-6.7, BUS-2.2, BUS-2.4
**Sub-domain:** Biometrics — `TouchlessIdentitySolution`, `gm-web-biometrics-boarding-api`, `ct-bioentexit-biometrics-apigee`
**Regulation:** TSA 49 CFR Part 1542, CBP Biometric Exit mandate, GDPR/CCPA
**Status:** Discovery — baselines for false non-match rate, opt-out path usability, and boarding throughput required

---

## Overview

Passenger presents face at gate podium → CBP TIS facial match → APPROVE/DENY/OPT-OUT in ≤3,000ms p95. Gate agent monitors; handles non-matches and opt-outs. Primary failure modes: false non-match (line backup), opt-out path obscured (CBP violation), biometric PII leaking into operational logs.

## Happy Path — Enrolled Passenger

```
1. Camera captures face frame at gate podium
2. gm-web-biometrics-boarding-api → ct-bioentexit-biometrics-apigee → CBP TIS match
3. TIS returns MATCH above threshold
4. API verifies PNR active + flight open for boarding → returns APPROVE
5. Gate podium shows green APPROVED; DCS boarding record updated
6. Audit: { pnr_token, gate_id, agent_id, match_result: APPROVE, match_event_id, timestamp }
   — no raw template, no match score
```

## Exception Paths

| Scenario | System Behaviour | Audit Requirement |
|----------|-----------------|-------------------|
| Non-match (enrolled, correct threshold) | DENY + typed reason code | pnr_token, gate_id, agent_id, reason_code, timestamp |
| Passenger opts out | OPT-OUT path, manual scan | match_result: OPT_OUT (never DENY) |
| TIS timeout >3s | SERVICE_UNAVAILABLE; fallback to manual scan | timeout event + fallback_scan flag |
| Boarding not open | BOARDING_NOT_OPEN; passenger waits | attempt logged with status |

## Non-Negotiables

- **Opt-out always visible** — reachable without agent involvement; never buried
- **Match threshold operator-configurable** — changes require supervisor auth + CBP notification
- **Every DENY has a typed reason code** — zero generic "FAILED" responses
- **Biometric PII never in operational logs** — pnr_token only; no templates, no match scores
- **Retention:** raw biometric deleted ≤12h post-departure (CBP mandate); audit events 7yr (CBP/TSA)

## Acceptance Criteria

- Boarding throughput via biometric path ≥22 pax/min at pilot gate (Sprint 0 baseline)
- False non-match rate ≤1.5% across enrolled passengers at pilot gate
- Opt-out reachable in ≤2 taps without agent involvement
- Zero generic FAILED responses — 100% typed reason codes on DENY
- 100% of boarding events emit full audit record; zero log entries with raw biometric template or match score
- Biometric deletion job confirmed running: purged ≤12h post-departure
