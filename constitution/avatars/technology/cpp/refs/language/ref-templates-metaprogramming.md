---
cpp_version_min: 11
cpp_version_note: >-
  SFINAE/enable_if (C++11) to Concepts (C++20) progression; consteval (C++20) noted.
avatar: cpp
---

# C++ Avatar Reference: Templates and Metaprogramming

---

## Template and Metaprogramming Governance

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md) (Complexity Limits), template metaprogramming must be governed to prevent compilation time explosion, binary bloat, and unmaintainable code.

> 💡 **Simpler alternative:** Prefer `if constexpr` (C++17) or concepts (C++20) over template specialization where possible. See [skill-cpp-code-simplification](agent-skills/skills-by-domain/platform-engineering/skill-cpp-code-simplification.md).

### C++20 Concepts Policy

All template functions accepting constrained types must use C++20 concepts. Prefer named concepts over ad-hoc `requires` clauses.

```cpp
// COMPLIANT — named concept with clear semantics
template<typename T>
concept Serializable = requires(const T& t, std::ostream& os) {
    { t.serialize(os) } -> std::same_as<void>;
    { T::deserialize(os) } -> std::same_as<T>;
};

template<Serializable T>
void write_to_audit(const T& record, AuditSink& sink);

// NON-COMPLIANT — unconstrained template with cryptic errors
template<typename T>
void write_to_audit(const T& record, AuditSink& sink);
```

**SFINAE migration:** For brownfield code using `std::enable_if_t<>`, migrate to concepts as modules are modernized. New code must not use SFINAE when concepts are available.

### `constexpr` and `consteval` Policy

- Prefer `constexpr` for computations that *can* be evaluated at compile time — configuration constants, lookup tables, validation of static invariants
- Use `consteval` for computations that *must* be compile-time — safety-critical constants (max passengers per aircraft type, IATA codes), cryptographic constants
- Do not overuse `constexpr` on functions that are never called at compile time — it adds complexity without benefit

```cpp
// COMPLIANT — compile-time validated aircraft capacity
consteval int max_passengers(AircraftType type) {
    switch (type) {
        case AircraftType::B737_800: return 189;
        case AircraftType::A321neo: return 244;
        default: throw "Unknown aircraft type";  // compile-time error
    }
}
```

### Template Bloat Control

- Use `extern template` declarations to prevent redundant instantiations across translation units
- Keep template implementations in `.cpp` files with explicit instantiation where possible
- Limit template nesting depth — deeply nested templates (e.g., `std::variant` visitors with multiple layers) must be refactored into named types

```cpp
// header: flight_serializer.h
extern template class Serializer<FlightPlan>;
extern template class Serializer<BookingRecord>;

// source: flight_serializer.cpp
template class Serializer<FlightPlan>;
template class Serializer<BookingRecord>;
```

### Template Specialization Governance

Template specialization (partial and full) must follow strict rules to prevent ODR violations and linker-time surprises.

```cpp
// COMPLIANT — full specialization declared in header, defined in ONE .cpp
// header: codec.h
template <typename T>
struct Codec {
    static std::string encode(const T& val);
};

template <>
struct Codec<FlightPlan>;  // ✅ declaration in header

// source: codec_flight.cpp
template <>
struct Codec<FlightPlan> {
    static std::string encode(const FlightPlan& plan) {
        return plan.to_json();
    }
};  // ✅ ONE definition in one TU

// NON-COMPLIANT — full specialization defined in header without inline
// codec.h
template <>
struct Codec<Booking> {
    static std::string encode(const Booking& b) { return b.to_json(); }
};  // ❌ ODR violation — included in multiple TUs
```

**Specialization rules:**
- Full specializations in headers must be `inline` or declared-only (defined in `.cpp`)
- Partial specializations must be in the **same namespace** as the primary template
- Never specialize `std::` templates except where the standard explicitly permits (e.g., `std::hash`)
- Ensure a specialization in a different TU is visible before use — otherwise the primary template instantiates silently (not a link error)

### Variadic Templates and Fold Expressions

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), variadic templates must be bounded and documented.

```cpp
// COMPLIANT — fold expression with constraint
template <typename... Args>
    requires (std::convertible_to<Args, std::string_view> && ...)
void log_all(Args&&... args) {
    (log::info("{}", args), ...);  // ✅ fold expression — clear intent
}

// NON-COMPLIANT — unbounded recursive template (pre-C++17 style)
template <typename First, typename... Rest>
void log_all(First&& first, Rest&&... rest) {
    log::info("{}", first);
    log_all(std::forward<Rest>(rest)...);  // ❌ recursive — limit depth
}
```

**Governance rules:**
- Prefer fold expressions (C++17) over recursive variadic templates — they produce better error messages and compile faster
- Constrain parameter packs with concepts: `requires (Constraint<Args> && ...)`
- Document maximum expected pack size in comments if relevant for stack/performance

### SFINAE to Concepts Migration Path

| Legacy (SFINAE) | Modern (Concepts) | Migration Notes |
|------------------|--------------------|-----------------|
| `std::enable_if_t<std::is_integral_v<T>>` | `template <std::integral T>` | Direct replacement |
| `std::enable_if_t<has_serialize_v<T>>` | `template <Serializable T>` | Extract named concept |
| `decltype(std::declval<T>().begin())` | `requires { t.begin(); }` | Use requires-expression |
| `void_t<...>` detection idiom | `concept` definition | C++20 makes void_t obsolete |

**When SFINAE is still needed:** Only in pre-C++20 code, or when implementing concept-like constraints that must work across compilers with incomplete C++20 support. New code must use concepts.

---

## Forwarding, ADL, and Template Safety

> ⚠️ **Complexity Warning:** Perfect forwarding and ADL are intermediate-to-advanced topics that cause subtle bugs. For most code, pass by `const&` or by value. Only use forwarding references when writing generic library-style code.

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md) (Complexity Limits) and [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design), template utilities must be correct under all instantiations, not just the ones tested.

### Perfect Forwarding

A **forwarding reference** (also called universal reference) is `T&&` where `T` is a deduced template parameter. It binds to both lvalues and rvalues, preserving value category.

```cpp
// COMPLIANT — forwarding reference with std::forward
template <typename... Args>
auto make_booking(Args&&... args) {
    log_creation(args...);  // ✅ read args before forwarding
    return Booking{std::forward<Args>(args)...};  // ✅ forward at end
}

// NON-COMPLIANT — forwarding the same argument twice
template <typename T>
void process(T&& val) {
    consume(std::forward<T>(val));      // moved from here
    log(std::forward<T>(val));          // ❌ UB — use after move!
}
```

**Governance rules:**
- `std::forward<T>(x)` must be the **last** use of `x` in an expression — never forward the same argument twice
- If `T&&` is **not** a deduced template parameter, it is an rvalue reference, not a forwarding reference — do not use `std::forward` on it
- Prefer overload sets (`const T&` + `T&&`) over forwarding references for public APIs — forwarding references are greedy and suppress implicit conversions
- Use `static_assert` to verify deduced types when debugging template resolution

### Argument-Dependent Lookup (ADL)

ADL finds functions in the namespaces of their argument types. This is essential for `operator<<` and `swap`, but can cause surprising behavior in templates.

```cpp
// SURPRISE — ADL pulls in unexpected overload
namespace airline {
    struct Flight { /* ... */ };
    void process(Flight f);  // found by ADL
}

namespace internal {
    template <typename T>
    void dispatch(T val) {
        process(val);  // ⚠️ calls airline::process via ADL, not internal::process
    }
}
```

**Governance rules:**
- Qualify function calls in templates to avoid ADL surprises: `internal::process(val)` instead of `process(val)`
- For customization points (like `swap`), use the two-step ADL idiom:
  ```cpp
  using std::swap;
  swap(a, b);  // ✅ finds custom swap via ADL, falls back to std::swap
  ```
- Never define `operator<<` or `operator==` in the global namespace — always in the type's namespace
- Use `std::invoke` for generic callable dispatch (avoids ADL issues with function objects)

### Forwarding Reference vs Rvalue Reference

This distinction is the #1 source of confusion in modern C++:

```cpp
template <typename T>
void foo(T&& x);      // ✅ forwarding reference (T is deduced)

void bar(Widget&& w);  // rvalue reference (no deduction)

auto&& z = expr;       // ✅ forwarding reference (auto deduced)
```

**Simplification:** Pass by `const T&` (read-only) or by value (sink) unless generic forwarding is genuinely needed.

---

## Lambda and Functional Pattern Governance

> ⚠️ **Complexity Warning:** Lambda captures are the #1 source of use-after-free in modern C++ async code. Default to capture-by-value for async lambdas.

Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design), lambdas passed to async operations must not capture dangling references.

### Lambda Capture Rules

| Capture | Safe for Async? | Risk |
|---------|----------------|------|
| `[=]` | ⚠️ Mostly — but captures `this` by pointer! | `this` may be destroyed before lambda runs |
| `[&]` | ❌ Never | All references dangle if lambda outlives scope |
| `[this]` | ❌ Dangerous | Same as `[=]` — pointer, not copy |
| `[*this]` (C++17) | ✅ Safe | Copies entire object |
| `[x = std::move(obj)]` | ✅ Safe | Moves ownership into lambda |

```cpp
// NON-COMPLIANT — [this] in async lambda
class FlightSearch {
    SearchCriteria criteria_;
public:
    void search_async() {
        executor_.submit([this] {        // ❌ `this` may be destroyed
            return do_search(criteria_);  // use-after-free
        });
    }
};

// COMPLIANT — capture by value or move
class FlightSearch {
    SearchCriteria criteria_;
public:
    void search_async() {
        executor_.submit([criteria = criteria_] {  // ✅ copy of data
            return do_search(criteria);
        });
    }
};

// COMPLIANT (C++17) — capture *this by value
void search_async() {
    executor_.submit([*this] {           // ✅ copies entire object
        return do_search(criteria_);
    });
}
```

### `std::function` Overhead

`std::function` uses type erasure and may heap-allocate. On hot paths, this is measurable.

```cpp
// NON-COMPLIANT on hot paths — heap allocation per call
void process_flights(const std::vector<Flight>& flights,
                     std::function<bool(const Flight&)> filter) {
    // std::function may allocate — avoid in tight loops
}

// COMPLIANT — template parameter avoids type erasure
template <typename Predicate>
void process_flights(const std::vector<Flight>& flights,
                     Predicate filter) {
    // ✅ zero overhead — inlined at call site
}

// COMPLIANT (C++23) — move-only function for unique ownership
std::move_only_function<void()> callback = [ptr = std::make_unique<Data>()](){ /* ... */ };
```

**Governance rules:**
- Use `std::function` for stored callbacks (event handlers, configuration) where allocation is acceptable
- Use template parameters for hot-path function arguments
- Use `std::move_only_function` (C++23) when the callable is not copyable
- Profile before optimizing — SBO (Small Buffer Optimization) means small lambdas avoid the heap

### `std::initializer_list` Traps

`std::initializer_list` causes three categories of surprises:

```cpp
// SURPRISE 1 — Constructor ambiguity
std::vector<int> v1(5, 0);   // 5 elements of value 0
std::vector<int> v2{5, 0};   // ❌ 2 elements: {5, 0} — braced-init prefers initializer_list!

// SURPRISE 2 — Dangling array (pre-C++17)
auto get_list() {
    return {1, 2, 3};  // ⚠️ underlying array may dangle
}

// SURPRISE 3 — Narrowing conversions
double d = 3.14;
int x{d};  // ❌ compile error — narrowing in braced-init
int y(d);  // ⚠️ compiles with warning — truncates to 3
```

**Governance rules:**
- Use `()` for size+value construction, `{}` for element lists
- Never return a bare `{...}` from a function — construct the container explicitly
- Prefer `std::array` or `std::span` over `std::initializer_list` for parameters
- Enable `-Wnarrowing` (default in C++11+) and treat as error

---

## Pre-C++11 Template Idiom Recognition ★ C++98/03

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md): recognise these in legacy template code. See [idiom atlas](docs/guides/avatars/cpp-classical-idiom-atlas.md).

| What you see | Classical name | Verdict |
|---|---|---|
| `template<class D> class Base { static_cast<D*>(this)-> }` | **CRTP** | ✅ **PRESERVE** in C++98/14 — do NOT refactor to virtual/Concepts (C++20 only) |
| `struct NullType{}; template<T,U> struct Typelist` | **Loki TypeList** | ⚠️ **MIGRATE** to `std::tuple` / `std::variant` |
| `template<bool,class T=void> struct EnableIf{}` | **Manual enable-if** | ✅ **MAP** to `std::enable_if_t` — do not rewrite existing SFINAE |
| `void fn(Iter&, n, random_access_tag{})` dummy tag | **Tag dispatching** | ✅ **PRESERVE** in working code — replace with `if constexpr` (C++17) only when refactoring |
| `template<class P1,class P2> class W : P1,P2` | **Policy-based design** | ✅ **VALID** C++98 static poly — prefer over virtual |
| `typename IsSame<T,U>::value` manual traits | **Manual type traits** | ✅ **MAP** to `std::is_same_v<T,U>` (`<type_traits>`) |

**CRTP note ([ENG-3.1](laws/engineering/eng-3-code-quality.md)):** LLMs suggest virtual — wrong in C++98; use CRTP.

---

## See Also

- [Advanced C++ Patterns](ref-advanced-patterns.md)
