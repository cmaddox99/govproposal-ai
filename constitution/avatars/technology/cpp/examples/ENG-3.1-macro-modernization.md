---
law_id: ENG-3.1
cpp_version_min: 17
cpp_version_note: >-
  Uses C++17 string_view and inline constexpr. Transitional teams: use const char* or std::string with extern linkage for global constants.
avatar: cpp
---

# ENG-3.1: Preprocessor Macro Modernization — C++ Examples

## The Rule

Preprocessor macros bypass the type system, ignore namespaces, and cannot be debugged. New code must not use `#define` for constants or function-like operations. Migrate legacy macros to `constexpr`, `inline constexpr`, or template functions.

## When to Use

Any codebase with `#define` constants or function-like macros — which is virtually every legacy C++ project. **Java has no preprocessor**, so this entire category of problems is new to Java developers.

## COMPLIANT: Modern Replacements

```cpp
// why: constexpr is type-safe, scoped, and debuggable
constexpr int kMaxSeats = 200;
constexpr double kPi = 3.14159265358979;

// why: inline constexpr for header-defined constants (ODR-safe)
inline constexpr std::string_view kAirlineCode = "AA";

// why: constexpr function avoids double-evaluation bug
constexpr auto square(auto x) { return x * x; }

// why: enum class for related constants — scoped and typed
enum class CabinClass : uint8_t {
    First = 1, Business = 2, PremiumEconomy = 3, Economy = 4
};

// why: if constexpr replaces #ifdef for compile-time branching
template<typename Config>
void initialize() {
    if constexpr (Config::kDebugMode) {   // why: no dead code, type-checked
        enableDiagnostics();
    }
}
```

## NON-COMPLIANT: Legacy Macros

```cpp
#define MAX_SEATS 200         // ❌ untyped, unscoped, pollutes all includers
#define PI 3.14159            // ❌ no type, conflicts with any identifier named PI
#define SQUARE(x) ((x) * (x)) // ❌ double-evaluation: SQUARE(i++) evaluates i++ twice
#define AA_AIRLINE_CODE "AA"  // ❌ no type, no namespace

#ifdef DEBUG                  // ❌ textual inclusion — dead code branch still parsed
    enableDiagnostics();
#endif
```

## Edge Cases & Warnings

- **Double-evaluation trap:** `SQUARE(getExpensiveValue())` calls the function twice. `constexpr` functions evaluate arguments once.
- **Macro name collisions:** `#define MAX` will break `std::max`. Legacy code often has `#undef` scattered to work around this — a red flag.
- **Include order dependency:** Macros defined in one header affect every subsequent header. This is why `#include` order matters in C++ (unlike Java's `import`).
- **Existing macros in third-party headers:** You cannot remove macros from libraries you don't own. Use `#undef` after including them, or wrap the include in a namespace-isolated header.
