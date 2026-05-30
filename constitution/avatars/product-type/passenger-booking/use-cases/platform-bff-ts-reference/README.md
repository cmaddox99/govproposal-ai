# Use Case: Platform BFF TypeScript Reference

**Laws:** PRD-1.1 (Product Discovery), PRD-4.1 (MVP), ENG-4.1 (Atomic TDD)
**Repo:** mobile-platform-bff — TypeScript/Node · 7.2/10 · **100% coverage**

## Why this matters for booking

`mobile-platform-bff` serves the AA mobile app's platform layer — feature toggles, native deep links, and notification registration. These capabilities gate booking flows: a wrong feature flag value can silently disable the booking CTA for a segment of users.

## What makes it the TS reference implementation

| Quality dimension | Score | Detail |
|---|---|---|
| Coverage | 100% | Statements, branches, functions, lines — all 100% |
| Largest file | 381 LOC | Within budget; versioned endpoint handler |
| TypeScript interfaces | 92 | Every request/response shape is named |
| Test blocks | 202 | 431 assertions; 2.13 assertions/test |
| Module-level side effects | 0 | All dependencies wired in app.ts |

## Pattern to copy

```typescript
// mobile-platform-bff: versioned endpoint factory
// New version = new file, old version intact — no regression risk
// app/routes/notificationRegistration/v1.0.ts  (143 LOC)
// app/routes/notificationRegistration/v1.1.ts  (new version, isolated)
```

This versioning pattern means a booking-related flag change in v1.1 cannot break v1.0 consumers.

## Product coaching note for booking team

Any new BFF endpoint serving booking flows must adopt platform-bff's pattern: typed request interfaces, 90%+ branch coverage, no `any`. The booking domain already has the Java reference (`aa-ct-mobile-booking-bff` at 7.4/10) — platform-bff is the TypeScript counterpart.
