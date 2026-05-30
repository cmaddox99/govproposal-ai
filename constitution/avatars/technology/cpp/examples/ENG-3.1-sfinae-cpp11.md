---
law_id: ENG-3.1
cpp_version_min: 11
cpp_version_note: >-
  SFINAE with std::enable_if and <type_traits> — the C++11/14 mechanism
  for constraining templates before C++20 concepts. Includes void_t idiom
  (C++17) and concepts migration path. For C++20+ projects see
  ENG-3.1-concepts.md.
avatar: cpp
---

# [ENG-3.1](laws/engineering/eng-3-code-quality.md): Code Quality — SFINAE and `enable_if` (C++11/14)

> ⚠️ **Version-sensitive.** If your project is C++20+, use concepts instead
> (`ENG-3.1-concepts.md`). SFINAE with `enable_if` is the **C++11/14 mechanism** —
> complex but necessary for teams that cannot adopt C++20 yet.

---

## COMPLIANT: Return-Type SFINAE with `enable_if`

The most portable SFINAE form — works in C++11 with any compiler:

```cpp
#include <type_traits>
#include <string>

// Enable only for integral types (int, long, uint64_t, etc.)
template<typename T>
typename std::enable_if<std::is_integral<T>::value, std::string>::type
format_id(T id) {
    return "ID-" + std::to_string(static_cast<long long>(id));
}

// Enable only for floating-point types
template<typename T>
typename std::enable_if<std::is_floating_point<T>::value, std::string>::type
format_id(T value) {
    return "FARE-" + std::to_string(value);
}

// Usage — compiler selects the correct overload
auto flight_id = format_id(12345);     // -> "ID-12345"
auto fare_str  = format_id(299.99);    // -> "FARE-299.990000"
```

**Why compliant:** SFINAE substitution failure is not an error — the compiler silently
discards the overload that does not match, giving clean compile-time dispatch without
runtime branching.

---

## COMPLIANT: Default-Template-Parameter SFINAE (C++11)

Often cleaner for class templates and avoids the verbose return-type form:

```cpp
#include <type_traits>

// Primary template — enabled for arithmetic types
template<typename T,
         typename = typename std::enable_if<std::is_arithmetic<T>::value>::type>
class SafeCounter {
    T count_{};
public:
    void increment() { ++count_; }
    T value() const  { return count_; }
};

// Specialization guard — this prevents SafeCounter<std::string>
// SafeCounter<int>       OK
// SafeCounter<double>    OK
// SafeCounter<std::string> compile error: no matching type
```

---

## COMPLIANT: `void_t` Idiom for Type Detection (C++17 / C++11 polyfill)

Detects whether a type has a particular member or nested type:

```cpp
// C++17 built-in; for C++11/14 add this polyfill:
template<typename...> using void_t = void;

// Detector: does T have a .reserve(size_t) method?
template<typename T, typename = void>
struct has_reserve : std::false_type {};

template<typename T>
struct has_reserve<T,
    void_t<decltype(std::declval<T&>().reserve(std::declval<std::size_t>()))>>
    : std::true_type {};

// Optimise: pre-allocate if the container supports it
template<typename Container>
typename std::enable_if<has_reserve<Container>::value>::type
maybe_reserve(Container& c, std::size_t n) { c.reserve(n); }

template<typename Container>
typename std::enable_if<!has_reserve<Container>::value>::type
maybe_reserve(Container&, std::size_t) {}  // no-op for std::list, std::set etc.
```

---

## COMPLIANT: `enable_if_t` Alias (C++14 shorthand)

```cpp
// C++11 verbose form:
typename std::enable_if<std::is_integral<T>::value, int>::type foo(T);

// C++14 alias (much cleaner):
std::enable_if_t<std::is_integral<T>::value, int> foo(T);

// Common C++14 pattern: trailing return type with enable_if_t
template<typename T>
auto serialize(const T& val)
    -> std::enable_if_t<std::is_trivially_copyable<T>::value, std::vector<uint8_t>>
{
    std::vector<uint8_t> buf(sizeof(T));
    std::memcpy(buf.data(), &val, sizeof(T));
    return buf;
}
```

---

## C++20 Migration Path

When your project upgrades to C++20, replace SFINAE with concepts:

```cpp
// C++11/14 SFINAE:
template<typename T>
std::enable_if_t<std::is_integral<T>::value, std::string> format_id(T id);

// ★ C++20 equivalent — far more readable:
template<std::integral T>
std::string format_id(T id);

// Or with requires clause for complex constraints:
template<typename T>
    requires std::is_integral_v<T> && (sizeof(T) <= 8)
std::string format_id(T id);
```

See `ENG-3.1-concepts.md` for the full C++20 concepts reference.

---

## NON-COMPLIANT: SFINAE Anti-Patterns

```cpp
// BUG 1: void return type with enable_if — silently accepted by some
// compilers but the intent is ambiguous with actual void functions
template<typename T>
void process(T val, typename std::enable_if<std::is_integral<T>::value>::type* = nullptr);
// Prefer return-type or default-parameter SFINAE forms above

// BUG 2: enable_if on a non-template function — no substitution occurs,
// this is just a hard error if the condition is false
void reserve_seats(int n, std::enable_if_t<std::is_integral<int>::value>* = nullptr);
// enable_if only works when T is a deduced template parameter

// BUG 3: overly-broad constraint misses an important type
template<typename T>
std::enable_if_t<std::is_pod<T>::value, void> serialize(const T&);
// std::is_pod is deprecated in C++20; use is_trivially_copyable instead
```

---

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| `enable_if` on both overloads with complementary conditions | Compilation fails for types where neither condition is true (e.g., bool in is_integral + float in is_floating_point — bool is integral, so both might match) | Use `!std::is_same<T, bool>::value` guards where needed |
| Deep SFINAE nesting causes cryptic error messages | Substitution failure cascade — GCC/Clang report 20+ nested errors | Test each trait in isolation; use `static_assert` to document intent |
| `is_pod` used for serialization guard | Deprecated in C++20; some conforming compilers warn | Replace with `is_trivially_copyable<T> && is_standard_layout<T>` |
| SFINAE and `constexpr if` (C++17) | `if constexpr` solves most single-function dispatch needs more cleanly than SFINAE | Prefer `if constexpr` for function body branching in C++17+; use SFINAE only for interface-level overload selection |
