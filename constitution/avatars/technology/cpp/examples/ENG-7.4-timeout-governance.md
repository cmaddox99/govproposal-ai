---
law_id: ENG-7.4
cpp_version_min: 17
cpp_version_note: >-
  Uses C++17 std::optional for optional timeout values. Transitional teams: use boolean flag + value pair; brownfield: use magic value (0 = no timeout) with docs.
avatar: cpp
---

# Timeout Governance — C++ Implementation

Per [ENG-7.4](laws/engineering/eng-7-reliability.md), every external call must have an explicit timeout. No call may block indefinitely.

> ⚠️ **`std::future` destructor blocks — do NOT use as a production timeout.**
> `std::async(std::launch::async)` returns a `std::future` whose **destructor blocks
> until the launched task completes** ([futures.future.dtor]). If `wait_for` returns
> `timeout`, the `future` goes out of scope and its destructor **immediately blocks
> for the same duration** — negating the timeout entirely. See Effective Modern C++
> Item 38. The pattern below is shown for deadline *propagation* only.
>
> **Correct approach:** Use **API-native timeouts** (gRPC deadline, socket `SO_TIMEOUT`,
> HTTP client timeout config) or **cooperative cancellation** via `std::stop_token`
> (C++20) or a `std::atomic<bool>` stop flag (C++11+).

## COMPLIANT — Deadline propagation (use alongside API-native timeouts)

```cpp
#include <chrono>
#include <future>
#include <optional>

// ⚠️ NOT a production timeout: std::future destructor blocks until task completes.
// Use only for deadline PROPAGATION with API-native per-call timeouts.
// See warning above.
template <typename Func>
auto wait_with_deadline(Func&& fn, std::chrono::milliseconds timeout)
    -> std::optional<decltype(fn())>
{
    auto future = std::async(std::launch::async, std::forward<Func>(fn));
    if (future.wait_for(timeout) == std::future_status::ready) {
        return future.get();  // completed within deadline
    }
    return std::nullopt;  // deadline exceeded — future destructor still blocks here!
}

// Deadline propagation — child calls respect remaining budget
class DeadlineContext {
public:
    explicit DeadlineContext(std::chrono::milliseconds budget)
        : deadline_{Clock::now() + budget} {}

    std::chrono::milliseconds remaining() const {
        auto left = deadline_ - Clock::now();
        return std::max(std::chrono::milliseconds{0},
                        std::chrono::duration_cast<std::chrono::milliseconds>(left));
    }

    bool expired() const { return Clock::now() >= deadline_; }

private:
    using Clock = std::chrono::steady_clock;
    Clock::time_point deadline_;
};

// Usage — chain calls share a deadline budget
FlightResult search_flights(const Criteria& c) {
    DeadlineContext deadline{std::chrono::seconds{10}};  // 10s total budget

    auto avail = wait_with_deadline(
        [&] { return sabre.get_availability(c); },
        deadline.remaining());
    if (!avail) return FlightResult::timeout("Sabre");

    auto pricing = wait_with_deadline(
        [&] { return pricing_engine.price(*avail); },
        deadline.remaining());  // uses remaining budget
    if (!pricing) return FlightResult::timeout("pricing");

    return FlightResult::success(*pricing);
}
```

## NON-COMPLIANT — Indefinite blocking

```cpp
// ❌ No timeout — blocks forever if remote service hangs
auto result = client.get(url);

// ❌ Timeout on outer call but not inner calls
auto outer = wait_with_deadline([&] {
    auto a = serviceA.call();   // no timeout — can consume entire budget
    auto b = serviceB.call();   // may never execute
    return combine(a, b);
}, 10s);
```

## COMPLIANT — Cooperative cancellation with stop flag (C++11+, real timeout)

When API-native timeouts are unavailable, pass a `std::atomic<bool>` stop flag into
the task. The thread joins promptly after expiry — a **real** timeout, not the blocking
`std::future` pattern.

```cpp
#include <atomic>
#include <chrono>
#include <thread>
#include <optional>

// Task must accept and check stop_flag
std::optional<FlightResult> fetch_with_cancel(
    const SearchCriteria& c, std::atomic<bool>& stop)
{
    for (auto& seg : c.segments()) {
        if (stop.load(std::memory_order_relaxed)) return std::nullopt;
        seg.fetch_pricing();
    }
    return assemble_result(c);
}

// Caller sets deadline and signals stop on expiry
auto run_with_timeout(const SearchCriteria& c,
                      std::chrono::milliseconds budget)
    -> std::optional<FlightResult>
{
    std::atomic<bool> stop{false};
    std::optional<FlightResult> result;
    std::thread worker([&] { result = fetch_with_cancel(c, stop); });

    auto deadline = std::chrono::steady_clock::now() + budget;
    while (std::chrono::steady_clock::now() < deadline && !result)
        std::this_thread::sleep_for(std::chrono::milliseconds{5});

    stop.store(true);
    worker.join();  // joins promptly — task checks stop flag
    return result;
}
```

## Key Rules

| Rule | Rationale |
|------|-----------|
| Every external call has explicit timeout | No indefinite blocking |
| Use `std::chrono` durations, not raw `int` | Type safety per [ENG-3.1](laws/engineering/eng-3-code-quality.md) |
| Propagate deadline budget to child calls | Inner calls must not exceed outer deadline |
| Configure timeouts per dependency | Different services have different SLAs |
| Log timeout events with service name | Diagnosability per [ENG-5.5](laws/engineering/eng-5-devops.md) |

## Edge Cases & Warnings

| Scenario | Safe Approach |
|----------|---------------|
| `wait_for` returns `deferred` (not `timeout`) — future never starts | Treat `deferred` as error; never interpret as completed |
| Inner timeout shorter than outer — premature cancel | Pass deadline timestamps, not durations, through the call stack |
| Clock skew fires timeout immediately | Use `steady_clock` internally; only convert to `system_clock` for external timestamps |
