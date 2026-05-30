---
id: ref-concurrency-advanced-part2
cpp_version_min: 20
cpp_version_note: >-
  Advanced concurrency Part 2: std::jthread, std::stop_token,
  std::stop_callback, CP.51/CP.52/CP.53 coroutine-concurrency safety rules.
  All patterns require C++20 or later.
avatar: cpp
---

# Advanced Concurrency — Part 2 (C++20+)

Per [ENG-6.1](laws/engineering/eng-6-security.md), all concurrency patterns
must address data races and undefined behaviour.

---

## `std::jthread` and `std::stop_token` (C++20)

`std::jthread` auto-joins on destruction, eliminating the `thread::join()`
call that `std::thread` requires (forgetting it calls `std::terminate`).
Per [ENG-6.1](laws/engineering/eng-6-security.md) and
[Core Guidelines CP.25](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rconc-join),
prefer `jthread` for all new code.

### COMPLIANT: `jthread` with Cooperative Cancellation

```cpp
#include <thread>
#include <stop_token>

// AA domain: cancellable fare-search background thread
std::jthread start_fare_search(const SearchRequest& req) {
    return std::jthread([req](std::stop_token stoken) {
        for (const auto& origin : req.origins) {
            if (stoken.stop_requested()) return;  // ✅ cooperative cancel
            auto fares = fetch_fares(origin, req.destination);
            publish(fares);
        }
    });
}   // ✅ auto-joins on destruction — no dangling thread, no terminate()
```

Caller cancels by destroying the `jthread` or calling `request_stop()`:

```cpp
{
    auto search = start_fare_search(req);
    std::this_thread::sleep_for(std::chrono::seconds(2));
    search.request_stop();  // ✅ signals stop; destructor joins
}   // ✅ joined here — no resource leak
```

### `stop_callback` for Cleanup on Cancellation

`stop_callback` fires synchronously when `stop_requested()` first becomes
true, regardless of whether the thread has checked yet — use for I/O
cancellation and condvar wakeup:

```cpp
std::jthread worker([](std::stop_token stoken) {
    std::mutex mtx;
    std::condition_variable_any cv;

    std::stop_callback on_stop{stoken, [&]{ cv.notify_all(); }};  // ✅

    std::unique_lock lock{mtx};
    cv.wait(lock, stoken, [&]{ return work_available() || stoken.stop_requested(); });
    // ✅ wakes immediately on stop — no stuck thread
});
```

### NON-COMPLIANT: `std::thread` + `std::atomic<bool>` Stop Flag

```cpp
std::atomic<bool> stop_flag{false};

std::thread worker([&stop_flag]() {
    while (!stop_flag.load(std::memory_order_relaxed)) {  // ❌ manual flag
        do_work();
    }
});

stop_flag.store(true);
worker.join();  // ❌ must remember to join; missed join = std::terminate
```

Problems: manual `join()` must never be skipped (RAII not enforced); no
structured cleanup path; `stop_flag` must be kept alive for the thread's
lifetime (dangling reference if local).

### Migration Path

| Old pattern | C++20 replacement |
|---|---|
| `std::thread` | `std::jthread` |
| `atomic<bool> stop` | `std::stop_token` parameter |
| Manual cleanup lambda | `std::stop_callback` |
| `condition_variable` + flag | `condition_variable_any` + `stop_token` |

---

## See Also

- `ref-concurrency-advanced-part1.md` — C++11/17 concurrency: memory ordering, condition variables, lock-free

---

## Coroutine-Concurrency Safety — CP.51/CP.52/CP.53 (C++20)

Per [ENG-6.1](laws/engineering/eng-6-security.md): coroutines introduce
new lifetime and locking hazards that do not exist in ordinary functions.
Three Core Guidelines rules govern safe coroutine-concurrency interaction.
See also `coroutines.md` for generator and async-task patterns.

### CP.51 — No Capturing Lambda Coroutines

A lambda that captures by reference becomes a coroutine whose closure may
be destroyed before the coroutine resumes — a dangling reference.

```cpp
// NON-COMPLIANT: CP.51
auto make_gen = [&data]() -> Generator<int> {  // ❌ capture by ref
    for (auto& x : data) co_yield x;           // ❌ data may be gone at resume
};

// COMPLIANT: CP.51 — pass by value or use a named free function
Generator<int> generate(std::vector<int> data) {  // ✅ owns data
    for (auto x : data) co_yield x;
}
```

### CP.52 — No Locks Held Across Suspension Points

A coroutine suspended while holding a mutex will not release it until
resumed — which may never happen if the awaiter is abandoned, causing
deadlock.

```cpp
// NON-COMPLIANT: CP.52
Task process() {
    std::lock_guard lk{mtx_};   // ❌ lock held...
    co_await fetch_fare();      // ❌ ...across suspension — potential deadlock
}

// COMPLIANT: CP.52 — scope the lock to exclude suspension points
Task process() {
    { std::lock_guard lk{mtx_}; read_shared_state(); }  // ✅ released before await
    co_await fetch_fare();                               // ✅ no lock held
}
```

### CP.53 — No Reference Parameters to Coroutines

Coroutine parameters are copied into the frame; references refer to the
caller's stack which may not exist when the coroutine resumes.

```cpp
// NON-COMPLIANT: CP.53
Task process(const Request& req) {  // ❌ req lives on caller stack
    co_await async_io();            // ❌ caller may have returned; req is dangling
    use(req);
}

// COMPLIANT: CP.53 — pass by value
Task process(Request req) {  // ✅ req copied into coroutine frame
    co_await async_io();
    use(req);                // ✅ safe — owned by coroutine
}
```
