---
skill:
  id: skill-cpp-resiliency-failure-modes
  name: "C++ Resiliency & Failure Mode Governance"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-7.1
      title: Reliability Law
    - id: ENG-7.4
      title: Graceful Degradation Law
  references:
    - id: ENG-6.1
      title: Security by Design Law (NON-NEGOTIABLE)
    - id: ENG-5.5
      title: Observability Law

triggers:
  phrases:
    - "C++ circuit breaker"
    - "C++ retry"
    - "C++ timeout"
    - "C++ resiliency"
    - "C++ failure handling"
    - "C++ bulkhead"

followed_by:
  - skill-cpp-exception-safety-governance
  - skill-27-constitution-compliance
---

# Skill: C++ Resiliency & Failure Mode Governance

## Purpose

Ensure C++ services degrade gracefully under partial failure. Per [ENG-7.1](laws/engineering/eng-7-reliability.md), systems must be reliable; per [ENG-7.4](laws/engineering/eng-7-reliability.md), critical paths must remain available when non-critical dependencies fail.

## Procedure

1. **Implement circuit breakers** — wrap calls to external systems (Sabre, ACARS, gate systems) with a circuit breaker that transitions through CLOSED → OPEN → HALF-OPEN states
2. **Use exponential backoff with jitter** — retry delays must follow `base * 2^attempt + random_jitter` to prevent thundering herd on shared dependencies
3. **Propagate timeout budgets** — pass a `std::chrono::steady_clock::time_point` deadline across service boundaries; each layer deducts its processing time before forwarding
4. **Isolate with bulkheads** — separate thread pools or connection pools for critical (booking, check-in) vs non-critical (analytics, recommendations) paths
5. **Govern health check endpoints** — expose `/healthz` (liveness) and `/readyz` (readiness) that verify downstream connectivity
6. **Define termination vs recovery** — call `std::terminate` only for irrecoverable corruption (double-free, invariant violation); all other failures must attempt recovery or graceful degradation

## Governance Gate

Per [ENG-7.4](laws/engineering/eng-7-reliability.md), any external service call without a circuit breaker and timeout is a **blocking violation**. Per [ENG-7.1](laws/engineering/eng-7-reliability.md), retry logic without backoff+jitter is rejected at review.

## Signal Handling for Crash Reporting

- Register handlers for SIGSEGV, SIGABRT, and SIGBUS to capture stack traces before termination
- Use `sigaltstack` to ensure the handler runs even on stack overflow
- Write crash reports to a pre-allocated buffer; do not allocate memory in signal handlers
