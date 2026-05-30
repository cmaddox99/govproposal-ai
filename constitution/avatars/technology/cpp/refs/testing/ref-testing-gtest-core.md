---
cpp_version_min: 98
cpp_version_note: >-
  GoogleTest 1.8.x is the final release with C++98/03 compiler support (EOL 2018).
  Pin with vcpkg "gtest==1.8.1" for C++98/03 projects on GCC or MSVC 8.0+ (VS 2005+).
  MSVC 7.1 (VS 2003) is not officially supported but workable with manual patches
  to gtest-port.h: set GTEST_HAS_TR1_TUPLE=0, add type-trait stubs, adjust the
  _MSC_VER check to >= 1310. GoogleTest 1.12+ requires C++11 minimum. MSVC 6.0
  (VS 6.0) has no viable path with any GTest release; use the stdlib golden-master
  pattern in ref-brownfield-survival.md instead.
avatar: cpp
---

# C++ Avatar Reference: GoogleTest Core Patterns

---

## Testing Framework

**Primary Framework:** GoogleTest + GoogleMock

### Test Structure

```cpp
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "order_service.h"
#include "mock_order_repository.h"

class OrderServiceTest : public ::testing::Test {
protected:
    MockOrderRepository repository_;
    OrderService service_{repository_};
};

TEST_F(OrderServiceTest, CreateOrderReturnsNewDraftOrder) {
    // Arrange
    auto customer_id = CustomerId{"cust-123"};

    // Act
    auto order = service_.create_order(customer_id);

    // Assert
    EXPECT_EQ(order.customer_id(), customer_id);
    EXPECT_EQ(order.status(), OrderStatus::kDraft);
    EXPECT_EQ(order.total(), Money::zero());
}

TEST_F(OrderServiceTest, AddItemUpdatesTotal) {
    // Arrange
    auto order = Order::create(CustomerId{"cust-123"});
    auto product = Product{"SKU-1", Money::of(100)};

    // Act
    order.add_item(product, 2);

    // Assert
    EXPECT_EQ(order.total(), Money::of(200));
}
```

### Testing Patterns

- Use `TEST_F` with fixtures for shared setup; `TEST` for standalone cases
- Use `EXPECT_*` for non-fatal assertions, `ASSERT_*` when continuation is meaningless
- Use `MOCK_METHOD` for mock definitions with `EXPECT_CALL` / `ON_CALL`
- Separate unit tests (`tests/unit/`) from integration tests (`tests/integration/`)
- Use parameterized tests with `INSTANTIATE_TEST_SUITE_P` for data-driven tests
- Per [ENG-4.1](laws/engineering/eng-4-testing.md): one test per TDD (Test-Driven Development) cycle, RED→GREEN→REFACTOR

### Testing Framework Policy

**Approved framework:** GoogleTest 1.14+ with GoogleMock (bundled in the same distribution).

**Version requirement:**
- GoogleTest **1.14.0 minimum** — required for full C++20 compatibility and improved `MOCK_METHOD` support
- Include via `vcpkg` (preferred): add `gtest` to `vcpkg.json`; or via CMake `FetchContent`:

```cmake
include(FetchContent)
FetchContent_Declare(googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG v1.14.0)
FetchContent_MakeAvailable(googletest)
```

**Mocking governance:**
- GoogleMock is the approved mocking framework — avoid third-party mocking libraries unless documented exception exists
- Use `MOCK_METHOD` macro (not the legacy `MOCK_METHODn` variants)
- Prefer `NiceMock<T>` for tests that don't care about uninteresting calls; `StrictMock<T>` for protocol-sensitive tests

**Test naming convention:**
- Test suite: `TestSuiteName` in PascalCase matching the class under test (e.g., `OrderServiceTest`)
- Test case: descriptive PascalCase describing behavior (e.g., `CreateOrderReturnsNewDraftOrder`)
- Pattern: `TEST_F(ClassUnderTestTest, MethodUnderTest_Scenario_ExpectedResult)`

**Test pyramid compliance (per [ENG-4.2](laws/engineering/eng-4-testing.md)):**
- Unit tests (`tests/unit/`): majority of tests — fast, isolated, mock external dependencies
- Integration tests (`tests/integration/`): verify cross-component behavior with real dependencies
- Maintain pyramid ratio: unit tests should significantly outnumber integration tests

**Adoption rules:**
- **Greenfield:** GoogleTest + GoogleMock is mandatory from project start
- **Brownfield without test framework:** adopt immediately — no exception path
- **Brownfield with existing framework** (e.g., Catch2, Boost.Test, CppUnit): plan migration to GoogleTest with documented milestones; new tests must use GoogleTest; existing tests may remain until migration completes

### Mutation Testing

**Default tool:** [Mull](https://github.com/mull-project/mull) — an LLVM-based mutation testing tool for C/C++.

> **Cross-reference:** The parallel [mutation-testing-governance](hangar-ai-specs/changes/mutation-testing-governance/PROPOSAL.md) proposal is creating [ENG-4.11](laws/engineering/eng-4-testing.md) as a new governance law. Until [ENG-4.11](laws/engineering/eng-4-testing.md) is ratified, Mull adoption follows this section as the interim C++ standard.

**LLVM/Clang prerequisite:**
- Mull requires the **LLVM/Clang toolchain** (Clang 15+ / LLVM 15+ minimum)
- Projects using GCC-only or MSVC-only toolchains must add a Clang build configuration specifically for mutation testing, or document the constraint as a brownfield exception
- Mull operates on LLVM bitcode — the test binary must be compiled with Clang and `-fembed-bitcode` or Mull's compiler wrapper

**Mutation score thresholds (per [ENG-4.11](laws/engineering/eng-4-testing.md)):**
- ≥70% mutation score for general application code
- ≥85% mutation score for critical paths (crew-scheduling, dispatch, maintenance compliance)
- Performance SLA: mutation testing runs must complete in <5 minutes per 1000 LOC

**Greenfield adoption:**
- Enable Mull in CI as a recommended gate when the LLVM/Clang toolchain is available
- Add `mull-runner` invocation to the test pipeline after unit tests pass
- Configure mutation operators in `.mull.yml` at the project root

**Brownfield exception path (phased adoption):**
- If a repository cannot practically support Mull yet (e.g., no LLVM/Clang available, legacy build system incompatibility), document the constraint in the repository's `AGENTS.md` or `README.md`
- Treat mutation testing as a **phased adoption item** — it must not block initial avatar adoption
- Phase 1: add Clang build config alongside existing compiler; Phase 2: enable Mull on new modules; Phase 3: expand to legacy modules as modernization proceeds
- Each phase must have documented milestones and a target completion timeline

**Mull CLI usage:**

```bash
# Build test binary with Clang for Mull
clang++ -fembed-bitcode -std=c++20 -o build/tests/unit/order_test tests/unit/order_test.cpp

# Run mutation testing
mull-runner ./build/tests/unit/order_test

# Run with configuration file
mull-runner --config .mull.yml ./build/tests/unit/order_test
```

---


## GoogleTest Core Macro Reference

> Per [ENG-4.1](laws/engineering/eng-4-testing.md) (Atomic TDD Law): every
> assertion must drive a single failing test before any production code is
> written. Patterns below are sourced from `facebook/folly/tree/main/folly/test`.

### TEST() vs TEST_F()

Use **`TEST(SuiteName, BehaviorUnderTest)`** for standalone cases with no shared
state — the vast majority of Folly's test files:

```cpp
// CancellationTokenTest.cpp pattern
TEST(CancellationTokenTest, DefaultTokenIsNotCancellable) {
    CancellationToken t;
    EXPECT_FALSE(t.isCancellationRequested());
    EXPECT_FALSE(t.canBeCancelled());
}
```

Use **`TEST_F(FixtureName, BehaviorUnderTest)`** when multiple tests share
`SetUp`/`TearDown` or data members. The fixture class inherits `testing::Test`:

```cpp
// ChronoTest.cpp / DemangleTest.cpp pattern
class FlightDurationTest : public testing::Test {
protected:
    FlightDuration dur_{Minutes{90}};
};

TEST_F(FlightDurationTest, ConvertToSeconds) {
    EXPECT_EQ(dur_.seconds(), 5400);
}
```

### EXPECT_* vs ASSERT_* Decision Table

| Macro Family | Behaviour on Failure | When to Use |
|--------------|---------------------|-------------|
| `EXPECT_EQ`, `EXPECT_TRUE`, `EXPECT_FALSE` | Records failure, continues | Default — most assertions |
| `EXPECT_NE`, `EXPECT_LT`, `EXPECT_GT`, `EXPECT_LE`, `EXPECT_GE` | Records failure, continues | Numeric ordering assertions |
| `EXPECT_THAT(val, matcher)` | Records failure, continues | GMock matchers (HasSubstr, Contains, etc.) |
| `ASSERT_EQ`, `ASSERT_NE`, `ASSERT_TRUE` | Aborts current test function | When continuing would crash or produce nonsense |

**Rule of thumb (Folly convention):** use `EXPECT_*` everywhere; switch to
`ASSERT_*` only when a null pointer dereference or corrupt state would follow.

```cpp
// COMPLIANT — use EXPECT_* by default
EXPECT_EQ(counter.count(), 1);

// COMPLIANT — ASSERT when nullptr dereference would follow
ASSERT_NE(ptr, nullptr);
EXPECT_EQ(ptr->value(), 42);
```

### ADD_FAILURE() — Manual Failure Injection

`ADD_FAILURE()` records a non-fatal failure from inside catch blocks or helper
functions where assertion macros cannot reach the test body directly.
Folly's `ConvTest.cpp` uses it in a `catch(...)` block:

```cpp
try {
    auto result = to<float>(std::numeric_limits<double>::min());
    EXPECT_TRUE(result == std::numeric_limits<float>::min() || result == 0.f);
} catch (...) {
    ADD_FAILURE();   // unexpected exception — flag it without aborting
}
```

### Compile-Time Contracts with static_assert

Folly's `ChronoTest.cpp` places `static_assert` at file scope before any test
to validate trait invariants at compile time rather than runtime:

```cpp
// Verify clock abstraction contract — fails at compile time if broken
static_assert(
    std::is_same_v<clock_traits<steady_clock>::spec,
                   clock_traits<coarse_steady_clock>::spec>);
```

---

---

## GTest Exception Testing

> Per [ENG-4.1](laws/engineering/eng-4-testing.md): exception paths are
> first-class behaviors — each deserves its own test cycle. Patterns below
> are sourced from Folly's `ConvTest.cpp` and `ConstructorCallbackListTest.cpp`.

### The Three Exception Macros

| Macro | Passes When | Use Case |
|-------|------------|----------|
| `EXPECT_THROW(expr, ExcType)` | `expr` throws exactly `ExcType` | Known exception type expected |
| `EXPECT_ANY_THROW(expr)` | `expr` throws anything | Testing that an invalid call throws |
| `EXPECT_NO_THROW(expr)` | `expr` does not throw | Happy-path safety check |

```cpp
// ConvTest.cpp — testing type conversion overflow throws
EXPECT_ANY_THROW(to<float>(std::numeric_limits<double>::max()));

// ConstructorCallbackListTest.cpp — overflow boundary throws std::length_error
EXPECT_THROW(
    folly::ConstructorCallbackList<Object>::addCallback(callbackF),
    std::length_error);

// Happy path must not throw
EXPECT_NO_THROW(to<int>(42));
```

### Testing the CALPException Hierarchy (IOC_ALP Migration Context)

IOC_ALP's `std::exception → CALPException → CHostException → 15+ types`
exception hierarchy maps directly to `EXPECT_THROW` patterns. Use the most
specific type in the hierarchy for precise contract testing:

```cpp
// NON-COMPLIANT — catching base only; hides regression if type changes
EXPECT_THROW(service.loadFlight("ZFW-999"), std::exception);

// COMPLIANT — lock to the specific type from the CALPException hierarchy
EXPECT_THROW(service.loadFlight("ZFW-999"), CFlightNotFoundException);

// COMPLIANT — for internal boundary testing where exact type is unknown
EXPECT_ANY_THROW(service.computeCG(corruptWeight));
```

### Exception Testing in Try/Catch vs EXPECT_THROW

Prefer `EXPECT_THROW` over manual `try/catch` — it produces a clearer failure
message and does not require `FAIL()` / `ADD_FAILURE()` boilerplate:

```cpp
// NON-COMPLIANT — verbose and error-prone
try {
    service.loadFlight("ZFW-999");
    FAIL() << "Expected CFlightNotFoundException";
} catch (const CFlightNotFoundException&) { /* pass */ }

// COMPLIANT — one line, clear failure message
EXPECT_THROW(service.loadFlight("ZFW-999"), CFlightNotFoundException);
```

---

---


---

## See Also

- [CI Quality Toolchain Policy](ref-testing-ci-policy.md)
- [GoogleTest Advanced Patterns](ref-testing-gtest-advanced.md)
