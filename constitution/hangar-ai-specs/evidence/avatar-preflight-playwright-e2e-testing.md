# Avatar Pre-flight Evidence — Playwright E2E Testing

**Date:** 2026-05-01
**Author:** Copilot (AI-assisted)
**Mode:** Generate (Mode 1)

---

## Step 0.1 — Intent Classification

| Field | Value |
|-------|-------|
| **Intent** | Create a technology avatar for Playwright E2E/UI testing |
| **Inferred Mode** | Generate → technology |
| **Avatar Type** | `technology` |
| **Domain Slug** | `playwright-e2e-testing` |
| **Path** | `avatars/technology/playwright-e2e-testing/` |

## Step 0.2 — Deduplication Check

| Existing Avatar | Overlap Score | Reasoning |
|----------------|---------------|-----------|
| `react-typescript` | ~15% | Mentions Playwright in stack.testing but focuses on React component dev, not E2E testing patterns |
| `java-spring` | ~5% | Java stack overlap only; no E2E testing focus |
| `nodejs-typescript` | ~10% | TypeScript language overlap; focuses on Express BFF, not testing |
| `angular` | ~5% | Mentions Jasmine/Karma testing; no Playwright content |

**Result:** All scores < 40%. ✅ PROCEED — no semantic overlap with existing avatars.

## Step 0.3 — Law Boundary Acknowledgement

This avatar is `type: technology`. It may only specialize `ENG-*` laws. `PRD-*` and `BUS-*` laws are FORBIDDEN in this avatar. Product and compliance concerns belong in product-type or industry avatars that compose with this one.

**Acknowledged:** ✅

## Step 0.4 — 5 Canonical RAG Query Patterns

| # | Query | Expected Files |
|---|-------|----------------|
| Q1 | "How do I write an E2E test with Playwright?" | `examples/ENG-4.1-atomic-tdd.md` |
| Q2 | "When should I write E2E vs unit vs UI-mocked tests?" | `examples/ENG-4.2-test-pyramid.md` |
| Q3 | "What are the non-negotiable rules for Playwright E2E testing?" | `guidance.md` |
| Q4 | "What is the project structure for a Playwright test suite?" | `manifest.yaml` |
| Q5 | "How do I handle AA SSO authentication in Playwright tests?" | `guidance.md` + `examples/ENG-6.1-security.md` |

## Reference Codebases

| Repo | Language | Key Patterns |
|------|----------|-------------|
| `AAInternal/epays3-ui` | TypeScript | Setup project auth, storageState, sessionStorage injection, mobile+desktop configs |
| `AAInternal/hangar-playwright-auth` | TypeScript | Reusable auth library, createAuthSetup(), multi-selector PingFederate handling |
| `AAInternal/OSP-Automation` | Java | Maven+Playwright+Cucumber+TestNG, PlaywrightFactory, Page Object Model, LoginPageObjects |
