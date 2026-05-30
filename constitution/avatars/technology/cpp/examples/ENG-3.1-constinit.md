---
id: ENG-3.1-constinit
law_id: ENG-3.1
avatar: cpp
title: constinit — Compile-Time Initialization Guarantee
cpp_version_min: "20"
tags: [constinit, static-init, thread-safety, initialization-order]
---

# `constinit` — ENG-3.1

Per [ENG-3.1](../../../laws/engineering/eng-3-code-quality.md), use `constinit`
on global/static variables to guarantee compile-time initialization and prevent
the **static initialization order fiasco**.

## COMPLIANT

```cpp
#include <atomic>

// constinit atomic: compile-time zero-init + thread-safe increment
// ✅ constinit guarantees init before first use across TUs; std::atomic gives thread safety
constinit std::atomic<int> active_flights{0};

// Thread-local with constinit: each thread starts at 0, guaranteed compile-time
constinit thread_local int thread_flight_cache = 0;

void record_departure() {
    active_flights.fetch_add(1, std::memory_order_relaxed);
    ++thread_flight_cache;  // thread-local: no data race
}
```

> **Note:** A plain `constinit int` does NOT provide thread safety. If the variable is
> written concurrently, use `std::atomic<int>` as shown above. `constinit` only
> guarantees **when** initialization happens (compile-time), not **how** mutation is
> synchronised.

## NON-COMPLIANT

```cpp
// Dynamic init: value depends on another TU's static — order is undefined across TUs
// In any other TU that links against this, get_base_count() may not yet be initialised
extern int get_base_count();                    // defined in another TU
static int flight_counter = get_base_count();  // ❌ dynamic init — order undefined across TUs
```

## Edge Cases & Warnings

| Scenario | Risk | Mitigation |
|----------|------|------------|
| Non-trivial type | `constinit` requires constant-initialization (constexpr constructor or trivial type) | Ensure the type has a `constexpr` constructor |
| `constinit` ≠ `constexpr` | Value CAN be modified at runtime | Use `const` or `constexpr` if immutability needed |
| `thread_local constinit` | Per-thread init is compile-time; destructor still runs | Safe for trivial types; add noexcept dtor for others |
| ODR across TUs | Two TUs defining same `constinit` name → linker error | Declare `extern constinit` in header; define once |
