---
law_id: ENG-6.1
cpp_version_min: 17
cpp_version_note: >-
  Uses C++17 std::variant as type-safe void* replacement. Transitional teams: use tagged union or virtual dispatch; brownfield: maintain existing void* with bounds docs.
avatar: cpp
---
# ENG-6.1 — `void*` → Type-Safe Alternatives

> **Law:** [ENG-6.1 — Security by Design](laws/engineering/eng-6-security.md)
> **The Rule:** Eliminate `void*` from all new code. Casting from `void*` to the wrong type is UB — no runtime check, no exception.

## Java Comparison

Java's `Object` base class allows safe runtime downcasting via `instanceof` and `ClassCastException`. C++'s `void*` has **no runtime type information** — casting to the wrong type silently corrupts memory.

## When to Use

- Replacing legacy callback `void*` context pointers
- Migrating C-style heterogeneous containers
- Wrapping C library opaque handles (`void*` → RAII typed wrapper)

## COMPLIANT ✅

```cpp
// Closed set of types → std::variant (compile-time checked)
using PassengerEvent = std::variant<
    BookingConfirmed,
    SeatAssigned,
    CheckInComplete
>;

void handle(const PassengerEvent& event) {
    std::visit(overloaded{
        [](const BookingConfirmed& e) { notify_crew(e); },
        [](const SeatAssigned& e)     { update_manifest(e); },
        [](const CheckInComplete& e)  { print_pass(e); }
    }, event);  // compiler enforces all types handled
}

// Open type set → std::any (runtime checked)
std::any plugin_data = load_plugin_config();
auto& cfg = std::any_cast<PluginConfig&>(plugin_data);  // throws on wrong type
```

## NON-COMPLIANT ❌

```cpp
// void* callback — wrong cast = silent UB
void on_event(void* ctx) {
    auto* booking = static_cast<Booking*>(ctx);  // UB if ctx isn't Booking*
    booking->confirm();
}

// void* in container — no type safety
std::vector<void*> events;
events.push_back(new Booking{});
auto* b = static_cast<Flight*>(events[0]);  // UB: wrong type, no detection
```

## Edge Cases

- **C API interop:** When wrapping C libraries that require `void*` callbacks, isolate the `void*` at the boundary and immediately cast to a typed wrapper inside the callback. Never pass `void*` deeper than one call.
- **`std::variant` vs `std::any`:** Prefer `std::variant` (compile-time exhaustive, no heap alloc). Use `std::any` only for truly open type sets (plugin systems).
- **Performance:** `std::variant` stores values inline (no allocation for small types). For large types, use `std::variant<std::unique_ptr<A>, std::unique_ptr<B>>`.
- **The `overloaded` helper:** Required for multi-lambda `std::visit`. Define once: `template<class... Ts> struct overloaded : Ts... { using Ts::operator()...; };`
