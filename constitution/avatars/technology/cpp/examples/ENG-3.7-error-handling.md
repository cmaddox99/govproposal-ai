---
law_id: ENG-3.7
cpp_version_min: 23
cpp_version_note: >-
  Uses C++23 std::expected. Transitional teams: use enum class error codes with output parameters; brownfield teams: use exception-based error paths.
avatar: cpp
title: Error Handling — C++ Patterns
tokens: ~450
---

# ENG-3.7 Error Handling — C++ Patterns

**Law:** ENG-3.7 (Error Handling Law)  
**Avatar:** `avatars/technology/cpp/`  

---

## Core Rule

C++ code MUST communicate failure through the return type, not side-channel state.
Exceptions are permitted only at integration boundaries (JNI, OS API, third-party).
All internal domain logic uses value-based error representation.

---

## COMPLIANT Patterns

### 1. `std::expected<T, E>` (C++23 / backport via tl::expected)

```cpp
// Preferred for C++23 greenfield
#include <expected>

std::expected<FlightPlan, SchedulingError>
build_flight_plan(const FlightRequest& req) {
    if (!req.is_valid())
        return std::unexpected(SchedulingError::InvalidRequest);
    return FlightPlan{req};
}

// Call site — error is visible in the type
auto plan = build_flight_plan(req);
if (!plan) handle_error(plan.error());
```

### 2. Error Code + `noexcept` (C++11/14 brownfield, CWR)

```cpp
enum class CrewError { None, Unavailable, RestViolation, NotQualified };

// noexcept contract: function CANNOT throw — callers need not catch
CrewError assign_crew(FlightId flight, CrewId crew) noexcept {
    if (!is_available(crew)) return CrewError::Unavailable;
    if (violates_rest(crew, flight)) return CrewError::RestViolation;
    roster_.emplace(flight, crew);
    return CrewError::None;
}
```

### 3. RAII Safety on Error Paths

```cpp
// Destructor always runs — resource never leaks on error return
class ScopedCrewLock {
    CrewId id_;
public:
    explicit ScopedCrewLock(CrewId id) : id_(id) { lock(id_); }
    ~ScopedCrewLock() { unlock(id_); }                // runs on return OR exception
    ScopedCrewLock(const ScopedCrewLock&) = delete;   // non-copyable lock
};

CrewError reserve_crew(CrewId id) noexcept {
    ScopedCrewLock guard(id);          // unlocks on any return path
    if (!is_available(id)) return CrewError::Unavailable;
    mark_reserved(id);
    return CrewError::None;
}
```

---

## NON-COMPLIANT Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| `int` return code with no enum | Callers ignore silently | Use `enum class ErrorCode` |
| `throw` inside `noexcept` function | Calls `std::terminate` | Remove `noexcept` or don't throw |
| Global `errno`-style state | Not thread-safe | Return value per call |
| Empty catch block `catch(...){}` | Swallows errors invisibly | Log + rethrow or return error |

---

## CWR Brownfield Path

CWR uses C++03 — `std::expected` unavailable. Use:
1. **Error code enums** as return type (`CrewError`, `SchedulingError`)
2. **`noexcept` annotation** on all domain functions (C++11 available in CWR)
3. **Output-parameter pattern** only at legacy API boundaries — never for new code

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| `std::expected<void, E>` in a monadic chain where an intermediate step returns `void` | `.and_then([](){ ... })` on `expected<void,E>` requires the lambda to return `expected<void,E>`, not `void`; incorrect return type produces a cryptic template error | Explicitly return `std::expected<void, E>{}` (success) from `void`-returning lambdas in the chain |
| Exception-neutral library code mixed with `std::expected`-returning callers | The library throws; the caller catches nothing; the exception propagates past the `expected` boundary, bypassing all error-handling logic | Wrap exception-throwing calls in a try/catch at the integration point; convert exceptions to `std::unexpected` before they cross the `expected` boundary |
| Error code enum sliced in an inheritance hierarchy (derived error not representable in base enum) | Caller receives a base enum value that cannot represent the derived error; detail is lost; debugging is impossible | Use a sum type (`std::variant<DerivedError1, DerivedError2>`) or error-code category objects rather than inheritance for error taxonomies |
