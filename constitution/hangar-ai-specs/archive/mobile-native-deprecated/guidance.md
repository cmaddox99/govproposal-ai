# iOS/Android Native Guidance

> **⚠️ iOS-Specific Patterns:** For dedicated iOS Swift guidance — Jon Reid Quality Coding TDD, Keychain security, fastlane CI/CD, Swift 6 `@MainActor`, certificate pinning — use the **`ios-swift` avatar** (`avatars/technology/ios-swift/`).

> **⚠️ Android-Specific Patterns:** For dedicated Android Kotlin guidance — Jeroen Mols TDD, MockK + Turbine, Android Keystore, Hilt, fastlane supply, Jetpack Compose — use the **`android-kotlin` avatar** (`avatars/technology/android-kotlin/`).

> **Purpose:** Cross-platform iOS + Android migration guidance only. Both platforms now have dedicated avatars. This avatar will be deprecated once `android-kotlin` is fully shipped.

---

## Overview

This guidance provides patterns for AI agents working with native mobile applications. It covers testing with XCTest (iOS) and JUnit (Android), architecture patterns like MVVM, and platform-specific idioms.

---

## iOS (Swift) Behaviors

### Testing Framework

**Primary Framework:** XCTest + Quick/Nimble (optional)

#### Test Structure

```swift
import XCTest
@testable import MyApp

final class OrderTests: XCTestCase {

    func test_newOrder_hasZeroTotal() {
        // Arrange
        let customerId = CustomerId("cust-123")

        // Act
        let order = Order.create(customerId: customerId)

        // Assert
        XCTAssertEqual(order.total, .zero)
        XCTAssertEqual(order.status, .draft)
    }

    func test_addItem_updatesTotal() {
        // Arrange
        var order = Order.create(customerId: CustomerId("cust-123"))
        let product = Product(id: "prod-1", price: Money(amount: 100))

        // Act
        order.addItem(product: product, quantity: 2)

        // Assert
        XCTAssertEqual(order.total, Money(amount: 200))
        XCTAssertEqual(order.lines.count, 1)
    }

    func test_addItem_whenNotDraft_throws() {
        // Arrange
        var order = Order.create(customerId: CustomerId("cust-123"))
        order.addItem(product: Product(id: "p1", price: Money(amount: 100)), quantity: 1)
        try? order.place()

        // Act & Assert
        XCTAssertThrowsError(try order.addItem(product: Product(id: "p2", price: Money(amount: 50)), quantity: 1)) { error in
            XCTAssertEqual(error as? OrderError, .notModifiable)
        }
    }
}
```

### Domain Modeling (Swift)

#### Entity Pattern

```swift
struct Order {
    let id: OrderId
    let customerId: CustomerId
    private(set) var lines: [OrderLine]
    private(set) var status: OrderStatus

    var total: Money {
        lines.reduce(.zero) { $0 + $1.total }
    }

    static func create(customerId: CustomerId) -> Order {
        Order(
            id: OrderId(),
            customerId: customerId,
            lines: [],
            status: .draft
        )
    }

    mutating func addItem(product: Product, quantity: Int) throws {
        guard status == .draft else {
            throw OrderError.notModifiable
        }

        if let index = lines.firstIndex(where: { $0.productId == product.id }) {
            lines[index].increaseQuantity(by: quantity)
        } else {
            lines.append(OrderLine(product: product, quantity: quantity))
        }
    }

    mutating func place() throws {
        guard !lines.isEmpty else {
            throw OrderError.empty
        }
        status = .placed
    }
}

enum OrderStatus {
    case draft, placed, shipped, delivered
}

enum OrderError: Error, Equatable {
    case notModifiable
    case empty
}
```

#### Value Object Pattern

```swift
struct Money: Equatable {
    let amount: Decimal
    let currency: String

    static let zero = Money(amount: 0, currency: "USD")

    init(amount: Decimal, currency: String = "USD") {
        precondition(amount >= 0, "Amount cannot be negative")
        self.amount = amount
        self.currency = currency
    }

    static func + (lhs: Money, rhs: Money) -> Money {
        precondition(lhs.currency == rhs.currency, "Currency mismatch")
        return Money(amount: lhs.amount + rhs.amount, currency: lhs.currency)
    }

    static func * (lhs: Money, rhs: Int) -> Money {
        Money(amount: lhs.amount * Decimal(rhs), currency: lhs.currency)
    }
}
```

### MVVM Pattern (iOS SwiftUI)

```swift
// ViewModel
@MainActor
class OrderListViewModel: ObservableObject {
    @Published private(set) var orders: [Order] = []
    @Published private(set) var isLoading = false
    @Published private(set) var error: String?

    private let orderService: OrderService

    init(orderService: OrderService) {
        self.orderService = orderService
    }

    func loadOrders() async {
        isLoading = true
        error = nil

        do {
            orders = try await orderService.getOrders()
        } catch {
            self.error = "Failed to load orders"
        }

        isLoading = false
    }
}

// View
struct OrderListView: View {
    @StateObject private var viewModel: OrderListViewModel

    var body: some View {
        List(viewModel.orders) { order in
            OrderRow(order: order)
        }
        .task {
            await viewModel.loadOrders()
        }
    }
}
```

---

## Android (Kotlin) Behaviors

### Testing Framework

**Primary Framework:** JUnit 5 + MockK + Turbine (for Flow)

#### Test Structure

```kotlin
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertThrows
import kotlin.test.assertEquals

class OrderTest {

    @Test
    fun `new order has zero total`() {
        // Arrange
        val customerId = CustomerId("cust-123")

        // Act
        val order = Order.create(customerId)

        // Assert
        assertEquals(Money.ZERO, order.total)
        assertEquals(OrderStatus.DRAFT, order.status)
    }

    @Test
    fun `add item updates total`() {
        // Arrange
        val order = Order.create(CustomerId("cust-123"))
        val product = Product(ProductId("prod-1"), Money(100))

        // Act
        order.addItem(product, quantity = 2)

        // Assert
        assertEquals(Money(200), order.total)
        assertEquals(1, order.lines.size)
    }

    @Test
    fun `add item when not draft throws exception`() {
        // Arrange
        val order = Order.create(CustomerId("cust-123"))
        order.addItem(Product(ProductId("p1"), Money(100)), 1)
        order.place()

        // Act & Assert
        assertThrows<OrderNotModifiableException> {
            order.addItem(Product(ProductId("p2"), Money(50)), 1)
        }
    }
}
```

#### ViewModel Testing with Turbine

```kotlin
import app.cash.turbine.test
import io.mockk.coEvery
import io.mockk.mockk
import kotlinx.coroutines.test.runTest
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

class OrderListViewModelTest {

    private val orderRepository = mockk<OrderRepository>()
    private val viewModel = OrderListViewModel(orderRepository)

    @Test
    fun `loads orders on init`() = runTest {
        // Arrange
        val orders = listOf(Order.create(CustomerId("cust-1")))
        coEvery { orderRepository.getOrders() } returns orders

        // Act & Assert
        viewModel.uiState.test {
            assertEquals(OrderListUiState.Loading, awaitItem())
            assertEquals(OrderListUiState.Success(orders), awaitItem())
        }
    }

    @Test
    fun `shows error when load fails`() = runTest {
        // Arrange
        coEvery { orderRepository.getOrders() } throws Exception("Network error")

        // Act & Assert
        viewModel.uiState.test {
            assertEquals(OrderListUiState.Loading, awaitItem())
            val error = awaitItem()
            assert(error is OrderListUiState.Error)
        }
    }
}
```

### Domain Modeling (Kotlin)

#### Entity Pattern

```kotlin
class Order private constructor(
    val id: OrderId,
    val customerId: CustomerId,
    private val _lines: MutableList<OrderLine> = mutableListOf(),
    private var _status: OrderStatus = OrderStatus.DRAFT
) {
    val lines: List<OrderLine> get() = _lines.toList()
    val status: OrderStatus get() = _status

    val total: Money
        get() = _lines.fold(Money.ZERO) { acc, line -> acc + line.total }

    fun addItem(product: Product, quantity: Int) {
        ensureModifiable()

        val existingLine = _lines.find { it.productId == product.id }
        if (existingLine != null) {
            existingLine.increaseQuantity(quantity)
        } else {
            _lines.add(OrderLine(product.id, product.price, quantity))
        }
    }

    fun place() {
        require(_lines.isNotEmpty()) { "Cannot place empty order" }
        _status = OrderStatus.PLACED
    }

    private fun ensureModifiable() {
        if (_status != OrderStatus.DRAFT) {
            throw OrderNotModifiableException(id, _status)
        }
    }

    companion object {
        fun create(customerId: CustomerId): Order {
            return Order(
                id = OrderId.generate(),
                customerId = customerId
            )
        }
    }
}

enum class OrderStatus {
    DRAFT, PLACED, SHIPPED, DELIVERED
}
```

#### Value Object Pattern

```kotlin
@JvmInline
value class Money(val amount: Int) {
    init {
        require(amount >= 0) { "Amount cannot be negative" }
    }

    operator fun plus(other: Money): Money = Money(amount + other.amount)
    operator fun times(quantity: Int): Money = Money(amount * quantity)

    companion object {
        val ZERO = Money(0)
    }
}

@JvmInline
value class OrderId(val value: String) {
    companion object {
        fun generate(): OrderId = OrderId(UUID.randomUUID().toString())
    }
}

@JvmInline
value class CustomerId(val value: String)
```

### MVVM Pattern (Android Compose)

```kotlin
// ViewModel
@HiltViewModel
class OrderListViewModel @Inject constructor(
    private val orderRepository: OrderRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<OrderListUiState>(OrderListUiState.Loading)
    val uiState: StateFlow<OrderListUiState> = _uiState.asStateFlow()

    init {
        loadOrders()
    }

    fun loadOrders() {
        viewModelScope.launch {
            _uiState.value = OrderListUiState.Loading
            try {
                val orders = orderRepository.getOrders()
                _uiState.value = OrderListUiState.Success(orders)
            } catch (e: Exception) {
                _uiState.value = OrderListUiState.Error("Failed to load orders")
            }
        }
    }
}

// Composable
@Composable
fun OrderListScreen(viewModel: OrderListViewModel = hiltViewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    when (val state = uiState) {
        is OrderListUiState.Loading -> LoadingIndicator()
        is OrderListUiState.Success -> OrderList(orders = state.orders)
        is OrderListUiState.Error -> ErrorMessage(message = state.message)
    }
}
```

---

## Repository Pattern

### iOS

```swift
protocol OrderRepository {
    func getOrders() async throws -> [Order]
    func getOrder(id: OrderId) async throws -> Order?
    func save(_ order: Order) async throws
}

class APIOrderRepository: OrderRepository {
    private let apiClient: APIClient

    init(apiClient: APIClient) {
        self.apiClient = apiClient
    }

    func getOrders() async throws -> [Order] {
        let dtos: [OrderDTO] = try await apiClient.get("/orders")
        return dtos.map { $0.toDomain() }
    }
}
```

### Android

```kotlin
interface OrderRepository {
    suspend fun getOrders(): List<Order>
    suspend fun getOrder(id: OrderId): Order?
    suspend fun save(order: Order)
}

class OrderRepositoryImpl @Inject constructor(
    private val orderApi: OrderApi,
    private val orderDao: OrderDao
) : OrderRepository {

    override suspend fun getOrders(): List<Order> {
        return try {
            val dtos = orderApi.getOrders()
            dtos.map { it.toDomain() }
        } catch (e: Exception) {
            orderDao.getAll().map { it.toDomain() }
        }
    }
}
```

---

## Tools and Commands

### iOS

```bash
# Run tests
xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15'

# Build
xcodebuild build -scheme MyApp

# Run specific test
xcodebuild test -scheme MyApp -only-testing:MyAppTests/OrderTests

# Coverage
xcodebuild test -scheme MyApp -enableCodeCoverage YES
```

### Android

```bash
# Run unit tests
./gradlew test

# Run specific test class
./gradlew test --tests "com.example.myapp.domain.OrderTest"

# Run instrumented tests
./gradlew connectedAndroidTest

# Build
./gradlew assembleDebug

# Lint
./gradlew lint
```

---

## Platform-Specific Guidance

### iOS Accessibility

```swift
Button("Checkout") {
    checkout()
}
.accessibilityLabel("Checkout")
.accessibilityHint("Proceeds to payment")

Text(order.total.formatted())
    .accessibilityLabel("Order total: \(order.total.formatted())")
```

### Android Accessibility

```kotlin
Button(
    onClick = { onCheckout() },
    modifier = Modifier.semantics {
        contentDescription = "Checkout"
    }
) {
    Text("Checkout")
}

Text(
    text = order.total.format(),
    modifier = Modifier.semantics {
        contentDescription = "Order total: ${order.total.format()}"
    }
)
```
