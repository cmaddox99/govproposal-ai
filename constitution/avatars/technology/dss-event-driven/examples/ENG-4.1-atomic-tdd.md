---
avatar: avatar-tech-dss-event-driven
law: ENG-4.1
title: "Atomic TDD Law"
---

# ENG-4.1 — Atomic TDD Law: DSS Event-Driven

**One failing test per layer before one line of implementation. Three layers — three test patterns.**

---

## Layer 1 — Event Processor (Node.js + Jest + Testcontainers)

```typescript
// RED — test/flight-event-handler.test.ts
import { createFlightEventHandler } from '../src/handlers/flight-event-handler';
import { createTestDb } from './helpers/testcontainers';

describe('FlightEventHandler', () => {
  let db: TestDatabase;
  let handler: FlightEventHandler;

  beforeAll(async () => { db = await createTestDb(); handler = createFlightEventHandler(db); });

  it('updates flight status to DELAYED on delay event', async () => {
    const event = { eventId: 'evt-001', type: 'FLIGHT_DELAYED',
      flightId: 'AA-123', gateId: 'A12', delayMinutes: 45 };
    await db.seed.flight({ flightId: 'AA-123', status: 'ON_TIME' });
    await handler.process(event);
    const flight = await db.query.flight('AA-123');
    expect(flight.status).toBe('DELAYED');
    expect(flight.lastEventId).toBe('evt-001');  // idempotency key saved
  });

  it('is idempotent — same event twice does not double-apply', async () => {
    await handler.process(event);
    await handler.process(event);  // duplicate
    const flight = await db.query.flight('AA-123');
    expect(flight.delayMinutes).toBe(45);  // not 90
  });
});
// GREEN — implement with PostgreSQL upsert on eventId as idempotency key
// REFACTOR — extract event normalization (timestamp, gateId validation) to shared event-normalizer
```

---

## Layer 2 — Display API (Node.js + supertest)

```typescript
// RED — test/gate-display.test.ts
describe('GET /api/v1/displays/gate/:gateId', () => {
  it('returns gate data from Redis cache (no DB call on hit)', async () => {
    const { app, redis, pg } = createTestApp();
    redis.get.mockResolvedValue(JSON.stringify({ status: 'BOARDING', gateId: 'A12' }));
    const res = await request(app)
      .get('/api/v1/displays/gate/A12')
      .set('x-correlation-id', 'test-corr-001');
    expect(res.status).toBe(200);
    expect(res.body.source).toBe('cache');
    expect(pg.query).not.toHaveBeenCalled();  // Redis hit — no DB
  });

  it('falls back to PostgreSQL and marks staleness on Redis miss', async () => {
    redis.get.mockResolvedValue(null);
    pg.query.mockResolvedValue({ rows: [{ status: 'ON_TIME', gateId: 'A12' }] });
    const res = await request(app).get('/api/v1/displays/gate/A12');
    expect(res.body.source).toBe('db');
    expect(res.body.stale).toBe(true);
  });
});
```

---

## Layer 3 — React UI Component (Jest + React Testing Library)

```tsx
// RED — src/__tests__/GateDisplayBoard.test.tsx
it('renders BOARDING status with correct styling', () => {
  render(<GateDisplayBoard flightId="AA-123" status="BOARDING" gateId="A12" />);
  const badge = screen.getByTestId('status-badge');
  expect(badge).toHaveTextContent('BOARDING');
  expect(badge).toHaveClass('status-boarding');
});

it('shows staleness indicator when stale=true', () => {
  render(<GateDisplayBoard flightId="AA-123" status="ON_TIME" stale={true} />);
  expect(screen.getByTestId('staleness-banner')).toBeVisible();
});
// Never go dark — stale display is always preferable to blank
```
