# Use Case: Carry-On Baggage Compliance

**Avatar:** gate-management
**Laws:** PRD-2.1, ENG-6.7, BUS-2.2, BUS-2.4
**Sub-domain:** Carry-On — `ct-carryonmgt-bagmatrix`, `ct-carryonmgt-apigee`, `gm-web-bagmatrix-admin`
**Regulation:** DOT 14 CFR Part 259 (baggage disclosure, denied boarding), DOT consumer protection
**Status:** Discovery — gate-check rate baseline, override rate, and policy propagation time require measurement

---

## Overview

Gate agent scans/measures carry-on → bag matrix service returns COMPLIANT/GATE-CHECK/DENIED with rule version → agent enforces decision. Station manager updates bag matrix rules from admin UI without engineering. Every decision is immutable in the audit log. Primary failure modes: rule version mismatch across gates, silent agent override, policy change latency.

## Happy Path — COMPLIANT Bag

```
1. Agent scans bag at gate podium
2. Scanner → ct-carryonmgt-apigee (OAuth 2.0 enforced) → ct-carryonmgt-bagmatrix
3. Bag matrix evaluates dimensions → returns { decision: COMPLIANT, rule_version: "v2.4.1" }
4. Agent scanner UI shows green COMPLIANT + rule version visible
5. Audit: { decision, rule_version, bag_dimensions, gate_id, agent_id, pnr_token, timestamp }
```

## Happy Path — Policy Rule Change (Station Manager)

```
1. Manager creates/updates rule in gm-web-bagmatrix-admin
2. Admin UI requires: rule_id, effective_date, change_reason, manager_id
3. New rule version published (e.g., v2.4.2) → propagates to all gates in station
4. Admin UI shows per-gate propagation status: N/M gates updated
5. All gates running v2.4.2 within 60 seconds of publish
6. Audit: { rule_version: "v2.4.2", changed_by: manager_id, change_reason, propagation_timestamp }
```

## Exception Paths

| Scenario | System Behaviour | Audit Requirement |
|----------|-----------------|-------------------|
| Agent requests override | UI requires supervisor auth code; blocked without it | override + supervisor_id + auth_code + timestamp |
| Bag matrix service timeout | DECISION_UNAVAILABLE; agent applies manual policy | service timeout + fallback flag + MANUAL_DECISION |
| Rule propagation failure (gate >60s) | Admin UI shows gate RED | propagation failure + gate_id + version mismatch |
| Manual dimension entry (no scanner) | Manual entry flagged in audit | manual_entry flag + dimensions + agent_id |

## Non-Negotiables

- **Rule version logged with every decision** — COMPLIANT, GATE-CHECK, DENIED, MANUAL all include rule_version
- **Override requires supervisor auth** — blocked at UI without auth code; no silent overrides
- **Policy propagation ≤60 seconds** — from admin submit to all station gates; status visible in admin UI
- **Admin rule changes versioned** — no in-place edits; every change creates a new version with timestamp

## Acceptance Criteria

- Every compliance decision returns rule_version in response payload and displays it to agent
- Override path: UI blocks submission without supervisor auth code — zero silent overrides via normal UI
- Policy propagation p95 ≤60s; admin UI shows per-gate propagation status; failure alert within 90s
- Bag matrix p95 latency ≤2,000ms from scan to decision
- 100% of compliance decisions emit audit record with rule_version, agent_id, pnr_token, timestamp
- 100% of override events include supervisor_id and override reason
