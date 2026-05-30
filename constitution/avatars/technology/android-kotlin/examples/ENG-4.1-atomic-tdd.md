---
law_id: ENG-4.1
avatar: android-kotlin
non_negotiable: true
authority: Jeroen Mols (jeroenmols.com) + Philipp Hauer (phauer.com / KotlinConf 2018)
---

# ENG-4.1 — Atomic TDD (Android Kotlin)

> One failing test → pass → refactor. Backtick names. `@TestInstance(PER_CLASS)`. Turbine for Flow.

## COMPLIANT

```kotlin
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class PlaceOrderUseCaseTest {
    private val repository = mockk<OrderRepository>()
    private val sut = PlaceOrderUseCase(repository)

    @BeforeEach fun setUp() = clearMocks(repository)

    @Test
    fun `places order and emits audit event`() = runTest {
        val order = Order.stub(status = OrderStatus.DRAFT)
        coEvery { repository.getOrder(order.id) } returns order
        coEvery { repository.save(any()) } just runs

        val result = sut(order.id)

        assertTrue(result.isSuccess)
        coVerify(exactly = 1) { repository.save(match { it.status == OrderStatus.PLACED }) }
    }
}
```

## COMPLIANT — Flow with Turbine

```kotlin
@Test
fun `loading orders emits Loading then Success`() = runTest {
    coEvery { repository.getOrders() } returns listOf(Order.stub())

    viewModel.uiState.test {
        assertEquals(OrderListUiState.Loading, awaitItem())
        assertIs<OrderListUiState.Success>(awaitItem())
        cancelAndConsumeRemainingEvents()
    }
}
```

## VIOLATION

```kotlin
// ❌ Multiple concerns in one test — not atomic
@Test
fun testBooking() {
    viewModel.search("DFW", "LHR")
    viewModel.selectFlight(flightId)
    viewModel.confirmBooking()
    assertEquals("confirmed", viewModel.status)  // tests 3 state transitions at once
}
```

> Full detail with MockK slot capturing, spy patterns, @Nested contexts: see `ENG-4.1-atomic-tdd-detail.md`.
