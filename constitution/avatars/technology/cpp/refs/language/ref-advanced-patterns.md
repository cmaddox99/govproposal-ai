---
cpp_version_min: 11
cpp_version_note: >-
  Macro governance and constexpr replacement (C++11+); if constexpr (C++17) and abbreviated templates (C++20) noted.
avatar: cpp
---

# C++ Avatar Reference: Advanced C++ Patterns

---

## Preprocessor and Macro Governance

> Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), preprocessor macros are the most dangerous construct in C++ — they bypass the type system, ignore namespaces, and cannot be debugged. **Java has no preprocessor.** If you are coming from Java, treat `#define` like an unscoped global find-and-replace that runs before the compiler sees your code.

### Migration Priority Table

| Legacy Pattern | Modern Replacement | Why | Priority |
|---------------|-------------------|-----|----------|
| `#define MAX_SEATS 200` | `constexpr int kMaxSeats = 200;` | Type-safe, scoped, debuggable | HIGH — safe, mechanical replacement |
| `#define SQUARE(x) ((x) * (x))` | `constexpr auto square(auto x) { return x * x; }` | No double-evaluation bug, type-checked | HIGH — eliminates subtle bugs |
| `#define PI 3.14159` | `inline constexpr double kPi = 3.14159;` | ODR-safe, typed, scoped to namespace | HIGH |
| `#ifndef FLIGHT_H` / `#define FLIGHT_H` | `#pragma once` | Simpler, fewer errors, widely supported | MEDIUM — both are acceptable |
| `#ifdef DEBUG` / `#endif` | `if constexpr (kDebugMode)` | Compile-time branch, type-checked, no dead code | MEDIUM — requires C++17 |
| `#define FOREACH(x, container)` | Range-based `for (auto& x : container)` | Language feature, no macro needed | HIGH |
| X-macros for enum-to-string | `magic_enum` library or manual `constexpr` map | Macros for this are fragile and undebuggable | LOW — complex to replace |

### Macro Risks for Java Developers

Macros have no concept of:
- **Scope** — a `#define` in one header pollutes every file that includes it
- **Namespaces** — `#define MAX` will conflict with `std::max` or any variable named `MAX`
- **Types** — `#define TIMEOUT 30` has no type; `constexpr int kTimeout = 30;` is `int`
- **Debugging** — debuggers show the expanded form, not the macro name

### Rules

1. **New code MUST NOT use `#define` for constants** — use `constexpr` or `inline constexpr`
2. **New code MUST NOT use function-like macros** — use `constexpr` functions or templates
3. **Existing macros**: migrate opportunistically per [ENG-1.4](laws/engineering/eng-1-core-principles.md) (Boy Scout Rule)
4. **Include guards**: either `#pragma once` or traditional `#ifndef` — be consistent per project
5. **Conditional compilation**: limit `#ifdef` usage; prefer `if constexpr` where possible (C++17+)
6. **Platform detection**: use CMake's `target_compile_definitions()` instead of manual `#ifdef _WIN32`

---

## Allocator Governance

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), custom allocators must be justified by profiling data. The default allocator is correct for most use cases.

> 💡 **Simpler alternative:** Use the default allocator unless profiling proves it's a bottleneck. Java developers: C++'s default `new`/`delete` is analogous to JVM heap allocation — it works well for most cases. PMR (★ C++17) and custom allocators are the C++ equivalent of writing a custom garbage collector — you almost never need to.

### Allocator Decision Policy

| Scenario | Strategy | Justification Required |
|----------|----------|----------------------|
| General application code | Default `std::allocator` | None — this is the default |
| Hot path with allocation pressure | PMR with `std::pmr::monotonic_buffer_resource` | Profiling data showing allocation bottleneck |
| Real-time / latency-critical | Arena/pool allocator | Latency budget documentation |
| Custom hardware / embedded | Custom allocator | Hardware specification |

### PMR (Polymorphic Memory Resource) Patterns ★ C++17

When profiling identifies allocation as a bottleneck, use C++17 PMR as the first optimization:

```cpp
#include <memory_resource>
#include <vector>

// COMPLIANT — PMR with arena allocation, justified by profiling
// Note: std::span requires C++20; replace with const FlightData* + size_t on C++17
void process_flight_batch(std::span<const FlightData> flights) {
    std::array<std::byte, 64 * 1024> buffer;  // 64KB stack arena
    std::pmr::monotonic_buffer_resource arena(buffer.data(), buffer.size());
    std::pmr::vector<ProcessedFlight> results(&arena);

    for (const auto& flight : flights) {
        results.push_back(process(flight));
    }
    // arena freed automatically when buffer goes out of scope
}
```

### Governance Rules

1. **Default first** — do NOT use custom allocators without profiling evidence (per [ENG-3.1](laws/engineering/eng-3-code-quality.md))
2. **Sanitizer compatibility** — custom allocators MUST work with AddressSanitizer. ASan intercepts `malloc`/`free`; ensure custom allocators either delegate to these or provide ASan integration
3. **Testability** — allocator-aware code must be testable with default allocators in unit tests
4. **Document allocation strategy** — any non-default allocator must have a comment citing the profiling evidence and expected performance gain

---

## ABI Stability and Binary Compatibility

Per [ENG-2.3](laws/engineering/eng-2-architecture.md) (Vertical Slice Architecture), public library APIs must maintain ABI stability across minor versions. Breaking ABI silently causes runtime crashes in downstream services — not compile-time errors.

> 💡 **Simpler alternative:** Start with the PIMPL idiom for ABI isolation. Only invest in symbol visibility attributes, version scripts, and `abi_tag` when you're shipping shared libraries consumed by external teams. For internal services, static linking eliminates ABI concerns entirely.

### ABI Governance Rules

1. **Pimpl idiom for public APIs** — all classes exported from shared libraries must use Pimpl (pointer-to-implementation) to insulate callers from private member changes. Adding a private field to a non-Pimpl class changes the object layout, breaking all compiled consumers.

```cpp
// COMPLIANT — Pimpl insulates ABI
class FlightPlanService {
public:
    FlightPlanService();
    ~FlightPlanService();
    FlightPlanService(FlightPlanService&&) noexcept;
    FlightPlanService& operator=(FlightPlanService&&) noexcept;
    Result<FlightPlan> create(FlightId id, Route route);
private:
    struct Impl;
    std::unique_ptr<Impl> impl_;
};
```

2. **Symbol visibility** — compile shared libraries with `-fvisibility=hidden` and explicitly export public symbols. This prevents symbol collisions, reduces dynamic linking time, and avoids exposing internal implementation.

```cmake
# CMakeLists.txt
set(CMAKE_CXX_VISIBILITY_PRESET hidden)
set(CMAKE_VISIBILITY_INLINES_HIDDEN ON)
```

3. **ABI break detection in CI** — use `abi-compliance-checker` or `libabigail` (`abidiff`) to detect ABI breaks between library versions before release. Add as a CI gate for shared library projects.

4. **Versioned namespaces** — for libraries with multiple consumers, use inline versioned namespaces to allow ABI-incompatible versions to coexist:

```cpp
namespace aa::flight::inline v2 {
    class FlightPlan { /* v2 layout */ };
}
```

5. **SOName versioning** — shared libraries must follow semantic versioning for SOName: `libflight.so.1.2.3` with `SONAME libflight.so.1`. Major version bumps indicate ABI breaks.

---

## See Also

- [Core Language Patterns](ref-core-language.md)
- [Safety-Critical & Memory](ref-safety-memory.md)


---

## See Also

- [Templates and Metaprogramming](ref-templates-metaprogramming.md)
