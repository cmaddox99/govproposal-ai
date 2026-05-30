---
law_id: ENG-6.1
cpp_version_min: 11
cpp_version_note: "condition_variable requires C++11; condition_variable_any + stop_token requires C++20."
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): `std::condition_variable` (C++11)

Per [ENG-6.1](laws/engineering/eng-6-security.md), condition variable waits
must always use a predicate to guard against spurious wakeups and lost
notifications.

## COMPLIANT: Bounded Queue with Predicate Wait

```cpp
#include <condition_variable>
#include <mutex>
#include <queue>

// AA domain: booking request queue with bounded backpressure
template<typename T, std::size_t Cap>
class BoundedQueue {
    std::queue<T>           q_;
    std::mutex              mtx_;
    std::condition_variable not_full_, not_empty_;
public:
    void push(T item) {
        std::unique_lock lk{mtx_};
        not_full_.wait(lk, [this]{ return q_.size() < Cap; });  // ✅ predicate
        q_.push(std::move(item));
        not_empty_.notify_one();
    }
    T pop() {
        std::unique_lock lk{mtx_};
        not_empty_.wait(lk, [this]{ return !q_.empty(); });  // ✅ predicate
        T item = std::move(q_.front()); q_.pop();
        not_full_.notify_one();
        return item;
    }
};
```

## COMPLIANT: `condition_variable_any` + `stop_token` (C++20)

```cpp
std::condition_variable_any cv;
// ✅ overload with stop_token — wakes on stop OR predicate
cv.wait(lk, stoken, [&]{ return !q_.empty() || stoken.stop_requested(); });
```

## NON-COMPLIANT: Bare `wait()` Without Predicate

```cpp
cv.wait(lk);                     // ❌ spurious wakeup → premature wake
auto item = q_.front();          // ❌ queue may be empty — undefined behaviour
```

## Edge Cases & Warnings

| Scenario | Risk | Mitigation |
|----------|------|------------|
| Lost wakeup | Notify before wait can be missed | Predicate re-evaluated on every wakeup — no message lost |
| Spurious wakeup | `wait()` can return without notify | Always use predicate form `wait(lk, []{ return ready; })` |
| `notify_all` thundering herd | All threads wake; only one proceeds | Use `notify_one` when only one consumer should run |
| Holding lock during notify | No correctness issue, but can stall | Notify after releasing lock for best throughput |
