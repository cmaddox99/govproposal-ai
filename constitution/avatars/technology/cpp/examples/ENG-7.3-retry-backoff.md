---
law_id: ENG-7.3
cpp_version_min: 11
avatar: cpp
---

# Retry with Exponential Backoff — C++ Implementation

Per [ENG-7.3](laws/engineering/eng-7-reliability.md), transient failures must be retried with exponential backoff and jitter.

## COMPLIANT — Backoff with jitter prevents thundering herd

**Note:** `thread_local` is C++'s equivalent of Java's `ThreadLocal<T>`. The jitter calculation adds randomness to prevent thundering herd.

```cpp
#include <chrono>
#include <random>
#include <thread>

// Retry with exponential backoff + jitter
// Only catches TransientException — permanent errors propagate immediately
template <typename Func>
auto retry_with_backoff(
    Func&& fn,
    int max_retries = 3,
    std::chrono::milliseconds base_delay = std::chrono::milliseconds{100})
    -> decltype(fn())
{
    static thread_local std::mt19937 rng{std::random_device{}()};

    for (int attempt = 0;; ++attempt) {
        try {
            return fn();
        } catch (const TransientException& e) {
            if (attempt >= max_retries) throw;

            // Exponential: 100ms, 200ms, 400ms, 800ms...
            auto delay = base_delay * (1 << attempt);
            // Jitter: random 0 to 50% of delay
            auto jitter = std::chrono::milliseconds{
                std::uniform_int_distribution<int>{
                    0, static_cast<int>(delay.count() / 2)}(rng)
            };

            log::info("Retry attempt {}/{} after {}ms",
                      attempt + 1, max_retries,
                      (delay + jitter).count());
            std::this_thread::sleep_for(delay + jitter);
        }
        // Non-transient exceptions propagate immediately (no retry)
    }
}
```

## NON-COMPLIANT — Fixed delay retry

```cpp
// ❌ All clients retry at the same time → thundering herd
for (int i = 0; i < 3; ++i) {
    try { return fetch(url); }
    catch (...) { std::this_thread::sleep_for(std::chrono::seconds{1}); }
}
```

## Key Rules

| Rule | Rationale |
|------|-----------|
| Exponential backoff (not fixed) | Prevents synchronized retry storms |
| Add random jitter | Spreads retries across time window |
| Only retry transient errors | Auth/validation failures should not retry |
| Configurable max retries + base delay | Tune per dependency SLA |
| Log each attempt per [ENG-6.7](laws/engineering/eng-6-security.md) | Audit trail for retry behavior |
| Cap maximum delay (e.g., 30s) | Prevent unbounded backoff |

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Retry on a non-idempotent operation causes duplicate side-effects | POST request that creates a booking retried after a timeout — two bookings are created | Classify each operation as idempotent or not at the API boundary; non-idempotent calls must not be retried without idempotency keys |
| Jitter implementation using non-thread-safe `std::rand()` | `std::rand()` has a global state; concurrent threads produce identical jitter values, causing thundering herd | Use a thread-local `std::mt19937` seeded with `std::random_device`; one instance per thread |
| Retry loop masks a persistent configuration error | Wrong endpoint URL causes all retries to fail; 3 retries × 5 s = 15 s delay before the caller discovers the misconfiguration | Distinguish transient errors (timeout, 503) from persistent errors (404, 400, auth fail); never retry on persistent errors |
