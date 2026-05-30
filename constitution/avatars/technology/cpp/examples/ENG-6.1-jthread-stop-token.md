---
law_id: ENG-6.1
cpp_version_min: 20
cpp_version_note: >-
  std::jthread and std::stop_token require C++20. For C++11/14 projects,
  see ENG-6.1-thread-stop-flag.md (atomic<bool> cooperative cancellation).
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): `std::jthread` and `std::stop_token` (C++20)

Per [ENG-6.1](laws/engineering/eng-6-security.md), background threads must
be safely stoppable without data races. `jthread` auto-joins on destruction;
`stop_token` enables cooperative cancellation without shared mutable flags.

## COMPLIANT: Cancellable Validation Task

```cpp
#include <thread>
#include <stop_token>

// AA domain: background seat-map validation with cooperative cancel
std::jthread start_validation(const FlightId& fid) {
    return std::jthread([fid](std::stop_token stoken) {
        for (auto& seat : load_seat_map(fid)) {
            if (stoken.stop_requested()) return;  // ✅ cooperative cancel
            validate_seat(seat);
        }
    });
}   // ✅ auto-joins on destruction — no detached thread, no terminate()
```

`stop_callback` for cleanup on cancellation:

```cpp
std::jthread worker([](std::stop_token stoken) {
    std::stop_callback on_stop{stoken, []{ cancel_pending_io(); }};  // ✅
    do_blocking_io(stoken);
});
worker.request_stop();  // ✅ fires callback, then joins in destructor
```

## NON-COMPLIANT: Raw Thread + `volatile bool` Stop Flag

```cpp
volatile bool stop = false;           // ❌ volatile ≠ atomic — data race
std::thread t([&stop]{
    while (!stop) do_work();          // ❌ UB: concurrent read+write
});
stop = true;
t.join();                             // ❌ must not forget join
```

Problems: `volatile` does not provide atomicity; missed `join()` is UB
(`std::terminate`); no structured cleanup path.

## Edge Cases

- **jthread + coroutine**: check CP.52 — do not hold locks across `co_await`
  suspension points (see `coroutines.md`)
- **stop_callback lifetime**: fires immediately if stop already requested at
  construction — always register before blocking
- **Multiple stop_callbacks**: all fire in LIFO order on `request_stop()`

