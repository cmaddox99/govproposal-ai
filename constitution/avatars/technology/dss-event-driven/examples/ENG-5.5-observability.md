---
avatar: avatar-tech-dss-event-driven
law: ENG-5.5
title: "Observability Law"
---

# ENG-5.5 — Observability Law: DSS Event-Driven

**Structured JSON logs. Display staleness metric on every event. PagerDuty alert if staleness >10s for 60s.**

---

## Structured Log Schema — All DSS Services

Every log entry across all DSS services must include these fields (structured JSON):

```json
{
  "timestamp": "ISO-8601",
  "level": "INFO | WARN | ERROR",
  "service": "dss-displayhub-flightevent",
  "correlation_id": "uuid",
  "flight_id": "AA-1234",
  "gate_id": "DFW-A15",
  "display_type": "GIDS | FIDS | BIDS | WIDS | null",
  "event_type": "FLIGHT_DELAYED | GATE_CHANGE | ...",
  "message": "Human-readable description"
}
```

**NEVER include:** `pnr`, `passenger_name`, `biometric_template`, or `biometric_score` in DSS log streams.

---

## Custom Metric: event_to_display_latency_ms

```typescript
// In DisplayHub event processor — record after state is persisted AND cache invalidated
import { TelemetryClient } from 'applicationinsights';

const appInsights = new TelemetryClient(process.env.APPINSIGHTS_CONNECTIONSTRING);

async function processEvent(event: DisplayHubEvent): Promise<void> {
  const startMs = Date.now();
  await db.upsert(event);
  await redis.invalidate(`gate:${event.gateId}`);
  const latencyMs = Date.now() - startMs;

  appInsights.trackMetric({
    name: 'event_to_display_latency_ms',
    value: latencyMs,
    properties: {
      gateId: event.gateId,
      displayType: event.displayType,
      eventType: event.type
    }
  });
}
```

---

## Alert Configuration — Azure Monitor + PagerDuty

```json
{
  "alertName": "DSS Display Staleness Critical",
  "condition": {
    "metric": "event_to_display_latency_ms",
    "operator": "GreaterThan",
    "threshold": 10000,
    "aggregation": "Average",
    "windowSize": "PT1M",
    "frequency": "PT1M"
  },
  "severity": 1,
  "actionGroup": "PagerDuty-DSS-P1",
  "description": "Display staleness >10s for 60s — gate displays may be showing stale flight data"
}
```

**Two alert thresholds:**
- **WARNING (5s–10s):** Send to Slack #dss-ops — investigate
- **CRITICAL (>10s for 60s):** PagerDuty P1 — operational incident, wake engineer

---

## Cache Hit Rate Metric

```typescript
// Track cache hit rate per display type
appInsights.trackMetric({
  name: 'redis_cache_hit_rate',
  value: hitCount / totalCount,
  properties: { displayType: 'GIDS', gateId: event.gateId }
});
// Alert if cache hit rate <90% for any display type (indicates Redis issue)
```

---

## Acceptance Criteria
- [ ] All services log structured JSON with required fields — schema validation test in CI
- [ ] `event_to_display_latency_ms` metric emitted for every processed event
- [ ] PagerDuty alert fires when staleness >10s (integration test with mock metric threshold)
- [ ] No PNR/biometric data in any DSS log — automated scan in CI
