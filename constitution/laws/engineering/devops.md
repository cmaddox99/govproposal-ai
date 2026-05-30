---
domain: engineering
article: V
title: DevOps Laws
laws:
  - id: ENG-5.1
    title: Infrastructure as Code Law
    summary: ALL infrastructure SHALL be defined in code, version controlled, and reproducible
  - id: ENG-5.2
    title: CI/CD Pipeline Law
    summary: ALL deployments SHALL go through automated pipelines with no manual deployments to production
  - id: ENG-5.3
    title: Environment Parity Law
    summary: All environments SHALL be as similar as possible
  - id: ENG-5.4
    title: Git Workflow Law
    summary: Code changes SHALL follow standard branching strategy and commit message format
  - id: ENG-5.5
    title: Observability Law
    summary: All systems SHALL implement the three pillars (Logs, Metrics, Traces)
  - id: ENG-5.6
    title: Configuration Management Law
    summary: Configuration SHALL be externalized with secrets stored in vault/secret manager
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article V: DevOps Laws

## Section 5.1: Infrastructure as Code Law

**Law ID:** `ENG-5.1`

ALL infrastructure SHALL be defined in code:

- Version controlled alongside application code
- Reproducible across environments
- No manual infrastructure changes in production
- Drift detection enabled

### Tool Selection

Tool selection per technology avatar. All tools must support version control, reproducibility, and drift detection.

---

## Section 5.2: CI/CD Pipeline Law

**Law ID:** `ENG-5.2`

ALL deployments SHALL go through automated pipelines:

```
Commit → Build → Test → Security → Quality → Deploy → Verify
   │       │       │        │         │        │        │
   │       │       │        │         │        │        └─ Smoke tests
   │       │       │        │         │        └─ Blue/Green or Canary
   │       │       │        │         └─ Code quality gates
   │       │       │        └─ SAST, dependency scan
   │       │       └─ Unit, Integration, Contract
   │       └─ Compile, package
   └─ Trigger pipeline
```

### PROHIBITED

- Manual deployments to production
- Skipping quality gates ("emergency bypass")
- Deploying without tests passing

---

## Section 5.3: Environment Parity Law

**Law ID:** `ENG-5.3`

All environments SHALL be as similar as possible:

| Environment | Purpose | Data |
|-------------|---------|------|
| **Local** | Developer workstation | Synthetic/seeded |
| **Dev** | Integration testing | Synthetic |
| **UAT/Staging** | Pre-production validation | Anonymized production-like |
| **Production** | Live system | Real |

Configuration differences via environment variables only.

---

## Section 5.4: Git Workflow Law

**Law ID:** `ENG-5.4`

### Branching Strategy

```
main (production-ready)
  │
  ├── feature/TICKET-123-add-feature
  ├── fix/TICKET-456-fix-bug
  ├── refactor/TICKET-789-improve-code
  └── hotfix/TICKET-000-critical-fix
```

### Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`

### Rules

- Feature branches from main
- Squash merge to main (clean history)
- Delete branches after merge
- No direct commits to main (PRs required)

---

## Section 5.5: Observability Law

**Law ID:** `ENG-5.5`

All systems SHALL implement the three pillars:

1. **Logs** - Structured, centralized, searchable
2. **Metrics** - Business and technical KPIs
3. **Traces** - Distributed request tracing

### Required Metrics

- Request rate, error rate, duration (RED)
- Saturation (queue depths, resource usage)
- Business metrics (orders, payments, etc.)

---

## Section 5.6: Configuration Management Law

**Law ID:** `ENG-5.6`

Configuration SHALL be:

- Externalized (not hardcoded)
- Environment-specific via env vars or config service
- Secrets stored in vault/secret manager (never in code)
- Validated at startup (fail fast on bad config)
