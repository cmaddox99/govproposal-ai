---
avatar: avatar-playwright-e2e-testing
law: ENG-6.7
title: "Audit Trail Law"
---

# ENG-6.7 — Audit Trail: Playwright E2E Application

## What This Law Requires

E2E test runs must produce traceable artifacts: which tests ran, pass/fail status, environment, timestamps, and failure evidence. CI/CD pipelines must retain test reports for audit review.

## Compliant Example

**Playwright config — reporting and tracing:**

```typescript
// playwright.config.ts
export default defineConfig({
  reporter: [
    ['html', { open: 'never' }],           // HTML report for humans
    ['json', { outputFile: 'test-results/results.json' }], // machine-readable
    ['junit', { outputFile: 'test-results/junit.xml' }],   // CI/CD integration
  ],
  use: {
    trace: 'retain-on-failure', // Playwright trace for debugging failures
    screenshot: 'only-on-failure',
  },
});
```

**Java — ExtentReports + Allure for audit trail:**

```java
// Hooks.java — step-level logging with screenshots
@After
public void afterScenario(Scenario scenario) {
    if (scenario.getStatus().toString().equalsIgnoreCase("passed")) {
        tl.logPass("TEST PASSED", scenarioThread.page);
    } else {
        tl.logFailure("TEST FAILED", scenarioThread.page);
    }
    tl.flush(); // persist report to disk
}
```

**CI/CD — artifact upload (GitHub Actions):**

```yaml
- uses: actions/upload-artifact@v4
  if: always()
  with:
    name: playwright-report
    path: |
      playwright-report/
      test-results/
    retention-days: 30
```

## Violation Example

```typescript
// BAD: No reporter configured — results lost after run
export default defineConfig({
  reporter: [], // silent — no audit trail
});

// BAD: Empty catch blocks suppress failure evidence
afterEach(() => { try { /* cleanup */ } catch {} });
```

## Edge Cases

- Trace files can be large (10+ MB) — configure retention policies in CI
- For Cucumber (Java), ensure JSON output is enabled for pipeline integration
