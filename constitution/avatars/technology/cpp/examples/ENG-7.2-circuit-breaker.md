---
law_id: ENG-7.2
cpp_version_min: 11
avatar: cpp
---

# Circuit Breaker — C++ Implementation

Per [ENG-7.2](laws/engineering/eng-7-reliability.md), external dependency calls must use a circuit breaker to prevent cascade failures.

## COMPLIANT — Atomic state-machine circuit breaker

**Note:** This example uses `std::atomic` with memory ordering (`memory_order_acquire`/`release`). These are C++'s low-level concurrency primitives — Java's closest equivalent is `java.util.concurrent.atomic` classes.

```cpp
#include <atomic>
#include <chrono>
#include <stdexcept>

enum class CBState { Closed, Open, HalfOpen };

class CircuitBreaker {
public:
    explicit CircuitBreaker(int threshold = 5,
                            std::chrono::seconds recovery = std::chrono::seconds{30})
        : threshold_{threshold}, recovery_{recovery} {}

    // Wraps any callable with circuit breaker protection
    template <typename Func>
    auto call(Func&& fn) -> decltype(fn()) {
        auto now = Clock::now();
        auto state = state_.load(std::memory_order_acquire);
        if (state == CBState::Open) {
            if (now - last_failure_.load() > recovery_) {
                state_.store(CBState::HalfOpen, std::memory_order_release);
            } else {
                throw std::runtime_error{"circuit breaker open"};
            }
        }
        try {
            auto result = fn();
            failure_count_.store(0, std::memory_order_relaxed);
            state_.store(CBState::Closed, std::memory_order_release);
            return result;
        } catch (...) {
            last_failure_.store(now, std::memory_order_release);
            if (++failure_count_ >= threshold_) {
                state_.store(CBState::Open, std::memory_order_release);
            }
            throw;
        }
    }

    CBState state() const { return state_.load(std::memory_order_acquire); }

private:
    using Clock = std::chrono::steady_clock;
    int threshold_;
    std::chrono::seconds recovery_;
    std::atomic<CBState> state_{CBState::Closed};
    std::atomic<int> failure_count_{0};
    std::atomic<Clock::time_point> last_failure_{};
};
```

## NON-COMPLIANT — Raw external call without protection

```cpp
// ❌ No circuit breaker — cascade failure if Sabre is down
auto result = sabre_client.get_availability(criteria);
```

## Key Rules

| Rule | Rationale |
|------|-----------|
| Every external call gets a circuit breaker | Prevent thread starvation from blocked calls |
| Thresholds are configurable | Different deps have different failure profiles |
| Expose metrics (`open_total`, `half_open_total`) | Observability per [ENG-5.5](laws/engineering/eng-5-devops.md) |
| Test state transitions in GoogleTest | Inject failures to verify Open/HalfOpen/Closed cycle |

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Half-open state does not reset under sustained low error rate | Circuit breaker stays permanently half-open because occasional failures prevent CLOSED transition; service capacity is capped | Require N *consecutive* successes (not N out of M) to transition HALF-OPEN → CLOSED |
| Circuit breaker trips on client-side timeout, not actual server error | Downstream is healthy; client's own thread pool is saturated; timeouts are misclassified as server failures | Distinguish timeout errors from server errors in the failure counter; count only 5xx responses as "circuit-trip eligible" |
| All instances trip simultaneously under correlated load spike | A traffic spike causes all instances to open their circuit breakers at the same time; the dependency receives zero traffic and cannot recover | Add randomised jitter to the OPEN → HALF-OPEN probe window; stagger recovery across instances |
