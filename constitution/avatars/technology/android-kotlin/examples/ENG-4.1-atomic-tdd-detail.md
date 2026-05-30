---
law_id: ENG-4.1
avatar: android-kotlin
non_negotiable: true
authority: Jeroen Mols (jeroenmols.com) + Philipp Hauer (phauer.com / KotlinConf 2018)
---

# ENG-4.1: Atomic TDD Examples for Android (Kotlin)

> **Law:** Every code change MUST follow RED → GREEN → REFACTOR. One test at a time. No production code without a failing test first.

---

## AA Codebase Context

JUnit 4 is dominant (416 files use `import org.junit.Test`; JUnit 5 not yet adopted). Both backtick and underscore test naming patterns are present. New code SHOULD use backtick names per Philipp Hauer for readability.

---

## COMPLIANT: Full RED → GREEN → REFACTOR Cycle (JUnit 4)

### Step 1 — RED: Write ONE failing test

```kotlin
// OrderTest.kt
import org.junit.Test
import kotlin.test.assertEquals

class OrderTest {

    @Test
    fun `new order has zero total`() {
        val order = Order.create(CustomerId("cust-1"))
        assertEquals(Money.ZERO, order.total)
    }
}
// Run: ./gradlew :core:domain:testDebugUnitTest --tests '*.OrderTest.new order has zero total'
// Required output: BUILD FAILED — test fails ✗
```

### Step 2 — GREEN: Write minimum code to pass

```kotlin
// Order.kt
data class Order(
    val id: OrderId,
    val customerId: CustomerId,
    val lines: List<OrderLine> = emptyList(),
    val status: OrderStatus = OrderStatus.DRAFT
) {
    val total: Money get() = Money.ZERO  // minimum to pass

    companion object {
        fun create(customerId: CustomerId) = Order(
            id = OrderId.generate(),
            customerId = customerId
        )
    }
}
// Run same test → BUILD SUCCESSFUL — test passes ✓
```

### Step 3 — REFACTOR: Drive real behaviour with next test

```kotlin
@Test
fun `adding item updates total`() {
    val order = Order.create(CustomerId("cust-1"))
    val product = Product(ProductId("p1"), Money(250))

    val updated = order.addItem(product, quantity = 2)

    assertEquals(Money(500), updated.total)
}

// Refactor Order.total to support items:
val total: Money get() = lines.fold(Money.ZERO) { acc, line -> acc + line.total }

// Run full suite → all tests PASSED ✓
```

---

## COMPLIANT: ViewModel TDD with MockK + Turbine (JUnit 4)

```kotlin
import app.cash.turbine.test
import io.mockk.clearMocks
import io.mockk.coEvery
import io.mockk.mockk
import kotlinx.coroutines.test.runTest
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import kotlin.test.assertEquals
import kotlin.test.assertIs

class OrderListViewModelTest {

    @get:Rule
    val coroutineRule = TestCoroutineRule()  // JUnit 4 @Rule for coroutines

    private val repository = mockk<OrderRepository>()
    private lateinit var sut: OrderListViewModel

    @Before
    fun setUp() {
        clearMocks(repository)
        sut = OrderListViewModel(repository)
    }

    @Test
    fun `loading orders emits loading then success`() = runTest {
        val orders = listOf(Order.create(CustomerId("cust-1")))
        coEvery { repository.getOrders() } returns orders

        sut.uiState.test {
            assertEquals(OrderListUiState.Loading, awaitItem())
            assertEquals(OrderListUiState.Success(orders), awaitItem())
            cancelAndConsumeRemainingEvents()
        }
    }

    @Test
    fun `loading orders emits error on repository failure`() = runTest {
        coEvery { repository.getOrders() } throws IOException("timeout")

        sut.uiState.test {
            skipItems(1)  // Loading
            assertIs<OrderListUiState.Error>(awaitItem())
            cancelAndConsumeRemainingEvents()
        }
    }
}
```

---

## VIOLATION: Multiple Behaviours in One Test

```kotlin
// BAD: multiple assertions, multiple behaviours — one failure hides others
@Test
fun testOrderFlow() {
    val order = Order.create(CustomerId("c1"))
    // VIOLATION: three unrelated assertions in one test
    assertEquals(Money.ZERO, order.total)
    assertEquals(OrderStatus.DRAFT, order.status)
    assertEquals(0, order.lines.size)
}

// BAD: Java-style test name — failure message is cryptic
@Test
fun testAddItemUpdatesTotal() { ... }  // ❌ use backtick: `adding item updates total`
```

**Why ENG-4.1 violated:** Multiple assertions per test obscure the failure cause. Production code before a failing test skips RED. Java-style names produce unhelpful failure messages.

---

## TDD Commands

```bash
# RED: run specific test, confirm it fails
./gradlew :core:domain:testDebugUnitTest --tests '*.OrderTest.new order has zero total'

# GREEN: implement minimum, run same test
./gradlew :core:domain:testDebugUnitTest --tests '*.OrderTest.new order has zero total'

# REFACTOR: run all domain tests
./gradlew :core:domain:testDebugUnitTest

# VERIFY: full suite
./gradlew testDebugUnitTest -Papp.isJenkins=true
aa-constitution-lint .
```
