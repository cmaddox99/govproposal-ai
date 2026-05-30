---
law_id: ENG-6.1
cpp_version_min: 14
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): Security by Design — Smart Pointers

## COMPLIANT: Ownership-Safe Resource Management

```cpp
#include <memory>
#include <unordered_map>

struct FlightPlan {
    std::string flight_number;
    std::string route;
};

// Factory returns unique ownership
auto create_flight_plan(std::string flight, std::string route)
    -> std::unique_ptr<FlightPlan> {
    return std::make_unique<FlightPlan>(std::move(flight), std::move(route));
}

// Shared cache entry with weak observer
class FlightPlanCache {
    std::unordered_map<std::string, std::shared_ptr<FlightPlan>> cache_;
public:
    std::shared_ptr<FlightPlan> get(const std::string& key) {
        return cache_[key];
    }
    std::weak_ptr<FlightPlan> observe(const std::string& key) {
        return cache_[key];  // weak_ptr breaks ownership cycle
    }
};
```

**Why compliant:** Unique ownership for factories, shared for caches, weak to break cycles. No manual delete.

## Ownership Transfer at Call Sites

```cpp
// Transfer ownership INTO a function — pass unique_ptr by value
void register_plan(std::unique_ptr<FlightPlan> plan) {
    registry_.store(std::move(plan));  // sink takes ownership
}

// Use the object WITHOUT transferring — pass by const reference
void print_plan(const FlightPlan& plan) {
    fmt::print("{}: {}\n", plan.flight_number, plan.route);
}

// Caller:
auto plan = create_flight_plan("AA100", "DFW-ORD");
print_plan(*plan);                   // borrow — no transfer
register_plan(std::move(plan));      // transfer — plan is now empty
```

**The rule:** Pass `unique_ptr` by value to transfer, by `const&` to the pointee to borrow. Never pass `unique_ptr` by reference unless the callee may reseat it.

## NON-COMPLIANT: Raw new/delete

```cpp
FlightPlan* create_flight_plan(std::string flight, std::string route) {
    auto* fp = new FlightPlan{flight, route};
    validate(fp);  // if this throws, fp leaks
    return fp;     // caller must remember to delete
}
```

**Why non-compliant:** Raw new leaks on exception. Caller ownership unclear. Violates RAII principle.

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| `shared_ptr` forming a reference cycle (e.g., parent→child, child→parent) | Reference count never reaches zero; both objects leak for the process lifetime | Break cycles with `weak_ptr` on the back-pointer (child holds `weak_ptr<Parent>`); document ownership direction in class header |
| `weak_ptr::lock()` called after the owning `shared_ptr` is destroyed in another thread | `lock()` can return an empty `shared_ptr` without throwing; use of the returned value is UB if not checked | Always check `if (auto sp = wp.lock())` before dereferencing; never assume `weak_ptr` validity without the lock check |
| `unique_ptr<T[]>` storing objects with virtual destructors | Deleting through `T*` from `unique_ptr<T[]>` calls `T::~T()`, not the derived destructor; slices memory | Use `unique_ptr<Base[]>` only for trivially-destructible types; use `vector<unique_ptr<Base>>` for polymorphic arrays |
| Passing `unique_ptr` by value into a function that returns it via `std::move` | Move-only type passed to a function that stores it; caller's pointer is now null even if the function "returns" it | Make ownership transfer explicit in the API name and signature; add assertions in DEBUG builds that returned pointers are non-null |
