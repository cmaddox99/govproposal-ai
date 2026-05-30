# Use Case: Connect Me Flight Event Notification

**Avatar:** gate-management
**Laws:** PRD-2.1, ENG-6.7, BUS-2.4
**Sub-domain:** Connect Me — `cme-bot-core`, `cme-flc-service`, `cme-flightevent-consumer`, `cme-workflow-manager`
**Regulation:** FAR Part 139 (ops logging), load control regulatory traceability
**Status:** Discovery — alert latency baseline, unread rate, and FLC load plan version gap require measurement

---

## Overview

Flight ops event fires → right person receives actionable alert in Microsoft Teams before the decision window closes. Gate agents, ramp crews, and FLCs work from a single Teams-based action queue. No polling; push only. Primary failure modes: alert arrives after decision window, unread alert (poll workaround still active), stale FLC load data, workflow task not logged.

## Happy Path — Gate Change Alert (IROP)

```
1. Ops Controller fires gate-change in AOC (C14 → C22)
2. AOC publishes to Azure Service Bus: flight-ops-events
3. cme-flightevent-consumer receives event (target: ≤2,000ms from publish)
4. cme-bot-core sends Teams message to gate agent:
   "⚠️ GATE CHANGE — AA 1234 | C14 → C22 | Departs 14:35 | Please confirm"
5. Agent taps CONFIRM on task card
6. Audit: { event_type, flight_id, gate_id, recipient_id, delivered_at, actioned_at,
   action: CONFIRMED, delivery_latency_ms, schema_version }
```

**Latency target:** AOC publish → Teams device delivery: ≤30,000ms p95

## Happy Path — FLC Load Plan Sign-Off

```
1. Load plan updated → published to Azure Service Bus
2. cme-flc-service retrieves plan: { version: "v3", timestamp, total_pax, cargo_kg }
3. cme-bot-core sends task card to FLC:
   "Load Plan Ready — AA 1234 | v3 | Updated 14:12 | [APPROVE] [REQUEST REVISION]"
   — version and timestamp always visible on card
4. FLC taps APPROVE
5. Audit: { flight_id, load_plan_version: v3, flc_id, approved_at }
```

## Exception Paths

| Scenario | System Behaviour | Audit Requirement |
|----------|-----------------|-------------------|
| Teams delivery failure >30s | Retry ×3 exponential backoff; ops controller notified | delivery failure + retry_count + fallback_triggered |
| Agent no-confirm after 5min | Escalation reminder + ops controller notified | escalation event + unconfirmed_duration |
| Newer load plan version published before FLC acts | Old task card invalidated; new card sent | stale task invalidated + version_superseded |
| AOC event malformed (missing flight_id) | Consumer logs parse error; event → DLQ | parse error + raw event reference |

## Non-Negotiables

- **All operational alerts are push** — agents/FLCs must never poll for status
- **FLC task cards always show load plan version and timestamp** — FLC confirms currency without opening load system
- **Workflow completions logged with actor and timestamp** — confirm/approve/reject all require actor_id + task_version + ISO 8601 timestamp

## Acceptance Criteria

- Gate change alert delivered to correct agent within 30,000ms of AOC publish (p95)
- FLC load plan card shows version and timestamp on 100% of load plan tasks
- Unconfirmed gate change: escalation triggered after 5 minutes
- Stale task card superseded automatically when newer version published
- `connectme.alert.delivery_latency_ms` metric wired to Azure App Insights per alert type (Sprint 1)
- Unread alert rate metric: alert fires if >5% unread within 5 minutes
