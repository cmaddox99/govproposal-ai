---
cpp_version_min: 98
cpp_version_note: >-
  Legacy antipattern catalog (god classes, header bloat); applies from C++98/03.
avatar: cpp
---

# C++ Avatar Reference: Legacy Code Smells - Patterns

---

### 8. Header-Only Bloat

**Recognition pattern:** Build takes >10 minutes. Touching one header triggers recompilation of 100+ files. Header files contain full class definitions, function bodies, and template implementations.

**Severity:** MEDIUM — Developer productivity killer. Slow CI.

**Why it exists:** Header-only is "easy" (no linker issues). Template code must be in headers. Over time, everything migrated to headers for convenience.

**Remediation:**
1. Apply PIMPL to classes with stable interfaces but changing internals
2. Move non-template function bodies to `.cpp` files
3. Use forward declarations aggressively — only include what you *use*, not what you *mention*
4. Use explicit template instantiation for templates used with limited types

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Measure baseline build time
- Commit 2: Apply PIMPL to one high-churn header
- Commit 3: Measure build time improvement; document in PR

### 9. Rule of 3/5/0 Violations

**Recognition pattern:** Class has a user-defined destructor but no copy constructor or copy assignment operator. Or has copy operations but no move operations. Resource leaks on copy; double-free on destruction.

**Severity:** HIGH — Silent resource leaks and double-free bugs.

**Why it exists:** Pre-C++11, the Rule of 3 was the standard. C++11 added move semantics (Rule of 5). Many classes were never updated.

**Remediation:**
1. **Rule of 0 (preferred):** Use smart pointers and RAII members so the compiler-generated special members are correct
2. **Rule of 5 (when needed):** If you define any of {destructor, copy ctor, copy assign, move ctor, move assign}, define or `= default` all five
3. `= delete` copy operations on non-copyable resources (file handles, connections)

```cpp
// Rule of 0 — preferred
class FlightRecord {
    std::string pnr_;
    std::unique_ptr<RouteData> route_;  // unique_ptr handles cleanup
    // NO user-defined destructor, copy, or move needed
};

// Rule of 5 — when managing raw resource
class LegacyConnection {
    int socket_fd_;
public:
    ~LegacyConnection();                                     // Destructor
    LegacyConnection(const LegacyConnection&) = delete;      // No copy
    LegacyConnection& operator=(const LegacyConnection&) = delete;
    LegacyConnection(LegacyConnection&& other) noexcept;     // Move ctor
    LegacyConnection& operator=(LegacyConnection&&) noexcept; // Move assign
};
```

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Add test verifying resource leak / double-free (sanitizer-detected)
- Commit 2: Add missing special members (or refactor to Rule of 0)
- Commit 3: Verify sanitizer clean

### 10. Implicit Conversion Abuse

**Recognition pattern:** Functions accept `Flight` but callers pass `std::string` and it compiles. Single-argument constructors act as implicit conversion operators. Surprising overload resolution.

**Severity:** HIGH — Silent type coercion causes logic bugs that pass compilation.

**Why it exists:** C++ allows single-argument constructors to serve as implicit conversions. This was a "feature" that predates modern type safety awareness.

**Remediation:**
1. Mark ALL single-argument constructors `explicit`
2. Mark all conversion operators `explicit`
3. Fix call sites to use explicit construction
4. Add `-Wconversion` flag to CI builds

```cpp
// BEFORE — implicit conversion
class FlightId {
public:
    FlightId(const std::string& id);  // Implicit: string → FlightId
};
void process(FlightId id);
process("AA100");  // Compiles! Silent conversion string → FlightId

// AFTER — explicit conversion
class FlightId {
public:
    explicit FlightId(const std::string& id);  // No implicit conversion
};
process(FlightId("AA100"));  // Must be explicit — intent is clear
```

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Add `explicit` to one class's constructors
- Commit 2: Fix compile errors at call sites
- Commit 3: Add test verifying no implicit conversion compiles

### 11. Public Data Members

**Recognition pattern:** `flight.departureTime = newTime;` scattered throughout codebase. No invariant protection. Any code can mutate any field at any time.

**Severity:** MEDIUM — Prevents adding validation, logging, or thread safety later.

**Why it exists:** C legacy ("structs with public fields"), or developers treating C++ classes as data bags.

**Remediation:**
1. For pure data (DTOs, config records): use `struct` with all public members — this is fine
2. For objects with invariants: encapsulate with getters/setters
3. Use `[[nodiscard]]` on getters to prevent ignoring return values

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Add getter/setter for one data member
- Commit 2: Update call sites to use accessor
- Commit 3: Make data member private

### 12. Output Parameter Overuse

**Recognition pattern:** `void getFlights(std::vector<Flight>& result)` instead of returning a vector. Legacy C++ feared returning large objects by value due to copy cost.

**Severity:** MEDIUM — Harms readability and prevents chaining. Creates uninitialized-variable risk.

**Why it exists:** Pre-C++11, returning a `vector` copied it. Output parameters avoided the copy. Since C++11, move semantics and copy elision (RVO/NRVO) make return-by-value efficient.

**Remediation:**
1. Change `void f(T& out)` to `T f()`
2. Rely on move semantics and guaranteed copy elision (C++17)
3. For multiple return values, use `std::tuple`, `std::pair`, or a struct with structured bindings

```cpp
// BEFORE — output parameter
void findFlights(const std::string& origin,
                 std::vector<Flight>& results);

// AFTER — return by value (zero-copy thanks to RVO)
std::vector<Flight> findFlights(const std::string& origin);

// Usage with structured bindings (C++17)
auto [flights, errors] = searchFlights(query);
```

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Change one function signature to return-by-value
- Commit 2: Update all call sites
- Commit 3: Verify no performance regression with benchmark

### 13. Mixed Error Handling

**Recognition pattern:** Same module uses exceptions for some errors, error codes for others, and `errno` for C library calls. Callers must know which style each function uses.

**Severity:** HIGH — Missed errors, leaked resources, inconsistent caller patterns.

**Why it exists:** C++ supports all three mechanisms. Libraries use different conventions. Over time, modules mixed styles as different developers contributed.

**Remediation:**
1. Choose ONE strategy per module boundary:
   - **Exceptions** for truly exceptional conditions (preferred in application logic)
   - **Error codes / `std::expected` (C++23)** for expected failures (file not found, network timeout)
   - **`std::optional`** for "might not have a result" (lookup misses)
2. At module boundaries, translate between strategies
3. Document the strategy in the module header

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Document chosen strategy in module header comment
- Commit 2: Convert one function to chosen strategy
- Commit 3: Add test for error path
- Commit 4: Convert remaining functions

### 14. Multiple Return Paths with Resource Cleanup

**Recognition pattern:** `goto cleanup;` labels. Repeated `delete` or `close()` calls before every `return`. Functions with 5+ return paths, each needing manual cleanup. Missing cleanup on one path = resource leak.

**Severity:** CRITICAL — Resource leaks, double-free, and exception-unsafe code.

**Why it exists:** C-style resource management. Developers manually tracked every allocation.

**Remediation:**
1. Convert EVERY manually managed resource to RAII:
   - `new`/`delete` → `std::unique_ptr`
   - `fopen`/`fclose` → `std::fstream` or RAII wrapper
   - `lock`/`unlock` → `std::lock_guard`
   - Custom allocations → custom RAII wrapper class
2. Once all resources are RAII-managed, returns become safe — no cleanup needed
3. Remove `goto cleanup` patterns entirely

```cpp
// BEFORE — manual cleanup, exception-unsafe
int processManifest(const char* path) {
    FILE* f = fopen(path, "r");
    if (!f) return -1;

    char* buf = (char*)malloc(4096);
    if (!buf) { fclose(f); return -2; }  // cleanup path 1

    if (parse(buf) < 0) {
        free(buf); fclose(f); return -3;  // cleanup path 2
    }

    free(buf);
    fclose(f);
    return 0;  // cleanup path 3
}

// AFTER — RAII, every return is safe
int processManifest(const std::filesystem::path& path) {
    std::ifstream file(path);
    if (!file) return -1;  // No cleanup needed

    std::string buf(4096, '\0');
    if (parse(buf) < 0) return -3;  // No cleanup needed — file closes via RAII

    return 0;  // No cleanup needed
}
```

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Add RAII wrapper for one resource type
- Commit 2: Convert one function to use RAII wrapper
- Commit 3: Remove manual cleanup code, verify with sanitizer

---

## See Also

- [Legacy Code Navigation](ref-legacy-navigation.md)
- [Mental Model Transitions](ref-legacy-mental-models.md)


---

## See Also

- [Legacy Code Smells - Structural](ref-legacy-smells-structural.md)
