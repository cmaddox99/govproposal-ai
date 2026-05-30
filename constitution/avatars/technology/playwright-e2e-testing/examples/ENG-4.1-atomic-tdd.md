---
avatar: avatar-playwright-e2e-testing
law: ENG-4.1
title: "Atomic TDD Law"
---

# ENG-4.1 — Atomic TDD: Playwright E2E Application

## What This Law Requires

Each E2E test covers exactly one user scenario. Write the test first (RED), implement the feature (GREEN), then refactor. Tests are isolated via Playwright's browser context per test.

## Compliant Example

**TypeScript (`@playwright/test`):**

```typescript
// tests/pay-statement.spec.ts — ONE scenario per test
import { test, expect } from '@playwright/test';
import { setupAuthSession } from './helpers/authSessionHelper';

test.use({ storageState: 'playwright/.auth/user.json' });

test.beforeEach(async ({ page }) => {
  await setupAuthSession(page);
});

test('employee can view current pay statement', async ({ page }) => {
  await page.goto('/pay-statements');
  await expect(page.getByRole('heading', { name: 'Pay Statements' })).toBeVisible();
  await page.getByRole('row').first().click();
  await expect(page.getByText('Net Pay')).toBeVisible();
});
```

**Java (Playwright + Cucumber):**

```java
// LogintoApplication.java — single step, single concern
@Given("Login into OSP Application")
public void login_into_osp_application() {
    testContext.page.navigate(ConfigReader.get("url"));
    Utilities.fill(testContext.page, LoginPageObjects.USERNAME_INPUT, username);
    Utilities.click(testContext.page, LoginPageObjects.NEXT);
    Utilities.fill(testContext.page, LoginPageObjects.PASSWORD_INPUT, password);
    Utilities.click(testContext.page, LoginPageObjects.LOGIN_BUTTON);
    Utilities.waitForElement(testContext.page, LoginPageObjects.HOME_HEADER);
}
```

## Violation Example

```typescript
// BAD: Multiple unrelated scenarios in one test
test('pay statements page', async ({ page }) => {
  // Tests viewing, filtering, downloading, AND printing — four scenarios in one
  await page.goto('/pay-statements');
  await expect(page.getByText('Pay Statements')).toBeVisible();
  await page.getByLabel('Date range').selectOption('2025');
  await page.getByRole('button', { name: 'Download' }).click();
  await page.getByRole('button', { name: 'Print' }).click();
});
```

## Edge Cases

- Auth setup (`auth.setup.ts`) is NOT a feature test — it runs once as a dependency, not per-test
- Scenario Outlines in Cucumber are acceptable — they parameterize ONE scenario, not combine multiple
