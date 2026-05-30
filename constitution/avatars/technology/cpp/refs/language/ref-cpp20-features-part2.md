---
id: ref-cpp20-features-part2
cpp_version_min: 20
cpp_version_note: >-
  C++20 features Part 2: coroutine generators (co_yield), aggregate
  improvements, calendar/timezone with std::chrono and FAR 117 patterns.
  See Part 1 for modules, ranges, span, spaceship operator.
  See Part 3 for std::format, std::bit_cast, source_location, constinit, atomic_ref.
avatar: cpp
---

# C++20 Core Features — Part 2

> **Status:** Complete — all sections populated as part of the C++ External Sources Enrichment (ESE) proposal.
> See `hangar-ai-specs/changes/cpp-external-sources-enrichment/tasks.md`.

Per [ENG-2.2](laws/engineering/eng-2-architecture.md) (Architecture Law), all C++20
features must be introduced with governing context and migration guidance.

---

## Coroutine Generators (co_yield)

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md) (Complexity), `co_yield` generators
produce lazy sequences without allocating intermediate containers. This section covers the
`co_yield` generator pattern; for `co_await` task coroutines see
`coroutines.md`.

### co_yield Mechanics

A coroutine function becomes a generator when it uses `co_yield`. Each `co_yield expr`
suspends execution and delivers `expr` to the caller:

```cpp
// COMPLIANT — lazy generator over available flights for a route
Generator<FlightId> available_flights(std::string_view origin,
                                      std::string_view dest) {
    for (const auto& rec : flight_database()) {
        if (rec.origin == origin && rec.destination == dest && rec.has_seats)
            co_yield rec.id;    // ✅ suspends here; resumes on next iteration
    }
    // implicit co_return at end of function
}

// Usage — pulls one value at a time; no intermediate vector
for (const FlightId& id : available_flights("DFW", "LAX")) {
    if (book(id)) break;        // ✅ stop early; remaining flights never evaluated
}

// NON-COMPLIANT — eager: allocates full result vector before any booking attempt
std::vector<FlightId> flights = collect_available("DFW", "LAX");  // ❌ heap alloc
for (const auto& id : flights) { if (book(id)) break; }
```

### Generator\<T\> promise_type

C++20 does not ship `std::generator` (that is C++23). In C++20 you provide a minimal
`promise_type`:

```cpp
// COMPLIANT — minimal Generator<T> for C++20
template<typename T>
struct Generator {
    struct promise_type {
        T current_value;

        Generator get_return_object() {
            return Generator{
                std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_always final_suspend()   noexcept { return {}; }
        std::suspend_always yield_value(T v) {
            current_value = std::move(v);
            return {};
        }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };

    // Range interface
    struct iterator {
        std::coroutine_handle<promise_type> h;
        bool operator==(std::default_sentinel_t) const { return h.done(); }
        iterator& operator++() { h.resume(); return *this; }
        const T& operator*() const { return h.promise().current_value; }
    };
    iterator begin() { handle_.resume(); return {handle_}; }
    std::default_sentinel_t end() { return {}; }

    ~Generator() { if (handle_) handle_.destroy(); }

    // Move-only: copying a Generator would double-destroy the coroutine handle
    Generator(const Generator&)            = delete;
    Generator& operator=(const Generator&) = delete;
    Generator(Generator&& o) noexcept : handle_(std::exchange(o.handle_, {})) {}
    Generator& operator=(Generator&& o) noexcept {
        if (this != &o) { if (handle_) handle_.destroy(); handle_ = std::exchange(o.handle_, {}); }
        return *this;
    }
    // After move, moved-from generator has nullptr handle; do not iterate

private:
    explicit Generator(std::coroutine_handle<promise_type> h) : handle_(h) {}
    std::coroutine_handle<promise_type> handle_;
};
```

### Cancellable Generator with stop_token

```cpp
// COMPLIANT — generator respects cooperative cancellation
Generator<FlightId> available_flights_cancellable(
        std::string_view origin, std::string_view dest,
        std::stop_token stop) {
    for (const auto& rec : flight_database()) {
        if (stop.stop_requested()) co_return;   // ✅ cooperative cancellation
        if (rec.origin == origin && rec.destination == dest && rec.has_seats)
            co_yield rec.id;
    }
}
```

### std::generator (C++23 Preview)

C++23 ships `std::generator<T>` in `<generator>` — a standardised, optimised generator
that avoids the boilerplate above. Use it when your compiler/stdlib ships C++23:

```cpp
// C++23 — std::generator replaces the manual promise_type above
#include <generator>
std::generator<FlightId> available_flights(std::string_view origin,
                                           std::string_view dest) {
    for (const auto& rec : flight_database())
        if (rec.origin == origin && rec.destination == dest && rec.has_seats)
            co_yield rec.id;
}
```

**Migration path:** Write the `co_yield` logic now; swap `Generator<T>` for
`std::generator<T>` when upgrading to C++23 — the `co_yield` body is unchanged.

---

## See Also

---

## C++20 Aggregate Improvements

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), C++20 extends aggregates
with parenthesis initialization and CTAD, reducing friction between aggregate and non-aggregate usage.

**What changed in C++20:**

```cpp
struct FlightRequest {
    std::string origin;
    std::string dest;
    int passengers;
};

// C++20: parenthesis-init works for aggregates (as well as brace-init)
FlightRequest r1{"LAX", "DFW", 180};   // C++11+
FlightRequest r2("LAX", "DFW", 180);   // C++20 — same effect

// CTAD (Class Template Argument Deduction) with aggregates (C++20)
template<typename T>
struct Wrapper { T value; };
Wrapper w{42};          // deduced: Wrapper<int> — C++20 CTAD for aggregates
```

**Aggregate inheritance (C++20):** a class derived from an aggregate can itself be aggregate:

```cpp
struct NamedFlight : FlightRequest { std::string callsign; };
NamedFlight nf{"LAX", "DFW", 180, "AAL123"};  // designated or positional
```

**Interaction with designated initializers:** parenthesis-init does NOT support designated
syntax (`FlightRequest(.dest = "DFW")` is ill-formed); use brace-init for named fields.

| Init Style | Syntax | Designated? | Narrowing check |
|------------|--------|-------------|-----------------|
| Brace (C++11) | `{...}` | Yes (C++20) | Yes |
| Paren (C++20) | `(...)` | No | No |

## Calendar and Timezone (chrono C++20) — FAR 117

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), use `std::chrono` calendar
and timezone types for all aviation time math — FAR 117 duty period calculations require
timezone-aware arithmetic to avoid ambiguous or incorrect rest-time computations.

```cpp
#include <chrono>
using namespace std::chrono;

// year_month_day: calendar date arithmetic
year_month_day departure_date{2025y / January / 15d};

// Build LOCAL block-on time (08:00 local in DFW acclimation timezone)
// Use local_days to stay in local time — NOT sys_days (which is UTC)
auto tz_acc = locate_zone("America/Chicago");  // crew's acclimation timezone
// local_days + 8h yields local_time<hours>; implicitly widens to local_time<minutes> in zoned_time<minutes>
local_time<minutes> local_block_on{local_days{departure_date} + 8h};
zoned_time<minutes> block_on{tz_acc, local_block_on};

// Convert to UTC sys_time for FAR 117 comparison
sys_time<minutes> utc_block_on = block_on.get_sys_time();

// Duration arithmetic with hh_mm_ss
auto duty_duration = hours{14} + minutes{30};
hh_mm_ss<minutes> duty_hhmmss{duty_duration};
// duty_hhmmss.hours() == 14h, duty_hhmmss.minutes() == 30min
```

**Timezone database access:**

```cpp
// List all available timezone names
const auto& db = get_tzdb();
for (const auto& zone : db.zones) { /* ... */ }

// Convert local → UTC for crew rest window check
local_time<seconds> local_block_off{local_days{2025y/January/15d} + 22h};
zoned_time<seconds> zt{locate_zone("America/Los_Angeles"), local_block_off};
sys_time<seconds>   utc_bo = zt.get_sys_time();
```

**Aviation note:** FAR 117.25/117.27 rest requirements are enforced against the crewmember's
acclimation timezone; use `zoned_time` — never raw UTC offsets — to avoid DST errors.
`zoned_time` automatically handles DST transitions when converting local→UTC.
**Test cases must cover dates near DST boundaries** (spring-forward gap in March,
fall-back ambiguity in November) to verify correct rest-period calculations.

**DST spring-forward gap** — during spring-forward, local times in the gap (e.g., 2:00–3:00 AM)
do not exist. `zoned_time` throws `std::chrono::nonexistent_local_time`:

```cpp
try {
    zoned_time<minutes> zt{tz_acc, ambiguous_local};  // may throw
} catch (const std::chrono::nonexistent_local_time&) {
    // time falls in spring-forward gap — advance to post-transition time
    // per FAR 117 operational procedure (coordinate with crew scheduling)
}
```

## See Also

- `ref-cpp20-features-part1.md` — modules, format, span, ranges, spaceship, bit_cast
- `coroutines.md` — `co_await` task coroutines and async patterns

