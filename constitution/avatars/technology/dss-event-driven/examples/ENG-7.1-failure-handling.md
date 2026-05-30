---
avatar: avatar-tech-dss-event-driven
law: ENG-7.1
title: "Failure Handling Law"
---

# ENG-7.1 — Failure Handling Law: DSS Event-Driven

**Fail open with stale data — never dark. Idempotent processors. DLQ alert in 5 minutes. Circuit breaker on PostgreSQL reads.**

---

## Idempotent Event Processors

```typescript
// Every processor uses event ID as PostgreSQL upsert key
async function processGateEvent(event: GateEvent): Promise<void> {
  await db.query(
    `INSERT INTO gate_state (event_id, gate_id, flight_id, status, updated_at)
     VALUES ($1, $2, $3, $4, NOW())
     ON CONFLICT (event_id) DO NOTHING`,  // idempotency: same event = no-op
    [event.eventId, event.gateId, event.flightId, event.status]
  );
  await redis.del(`gate:${event.gateId}`);  // invalidate cache after state write
}
// Reprocessing the same event twice produces the same state — safe for at-least-once delivery
```

---

## Dead-Letter Queue — Alert Within 5 Minutes

```hcl
resource "azurerm_monitor_metric_alert" "dss_dlq_alert" {
  name                = "dss-flightevent-dlq-alert"
  resource_group_name = var.resource_group
  scopes              = [azurerm_servicebus_queue.dss_flight_events.id]
  criteria {
    metric_namespace = "Microsoft.ServiceBus/namespaces"
    metric_name      = "DeadLetteredMessageCount"
    aggregation      = "Total"
    operator         = "GreaterThan"
    threshold        = 0
  }
  window_size = "PT5M"
  frequency   = "PT1M"
  action { action_group_id = azurerm_monitor_action_group.pagerduty_dss.id }
}
```

---

## Redis Fail-Open (Never Dark Display)

```typescript
// Display API: Redis miss → PostgreSQL fallback → stale indicator, never blank
async function getGateDisplay(gateId: string): Promise<GateDisplay> {
  try {
    const cached = await redis.get(`gate:${gateId}`);
    if (cached) return { ...JSON.parse(cached), stale: false, source: 'cache' };
  } catch (redisErr) {
    logger.warn('Redis unavailable — falling back to PostgreSQL', { gateId });
    // DO NOT throw — continue to PostgreSQL fallback
  }

  try {
    const dbData = await pg.queryGateDisplay(gateId);
    return { ...dbData, stale: true, source: 'db' };  // stale indicator on DB fallback
  } catch (pgErr) {
    logger.error('PostgreSQL unavailable — serving last known state from local cache', { gateId });
    const lastKnown = localCache.get(gateId);  // in-memory LRU as last resort
    if (lastKnown) return { ...lastKnown, stale: true, source: 'local-cache' };
    throw pgErr;  // only throw if truly no data available
  }
}
// A gate display with a "Data may be delayed" banner is always better than a blank screen
```

---

## Web UI — Graceful Degradation

```tsx
// React: always render last known state with staleness indicator
function GateDisplayBoard({ status, stale }: { status: string; stale: boolean }) {
  return (
    <div>
      {stale && <StalenessIndicator message="Data may be delayed" />}
      <StatusBadge status={status} data-testid="status-badge" />
    </div>
  );
  // Never render blank — always show something, even if stale
}
```

---

## Acceptance Criteria
- [ ] Idempotency test: same event delivered twice → state unchanged (Jest + Testcontainers)
- [ ] DLQ alert configured for every Service Bus queue in DSS — verified in Terraform plan
- [ ] Display API test: Redis throws → response still returns with `stale: true`, not 500
- [ ] Web UI test: `stale=true` prop renders staleness indicator (RTL test passing)
