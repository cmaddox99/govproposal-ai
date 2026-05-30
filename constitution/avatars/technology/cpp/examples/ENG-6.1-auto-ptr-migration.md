---
law_id: ENG-6.1
cpp_version_min: 14
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md) — auto_ptr to unique_ptr Migration

## The Rule

`std::auto_ptr` is **removed** in C++17 and was deprecated since C++11. Every `auto_ptr` must be migrated to `std::unique_ptr` with explicit `std::move()` semantics.

## When to Use

Apply this migration to **any C++98/03 codebase** being modernized. Prioritize it early — `auto_ptr` removal is a prerequisite for compiling under `-std=c++17` or later.

## NON-COMPLIANT: auto_ptr (C++98)

```cpp
// ❌ auto_ptr transfers ownership on COPY — silent and deadly
std::auto_ptr<FlightPlan> plan1(new FlightPlan("AA100"));
std::auto_ptr<FlightPlan> plan2 = plan1;  // ❌ plan1 is now NULL — no compiler warning
plan1->get_route();                        // ❌ UNDEFINED BEHAVIOR: null dereference

// ❌ auto_ptr in containers was ALWAYS undefined behavior
std::vector<std::auto_ptr<Flight>> flights;  // ❌ UB — sort/copy corrupts pointers
```

## COMPLIANT: unique_ptr (C++11+)

```cpp
// unique_ptr makes transfer EXPLICIT via std::move
auto plan1 = std::make_unique<FlightPlan>("AA100");  // why: factory avoids naked new
auto plan2 = std::move(plan1);                        // why: ownership transfer is visible
// plan1 is now nullptr — compiler helps prevent misuse
if (plan1) plan1->get_route();                        // why: guarded access prevents UB

// Containers work correctly with unique_ptr
std::vector<std::unique_ptr<Flight>> flights;         // why: move semantics are well-defined
flights.push_back(std::make_unique<Flight>("AA100")); // why: vector owns each element
```

## Edge Cases & Warnings

| Scenario | Guidance |
|----------|----------|
| `auto_ptr` in containers | Was **always UB** even in C++98 — sort/resize silently corrupted pointers. Replace with `vector<unique_ptr<T>>`. |
| Sed-replace `auto_ptr` → `unique_ptr` | **Never** do a blind find-replace. Review each site — if code relied on copy-transfer, add explicit `std::move()`. |
| `auto_ptr` in function returns | Direct replacement works — C++11 move semantics handle return-by-value naturally. |
| Third-party headers using `auto_ptr` | Wrap at the boundary: accept `auto_ptr`, immediately convert to `unique_ptr` inside your code. |
