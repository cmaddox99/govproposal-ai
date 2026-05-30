---
law_id: ENG-6.1
cpp_version_min: 20
cpp_version_note: >-
  std::format requires C++20. For C++11/14 projects, see
  ENG-6.1-fmtlib-format.md (fmtlib bridge library, identical API).
avatar: cpp
rag_exclude: true  # placeholder — content pending; excluded from RAG routing
---

# [ENG-6.1](laws/engineering/eng-6-security.md): `std::format` (C++20)

Per [ENG-6.1](laws/engineering/eng-6-security.md), `std::format` provides
compile-time type-safe formatting — format/argument type mismatches are
compile errors, not silent UB as with `printf`/`sprintf`.

## COMPLIANT: `std::format` for Audit Log

```cpp
#include <format>

struct FlightId { int value; };

// Audit entry — types verified at compile time
std::string audit_msg(FlightId id, const std::string& action) {
    return std::format("[AUDIT] flight={} action={}", id.value, action); // ✅
}

// format_to: write into a pre-sized buffer (no heap allocation)
void write_audit_header(std::span<char> buf, int seq) {
    std::format_to_n(buf.data(), buf.size() - 1,
                     "SEQ={:06d}", seq);                                 // ✅
}
```

## COMPLIANT: Custom `std::formatter<FlightId>`

```cpp
template<>
struct std::formatter<FlightId> {
    constexpr auto parse(std::format_parse_context& ctx) { return ctx.begin(); }

    auto format(const FlightId& id, std::format_context& ctx) const {
        return std::format_to(ctx.out(), "FL-{:04d}", id.value);
    }
};

// Now FlightId formats directly:
auto msg = std::format("Booking flight {}", FlightId{42}); // → "Booking flight FL-0042"
```

## NON-COMPLIANT: `sprintf` — Type-Unsafe, Buffer-Overflowable

```cpp
char buf[64];
// ❌ passing int where %s expected — UB, not a compile error
sprintf(buf, "flight=%s action=%s", flight_id.value, action.c_str());

// ❌ fixed buffer: no overflow protection
sprintf(buf, "SEQ=%06d", seq);   // silent truncation if seq > 999999
```

## Edge Cases

### `std::vformat` — Runtime Format Strings

`std::vformat` accepts a runtime `string_view` format string. Per
[ENG-6.1](laws/engineering/eng-6-security.md), **never pass user-supplied
input as the format string** — a malformed format string throws
`std::format_error` but a crafted string can expose sensitive field values
through unintended argument expansion:

```cpp
// NON-COMPLIANT — user_fmt comes from external input
auto msg = std::vformat(user_fmt, std::make_format_args(flight_id)); // ❌

// COMPLIANT — format string is always a compile-time literal
auto msg = std::format("{}", flight_id);  // ✅
```
