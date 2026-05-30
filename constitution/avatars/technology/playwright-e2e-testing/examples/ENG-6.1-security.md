---
avatar: avatar-playwright-e2e-testing
law: ENG-6.1
title: "Security by Design Law"
---

# ENG-6.1 — Security by Design: Playwright E2E Application

## What This Law Requires

Test credentials and auth state must be handled securely. Credentials come from environment variables only. Auth state files are `.gitignore`d. SSO login is automated via a setup project that runs once per test suite and supports both PingFederate and MSAL.

## Compliant Example

**TypeScript — AA SSO Authentication Setup (PingFederate + MSAL):**

```typescript
// tests/auth.setup.ts — authenticates once, detects auth mode, saves provider-specific state
import { test as setup } from '@playwright/test';
type AuthMode = 'pingfederate' | 'msal';

function resolveMode(host: string, forcedMode?: string): AuthMode {
  if (forcedMode === 'pingfederate' || forcedMode === 'msal') {
    return forcedMode;
  }
  if (host.includes('pfloginapp')) {
    return 'pingfederate';
  }
  if (host.includes('login.microsoftonline.com') || host.includes('loginb2e')) {
    return 'msal';
  }
  throw new Error(`Unsupported auth host: ${host}`);
}

setup('authenticate via AA SSO', async ({ page }) => {
  const forcedMode = process.env.AUTH_MODE; // auto | pingfederate | msal

  await page.goto('/');
  await page.waitForURL(
    url => {
      const host = url.hostname.toLowerCase();
      return (
        host.includes('pfloginapp') ||
        host.includes('login.microsoftonline.com') ||
        host.includes('loginb2e')
      );
    },
    { timeout: 30000 }
  );

  const authHost = new URL(page.url()).hostname.toLowerCase();
  const mode = resolveMode(authHost, forcedMode);
  const authFile = `playwright/.auth/${mode}.user.json`;
  const genericAuthFile = 'playwright/.auth/user.json';

  if (mode === 'pingfederate') {
    const usernameField = page.locator(
      'input[name="pf.username"], input[name="username"], input[type="text"]'
    ).first();
    await usernameField.fill(process.env.TEST_USER_ID!);
    await page.getByRole('button', { name: /next|sign in|continue/i }).first().click();
    await page.locator('input[type="password"]').fill(process.env.TEST_PASSWORD!);
    await page.locator('input[type="submit"], button[type="submit"]').first().click();
  } else {
    await page.locator('input[type="email"], input[name="loginfmt"]').first().fill(process.env.TEST_USER_ID!);
    await page.getByRole('button', { name: /next/i }).click();
    await page.locator('input[type="password"], input[name="passwd"]').first().fill(process.env.TEST_PASSWORD!);
    await page.getByRole('button', { name: /sign in/i }).click();
    const staySignedIn = page.getByRole('button', { name: /yes|no/i }).first();
    if (await staySignedIn.isVisible().catch(() => false)) {
      await staySignedIn.click();
    }
  }

  // Wait for redirect back to app
  await page.waitForURL(url => {
    const host = url.hostname.toLowerCase();
    return (
      !host.includes('pfloginapp') &&
      !host.includes('login.microsoftonline.com') &&
      !host.includes('loginb2e')
    );
  });

  await page.context().storageState({ path: authFile });
  await page.context().storageState({ path: genericAuthFile });
});
```

**playwright.config.ts — setup project + shared state:**

```typescript
projects: [
  { name: 'setup', testMatch: /auth\.setup\.ts/, timeout: 300_000 },
  {
    name: 'e2e',
    use: { storageState: 'playwright/.auth/user.json' },
    dependencies: ['setup'],
  },
]
```

**Environment Variables (required):**

```bash
TEST_USER_ID=<from secret store>
TEST_PASSWORD=<from secret store>
AUTH_MODE=auto # or pingfederate|msal
```

**.gitignore — REQUIRED entries:**

```
playwright/.auth/
.env.test.local
```

**Java — credentials from properties file (not committed):**

```java
// ConfigReader loads from environment-specific .properties
String username = ConfigReader.get("username");
String password = ConfigReader.get("password");
testContext.page.navigate(ConfigReader.get("url"));
```

## Violation Example

```typescript
// BAD: Hardcoded credentials
await page.fill('#username', 'test.user.361');
await page.fill('#password', 'P@ssw0rd123');

// BAD: Auth state committed to repo
// playwright/.auth/user.json checked into git
```

## Edge Cases

- `storageState` files contain session cookies — treat as secrets even in non-production environments
- SessionStorage is NOT persisted by `storageState`. Use `page.addInitScript()` to inject session flags like `epays3_tab_session` before page JavaScript runs
- Some apps route through `loginb2e` before/after `login.microsoftonline.com` in the same MSAL journey. Treat both hosts as the same auth mode
- For CI/CD, use GitHub Actions secrets for `TEST_USER_ID` and `TEST_PASSWORD`
