---
id: ref-concurrency-advanced-part1
cpp_version_min: 11
cpp_version_note: >-
  Advanced concurrency Part 1: std::memory_order happens-before reasoning,
  condition variable patterns (CP.42), lock-free data structures, thread
  pools, false sharing, std::promise/future, Amdahl's Law. All patterns
  require C++11 or later.
avatar: cpp
---

# Advanced Concurrency — Part 1 (C++11/14/17)

Per [ENG-6.1](laws/engineering/eng-6-security.md), all concurrency patterns
must address data races and undefined behavior.

Use ThreadSanitizer (TSan) to detect data races: `clang++ -fsanitize=thread`.
Use `std::atomic<T>` for single-variable lock-free operations; mutexes for complex shared state.

---

## Condition Variable Patterns (C++11)

Per [ENG-6.1](laws/engineering/eng-6-security.md) and
[CP.42](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rconc-wait):
**never wait on a `condition_variable` without a predicate** — bare `wait()`
is vulnerable to spurious wakeups and lost notifications.

### COMPLIANT: Predicate-Protected Wait (Producer-Consumer)

```cpp
#include <condition_variable>
#include <mutex>
#include <queue>

// AA domain: fare-update notification pipeline
class FareUpdateQueue {
    std::queue<FareUpdate> q_;
    std::mutex              mtx_;
    std::condition_variable cv_;
public:
    void push(FareUpdate u) {
        { std::lock_guard lk{mtx_}; q_.push(std::move(u)); }
        cv_.notify_one();  // ✅ notify after lock released (avoids contention)
    }
    FareUpdate pop() {
        std::unique_lock lk{mtx_};
        cv_.wait(lk, [this]{ return !q_.empty(); });  // ✅ predicate re-checked on spurious wakeup
        auto u = std::move(q_.front()); q_.pop();
        return u;
    }
};
```

### COMPLIANT: `wait_for` with Timeout

```cpp
auto status = cv_.wait_for(lk, std::chrono::seconds(5),
                            [this]{ return !q_.empty(); });
// ✅ returns false if timed out; predicate still guards spurious wakeup
if (!status) handle_timeout();
```

### NON-COMPLIANT: Bare `wait()` Without Predicate

```cpp
cv_.wait(lk);                    // ❌ spurious wakeup causes premature wake
auto u = q_.front();             // ❌ queue may be empty — undefined behaviour
```

### CP.42 Checklist

| Requirement | Correct pattern |
|---|---|
| Never bare wait | `cv.wait(lk, predicate)` |
| Lock type for wait | `unique_lock`, not `lock_guard` |
| Notify timing | after releasing lock (or with lock held — both valid; post-release preferred) |
| Predicate captures | only what outlives the wait scope |

---

## Lock-free Data Structures (C++11)

Per [ENG-6.1](laws/engineering/eng-6-security.md): **lock-free ≠ fast**.
Always profile before replacing a mutex with atomic operations — cache line
contention can make lock-free slower than a well-contended mutex.

> **Rule:** Lock-free is rarely appropriate at the application layer.
> Use mutexes first; reach for atomics only with profiler evidence.

### When NOT to Use Lock-free

- Multiple threads sharing the same cache line → false sharing dominates
- Contended `compare_exchange` loops → worse than a mutex under high load
- Complex invariants spanning multiple variables → atomics cannot help

### ABA Problem

```cpp
// ABA: thread reads A, another thread changes A→B→A, CAS succeeds wrongly
// Mitigation: stamped/versioned pointer
struct Stamped { Node* ptr; uintptr_t ver; };
std::atomic<Stamped> head;
// ✅ increment version on every CAS to distinguish A-original from A-returned
```

### COMPLIANT: SPSC Ring Buffer (Lock-free)

```cpp
// Single-producer single-consumer — no contention by design
// Requires: T must be default-constructible and move-assignable.
// For optimal lock-free safety, prefer trivially-copyable types (avoids N ctor calls at init).
template<typename T, std::size_t N>
    requires std::is_default_constructible_v<T> && std::is_move_assignable_v<T>
class SpscRingBuffer {
    std::array<T, N>      buf_{};
    std::atomic<std::size_t> head_{0}, tail_{0};
public:
    bool push(T val) {                         // producer only
        auto h = head_.load(std::memory_order_relaxed);
        auto next = (h + 1) % N;
        if (next == tail_.load(std::memory_order_acquire)) return false;  // full
        buf_[h] = std::move(val);
        head_.store(next, std::memory_order_release);  // ✅ publish
        return true;
    }
    bool pop(T& val) {                         // consumer only
        auto t = tail_.load(std::memory_order_relaxed);
        if (t == head_.load(std::memory_order_acquire)) return false;     // empty
        val = std::move(buf_[t]);
        tail_.store((t + 1) % N, std::memory_order_release);  // ✅ consume
        return true;
    }
};
```

### `std::atomic<shared_ptr<T>>` — Atomic, Not Necessarily Lock-free (C++20)

```cpp
std::atomic<std::shared_ptr<FlightNode>> head;

// ✅ atomic update — thread-safe; but is_lock_free() may be false
auto old = head.load(std::memory_order_acquire);
auto new_node = std::make_shared<FlightNode>(data);
head.compare_exchange_strong(old, new_node, std::memory_order_acq_rel);

// ✅ ALWAYS check before assuming lock-free performance
if (!head.is_lock_free()) {
    // implementation uses a mutex internally — profile accordingly
}
```

### NON-COMPLIANT: Assuming `atomic<shared_ptr>` Is Lock-free

```cpp
// ❌ assuming lock-free behaviour without checking is_lock_free()
// ❌ replacing a mutex purely for "performance" without profiling
// ❌ MPMC (multi-producer multi-consumer) without formal correctness proof
```

---

## Thread Pool and Work-Stealing (C++11)

Per [ENG-6.1](laws/engineering/eng-6-security.md) and
[CP.41](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rconc-create):
**minimise thread creation** — each `std::thread` costs ~64 KB stack plus
OS scheduling overhead. Reuse threads via a pool.

### COMPLIANT: Fixed-Size Thread Pool (Producer-Consumer)

```cpp
// AA domain: parallel crew pairing feasibility checks
class ThreadPool {
    std::vector<std::thread>          workers_;
    std::queue<std::function<void()>> tasks_;
    std::mutex                        mtx_;
    std::condition_variable           cv_;
    bool                              stop_{false};
public:
    explicit ThreadPool(std::size_t n) {
        workers_.reserve(n);
        for (std::size_t i = 0; i < n; ++i)
            workers_.emplace_back([this] {
                for (;;) {
                    std::function<void()> task;
                    { std::unique_lock lk{mtx_};
                      cv_.wait(lk, [this]{ return stop_ || !tasks_.empty(); });
                      if (stop_ && tasks_.empty()) return;
                      task = std::move(tasks_.front()); tasks_.pop(); }
                    task();  // ✅ execute outside lock
                    // Note: unhandled exceptions in task() call std::terminate
                    // (std::thread behaviour). For production, wrap in try/catch
                    // or use std::packaged_task to propagate via futures.
                }
            });
    }
    template<typename F>
    void submit(F&& f) {
        { std::lock_guard lk{mtx_}; tasks_.emplace(std::forward<F>(f)); }
        cv_.notify_one();
    }
    ~ThreadPool() {
        { std::lock_guard lk{mtx_}; stop_ = true; }
        cv_.notify_all();
        for (auto& w : workers_) w.join();  // ✅ RAII join
    }
};

// Usage: submit N crew pairing checks to hardware_concurrency() threads
ThreadPool pool{std::thread::hardware_concurrency()};
for (auto& pair : candidates)
    pool.submit([&pair]{ pair.check_feasibility(); });
```

### Work-Stealing Concept

Work-stealing improves load balancing: idle threads steal tasks from the
back of busy threads' deques while the owner takes from the front, reducing
contention. Prefer `std::execution` policies (`par_unseq`) or a library
(Intel TBB, taskflow) over hand-rolled work-stealing for production code.

### `std::async` vs Thread Pool

| Pattern | When to use |
|---|---|
| `std::async(std::launch::async, f)` | one-off async result, low volume |
| Thread pool | repeated short tasks (crew checks, fare combos) |
| `std::thread` per task | ❌ — CP.41 violation; prefer pool |

### NON-COMPLIANT: Unbounded Thread Creation

```cpp
for (auto& pair : candidates)
    std::thread([&pair]{ pair.check_feasibility(); }).detach();  // ❌ CP.41
// ❌ N threads for N tasks — no bound; OOM/scheduling collapse under load
```

---

## False Sharing and Cache Line Alignment (C++17)

Per [ENG-6.1](laws/engineering/eng-6-security.md): false sharing is a
**silent performance hazard** — two threads writing different variables on
the same 64-byte cache line cause the cache coherency protocol to bounce
the line between cores, serialising what should be independent writes.

### COMPLIANT: Per-Thread Accumulator with `alignas`

```cpp
#include <new>  // hardware_destructive_interference_size

// ✅ each counter on its own cache line — no false sharing
struct alignas(std::hardware_destructive_interference_size) PaddedCounter {
    std::atomic<std::uint64_t> value{0};
};

// AA domain: per-thread fare-search stats accumulator
std::vector<PaddedCounter> stats(std::thread::hardware_concurrency());

void record_hit(std::size_t tid) {
    stats[tid].value.fetch_add(1, std::memory_order_relaxed);  // ✅
}
std::uint64_t total_hits() {
    std::uint64_t n = 0;
    for (auto& c : stats) n += c.value.load(std::memory_order_relaxed);
    return n;
}
```

### NON-COMPLIANT: Adjacent Hot Counters (False Sharing)

```cpp
struct Counters {
    std::atomic<uint64_t> hits{0};    // ❌ same cache line as misses
    std::atomic<uint64_t> misses{0};  // ❌ writing misses invalidates hits' line
};
```

### Key Facts

| Fact | Value |
|---|---|
| Typical cache line (x86/ARM) | 64 bytes |
| `hardware_destructive_interference_size` | ≥ cache line (compile-time constant) |
| `hardware_constructive_interference_size` | fit related items in one line |
| Detection | `perf c2c` or VTune memory access analysis |

---

## `std::promise` and `std::future` Patterns (C++11)

Per [ENG-6.1](laws/engineering/eng-6-security.md): use `promise`/`future`
to transfer a single async result (or exception) safely between threads.
Prefer `std::async` for simple cases; use `promise` when the producing
thread is not the launching thread.

### COMPLIANT: Async Fare Availability Check with Timeout

```cpp
// AA domain: async fare availability check
std::promise<FareResult> prom;
std::future<FareResult>  fut = prom.get_future();

std::thread producer([p = std::move(prom)]() mutable {
    try {
        p.set_value(fetch_fare_availability());  // ✅ or set_exception on failure
    } catch (...) {
        p.set_exception(std::current_exception());  // ✅ propagates to get()
    }
});
producer.detach();

// Consumer: wait up to 3 s
if (fut.wait_for(std::chrono::seconds(3)) == std::future_status::ready) {
    auto result = fut.get();  // ✅ re-throws stored exception if set
} else {
    handle_timeout();
}
```

### `packaged_task` and `shared_future`

```cpp
// packaged_task: deferred callable with built-in promise
std::packaged_task<FareResult()> task{fetch_fare_availability};
std::future<FareResult> fut2 = task.get_future();
pool.submit(std::move(task));  // submit to thread pool

// shared_future: multi-consumer broadcast
std::shared_future<FareResult> sf = fut2.share();  // ✅ copyable
```

### NON-COMPLIANT: Shared-State Lifetime Bug

```cpp
std::future<int> make_future() {
    std::promise<int> p;
    auto f = p.get_future();
    // ❌ p destroyed here without set_value/set_exception
    //    → shared state marked broken → get() throws std::future_error(broken_promise)
    return f;
}
```

---

## Amdahl's Law and Gustafson's Law (C++11)

Per [ENG-6.1](laws/engineering/eng-6-security.md): before parallelising
crew scheduling optimisers or fare combinatorics, quantify the theoretical
speedup limit — over-parallelising a serial-bottlenecked algorithm wastes
engineering effort and can increase latency.

### Amdahl's Law

    Speedup(n) = 1 / (s + (1−s)/n)

`s` = serial fraction (0–1), `n` = number of parallel workers.

**Key insight: 20% serial code (s = 0.2) caps speedup at 5× regardless of
how many cores you add.**

| Serial fraction (s) | Max speedup (n → ∞) |
|---|---|
| 0.50 | 2× |
| 0.20 | **5×** |
| 0.10 | 10× |
| 0.01 | 100× |

### Gustafson's Law

    Scaled speedup(n) = n − s × (n − 1)

As the problem size grows with core count, efficiency holds even with a
fixed serial fraction. Applicable to AA fare combinatorics where the input
(routes × date range) scales with available compute.

### When NOT to Parallelize

- Serial fraction > 50% → < 2× gain; complexity not justified
- Task duration < ~1 ms → thread pool submission overhead dominates
- Data dependencies span the whole dataset → refactor the serial bottleneck first

### Measuring Serial Fraction

```cpp
// Profile with perf stat or VTune's Parallelism advisor.
// Identify the serial bottleneck; parallelise only that region.
// Rule: measure first, optimise second — never guess.
```

## See Also
- `ref-concurrency-advanced-part2.md` — C++20 concurrency: jthread, stop_token, coroutine safety

## Further Reading

> Further reading: Williams, *C++ Concurrency in Action* 2nd Ed. (2019, Manning) — the definitive
> practitioner reference for `std::atomic`, memory ordering models, and lock-free data structures.

> Further reading: Boehm & Adve, "Foundations of the C++ Concurrency Memory Model" (PLDI 2008) —
> formal basis for the C++11 memory model; explains acquire/release and sequentially consistent
> ordering from first principles.

> C++ Core Guidelines CP.* section: https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#cp-concurrency-and-parallelism
