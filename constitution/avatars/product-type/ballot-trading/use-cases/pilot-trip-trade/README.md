# Use Case: Pilot Real-Time Trip Trade

## Context

A line pilot at DFW domicile wants to trade a trip pairing with another pilot using the DOTC Portal and PTTS/BTS real-time trade matching system. CBA rules enforced by the CCA engine determine eligibility.

## Trigger

Pilot selects a pairing they wish to trade in the DOTC Pilot Portal and initiates a trade request.

## Happy Path

1. **Pilot authenticates** into DOTC Pilot Portal; session scoped to their base domicile (DFW).
2. **Pilot views available pairings** — `dotc_ras_pilotportal_cloud` queries `dotc_ras_cache` (Redis) for current assignments and availability windows.
3. **Pilot selects target pairing** for trade and confirms trade intent.
4. **Trade request submitted** — DOTC Portal sends request to PTTS/BTS via Apigee API Gateway (east region: `bts-rtt-service-mgw` → `bts-rtt-service`).
5. **CBA eligibility check** — `bts-rtt-service` calls CCA (`pcs_cca`) with: pilot ID, pairing ID, proposed trade date. CCA evaluates against:
   - Art. 12.3: monthly flight hours limit
   - Art. 14.1: minimum rest between pairings
   - Art. 20.2: seniority order (other pilot must accept or system finds match)
   - Art. 22.4: overtime limit check via `pilottts_otlimitservice`
6. **CCA returns PASS** — trade award written; `pcs_cca_poller` propagates schedule update to downstream systems. **BUS-7.1 audit record written** (pilot ID masked, CBA article, decision, timestamp).
7. **Pilot notified** in DOTC Portal: "Trade awarded — [pairing details]." End-to-end: <60 seconds.

## Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| **CBA ineligibility (duty-time)** | CCA returns `REJECTED` + reason code "DUTY_TIME_LIMIT_EXCEEDED (Art. 12.3)". DOTC Portal displays reason with CBA article reference. Scheduler escalation option offered. Audit record written for rejection. |
| **Seniority conflict** | No eligible swap partner found in seniority order. System returns `QUEUED_FOR_BATCH` — trade placed in next ballot period. Pilot notified with expected batch window. |
| **System timeout (Apigee → BTS)** | Apigee returns 504 after 30s. DOTC Portal shows "Request could not be processed — please retry." No audit record written for incomplete request (transaction not committed). |

## Laws Applied

| Law | Role in This Use Case |
|---|---|
| PRD-2.1 | This use case IS the primary journey map for the Line Pilot persona. All steps above derived from PRD-2.1 mapping. |
| BUS-7.1 | Audit record written at Step 6 (award) and on rejection at Step 5 failure. Audit records support CBA dispute resolution. |
| BUS-2.2 | Every CBA rule evaluated in Step 5 maps to a control table entry (CTL-001 through CTL-004). Bidirectional traceability to CBA articles enforced. |
| BUS-3.1 | Pilot ID masked in audit record and all log output. Trade data classified as Confidential; encrypted at rest in CCA DB and PTTS audit store. |

## Success Metric

Trade awarded within 60 seconds with a BUS-7.1-compliant audit record and zero CBA compliance incidents, measured over a 30-day ballot period observation window.
