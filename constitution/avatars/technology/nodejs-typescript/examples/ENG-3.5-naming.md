# ENG-3.5 — Naming Conventions · Node.js/TypeScript

**AA Confirmed Bugs via Bad Naming — FLIFO-BFF:**

| Typo | File | Impact |
|---|---|---|
| `valistringdQuery` (should be `validatedQuery`) | `types/client/flightStatus.ts` | Wrong type name used across 5+ call sites |
| `caclulateMaxAge` (should be `calculateMaxAge`) | `cacheControlHeaderUtil.ts` | Silently wrong — callers may reference both |

Both are shipped bugs. TypeScript does not catch typos in type/interface names at the point of definition.

## AA Naming Rules

```typescript
// AA BFF standard file naming (kebab-case):
flightStatusBuilder.ts   ✅
flightStatusController.ts ✅
logFetch.ts              ❌  // inconsistent — should be fetch-logger.ts or log-fetch.ts

// Interface naming — prefix with context, not I:
interface FlightStatusRequest { ... }   ✅
interface IFlightStatus { ... }         ❌  // Java habit, not TS convention

// Boolean predicates — must be verb phrases:
isDepartureDelayed()  ✅
isArrivalDelayed()    ✅
delayed()             ❌
```

**`any` as naming failure:** When a parameter is typed `any`, it has no name that conveys meaning. Each `any` must become a named interface. FLIFO-BFF has 15+ — `validatedQuery: any`, `req: any`, `requestId: any`.
