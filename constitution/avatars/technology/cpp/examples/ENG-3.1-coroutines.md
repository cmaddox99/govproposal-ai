---
law_id: ENG-3.1
cpp_version_min: 20
cpp_version_note: >-
  Uses C++20 coroutines (co_await/co_yield). Transitional/brownfield teams: use std::thread with callback or std::future instead.
avatar: cpp
---

# [ENG-3.1](laws/engineering/eng-3-code-quality.md): Complexity Limits — Coroutines

**Java equivalent:** Java's `CompletableFuture` is the closest analogy, but C++ coroutines are fundamentally different — they are compiler-transformed functions that can suspend and resume. The `promise_type` is the state machine that controls suspension. If you're new to C++, start with `std::async` + `std::future` instead.

## Critical Warning: Dangling References After `co_await`

After the first `co_await`, the coroutine frame may resume on a different thread. Reference parameters bound to the caller's stack are dangling. Take parameters **by value** (or `std::shared_ptr`) in coroutine signatures.

```cpp
Task<void> process(const std::string& pnr);  // ❌ UB: reference dangles after co_await
Task<void> process(std::string pnr);          // ✅ Safe: value copied into frame
```

## When to Use

- **I/O-bound concurrency** — flight search fan-out, DB queries, HTTP calls. Coroutines keep linear control flow without callback spaghetti.
- **Streaming pipelines** — PNR update processing where `co_yield` models the stream.

## When NOT to Use

- **CPU-bound work** — fare optimisation, crew scheduling. Use `std::jthread` + work-stealing pool.
- **Simple sequential code** — no suspension point means a coroutine just adds complexity.

## COMPLIANT: Structured Coroutine with Cancellation

```cpp
#include <coroutine>
#include <stop_token>
#include <vector>
#include <string>

struct FlightResult { std::string flight; int price; };

// Simplified task type (real impl uses library like cppcoro)
template<typename T> struct Task {
    struct promise_type {
        T value;
        Task get_return_object() { return {this}; }
        std::suspend_never initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        void return_value(T v) { value = std::move(v); }
        void unhandled_exception() { std::terminate(); }
    };
    promise_type* promise;
};

Task<std::vector<FlightResult>> search_flights(
    std::string origin, std::string dest, std::stop_token stop) {
    std::vector<FlightResult> results;
    for (auto& provider : get_providers()) {
        if (stop.stop_requested()) co_return results;  // cooperative cancel
        auto flights = co_await provider.query(origin, dest);
        results.insert(results.end(), flights.begin(), flights.end());
    }
    co_return results;
}
```

**Why compliant:** Structured ownership, cooperative cancellation via stop_token, linear control flow despite async.

## NON-COMPLIANT: Fire-and-Forget Lambda Coroutine

```cpp
void search_flights(std::string origin, std::string dest) {
    [=]() -> Task<void> {  // detached coroutine — who owns this?
        auto results = co_await query_all(origin, dest);
        cache.store(results);  // dangling ref if cache destroyed first
    }();  // launched and forgotten — no cancellation, no error handling
}
```

**Why non-compliant:** Detached coroutine has no owner, no cancellation, dangling reference risk.

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Coroutine frame heap-allocated per `co_await` in a tight loop | Hidden allocation cliff on hot paths | Profile first; use coroutine allocator customisation to pool frames |
| Coroutine destroyed before final suspend | Accessing the handle result is UB | Check `std::coroutine_handle::done()` before accessing the value |
| `co_await` inside a destructor-called function | Destructors cannot be coroutines; UB | Move async cleanup to an explicit `async_close()` method |
