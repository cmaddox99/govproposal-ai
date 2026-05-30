---
avatar: avatar-tech-dss-event-driven
domain: DSS Event-Driven Microservices — DisplayHub · Display APIs · Web UIs
laws: [ENG-4.1, ENG-2.1, ENG-3.1, ENG-5.5, ENG-6.4, ENG-7.1]
---

# DSS Event-Driven Microservices — Guidance

> Governs AI agent behavior when building DisplayHub processors, Display APIs, and gate display Web UIs.
> Cardinal rule: processors write, APIs read, UIs render — no layer reaches backwards.
> A gate display must never go dark — fail open with stale data, never blank screen.

## Laws

| Law | Title | Example |
|-----|-------|---------|
| ENG-4.1 | Atomic TDD Law | `examples/ENG-4.1-atomic-tdd.md` |
| ENG-2.1 | Domain-Driven Design Law | `examples/ENG-2.1-ddd.md` |
| ENG-3.1 | Complexity Limits | `examples/ENG-3.1-complexity.md` |
| ENG-5.5 | Observability Law | `examples/ENG-5.5-observability.md` |
| ENG-6.4 | Data Protection Law | `examples/ENG-6.4-data-protection.md` |
| ENG-7.1 | Failure Handling Law | `examples/ENG-7.1-failure-handling.md` |

## Key Patterns

| Pattern | File |
|---------|------|
| Event processor idempotency key | `examples/ENG-7.1-failure-handling.md` |
| Bounded context event contracts | `examples/ENG-2.1-ddd.md` |
| Per-layer TDD (Node.js / Java / React) | `examples/ENG-4.1-atomic-tdd.md` |
| Staleness metric + PagerDuty alert | `examples/ENG-5.5-observability.md` |
