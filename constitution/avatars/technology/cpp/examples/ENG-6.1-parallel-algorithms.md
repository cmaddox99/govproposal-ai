---
law_id: ENG-6.1
cpp_version_min: 17
cpp_version_note: >-
  C++17 + parallel STL backend required (MSVC, libstdc++/TBB, libc++/OpenMP).
  For C++11/14 use std::async or manual thread pools.
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): Parallel Algorithms — `std::execution` (C++17)

Per [ENG-6.1](laws/engineering/eng-6-security.md), choose the weakest execution
policy that satisfies performance requirements. Wrong policies silently introduce
data races or mask non-determinism in tests.

## Execution Policy Reference

| Policy | Ordering | Threads | Vectorised | Use when |
|--------|----------|---------|-----------|---------|
| `seq` | In-order | Caller only | No | Tests, debugging |
| `par` | Unordered | Thread pool | No | CPU-bound, I/O-tolerant |
| `par_unseq` | Unordered | Thread pool | Yes (SIMD) | Pure math, no locks |

## COMPLIANT: `par_unseq` for Batch Fare Calculation

```cpp
#include <algorithm>
#include <execution>
#include <vector>

struct FlightFare { int base_usd; int adjusted_usd; };

// ✅ independent elements — no shared mutable state
void apply_surcharges(std::vector<FlightFare>& fares, float factor) {
    std::transform(
        std::execution::par_unseq,
        fares.begin(), fares.end(), fares.begin(),
        [factor](FlightFare f) {
            f.adjusted_usd = static_cast<int>(f.base_usd * factor);
            return f;  // ✅ value copy
        });
}
```

## COMPLIANT: `seq` for Tests, `par` for I/O Work

```cpp
// ✅ seq: deterministic — required for unit tests
std::sort(std::execution::seq, fares.begin(), fares.end(), by_price);

// ✅ par: thread pool, safe for blocking I/O
std::for_each(std::execution::par,
              segments.begin(), segments.end(),
              [](Segment& s) { s.load_availability(); });
```

## NON-COMPLIANT: Order Assumption with `par_unseq`

```cpp
int sequence = 0;
// ❌ no ordering guarantee — sequence++ is a data race (UB)
std::for_each(std::execution::par_unseq, fares.begin(), fares.end(),
              [&](FlightFare& f) {
                  f.adjusted_usd = sequence++ * f.base_usd; // ❌ data race
              });
```

## Edge Cases

### Exception Propagation

`par_unseq` calls `std::terminate` on any throw. `par`/`seq` rethrow the
first exception at the call site:

```cpp
try {
    std::for_each(std::execution::par, v.begin(), v.end(), risky_op);
} catch (const std::exception& e) { /* first exception */ }
```

### Shared Mutable State — Data Race

Writes to variables shared across iterations require atomics or a mutex even
with `par`. Prefer `std::transform` into a separate output range.

### `par_unseq` SIMD Alignment

SIMD throughput benefits from 32/64-byte aligned data. Misaligned
`std::vector` falls back to scalar. Use `alignas` or `std::aligned_alloc`
for SIMD paths.
