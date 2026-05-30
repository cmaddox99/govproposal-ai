---
law_id: ENG-7.5
cpp_version_min: 20
cpp_version_note: >-
  Uses std::counting_semaphore (<semaphore>, C++20). For C++11/14/17: use the
  condition_variable-based Semaphore class shown below.
avatar: cpp
---

# [ENG-7.5](laws/engineering/eng-7-reliability.md): Bulkhead Isolation — C++ Implementation

## COMPLIANT: Semaphore-Based Bulkhead (C++20)

```cpp
#include <chrono>
#include <optional>
#include <semaphore>

// Isolates each dependency with its own concurrency limit
class Bulkhead {
public:
    explicit Bulkhead(int max_concurrent)
        : semaphore_{max_concurrent} {}

    // Returns nullopt if bulkhead is full (load shedding)
    template <typename Func>
    auto call(Func&& fn,
              std::chrono::milliseconds timeout = std::chrono::seconds{5})
        -> std::optional<decltype(fn())>
    {
        if (!semaphore_.try_acquire_for(timeout)) {
            return std::nullopt;  // shed load — don't wait
        }
        struct Guard {
            std::counting_semaphore<>& s;
            ~Guard() { s.release(); }
        } guard{semaphore_};

        return fn();
    }

private:
    std::counting_semaphore<> semaphore_;
};

// Usage — separate bulkheads per external dependency
class FlightSearchService {
    Bulkhead sabre_bulkhead_{10};     // max 10 concurrent Sabre calls
    Bulkhead amadeus_bulkhead_{5};    // max 5 concurrent Amadeus calls

public:
    std::optional<FlightResult> search_sabre(const SearchCriteria& c) {
        return sabre_bulkhead_.call([&] {
            return sabre_client_.search(c);
        });
    }

    std::optional<FlightResult> search_amadeus(const SearchCriteria& c) {
        return amadeus_bulkhead_.call([&] {
            return amadeus_client_.search(c);
        });
    }
};
```

## COMPLIANT: Semaphore-Based Bulkhead (C++11/14/17 — no `<semaphore>`)

For projects below C++20, implement the semaphore with `std::condition_variable`:

```cpp
#include <chrono>
#include <condition_variable>
#include <mutex>
#include <optional>

// Portable semaphore — C++11/14/17 compatible
class Semaphore {
public:
    explicit Semaphore(int max) : count_{max} {}

    bool try_acquire_for(std::chrono::milliseconds timeout) {
        std::unique_lock<std::mutex> lk{mtx_};
        return cv_.wait_for(lk, timeout, [&] { return count_ > 0; })
               ? (--count_, true) : false;
    }

    void release() {
        std::lock_guard<std::mutex> lk{mtx_};
        ++count_;
        cv_.notify_one();
    }

private:
    std::mutex mtx_;
    std::condition_variable cv_;
    int count_;
};

// Bulkhead using the portable Semaphore — identical interface to C++20 version
class Bulkhead {
public:
    explicit Bulkhead(int max_concurrent) : semaphore_{max_concurrent} {}

    template <typename Func>
    auto call(Func&& fn,
              std::chrono::milliseconds timeout = std::chrono::milliseconds{5000})
        -> std::optional<decltype(fn())>
    {
        if (!semaphore_.try_acquire_for(timeout)) {
            return std::nullopt;  // shed load
        }
        struct Guard {
            Semaphore& s;
            ~Guard() { s.release(); }
        } guard{semaphore_};

        return fn();
    }

private:
    Semaphore semaphore_;
};
```

## NON-COMPLIANT: Shared Thread Pool for All Dependencies

```cpp
// ❌ All external calls share one pool — Sabre outage starves Amadeus
auto pool = ThreadPool{20};

pool.submit([&] { return sabre.search(criteria); });    // blocks all 20 threads
pool.submit([&] { return amadeus.search(criteria); });  // never gets a thread
pool.submit([&] { return weather.get(airport); });      // also starved
```

## Key Rules

| Rule | Rationale |
|------|-----------|
| One bulkhead per external dependency | Failure in one doesn't starve others |
| Configurable concurrency limits | Different deps have different capacities |
| Return `nullopt` on rejection (not throw) | Caller decides degraded vs error response |
| Log bulkhead rejections per [ENG-5.5](laws/engineering/eng-5-devops.md) | Detect capacity issues early |
| Test with simulated slow dependency | Verify isolation under load |

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Bulkhead pool exhaustion not surfaced as a distinct error code | Caller receives a generic `timeout` instead of `BULKHEAD_FULL`; capacity planning and alerting cannot distinguish the two | Return a typed error (`BulkheadExhaustedError`) from the rejection path; log and alert on it separately from timeouts |
| Shared thread pool defeats the isolation guarantee | Two downstream dependencies share the same thread pool; slow dep A starves dep B; the bulkhead is illusory | Each bulkhead must own its own thread pool or use dedicated async channels; never reuse pools across isolation boundaries |
| Concurrency limit set too low after a dependency becomes faster | The limit is never reached at steady state but a burst fills all slots immediately; P99 latency spikes | Review bulkhead limits quarterly against actual p99 concurrency metrics; set limits at 2x the observed p99 active-request count |
