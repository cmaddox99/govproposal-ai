---
skill:
  id: skill-cpp-concurrency-thread-safety-governance
  name: "C++ Concurrency & Thread Safety Governance"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-6.1
      title: Security by Design Law (NON-NEGOTIABLE)
    - id: ENG-7.1
      title: Reliability Law
  references:
    - id: ENG-4.1
      title: Atomic TDD Law (NON-NEGOTIABLE)
    - id: ENG-5.2
      title: Build & Deploy Law

triggers:
  phrases:
    - "C++ thread safety"
    - "C++ concurrency"
    - "C++ data race"
    - "C++ mutex"
    - "C++ atomic"
    - "C++ lock-free"

followed_by:
  - skill-cpp-sanitizer-hardening
  - skill-27-constitution-compliance
---

# Skill: C++ Concurrency & Thread Safety Governance

## Purpose

Prevent data races, deadlocks, and undefined behavior in concurrent C++ code. Per [ENG-6.1](laws/engineering/eng-6-security.md), thread safety is a security design constraint; per [ENG-7.1](laws/engineering/eng-7-reliability.md), concurrency bugs are reliability failures.

## Procedure

1. **Enforce lock hierarchy** — assign a numeric level to every mutex; always acquire in ascending order. Document the hierarchy in the module header
2. **Mandate RAII synchronization** — use `std::scoped_lock` (multi-lock) or `std::lock_guard` (single-lock). Raw `lock()`/`unlock()` calls are a blocking violation
3. **Govern atomic memory ordering** — default to `memory_order_seq_cst`; weaker orderings (`acquire`/`release`, `relaxed`) require profiling evidence and code-review approval
4. **Use cooperative cancellation** — prefer `std::jthread` with `std::stop_source`/`std::stop_token` over manual thread shutdown flags
5. **Gate lock-free data structures** — lock-free implementations require a formal correctness proof and benchmark comparison against the locked alternative
6. **Require ThreadSanitizer (TSan)** — TSan must be enabled as a mandatory CI gate for any target that spawns threads or uses atomics
7. **Handle condition variable spurious wakeups** — every `wait()` call must use the predicate overload or a while-loop guard

## Governance Gate

Per [ENG-6.1](laws/engineering/eng-6-security.md), a raw `mutex.lock()`/`mutex.unlock()` pair or a missing TSan CI gate is a **blocking violation**. Per [ENG-7.1](laws/engineering/eng-7-reliability.md), any data race detected by TSan must be resolved before merge.

## Deadlock Prevention Checklist

- [ ] All mutexes assigned a hierarchy level
- [ ] No nested lock acquisitions violate the hierarchy
- [ ] `std::scoped_lock` used when acquiring multiple locks
- [ ] No lock held across blocking I/O or unbounded waits

## Legacy Standard Support

### C++11/14/17 Alternatives
- **std::thread** (C++11): Use instead of std::jthread; requires manual join/detach via RAII guard
- **std::atomic<bool>** (C++11): Use for stop signaling instead of std::stop_token
- **std::lock_guard** (C++11): Use instead of std::scoped_lock (single mutex only)
- **std::condition_variable** (C++11): Use for thread coordination
- **std::async** (C++11): Use for simple fire-and-forget tasks; avoid for complex async

### Pre-C++11 Threading
For C++98/03 codebases still using POSIX threads or Win32 threading:
- Wrap `pthread_mutex_t` in RAII class before any other modernization
- Migrate to `std::thread`/`std::mutex` only after upgrading to C++11
- Document all synchronization points in comments until proper C++11 primitives available
