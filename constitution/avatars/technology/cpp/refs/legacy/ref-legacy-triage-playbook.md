---
cpp_version_min: 98
cpp_version_note: >-
  Legacy codebase triage playbook covering C++98/03 and later.
avatar: cpp
---

# C++ Avatar Reference: Legacy Codebase Triage Playbook

---

## Legacy Codebase Triage Playbook

> Per [ENG-4.1](laws/engineering/eng-4-testing.md), code changes require test coverage. Per [ENG-6.1](laws/engineering/eng-6-security.md), security analysis must precede major refactoring. This playbook provides a structured approach to triaging and stabilizing a legacy C++ codebase in your first month.

### Week-1 Daily Priority List

**Day 1-2: Build It — Establish Reproducibility**

Your first goal is a clean, reproducible build. Nothing else matters until you can build.

```bash
# Document EXACT build steps (not "ask Bob")
git clone <repo>
cd <repo>

# Record compiler version, OS, dependencies
cmake --version && g++ --version

# Attempt build — capture ALL output
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Debug 2>&1 | tee cmake-output.log
make -j$(nproc) 2>&1 | tee build-output.log

# Run existing tests — capture baseline
ctest --output-on-failure 2>&1 | tee test-output.log

# Record: How many tests? How many pass? How many skip?
echo "BASELINE: $(grep -c 'PASSED' test-output.log) passed, $(grep -c 'FAILED' test-output.log) failed"
```

**Day 2-3: Enable Sanitizers — Measure Memory Safety Debt**

```bash
# Rebuild with sanitizers
cmake .. -DCMAKE_BUILD_TYPE=Debug \
         -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined -fno-omit-frame-pointer"
make -j$(nproc)

# Run tests under sanitizer
ctest --output-on-failure 2>&1 | tee sanitizer-output.log

# Count sanitizer findings = "memory safety debt"
grep -c "ERROR: AddressSanitizer\|ERROR: UndefinedBehaviorSanitizer" sanitizer-output.log
```

**Day 3-4: Enable Warnings — Measure Type Safety Debt**

```bash
# Add warnings WITHOUT -Werror (don't break the build)
cmake .. -DCMAKE_CXX_FLAGS="-Wall -Wextra -Wpedantic -Wno-error"
make -j$(nproc) 2>&1 | tee warning-output.log

# Count and categorize warnings
grep -c "warning:" warning-output.log
grep "warning:" warning-output.log | sed 's/.*\[-W//' | sort | uniq -c | sort -rn | head -20
```

**Day 4-5: Map Dependencies — Measure Architecture Debt**

```bash
# Generate dependency graph
cmake .. --graphviz=deps.dot
dot -Tpng deps.dot -o deps.png

# Or use include-what-you-use
iwyu_tool.py -p build/ -- -Xiwyu --no_fwd_decls 2>&1 | tee iwyu-output.log

# Identify circular dependencies and god headers
# God header = included by >50% of translation units
grep -rh '#include' src/ | sort | uniq -c | sort -rn | head -20
```

**Day 5: Write 5 Characterization Tests**

Target the 5 most-called public functions. These tests document *current behavior* — not correctness:

```cpp
// Characterization test — documents existing behavior, not intent
TEST(FlightServiceCharacterization, parseFlightNumber_standard_format) {
    // This test captures what the code DOES, not what it SHOULD do
    auto result = FlightService::parseFlightNumber("AA100");
    EXPECT_EQ(result.carrier, "AA");
    EXPECT_EQ(result.number, 100);
}

TEST(FlightServiceCharacterization, parseFlightNumber_with_leading_zeros) {
    auto result = FlightService::parseFlightNumber("AA0042");
    EXPECT_EQ(result.number, 42);  // Discovered: leading zeros stripped
}
```

### Month-1 Remediation Plan

**Weeks 1-2: Establish CI Safety Net**

| Goal | Metric | Target |
|------|--------|--------|
| Green CI | All existing tests pass | 100% pass rate |
| Warning baseline | Compiler warnings tracked | Counted, categorized |
| Sanitizer CI | ASan + UBSan run on every PR | Job exists and runs |
| Characterization tests | Tests for critical paths | 20+ tests |

**Week 3: Fix CRITICAL Sanitizer Findings**

Priority order for sanitizer fixes:
1. **Use-after-free** — Convert to `unique_ptr` or `shared_ptr`
2. **Buffer overflow** — Replace raw arrays with `std::vector` or `std::array`
3. **Uninitialized reads** — Add initializers, use RAII
4. **Data races** — Add `std::mutex` or use `std::atomic`

**Week 4: Begin const Correctness and override Sweep**

Start with **leaf modules** (modules that depend on nothing else):
1. Add `const` to every parameter and member function that doesn't mutate
2. Add `override` to every virtual function override
3. Add `[[nodiscard]]` to functions whose return value should never be ignored
4. Each sweep is one PR per module

### The "DO NOT TOUCH" List

Per [ENG-4.1](laws/engineering/eng-4-testing.md), some code should be explicitly left alone during triage:

| # | Category | Reason |
|---|----------|--------|
| 1 | Working code in unrelated modules | Risk exceeds value; no test coverage to verify changes |
| 2 | Third-party / vendored code | Upstream maintains it; local changes prevent updates |
| 3 | Platform-specific `#pragma` directives | Compiler-specific behavior; changes may break other platforms |
| 4 | Global variable initialization order | C++ static initialization order is undefined across TUs; touching it causes Heisenbugs |
| 5 | Performance-critical hot loops | Requires profiling before AND after; premature modernization may regress |
| 6 | Naming conventions in untouched files | Consistency within a file > consistency across codebase; rename only when modifying |

### Building a Safety Net of Characterization Tests

> Characterization tests document what the code *does*, not what it *should* do. They are your safety net for refactoring.

**Procedure:**

1. **Identify critical paths** — trace every HTTP request handler, every message queue consumer, every scheduled job entry point. For aviation: booking, check-in, crew scheduling, weight-and-balance, flight planning.

2. **Test black-box behavior** — call the public API with known inputs, assert on outputs. Do NOT read the implementation first — you're testing behavior, not code.

3. **Test error paths** — pass null, empty string, negative numbers, maximum values. Document what the code does (even if it's wrong). These tests protect against regression during refactoring.

4. **Use Approval Testing pattern** for complex outputs:

```cpp
// Instead of asserting each field, snapshot the entire output
TEST(ManifestCharacterization, fullManifest_approval) {
    auto manifest = ManifestService::generate("AA100", "2025-06-20");
    // First run: creates approved/manifest_AA100.txt
    // Subsequent runs: diffs against approved snapshot
    Approvals::verify(manifest.toString());
}
```

5. **Target: 50+ characterization tests in month 1.** This sounds aggressive but each test is simple — call function, assert output. 10 per critical module × 5 modules = 50.

### Identifying Seams for Safe Modification

Per Michael Feathers' *Working Effectively with Legacy Code*, a **seam** is a place where you can alter behavior without editing the code at that point. C++ offers three types:

**Preprocessing Seam:**

```cpp
// In production:
#include "RealDatabase.h"

// In test (via compile flag -DTEST_BUILD):
#ifdef TEST_BUILD
#include "MockDatabase.h"
#else
#include "RealDatabase.h"
#endif
```

Use sparingly — this is a blunt instrument, but it's the fastest way to inject a test double in legacy code with no interfaces.

**Link Seam:**

```cpp
// Production build links: FlightService.o + RealDatabase.o
// Test build links:       FlightService.o + MockDatabase.o

// Same header (Database.h), different .cpp files at link time
// FlightService never changes — only the linked .o file differs
```

This is powerful for legacy code where you cannot change the source. Create a mock `.cpp` with identical function signatures.

**Object Seam:**

```cpp
// Extract interface from concrete class
class IDatabase {
public:
    virtual ~IDatabase() = default;
    virtual FlightRecord lookup(const std::string& pnr) = 0;
};

// Production: class RealDatabase : public IDatabase { ... };
// Test:       class MockDatabase : public IDatabase { ... };

// Inject via constructor
class FlightService {
    std::unique_ptr<IDatabase> db_;
public:
    explicit FlightService(std::unique_ptr<IDatabase> db)
        : db_(std::move(db)) {}
};
```

This is the gold standard. Prefer object seams for new code per [ENG-3.1](laws/engineering/eng-3-code-quality.md).

### Metrics to Track

| Metric | Tool | Frequency | Target Trend |
|--------|------|-----------|-------------|
| Compiler warning count | `-Wall -Wextra` output | Every PR | ↓ Decreasing |
| Sanitizer finding count | ASan + UBSan | Every PR | ↓ Decreasing |
| Characterization test count | CTest / GTest | Weekly | ↑ Increasing |
| Cyclomatic complexity | `lizard`, `cppcheck` | Weekly | ↓ Decreasing (for modified files) |
| Build time (clean) | CI metrics | Weekly | ↓ or stable |
| Build time (incremental) | CI metrics | Weekly | ↓ Decreasing |
| Include depth (max) | `iwyu` | Monthly | ↓ Decreasing |

---

## Priority Matrix
| Module | Risk (1-5) | Impact (1-5) | Score | Status |
|--------|-----------|--------------|-------|--------|
| FlightService | 5 | 5 | 25 | In Progress |
| CrewScheduler | 4 | 4 | 16 | Planned Q3 |
| BookingEngine | 3 | 5 | 15 | Planned Q4 |
```

**2. Establish compiler warning dashboard.**

Track warning counts by module over time. Make it visible. Celebrate when a module hits zero warnings.

```bash
# Per-module warning count script
for dir in src/*/; do
    module=$(basename "$dir")
    count=$(grep -c "warning:.*$dir" build-output.log)
    echo "$module: $count warnings"
done | sort -t: -k2 -rn
```

**3. Champion incremental compiler upgrades.**

Add a newer compiler as a CI build (e.g., GCC 14 alongside GCC 11). Don't enforce it yet — just make it visible. Track new warnings. When the team is ready, make it the default.

**4. Train the team.**

Share the Mental Model Transitions section with new developers. Run a "C++ Gotchas" session covering UB, RAII, and value semantics. Create a team wiki page with your codebase-specific patterns and pitfalls.

---

## See Also

- [Legacy Code Smell Catalog](ref-legacy-smells.md)
- [Mental Model Transitions](ref-legacy-mental-models.md)


---

## See Also

- [Legacy Navigation](ref-legacy-navigation.md)
