---
avatar: avatar-tech-apigee-azure
law: ENG-6.7
title: "Audit Trail Law"
---

# ENG-6.7 — Audit Trail Law: Apigee + Azure

**Every request logged. Correlation ID generated at Apigee edge and propagated to all downstream services.**

---

## Apigee — Correlation ID (Non-Negotiable)

```xml
<!-- Generate at edge if not present — REQUIRED on every proxy -->
<AssignMessage name="AM-CorrelationId">
  <AssignVariable>
    <Name>correlationId</Name>
    <Ref>request.header.x-correlation-id</Ref>
    <Value>{generateUUID()}</Value>  <!-- generate if not provided by caller -->
  </AssignVariable>
  <Set>
    <Headers>
      <Header name="x-correlation-id">{correlationId}</Header>
    </Headers>
  </Set>
  <IgnoreUnresolvedVariables>true</IgnoreUnresolvedVariables>
</AssignMessage>
```

This ID must appear in:
1. Apigee MessageLogging to Azure Monitor
2. All downstream Azure Function logs (propagated via HTTP header)
3. Azure Application Insights traces for the same request

---

## Apigee — MessageLogging Policy (No PII)

```xml
<MessageLogging name="ML-AzureMonitor">
  <Syslog>
    <Message>
      {
        "correlation_id": "{correlationId}",
        "proxy": "{apiproxy.name}",
        "verb": "{request.verb}",
        "path": "{proxy.pathsuffix}",
        "status": "{response.status.code}",
        "latency_ms": "{target.elapsed.time}",
        "client_id": "{client_id}",
        "timestamp": "{system.timestamp}"
      }
    </Message>
    <!-- NEVER log: request.body, response.body, Authorization header, PNR, biometric data -->
  </Syslog>
</MessageLogging>
```

**Log metadata only — never request/response body.** PNR and biometric identifiers must never appear in Apigee logs.

---

## Azure Functions — Structured JSON Logging

```csharp
// Every Function invocation logs these fields
log.LogInformation(
    "Processed {EventType} | correlationId={CorrelationId} | flightId={FlightId} | gateId={GateId} | result={Result}",
    eventType, correlationId, flightId, gateId, result
);
// Azure Application Insights picks up structured properties for filtering
```

---

## Acceptance Criteria
- [ ] Every proxy has AM-CorrelationId + ML-AzureMonitor policies — verified by proxy scan in CI
- [ ] Correlation ID appears in both Apigee log and Azure Monitor for same request (integration test)
- [ ] No PNR, biometric template, or Authorization header value in any Apigee MessageLogging body
