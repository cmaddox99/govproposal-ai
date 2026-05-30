---
cpp_version_min: 20
cpp_version_note: >-
  C++20 only: co_await, co_yield, co_return require C++20 coroutines support.
avatar: cpp
---

# C++ Avatar Reference: Coroutines (C++20+)

> ★ **C++20+ only.** For C++11/14/17 teams use `std::async` + `std::future` or
> `std::thread` with `std::condition_variable`. See
> [ref-concurrency-threading.md](../safety/ref-concurrency-threading.md).

---

## Coroutines

C++20 coroutines (`co_await`, `co_yield`, `co_return`) enable structured asynchronous
programming. Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), coroutine usage
must be governed to prevent complexity growth.

> 💡 **Simpler alternative:** If you're coming from Java's `CompletableFuture`, start with
> `std::async` + `std::future` — it's simpler and sufficient for most async patterns. Only
> adopt coroutines when you need cooperative multitasking, lazy generators, or async I/O
> with thousands of concurrent operations. See
> [skill-cpp-code-simplification](agent-skills/skills-by-domain/platform-engineering/skill-cpp-code-simplification.md)
> for guidance.

### When to Use Coroutines

| Use Case | Appropriate | Alternative |
|----------|-------------|-------------|
| Async I/O (network, file) | ✅ Yes | `std::async` (simpler but less control) |
| Generator/lazy sequences | ✅ Yes | Iterator pattern |
| Parallel computation | ❌ No — use `std::jthread` + `std::atomic` | Thread pool |
| Simple request-response | ❌ Overkill | Direct function call |

### Coroutine Governance Rules

1. **Thread affinity** — document which executor/scheduler the coroutine resumes on. Coroutines that resume on arbitrary threads must be thread-safe.
2. **Cancellation** — every coroutine must support cooperative cancellation via `std::stop_token` or equivalent. Fire-and-forget coroutines are prohibited in production code.
3. **Exception propagation** — exceptions in `co_await`-ed operations must be caught at the coroutine boundary and translated to the caller's error model.
4. **Testing** — coroutine-based code must be testable with GoogleTest. Use synchronous executors in tests to avoid non-deterministic scheduling.

```cpp
// COMPLIANT — coroutine with cancellation support
Task<FlightResult> search_flights(
    SearchCriteria criteria,
    std::stop_token stop) {
    if (stop.stop_requested()) co_return FlightResult::cancelled();
    auto availability = co_await check_availability(criteria);
    if (stop.stop_requested()) co_return FlightResult::cancelled();
    co_return FlightResult::success(availability);
}
```

### Anti-Pattern: Fire-and-Forget Coroutine

```cpp
// NON-COMPLIANT — no cancellation, no error handling, no caller control
void launch_search(SearchCriteria c) {
    [](SearchCriteria c) -> Task<void> {
        co_await do_search(c);  // exception lost, no cancellation
    }(c);
}
```

### Coroutine Lifetime Traps

> ⚠️ **Advanced:** Coroutine frames are heap-allocated and outlive the creating scope.
> References captured at coroutine creation may dangle when the coroutine resumes on a
> different thread or after a `co_await`.

```cpp
// NON-COMPLIANT — reference parameter dangles after first co_await
Task<void> process(const FlightPlan& plan) {  // ❌ reference!
    co_await validate(plan);     // suspends here
    co_await submit(plan);       // ❌ plan may be destroyed — caller returned
}

// COMPLIANT — pass by value into coroutines
Task<void> process(FlightPlan plan) {  // ✅ copied into coroutine frame
    co_await validate(plan);
    co_await submit(plan);       // ✅ plan lives in coroutine frame
}

// NON-COMPLIANT — temporary lifetime trap
Task<void> search(std::string origin) {
    auto result = co_await fetch(std::string_view{origin});  // ✅ OK
    co_await fetch(std::string_view{"AADFW"});               // ❌ string_view to temporary
}
```

**Coroutine safety rules:**
- **Never** take reference parameters in coroutines — always pass by value or `shared_ptr`
- **Never** capture `this` in a coroutine lambda — the object may be destroyed before the coroutine completes
- Avoid `std::string_view` and `std::span` in coroutine parameters — the underlying data may not outlive the coroutine frame
- **Symmetric transfer** (`co_await` returning another coroutine) avoids stack overflow but can cause unbounded chains — limit chain depth in production

---

## See Also

- [ref-concurrency-threading.md](../safety/ref-concurrency-threading.md) — mutex, atomic, exception safety, termination (C++11+)
- [ref-concurrency-async.md](../safety/ref-concurrency-async.md) — circuit breaker, retry, bulkhead, timeout (C++17+)
