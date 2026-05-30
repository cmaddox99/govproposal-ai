# ENG-3.3 — Law of Demeter · Node.js/TypeScript

**AA Pattern — FLIFO-BFF controller reaching into request:**

```typescript
// BAD — liveActivityService.ts reaches into validatedRequestRegister manually
const flightNumber = req.validatedQuery.flightNumber;
const origin = req.validatedQuery.origin;
const destination = req.validatedQuery.destination;
// ... 12+ field extractions

// FIX — request object responsible for its own transformation
interface LiveActivityRequest {
  toServiceInput(): LiveActivityServiceInput;
}
const input = req.liveActivityRequest.toServiceInput();
```

**AA Pattern — inline condition chains violate readable demeter:**

```typescript
// BAD — FLIFO-BFF confirmed (single boolean expression, 5-part chain)
appVersion !== undefined &&
  appVersion !== null &&
  String(appVersion).trim() !== '' &&
  String(appVersion).toUpperCase() !== 'N/A' &&
  appVersion >= env.FLIGHTSTATUS_ERROR_VERSION

// FIX — named predicate
function isValidAppVersion(v: unknown): boolean {
  return v != null &&
    String(v).trim() !== '' &&
    String(v).toUpperCase() !== 'N/A' &&
    Number(v) >= env.FLIGHTSTATUS_ERROR_VERSION;
}
```

**Rule:** No chain of more than 2 property accesses on an external object. If you need 3+, ask the object for what you need.
