# Use Case: `:any` Type Elimination

**Laws:** ENG-2.1 (Aggregate Root), ENG-3.5 (Naming), ENG-4.1 (Atomic TDD)
**Repo:** Mobile-FLIFO-BFF — 15+ `:any` annotations; mobile-cache-ms — 9

## Problem

FLIFO-BFF has `validatedQuery: any` in 5+ function signatures, `req: any` in 3 controllers, `requestId: any` in 2 services. The compiler cannot catch field name typos or wrong argument order. The confirmed typo `valistringdQuery` in `types/client/flightStatus.ts` is a direct consequence — no type checker catches an interface property name typo.

## Migration Pattern

**Step 1 — Define the interface for the specific endpoint:**
```typescript
// types/requests/flightStatusRequest.ts
export interface FlightStatusQuery {
  readonly flightNumber: string;
  readonly departureDate: string;
  readonly origin?: string;
  readonly destination?: string;
}
```

**Step 2 — Replace `any` at the call site:**
```typescript
// BEFORE
async function createFlightStatus(validatedQuery: any, requestId: any) { ... }

// AFTER
async function createFlightStatus(
  query: FlightStatusQuery,
  requestId: string
): Promise<FlightStatus> { ... }
```

**Step 3 — Write a compile-time test:**
```typescript
// Compile-time proof — this line failing at build = regression caught
const _typeCheck: FlightStatusQuery = {
  flightNumber: 'AA100',
  departureDate: '2026-04-27',
};
```

## AA Confirmation

`mobile-platform-bff` eliminated `:any` with 92 TypeScript interfaces — highest coverage in fleet (100%). FLIFO-BFF at 15+ `:any` correlates directly with its 80% branch coverage: untypeable branches are also untested branches.

## Rule

Zero `:any` in new TypeScript BFF code. Every `eslint-disable @typescript-eslint/no-explicit-any` comment is a BLOCKING review finding.
