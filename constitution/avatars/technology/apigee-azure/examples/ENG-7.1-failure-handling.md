---
avatar: avatar-tech-apigee-azure
law: ENG-7.1
title: "Failure Handling Law"
---

# ENG-7.1 — Failure Handling Law: Apigee + Azure

**Every failure has an expected response. No unhandled exceptions, no unbounded timeouts, no silent message loss.**

---

## Apigee — FaultRules (Normalized Error Envelope)

```xml
<!-- REQUIRED on every proxy — catches all unhandled faults -->
<FaultRules>
  <FaultRule name="UnknownFault">
    <Step><Name>RF-NormalizedError</Name></Step>
    <Condition>true</Condition>
  </FaultRule>
</FaultRules>

<RaiseFault name="RF-NormalizedError">
  <FaultResponse>
    <Set>
      <Payload contentType="application/json">
        { "code": "{fault.name}", "message": "An error occurred", "correlationId": "{correlationId}" }
      </Payload>
      <StatusCode>500</StatusCode>
    </Set>
  </FaultResponse>
</RaiseFault>
```

**Never expose internal stack traces.** The normalized envelope always includes the correlation ID for investigation.

---

## Apigee — Target Timeout (Non-Negotiable)

```xml
<HTTPTargetConnection>
  <Properties>
    <Property name="connect.timeout.millis">5000</Property>   <!-- 5s connect timeout -->
    <Property name="io.timeout.millis">30000</Property>       <!-- 30s read timeout — never unbounded -->
  </Properties>
</HTTPTargetConnection>
```

---

## Azure Functions — Service Bus DLQ Monitoring

```hcl
# Terraform — alert on first DLQ message within 5 minutes
resource "azurerm_monitor_metric_alert" "dlq_alert" {
  name                = "biometric-events-dlq-alert"
  resource_group_name = var.resource_group
  scopes              = [azurerm_servicebus_queue.biometric_events.id]
  criteria {
    metric_name = "DeadLetteredMessageCount"
    operator    = "GreaterThan"
    threshold   = 0
  }
  window_size = "PT5M"
  frequency   = "PT1M"
}
```

---

## Azure Functions — Idempotency (Service Bus at-least-once delivery)

```csharp
[FunctionName("ProcessBiometricMatchEvent")]
public async Task Run(
    [ServiceBusTrigger("biometric-events")] BiometricMatchEvent evt,
    ILogger log)
{
    if (await _store.ExistsAsync(evt.EventId))
    {
        log.LogInformation("Duplicate {EventId} — skipping", evt.EventId);
        return;  // idempotent exit — do not throw
    }
    await _store.ProcessAndMarkAsync(evt);
}
```

---

## Acceptance Criteria
- [ ] All proxies have FaultRules with RF-NormalizedError — verified by proxy scan in CI
- [ ] All target connections have `io.timeout.millis` ≤30000 — verified by policy scan
- [ ] DLQ metric alert configured for every Service Bus queue — verified in Terraform plan
- [ ] Idempotency test passing: same event delivered twice produces same state (not double-applied)
