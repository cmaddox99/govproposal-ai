---
domain: engineering
article: VII
title: Resiliency Laws
laws:
  - id: ENG-7.1
    title: Failure Handling Law
    summary: Systems SHALL handle failures gracefully - expect failure as normal
  - id: ENG-7.2
    title: Circuit Breaker Law
    summary: External dependencies SHALL be protected by circuit breakers
  - id: ENG-7.3
    title: Retry & Backoff Law
    summary: Transient failures SHALL be retried with exponential backoff and jitter
  - id: ENG-7.4
    title: Timeout Law
    summary: All I/O operations SHALL have timeouts - never wait forever
  - id: ENG-7.5
    title: Bulkhead Law
    summary: Critical resources SHALL be isolated to prevent cascade failures
  - id: ENG-7.6
    title: Idempotency Law
    summary: Operations SHALL be idempotent where possible
  - id: ENG-7.7
    title: Health Check Law
    summary: All services SHALL expose health checks (liveness, readiness, startup)
  - id: ENG-7.8
    title: Disaster Recovery Law
    summary: Systems SHALL have DR capabilities with defined RTO/RPO
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article VII: Resiliency Laws

## Section 7.1: Failure Handling Law

**Law ID:** `ENG-7.1`

Systems SHALL handle failures gracefully:

- Expect failure as normal (design for it)
- Fail fast on unrecoverable errors
- Degrade gracefully on partial failures
- Never fail silently (log and alert)

---

## Section 7.2: Circuit Breaker Law

**Law ID:** `ENG-7.2`

External dependencies SHALL be protected by circuit breakers:

```
States:
┌─────────┐    failures    ┌─────────┐
│ CLOSED  │───────────────→│  OPEN   │
│(normal) │                │(failing)│
└────┬────┘                └────┬────┘
     │                          │
     │   ←───────────────────   │
     │        timeout           │
     │                          │
     │                          ▼
     │                    ┌───────────┐
     │                    │HALF-OPEN  │
     └────────────────────│(testing)  │
           success        └───────────┘
```

### Required Parameters

- Failure threshold (e.g., 5 failures)
- Timeout duration (e.g., 30 seconds)
- Recovery attempts (e.g., 1 test call)

---

## Section 7.3: Retry & Backoff Law

**Law ID:** `ENG-7.3`

Transient failures SHALL be retried:

- Exponential backoff with jitter
- Maximum retry count (typically 3)
- Retry only on transient errors (not 4xx)
- Idempotent operations only

### Formula

```
delay = base * (2 ^ attempt) + random_jitter
```

---

## Section 7.4: Timeout Law

**Law ID:** `ENG-7.4`

All I/O operations SHALL have timeouts:

| Operation | Typical Timeout |
|-----------|-----------------|
| Database query | 5-30 seconds |
| HTTP API call | 10-30 seconds |
| Message queue | 30-60 seconds |
| File operations | 60 seconds |

**Never wait forever.**

---

## Section 7.5: Bulkhead Law

**Law ID:** `ENG-7.5`

Critical resources SHALL be isolated:

- Separate thread pools for different operations
- Separate connection pools for different services
- Rate limiting per tenant/user
- Failure in one area doesn't cascade to others

---

## Section 7.6: Idempotency Law

**Law ID:** `ENG-7.6`

Operations SHALL be idempotent where possible:

- Same request can be safely retried
- Use idempotency keys for mutations
- Track processed requests to prevent duplicates
- Design for "at least once" delivery

---

## Section 7.7: Health Check Law

**Law ID:** `ENG-7.7`

All services SHALL expose health checks:

- **Liveness:** Is the process running?
- **Readiness:** Can it handle requests?
- **Startup:** Has initialization completed?

Health checks verify dependencies (DB, cache, etc.)

---

## Section 7.8: Disaster Recovery Law

**Law ID:** `ENG-7.8`

Systems SHALL have DR capabilities:

| Metric | Target | Definition |
|--------|--------|------------|
| **RTO** | < 4 hours | Recovery Time Objective |
| **RPO** | < 1 hour | Recovery Point Objective |
| **Backup frequency** | Daily minimum | Regular backups |
| **Backup testing** | Quarterly | Verify restore works |
