# Use Case: Module Side Effects → Constructor Injection

**Laws:** ENG-2.2 (Layered Architecture), ENG-4.1 (Atomic TDD)
**Repo:** mobile-cache-ms — `redis.ts` runs `initiateConnections()` on import; `Token` singleton created at module scope

## Problem

`redis.ts` calls `initiateConnections()` as a module-level statement — executes on first `import`. Any test file that imports anything touching `redis.ts` triggers real Redis connection attempts. Result: 59% branch coverage (cache-ms fleet low) because the Redis error branches are untestable without deep `jest.mock()` module intercepts.

```typescript
// BAD — mobile-cache-ms redis.ts (confirmed)
export const connections: RedisClient[] = [];
initiateConnections(); // ← runs on import, not on call
```

## Fix Pattern

```typescript
// STEP 1 — factory function, caller controls lifecycle
export function createRedisConnections(config: RedisConfig): RedisClient[] {
  const ibm = new RedisClient(config.ibm);
  const azure = new RedisClient(config.azure);
  assignEventListeners(ibm, 'IBM');
  assignEventListeners(azure, 'Azure');
  return [ibm, azure];
}

// STEP 2 — inject into CacheController
export class CacheController {
  constructor(private readonly clients: RedisClient[]) {}
  // Tests inject a mock array — no module-level wiring needed
}

// STEP 3 — wire in app.ts startup (one place)
const clients = createRedisConnections(config.redis);
app.use('/cache', new CacheController(clients).router());
```

## Expected Outcome

Branch coverage rises from 59% → 90%+ because Redis error paths are now testable by injecting a mock client that throws on `get()`/`set()`.

## Reference

`mobile-platform-bff` — no module-level side effects. All dependencies wired in `app.ts`. 100% branch coverage.
