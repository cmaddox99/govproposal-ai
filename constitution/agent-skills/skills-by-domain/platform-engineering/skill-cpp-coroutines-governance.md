---
skill:
  id: skill-cpp-coroutines-governance
  name: "C++ Coroutines Governance"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-3.1
      title: Complexity Limits Law
    - id: ENG-6.1
      title: Security by Design Law (NON-NEGOTIABLE)
  references:
    - id: ENG-4.1
      title: Atomic TDD Law

triggers:
  phrases:
    - "C++ coroutines"
    - "C++ co_await"
    - "C++ async pattern"
    - "C++ structured concurrency"
    - "C++ generator"

followed_by:
  - skill-cpp-exception-safety-governance
  - skill-08-code-review
---

# Skill: C++ Coroutines Governance

## Purpose

Govern C++20 coroutine usage to prevent unstructured async patterns, resource leaks, and non-deterministic test failures. Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), coroutine complexity must be bounded.

## Procedure

1. **Validate use case** — coroutines are appropriate for async I/O and generators; not for simple request-response or parallel computation
2. **Require cancellation support** — every coroutine must accept `std::stop_token` or equivalent. Fire-and-forget coroutines are prohibited
3. **Document thread affinity** — specify which executor/scheduler the coroutine resumes on; coroutines resuming on arbitrary threads must be thread-safe
4. **Enforce exception boundaries** — exceptions in `co_await`-ed operations must be caught and translated at the coroutine boundary
5. **Test with synchronous executors** — use deterministic test executors in GoogleTest to avoid scheduling non-determinism

## Governance Gate

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md) and [ENG-6.1](laws/engineering/eng-6-security.md), a fire-and-forget coroutine (no cancellation, no error propagation) is a **blocking violation**. Coroutines without documented thread affinity are incomplete.

## C++ Specific Patterns

- Use `co_await` for I/O-bound operations; prefer `std::jthread` for CPU-bound parallelism
- Implement `Task<T>` or use a library type (cppcoro, folly::coro) — do not hand-roll promise types
- Check `stop_token.stop_requested()` at suspension points for cooperative cancellation
- Return `co_return` with error type rather than throwing across coroutine boundaries
