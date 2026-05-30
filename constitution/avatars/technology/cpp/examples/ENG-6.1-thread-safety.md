---
law_id: ENG-6.1
cpp_version_min: 17
cpp_version_note: >-
  Uses C++17 std::scoped_lock for multi-mutex locking. Transitional teams: use std::lock_guard; brownfield: use RAII wrapper around CRITICAL_SECTION.
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): Security by Design — Thread Safety

## COMPLIANT: Scoped Lock and Atomic Counter

```cpp
#include <mutex>
#include <atomic>
#include <unordered_map>
#include <string>

class SeatInventory {
    mutable std::mutex mtx_;
    std::unordered_map<std::string, int> seats_;  // flight -> available
    std::atomic<uint64_t> query_count_{0};
public:
    bool reserve(const std::string& flight) {
        std::scoped_lock lock(mtx_);
        if (auto it = seats_.find(flight); it != seats_.end() && it->second > 0) {
            --it->second;
            return true;
        }
        return false;
    }

    int available(const std::string& flight) const {
        ++query_count_;
        std::scoped_lock lock(mtx_);
        auto it = seats_.find(flight);
        return it != seats_.end() ? it->second : 0;
    }
};
```

**Why compliant:** scoped_lock guarantees unlock on all exit paths. Atomic counter avoids lock for read-only stats.

## COMPLIANT: shared_mutex for Read-Heavy Workloads

```cpp
#include <shared_mutex>

class FlightScheduleCache {
    mutable std::shared_mutex mtx_;
    std::unordered_map<std::string, Schedule> cache_;
public:
    Schedule lookup(const std::string& flight) const {
        std::shared_lock lock(mtx_);  // multiple readers allowed
        return cache_.at(flight);
    }

    void update(const std::string& flight, Schedule sched) {
        std::unique_lock lock(mtx_);  // exclusive writer
        cache_[flight] = std::move(sched);
    }
};
```

**Why compliant:** `shared_lock` allows concurrent reads; `unique_lock` blocks for writes. Critical for high-query services like flight search.

## NON-COMPLIANT: Manual Lock/Unlock

```cpp
bool reserve(const std::string& flight) {
    mtx_.lock();
    auto it = seats_.find(flight);
    if (it == seats_.end()) throw std::runtime_error("unknown");  // DEADLOCK: never unlocks
    --it->second;
    mtx_.unlock();
    return true;
}
```

**Why non-compliant:** Exception between lock/unlock leaves mutex permanently locked. Classic deadlock bug.

## The Rule

1. Always use RAII locks (`scoped_lock`, `shared_lock`, `unique_lock`) — never raw `lock()`/`unlock()`
2. Use `std::atomic` for simple counters and flags — no mutex needed
3. Use `shared_mutex` when reads vastly outnumber writes
4. Lock ordering: when acquiring multiple mutexes, use `std::scoped_lock(m1, m2)` to prevent deadlock
5. Run ThreadSanitizer (TSan) in CI to detect races

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| `static` local variable initialization race in pre-C++11 compilers (brownfield) | The C++11 standard guarantees thread-safe static local init; pre-C++11 compilers do not; two threads can initialise the same static simultaneously | In C++03 brownfield code, use an explicit `pthread_once` or a `double-checked locking` pattern with a `volatile` flag plus a memory barrier |
| `volatile` used as a synchronisation mechanism | `volatile` prevents the compiler from caching the value in a register but does NOT prevent CPU reordering; still a data race | Use `std::atomic` for inter-thread communication; `volatile` is only appropriate for hardware-mapped memory-mapped I/O registers |
| Recursive locking of a non-recursive mutex | Thread acquires `std::mutex` then calls a function that tries to acquire the same mutex — deadlock | Use `std::recursive_mutex` only as a last resort; prefer refactoring to remove recursion; document recursive mutexes prominently |
