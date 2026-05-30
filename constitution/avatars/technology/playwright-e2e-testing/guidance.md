# Playwright E2E/UI Testing Guidance

> **Purpose:** Agent guidance for Playwright-based E2E and UI testing of web applications at AA.

---

## Overview

Playwright enables cross-browser E2E testing (real API + database) and UI testing (mocked API) for TypeScript, Java, and Python. At AA, SSO may use either PingFederate (`pfloginapp-stage.cloud.aa.com`) or MSAL/Azure AD (`login.microsoftonline.com` and `loginb2e`).

## Non-Negotiable Laws

### ENG-4.1 — Atomic TDD Law
- **Requirement:** Each E2E test covers one user scenario. Write the failing test, implement the feature, then pass.
- **Violation:** Tests that combine multiple unrelated assertions or test multiple user flows.
- **Note:** Use Playwright's setup project pattern to isolate auth from feature tests.

### ENG-4.2 — Test Pyramid Law
- **Requirement:** E2E tests are the smallest layer. Prefer unit tests for logic, UI-mocked tests for rendering, E2E only for critical user journeys.
- **Violation:** Writing E2E tests for logic that can be unit tested.

### ENG-3.1 — Complexity Limits
- **Requirement:** No test file > 300 LOC. No page object > 200 LOC. Extract helpers for repeated patterns.
- **Violation:** God test files or monolithic page objects.

### ENG-6.1 — Security by Design
- **Requirement:** Test credentials in environment variables only. Auth state files (`playwright/.auth/`) in `.gitignore`. Never commit secrets.
- **Violation:** Hardcoded passwords, committed `.auth/` directory.

## Key Patterns

- **AA SSO Auth with mode detection:** Use setup projects (TS) or `@Before` hooks (Java) to authenticate once, save `storageState`, and reuse across tests. Detect auth mode from redirect host unless explicitly pinned. See `examples/ENG-6.1-security.md`.
- **Auth mode config:** Support `AUTH_MODE=auto|pingfederate|msal`.
- `AUTH_MODE=auto`: detect by first auth redirect host
- `AUTH_MODE=pingfederate`: force PingFederate flow (hosts matching `pfloginapp`)
- `AUTH_MODE=msal`: force MSAL flow (hosts matching `login.microsoftonline.com` or `loginb2e`)
- **Playwright setup state by mode:** Persist separate states per mode (for example `playwright/.auth/pingfederate.user.json` and `playwright/.auth/msal.user.json`) to avoid cross-provider cookie contamination.
- **SessionStorage injection:** Playwright restores cookies/localStorage but NOT sessionStorage. Use `page.addInitScript()` to inject required session flags before page JS runs.
- **Agent tooling:** Prefer `playwright-cli` for AI-assisted E2E testing (token-efficient). Use `state-save`/`state-load` for auth state.

## Authentication Mode Detection (Recommended)

Use a single auth setup that resolves provider at runtime:

1. Navigate to the app entry URL.
2. Wait for redirect to an external auth host.
3. Resolve mode based on host (`pfloginapp` => PingFederate, `login.microsoftonline.com` or `loginb2e` => MSAL).
4. Execute provider-specific selectors and submit steps.
5. Save provider-specific `storageState` file.

Prefer explicit override in CI when app behavior is known (`AUTH_MODE=msal` or `AUTH_MODE=pingfederate`) and keep `auto` as the local default.

## Anti-Patterns to Avoid

- **Re-authenticating per test** — use setup project + `storageState` persistence
- **Credentials in code** — always use env vars (`TEST_USER_ID`, `TEST_PASSWORD`)
- **Single hardcoded IdP assumption** — do not assume every AA app uses `pfloginapp`; support MSAL hosts as first-class flows
- **Ignoring sessionStorage gap** — apps checking session flags will break without `addInitScript()` injection
