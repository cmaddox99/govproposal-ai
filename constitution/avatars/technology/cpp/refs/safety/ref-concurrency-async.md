---
cpp_version_min: 11
cpp_version_note: >-
  Async patterns primary: C++17 std::async. C++11 condition_variable fallback included.
avatar: cpp
---

# C++ Avatar Reference: Async and Resiliency Patterns

---

## Resiliency Patterns

C++ services lack framework-level resiliency defaults (unlike Spring Boot or .NET Polly). Per [ENG-7.1](laws/engineering/eng-7-reliability.md) (Failure Handling), every C++ service that makes external calls **must** implement explicit resiliency patterns. Unlike Java/Python ecosystems where these patterns come from libraries, C++ teams must build or adopt them deliberately.

> ⚠️ **Simplification-first:** Before implementing custom resiliency logic, evaluate whether an existing library (gRPC retry policy, Envoy sidecar, or AWS SDK retry config) already provides the pattern. Only implement in-process when latency or control requirements demand it.

### Circuit Breaker ([ENG-7.2](laws/engineering/eng-7-reliability.md))

Per [ENG-7.2](laws/engineering/eng-7-reliability.md) (Circuit Breaker Law), calls to external dependencies must be protected by a circuit breaker to prevent cascade failures. The circuit breaker has three states: **Closed** (requests flow), **Open** (requests fail fast), **Half-Open** (probe to test recovery).

```cpp
// COMPLIANT — Circuit breaker with atomic state machine
class CircuitBreaker {
public:
    enum class State { Closed, Open, HalfOpen };

    explicit CircuitBreaker(int failure_threshold = 5,
                            std::chrono::seconds recovery_timeout = std::chrono::seconds{30})
        : failure_threshold_{failure_threshold},
          recovery_timeout_{recovery_timeout} {}

    template <typename Func>
    auto call(Func&& fn) -> decltype(fn()) {
        if (state_.load() == State::Open) {
            if (Clock::now() - last_failure_time_.load() > recovery_timeout_) {
                state_.store(State::HalfOpen);
            } else {
                throw CircuitOpenException{"circuit breaker is open"};
            }
        }
        try {
            auto result = fn();
            on_success();
            return result;
        } catch (...) {
            on_failure();
            throw;
        }
    }

private:
    using Clock = std::chrono::steady_clock;
    void on_success() {
        failure_count_.store(0);
        state_.store(State::Closed);
    }
    void on_failure() {
        last_failure_time_.store(Clock::now());
        if (++failure_count_ >= failure_threshold_) {
            state_.store(State::Open);
        }
    }
    int failure_threshold_;
    std::chrono::seconds recovery_timeout_;
    std::atomic<State> state_{State::Closed};
    std::atomic<int> failure_count_{0};
    std::atomic<Clock::time_point> last_failure_time_{};
};
```

```cpp
// NON-COMPLIANT — no circuit breaker on external call
auto result = http_client.get(url);  // cascade failure if service is down
```

**Governance rules:**
- Every external HTTP, gRPC, or database call must use a circuit breaker
- Circuit breaker thresholds must be configurable (not hardcoded)
- Metrics: expose `circuit_open_total`, `circuit_half_open_total` counters per [ENG-5.5](laws/engineering/eng-5-devops.md)
- Test circuit breaker transitions with GoogleTest (inject failures)

### Retry with Exponential Backoff ([ENG-7.3](laws/engineering/eng-7-reliability.md))

Per [ENG-7.3](laws/engineering/eng-7-reliability.md) (Retry/Backoff Law), transient failures must be retried with exponential backoff and jitter to prevent thundering-herd effects.

```cpp
// COMPLIANT — Exponential backoff with jitter
template <typename Func>
auto retry_with_backoff(Func&& fn,
                        int max_retries = 3,
                        std::chrono::milliseconds base_delay = std::chrono::milliseconds{100})
    -> decltype(fn())
{
    static thread_local std::mt19937 rng{std::random_device{}()};

    for (int attempt = 0; attempt <= max_retries; ++attempt) {
        try {
            return fn();
        } catch (const TransientException&) {
            if (attempt == max_retries) throw;
            auto delay = base_delay * (1 << attempt);  // exponential
            auto jitter = std::chrono::milliseconds{
                std::uniform_int_distribution<int>{0, static_cast<int>(delay.count() / 2)}(rng)
            };
            std::this_thread::sleep_for(delay + jitter);
        }
    }
    __builtin_unreachable();  // silence compiler warning
}
```

```cpp
// NON-COMPLIANT — fixed-delay retry (thundering herd)
for (int i = 0; i < 3; ++i) {
    try { return fetch(url); }
    catch (...) { std::this_thread::sleep_for(1s); }  // all retries hit at same time
}
```

**Governance rules:**
- Retries MUST use exponential backoff (not fixed delay)
- Jitter MUST be added to prevent synchronized retry storms
- Maximum retry count and base delay must be configurable
- Only retry on transient errors — never retry on authentication or validation failures
- Log each retry attempt with attempt number for audit per [ENG-6.7](laws/engineering/eng-6-security.md)

### Timeout Governance ([ENG-7.4](laws/engineering/eng-7-reliability.md))

Per [ENG-7.4](laws/engineering/eng-7-reliability.md) (Timeout Law), every external call must have an explicit timeout. No call may block indefinitely.

```cpp
// COMPLIANT — Timeout with deadline propagation
template <typename Func>
auto with_timeout(Func&& fn,
                  std::chrono::milliseconds timeout) -> std::optional<decltype(fn())>
{
    auto future = std::async(std::launch::async, std::forward<Func>(fn));
    if (future.wait_for(timeout) == std::future_status::ready) {
        return future.get();
    }
    return std::nullopt;  // timed out — caller decides recovery
}

// Usage — every external call has explicit timeout
auto flight_data = with_timeout(
    [&] { return sabre_client.get_availability(criteria); },
    std::chrono::seconds{5}
);
if (!flight_data) {
    log::warn("Sabre availability timed out after 5s");
    return cached_fallback(criteria);
}
```

```cpp
// NON-COMPLIANT — blocking call with no timeout
auto result = client.get(url);  // blocks forever if remote hangs
```

**Governance rules:**
- Every network call, database query, and file I/O operation must have an explicit timeout
- Timeouts must be configurable per dependency (not a single global value)
- When a deadline is propagated from an upstream caller (e.g., gRPC deadline), child calls must respect the remaining budget
- Prefer `std::chrono` duration types over raw integers for timeout values per [ENG-3.1](laws/engineering/eng-3-code-quality.md)
- Log timeout events with dependency name and configured timeout value

### Bulkhead Isolation ([ENG-7.5](laws/engineering/eng-7-reliability.md))

Per [ENG-7.5](laws/engineering/eng-7-reliability.md) (Bulkhead Law), failures in one dependency must not exhaust resources needed by others. Use thread pool or semaphore isolation.

```cpp
// COMPLIANT — Semaphore-based bulkhead (C++20)
class Bulkhead {
public:
    explicit Bulkhead(int max_concurrent) : semaphore_{max_concurrent} {}

    template <typename Func>
    auto call(Func&& fn, std::chrono::milliseconds timeout = std::chrono::seconds{5})
        -> std::optional<decltype(fn())>
    {
        if (!semaphore_.try_acquire_for(timeout)) {
            return std::nullopt;  // bulkhead full — shed load
        }
        auto guard = ScopeGuard{[this] { semaphore_.release(); }};
        return fn();
    }

private:
    std::counting_semaphore<> semaphore_;
};

// Usage — separate bulkheads per dependency
Bulkhead sabre_bulkhead{10};    // max 10 concurrent Sabre calls
Bulkhead amadeus_bulkhead{5};   // max 5 concurrent Amadeus calls
```

```cpp
// COMPLIANT — C++11/17 fallback: condition_variable-based semaphore
class Semaphore {
public:
    explicit Semaphore(int count) : count_{count} {}

    bool try_acquire_for(std::chrono::milliseconds timeout) {
        std::unique_lock<std::mutex> lock{mutex_};
        return cv_.wait_for(lock, timeout, [this] { return count_ > 0; })
               && (--count_, true);
    }
    void release() {
        std::lock_guard<std::mutex> lock{mutex_};
        ++count_;
        cv_.notify_one();
    }

private:
    std::mutex mutex_;
    std::condition_variable cv_;
    int count_;
};

class BulkheadCpp11 {
public:
    explicit BulkheadCpp11(int max_concurrent) : sem_{max_concurrent} {}

    template <typename Func>
    auto call(Func&& fn, std::chrono::milliseconds timeout = std::chrono::seconds{5})
        -> std::optional<decltype(fn())>
    {
        if (!sem_.try_acquire_for(timeout)) return std::nullopt;
        struct Guard { Semaphore& s; ~Guard() { s.release(); } } guard{sem_};
        return fn();
    }

private:
    Semaphore sem_;
};
```

```cpp
// NON-COMPLIANT — shared thread pool for all dependencies
auto pool = ThreadPool{20};
pool.submit([&] { return sabre.call(); });   // Sabre outage...
pool.submit([&] { return amadeus.call(); }); // ...starves Amadeus
```

**Governance rules:**
- Each external dependency must have an isolated concurrency limit
- Use `std::counting_semaphore` (C++20) or the `condition_variable`-based `Semaphore` (C++11/17) per dependency
- Configure bulkhead sizes based on dependency SLA and capacity
- When a bulkhead rejects a request, return a degraded response (not an error) when possible

### Idempotency ([ENG-7.6](laws/engineering/eng-7-reliability.md))

Per [ENG-7.6](laws/engineering/eng-7-reliability.md) (Idempotency Law), operations that may be retried must be idempotent — producing the same result regardless of how many times they execute.

```cpp
// COMPLIANT — Idempotent operation with request deduplication
class BookingService {
public:
    BookingResult create_booking(const IdempotencyKey& key,
                                 const BookingRequest& request) {
        // Check if already processed
        if (auto existing = cache_.get(key)) {
            return *existing;  // return cached result — idempotent
        }
        auto result = process_booking(request);
        cache_.put(key, result, /*ttl=*/std::chrono::hours{24});
        return result;
    }
private:
    IdempotencyCache cache_;
};
```

**Governance rules:**
- All POST/PUT handlers in C++ services must accept an idempotency key
- Use atomic compare-and-swap for in-memory deduplication in high-throughput paths
- Idempotency cache TTL must match the retry window (typically 24h)
- Database operations: use `INSERT ... ON CONFLICT DO NOTHING` or equivalent
- Document which operations are idempotent in API contracts per [ENG-1.5](laws/engineering/eng-1-core-principles.md)

---

## See Also

- [Safety-Critical & Memory](ref-safety-memory.md)
- [Advanced C++ Patterns](ref-advanced-cpp.md)


---

## See Also

- [Concurrency and Threading](ref-concurrency-threading.md)
