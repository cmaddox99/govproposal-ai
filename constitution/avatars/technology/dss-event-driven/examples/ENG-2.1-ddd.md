---
avatar: avatar-tech-dss-event-driven
law: ENG-2.1
title: "Domain-Driven Design Law"
---

# ENG-2.1 — Domain-Driven Design Law: DSS Event-Driven

**Each display type is a bounded context. Write model and read model are strictly separated.**

---

## Bounded Context Map — DSS

```
┌─────────────────────────────────────────────────────────┐
│                  DisplayHub (Write Model)                │
│  dss-displayhub-flightevent  →  PostgreSQL flight state │
│  dss-displayhub-gateevent    →  PostgreSQL gate state   │
│  dss-displayhub-bossevent    →  PostgreSQL baggage state│
│  dss-displayhub-flightcache  →  shared READ infrastructure│
└──────────────────────────┬──────────────────────────────┘
                           │  EVENT (not direct DB call)
┌──────────────────────────▼──────────────────────────────┐
│                  Display APIs (Read Model)               │
│  dss-web-fids-api   → serves FIDS context only          │
│  dss-web-gids-api   → serves GIDS context only          │
│  dss-web-bids-api   → serves BIDS context only          │
└─────────────────────────────────────────────────────────┘
```

**The cardinal rule:** No Display API queries a DisplayHub internal table directly. Cross-context data always travels via event or API contract.

---

## Aggregate Roots Per Context

```typescript
// CORRECT — GIDS bounded context owns its own aggregate
// dss-displayhub-gateevent/src/domain/gate-display.aggregate.ts
export class GateDisplayAggregate {
  private readonly gateId: string;
  private flightId: string;
  private status: DisplayStatus;
  private lastEventId: string;  // idempotency

  apply(event: GateEvent): void {
    if (event.eventId === this.lastEventId) return;  // idempotent
    this.flightId = event.flightId;
    this.status = mapEventToStatus(event.type);
    this.lastEventId = event.eventId;
  }
}

// WRONG — Display API directly querying DisplayHub's table
// SELECT * FROM dss_displayhub_gateevent.gate_state WHERE gate_id = $1
// ❌ BLOCKING — cross-context DB query violates bounded context isolation
```

---

## Event Contract Between Contexts

```typescript
// Context boundary: DisplayHub publishes; Display APIs consume
interface GateDisplayUpdatedEvent {
  eventId: string;
  gateId: string;
  flightId: string;
  newStatus: 'BOARDING' | 'DELAYED' | 'CANCELLED' | 'ON_TIME';
  updatedAt: string;  // ISO-8601
  // No internal DisplayHub model fields — only what consumers need
}
```

**Events are the only cross-context interface.** No shared domain models, no shared databases across contexts.

---

## flight-cache — Shared Infrastructure, Not Shared Domain

`dss-displayhub-flightcache` is shared infrastructure (like a database). Access it via its API — never via direct table query from another context.

```typescript
// CORRECT
const flight = await flightCacheApi.getFlight(flightId);  // API call

// WRONG
const flight = await db.query('SELECT * FROM dss_flight_cache WHERE id = $1', [flightId]);
// ❌ bypasses the API contract
```
