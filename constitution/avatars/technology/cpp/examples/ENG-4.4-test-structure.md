---
law_id: ENG-4.4
cpp_version_min: 17
cpp_version_note: >-
  Uses C++17 structured bindings (auto [x,y]=). Transitional teams: use std::tie or explicit member access in test assertions.
avatar: cpp
---

# [ENG-4.4](laws/engineering/eng-4-testing.md): Test Structure — C++ Examples

## COMPLIANT: Arrange-Act-Assert with Clear Sections

```cpp
TEST_F(BookingServiceTest, ConfirmBookingSendsNotification) {
    // Arrange
    auto booking = Booking::create(PassengerId{"pax-001"}, FlightId{"AA100"});
    EXPECT_CALL(repository_, find(booking.id())).WillOnce(Return(booking));
    EXPECT_CALL(repository_, save(_)).Times(1);
    EXPECT_CALL(notifier_, send(_, _)).Times(1);

    // Act
    service_.confirm(booking.id());

    // Assert — implicit via EXPECT_CALL verification
}
```

**Why compliant:** Clear Arrange-Act-Assert separation. One behavior tested. Mock expectations set before action.

## NON-COMPLIANT: No Structure

```cpp
TEST(Misc, Test1) {
    auto b = Booking::create(PassengerId{"p"}, FlightId{"f"});
    b.confirm(); b.cancel(); b.confirm();  // Multiple actions
    EXPECT_TRUE(b.is_confirmed());  // What exactly are we testing?
    auto b2 = Booking::create(PassengerId{"q"}, FlightId{"g"});
    EXPECT_NE(b.id(), b2.id());  // Unrelated assertion in same test
}
```

**Why non-compliant:** No structure. Multiple actions and unrelated assertions. Unclear what behavior is under test.

## COMPLIANT: Parameterized Test for Data-Driven Validation

```cpp
struct FareCase { int base; double tax_rate; int expected; };

class FareCalculationTest : public ::testing::TestWithParam<FareCase> {};

TEST_P(FareCalculationTest, AppliesTaxCorrectly) {
    auto [base, rate, expected] = GetParam();
    EXPECT_EQ(calculate_fare(Money::of(base), rate), Money::of(expected));
}

INSTANTIATE_TEST_SUITE_P(FareCases, FareCalculationTest, ::testing::Values(
    FareCase{100, 0.10, 110},
    FareCase{200, 0.15, 230},
    FareCase{0,   0.10, 0}
));
```

**The Rule:** Each test method tests one behavior. Use Arrange-Act-Assert structure with visible comment separators. Use parameterized tests (`TestWithParam`) for data-driven scenarios — each parameter set runs as a separate test case. Use `EXPECT_*` (non-fatal) for most checks; `ASSERT_*` only when continuation is meaningless.

## When to Use `TestWithParam` vs `TEST_F`

| Use | When |
|-----|------|
| `TEST_F` (fixture) | Behavior under test has **setup/teardown** needs (mocks, DB connections, file handles). One logical behavior per test. |
| `TestWithParam` | Same logic, **different data inputs**. E.g., tax rates across fare classes, validation rules across input formats. Each parameter set becomes its own test case in output. |
| `TEST` (plain) | Stateless, simple, no fixture needed. Prefer for pure-function unit tests. |

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| `INSTANTIATE_TEST_SUITE_P` with 500+ cases | CI dashboards become unreadable; total test time balloons | Keep parameterized sets to ~20 representative cases; use a nightly fuzzing target for exhaustive coverage |
| Default GTest parameterized test names (`/0`, `/1`) | CI failure output is unreadable; no indication which case broke | Use a custom `PrintToStringParamName` functor to get readable names like `FareCases/base100_tax10` |
| `SCOPED_TRACE` in a deeply nested loop body | Each iteration adds another trace frame; output contains hundreds of frames with no useful signal | Use `SCOPED_TRACE` at the outer loop level only; for inner loops, use `EXPECT_EQ` with a message parameter containing the iteration index |
