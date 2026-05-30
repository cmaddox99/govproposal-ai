---
law_id: ENG-6.1
cpp_version_min: 14
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md) — Legacy C++98 to Modern C++11 Before/After

## The Rule

Modernize legacy C++98/03 patterns **incrementally, one pattern at a time**. Each change should be a safe, isolated improvement that can be reviewed and tested independently.

## Practical Context — Safest Migration Order

Apply changes in this priority order (safest first):

1. **`NULL` → `nullptr`** — Pure type fix, zero risk
2. **`#define` → `constexpr`** — Eliminates macro bugs, no behavior change
3. **`typedef` → `using`** — Readability, no behavior change
4. **Manual iterator → range-for** — Eliminates off-by-one, easy to verify
5. **`virtual` → `override`** — Catches silent signature mismatches at compile time
6. **`new`/`delete` → `unique_ptr`** — Requires ownership analysis (do last)

## NON-COMPLIANT / COMPLIANT: Side-by-Side

```cpp
// 1. NULL → nullptr
FlightPlan* plan = NULL;       // ❌ implicit int conversion possible
FlightPlan* plan = nullptr;    // why: type-safe, no implicit conversions

// 2. typedef → using
typedef std::vector<Flight> FlightList;          // ❌ opaque syntax
using FlightList = std::vector<Flight>;          // why: clearer, supports templates

// 3. Manual iterator → range-for
for (std::vector<Flight>::iterator it = flights.begin();
     it != flights.end(); ++it) {
    process(*it);                                // ❌ verbose, off-by-one risk
}
for (const auto& flight : flights) {
    process(flight);                             // why: no iterator bugs, intent is clear
}

// 4. #define → constexpr
#define MAX_PASSENGERS 189                       // ❌ no type, no scope, no debugger visibility
constexpr int kMaxPassengers = 189;              // why: typed, scoped, debuggable

// 5. virtual → override
virtual void on_delay(int minutes);              // ❌ silent mismatch if base changes signature
void on_delay(int minutes) override;             // why: compiler error on signature mismatch

// 6. C callback → std::function + lambda
void register_callback(void(*fn)(int, void*), void* ctx);  // ❌ void* loses type safety
void register_callback(std::function<void(int)> fn);        // why: type-safe, captures context

// 7. new/delete → unique_ptr
FlightPlan* p = new FlightPlan();               // ❌ leak on any throw between new and delete
auto p = std::make_unique<FlightPlan>();         // why: RAII — exception-safe by construction
```

## Edge Cases & Warnings

| Scenario | Guidance |
|----------|----------|
| Batch-rewriting untouched files | **Don't.** Only modernize files you are already changing — reduces review noise and regression risk. |
| `override` on destructors | Use `override` on virtual destructors too — catches missing `virtual` on base. |
| `std::function` overhead | Has heap allocation. In tight loops, prefer templates or `std::move_only_function` (C++23). |
| `constexpr` vs `const` | Use `constexpr` for compile-time constants. Use `const` for runtime-immutable values. |

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Modernisation introduces an ABI break invisible to unit tests | Changing `int` to `int32_t` in a public header recompiles cleanly but breaks calling code compiled against the old header | Run ABI compliance checks (`abi-compliance-checker` or `abidiff`) as part of the modernisation PR |
| Applying `noexcept` to a legacy function that does internally throw | The program calls `std::terminate` instead of propagating the exception; behaviour changes silently | Only add `noexcept` after confirming no code path throws; add a test with an error-injecting mock |
| Modernisation of a hot path degrades performance | `std::string` replace of a `char[]` buffer adds heap allocations on every request | Profile before and after with perf/callgrind; keep the old implementation behind a flag until the profile confirms no regression |
