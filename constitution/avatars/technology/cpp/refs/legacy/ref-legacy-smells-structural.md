---
cpp_version_min: 98
cpp_version_note: >-
  Legacy code structural smells catalog; applies to C++98/03 codebases.
avatar: cpp
---

# C++ Avatar Reference: Legacy Code Smells - Structural

---

## Legacy Code Smell Catalog

> Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), legacy C++ codebases accumulate characteristic patterns of technical debt. This catalog enables rapid identification, triage, and remediation of the 14 most common C++ code smells. Each smell includes recognition patterns, severity classification, historical context, and incremental remediation strategies compatible with [ENG-4.1](laws/engineering/eng-4-testing.md) Atomic TDD.

### Summary Table

| # | Smell | Severity | Recognition | One-Line Fix |
|---|-------|----------|-------------|-------------|
| 1 | God Classes (>2000 LOC) | CRITICAL | Single file >2000 lines, 50+ methods | Extract Class by responsibility |
| 2 | Deep Inheritance (4+ levels) | CRITICAL | `class D : public C : public B : public A` | Flatten hierarchy, prefer composition |
| 3 | Circular `#include` Dependencies | HIGH | Build breaks when header order changes | Forward declarations + PIMPL |
| 4 | `#ifdef` Spaghetti | HIGH | Nested `#ifdef` blocks >3 levels deep | `if constexpr`, strategy pattern |
| 5 | Copy-Paste Polymorphism | HIGH | Near-identical functions differing by type | Templates or virtual dispatch |
| 6 | Singleton Abuse | HIGH | `::getInstance()` scattered throughout | Dependency injection |
| 7 | Fragile Base Class | MEDIUM | Base class change breaks 10+ derived classes | NVI pattern, composition |
| 8 | Header-Only Bloat | MEDIUM | Build takes >10 min, touching one header rebuilds everything | PIMPL + forward declarations |
| 9 | Rule of 3/5/0 Violations | HIGH | Custom destructor but no copy/move ops | `= default` all or Rule of 0 |
| 10 | Implicit Conversion Abuse | HIGH | Surprising function calls with wrong type | `explicit` on single-arg constructors |
| 11 | Public Data Members | MEDIUM | `obj.member = value` throughout codebase | Encapsulate or use plain struct |
| 12 | Output Parameter Overuse | MEDIUM | `void getFlight(Flight& out)` pattern | Return by value (move semantics) |
| 13 | Mixed Error Handling | HIGH | Exceptions + error codes + errno in same module | One strategy per module boundary |
| 14 | Multiple Return Paths with Resource Cleanup | CRITICAL | `goto cleanup;` or repeated `delete` before `return` | RAII guards |

### 1. God Classes (>2000 LOC)

**Recognition pattern:** A single class file exceeds 2000 lines. The class has 50+ methods spanning unrelated responsibilities (e.g., `FlightManager` handles scheduling, pricing, crew assignment, and logging). Constructor takes 15+ parameters.

**Severity:** CRITICAL — These classes are the #1 source of merge conflicts and untestable code.

**Why it exists:** Organic growth over years. Each feature was "just one more method." No ownership boundaries enforced.

**Remediation:**
1. Identify 3-5 responsibility clusters (use method call graphs)
2. Extract each cluster into a new class with a focused interface
3. Original class becomes a façade delegating to extracted classes
4. Each extraction is one PR with characterization tests

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Add characterization tests for methods being extracted
- Commit 2: Extract class with methods moved (tests still pass)
- Commit 3: Update callers to use new class directly
- Commit 4: Remove delegation methods from original class

### 2. Deep Inheritance Hierarchies (4+ levels)

**Recognition pattern:** Class hierarchy exceeds 4 levels. Adding behavior requires understanding all ancestor classes. `dynamic_cast` used frequently to work around rigid hierarchy. "Diamond" inheritance patterns emerge.

**Severity:** CRITICAL — Tight coupling makes any base class change cascade unpredictably.

**Why it exists:** 1990s OOP culture promoted deep hierarchies as "proper design." Java/C++ textbooks taught `Animal → Mammal → Dog → GuideDog`.

**Remediation:**
1. Identify which levels add behavior vs. merely categorize
2. Flatten categorization levels into composed components
3. Extract interfaces (pure virtual base classes) for polymorphic needs
4. Use composition: `GuideDog` *has-a* `GuidingBehavior`, not *is-a* chain

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Characterization tests for leaf classes
- Commit 2: Extract component class for one responsibility
- Commit 3: Replace inheritance with composition for that responsibility
- Commit 4: Repeat for next responsibility

### 3. Circular `#include` Dependencies

**Recognition pattern:** Header A includes Header B, which includes Header C, which includes Header A. Build breaks when include order changes. Adding an include in one file causes unrelated compile errors.

**Severity:** HIGH — Circular includes cause cryptic compile errors and massively slow builds.

**Why it exists:** Classes reference each other (Flight references Crew, Crew references Flight). Without forward declarations, developers reach for `#include`.

**Remediation:**
1. Map the dependency cycle using `include-what-you-use` or manual inspection
2. Replace includes with forward declarations wherever possible (`class Flight;`)
3. For remaining cycles, apply PIMPL (Pointer to Implementation) to break the chain
4. Apply dependency inversion: both depend on an abstract interface

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Add forward declarations, remove unnecessary includes (build still works)
- Commit 2: Apply PIMPL to one side of the cycle
- Commit 3: Verify build time improvement; add characterization test

### 4. `#ifdef` Spaghetti

**Recognition pattern:** Nested `#ifdef` blocks 3+ levels deep. Same `#ifdef` condition repeated in 10+ files. Logic flow is impossible to follow because half the code may not exist depending on build flags.

**Severity:** HIGH — Untestable code paths. Combinatorial explosion of configurations.

**Why it exists:** Platform-specific code, feature flags, and debug instrumentation accumulated over decades.

**Remediation:**
1. Catalog all `#ifdef` symbols — many are dead (platform no longer supported)
2. Replace compile-time branches with `if constexpr` where possible (C++17)
3. Use strategy pattern or policy classes for platform-specific behavior
4. Move build-system configuration to CMake options, not in-source `#ifdef`

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Remove dead `#ifdef` branches (verify with build matrix)
- Commit 2: Replace one `#ifdef` cluster with `if constexpr` or strategy
- Commit 3: Add tests covering both code paths

### 5. Copy-Paste Polymorphism

**Recognition pattern:** Near-identical functions that differ only in type or minor logic. `processBoeing737()`, `processAirbus320()`, `processEmbraer175()` with 90% identical bodies.

**Severity:** HIGH — Bug fixes applied to one copy are missed in others.

**Why it exists:** Templates were perceived as "too complex" or the developer came from C.

**Remediation:**
1. Identify the varying axis (type, algorithm, configuration)
2. For type variation: extract a template
3. For algorithm variation: extract a virtual interface or strategy
4. For configuration: extract a data-driven approach

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Tests for one variant (characterization)
- Commit 2: Extract common logic into template/base
- Commit 3: Convert remaining variants to use the common code
- Commit 4: Delete dead copy-paste variants

### 6. Singleton Abuse

**Recognition pattern:** `FlightCache::getInstance()`, `Logger::getInstance()` called from dozens of files. Unit tests cannot run in parallel because singletons carry global state. Test setup requires "resetting" singletons.

**Severity:** HIGH — Singletons are hidden global state that makes testing and concurrency extremely difficult.

**Why it exists:** Design Patterns (GoF) popularized singletons. They were the easy answer to "where do I put shared state?"

**Remediation:**
1. Identify all call sites of `getInstance()`
2. Add the singleton as a constructor parameter (dependency injection)
3. Create an interface for the singleton's public API
4. In tests, inject a mock; in production, inject the real implementation
5. Finally, remove the `getInstance()` method

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Extract interface from singleton
- Commit 2: Add constructor parameter to one consumer class
- Commit 3: Add unit test using mock implementation
- Commit 4: Migrate remaining consumers (may span multiple PRs)

### 7. Fragile Base Class

**Recognition pattern:** Changing a virtual function's behavior in a base class unexpectedly breaks 10+ derived classes. Base class methods call virtual functions internally, creating invisible contracts.

**Severity:** MEDIUM — Silent breakage that manifests only in derived class behavior.

**Why it exists:** Base classes grew "smart" over time, calling their own virtual functions from non-virtual public methods. Derived classes depend on internal call sequences.

**Remediation:**
1. Apply **Non-Virtual Interface (NVI) pattern**: public methods are non-virtual, calling private virtual "customization points"
2. Prefer composition — extract the varying behavior into a separate object
3. Document the base class's internal contract explicitly

**Commit strategy per [ENG-4.1](laws/engineering/eng-4-testing.md):**
- Commit 1: Characterization tests for base + derived behavior
- Commit 2: Convert one public virtual to NVI
- Commit 3: Repeat for next virtual method


---

## See Also

- [Legacy Code Smells - Patterns](ref-legacy-smells-patterns.md)
