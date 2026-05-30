---
cpp_version_min: 98
cpp_version_note: >-
  C++98/03 POSIX and Win32 threading patterns for pre-C++11 codebases.
avatar: cpp
---

# C++ Avatar Reference: Brownfield Concurrency (C++98/03 and POSIX/Windows)

> 📌 **C++98/03 and legacy teams.** This reference documents safe patterns for code that
> cannot migrate to C++11 threading primitives. For C++11+ projects see
> [ref-concurrency-threading.md](../safety/ref-concurrency-threading.md).

---

## Context

The C++ Standard Library had **no threading support before C++11**. Legacy and brownfield
codebases use POSIX threads (`pthread`) on Linux/macOS or Win32 threading primitives on
Windows. Per [ENG-6.1](laws/engineering/eng-6-security.md), these APIs must still follow
the RAII principle — wrap every primitive in a scoped guard.

Failing to do so introduces data races and resource leaks that are notoriously difficult
to detect. Use ThreadSanitizer (TSan) in CI to catch races early, even in C++98 code.
C++11 standardized these primitives as `std::mutex`, `std::lock_guard<std::mutex>`,
`std::condition_variable`, and `std::atomic`. Use the migration table at the end of
this file when a module is ready to upgrade.

---

## POSIX Threading Patterns (`pthread`)

Per [ENG-6.1](laws/engineering/eng-6-security.md), wrap every `pthread` primitive in an RAII guard — never call `pthread_mutex_lock` without a corresponding `pthread_mutex_unlock` on every path.

### Mutex with RAII Guard

```cpp
// POSIX mutex — C++98 RAII wrapper (no exceptions in destructor)
class PosixMutex {
public:
    PosixMutex()  { pthread_mutex_init(&m_, nullptr); }
    ~PosixMutex() { pthread_mutex_destroy(&m_); }

    void lock()   { pthread_mutex_lock(&m_); }
    void unlock() { pthread_mutex_unlock(&m_); }

private:
    pthread_mutex_t m_;
    PosixMutex(const PosixMutex&);            // non-copyable
    PosixMutex& operator=(const PosixMutex&); // non-copyable
};

// RAII lock guard
class PosixLockGuard {
public:
    explicit PosixLockGuard(PosixMutex& m) : m_(m) { m_.lock(); }
    ~PosixLockGuard() { m_.unlock(); }
private:
    PosixMutex& m_;
    PosixLockGuard(const PosixLockGuard&);
    PosixLockGuard& operator=(const PosixLockGuard&);
};

// GOOD — RAII guard; mutex unlocked even on early return or exception
void FlightCache::update(const std::string& key, const FlightData& data) {
    PosixLockGuard lock(mutex_);
    cache_[key] = data;
}
```

### Condition Variable (pthread_cond_t)

```cpp
// GOOD — condition variable with predicate loop (guards against spurious wakeup)
class WorkQueue {
public:
    void push(const WorkItem& item) {
        PosixLockGuard lock(mutex_);
        queue_.push_back(item);
        pthread_cond_signal(&cond_);
    }

    WorkItem pop() {
        PosixLockGuard lock(mutex_);
        while (queue_.empty()) {
            pthread_mutex_lock(&mutex_.raw());  // cond_wait needs raw mutex
            pthread_cond_wait(&cond_, &mutex_.raw());
        }
        WorkItem item = queue_.front();
        queue_.pop_front();
        return item;
    }

private:
    PosixMutex mutex_;
    pthread_cond_t cond_;
    std::deque<WorkItem> queue_;
};
```

### Read-Write Lock

```cpp
// For read-heavy data shared across many threads
class RWLock {
public:
    RWLock()  { pthread_rwlock_init(&lock_, nullptr); }
    ~RWLock() { pthread_rwlock_destroy(&lock_); }

    void read_lock()    { pthread_rwlock_rdlock(&lock_); }
    void write_lock()   { pthread_rwlock_wrlock(&lock_); }
    void unlock()       { pthread_rwlock_unlock(&lock_); }

private:
    pthread_rwlock_t lock_;
};
```

---

## Windows Threading Patterns (Win32)

Per [ENG-6.1](laws/engineering/eng-6-security.md), apply RAII to Win32 handles — always pair `InitializeCriticalSection` with `DeleteCriticalSection` and `CreateEvent` with `CloseHandle`.

```cpp
// CRITICAL_SECTION — lower overhead than HANDLE-based mutex for in-process locking
class Win32CriticalSection {
public:
    Win32CriticalSection()  { InitializeCriticalSection(&cs_); }
    ~Win32CriticalSection() { DeleteCriticalSection(&cs_); }

    void lock()   { EnterCriticalSection(&cs_); }
    void unlock() { LeaveCriticalSection(&cs_); }

private:
    CRITICAL_SECTION cs_;
};

// Event-based signaling (replaces condition_variable for Win32-only code)
class Win32Event {
public:
    explicit Win32Event(bool manual_reset = false)
        : handle_(CreateEvent(nullptr, manual_reset, FALSE, nullptr)) {}
    ~Win32Event() { if (handle_) CloseHandle(handle_); }

    void signal()                                    { SetEvent(handle_); }
    bool wait(DWORD timeout_ms = INFINITE) {
        return WaitForSingleObject(handle_, timeout_ms) == WAIT_OBJECT_0;
    }

private:
    HANDLE handle_;
};
```

---

## ⚠️ `volatile` Is NOT Atomic — Critical Pitfall

Per [ENG-6.1](laws/engineering/eng-6-security.md), `volatile` is not a synchronization primitive. Using it as a substitute for a mutex or atomic is a data race.

```cpp
// NON-COMPLIANT — volatile does NOT provide atomicity or memory ordering
volatile int g_counter = 0;
void increment() { ++g_counter; }  // ❌ read-modify-write is NOT atomic

// NON-COMPLIANT — volatile does NOT prevent data races
volatile bool g_done = false;
void worker() {
    while (!g_done) { /* spin */ }  // ❌ compiler may cache g_done in register
}
```

**Why volatile fails:**
- `volatile` only prevents the *compiler* from caching a value in a register; it says nothing about CPU caches or memory ordering between threads
- On modern multi-core CPUs, a write by thread A may not be visible to thread B even with `volatile`
- `++g_counter` compiles to three instructions (read, add, write) — another thread can interleave between them

```cpp
// COMPLIANT — use mutex for counters (C++98)
PosixLockGuard lock(mutex_);
++counter_;

// COMPLIANT — C++11 upgrade path: std::atomic (use when migrating)
// std::atomic<int> counter_{0};
// counter_.fetch_add(1, std::memory_order_relaxed);
```

---

## Safe Static Initialization (C++98)

Per [ENG-6.1](laws/engineering/eng-6-security.md), singleton initialization must be thread-safe. In C++98 use `pthread_once`; in C++11+ local statics are guaranteed thread-safe by the standard.

C++11 guarantees that local statics are initialized exactly once. In C++98 this is
**not** guaranteed across threads. Use `pthread_once` or a mutex-protected singleton.

```cpp
// COMPLIANT — pthread_once for thread-safe singleton (C++98)
static pthread_once_t g_init_once = PTHREAD_ONCE_INIT;
static ConfigRegistry* g_registry = nullptr;

static void init_registry() {
    g_registry = new ConfigRegistry();
}

ConfigRegistry& ConfigRegistry::instance() {
    pthread_once(&g_init_once, init_registry);
    return *g_registry;
}

// NON-COMPLIANT — double-checked locking WITHOUT memory barriers (C++98)
// The compiler or CPU may reorder the store to g_instance before
// the object's constructor has finished — another thread sees a non-null
// but uninitialised pointer.
static ConfigRegistry* g_instance = nullptr;
static PosixMutex g_mutex;

ConfigRegistry* get() {
    if (!g_instance) {                 // ❌ first check outside lock
        PosixLockGuard lock(g_mutex);
        if (!g_instance) {
            g_instance = new ConfigRegistry();  // ❌ reorder risk
        }
    }
    return g_instance;
}
```

---

## Migration Path to C++11

Per [ENG-6.1](laws/engineering/eng-6-security.md), migrate threading primitives module-by-module. Do not mix POSIX and C++11 primitives protecting the same data.

When a module is ready to adopt C++11 threading, replace primitives in this order:

| Brownfield Primitive | C++11 Replacement |
|---------------------|-------------------|
| `PosixMutex` / `CRITICAL_SECTION` | `std::mutex` |
| `PosixLockGuard` | `std::lock_guard<std::mutex>` |
| `pthread_cond_t` / `Win32Event` | `std::condition_variable` |
| `volatile` counter | `std::atomic<int>` |
| `pthread_once` singleton | Local static (thread-safe by standard) |
| `pthread_rwlock_t` | `std::shared_mutex` (C++17) |

See [ref-concurrency-threading.md](../safety/ref-concurrency-threading.md) for C++11+ patterns.

---

## See Also

- [ref-legacy-navigation.md](ref-legacy-navigation.md) — broader brownfield navigation strategies
- [ref-migration-pre-cpp17.md](ref-migration-pre-cpp17.md) — step-by-step modernization approach
- [ref-concurrency-threading.md](../safety/ref-concurrency-threading.md) — C++11+ threading (std::mutex, std::lock_guard)
