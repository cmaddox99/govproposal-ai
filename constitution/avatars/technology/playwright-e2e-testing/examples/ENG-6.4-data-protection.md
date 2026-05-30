---
avatar: avatar-playwright-e2e-testing
law: ENG-6.4
title: "Data Protection Law"
---

# ENG-6.4 — Data Protection: Playwright E2E Application

## What This Law Requires

Test data containing PII (employee IDs, SSNs, names) must be protected. Test accounts use synthetic or dedicated test identities. No production PII in test fixtures, screenshots, or trace files.

## Compliant Example

**Environment-based test identity (never hardcoded):**

```typescript
// .env.test.local (.gitignored)
TEST_USER_ID=361
TEST_PASSWORD=test.account.secret
TEST_SSN_LAST4=0000

// tests/config/test.config.ts
export const testConfig = {
  testUserId: process.env.TEST_USER_ID!,
  testPassword: process.env.TEST_PASSWORD!,
  testSsnLast4: process.env.TEST_SSN_LAST4!,
};
```

**Playwright config — artifacts contain PII risk:**

```typescript
// playwright.config.ts
export default defineConfig({
  outputDir: 'test-results', // .gitignored — may contain screenshots with PII
  use: {
    screenshot: 'only-on-failure', // minimize PII capture
    video: 'retain-on-failure',
    trace: 'retain-on-failure',
  },
});
```

**.gitignore — REQUIRED entries:**

```
test-results/
playwright-report/
playwright/.auth/
.env.test.local
```

## Violation Example

```typescript
// BAD: Production employee data in test fixtures
const testEmployee = { id: '123456', ssn: '555-12-3456', name: 'John Smith' };

// BAD: Committing trace/screenshot files containing PII
// test-results/ checked into git
```

## Edge Cases

- CI/CD artifacts (screenshots, traces) may contain PII — configure retention policies
- `storageState` files contain session tokens — treat as PII-adjacent secrets
