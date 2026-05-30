---
avatar: avatar-tech-dss-event-driven
law: ENG-6.7
title: "Audit Trail Law"
---

# ENG-6.7 — Audit Trail Law: DSS Event-Driven

**What this law requires:** Every significant action must produce a structured, immutable audit record containing who, what, when, where, and result. For event-driven microservices, correlation IDs must be propagated across all services and events so a single flight event can be traced end-to-end across Azure Service Bus, all processing microservices, and all downstream systems.

---

## Correlation ID Propagation Strategy

The **Azure Service Bus Message ID** serves as the system-wide correlation ID. Every service that processes or emits events must carry this ID forward — never generate a new one mid-flow.

```typescript
// dss-displayhub-flightevent/src/middleware/correlation.middleware.ts
import { ServiceBusReceivedMessage } from "@azure/service-bus";

export interface CorrelationContext {
  correlationId: string;    // Azure Service Bus messageId — never regenerated mid-flow
  causationId: string;      // ID of the event that triggered this one
  traceId: string;          // Distributed trace ID (OpenTelemetry W3C traceparent)
  spanId: string;
}

export function extractCorrelation(msg: ServiceBusReceivedMessage): CorrelationContext {
  return {
    correlationId: msg.messageId as string,          // Service Bus message ID is source of truth
    causationId: msg.correlationId ?? msg.messageId as string,
    traceId: (msg.applicationProperties?.["traceparent"] as string) ?? "",
    spanId: (msg.applicationProperties?.["tracestate"] as string) ?? "",
  };
}

// Propagate to outbound events
export function propagateCorrelation(
  ctx: CorrelationContext,
  outboundProps: Record<string, unknown>
): Record<string, unknown> {
  return {
    ...outboundProps,
    correlationId: ctx.correlationId,     // Preserve original — never replace
    causationId: ctx.correlationId,       // This event was caused by the inbound event
    traceparent: ctx.traceId,
  };
}
```

---

## Structured Audit Logging (Who / What / When / Where / Result)

```typescript
// dss-shared/src/audit/audit-logger.ts
import { createLogger, format, transports } from "winston";

export interface AuditEvent {
  correlationId: string;    // Propagated from Service Bus messageId
  actor: string;            // Service principal or AAD identity (no end-user PII)
  action: string;           // e.g., "FLIGHT_EVENT_PROCESSED", "GATE_DISPLAY_UPDATED"
  resource: string;         // e.g., "flight:AA1234/gate:B22"
  outcome: "SUCCESS" | "FAILURE" | "PARTIAL";
  timestamp: string;        // ISO-8601 UTC
  durationMs: number;
  metadata?: Record<string, unknown>;
}

const auditLogger = createLogger({
  level: "info",
  format: format.combine(
    format.timestamp(),
    format.json()            // Structured JSON — parseable by Azure Log Analytics
  ),
  defaultMeta: { service: process.env.SERVICE_NAME, version: process.env.SERVICE_VERSION },
  transports: [new transports.Console()],  // AKS captures stdout → Azure Monitor
});

export function auditLog(event: AuditEvent): void {
  auditLogger.info("AUDIT", { ...event, type: "AUDIT_EVENT" });
}
```

---

## Flight Event Processing Audit Example

```typescript
// dss-displayhub-flightevent/src/handlers/flight-event.handler.ts
import { auditLog } from "../../shared/src/audit/audit-logger";
import { extractCorrelation } from "../middleware/correlation.middleware";

export async function handleFlightEvent(
  msg: ServiceBusReceivedMessage
): Promise<void> {
  const ctx = extractCorrelation(msg);
  const startMs = Date.now();

  try {
    const event = FlightEventSchema.parse(msg.body);
    await updateGateDisplay(event, ctx);
    await notifyGateAgents(event, ctx);

    auditLog({
      correlationId: ctx.correlationId,
      actor: "dss-flightevent-service",        // Service identity — no end-user PII
      action: "FLIGHT_EVENT_PROCESSED",
      resource: `flight:${event.flightNumber}/gate:${event.departureGate}`,
      outcome: "SUCCESS",
      timestamp: new Date().toISOString(),
      durationMs: Date.now() - startMs,
      metadata: {
        eventType: event.eventType,
        flightNumber: event.flightNumber,
        gate: event.departureGate,
      },
    });
  } catch (err) {
    auditLog({
      correlationId: ctx.correlationId,
      actor: "dss-flightevent-service",
      action: "FLIGHT_EVENT_PROCESSED",
      resource: `flight:${msg.body?.flightNumber ?? "unknown"}`,
      outcome: "FAILURE",
      timestamp: new Date().toISOString(),
      durationMs: Date.now() - startMs,
      metadata: { error: (err as Error).message },
    });
    throw err;  // Re-throw so Service Bus can dead-letter after max retries
  }
}
```

---

## End-to-End Trace in Azure Log Analytics

All DSS services emit to the same Log Analytics workspace. A single KQL query reconstructs the full event chain by `correlationId`:

```kusto
// Reconstruct full flight event processing chain — paste correlation ID from incident ticket
let correlationId = "msg-20260315-AA1234-B22-001";
union ContainerLog, AppTraces, AppExceptions
| where Properties.correlationId == correlationId
    or Properties["correlationId"] == correlationId
| project TimeGenerated, ContainerName, Properties.service, Properties.action,
          Properties.outcome, Properties.resource, Properties.durationMs, Message
| order by TimeGenerated asc
```

---

## Audit Retention and Immutability

| Requirement | Implementation |
|-------------|---------------|
| Retention period | 90 days hot (Log Analytics) + 7 years cold (Azure Storage immutable blob) |
| Tamper protection | Immutable storage policy — blobs locked after 24 h; no delete/overwrite |
| Access control | Read-only for application identities; write via diagnostic settings only |
| Query SLA | P95 audit query < 5 s for 90-day window (Log Analytics tier S2) |
| Correlation completeness | Every Service Bus message must carry `correlationId` before processing |
