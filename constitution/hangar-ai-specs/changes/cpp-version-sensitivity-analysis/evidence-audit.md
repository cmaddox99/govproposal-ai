# Evidence Audit — C++ Avatar Version-Sensitivity Analysis

> Evidence matrix across 5 problem domains × 3 C++ version anchors.
> For panel review records of each finding, see `panel-review.md`.

---

## Summary Matrix

| Domain | C++98/03 | C++14 | C++23 |
|--------|----------|-------|-------|
| Memory Management | Mixed (some tagged) | Mostly untagged | Assumed default |
| Concurrency | Limited coverage | Partial | Good but implicit |
| I/O and Streams | Absent | Absent | Partial |
| Templates/Generics | Partial (SFINAE noted) | Implicit | Tagged (Concepts) |
| Comparison/Operators | Absent | Absent | Partial |

---

## Domain 1: Memory Management

### Version Anchor: C++98/03

#### What the Avatar Says

From `ref-safety-aviation.md` (AP-2: Raw malloc):
```cpp
// BEFORE (C++98 anti-pattern)
char* buf = (char*)malloc(MAX_RESPONSE);
// ... many code paths, some with early return — leak risk

// AFTER (C++98-compatible RAII)
std::string buf;
buf.reserve(MAX_RESPONSE);  // no leak on any path
```

From `ref-safety-aviation.md` (AP-6: FILE* Without RAII):
```cpp
// Remedy (C++98-compatible):
struct FileGuard {
    FILE* fp;
    explicit FileGuard(const char* path, const char* mode) : fp(fopen(path, mode)) {}
    ~FileGuard() { if (fp) fclose(fp); }  // always closes
private:
    FileGuard(const FileGuard&);            // non-copyable (C++98)
};
```

From `examples/ENG-6.1-smart-pointer-migration.md`:
```cpp
// ❌ C++98 workaround: manual RAII guard — fragile, non-standard
class PlanGuard {
    FlightPlan* ptr_;
public:
    explicit PlanGuard(FlightPlan* p) : ptr_(p) {}
    ~PlanGuard() { delete ptr_; }
    FlightPlan* get() { return ptr_; }
private:
    PlanGuard(const PlanGuard&);             // ❌ boilerplate to prevent copies
    PlanGuard& operator=(const PlanGuard&);
};
```

#### Version-Tagging Status: `[PARTIAL]`

- C++98 RAII workarounds exist in `ref-safety-aviation.md` with explicit `(C++98-compatible)` labels
- Example files like `ENG-6.1-smart-pointers.md` assume C++11+ without version tags
- `auto_ptr` migration example is explicitly tagged: "Apply this migration to **any C++98/03 codebase**"

#### Mislead Risk: `[MEDIUM]`

A C++98 developer asking "how to manage memory" may receive `std::make_unique` guidance which is unavailable (C++14 for `make_unique`, C++11 for `unique_ptr`).

#### Example Corpus Coverage: `[PARTIAL]`

- `ENG-6.1-auto-ptr-migration.md` — explicitly addresses C++98 → C++11+
- `ENG-6.1-smart-pointer-migration.md` — shows C++98 workaround but marks it NON-COMPLIANT
- No example showing idiomatic C++98 resource management patterns as COMPLIANT

#### Confidence: `[CONFIDENT]`

---

### Version Anchor: C++14

#### What the Avatar Says

From `ref-migration-playbooks.md` (C++11→C++14):
```
| 3 | `std::make_unique` | Eliminates last reason for raw `new` in non-placement contexts |
```

From `manifest.yaml`:
```yaml
compilers:
  active_brownfield:
    - "GCC 7+ (C++14/17)"
    - "Clang 5+ (C++14/17)"
    - "MSVC 19.14+ (VS 2017 15.7+)"
```

From `examples/ENG-6.1-smart-pointers.md`:
```cpp
auto create_flight_plan(std::string flight, std::string route)
    -> std::unique_ptr<FlightPlan> {
    return std::make_unique<FlightPlan>(std::move(flight), std::move(route));
}
```

#### Version-Tagging Status: `[UNTAGGED]`

- `std::make_unique` is shown without noting it requires C++14
- The migration playbook contextualizes it (C++11→C++14 section) but example files do not
- A developer at C++11 trying to use `make_unique` would get a compile error

#### Mislead Risk: `[MEDIUM]`

- C++11 developer may assume `make_unique` is available
- Workaround (`std::unique_ptr<T>(new T(...))`) is not shown alongside

#### Example Corpus Coverage: `[PRESENT]`

- Smart pointer examples demonstrate C++14 patterns
- However, C++11-only alternatives not shown

#### Confidence: `[CONFIDENT]`

---

### Version Anchor: C++23

#### What the Avatar Says

From `manifest.yaml`:
```yaml
stack:
  language: "C++20 / C++23"
version_policy:
  greenfield: "C++20 minimum (mandatory); C++23 recommended where toolchain supports it"
```

From `examples/ENG-3.1-pmr-allocators.md` (C++17 feature, often associated with modern C++):
```cpp
#include <memory_resource>
std::pmr::monotonic_buffer_resource pool(buf, sizeof(buf));
std::pmr::vector<int> subtotals(&pool);
```

#### Version-Tagging Status: `[ASSUMED]`

- C++23 features like `std::expected` are documented but not always explicitly tagged
- From `examples/ENG-6.1-expected-errors.md`: "Note: `std::expected` is C++23 — use `tl::expected` for C++17"
- This is rare — most examples don't note version requirements

#### Mislead Risk: `[LOW]`

- Modern features are generally documented with polyfill alternatives
- The avatar's default posture assumes C++20+ for greenfield

#### Example Corpus Coverage: `[PRESENT]`

- `ENG-6.1-expected-errors.md` covers `std::expected` with C++23 tag
- PMR examples (C++17) present but not explicitly version-tagged

#### Confidence: `[CONFIDENT]`

---

## Domain 2: Concurrency

### Version Anchor: C++98/03

#### What the Avatar Says

From `ref-legacy-mental-models.md` (§9):
```
In C++03 brownfield code, use an explicit `pthread_once` or a `double-checked locking` 
pattern with a `volatile` flag plus a memory barrier
```

From `examples/ENG-6.1-thread-migration.md`:
```
**Legacy C++98:** Keep `pthread_*` but wrap in RAII class with explicit join in 
destructor; plan migration to C++11+
```

From `ref-safety-aviation.md` (AP-3: Global extern Variables):
```cpp
// BEFORE
extern int g_solver_mode;          // shared, racy under concurrent JNI calls

// AFTER (C++98-compatible)
struct SolverContext {
    int solver_mode;
    const FAR117Table far117_table;  // const after construction
};
```

#### Version-Tagging Status: `[TAGGED]`

- Thread migration example explicitly addresses C++98: "Legacy C++98: Keep `pthread_*`"
- Mental model transitions note C++03 vs C++11 memory model difference
- CWR anti-patterns show C++98-compatible patterns

#### Mislead Risk: `[LOW]`

- The avatar acknowledges C++98 threading limitations
- Guidance is "plan migration" rather than offering full C++98 threading patterns

#### Example Corpus Coverage: `[PARTIAL]`

- `ENG-6.1-thread-migration.md` mentions C++98 but focuses on POSIX→std::thread
- No dedicated C++98 threading example file

#### Confidence: `[CONFIDENT]`

---

### Version Anchor: C++14

#### What the Avatar Says

From `examples/ENG-6.1-thread-safety.md`:
```cpp
class SeatInventory {
    mutable std::mutex mtx_;
    std::atomic<uint64_t> query_count_{0};
    // ...
    bool reserve(const std::string& flight) {
        std::scoped_lock lock(mtx_);
        // ...
    }
};
```

Note: `std::scoped_lock` is C++17, not C++14. The example doesn't clarify this.

From `ref-concurrency.md`:
```
Use RAII lock guards (`std::lock_guard`, `std::scoped_lock`) — never raw `mutex.lock()`/`unlock()`
```

#### Version-Tagging Status: `[AMBIGUOUS]`

- Examples mix C++11 (`std::mutex`, `std::atomic`), C++14, and C++17 (`std::scoped_lock`) features
- No explicit version tags on which lock guard to use at which standard
- `std::lock_guard` (C++11) vs `std::scoped_lock` (C++17) distinction not made

#### Mislead Risk: `[MEDIUM]`

- A C++14 developer may use `std::scoped_lock` and get a compile error
- Should recommend `std::lock_guard` for pre-C++17

#### Example Corpus Coverage: `[PRESENT]`

- Thread safety examples exist but version-mixed
- No C++14-specific threading example

#### Confidence: `[CONFIDENT]`

---

### Version Anchor: C++23

#### What the Avatar Says

From `ref-concurrency.md` (Coroutines section):
```
C++20 coroutines (`co_await`, `co_yield`, `co_return`) enable structured asynchronous programming.
```

From `examples/ENG-3.1-coroutines.md`:
```cpp
Task<std::vector<FlightResult>> search_flights(
    std::string origin, std::string dest, std::stop_token stop) {
    // ...
    if (stop.stop_requested()) co_return results;  // cooperative cancel
}
```

From `ref-migration-playbooks.md`:
```
Priority 7: Coroutines — Async I/O — adopt only after stable executor library is chosen
```

#### Version-Tagging Status: `[AMBIGUOUS]`

- Coroutines are C++20 but example doesn't state "C++20 required"
- `std::stop_token` (C++20) used without version note
- C++23 features like `std::generator` mentioned: "NO standard task/generator types until C++23"

#### Mislead Risk: `[LOW]`

- The features used (coroutines, stop_token) are clearly modern C++20+
- A pre-C++20 developer would likely understand these are unavailable

#### Example Corpus Coverage: `[PRESENT]`

- `ENG-3.1-coroutines.md` demonstrates C++20 patterns
- No explicit C++23-only concurrency examples

#### Confidence: `[CONFIDENT]`

---

## Domain 3: Templates and Generic Programming

### Version Anchor: C++98/03

#### What the Avatar Says

The avatar does not provide C++98 template guidance. The closest reference is in `ref-legacy-smells.md`:

```
**Why it exists:** Templates were perceived as "too complex" or the developer came from C.
```

And from `ref-migration-playbooks.md`:
```
| Pattern | C++11 | C++14 | C++17 | C++20+ |
| Compile-time logic | `std::enable_if` | `std::enable_if` | `if constexpr` | Concepts |
```

#### Version-Tagging Status: `[ABSENT]`

- No C++98 template patterns documented
- The table above starts at C++11

#### Mislead Risk: `[HIGH]`

- C++98 developer asking about templates would receive SFINAE or Concepts guidance
- No acknowledgment that `std::enable_if` requires C++11

#### Example Corpus Coverage: `[ABSENT]`

- No C++98 template examples

#### Confidence: `[CONFIDENT]`

---

### Version Anchor: C++14

#### What the Avatar Says

From `ref-advanced-cpp.md`:
```
**SFINAE migration:** For brownfield code using `std::enable_if_t<>`, migrate to concepts 
as modules are modernized. New code must not use SFINAE when concepts are available.
```

SFINAE Migration Table from `ref-advanced-cpp.md`:
```
| Legacy (SFINAE) | Modern (Concepts) | Migration Notes |
|------------------|--------------------|-----------------|
| `std::enable_if_t<std::is_integral_v<T>>` | `template <std::integral T>` | Direct replacement |
```

Note: `std::enable_if_t` is C++14; `std::is_integral_v` is C++17.

#### Version-Tagging Status: `[PARTIAL]`

- SFINAE patterns shown but version requirements not explicit
- The migration table helps C++14 developers understand what to migrate to
- However, a C++14 developer wouldn't know `std::is_integral_v` requires C++17

#### Mislead Risk: `[MEDIUM]`

- `_v` and `_t` suffixes have different C++ version requirements
- `enable_if_t` is C++14; `is_integral_v` is C++17

#### Example Corpus Coverage: `[PARTIAL]`

- No dedicated C++14 template example
- SFINAE shown in migration context

#### Confidence: `[CONFIDENT]`

---

### Version Anchor: C++23

#### What the Avatar Says

From `examples/ENG-3.1-concepts.md`:
```cpp
template<typename T>
concept Serializable = requires(const T& t) {
    { t.to_json() } -> std::convertible_to<std::string>;
    { T::from_json(std::string{}) } -> std::same_as<T>;
};
```

From `ref-advanced-cpp.md`:
```
All template functions accepting constrained types must use C++20 concepts. 
Prefer named concepts over ad-hoc `requires` clauses.
```

#### Version-Tagging Status: `[TAGGED]`

- Concepts are clearly C++20 features
- The guidance explicitly states "C++20 concepts"

#### Mislead Risk: `[LOW]`

- Concepts guidance is implicitly C++20+
- Pre-C++20 developers would understand these aren't available

#### Example Corpus Coverage: `[PRESENT]`

- `ENG-3.1-concepts.md` provides dedicated example
- SFINAE to Concepts migration path documented

#### Confidence: `[CONFIDENT]`

---

## Domain 4: I/O and Streams

### Version Anchor: C++98/03

#### What the Avatar Says

No dedicated I/O/streams guidance exists in the avatar. The closest reference is from `ref-infrastructure.md`:

```
Use **spdlog** as the structured logging framework.
```

C++98 would use `printf` or `iostream` but this is not documented.

#### Version-Tagging Status: `[ABSENT]`

- No `printf` vs `iostream` guidance
- No C++98 I/O patterns

#### Mislead Risk: `[HIGH]`

- C++98 developer asking about I/O would receive no avatar-specific guidance
- Format string security risks (printf) not addressed

#### Example Corpus Coverage: `[ABSENT]`

- No I/O example files

#### Confidence: `[CONFIDENT]`

---

### Version Anchor: C++14

#### What the Avatar Says

Only indirect reference via feature detection:

From `examples/ENG-3.1-feature-detection.md`:
```cpp
#ifdef __has_include
  #if __has_include(<format>)
    #include <format>
    #define HAS_STD_FORMAT 1
  #else
    #include <fmt/format.h>  // fallback to fmtlib
    #define HAS_STD_FORMAT 0
  #endif
#endif
```

#### Version-Tagging Status: `[ABSENT]`

- No C++14-specific I/O guidance
- Feature detection shows `fmt` as polyfill but doesn't compare approaches

#### Mislead Risk: `[MEDIUM]`

- Developer may not know to use `fmt` library as `std::format` alternative
- No guidance on `iostream` performance characteristics

#### Example Corpus Coverage: `[ABSENT]`

- Feature detection file only

#### Confidence: `[CONFIDENT]`

---

### Version Anchor: C++23

#### What the Avatar Says

From `ref-migration-playbooks.md` (polyfills):
```
- `fmt::format` → backport of `std::format` for pre-C++20
```

From `manifest.yaml`:
```yaml
stack:
  language: "C++20 / C++23"
```

`std::print` (C++23) is not mentioned anywhere in the avatar.

#### Version-Tagging Status: `[PARTIAL]`

- `std::format` polyfill mentioned
- `std::print` (C++23) not documented

#### Mislead Risk: `[MEDIUM]`

- C++23 developer may not find `std::print` guidance
- The avatar's logging guidance uses spdlog, not standard library

#### Example Corpus Coverage: `[ABSENT]`

- No `std::format` or `std::print` examples

#### Confidence: `[CONFIDENT]`

---

## Domain 5: Comparison and Operators

### Version Anchor: C++98/03

#### What the Avatar Says

No explicit C++98 comparison operator guidance. From `ref-domain-modeling.md` (Value Object):

```cpp
bool operator==(const Money& other) const = default;
```

This is C++20. No C++98 equivalent shown.

#### Version-Tagging Status: `[ABSENT]`

- No C++98 comparison patterns
- Manual `operator<`, `operator==` patterns not documented

#### Mislead Risk: `[HIGH]`

- C++98 developer would need to write 6 comparison operators manually
- No guidance on this pattern

#### Example Corpus Coverage: `[ABSENT]`

- No C++98 comparison examples

#### Confidence: `[CONFIDENT]`

---

### Version Anchor: C++14

#### What the Avatar Says

No C++14-specific comparison guidance.

#### Version-Tagging Status: `[ABSENT]`

- C++14 has same manual comparison requirements as C++98
- No guidance on `std::tie` for comparison implementation

#### Mislead Risk: `[MEDIUM]`

- No pre-C++20 comparison patterns
- `std::tie` idiom for operator< not mentioned

#### Example Corpus Coverage: `[ABSENT]`

- No comparison examples for pre-C++20

#### Confidence: `[CONFIDENT]`

---

### Version Anchor: C++23

#### What the Avatar Says

From `ref-migration-playbooks.md` (C++17→C++20):
```
| Priority 2 | Three-way comparison (`<=>`) | Eliminates boilerplate comparison operators; catches bugs |
```

From `ref-domain-modeling.md`:
```cpp
bool operator==(const Money& other) const = default;
```

Note: Defaulted `operator==` is C++20, not explicitly tagged.

#### Version-Tagging Status: `[PARTIAL]`

- Three-way comparison mentioned in migration playbook
- Defaulted comparison shown but not version-tagged

#### Mislead Risk: `[LOW]`

- `= default` for comparisons is clearly modern syntax
- Migration playbook places it in C++20 section

#### Example Corpus Coverage: `[PARTIAL]`

- No dedicated `operator<=>` example file
- Defaulted comparison shown in domain modeling

#### Confidence: `[CONFIDENT]`

---

## Evidence Summary Table

| Domain | C++98/03 Status | C++14 Status | C++23 Status | Overall Mislead Risk |
|--------|-----------------|--------------|--------------|---------------------|
| Memory Management | `[PARTIAL]` | `[UNTAGGED]` | `[PRESENT]` | `[MEDIUM]` |
| Concurrency | `[TAGGED]` | `[AMBIGUOUS]` | `[AMBIGUOUS]` | `[MEDIUM]` |
| I/O and Streams | `[ABSENT]` | `[ABSENT]` | `[PARTIAL]` | `[HIGH]` |
| Templates/Generics | `[ABSENT]` | `[PARTIAL]` | `[TAGGED]` | `[MEDIUM]` |
| Comparison/Operators | `[ABSENT]` | `[ABSENT]` | `[PARTIAL]` | `[HIGH]` |

---

## Key Findings

### Gaps with Highest Mislead Risk

1. **I/O and Streams** — No `printf` vs `iostream` vs `std::format` comparison; no format string security guidance
2. **Comparison Operators** — No pre-C++20 patterns documented
3. **Templates at C++98** — No C++98 template patterns; SFINAE requires C++11

### Well-Tagged Areas

1. **Thread Migration** — Explicitly addresses C++98/C++11/C++20
2. **auto_ptr Migration** — Explicitly addresses C++98→C++11
3. **Concepts** — Clearly C++20 with SFINAE migration path

### Structural Issue

The avatar assumes a modern C++ baseline (C++20/23 for greenfield, C++14+ for brownfield) but:
- Example files lack version metadata in frontmatter
- No RAG routing based on project's declared standard
- Reference files mix version-specific guidance without clear version tags

---

*Document generated as part of C++ Avatar Version-Sensitivity Analysis.*
