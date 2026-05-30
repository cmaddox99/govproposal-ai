# Use Case: Real-Time DSS Display Update

**Avatar:** gate-management
**Laws:** PRD-2.1, ENG-6.7, BUS-2.2
**Sub-domain:** DSS — `dss-displayhub-flightevent`, `dss-displayhub-gateevent`, `dss-displayhub-flightcache`, `dss-web-gids-ui`, `dss-web-fids`
**Regulation:** FAR Part 139, DOT 14 CFR Part 259 (tarmac timer)
**Status:** Discovery — staleness baseline and pipeline lag breakdown require instrumentation

---

## Overview

AOC fires a flight ops event → propagates to all display surfaces (GIDS, FIDS, BIDS, WIDS) within 5 seconds. Primary failure mode: **display staleness** — ops event fires but display hasn't updated before the agent decision window closes.

## Happy Path — Gate Change (IROP)

```
1. Ops Controller fires gate-change in AOC (C14 → C22)
2. AOC publishes to Azure Service Bus: flight-ops-events
3. dss-displayhub-gateevent consumer receives event (target: ≤2,000ms from publish)
4. Flight state cache updated: new_gate = C22
5. GIDS at C14 renders "Gate Changed → C22"; GIDS at C22 renders inbound flight
6. FIDS updates: departure board shows new gate C22
7. Audit: { flight_id, old_gate_id, new_gate_id, event_type: GATE_CHANGE,
   aoc_event_timestamp, display_updated_timestamp, staleness_ms }
```

**Total latency target:** AOC publish → GIDS updated: ≤5,000ms p95

## Happy Path — Tarmac Timer

```
1. Aircraft door closes → AOC publishes tarmac-timer-start event
2. dss-displayhub-flightevent consumer updates cache: tarmac_timer_active = true
3. GIDS renders tarmac timer in PRIMARY view — elapsed minutes since door close
4. At T+150min (domestic) / T+210min (international): threshold alert fires to Ops Controller
```

**Non-negotiable:** Tarmac timer in primary GIDS view always — never behind tab or sub-screen. DOT 14 CFR Part 259.

## Exception Paths

| Scenario | System Behaviour | Audit Requirement |
|----------|-----------------|-------------------|
| Service Bus lag >3s | Consumer lag metric alert fires | consumer lag metric + timestamp |
| DisplayHub render error | GIDS shows last-known-good + "refresh pending" | render error + display surface + timestamp |
| Flight cache stale | GIDS renders stale state + staleness indicator | cache miss + staleness_ms |
| Tarmac timer display fails | "Timer unavailable" shown | timer render failure — compliance event |

## Non-Negotiables

- **No polling of AOC** — DSS consumes from Service Bus; never polls AOC directly
- **Staleness SLA: 5 seconds** — from AOC publish to GIDS render; operational non-negotiable
- **Gate context in every log** — `flight_id`, `gate_id`, `timestamp` required on all audit events

## Acceptance Criteria

- Gate change: both GIDS surfaces updated within 5,000ms of AOC publish
- Tarmac timer: visible in primary GIDS view within 5,000ms of door-close; zero incidents in sub-screen
- `dss.display.staleness_ms` custom metric per surface wired to Azure App Insights (Sprint 1)
- Service Bus consumer lag alert: threshold >3s sustained >1min
- 100% of gate/flight state transitions emit audit record with `staleness_ms` field
