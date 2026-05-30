---
law_id: ENG-6.1
cpp_version_min: 11
cpp_version_note: >-
  Uses C++11 std::thread, std::mutex, and std::lock_guard — the first
  portable standard threading API. For C++17+ use std::scoped_lock.
  For C++98/POSIX brownfield code see ENG-6.1-thread-safety-brownfield-posix (coming Phase 2C).
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): Security by Design — Thread Safety (C++11)

## COMPLIANT: `lock_guard` + `atomic` Counter

```cpp
#include <mutex>
#include <atomic>
#include <thread>
#include <string>
#include <unordered_map>

class SeatInventory {
    mutable std::mutex mtx_;
    std::unordered_map<std::string, int> seats_;  // flight -> available count
    std::atomic<uint64_t> query_count_{0};
public:
    bool reserve(const std::string& flight) {
        std::lock_guard<std::mutex> lock(mtx_);   // C++11 RAII — always unlocks
        auto it = seats_.find(flight);
        if (it != seats_.end() && it->second > 0) {
            --it->second;
            return true;
        }
        return false;
    }

    int available(const std::string& flight) const {
        ++query_count_;                            // atomic — no lock needed
        std::lock_guard<std::mutex> lock(mtx_);
        auto it = seats_.find(flight);
        return it != seats_.end() ? it->second : 0;
    }
};
```

**Why compliant:** `lock_guard` unlocks on every exit path (normal return, throw).
`atomic<uint64_t>` counter requires no lock — hardware-atomic read-modify-write.

## COMPLIANT: Launching a `std::thread` with RAII Guard

```cpp
#include <thread>
#include <mutex>

void process_batch(std::vector<FlightRecord>& records, std::mutex& mtx) {
    std::lock_guard<std::mutex> lock(mtx);
    for (auto& r : records) r.process();
}

// Launch threads — join on scope exit via RAII wrapper or explicit join
std::thread worker(process_batch, std::ref(batch), std::ref(mtx));
worker.join();  // Must join before mutex/data is destroyed
```

**Why compliant:** `lock_guard` guards shared data; `join()` ensures the thread
completes before the guarded data goes out of scope. Forgetting `join()` terminates
the program via `std::terminate` when the thread destructor fires.

## COMPLIANT: Producer/Consumer with `condition_variable`

```cpp
#include <mutex>
#include <condition_variable>
#include <queue>

template<typename T>
class BoundedQueue {
    std::mutex mtx_;
    std::condition_variable not_full_;
    std::condition_variable not_empty_;
    std::queue<T> q_;
    std::size_t max_;
public:
    explicit BoundedQueue(std::size_t max) : max_(max) {}

    void push(T item) {
        std::unique_lock<std::mutex> lock(mtx_);
        not_full_.wait(lock, [this]{ return q_.size() < max_; });
        q_.push(std::move(item));
        not_empty_.notify_one();
    }

    T pop() {
        std::unique_lock<std::mutex> lock(mtx_);
        not_empty_.wait(lock, [this]{ return !q_.empty(); });
        T item = std::move(q_.front());
        q_.pop();
        not_full_.notify_one();
        return item;
    }
};
```

**Why compliant:** `unique_lock` is required for `condition_variable` — it allows
the mutex to be released during `wait()` and re-acquired on wake. The predicate
lambda (`[this]{ return ... }`) prevents spurious-wakeup data races: the thread
only proceeds when the condition is actually true.

## NON-COMPLIANT: Raw `lock()`/`unlock()`

```cpp
bool reserve(const std::string& flight) {
    mtx_.lock();
    auto it = seats_.find(flight);
    if (it == seats_.end()) throw std::runtime_error("unknown");  // DEADLOCK — never unlocks
    --it->second;
    mtx_.unlock();
    return true;
}
```

**Why non-compliant:** Any exception between `lock()` and `unlock()` permanently
deadlocks every subsequent caller. This includes `std::bad_alloc` from `find()`
on low-memory systems. There is no safe way to write this pattern without RAII.

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| `volatile` as sync | CPU reordering still causes races | Use `std::atomic<T>` |
| `detach()` with stack data | Thread outlives referenced data | Prefer `join()`; use `shared_ptr` if detach required |
| Recursive `std::mutex` | Re-entrant lock → deadlock | Use `std::recursive_mutex` only as last resort |
| C++03 compiler | `std::thread`/`std::mutex` absent | Use POSIX `pthread` — see `ref-concurrency-brownfield.md` |

1. Use `std::lock_guard<std::mutex>` for scoped locking — never raw `lock()`/`unlock()`
2. Use `std::unique_lock<std::mutex>` only when you need `condition_variable`
3. Use `std::atomic<T>` for counters/flags — no mutex needed
4. Use `std::thread` instead of `pthread_create` for portability
5. Run ThreadSanitizer (TSan) in CI to catch races
