---
law_id: ENG-3.1
cpp_version_min: 17
cpp_version_note: >-
  Uses C++17 PMR polymorphic allocators (std::pmr::). Transitional teams: use custom allocator template parameter or pool allocator wrapper.
avatar: cpp
---

# [ENG-3.1](laws/engineering/eng-3-code-quality.md): Complexity Limits — PMR Allocators

## The Rule

Prefer `std::pmr` allocators over custom `operator new`/`delete` overloads. PMR provides a standard, composable allocation interface that is testable and interchangeable — custom global allocators are not.

**Java equivalent:** PMR is like writing your own garbage collector for a specific allocation pattern. You almost never need this — use the default allocator unless profiling proves it's a bottleneck.

## When to Use

- **Request-scoped memory in high-throughput services** — e.g., fare calculation called 1000×/request. A `monotonic_buffer_resource` on the stack eliminates per-call heap traffic.
- **Latency-sensitive paths** — gate assignment solvers, real-time crew tracking where p99 jitter from `malloc` is unacceptable.
- **NOT for long-lived objects** — PMR monotonic buffers only grow; use them for short-lived, scoped work.

## COMPLIANT: Monotonic Buffer for Hot-Path Fare Calculation

```cpp
#include <memory_resource>
#include <vector>

struct FareComponent { int base; int tax; int surcharge; };

// Hot path: called per search result (~1000x per request)
int calculate_total_fare(std::span<const FareComponent> components) {
    alignas(alignof(FareComponent)) std::byte buf[4096];
    std::pmr::monotonic_buffer_resource pool(buf, sizeof(buf));
    std::pmr::vector<int> subtotals(&pool);
    subtotals.reserve(components.size());

    for (const auto& fc : components) {
        subtotals.push_back(fc.base + fc.tax + fc.surcharge);
    }
    int total = 0;
    for (auto s : subtotals) total += s;
    return total;
    // pool destroyed here — single dealloc, zero fragmentation
}
// Profiling: 3.2x throughput vs default allocator at p99 under load
```

**Why compliant:** Stack-backed arena avoids heap fragmentation on hot path. Justified by profiling data per [ENG-3.1](laws/engineering/eng-3-code-quality.md).

## NON-COMPLIANT: Default Allocator in Tight Loop

```cpp
int calculate_total_fare(std::span<const FareComponent> components) {
    std::vector<int> subtotals;  // heap alloc per call
    for (const auto& fc : components) {
        subtotals.push_back(fc.base + fc.tax + fc.surcharge);  // realloc + fragment
    }
    return std::accumulate(subtotals.begin(), subtotals.end(), 0);
}
// 1000 calls = 1000 heap allocs + deallocations = fragmentation + cache misses
```

**Why non-compliant:** Repeated heap allocation on hot path causes fragmentation and unpredictable latency spikes.

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| `monotonic_buffer_resource` backed by heap grows unbounded | Memory never returned to OS until destruction | Size stack buffer conservatively; set a hard upstream limit |
| Sharing a PMR resource across threads | `monotonic_buffer_resource` is not thread-safe | One resource per thread or request; never share across thread boundaries |
| Container copy propagates upstream allocator unexpectedly | `std::pmr::vector` copy uses destination allocator (POCCA=false) | Document propagation policy; use `assign` when destination allocator must be preserved |
