---
avatar: avatar-tech-apigee-azure
domain: API Gateway + Cloud Infrastructure — Runway Self Service Portal · Microgateway · Azure App Service · AKS
laws: [ENG-4.1, ENG-3.1, ENG-6.1, ENG-6.4, ENG-6.7, ENG-5.2, ENG-7.1]
codebase_source: "AAInternal/apigeeDocs"
---

# Apigee + Azure — Guidance

> **Purpose:** Governs AI agent behavior when building or modifying Apigee API proxies and Azure cloud infrastructure at American Airlines. All proxy provisioning flows through the **Runway Self Service Portal** (`https://developer.aa.com/apigee/create`). Getting this layer wrong has TSA/CBP/DOT regulatory consequences.

## Laws

| Law | Title | Example |
|-----|-------|---------|
| ENG-4.1 | Atomic TDD Law | `examples/ENG-4.1-atomic-tdd.md` |
| ENG-3.1 | Complexity Limits | `examples/ENG-3.1-complexity.md` |
| ENG-6.1 | Security by Design Law | `examples/ENG-6.1-security-by-design.md` |
| ENG-6.4 | Data Protection Law | `examples/ENG-6.4-data-protection.md` |
| ENG-6.7 | Audit Trail Law | `examples/ENG-6.7-audit-trail.md` |
| ENG-5.2 | CI/CD Pipeline Law | `examples/ENG-5.2-cicd-pipeline.md` |
| ENG-7.1 | Failure Handling Law | `examples/ENG-7.1-failure-handling.md` |

## Overview

Apigee Edge Microgateway is AA's API security and routing perimeter. Every inbound request hits an Apigee proxy first. Azure provides compute (Functions / App Service / AKS), secrets (Key Vault), identity (AAD), and messaging (Service Bus). Getting this layer wrong has TSA/CBP/DOT regulatory consequences.

**Two deployment types:**
| Type | Use when | Target format |
|---|---|---|
| **Microgateway on AKS** | Securing apps in Kubernetes / KPaaS | `http://svcname.namespace.svc.cluster.local` |
| **Microgateway on Azure App Service** | Docker container behind VNET or public | `https://<appservice>.azure.webservices.net` |
| **Edge Gateway** | Contact `#topic-apigee` before use | — |

> Microgateway max capacity: **100 TPS per instance**. Microgateway does **not** perform BOT detection — front with Akamai for BOT protection and load balancing.

---

## Runway Provisioning Workflow (AA Standard)

All proxy and developer app lifecycle management goes through Runway:

1. **Create proxy** → Runway portal → select `Micro Gateway` → Runway scaffolds GitHub repo with CI/CD
2. **Deploy** → Commits to repo trigger GitHub Actions — **never upload bundles manually via Apigee UI**
3. **Promote to prod** → Runway `MANAGE API` → raises PR automatically; merge triggers pipeline
4. **Create developer app** → Runway → requires **HashiCorp Vault namespace** first; credentials auto-stored in Vault
5. **Approve app** → Runway approval portal (allow 15 min after creation)
6. **Prod change request** → ServiceNow Team Name required for all production deployments

**EDGEMICRO org names:** `aa-dev` / `aa-test` / `aa-stage` / `aa-prod`
**Docker image:** `docker.aa.com/prod/datamovement/apigee/edgemicro:3.3.8.0`

---

## Proxy Naming Conventions (AA-Required)

| Rule | Correct | Prohibited |
|---|---|---|
| No "edgemicro" in proxy name | `user-profile-v1` | `edgemicro-user-profile` ❌ |
| Specific base paths | `/api/user-service/v1` | `/api` ❌, `/` ❌ |
| K8s target | `http://svcname.namespace.svc.cluster.local` | Public IP directly ❌ |

---

## Security Grant Types

- **Client credentials** — all service-to-service (AA standard; only supported grant type currently)
- **API key** — only for SPAs where Akamai fronts for BOT protection and load balancing
- **Auth code** — planned for future B2E applications; not yet supported
- **BasicAuthentication** — **BLOCKED** by Apigee policy review; never use

---

## Non-Negotiable Laws

### ENG-4.1 — Atomic TDD Law
- Every Apigee proxy, Terraform module, and Azure Function has tests written before code.
- One proxy = one test file. Shared flow changes require tests in all consumer proxies.
- See: `examples/ENG-4.1-atomic-tdd.md`

### ENG-3.1 — Complexity Limits
- Proxy FlowCondition logic ≤3 conditions per flow; Functions ≤8 cyclomatic complexity.
- Business logic must NOT be embedded in Apigee AssignMessage policies.
- See: `examples/ENG-3.1-complexity.md`

### ENG-6.1 — Security by Design Law
- OAuthV2 VerifyAccessToken on every proxy PreFlow — no exceptions.
- Managed Identity for all Azure service-to-service calls; no client secrets in app settings.
- See: `examples/ENG-6.1-security-by-design.md`

### ENG-6.4 — Data Protection Law
- All runtime secrets via Azure Key Vault `@Microsoft.KeyVault(SecretUri=...)` reference syntax.
- Developer app client credentials stored in HashiCorp Vault — never hardcoded.
- No plaintext credentials in KVM, `.tfvars`, or app settings.
- See: `examples/ENG-6.4-data-protection.md`

### ENG-6.7 — Audit Trail Law
- MessageLogging policy on every proxy; `x-correlation-id` generated at Apigee edge and propagated.
- Never log request/response body, Authorization header value, or PII.
- See: `examples/ENG-6.7-audit-trail.md`

### ENG-5.2 — CI/CD Pipeline Law
- `apigeetool deploy` in CI only (Runway-scaffolded GitHub Actions); no manual bundle upload.
- `terraform apply` to prod gated by human approval in GitHub environment protection rules.
- Prod deploys require ServiceNow Change Request (Team Name required).
- See: `examples/ENG-5.2-cicd-pipeline.md`

### ENG-7.1 — Failure Handling Law
- FaultRules on all proxies with normalized error envelope (never expose stack trace).
- All target connections have explicit `io.timeout.millis` — never unbounded.
- Service Bus DLQ alert within 5 minutes; idempotency check for at-least-once delivery.
- See: `examples/ENG-7.1-failure-handling.md`

---

## Key Patterns

| Pattern | Where to find it |
|---|---|
| Runway proxy creation + naming | This file (Runway Provisioning Workflow) |
| Proxy bundle structure + shared flows | `examples/ENG-4.1-atomic-tdd.md` |
| HashiCorp Vault + Key Vault reference syntax | `examples/ENG-6.4-data-protection.md` |
| Correlation ID propagation | `examples/ENG-6.7-audit-trail.md` |
| Idempotent Service Bus Functions | `examples/ENG-7.1-failure-handling.md` |

---

## Anti-Patterns to Avoid

- **"edgemicro" in proxy name** — Runway rejects this; use descriptive API functionality name.
- **`/api` or `/` as base path** — not specific enough; use `/api/{service}/{version}`.
- **Manual bundle upload via Apigee UI** — bypasses CI and audit trail; always use Runway/GitHub Actions.
- **Client secrets in Azure app settings** — use `@Microsoft.KeyVault(SecretUri=...)` reference syntax.
- **Developer app credentials outside HashiCorp Vault** — credentials must be stored in Vault namespace.
- **`terraform apply` to prod from local machine** — prod applies must run through CI with human approval gate.
- **BOT detection in Microgateway** — Microgateway does not support BOT detection; use Akamai.
- **Deploying to prod without ServiceNow CR** — required for all production changes.
