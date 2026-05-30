---
law_id: ENG-6.1
cpp_version_min: 20
cpp_version_note: >-
  Uses C++20 std::jthread (auto-joining, stop_token). Transitional teams: use std::thread with manual join; brownfield: use CRITICAL_SECTION/RAII wrapper.
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md) — Thread API Migration

**The Rule:** Platform-specific threading APIs (`pthread_*`, Win32 threads) must be replaced with portable C++ standard alternatives. Raw threads lack RAII — if an exception occurs between `pthread_create` and `pthread_join`, the thread is never joined and resources leak.

**Note:** `std::jthread` (C++20) is like Java's `Thread` with built-in interruption (`stop_token` ≈ `Thread.interrupt()`). For C++11, use `std::thread` + a manual RAII wrapper to ensure `join()` is called.

**When to use which:**
- **C++20+ (preferred):** `std::jthread` — automatic join on destruction + built-in cancellation via `stop_token`
- **C++11-17:** `std::thread` with a RAII join guard — you MUST join or detach before the `thread` destructor runs, or `std::terminate` is called
- **Legacy C++98:** Keep `pthread_*` but wrap in RAII class with explicit join in destructor; plan migration to C++11+

## NON-COMPLIANT: POSIX Threads (C++98)

```cpp
void* worker(void* arg) {
    auto* data = static_cast<WorkItem*>(arg);
    data->process();  // no type safety, no exception safety
    return nullptr;
}

pthread_t thread;
pthread_create(&thread, nullptr, worker, &work_item);
// ❌ if exception occurs here, thread is never joined → resource leak
pthread_join(thread, nullptr);
```

## COMPLIANT: std::jthread (C++20) / std::thread (C++11)

```cpp
// C++20: jthread with automatic join + stop token
std::jthread worker([&work_item](std::stop_token st) {
    while (!st.stop_requested()) {
        work_item.process_next();
    }
});
// destructor requests stop and joins — no leak possible

// C++11 minimum: thread with RAII join guard
std::thread worker([&work_item]() { work_item.process(); });
// MUST join or detach before destruction — std::terminate otherwise
struct JoinGuard {
    std::thread& t;
    ~JoinGuard() { if (t.joinable()) t.join(); }
};
JoinGuard guard{worker};
```

**⚠️ Edge cases:**
- **Never detach threads that capture local references** — the detached thread outlives the scope and reads dangling memory (use-after-free)
- Replace `pthread_mutex_*` → `std::mutex` + `std::scoped_lock`; `pthread_cond_*` → `std::condition_variable`
- `std::jthread` destructor calls `request_stop()` then `join()` — if your worker ignores the stop token, the destructor blocks forever

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| `pthread_cancel` called on a thread that has C++ objects with destructors | `pthread_cancel` uses async cancellation by default; C++ destructors may not run, leaking resources | Replace `pthread_cancel` with a `std::atomic<bool>` stop flag checked inside the thread loop; use `std::jthread` stop token for C++20 |
| POSIX thread priority (`SCHED_FIFO`) not available for `std::thread` | `std::thread` has no portable priority API; migrated code silently loses priority — real-time scheduling broken | After constructing `std::thread`, call `pthread_setschedparam` on `thread.native_handle()` and assert success |
| Detached pthread migrated to `std::thread::detach()` outlives `main()` | `std::thread::detach()` does not prevent the thread from reading globals destroyed during static-storage teardown | Prefer `std::jthread` with cooperative stop; if detach is unavoidable, ensure the thread holds no references to objects with static duration |
