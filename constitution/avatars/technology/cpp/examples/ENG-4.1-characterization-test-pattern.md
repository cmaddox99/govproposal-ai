---
law_id: ENG-4.1
cpp_version_min: 98
cpp_version_note: >-
  GoogleTest 1.8.x (final C++98-compatible release, EOL 2018) works with C++98/03
  projects on GCC and MSVC 8.0+ (VS 2005+). Use vcpkg pin: "gtest==1.8.1".
  MSVC 7.1 (VS 2003) is not officially supported but workable with patches to
  gtest-port.h (GTEST_HAS_TR1_TUPLE=0, type-trait stubs, _MSC_VER >= 1310).
  Modern GoogleTest (1.12+) requires C++11. For MSVC 6.0, see the stdlib-only
  golden-master pattern in ref-brownfield-survival.md.
avatar: cpp
---

# [ENG-4.1](laws/engineering/eng-4-testing.md): Characterization Test Pattern

## The Rule

Characterize before refactoring: never modify legacy code until you have tests that pin its current behavior. This creates a safety net proving your refactoring didn't break anything.

## When to Use

- **Legacy code with no tests** — inherited C or C++98 modules (fare calculators, ACARS parsers, weight-and-balance engines) that were written before your test framework existed.
- **Pre-refactoring** — before converting manual resource management to RAII, before introducing smart pointers, before extracting a class.
- **Bug investigation** — write a characterization test that reproduces the reported behavior, *then* decide if it's a bug or intended.

## Context

Before modifying legacy code, write characterization tests capturing existing behavior. These prove you haven't broken anything. Characterization tests document what code *does*, not what it *should* do.

## NON-COMPLIANT: Modifying Without Tests

```cpp
// Developer "modernizes" legacy function without tests
// Risk: silently changes behavior other modules depend on
int calculateFare(const char* origin, const char* dest, int paxCount) {
    // 200 lines of undocumented logic...
}
// Refactored version changes return semantics — breaks all callers
```

## COMPLIANT: Characterization Tests First

```cpp
#include <gtest/gtest.h>
extern "C" {
#include "legacy_fare_calculator.h"
}

class FareCharTest : public ::testing::Test {
protected:
    void SetUp() override { initFareDatabase("/data/fares.dat"); }
    void TearDown() override { shutdownFareDatabase(); }
};

// Capture behavior for known route
TEST_F(FareCharTest, DFW_to_LAX_single_pax) {
    EXPECT_EQ(calculateFare("DFW", "LAX", 1), 34500); // cents
}

// Capture edge case — zero passengers
TEST_F(FareCharTest, zero_passengers_returns_zero) {
    EXPECT_EQ(calculateFare("DFW", "LAX", 0), 0);
}

// Capture unknown route behavior
TEST_F(FareCharTest, unknown_route_returns_negative) {
    EXPECT_EQ(calculateFare("XXX", "YYY", 1), -1);
}

// Capture null input behavior
TEST_F(FareCharTest, null_origin_returns_negative) {
    EXPECT_EQ(calculateFare(nullptr, "LAX", 1), -2);
}
```

Per [ENG-4.1](laws/engineering/eng-4-testing.md): commit tests first, refactor second, fix bugs third.

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Characterization test encodes a bug | Legacy returns `-1` for unknown route; test pins that behaviour; the real answer should be `std::nullopt` | Keep the test green *during* refactoring; fix the bug in a **separate** commit after the refactoring is stable and reviewed |
| Non-deterministic legacy code (global state, wall-clock time, uninitialised memory) | Characterization test flakes randomly | Isolate global state in `SetUp()`/`TearDown()`; seed random generators before pinning outputs; mark flaky tests `DISABLED_` until stabilised |
| Over-characterizing internal helper functions | Tests couple to implementation details that will change during refactoring; tests break even when external behaviour is preserved | Focus on public API boundaries only; internal helpers are tested indirectly through the public interface |
