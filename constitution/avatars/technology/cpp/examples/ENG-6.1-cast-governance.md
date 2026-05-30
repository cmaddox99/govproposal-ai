---
law_id: ENG-6.1
cpp_version_min: 11
avatar: cpp
---

# ENG-6.1: Cast Governance — C++ Examples

## The Rule

Every type cast must use a named C++ cast (`static_cast`, `dynamic_cast`, `const_cast`, `reinterpret_cast`) — never a C-style cast. C-style casts are banned because they silently choose the most dangerous cast that compiles.

## When to Use

Any code that converts between types. **Java developers:** In Java, `(Flight) obj` is always safe — it throws `ClassCastException` on failure. In C++, `(Flight*) ptr` can silently reinterpret memory with no exception and no warning. This is one of the most dangerous Java→C++ traps.

## COMPLIANT: Named Casts

```cpp
// why: static_cast for numeric conversion — safe, compile-time checked
double altitude_ft = static_cast<double>(altitude_m) * 3.281;

// why: static_cast for upcast — known hierarchy, always safe
FlightBase* base = static_cast<FlightBase*>(derived);

// why: dynamic_cast for downcast — like Java instanceof + cast
if (auto* boeing = dynamic_cast<Boeing737*>(aircraft)) {
    boeing->checkWinglets();  // why: safe — nullptr returned if not Boeing737
}

// why: reinterpret_cast for byte access — intent is explicit
const std::byte* raw = reinterpret_cast<const std::byte*>(&flight_data);

// why: const_cast ONLY for legacy C API that lacks const-correctness
extern "C" int legacy_validate(char* data, size_t len);
void validate(const std::string& input) {
    legacy_validate(const_cast<char*>(input.c_str()), input.size());
}
```

## NON-COMPLIANT: C-Style and Dangerous Casts

```cpp
double alt_ft = (double)altitude_m * 3.281;     // ❌ C-style cast — may silently reinterpret
FlightBase* b = (FlightBase*)ptr;               // ❌ C-style — could be reinterpret_cast
const_cast<Flight&>(flight).setGate("B12");     // ❌ Modifying a truly const object is UB
reinterpret_cast<Flight*>(raw_bytes);           // ❌ Casting arbitrary bytes to object — UB
```

## Edge Cases & Warnings

- **C-style casts are unpredictable:** `(Type)expr` tries `const_cast`, then `static_cast`, then `reinterpret_cast` — whichever compiles first wins. You cannot tell by reading it which cast was used.
- **`dynamic_cast` requires virtual functions:** The base class must have at least one virtual method (typically a virtual destructor). Without it, `dynamic_cast` won't compile.
- **`const_cast` + mutation = UB:** Casting away `const` is only safe if the original object was not declared `const`. Modifying a truly `const` object is undefined behavior.
- **Enable `-Wold-style-cast`:** This compiler flag catches every C-style cast. Add it to your warning flags and fix violations incrementally.
