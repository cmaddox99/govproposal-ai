---
law_id: ENG-6.5
cpp_version_min: 20
cpp_version_note: >-
  Uses C++20 std::span for bounds-safe buffer views. Transitional teams: pass raw pointer + explicit size; validate length before any access.
avatar: cpp
---

# [ENG-6.5](laws/engineering/eng-6-security.md): Input Validation — C++ Examples

## COMPLIANT: Validated at Construction

```cpp
class AirportCode {
public:
    static AirportCode from_string(std::string_view code) {
        if (code.size() != 3) throw std::invalid_argument("Airport code must be 3 chars");
        for (char c : code) {
            if (!std::isupper(c)) throw std::invalid_argument("Airport code must be uppercase");
        }
        return AirportCode{std::string(code)};
    }

    std::string_view value() const { return code_; }

private:
    explicit AirportCode(std::string code) : code_(std::move(code)) {}
    std::string code_;
};
```

**Why compliant:** Input validated at construction boundary. Invalid state impossible after creation. Domain type prevents raw strings from propagating.

## NON-COMPLIANT: Unvalidated String Passthrough

```cpp
void search_flights(std::string origin, std::string dest) {
    // origin/dest could be empty, wrong length, lowercase, SQL injection...
    db_.query("SELECT * FROM flights WHERE origin='" + origin + "'");
}
```

**Why non-compliant:** No validation. Raw strings used directly in queries. SQL injection risk. Invalid inputs propagate through system.

## COMPLIANT: Bounds-Safe Buffer Access with span

```cpp
#include <span>
#include <stdexcept>

void process_weight_data(std::span<const double> weights) {
    if (weights.empty()) throw std::invalid_argument("weights must not be empty");
    double total = 0.0;
    for (double w : weights) {  // bounds-safe iteration
        if (w < 0.0 || w > 100'000.0) throw std::out_of_range("weight out of range");
        total += w;
    }
}

// string_view safety: NEVER store a string_view from a temporary
void log_airport(std::string_view code) {  // OK — borrowed, not stored
    spdlog::info("Airport: {}", code);
}
// std::string_view dangling = get_temp_string();  // BAD — dangling after statement
```

**The Rule:** Validate all input at the system boundary. Use domain types (`AirportCode`, not `string`) to make invalid states unrepresentable. Use `std::span` instead of pointer+size. Never store `string_view` from temporaries.

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Multi-byte UTF-8 in a fixed-width IATA field (3-char airport code) | `std::string::size()` returns byte count, not character count; a 2-byte UTF-8 code-point passes `size() == 3` but is an invalid IATA code | Validate with explicit ASCII-only check (`std::isalpha` in the C locale) rather than length alone |
| Integer promotion before range check: `uint8_t val = input; if (val > 255)` | Comparison is always false after promotion — overflow already occurred on assignment | Receive as `int`, check bounds, then narrow-cast: `if (raw < 0 || raw > 255) return error;` |
| Locale-sensitive `std::tolower` in IATA/FAA code normalisation | Turkish locale maps `I` → `ı` (not `i`), breaking comparisons silently in production | Use explicit ASCII case folding or ICU; never rely on `<cctype>` functions for standardised codes |
| Proxy struct wrapping a validated string re-introduces unvalidated state | Callers assume the struct is pre-validated; copy constructor moves raw bytes without re-checking | Seal domain-type constructor (`private` + `friend` factory); apply `[[nodiscard]]` to validation factory |
