# ENG-2.2 — Layered Architecture · Node.js/TypeScript

**AA Reference — mobile-platform-bff layer model:**
```
api/routes/ → application/services/ → domain/ → infrastructure/
```
13 route modules · versioned endpoints · no business logic in routes.

**HARD_BLOCK — module-level side effects (cache-ms confirmed):**

```typescript
// BAD — redis.ts runs side effects on import
import { initiateConnections } from './redis'; // ← runs immediately
// Every test that imports any module touching redis.ts triggers real connections

// FIX — factory function, caller controls lifecycle
export function createRedisConnections(config: RedisConfig): RedisClient[] {
  // called explicitly in app.ts startup — not on import
}
```

**HARD_BLOCK — no DI in any AA BFF TS repo today. Target pattern:**

```typescript
// BAD (cache-ms): Token is module-scope singleton — untestable
import { Token } from './token'; // instantiated on import

// FIX: constructor injection
export class CacheController {
  constructor(
    private readonly cache: CacheProvider,
    private readonly auth: AuthProvider
  ) {}
}
```

**AA Layer violation — FLIFO-BFF:** `flightScheduleService.ts` embeds environment-switching logic (4-branch `if/else` for prod/non-prod/dev/test) — infrastructure concern inside application layer. Extract to config module.
