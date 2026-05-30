---
law_id: ENG-6.1
cpp_version_min: 14
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md) — Raw Pointer to Smart Pointer Migration

## The Rule

Raw owning pointers (`new`/`delete`) **must be converted to smart pointers**. Use `std::unique_ptr` by default; use `std::shared_ptr` only when ownership is **truly shared** across multiple owners.

## Migration Decision Tree

1. **Single owner?** → `std::unique_ptr` (zero overhead, default choice)
2. **Multiple owners?** → `std::shared_ptr` (reference-counted)
3. **Observer (no ownership)?** → Raw pointer or `std::weak_ptr` (if observing a `shared_ptr`)
4. **Cycles possible?** → Break with `std::weak_ptr`

## NON-COMPLIANT: Raw Pointers (C++98)

```cpp
FlightPlan* plan = new FlightPlan();  // ❌ raw owning pointer
database.save(plan);  // ❌ if save() throws, plan leaks forever
delete plan;           // ❌ never reached on exception

// ❌ C++98 workaround: manual RAII guard — fragile, non-standard
class PlanGuard {
    FlightPlan* ptr_;
public:
    explicit PlanGuard(FlightPlan* p) : ptr_(p) {}
    ~PlanGuard() { delete ptr_; }
    FlightPlan* get() { return ptr_; }
private:
    PlanGuard(const PlanGuard&);             // ❌ boilerplate to prevent copies
    PlanGuard& operator=(const PlanGuard&);
};
```

## COMPLIANT: Smart Pointers (C++11+)

```cpp
// unique_ptr — single ownership, zero overhead
auto plan = std::make_unique<FlightPlan>();  // why: no naked new, exception-safe construction
database.save(*plan);                         // why: pass by ref — callee doesn't own

// shared_ptr — shared ownership when genuinely required
auto shared_plan = std::make_shared<FlightPlan>();  // why: single allocation for object + control block
cache.store(shared_plan);                            // why: cache co-owns the plan
scheduler.schedule(shared_plan);                     // why: scheduler co-owns — both release independently

// weak_ptr — break ownership cycles
struct Route {
    std::shared_ptr<Waypoint> start;
    std::weak_ptr<Route> parent_route;  // why: weak_ptr breaks circular reference
};
```

## Edge Cases & Warnings

| Scenario | Guidance |
|----------|----------|
| Cycles with `shared_ptr` | Circular `shared_ptr` references **leak forever**. Always use `weak_ptr` for back-references or parent pointers. |
| `make_shared` vs `shared_ptr(new T)` | Prefer `make_shared` — single allocation, exception-safe. Exception: custom deleters require the two-step form. |
| Non-owning parameters | Pass `T&` or `T*` (non-owning) to functions that don't affect lifetime. Don't pass `unique_ptr&` unless transferring ownership. |
| `unique_ptr` with custom deleter | Use for C APIs: `unique_ptr<FILE, decltype(&fclose)>(fopen(...), &fclose)`. |
