---
law_id: ENG-3.2
avatar: mobile-native
---

# ENG-3.2: Immutability Examples for iOS/Android Native

## COMPLIANT: Immutable Domain Models

### iOS (Swift)

```swift
// Immutable value objects using Swift structs

struct Money: Equatable, Hashable {
    let amount: Decimal
    let currency: Currency

    static let zero = Money(amount: 0, currency: .usd)

    func add(_ other: Money) -> Money {
        guard currency == other.currency else {
            fatalError("Cannot add different currencies")
        }
        return Money(amount: amount + other.amount, currency: currency)
    }

    static func + (lhs: Money, rhs: Money) -> Money {
        lhs.add(rhs)
    }
}

struct LineItem: Identifiable, Equatable {
    let id: UUID
    let name: String
    let price: Money
    let quantity: Int

    var total: Money {
        Money(amount: price.amount * Decimal(quantity), currency: price.currency)
    }

    func withQuantity(_ newQuantity: Int) -> LineItem {
        LineItem(id: id, name: name, price: price, quantity: newQuantity)
    }
}

struct Order: Equatable {
    let id: UUID
    let items: [LineItem]
    let status: OrderStatus
    let createdAt: Date

    var total: Money {
        items.reduce(.zero) { $0 + $1.total }
    }

    // Returns new Order instead of mutating
    func adding(_ item: LineItem) -> Order {
        Order(id: id, items: items + [item], status: status, createdAt: createdAt)
    }

    func removing(itemId: UUID) -> Order {
        Order(id: id, items: items.filter { $0.id != itemId }, status: status, createdAt: createdAt)
    }

    func withStatus(_ newStatus: OrderStatus) -> Order {
        Order(id: id, items: items, status: newStatus, createdAt: createdAt)
    }
}

enum OrderStatus: Equatable {
    case draft
    case submitted
    case confirmed
    case shipped
    case delivered
    case cancelled
}
```

### Android (Kotlin)

```kotlin
// Immutable value objects using Kotlin data classes and value classes

@JvmInline
value class Money(val cents: Long) {
    companion object {
        val ZERO = Money(0)
    }

    operator fun plus(other: Money): Money = Money(cents + other.cents)
    operator fun times(quantity: Int): Money = Money(cents * quantity)

    fun formatted(): String = "$${cents / 100}.${cents % 100}"
}

data class LineItem(
    val id: UUID,
    val name: String,
    val price: Money,
    val quantity: Int
) {
    val total: Money get() = price * quantity

    fun withQuantity(newQuantity: Int): LineItem = copy(quantity = newQuantity)
}

data class Order(
    val id: UUID,
    val items: List<LineItem>,
    val status: OrderStatus,
    val createdAt: Instant
) {
    val total: Money get() = items.fold(Money.ZERO) { acc, item -> acc + item.total }

    // Returns new Order instead of mutating
    fun adding(item: LineItem): Order = copy(items = items + item)

    fun removing(itemId: UUID): Order = copy(items = items.filter { it.id != itemId })

    fun withStatus(newStatus: OrderStatus): Order = copy(status = newStatus)
}

enum class OrderStatus {
    DRAFT, SUBMITTED, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
}
```

**Why compliant:** All domain objects are immutable. State changes return new instances. Value equality is used. Thread-safety is guaranteed.

---

## VIOLATION: Mutable Domain Objects

```swift
// BAD: Mutable classes with side effects
class Order {
    var id: UUID
    var items: [LineItem] = []  // VIOLATION: Mutable array
    var status: OrderStatus = .draft
    var total: Money = .zero  // VIOLATION: Cached value that can become stale

    init(id: UUID = UUID()) {
        self.id = id
    }

    // VIOLATION: Mutates internal state
    func addItem(_ item: LineItem) {
        items.append(item)
        recalculateTotal()
    }

    // VIOLATION: Can be called without updating total
    func removeItem(at index: Int) {
        items.remove(at: index)
        // BUG: Forgot to recalculateTotal()
    }

    // VIOLATION: Mutable state can be changed externally
    func updateStatus(_ status: OrderStatus) {
        self.status = status
    }

    private func recalculateTotal() {
        total = items.reduce(.zero) { $0 + $1.total }
    }
}

class LineItem {
    var name: String  // VIOLATION: Mutable properties
    var price: Money
    var quantity: Int

    var total: Money {
        // VIOLATION: Computed from mutable state
        Money(amount: price.amount * Decimal(quantity), currency: price.currency)
    }

    init(name: String, price: Money, quantity: Int) {
        self.name = name
        self.price = price
        self.quantity = quantity
    }
}

// Usage showing problems with mutability
let order = Order()
let item = LineItem(name: "Coffee", price: Money(amount: 4.50), quantity: 1)
order.addItem(item)

// VIOLATION: External mutation breaks encapsulation
item.quantity = 5  // Order.total is now wrong!
order.items.append(LineItem(name: "Hack", price: .zero, quantity: 1))  // Bypasses addItem
```

```kotlin
// BAD: Mutable data classes
data class Order(
    val id: UUID,
    var items: MutableList<LineItem>,  // VIOLATION: Mutable list
    var status: OrderStatus,  // VIOLATION: var instead of val
    var total: Money  // VIOLATION: Cached mutable state
) {
    // VIOLATION: Mutates internal state
    fun addItem(item: LineItem) {
        items.add(item)
        recalculateTotal()
    }

    private fun recalculateTotal() {
        total = items.fold(Money.ZERO) { acc, item -> acc + item.total }
    }
}

// Usage showing problems
val order = Order(UUID.randomUUID(), mutableListOf(), OrderStatus.DRAFT, Money.ZERO)
order.items.add(freeItem)  // Bypasses addItem, total not updated
order.status = OrderStatus.SHIPPED  // Can change status arbitrarily
```

**Why violates ENG-3.2:**
- Mutable state leads to bugs (stale cached values, external mutation)
- Not thread-safe (race conditions when accessed from multiple threads)
- Harder to reason about (state can change unexpectedly)
- Cannot safely share references (defensive copying required)
