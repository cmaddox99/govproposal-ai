---
law_id: ENG-6.1
cpp_version_min: 11
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): Security by Design — Strict Aliasing

**Java equivalent:** None. Java has no aliasing rules because the JVM manages memory access. In C++, the compiler assumes pointers of different types don't alias (point to the same memory). Violating this lets the compiler optimize away your reads/writes — your code 'works' in debug mode but breaks at -O2.

## COMPLIANT: Safe Type Punning with memcpy and bit_cast

```cpp
#include <bit>       // C++20 std::bit_cast
#include <cstring>   // std::memcpy
#include <cstdint>

// Safe type punning — memcpy (works all standards)
float int_bits_to_float(int32_t bits) {
    static_assert(sizeof(float) == sizeof(int32_t));
    float result;
    std::memcpy(&result, &bits, sizeof(result));  // ✅ defined behavior
    return result;  // compiler optimizes to register move
}

// Safe type punning — bit_cast (C++20, constexpr-friendly)
constexpr float int_bits_to_float_20(int32_t bits) {
    return std::bit_cast<float>(bits);  // ✅ works at compile time
}

// Safe byte inspection — char/byte access is always allowed
void dump_bytes(const void* ptr, size_t len) {
    auto* bytes = static_cast<const std::byte*>(ptr);
    for (size_t i = 0; i < len; ++i) {
        std::printf("%02x ", std::to_integer<int>(bytes[i]));
    }
}
```

## NON-COMPLIANT: Strict Aliasing Violations

```cpp
// ❌ Type punning through pointer cast — UNDEFINED BEHAVIOR
float bits_to_float_BROKEN(int32_t bits) {
    return *(float*)&bits;  // compiler may optimize away at -O2
}

// ❌ Accessing union through inactive member (except char/byte)
// NOTE: C allows reading a non-active union member; C++ does NOT —
// only the last-written member can be read. This is a common source
// of bugs when porting C code. Use std::bit_cast (C++20) or
// std::memcpy instead.
union TypePun {
    int32_t i;
    float f;
};
TypePun u;
u.i = 0x3F800000;
float val = u.f;  // ❌ UB in C++ (legal in C, but NOT in C++)

// ❌ reinterpret_cast between unrelated types
auto* flight = reinterpret_cast<FlightPlan*>(raw_buffer);
flight->origin = "DFW";  // UB — no FlightPlan object exists at that address
```

## When reinterpret_cast IS Safe

```cpp
// ✅ Pointer ↔ integer round-trip
auto addr = reinterpret_cast<uintptr_t>(ptr);
auto* back = reinterpret_cast<void*>(addr);  // same pointer

// ✅ Cast to char*/byte* for serialization (always allowed)
auto* bytes = reinterpret_cast<const char*>(&flight_plan);
```

## Migration Path

| From (Dangerous) | To (Safe) | Standard |
|-------------------|-----------|----------|
| `*(T*)&x` | `std::memcpy` | C++11+ |
| `*(T*)&x` | `std::bit_cast<T>(x)` | C++20+ |
| Union type punning | `std::memcpy` or `std::bit_cast` | C++11+ |
| `reinterpret_cast<T*>` | Placement new + `std::launder` | C++17+ |

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Union-based type punning in C++03 brownfield code | UB in C++ even though legal in C; compilers elide reads — values disappear in optimised builds | Use `memcpy` even in pre-C++11; it is always safe and optimises to a register copy |
| Casting through `char*` or `unsigned char*` then back to original type | Legal per aliasing rules (char exemption) but pointer arithmetic across object boundary is still UB | Restrict char-pointer aliasing to the exact object's lifetime and bounds |
| `volatile T*` cast used to prevent optimisation of aliasing violation | `volatile` does not fix strict aliasing UB; compiler may still reorder or elide | Use `std::memcpy` / `std::bit_cast`; `volatile` is for hardware-mapped I/O, not aliasing |
| ABI break between TUs compiled at different optimisation levels | `-O0` may appear to work; `-O2`/`-O3` with `-fstrict-aliasing` exposes the UB | Enforce `-fstrict-aliasing` + `-Wstrict-aliasing=2` project-wide in CI toolchain |
