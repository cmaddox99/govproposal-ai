---
cpp_version_min: 11
cpp_version_note: >-
  Designated initializers (C++20) are primary; legacy sections provide C++11/14/17 alternatives.
avatar: cpp
---

# C++ Avatar Reference: Core Modern Idioms

---

## Designated Initializers ★ C++20

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), prefer designated initializers (C++20) for struct construction. They provide named-parameter clarity familiar to Java developers who expect self-documenting constructors.

> **Java mental model:** Java uses `new FlightRequest.Builder().origin("DFW").destination("ORD").build()` for readable construction. C++20 designated initializers achieve the same readability without the Builder pattern overhead.

### The Rule

Use designated initializers for any struct with 3+ fields. This eliminates positional ambiguity and makes code self-documenting:

```cpp
// ❌ Positional — which string is origin? destination?
FlightRequest req{"DFW", "ORD", "2026-07-04", 2, "economy"};

// ✅ Designated — reads like documentation
FlightRequest req{
    .origin      = "DFW",
    .destination = "ORD",
    .date        = "2026-07-04",
    .passengers  = 2,
    .cabin_class = "economy"
};
```

### Legacy Migration

In C++17 and earlier codebases where designated initializers are unavailable, use one of these patterns:

```cpp
// Option 1: Named constructor (preferred for legacy)
auto req = FlightRequest::create()
    .origin("DFW")
    .destination("ORD")
    .date("2026-07-04")
    .build();

// Option 2: Comment each positional argument
FlightRequest req{
    /*origin=*/"DFW",
    /*destination=*/"ORD",
    /*date=*/"2026-07-04",
    /*passengers=*/2,
    /*cabin_class=*/"economy"
};
```

### Designated Initializer Rules

| Rule | Rationale |
|------|-----------|
| Fields must appear in **declaration order** | C++ standard requirement; reordering is ill-formed |
| Omitted fields are **value-initialized** (zeroed) | Unlike Java defaults, this means `0`, `nullptr`, `false` |
| Cannot mix designated and positional arguments | Pick one style per initialization |
| Nested designated initializers are allowed | `{.inner = {.x = 1, .y = 2}}` |

> **⚠️ Java trap:** Java records/POJOs have no field-order dependency. In C++ designated initializers, field order must match the struct declaration. The compiler enforces this, but it surprises Java developers who expect named parameters to be order-independent.

---

## Null Safety and Pointer Contracts

Per [ENG-6.1](laws/engineering/eng-6-security.md) and [ENG-3.1](laws/engineering/eng-3-code-quality.md), C++ code must define explicit null contracts for every pointer parameter and return type. Unlike Java, dereferencing a null pointer in C++ is **undefined behavior** — there is no `NullPointerException`, no stack trace, and no recovery.

> **Java mental model:** In Java, `obj.method()` on a null reference throws `NullPointerException` — a recoverable exception with a stack trace. In C++, `ptr->method()` on a null pointer is UB: the program may crash, silently corrupt memory, or appear to work. **There is no safety net.**

### The Null Contract Hierarchy

Prefer these types in order (strongest guarantee first):

| Preference | Type | Meaning | Java Equivalent |
|-----------|------|---------|-----------------|
| 1st | Value (`T`) | Cannot be null; always valid | `@NonNull T` |
| 2nd | Reference (`T&`) | Cannot be null; always valid | `@NonNull T` |
| 3rd | `std::optional<T>` | Explicitly nullable; checked access | `Optional<T>` |
| 4th | `gsl::not_null<T*>` | Pointer that is never null; enforced in debug builds (GSL contract-violation policy dependent) | `@NonNull T` |
| 5th | `std::unique_ptr<T>` | Owning nullable pointer; check before use | — |
| 6th | Raw pointer (`T*`) | Last resort; document null contract | `@Nullable T` |

### Mandatory Null Checks

```cpp
// ❌ UB: no null check before dereference
void process_booking(Booking* booking) {
    booking->confirm();  // UB if booking == nullptr
}

// ✅ Contract enforced at API boundary
void process_booking(gsl::not_null<Booking*> booking) {
    booking->confirm();  // guaranteed non-null
}

// ✅ Even better: use a reference (cannot be null by construction)
void process_booking(Booking& booking) {
    booking.confirm();
}

// ✅ When null is a valid state: use optional
void process_booking(std::optional<Booking>& booking) {
    if (booking) {
        booking->confirm();
    }
}
```

### Common Java Developer Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Assume null deref = exception | C++ has no NullPointerException; it's UB | Use references or `gsl::not_null` |
| Check `if (ptr)` then use `*ptr` across threads | Another thread may null the pointer | Copy the pointer first, then check the copy |
| Return `nullptr` from factory functions | Caller may forget to check | Return `std::optional<T>` or `expected<T,E>` |
| Use `dynamic_cast` without null check | `dynamic_cast<T*>` returns `nullptr` on failure | Always check result; prefer `std::variant` |

### Legacy `NULL` → `nullptr` Migration

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), replace all `NULL` and `0`-as-pointer with `nullptr` in touched code. The clang-tidy check `modernize-use-nullptr` automates this. `nullptr` is type-safe: it cannot implicitly convert to `int`, eliminating a class of overload-resolution bugs.

---

## Type-Safe Unions: `void*` → `std::variant` / `std::any` ★ C++17

Per [ENG-6.1](laws/engineering/eng-6-security.md) and [ENG-3.1](laws/engineering/eng-3-code-quality.md), eliminate `void*` from all new code and migrate legacy `void*` usage to type-safe alternatives.

> **Java mental model:** Java's `Object` type is the universal base class — casting from `Object` to a specific type is checked at runtime with `ClassCastException` on failure. C++'s `void*` is worse: casting from `void*` to the wrong type is **undefined behavior** — no exception, no detection, just silent corruption.

### Decision Table: Replacing `void*`

| Legacy Pattern | Modern Replacement | When to Use |
|---------------|-------------------|-------------|
| `void*` callback data | `std::any` or `std::variant` | Type is known at registration time |
| `void*` in container (heterogeneous) | `std::variant<A,B,C>` | Closed set of types |
| `void*` for type erasure | `std::function` or concept-based polymorphism | Callable or behavioral interface |
| `void*` for opaque handle (C API) | RAII wrapper class with typed interface | Wrapping C libraries |
| `void*` for allocator/buffer | `std::span<std::byte>` | Raw memory views |

### Migration Example

```cpp
// ❌ Legacy: void* callback — type error = silent corruption
struct EventCallback {
    void (*handler)(void* context);
    void* context;
};

// ✅ Modern: type-safe variant — compiler enforces exhaustive handling
using EventContext = std::variant<
    BookingContext,
    FlightContext,
    LoyaltyContext
>;

struct EventCallback {
    std::function<void(const EventContext&)> handler;
};

// Usage: compiler forces you to handle all types
void dispatch(const EventContext& ctx) {
    std::visit(overloaded{
        [](const BookingContext& b) { process_booking(b); },
        [](const FlightContext& f)  { process_flight(f); },
        [](const LoyaltyContext& l) { process_loyalty(l); }
    }, ctx);
}
```

### `std::variant` vs `std::any` — When to Use Each

| Feature | `std::variant<Ts...>` | `std::any` |
|---------|----------------------|------------|
| Type set | Closed (known at compile time) | Open (any type) |
| Access | `std::visit` — exhaustive, compile-checked | `std::any_cast` — may throw |
| Performance | No heap allocation (small types) | May heap-allocate |
| **Prefer when** | You know all possible types | Truly dynamic (plugin systems) |

> **Rule:** Prefer `std::variant` over `std::any`. Only use `std::any` when the set of types is genuinely unknown at compile time (e.g., plugin architectures). `std::variant` gives you compile-time exhaustiveness checking — the same safety Java developers get from sealed interfaces with pattern matching.

### The `overloaded` Helper

`std::visit` requires a single callable that handles all variant types. The `overloaded` helper combines multiple lambdas:

```cpp
// Define once in a utility header
template<class... Ts> struct overloaded : Ts... { using Ts::operator()...; };
template<class... Ts> overloaded(Ts...) -> overloaded<Ts...>;
```

---

## See Also

- [Core Type Safety](ref-core-type-safety.md)
- [Safety & Memory Lifetime](ref-safety-memory-lifetime.md)


---

## Parameter Passing (F.16–F.20)

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), use value/const-ref/move
semantics consistently; avoid redundant copies and unnecessary heap ownership transfers.

| Guideline | Rule | Pattern |
|-----------|------|---------|
| F.16 — in-params | small/cheap → value; big → `const&` | `void f(int x)` / `void f(const Bigobj& x)` |
| F.17 — in/out-params | pass by non-const `T&` | `void update(Record& r)` |
| F.18 — will-move-from | pass `T&&`, then `std::move` | `void push(T&& item) { vec_.push_back(std::move(item)); }` |
| F.20 — out-params | prefer return value over `T&` out-param | `T compute()` instead of `void compute(T& out)` |

**Sink constructor idiom** (takes ownership regardless of l/rvalue): pass by value, then move:

```cpp
class Route {
    std::string origin_, dest_;
public:
    Route(std::string o, std::string d)           // by-value sink
        : origin_(std::move(o)), dest_(std::move(d)) {}
};
```

## Rule of Zero / Five (C.20, C.21, C.22)

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), prefer the Rule of Zero
(let RAII handles own resources); use Rule of Five only when managing raw resources.

| Rule | When | Action |
|------|------|--------|
| C.20 — Rule of Zero | all members are RAII types | define NO special members; compiler generates correct ones |
| C.21 — Rule of Five | owns raw resource | define all five: dtor, copy-ctor, copy-assign, move-ctor, move-assign |
| C.22 — Consistency | defines any special member | define all five or use `= default` / `= delete` explicitly |

```cpp
// Rule of Zero — let unique_ptr manage memory
class FlightPlan {
    std::unique_ptr<Route[]> routes_;
    std::size_t count_;
    // No dtor/copy/move defined: unique_ptr handles it
};
```

## Regular Types (C.11)

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), value types passed
through STL containers should satisfy the *Regular* concept (C.11): default-constructible,
copyable, movable, and equality-comparable.

```cpp
struct Waypoint {
    double lat, lon;
    bool operator==(const Waypoint&) const = default;  // C++20
};
static_assert(std::regular<Waypoint>);
```

A *Semiregular* type (C.11) is default-constructible and copyable but lacks `==`.
Move-only handles (`std::unique_ptr`, file descriptors) satisfy `std::movable`
but are neither Regular nor Semiregular — they must never be duplicated.

## Container and Algorithm Selection Guide

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), choose the container
whose complexity guarantees match the dominant access pattern.

| Need | Container | Reason |
|------|-----------|--------|
| Sequential, cache-friendly | `std::vector` | Contiguous memory, O(1) random access |
| Stable iterators + O(1) insert/remove | `std::list` | No reallocation, but no random access |
| Sorted unique keys | `std::set` / `std::map` | O(log n) lookup, ordered traversal |
| Fast unordered lookup | `unordered_map` | O(1) avg; hash must be stable |
| Fixed-size compile-time array | `std::array` | Stack-allocated, bounds-safe |

Algorithm selection: prefer `<algorithm>` over hand-written loops (readability, auditability).
Use range-based for when index is not needed; reserve `for(int i=0; ...)` for index arithmetic.

## See Also

- [Core Type Safety](ref-core-type-safety.md)

## Further Reading

> Per Meyers, *Effective Modern C++* (2014) Items 23–30 — move semantics, perfect forwarding,
> and `auto` type deduction explained with motivation and pitfall catalog.

> Per Sutter & Alexandrescu, *C++ Coding Standards* (2004) — 101-item correctness checklist;
> Items 1–15 cover organizational and design-level hygiene applicable to all C++ versions.

> Further reading: Turner, *C++ Best Practices* (2022) — sanitizer workflow, const-correctness
> discipline, CMake best practices. https://github.com/cpp-best-practices (MIT license)
