# Use Case: FLIFO BFF TypeScript Layer

**Laws:** PRD-4.1 (MVP), ENG-3.1 (Complexity), ENG-4.1 (Atomic TDD)
**Repo:** Mobile-FLIFO-BFF — TypeScript/Express · 5.8/10 · 646 LOC god module

## What the FLIFO BFF does

`Mobile-FLIFO-BFF` aggregates flight status, schedules, and live activity data from 4 upstream services (FLIFO Flight Info, FLIFO Search, CNE Notifications, Locations) into mobile-friendly payloads. It is the TypeScript reference for the check-in domain's flight status UI.

## Confirmed bugs + gaps

| Finding | File | Impact |
|---|---|---|
| `valistringdQuery` typo in type definition | `flightStatus.ts` | Wrong field name used across 5+ call sites — silent runtime risk |
| `caclulateMaxAge` typo | `cacheControlHeaderUtil.ts` | Wrong function name — callers may bypass intended cache logic |
| `tokenCache` is module-level mutable state | `tokenGeneratorService.ts` | Race condition risk under concurrent requests |
| 15+ `any` type annotations | Multiple services | TypeScript type safety disabled in request handling |
| 80.34% branch coverage | Jest/Istanbul | Below ENG-4.1 90% threshold |

## Product implication

An incorrect `calculateMaxAge` means flight status responses may be cached for the wrong duration — passengers see stale departure times. The typo bug exists in production. Fix: rename + add a test asserting the correct cache duration for each status type.

## Reference implementation

`mobile-platform-bff` (7.2/10) shows the TS/Express architecture this BFF should reach: named interfaces for every request/response shape, 100% coverage, no module-level side effects.
