---
law_id: ENG-4.2
cpp_version_min: 98
avatar: cpp
---

# [ENG-4.2](laws/engineering/eng-4-testing.md): Test Pyramid — C++ Examples

**The Rule:** Tests must follow the pyramid distribution: **~70% unit / ~20% integration / ~10% E2E**. Unit tests mock external dependencies and run in milliseconds. Integration tests use real components (database, HTTP) and run in seconds. E2E tests exercise the full deployed system.

**Why this matters in C++:** C++ build times are slow. A test suite dominated by integration tests creates a 10+ minute feedback loop that breaks the TDD cycle. Unit tests with mocked dependencies compile and run in seconds.

## COMPLIANT: Proper Pyramid Distribution

```cpp
// tests/unit/flight_pricing_test.cpp — Fast, isolated (majority of tests)
TEST_F(FlightPricingTest, BaseFareAppliesForEconomy) { /* mock GDS */ }
TEST_F(FlightPricingTest, LoyaltyDiscountReducesTotal) { /* mock DB */ }
TEST_F(FlightPricingTest, SurchargeAppliesOnPeakDates) { /* mock calendar */ }
// ... 50+ unit tests — each runs in <10ms

// tests/integration/pricing_api_test.cpp — Real GDS sandbox (fewer tests)
TEST_F(PricingApiTest, LiveSabreQueryReturnsFares) { /* staging Sabre */ }
TEST_F(PricingApiTest, PricingRoundTripsToDatabase) { /* real PostgreSQL */ }
// ... 8 integration tests — each runs in 1-5s
```

## NON-COMPLIANT: Inverted Pyramid

```cpp
// ❌ No unit tests at all — everything through full stack
// tests/integration/ — all tests require database + external services
TEST_F(FullStackTest, TestCreateBooking) { /* 30-second test, flaky */ }
TEST_F(FullStackTest, TestCancelBooking) { /* 25-second test, flaky */ }
// Slow feedback, brittle, hard to isolate failures
```

**When NOT to over-unit-test:** Pure data containers and trivial getters don't need dedicated unit tests. Focus unit testing on business logic, state machines, and calculations. Integration tests verify that wiring (DI, serialization, database mapping) works correctly.

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Integration test disguised as a unit test via heavy mocking | 15 mocks in one test means you are testing the mock framework, not real behaviour; the test stays green while production breaks | Unit tests should mock at most 1–2 dependencies; if you need more, write an integration test that uses real implementations |
| Test pyramid inversion in a brownfield repo (more E2E than unit) | E2E tests are slow, brittle, and give no isolation; a single API change breaks dozens of tests with no indication of root cause | Introduce unit tests incrementally using the characterization test pattern (see ENG-4.1-characterization-test-pattern.md) before refactoring |
| Manual QA counts towards the integration-test quota | Team reports "integration covered" based on exploratory testing; no automated evidence in CI | Only automated tests count towards the pyramid; manual tests are supplementary and cannot satisfy the pyramid gate |
