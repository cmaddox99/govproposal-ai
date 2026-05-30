---
cpp_version_min: 11
cpp_version_note: >-
  Primary patterns use std::mutex and std::lock_guard (C++11). C++17 std::scoped_lock noted where used.
avatar: cpp
---

# C++ Avatar Reference: Concurrency and Threading

---

## Concurrency

Per [ENG-6.1](laws/engineering/eng-6-security.md), concurrent code must prevent data races by design. Use RAII synchronization and static analysis to enforce correctness.

**Core rules:**
- Use RAII lock guards — never raw `mutex.lock()`/`unlock()`
- Prefer `std::atomic` for simple shared state (counters, flags)
- Use ThreadSanitizer (TSan) in CI to detect data races at runtime
- Document synchronization contracts for shared data structures

```cpp
// GOOD — C++11: std::lock_guard for single-mutex RAII (all C++11+ projects)
class FlightStatusCache {
public:
    void update(FlightId id, FlightStatus status) {
        std::lock_guard<std::mutex> lock(mutex_);
        cache_[id] = status;
    }

    bool get(FlightId id, FlightStatus& out) const {
        std::lock_guard<std::mutex> lock(mutex_);
        auto it = cache_.find(id);
        if (it == cache_.end()) return false;
        out = it->second;
        return true;
    }

private:
    mutable std::mutex mutex_;
    std::unordered_map<FlightId, FlightStatus> cache_;
};

// GOOD — C++17 upgrade: std::scoped_lock (deadlock-safe for multiple mutexes)
// ★ C++17+ only — use std::lock_guard above for C++11/14 projects
class FlightStatusCache17 {
public:
    void update(FlightId id, FlightStatus status) {
        std::scoped_lock lock{mutex_};   // C++17: no template arg needed
        cache_[id] = status;
    }

private:
    mutable std::mutex mutex_;
    std::unordered_map<FlightId, FlightStatus> cache_;
};

// GOOD — std::atomic for simple shared counters (no mutex needed, all C++11+)
class RequestCounter {
public:
    void increment() { count_.fetch_add(1, std::memory_order_relaxed); }
    int64_t count() const { return count_.load(std::memory_order_relaxed); }

private:
    std::atomic<int64_t> count_{0};
};
```

**Race condition prevention checklist:**
- Every mutable shared field is protected by a mutex or is atomic
- Lock ordering is documented to prevent deadlocks (always acquire in consistent order)
- Critical sections are as small as possible — do not hold locks during I/O or computation
- TSan CI gate runs on every PR to catch data races early

---

## Exception Safety and Error Handling

Per [ENG-6.1](laws/engineering/eng-6-security.md) and [ENG-3.7](laws/engineering/eng-3-code-quality.md) (Error Handling Law), exception safety is a design constraint for all C++ code. Every public function must document its exception safety guarantee.

### Coming from Java: Exception Model Differences

| Java | C++ | Key Difference |
|------|-----|----------------|
| Checked exceptions (`throws IOException`) | No equivalent — all C++ exceptions are unchecked | `noexcept` is the inverse: declares what does NOT throw |
| `try-with-resources` (`try (var r = ...)`) | RAII — automatic, no special syntax | C++ is actually simpler here |
| `finally` block | No `finally` — RAII destructors replace it | Don't look for `finally`; write RAII wrappers instead |
| `Optional<T>` | `std::optional<T>` | Same concept, different API |
| Return error codes (rare in Java) | `std::expected<T, E>` (C++23) or `std::error_code` | C++ has richer error-return types |

**Which error strategy for which situation:**

| Situation | Java Pattern | C++ Pattern |
|-----------|-------------|-------------|
| Recoverable error on hot path | Checked exception | `std::expected<T, Error>` — no stack unwinding overhead |
| Unexpected failure (invariant broken) | `RuntimeException` | `throw` — let RAII unwind the stack |
| C API interop | N/A | `std::error_code` / `errno` |
| Value may not exist (no error info) | `Optional<T>` | `std::optional<T>` |
| Programming bug (should never happen) | `assert` | `assert()` or `std::terminate()` |

> **Rule for Java developers:** Default to exceptions (like Java), but switch to `std::expected` on performance-critical paths where stack unwinding is measurable. Never mix strategies within a single module boundary.

### Exception Safety Guarantee Levels

| Guarantee | Contract | Example |
|-----------|----------|---------|
| **Nothrow** | Never throws; marked `noexcept` | Destructors, `swap()`, move operations |
| **Strong** | On exception, state rolls back to pre-call | `push_back` with copy, transactional operations |
| **Basic** | On exception, invariants preserved but state may change | Most mutating operations |

### `noexcept` Contract Policy

The following MUST be declared `noexcept`:
- **Destructors** — always (compiler default since C++11)
- **Move constructors and move assignment operators** — enables efficient container operations
- **`swap()` functions** — required for strong guarantee implementations
- **Deallocation functions** — `operator delete`

```cpp
// COMPLIANT — move operations are noexcept
class FlightPlan {
public:
    FlightPlan(FlightPlan&& other) noexcept = default;
    FlightPlan& operator=(FlightPlan&& other) noexcept = default;
    ~FlightPlan() = default;  // implicitly noexcept
};
```

### Error Handling Decision Matrix

| Context | Strategy | Rationale |
|---------|----------|-----------|
| Domain logic (internal) | Exceptions (`std::runtime_error`, domain exceptions) | Natural flow; caught at use-case boundary |
| API boundary (public) | `std::expected<T,E>` (C++23) or error codes | Callers must handle; no hidden control flow |
| Resource cleanup | RAII (destructors) | Guaranteed cleanup regardless of exception path |
| Precondition violation | `assert` / `Expects()` (debug), throw (release) | Fail fast on programming errors |

When C++23 is not available, use a `Result<T,E>` type alias wrapping `std::variant<T,E>` or adopt `tl::expected` from vcpkg.

### Exception Boundary Policy

Exceptions are permitted within module boundaries. At service/API boundaries, catch and translate to error codes or `std::expected`. Per [ENG-6.7](laws/engineering/eng-6-security.md), exception occurrences at boundaries must be logged for audit.

---

## Termination and Recovery Policy

Per [ENG-7.1](laws/engineering/eng-7-reliability.md) (Failure Handling), C++ code must have an explicit policy for when to terminate vs. recover. Unrecoverable invariant violations must not be masked.

### Severity Classification

| Severity | Action | Example |
|----------|--------|---------|
| **Fatal / Unrecoverable** | `std::terminate()` immediately | Memory corruption detected, double-free, stack overflow, invariant violation in safety-critical data |
| **Critical / Service-level** | Log + circuit-break + alert | Database unreachable, external API timeout, certificate expiry |
| **Error / Request-level** | Return error to caller, log for audit | Invalid input, business rule violation, resource not found |
| **Warning / Degraded** | Log + continue with fallback | Cache miss (fall through to DB), non-critical config missing |

### `std::terminate` Policy

`std::terminate()` is the correct response when:
- Memory corruption is detected (ASan-like runtime checks in production)
- A `noexcept` function would throw (compiler calls `std::terminate` automatically)
- An invariant that protects downstream data integrity is violated
- Continuing execution would propagate corrupt state to other systems

**Never** call `std::terminate()` for recoverable business errors. Use exceptions or `std::expected` for those.

### Signal Handling

For production C++ services, install signal handlers for crash reporting:
- `SIGSEGV`, `SIGABRT`, `SIGBUS` — log stack trace + core dump, then terminate
- `SIGTERM` — initiate graceful shutdown (drain connections, flush logs)
- `SIGINT` — same as SIGTERM in production; immediate exit in development

---


---

## See Also

- [Concurrency Async and Resiliency Patterns](ref-concurrency-async.md)
- [Coroutines (C++20+)](../language/ref-concurrency-coroutines.md)
