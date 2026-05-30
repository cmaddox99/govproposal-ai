---
avatar: avatar-playwright-e2e-testing
law: ENG-4.2
title: "Test Pyramid Law"
---

# ENG-4.2 — Test Pyramid: Playwright E2E Application

## What This Law Requires

Tests must follow the pyramid distribution. E2E tests (top of pyramid) are the fewest, reserved for critical user journeys. UI-mocked tests cover rendering with mocked APIs. Unit tests cover business logic.

## Compliant Example

**Test Pyramid for a Web Application:**

| Layer | Tool | Scope | Ratio |
|-------|------|-------|-------|
| **Unit** | Jest / JUnit / pytest | Business logic, utilities, hooks | ~70% |
| **UI-mocked** | Playwright + MSW / route mocking | Component rendering with mocked API | ~20% |
| **E2E** | Playwright (real API + database) | Critical user journeys only | ~10% |

**When to write E2E (real API):**
- Login flow through SSO
- End-to-end form submission that writes to database
- Multi-page workflows (e.g., W-4 form → submission → confirmation)

**When to write UI-mocked (mocked API):**
- Page renders correct data shapes
- Error states display correctly
- Loading/empty states

**TypeScript — Mocked API test using Playwright route interception:**

```typescript
test('shows error when API fails', async ({ page }) => {
  await page.route('**/api/pay-statements', route =>
    route.fulfill({ status: 500, body: 'Internal Server Error' })
  );
  await page.goto('/pay-statements');
  await expect(page.getByText('Unable to load')).toBeVisible();
});
```

## Violation Example

```typescript
// BAD: E2E test for something that should be a unit test
test('formats currency correctly', async ({ page }) => {
  await page.goto('/pay-statements');
  const amount = await page.getByTestId('net-pay').textContent();
  expect(amount).toBe('$1,234.56'); // This is a unit test for formatCurrency()
});
```

## Edge Cases

- Auth setup tests don't count toward the pyramid — they are infrastructure
- Visual regression tests (`toHaveScreenshot`) sit between UI-mocked and E2E
