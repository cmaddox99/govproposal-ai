---
avatar: avatar-tech-dss-event-driven
law: ENG-3.1
title: "Complexity Limits"
---

# ENG-3.1 — Complexity Limits: DSS Event-Driven

**Max cyclomatic complexity: 8 per handler. Route handlers: max 30 lines. N event types = registry pattern.**

---

## Event Processor — Registry/Dispatch Pattern

```typescript
// WRONG — switch chain, complexity grows with every new event type
async function handleEvent(event: DisplayHubEvent) {
  if (event.type === 'FLIGHT_DELAYED') {
    // 20 lines of delay logic
  } else if (event.type === 'GATE_CHANGE') {
    // 20 lines of gate change logic
  } else if (event.type === 'FLIGHT_CANCELLED') {
    // 20 lines of cancel logic
  }
  // complexity = 4+ and rising with every new type
}

// CORRECT — registry pattern: one handler class per event type
// src/handlers/index.ts
const eventHandlers = new Map<string, EventHandler>([
  ['FLIGHT_DELAYED',   new FlightDelayedHandler(db, redis)],
  ['GATE_CHANGE',      new GateChangeHandler(db, redis)],
  ['FLIGHT_CANCELLED', new FlightCancelledHandler(db, redis)],
]);

async function dispatch(event: DisplayHubEvent): Promise<void> {
  const handler = eventHandlers.get(event.type);
  if (!handler) throw new UnknownEventTypeError(event.type);
  await handler.handle(event);  // complexity = 2
}

// Each handler class: complexity ≤ 8, single responsibility
class FlightDelayedHandler implements EventHandler {
  async handle(event: FlightDelayedEvent): Promise<void> {
    const idempotencyKey = event.eventId;
    if (await this.db.exists(idempotencyKey)) return;
    await this.db.upsertFlightDelay(event.flightId, event.delayMinutes, idempotencyKey);
    await this.redis.invalidate(`gate:${event.gateId}`);
  }
}
```

---

## Display API Route Handlers — Max 30 Lines

```typescript
// CORRECT — business logic in service layer, not route handler
router.get('/api/v1/displays/gate/:gateId', async (req, res) => {
  // route handler: orchestration only — ≤10 lines
  const { gateId } = req.params;
  const correlationId = req.headers['x-correlation-id'] as string;
  try {
    const display = await gateDisplayService.getDisplay(gateId, correlationId);
    res.json(display);
  } catch (err) {
    next(err);  // centralized error handler
  }
});

// Business logic lives here — testable in isolation
class GateDisplayService {
  async getDisplay(gateId: string, correlationId: string): Promise<GateDisplay> {
    const cached = await this.redis.get(`gate:${gateId}`);
    if (cached) return { ...JSON.parse(cached), source: 'cache', stale: false };
    const db = await this.pg.queryGate(gateId);
    return { ...db, source: 'db', stale: true };  // Redis miss = stale
  }
}
```

---

## Acceptance Criteria
- [ ] ESLint `complexity` rule set to max 8 — enforced in CI across all Node.js services
- [ ] No handler function longer than 30 lines — ESLint `max-lines-per-function` rule
- [ ] All new event types added via registry (no switch-chains) — code review checklist
