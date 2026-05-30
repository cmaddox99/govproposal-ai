---
avatar: avatar-playwright-e2e-testing
law: ENG-3.1
title: "Complexity Limits"
---

# ENG-3.1 — Complexity Limits: Playwright E2E Application

## What This Law Requires

Test files and page objects must stay within size limits. No test file > 300 LOC. No page object class > 200 LOC. Extract shared patterns into helpers.

## Compliant Example

**TypeScript — focused spec file + extracted helper:**

```typescript
// tests/helpers/authSessionHelper.ts (reusable, ≤100 LOC)
export async function setupAuthSession(page: Page): Promise<void> {
  const userData = loadUserData();
  await page.addInitScript((data) => {
    sessionStorage.setItem('app_tab_session', 'true');
    if (data?.userId) sessionStorage.setItem('user_id', data.userId);
  }, userData);
}

// tests/direct-deposit.spec.ts (focused, ≤150 LOC)
test.describe('Direct Deposit', () => {
  test.beforeEach(async ({ page }) => {
    await setupAuthSession(page);
    await page.goto('/direct-deposit');
  });

  test('displays current accounts', async ({ page }) => { /* ... */ });
  test('can add new account', async ({ page }) => { /* ... */ });
});
```

**Java — Page Object within limits:**

```java
// LoginPageObjects.java (constants only, ≤50 LOC)
public class LoginPageObjects {
    public static final String USERNAME_INPUT = "//input[@name='username']";
    public static final String NEXT = "//button[@type='submit']";
    public static final String PASSWORD_INPUT = "//input[@name='password']";
    public static final String LOGIN_BUTTON = "//button[@type='submit']";
}
```

## Violation Example

```java
// BAD: God page object (67K, 1500+ LOC) — real anti-pattern from AA codebase
public class OSPOilAddsPage {
    // 50+ locator constants
    // 80+ step definition methods
    // Mixed concerns: locators + actions + assertions + waits
}
```

## Edge Cases

- Cucumber feature files are exempt from LOC limits but should not exceed 20 scenarios per file
- Test utility files (helpers/) may reach 200 LOC if they are pure utility functions
