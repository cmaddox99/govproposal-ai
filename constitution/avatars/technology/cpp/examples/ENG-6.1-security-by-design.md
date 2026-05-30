---
law_id: ENG-6.1
cpp_version_min: 17
cpp_version_note: >-
  Uses C++17 string_view for boundary validation. Transitional teams: use const std::string& parameters; brownfield: char* with explicit length.
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): Security by Design — C++ Examples

## The Rule

Security is **not bolted on** after development — it is **designed in** from the start. Validate at boundaries, default to `const`, and use sanitizers in CI to catch memory bugs before production.

## C++ Security Essentials

- **Default to `const`** — every variable, parameter, and member function should be `const` unless mutation is required
- **Validate at boundaries** — all external input is untrusted until proven otherwise
- **Run sanitizers in CI** — AddressSanitizer (ASan), UndefinedBehaviorSanitizer (UBSan), ThreadSanitizer (TSan)
- **Use GSL contracts** — `Expects()` for preconditions, `Ensures()` for postconditions

## COMPLIANT: Input Validation at Boundary

```cpp
#include <stdexcept>
#include <string_view>
#include <gsl/gsl>

class FlightSearchRequest {
public:
    static FlightSearchRequest create(std::string_view origin, std::string_view dest) {
        Expects(!origin.empty() && origin.size() == 3);  // why: fail fast on invalid IATA code
        Expects(!dest.empty() && dest.size() == 3);       // why: precondition — enforced at boundary
        Expects(origin != dest);                           // why: domain rule — can't fly to same airport
        return FlightSearchRequest{std::string(origin), std::string(dest)};
    }

    // why: const by default — immutable after construction
    std::string_view origin() const { return origin_; }
    std::string_view destination() const { return destination_; }

private:
    FlightSearchRequest(std::string o, std::string d)
        : origin_(std::move(o)), destination_(std::move(d)) {}
    const std::string origin_;       // why: const member — no accidental mutation
    const std::string destination_;
};
```

## NON-COMPLIANT: No Input Validation

```cpp
struct FlightSearchRequest {
    std::string origin;        // ❌ public, mutable, no validation
    std::string destination;   // ❌ caller can set empty strings, same origin/dest
};
// ❌ Trusts external input — buffer overflows, injection, invalid state all possible
```

## Edge Cases & Warnings

| Scenario | Guidance |
|----------|----------|
| Sanitizer overhead in production | **Never** ship with sanitizers enabled — 2-5× slowdown. Use only in CI and dev builds (`-fsanitize=address,undefined`). |
| `const` members prevent move | `const` data members disable move assignment. Use `const` on local variables freely; for members, prefer private + `const` accessor. |
| GSL `Expects` vs `assert` | `Expects` is semantically clearer and can be configured to throw in test builds. `assert` is stripped in release. Choose based on failure policy. |
| String injection | Even with IATA code validation, always use parameterized queries downstream — never concatenate validated strings into SQL. |
