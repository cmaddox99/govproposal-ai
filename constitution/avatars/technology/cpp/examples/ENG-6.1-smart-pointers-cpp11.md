---
law_id: ENG-6.1
cpp_version_min: 11
cpp_version_note: >-
  C++11 smart pointer patterns using unique_ptr<T>(new T(...)) — the safe
  construction idiom before make_unique arrived in C++14. Also covers
  shared_ptr, weak_ptr, and custom deleters available since C++11.
  C++14 teams: prefer make_unique. C++17+: prefer make_shared.
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): Security by Design — Smart Pointers (C++11)

> ⚠️ **Version-sensitive.** `std::make_unique` requires C++14. If your project is
> C++11, use `std::unique_ptr<T>(new T(...))` — the safe two-step pattern shown below.
> Confirm your standard with `cpp.standard` in `.copilot/project.yaml`.

---

## COMPLIANT (C++11): `unique_ptr` with Manual `new`

```cpp
#include <memory>
#include <string>

class FlightPlan {
    std::string origin_;
    std::string destination_;
    int passengers_;
public:
    FlightPlan(std::string o, std::string d, int p)
        : origin_(std::move(o)), destination_(std::move(d)), passengers_(p) {}

    const std::string& origin() const { return origin_; }
};

// ── C++11: unique_ptr with explicit new ──────────────────────────────────────
// Two-step: allocation and ownership transfer are separate expressions.
// Safe because unique_ptr takes ownership before anything can throw.
std::unique_ptr<FlightPlan> plan(new FlightPlan("DFW", "ORD", 150));

// ── C++14+: prefer make_unique ───────────────────────────────────────────────
// auto plan = std::make_unique<FlightPlan>("DFW", "ORD", 150);
// make_unique avoids naming the type twice and is exception-safer in
// multi-argument function calls (no raw new in unevaluated sub-expressions).
```

**Why compliant:** Ownership is immediately transferred to `unique_ptr` — no window
where an exception can cause a leak. `unique_ptr` destructor guarantees `delete` on
all paths including exceptions.

---

## COMPLIANT (C++11): Factory Function Pattern

```cpp
// Preferred in C++11: factory encapsulates the new, callers never see raw pointers
std::unique_ptr<FlightPlan> make_flight_plan(
        const std::string& origin,
        const std::string& destination,
        int passengers) {
    return std::unique_ptr<FlightPlan>(
        new FlightPlan(origin, destination, passengers));
}

// Move semantics: unique_ptr returned by value — no copy, no allocation
auto plan = make_flight_plan("DFW", "ORD", 150);
```

---

## COMPLIANT (C++11): `shared_ptr` and `weak_ptr`

```cpp
// shared_ptr: shared ownership with reference counting
std::shared_ptr<FlightPlan> shared_plan =
    std::make_shared<FlightPlan>("DFW", "ORD", 150);  // make_shared: one allocation for control block + object
                                                        // Available C++11

// weak_ptr: observer — breaks reference cycles
// Does NOT extend lifetime; must lock() to use
std::weak_ptr<FlightPlan> observer = shared_plan;

if (auto locked = observer.lock()) {
    // Use locked — guaranteed non-null within this scope
    process(*locked);
}
// locked released here; shared_plan lifetime unaffected
```

**When to use each:**

| Pointer | Ownership | Use Case |
|---------|-----------|----------|
| `unique_ptr` | Exclusive | Default — service, resource, RAII handle |
| `shared_ptr` | Shared | Cache entries, shared buffers, callback registrations |
| `weak_ptr` | None (observer) | Breaking cycles; parent ↔ child graphs |

---

## COMPLIANT (C++11): Custom Deleter

```cpp
// Custom deleter for resources that require non-delete cleanup
// e.g., C API file handles, database connections
auto file_deleter = [](FILE* f) { if (f) fclose(f); };
std::unique_ptr<FILE, decltype(file_deleter)> file(fopen("log.txt", "r"), file_deleter);

// If file open failed (nullptr), unique_ptr destructor calls deleter with nullptr —
// the lambda guards against that with the null check.
```

---

## NON-COMPLIANT: Raw `new` / `delete`

```cpp
// BUG 1: manual delete missed if exception thrown between new and delete
FlightPlan* plan = new FlightPlan("DFW", "ORD", 150);
process(*plan);                      // if this throws, plan is leaked
delete plan;

// BUG 2: double delete — ownership unclear across call boundaries
FlightPlan* plan2 = create_plan();   // who owns this?
use_plan(plan2);
delete plan2;                        // also deleted in use_plan? UB.

// BUG 3: C++03-era auto_ptr — silently moves on copy
std::auto_ptr<FlightPlan> p(new FlightPlan("DFW","ORD",150));
std::auto_ptr<FlightPlan> p2 = p;    // p is now null — silent move!
// p->origin() — undefined behaviour
```

**Why non-compliant:** Raw `new`/`delete` has no exception safety, no ownership
clarity, and `auto_ptr` has broken copy semantics. Per ENG-6.1, all resources must
use RAII ownership.

---

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| C++11 function call with multiple `new` args: `f(new A(), new B())` | If `new A()` succeeds and `new B()` throws before the `unique_ptr` constructor runs, `A` leaks | Use factory functions or `make_unique` (C++14) to ensure each allocation is immediately owned |
| `shared_ptr` cycle: parent holds `shared_ptr<Child>`, child holds `shared_ptr<Parent>` | Reference count never reaches zero — memory leak | Child holds `weak_ptr<Parent>`; break all cycles with `weak_ptr` |
| Passing `unique_ptr` by value to thread | `unique_ptr` is move-only; `std::thread` requires copyable callable | Use `std::move` to transfer ownership: `std::thread([p = std::move(ptr)]{ use(*p); })` |
| `shared_ptr` from `this` inside a member function | Naive `shared_ptr<T>(this)` creates a second independent control block — double free | Inherit from `std::enable_shared_from_this<T>` and use `shared_from_this()` |
| Deleting through base class pointer without virtual destructor | `delete base_ptr` — derived destructor never called, partial resource leak | Always declare `virtual ~Base() = default;` in polymorphic base classes |
