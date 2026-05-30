---
avatar: avatar-tech-apigee-azure
law: ENG-3.1
title: "Complexity Limits"
---

# ENG-3.1 — Complexity Limits: Apigee + Azure

**Max cyclomatic complexity: 8 per function. Max 3 conditions per Apigee FlowCondition.**

---

## Apigee — Proxy Flow Complexity

### Violation: Nested conditions in one FlowCondition
```xml
<!-- WRONG — unreadable, untestable -->
<Flow name="BiometricsRouting">
  <Condition>
    (request.verb = "POST") AND (proxy.pathsuffix = "/boarding")
    AND (request.header.x-env != "test") AND (request.header.authorization != null)
  </Condition>
</Flow>
```

### Correct: One concern per named condition
```xml
<!-- CORRECT — each condition is named and testable -->
<Flow name="BiometricsBoardingPost">
  <Condition>request.verb = "POST" AND proxy.pathsuffix = "/boarding"</Condition>
  <!-- auth and env routing handled by shared flows, not inline conditions -->
</Flow>
```

**Rule:** If you need >3 conditions in one Flow, extract to a shared flow or use a KVM-backed routing table.

---

## Azure Functions — Handler Complexity

```typescript
// WRONG — cyclomatic complexity > 8
async function handle(event: GateEvent) {
  if (event.type === 'GATE_CHANGE') {
    if (event.flightId) {
      if (isValidGate(event.toGate)) {
        if (!isDuplicate(event.eventId)) {
          if (event.priority === 'HIGH') { /* ... */ }
          else { /* ... */ }
        }
      }
    }
  } else if (event.type === 'CANCEL') { /* ... */ }
  // complexity > 8 — linter will BLOCK
}

// CORRECT — dispatch registry pattern
const handlers: Record<string, (e: GateEvent) => Promise<void>> = {
  'GATE_CHANGE': handleGateChange,
  'CANCEL': handleCancel,
};

async function dispatch(event: GateEvent) {
  const handler = handlers[event.type];
  if (!handler) throw new UnknownEventTypeError(event.type);
  await handler(event);  // complexity = 2
}
```

---

## Terraform — Module Complexity

- One `azurerm_*` resource per module file (not 10 resources in one `main.tf`)
- Modules expose max 5 output variables — if more needed, split the module
- `count` / `for_each` conditionals: max 2 nesting levels
