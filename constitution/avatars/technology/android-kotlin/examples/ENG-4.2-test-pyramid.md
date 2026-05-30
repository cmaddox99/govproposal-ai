---
law_id: ENG-4.2
avatar: android-kotlin
authority: Jeroen Mols / jeroenmols.com
---

# ENG-4.2: Test Pyramid Examples for Android (Kotlin)

> **Law:** Test suites SHALL maintain proper distribution — Unit ≥70%, Integration ~20%, E2E ≤10%.
> **Principle (Jeroen Mols):** "Everything can be tested." DI dissolves Android coupling — push all business logic to fast JVM unit tests.

---

## Verdict: Android Test Pyramid

```
                    /\
                   /  \
                  / UI \           Compose Testing + Espresso — ≤10%
                 / Tests\          Instrumented, revenue-critical happy paths ONLY
                /────────\
               /Integration\       Robolectric + Hilt — ~20%
              /   Tests     \      Real Room DAOs, DI wiring, ViewModels
             /────────────────\
            /   Unit Tests     \   JUnit 5 + MockK + Turbine — ≥70%
           /   (JVM, Fast)     \   Domain, UseCases, ViewModels, Repositories
          /──────────────────────\
```

| Layer | Framework | Target % | Speed |
|-------|-----------|----------|-------|
| **Unit** | JUnit 5 + MockK + Turbine | **≥70%** | <10s JVM |
| **Integration** | Robolectric + Hilt | **~20%** | <45s |
| **UI (E2E)** | Compose Testing + Espresso | **≤10%** | 2–5 min (device) |

**Decision rules:**
1. Default to JVM unit. If testable via MockK at ViewModel/UseCase layer → unit test.
2. Integration = real Room DAO, real Hilt graph, Robolectric for Android APIs. No emulator.
3. Espresso/Compose UI only for end-to-end revenue flows. Max ≤10 scenarios.
4. Turbine for Flow assertions — runs at unit-test speed, no coroutine hacks needed.

---

## COMPLIANT: Unit Test — ViewModel with Turbine

```kotlin
// src/test/kotlin/com/aa/mobile/OrderViewModelTest.kt
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class OrderViewModelTest {
    private val repository = mockk<OrderRepository>()
    private val sut = OrderViewModel(repository)

    @Test
    fun `loading orders emits success state`() = runTest {
        val orders = listOf(Order.stub())
        coEvery { repository.getOrders() } returns orders

        sut.uiState.test {
            assertEquals(OrderUiState.Loading, awaitItem())
            assertEquals(OrderUiState.Success(orders), awaitItem())
            cancelAndConsumeRemainingEvents()
        }
    }
}
```

---

## VIOLATION: Inverted Pyramid (AA codebase pattern to avoid)

```
// ❌ BAD — mirrors AA's BookingViewModel (2,106 LOC, god class)
// 60% instrumented Espresso tests → 45-min CI, flaky on API version changes
AppUnitTests:          30 tests  (10%)   ~5s
AppIntegrationTests:   90 tests  (30%)  ~60s
AppInstrumentedTests: 180 tests  (60%)  ~50min  ← BLOCKS DEVELOPERS
```

Fix: extract logic from BookingViewModel into pure Kotlin UseCases testable with JUnit 5 + MockK.

---

## Commands: Verify Pyramid Health

```bash
# JVM unit tests — must be ≥70% of total
./gradlew test

# Robolectric integration tests
./gradlew testDebugUnitTest --tests '*.integration.*'

# Instrumented (device required — run in CI with Gradle Managed Devices)
./gradlew pixel6api34DebugAndroidTest
```
