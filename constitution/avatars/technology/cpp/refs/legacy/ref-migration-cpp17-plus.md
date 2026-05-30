---
cpp_version_min: 98
cpp_version_note: >-
  Migration guide from C++98 through C++17+; documents pre-modern patterns as starting point.
avatar: cpp
---

# C++ Avatar Reference: Migration Patterns (C++17+ and Survival)

---

## Survival Patterns

> Per [ENG-4.1](laws/engineering/eng-4-testing.md) and [ENG-3.1](laws/engineering/eng-3-code-quality.md), developers joining a legacy C++ codebase need a structured progression from cautious reader to confident contributor. This section replaces ad-hoc onboarding with a deliberate skill development path.

### Week 1: Reading and Understanding

Your first week is about building a mental model, not writing code. Resist the urge to fix things.

**1. Read execution-path-first, not top-down.**

Don't start with `main.cpp` line 1. Instead, pick a user-facing feature (e.g., "flight search") and trace the execution path from the entry point through every function call. Use your IDE's "Go to Definition" or grep to follow the chain.

```bash
# Find the entry point for a feature
grep -rn "searchFlight\|findFlight\|lookupFlight" src/ --include="*.cpp"
# Then trace each function call depth-first
```

**2. Use a debugger as a reading tool.**

Set a breakpoint at the entry point and step through with real input. GDB/LLDB show you what the code *actually does*, not what you think it does.

```bash
# Build with debug symbols
cmake .. -DCMAKE_BUILD_TYPE=Debug
make -j$(nproc)

# Run under GDB with a test case
gdb --args ./flight_service --test-mode
(gdb) break FlightService::search
(gdb) run
(gdb) step   # Step INTO function calls
(gdb) next   # Step OVER function calls
(gdb) print flight.carrier_  # Inspect state
```

**3. Draw the module dependency graph.**

On paper or with Graphviz. Boxes are modules/libraries. Arrows are `#include` or link dependencies. This reveals the architecture faster than reading code.

**4. Annotate pointer ownership.**

For every raw pointer you encounter, write in a comment: `// OWNS` or `// BORROWS`. This exercise surfaces lifetime bugs and unclear ownership — the #1 source of legacy C++ defects.

```cpp
class FlightService {
    Database* db_;        // BORROWS — created and owned by main()
    Route* cachedRoute_;  // OWNS — allocated in loadRoute(), freed in destructor
    // ^ This mismatch (raw pointer owns) is a smell. Should be unique_ptr.
};
```

**5. Read CMakeLists.txt / Makefile like a map.**

The build system tells you:
- What libraries exist (targets)
- What depends on what (`target_link_libraries`)
- What compiler flags are active (warnings, sanitizers, optimization)
- What third-party dependencies are used (`find_package`)

**6. Use `git log --follow` for archaeological record.**

```bash
# Who last changed this file and why?
git log --follow --oneline -20 -- src/FlightService.cpp

# When was this function last modified?
git log -p -S "parseFlightNumber" -- src/FlightService.cpp

# Who knows this module best? (most commits)
git shortlog -sn -- src/flight/
```

### Month 1: Safe Modification Patterns

You've built a mental model. Now make changes safely, one pattern at a time.

**1. Sprout Method**

Add new logic in a new function. Call it from the existing code. The existing function is unchanged except for the new call.

```cpp
// BEFORE — need to add validation
void processBooking(const Booking& b) {
    // ... 200 lines of existing logic ...
    save(b);
}

// AFTER — sprouted method
void validateBookingDates(const Booking& b) {  // NEW — fully testable
    if (b.departureDate() < Clock::now()) {
        throw InvalidBookingError("Departure in the past");
    }
}

void processBooking(const Booking& b) {
    validateBookingDates(b);  // NEW — one line added
    // ... 200 lines of existing logic unchanged ...
    save(b);
}
```

**2. Wrap Method**

Rename the existing function to `_impl`. Create a new function with the original name that calls `_impl` plus your new logic.

```cpp
// BEFORE
void FlightService::updateGate(const std::string& gate) {
    // ... existing logic ...
}

// AFTER
void FlightService::updateGate_impl(const std::string& gate) {
    // ... existing logic unchanged ...
}

void FlightService::updateGate(const std::string& gate) {
    auditLog("gate_change", gate);  // NEW behavior
    updateGate_impl(gate);          // Original behavior
    notifyPassengers(gate);         // NEW behavior
}
```

**3. Extract Interface**

Create a pure virtual base class. The existing class inherits from it. Tests use a mock implementation.

```cpp
// Extract from concrete class
class ICrewScheduler {
public:
    virtual ~ICrewScheduler() = default;
    virtual CrewAssignment assign(const Flight& f) = 0;
};

// Existing class now implements the interface
class CrewScheduler : public ICrewScheduler {
public:
    CrewAssignment assign(const Flight& f) override;
};

// Test mock
class MockCrewScheduler : public ICrewScheduler {
public:
    CrewAssignment assign(const Flight& f) override {
        return CrewAssignment::createDefault();
    }
};
```

**4. RAII Conversion**

Pick the single highest-value resource (most error-prone cleanup) and wrap it in RAII. One resource per PR.

```cpp
// BEFORE — manual lock management
void FlightService::updateStatus(FlightStatus status) {
    mutex_.lock();
    // ... what if this throws? Deadlock!
    status_ = status;
    mutex_.unlock();
}

// AFTER — RAII lock guard
void FlightService::updateStatus(FlightStatus status) {
    std::lock_guard<std::mutex> lock(mutex_);  // RAII — always released
    status_ = status;
    // lock_guard destructor releases mutex, even on exception
}
```

**5. Boy Scout Rule** — only modernize code you are already modifying (add `const`, `override`, smart pointers, `[[nodiscard]]`). Do NOT modernize untouched functions in the same file — that's scope creep.

### Month 3+: Contributing with Confidence

- New code follows modern standards (smart pointers, RAII, `const`, `[[nodiscard]]`). Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), new code must not introduce new technical debt.
- Create "islands of quality" — 100% test coverage, zero warnings, documented API, clean dependency graph.
- Propose small modernization PRs scoped to modules you've worked in.
- Build characterization test suite to 100+ tests (foundation for future refactoring).
- By month 6, create `MODERNIZATION_PLAN.md` prioritized by risk × impact. See `ref-legacy-navigation.md` for the full priority matrix.


---

## ActiveTest.h → GoogleTest Migration Playbook

> Per [ENG-4.1](laws/engineering/eng-4-testing.md): new tests must use
> GoogleTest; existing ActiveTest.h tests may coexist until migration completes.
> This playbook maps IOC_ALP's `TestRunner.lib + ActiveTest.h` idioms to
> canonical GTest equivalents.

### Macro Mapping Table

| ActiveTest.h | GoogleTest Equivalent | Notes |
|-------------|----------------------|-------|
| `ACTIVE_TEST(Suite, Name)` | `TEST(Suite, Name)` | Direct 1:1 replacement |
| `ACTIVE_TEST_F(Suite, Name)` | `TEST_F(Suite, Name)` | Fixture must inherit `testing::Test` |
| `CHECK_EQ(a, b)` | `EXPECT_EQ(a, b)` | Non-fatal; use ASSERT_EQ to abort |
| `CHECK_TRUE(x)` | `EXPECT_TRUE(x)` | Non-fatal |
| `CHECK_FALSE(x)` | `EXPECT_FALSE(x)` | Non-fatal |
| `FAIL_TEST("msg")` | `FAIL() << "msg"` | Aborts current test |
| `PASS_TEST()` | _(remove)_ | GTest passes by default if no assertion fails |
| Manual `try/catch + FAIL_TEST` | `EXPECT_THROW(expr, Type)` | See exception section |
| `TestRunner::run()` in `main()` | `RUN_ALL_TESTS()` | See entry point section |

### Step-by-Step Migration for IOC_ALP

**Step 1 — Add GoogleTest via vcpkg (MSVC / Visual Studio)**

```
vcpkg install gtest:x64-windows
# or in vcpkg.json:
{ "dependencies": ["gtest"] }
```

**Step 2 — CMakeLists.txt** (new test binary per module)

```cmake
find_package(GTest CONFIG REQUIRED)

add_executable(FlightServiceTests FlightServiceTest.cpp)
target_link_libraries(FlightServiceTests PRIVATE GTest::gtest_main GTest::gmock)
add_test(NAME FlightServiceTests COMMAND FlightServiceTests)
```

**Step 3 — Replace `#include "ActiveTest.h"` with GTest header**

```cpp
// BEFORE
#include "ActiveTest.h"

// AFTER
#include <gtest/gtest.h>
```

**Step 4 — Convert one test at a time (Strangler Fig)**

Start with the lowest-risk test class. Convert `ACTIVE_TEST` → `TEST`,
verify the new test passes, then delete the ActiveTest.h version.
Do NOT convert in bulk — each conversion is its own TDD cycle.

**Step 5 — Explicit main() if using GFlags**

```cpp
int main(int argc, char** argv) {
    testing::InitGoogleTest(&argc, argv);
    // If test uses DEFINE_int32 / DEFINE_double:
    // gflags::ParseCommandLineFlags(&argc, &argv, true);
    return RUN_ALL_TESTS();
}
```

### Migration Anti-Patterns

```cpp
// NON-COMPLIANT — copy-pasting ActiveTest assertions unchanged
CHECK_EQ(flight.zfw(), 87500);   // CHECK_EQ is not GTest; will fail to compile

// COMPLIANT — translated to GTest
EXPECT_EQ(flight.zfw(), 87500);
```

---

## See Also

- [Migration Playbooks (Pre-C++17 Foundation)](ref-migration-pre-cpp17.md)
