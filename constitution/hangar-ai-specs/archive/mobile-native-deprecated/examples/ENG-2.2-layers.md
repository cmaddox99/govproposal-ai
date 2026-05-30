---
law_id: ENG-2.2
avatar: mobile-native
---

# ENG-2.2: Layered Architecture Examples for iOS/Android Native

## COMPLIANT: Clean Layer Separation

### iOS (Swift)

```swift
// === DOMAIN LAYER (innermost - no dependencies) ===

// Domain/Entities/Order.swift
struct Order: Equatable {
    let id: UUID
    let items: [LineItem]
    let status: OrderStatus
}

// Domain/Repositories/OrderRepository.swift (Protocol only)
protocol OrderRepository {
    func save(_ order: Order) async throws
    func findById(_ id: UUID) async throws -> Order?
}

// Domain/Services/OrderService.swift
struct OrderService {
    private let repository: OrderRepository

    init(repository: OrderRepository) {
        self.repository = repository
    }

    func submitOrder(_ order: Order) async throws -> Order {
        let submittedOrder = order.withStatus(.submitted)
        try await repository.save(submittedOrder)
        return submittedOrder
    }
}


// === APPLICATION LAYER ===

// Application/UseCases/SubmitOrderUseCase.swift
struct SubmitOrderUseCase {
    private let orderService: OrderService
    private let notificationService: NotificationService

    func execute(_ order: Order) async throws -> Order {
        let submitted = try await orderService.submitOrder(order)
        await notificationService.notify(.orderSubmitted(submitted))
        return submitted
    }
}


// === INFRASTRUCTURE LAYER (outermost) ===

// Infrastructure/Repositories/CoreDataOrderRepository.swift
final class CoreDataOrderRepository: OrderRepository {
    private let context: NSManagedObjectContext

    func save(_ order: Order) async throws {
        // Converts domain Order to CoreData entity
        let entity = OrderEntity(context: context)
        entity.id = order.id
        entity.status = order.status.rawValue
        try context.save()
    }

    func findById(_ id: UUID) async throws -> Order? {
        // Converts CoreData entity back to domain Order
        let request = OrderEntity.fetchRequest()
        request.predicate = NSPredicate(format: "id == %@", id as CVarArg)
        guard let entity = try context.fetch(request).first else { return nil }
        return entity.toDomain()
    }
}


// === PRESENTATION LAYER ===

// Presentation/ViewModels/OrderViewModel.swift
@MainActor
final class OrderViewModel: ObservableObject {
    @Published private(set) var order: Order?
    @Published private(set) var isSubmitting = false

    private let submitOrderUseCase: SubmitOrderUseCase

    func submit() async {
        guard let order = order else { return }
        isSubmitting = true
        defer { isSubmitting = false }

        do {
            self.order = try await submitOrderUseCase.execute(order)
        } catch {
            // Handle error
        }
    }
}
```

### Android (Kotlin)

```kotlin
// === DOMAIN LAYER (innermost - no dependencies) ===

// domain/model/Order.kt
data class Order(
    val id: UUID,
    val items: List<LineItem>,
    val status: OrderStatus
)

// domain/repository/OrderRepository.kt (Interface only)
interface OrderRepository {
    suspend fun save(order: Order)
    suspend fun findById(id: UUID): Order?
}

// domain/service/OrderService.kt
class OrderService(private val repository: OrderRepository) {
    suspend fun submitOrder(order: Order): Order {
        val submittedOrder = order.withStatus(OrderStatus.SUBMITTED)
        repository.save(submittedOrder)
        return submittedOrder
    }
}


// === DATA LAYER (infrastructure) ===

// data/repository/RoomOrderRepository.kt
class RoomOrderRepository(
    private val orderDao: OrderDao
) : OrderRepository {

    override suspend fun save(order: Order) {
        orderDao.insert(order.toEntity())
    }

    override suspend fun findById(id: UUID): Order? {
        return orderDao.findById(id.toString())?.toDomain()
    }
}


// === PRESENTATION LAYER ===

// presentation/order/OrderViewModel.kt
@HiltViewModel
class OrderViewModel @Inject constructor(
    private val submitOrderUseCase: SubmitOrderUseCase
) : ViewModel() {

    private val _order = MutableStateFlow<Order?>(null)
    val order: StateFlow<Order?> = _order.asStateFlow()

    private val _isSubmitting = MutableStateFlow(false)
    val isSubmitting: StateFlow<Boolean> = _isSubmitting.asStateFlow()

    fun submit() {
        val currentOrder = _order.value ?: return

        viewModelScope.launch {
            _isSubmitting.value = true
            submitOrderUseCase.execute(currentOrder)
                .onSuccess { _order.value = it }
            _isSubmitting.value = false
        }
    }
}
```

**Why compliant:** Domain layer has no external dependencies, dependencies point inward, each layer has clear responsibility, infrastructure concerns are isolated.

---

## VIOLATION: Mixed Layers and Leaky Abstractions

```swift
// BAD: Domain model with infrastructure concerns
struct Order {
    let id: UUID
    var items: [LineItem]

    // VIOLATION: Domain depends on infrastructure (CoreData)
    @NSManaged var managedItems: NSSet

    // VIOLATION: Business logic mixed with persistence
    func save(to context: NSManagedObjectContext) throws {
        let entity = OrderEntity(context: context)
        entity.id = id
        try context.save()
    }

    // VIOLATION: UI concern in domain
    var displayTotal: String {
        "$\(total.amount)"
    }
}

// BAD: ViewModel doing everything
class OrderViewModel: ObservableObject {
    @Published var items: [LineItem] = []

    // VIOLATION: Direct database access in presentation layer
    private let context = PersistenceController.shared.container.viewContext

    func addItem(_ name: String, price: Double) {
        // VIOLATION: Business logic in ViewModel
        let item = LineItem(name: name, price: Money(amount: Decimal(price)))
        items.append(item)

        // VIOLATION: Direct network call from ViewModel
        URLSession.shared.dataTask(with: analyticsURL) { _, _, _ in }

        // VIOLATION: Direct CoreData access
        let entity = LineItemEntity(context: context)
        entity.name = name
        entity.price = price
        try? context.save()
    }

    // VIOLATION: SQL in presentation layer
    func search(query: String) -> [Order] {
        let sql = "SELECT * FROM orders WHERE name LIKE '%\(query)%'"
        // Direct database query...
    }
}
```

```kotlin
// BAD: Activity doing everything
class OrderActivity : AppCompatActivity() {
    // VIOLATION: Direct database instance in UI
    private val database = Room.databaseBuilder(
        applicationContext,
        AppDatabase::class.java,
        "orders"
    ).build()

    // VIOLATION: Business logic in Activity
    private fun calculateDiscount(items: List<LineItem>): Money {
        val total = items.sumOf { it.price.cents }
        return when {
            total > 10000 -> Money(total / 10)  // 10% off
            total > 5000 -> Money(total / 20)   // 5% off
            else -> Money.ZERO
        }
    }

    // VIOLATION: Network call in Activity
    private fun submitOrder() {
        lifecycleScope.launch {
            val response = Retrofit.Builder()
                .baseUrl("https://api.example.com")
                .build()
                .create(OrderApi::class.java)
                .submit(currentOrder)

            // VIOLATION: Direct database write after network
            database.orderDao().insert(response.toEntity())
        }
    }
}
```

**Why violates ENG-2.2:**
- Domain models depend on infrastructure (CoreData, Room)
- Presentation layer bypasses domain and accesses data directly
- Business logic scattered across layers
- SQL/database concerns leak into UI components
- No clear boundaries between layers
- Testing requires real database and network
