# Node.js/TypeScript Guidance

> **AA BFF TS Fleet (2026-04-27):** 4 repos — mobile-platform-bff (7.2/10, 100% coverage, **reference**), mobile-platform-config (6.9/10, 90% threshold enforced), Mobile-FLIFO-BFF (5.8/10, 646-LOC god module, 15+ `any` types), mobile-cache-ms (5.2/10, 9 `:any`, 59% branch coverage, module-level side effects).

## AA Patterns & Anti-patterns

**HARD_BLOCK — `:any` type annotations.** Each `any` erases TypeScript's value. Replace with explicit interfaces. `mobile-cache-ms` has 9; FLIFO-BFF has 15+. Pattern: define request/response shapes as named interfaces.

**HARD_BLOCK — module-level side effects.** `redis.ts` calls `initiateConnections()` on import — untestable without mocking at module scope. Use factory functions or constructor injection instead.

**HARD_BLOCK — `eslint-disable` comments suppressing type errors.** Fix the type, don't suppress the warning.

**HARD_BLOCK — God module.** `flightStatusBuilder.ts` (646 LOC, 25+ functions, 480 branches) violates ENG-3.1. Extract into focused builder modules ≤150 LOC each.

**Reference — mobile-platform-bff.** 100% statement/branch/function/line coverage. 92 TypeScript interfaces. No file > 381 LOC. Highest coverage in AA BFF fleet.

**Reference — mobile-platform-config.** Config-as-code: YAML configs served via GitHub API + dual-layer cache (TTL + permanent fallback). 90 LOC max file. Jest 90% threshold enforced.

## Stack Reality

- AA BFF TS uses Express 4, not NestJS. Tests use Jest + Supertest (not Vitest).
- `node-cache` for in-process caching; Redis for distributed caching (`mobile-cache-ms`).
- Structured logging with `{ requestId, from, message }` pattern (FLIFO-BFF, platform-bff).
- No DI container in any AA BFF TS repo — ES module imports only. Constructor injection is the target pattern.
