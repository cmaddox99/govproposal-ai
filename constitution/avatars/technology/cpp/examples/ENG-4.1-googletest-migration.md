---
law_id: ENG-4.1
cpp_version_min: 14
avatar: cpp
title: "IOC_ALP: GoogleTest Migration — ActiveTest.h to TEST_F"
description: "Demonstrates the correct TDD migration pattern from IOC_ALP ActiveTest.h to GoogleTest TEST_F with EXPECT_THROW and fixture setup."
source: "facebook/folly/tree/main/folly/test — CancellationTokenTest, ConstructorCallbackListTest"
---

# ENG-4.1: GoogleTest Migration — ActiveTest.h to TEST_F

## Context

IOC_ALP uses `TestRunner.lib + ActiveTest.h` — a legacy Windows-only test
harness. New and migrated tests **must** use GoogleTest. This example shows the
correct migration of a flight-service unit test.

---

## NON-COMPLIANT — ActiveTest.h Pattern

```cpp
// ActiveTest.h — IOC_ALP legacy test harness
#include "ActiveTest.h"

ACTIVE_TEST(FlightServiceTest, LoadFlightByNumber) {
    CFlightService svc;
    CFlight* f = svc.loadFlight("AA100");
    CHECK_TRUE(f != nullptr);
    CHECK_EQ(f->getNumber(), "AA100");
    // No TearDown — f leaks if CHECK fails mid-test
}

ACTIVE_TEST(FlightServiceTest, LoadMissingFlightThrows) {
    CFlightService svc;
    bool threw = false;
    try {
        svc.loadFlight("ZFW-999");
    } catch (...) {
        threw = true;
    }
    CHECK_TRUE(threw);
}
```

**Problems:**
- `CHECK_*` macros are not GoogleTest — will not compile with `gtest/gtest.h`
- Manual `try/catch` obscures the expected exception type
- Raw pointer `CFlight*` leaks on assertion failure

---

## COMPLIANT — GoogleTest TEST_F Pattern

```cpp
#include <gtest/gtest.h>

class FlightServiceTest : public testing::Test {
protected:
    void SetUp() override {
        // NOTE: If CFlightService requires MFC/CObject-derived constructor
        // arguments (common in IOC_ALP), inject them here or use a factory:
        //   svc_ = CFlightService::CreateForTest(mock_deps_);
        svc_ = std::make_unique<CFlightService>();
    }
    std::unique_ptr<CFlightService> svc_;
};

TEST_F(FlightServiceTest, LoadFlightByNumber) {
    auto flight = svc_->loadFlight("AA100");
    ASSERT_NE(flight, nullptr);
    EXPECT_EQ(flight->getNumber(), "AA100");
}

TEST_F(FlightServiceTest, LoadMissingFlightThrows) {
    EXPECT_THROW(svc_->loadFlight("ZFW-999"), CFlightNotFoundException);
}
```

**Why this is correct (per ENG-4.1):**
- `TEST_F` groups tests under a fixture with automatic `SetUp`/`TearDown`
- `ASSERT_NE` aborts if pointer is null — prevents null dereference below
- `EXPECT_THROW` names the exact exception type from the CALPException hierarchy
- `unique_ptr` in fixture data member — no leak on assertion failure

## Edge Cases & Warnings

- **`ASSERT_*` vs `EXPECT_*` in migration** — ActiveTest's `CHECK_TRUE` equivalent is `EXPECT_TRUE` (continues on failure) not `ASSERT_TRUE` (aborts test). Use `ASSERT_*` only when continuing the test after failure would cause undefined behavior (null dereference, corrupted state). Over-use of `ASSERT_*` hides multiple failures per test run.
- **MFC class default construction** — The `CFlightService` fixture uses `std::make_unique<CFlightService>()`. If the class derives from `CObject` or uses MFC `DECLARE_DYNCREATE`, it may require a registered factory or explicit heap construction via `new`. Use `SetUp()` to inject dependencies rather than in-line initialization in the member declaration.
- **`EXPECT_THROW` requires exact exception type** — `EXPECT_THROW(expr, CFlightNotFoundException)` fails if the code throws a base class (`CBaseException`). If the exception hierarchy changes during migration, update throw specs in tests before updating production code (RED step for the new exception type).
- **Macro name collisions** — ActiveTest macros (`CHECK_EQ`, `TEST_SETUP`) may collide with GTest macros if both headers are included during incremental migration. Guard the transition with `#ifdef ACTIVETEST_LEGACY` blocks and remove after migration is complete.
