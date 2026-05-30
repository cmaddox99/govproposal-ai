---
law_id: ENG-6.1
cpp_version_min: 11
cpp_version_note: >-
  Manual cooperative cancellation using std::atomic<bool> for C++11/14.
  When C++20 is available, replace with std::jthread + std::stop_token.
avatar: cpp
rag_exclude: true  # placeholder — content pending CBF adoption; excluded from RAG routing
---

# [ENG-6.1](laws/engineering/eng-6-security.md): Cooperative Thread Cancellation — C++11/14 Stop Flag

**Avatar:** C++ (Transitional C++11/14 — CWR / IOC_ALP)
**Pattern:** `std::atomic<bool>` stop flag with explicit memory ordering

## Context

Stopping a worker thread requires a signal that is:
1. **Visible** across threads — no CPU reordering, no compiler cache.
2. **Ordered** — the worker must see all work completed *before* the flag
   store; the requester must not proceed until the worker has read the flag.

`volatile bool` satisfies neither. Per [ENG-6.1](laws/engineering/eng-6-security.md),
use `std::atomic<bool>` with explicit `memory_order_release` / `memory_order_acquire`.

When C++20 is available, replace with `std::jthread` + `std::stop_token` —
see below.

## COMPLIANT — atomic<bool> Stop Flag

```cpp
// worker_thread.cpp  (CWR / IOC_ALP — C++11/14)
#include <atomic>
#include <thread>

class FlightDataWorker {
public:
    FlightDataWorker() : stop_flag_(false) {}

    void start()
    {
        thread_ = std::thread([this] { run(); });
    }

    void stop()
    {
        // release: all prior writes visible to any thread that acquires this.
        stop_flag_.store(true, std::memory_order_release);
        if (thread_.joinable()) thread_.join();
    }

    ~FlightDataWorker() { stop(); }

private:
    void run()
    {
        while (true) {
            // acquire: we see all writes made before the release store.
            if (stop_flag_.load(std::memory_order_acquire)) break;
            process_next_flight_update();
        }
    }

    std::atomic<bool> stop_flag_;
    std::thread       thread_;
};
```

**Why `memory_order_release` / `memory_order_acquire`:** The release store
on `stop_flag_` synchronizes-with the acquire load. Every write visible
before the store (e.g., flush of pending data) is guaranteed visible to the
loading thread. Using `memory_order_relaxed` on both sides would allow the
compiler or CPU to reorder the flag store before the flush — the worker could
see the flag set before seeing the completed flush.

## COMPLIANT — RAII Stop Guard

```cpp
// Scoped cancellation — flag is set automatically when guard goes out of scope.
struct StopGuard {
    explicit StopGuard(std::atomic<bool>& flag) : flag_(flag) {}
    ~StopGuard() { flag_.store(true, std::memory_order_release); }

    StopGuard(const StopGuard&) = delete;
    StopGuard& operator=(const StopGuard&) = delete;

private:
    std::atomic<bool>& flag_;
};

// Usage: flag is set at end of the calling scope even on exception.
void run_with_auto_cancel(std::atomic<bool>& flag)
{
    StopGuard guard(flag);
    do_work();  // if this throws, guard destructor still sets the flag
}
```

## NON-COMPLIANT

```cpp
// WRONG 1: volatile bool — does NOT prevent data race.
// volatile prevents compiler reordering relative to I/O but gives no
// guarantee about CPU reordering or visibility across cores.
// This is a data race (undefined behavior under the C++11 memory model).
volatile bool stop_flag = false;  // ← data race

void worker_bad()
{
    while (!stop_flag) { process_next_flight_update(); }
}

// WRONG 2: plain bool read without atomic load.
// The compiler may hoist the load out of the loop (valid optimization for
// non-atomic non-volatile variables), making the loop infinite.
bool stop_flag2 = false;

void worker_bad2()
{
    while (!stop_flag2) {  // compiler may cache in register — loop never exits
        process_next_flight_update();
    }
}

// WRONG 3: atomic<bool> but with memory_order_relaxed on both sides.
// Relaxed provides atomicity (no torn reads) but no ordering guarantee.
// The worker may see the stop flag set before seeing all prior work flushed.
std::atomic<bool> stop_flag3{false};

void requester_bad()
{
    flush_pending_data();
    stop_flag3.store(true, std::memory_order_relaxed);  // ← no sync guarantee
}
```

## C++20 Migration Note

Replace the manual stop flag with `std::jthread` + `std::stop_token`:

```cpp
// C++20: no manual flag, no explicit join — jthread handles both.
#include <thread>

class FlightDataWorker20 {
public:
    void start()
    {
        // stop_source is built in; stop() called automatically on destruction.
        thread_ = std::jthread([](std::stop_token stoken) {
            while (!stoken.stop_requested()) {
                process_next_flight_update();
            }
        });
    }
    // ~FlightDataWorker20() — jthread destructor calls request_stop() + join().

private:
    std::jthread thread_;
};
```

## Edge Cases & Warnings

- **`memory_order_relaxed` is not sufficient for stop flags:** Relaxed atomic
  operations are atomic (no torn reads) but provide no synchronization between
  threads. Use `release` on the store and `acquire` on the load to establish a
  happens-before relationship. Using `memory_order_seq_cst` (the default for
  `store`/`load` with no argument) is also correct but more expensive.

- **Spurious wakeup and spin-wait:** If the worker tight-loops on
  `stop_flag_.load()` between work items, it wastes a CPU core. Add a
  `std::this_thread::sleep_for` or a condition variable wait to yield between
  checks. Cooperative cancellation implies the worker checks the flag at
  natural pause points, not in a spin loop.

- **Flag not checked during blocking I/O:** If `process_next_flight_update()`
  blocks on network or disk I/O, the stop flag will not be checked until the
  I/O returns. Use timeouts on blocking calls and check the flag after each
  return.

- **`volatile` is not a substitute for `atomic` in C++11+:** The C++11 memory
  model defines data races on non-atomic variables as undefined behavior.
  `volatile` prevents compiler-reordering relative to I/O side effects but
  does not prevent CPU out-of-order execution and does not define
  synchronization semantics between threads.

Per [ENG-6.1](laws/engineering/eng-6-security.md): inter-thread signalling
must use `std::atomic` with appropriate memory ordering. `volatile bool`
stop flags are a data race under the C++11 memory model.
