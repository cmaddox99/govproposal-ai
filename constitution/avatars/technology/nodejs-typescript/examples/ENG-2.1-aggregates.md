# ENG-2.1 — DDD Aggregate Root · Node.js/TypeScript

**AA Fleet Reality — anemic domain models throughout.** All 4 TS BFF repos treat types as pure data containers. Zero TypeScript classes with behavior in FLIFO-BFF or cache-ms. `mobile-platform-bff` uses 92 interfaces — well-typed but still anemic.

## AA Pattern — typed value objects prevent typo bugs

FLIFO-BFF has `Flight` interface defined twice with different shapes — once in `flightStatus.ts` and again in `flightSchedules.ts`. No value object means the compiler can't distinguish them.

```typescript
// BAD — plain strings, compiler can't distinguish flight number from airport code
function buildStatus(flightNumber: string, origin: string): FlightStatus { }

// FIX — branded types prevent argument swap at compile time
type FlightNumber = string & { readonly _brand: 'FlightNumber' };
type AirportCode = string & { readonly _brand: 'AirportCode' };

function buildStatus(fn: FlightNumber, origin: AirportCode): FlightStatus { }
// buildStatus(origin, flightNumber) → compile error ✅
```

## Rule

Each BFF domain concept (flight, booking, config entry) must have a named type or interface. `any` is always wrong — it collapses the domain model to an opaque blob. `mobile-platform-bff` demonstrates the target: 92 interfaces, zero `any` in core domain code.
