---
law_id: ENG-4.1
cpp_version_min: 98
avatar: cpp
---

# [ENG-4.1](laws/engineering/eng-4-testing.md): Atomic TDD — C++ Examples

## COMPLIANT: Single Test with Arrange-Act-Assert

```cpp
#include <gtest/gtest.h>
#include "flight_plan_service.h"
#include "mock_flight_repository.h"

class FlightPlanServiceTest : public ::testing::Test {
protected:
    MockFlightRepository repository_;
    FlightPlanService service_{repository_};
};

TEST_F(FlightPlanServiceTest, CreateFlightPlanReturnsDraftStatus) {
    // Arrange
    auto flight_id = FlightId{"AA100"};

    // Act
    auto plan = service_.createFlightPlan(flight_id);

    // Assert
    EXPECT_EQ(plan.status(), FlightPlanStatus::kDraft);
    EXPECT_EQ(plan.flightId(), flight_id);
}
```

**Why compliant:** One test method per TDD cycle. Follows RED→GREEN→REFACTOR. Clear Arrange-Act-Assert structure. Tests one behavior.

## NON-COMPLIANT: Multiple Behaviors in One Test

```cpp
TEST_F(FlightPlanServiceTest, FlightPlanOperations) {
    auto plan = service_.createFlightPlan(FlightId{"AA100"});
    EXPECT_EQ(plan.status(), FlightPlanStatus::kDraft);

    plan.addWaypoint(Waypoint{"DFW", AltitudeFt{35000}});
    EXPECT_EQ(plan.waypointCount(), 1);

    plan.submit();
    EXPECT_EQ(plan.status(), FlightPlanStatus::kSubmitted);
}
```

**Why non-compliant:** Tests creation, waypoint addition, and submission in one method. Violates one-test-per-cycle rule. A failure gives ambiguous signal about which behavior broke.

## TDD Cycle Commands

```bash
# RED — Write ONE failing test, then:
cmake --build build --target flight_plan_service_test && ctest -R FlightPlanServiceTest --output-on-failure
# Expected: FAILED (1 failure)

# GREEN — Write MINIMUM code to pass:
cmake --build build --target flight_plan_service_test && ctest -R FlightPlanServiceTest --output-on-failure
# Expected: PASSED

# REFACTOR — Improve code, re-run to confirm:
cmake --build build && ctest --test-dir build --output-on-failure
# Expected: ALL PASSED (full suite)
```

**The Rule:** One test per TDD cycle. Write the test first (RED). Write the minimum code to pass (GREEN). Refactor without changing behavior. Run the full suite before committing. Never batch multiple tests into one commit.

## Why TDD Is Harder in C++ (and How to Fix It)

C++ compile times make the RED→GREEN feedback loop painful. A full rebuild after a one-line change can take minutes, tempting developers to skip the RED step.

**Practical tips to keep the cycle fast:**
- **`ccache`/`sccache`** — cache compiled objects; only changed TUs recompile. `cmake -DCMAKE_CXX_COMPILER_LAUNCHER=ccache ..`
- **Build only your test target** — `cmake --build build --target flight_plan_service_test` during RED/GREEN; full suite only at VERIFY.
- **Forward-declare aggressively** — reduces header coupling and rebuild times.

## Edge Cases & Warnings

- **Skipping the RED step** — Writing production code before a failing test exists is the most common ENG-4.1 violation. Per ENG-4.1, this is a constitutional violation regardless of whether the final tests pass.
- **Batching multiple tests into one commit** — Running RED-GREEN-REFACTOR for 3 behaviors then committing all at once violates atomicity. Each behavior gets its own commit; the commit hash is the traceability anchor.
