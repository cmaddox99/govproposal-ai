---
law_id: ENG-4.1
avatar: mobile-native
---

# ENG-4.1: Atomic TDD Examples for iOS/Android Native

## COMPLIANT: TDD Cycle with XCTest (iOS) and JUnit (Android)

### iOS (Swift/XCTest)

```swift
// OrderTests.swift

// Step 1: RED - Write failing test
func test_addingItem_updatesTotal() {
    // GIVEN
    let order = Order()
    let item = LineItem(name: "Coffee", price: Money(amount: 4.50))

    // WHEN
    order.add(item)

    // THEN
    XCTAssertEqual(order.total, Money(amount: 4.50))
}


// Step 2: GREEN - Write minimum code (in Order.swift)
struct Order {
    private(set) var items: [LineItem] = []

    var total: Money {
        items.first?.price ?? Money.zero
    }

    mutating func add(_ item: LineItem) {
        items.append(item)
    }
}


// Step 3: REFACTOR - Handle multiple items
struct Order {
    private(set) var items: [LineItem] = []

    var total: Money {
        items.reduce(Money.zero) { $0 + $1.price }
    }

    mutating func add(_ item: LineItem) {
        items.append(item)
    }
}


// Step 4: Commit, then write NEXT test
func test_removingItem_updatesTotal() {
    // Next TDD cycle...
}
```

### Android (Kotlin/JUnit 5)

```kotlin
// OrderTest.kt

// Step 1: RED - Write failing test
@Test
fun `adding item updates total`() {
    // GIVEN
    val order = Order()
    val item = LineItem(name = "Coffee", price = Money(4.50))

    // WHEN
    order.add(item)

    // THEN
    assertThat(order.total).isEqualTo(Money(4.50))
}


// Step 2: GREEN - Write minimum code (in Order.kt)
class Order {
    private val _items = mutableListOf<LineItem>()
    val items: List<LineItem> get() = _items

    val total: Money
        get() = _items.firstOrNull()?.price ?: Money.ZERO

    fun add(item: LineItem) {
        _items.add(item)
    }
}


// Step 3: REFACTOR - Handle multiple items
class Order {
    private val _items = mutableListOf<LineItem>()
    val items: List<LineItem> get() = _items

    val total: Money
        get() = _items.fold(Money.ZERO) { acc, item -> acc + item.price }

    fun add(item: LineItem) {
        _items.add(item)
    }
}


// Step 4: Commit, then write NEXT test
@Test
fun `removing item updates total`() {
    // Next TDD cycle...
}
```

**Why compliant:** One test at a time, minimal code to pass, refactor continuously. Same pattern works across iOS and Android.

---

## VIOLATION: UI-Dependent Tests Without Isolation

```swift
// BAD: Tests that require running the full app
class OrderViewControllerTests: XCTestCase {

    func test_orderFlow() {
        // VIOLATION: Tests multiple behaviors at once
        let app = XCUIApplication()
        app.launch()

        // VIOLATION: Depends on UI state
        app.buttons["Add Item"].tap()
        app.textFields["Item Name"].typeText("Coffee")
        app.textFields["Price"].typeText("4.50")
        app.buttons["Save"].tap()

        // VIOLATION: Tests UI, business logic, and persistence together
        XCTAssertEqual(app.staticTexts["Total"].label, "$4.50")

        // VIOLATION: Multiple assertions testing different concerns
        app.buttons["Checkout"].tap()
        XCTAssertTrue(app.staticTexts["Order Confirmed"].exists)
    }
}
```

```kotlin
// BAD: Android tests without proper isolation
class OrderActivityTest {

    @Test
    fun testFullOrderFlow() {
        // VIOLATION: Integration test disguised as unit test
        val scenario = ActivityScenario.launch(OrderActivity::class.java)

        // VIOLATION: Tests entire flow, not atomic behavior
        onView(withId(R.id.addItem)).perform(click())
        onView(withId(R.id.itemName)).perform(typeText("Coffee"))
        onView(withId(R.id.price)).perform(typeText("4.50"))
        onView(withId(R.id.save)).perform(click())

        // VIOLATION: Multiple concerns in one test
        onView(withId(R.id.total)).check(matches(withText("$4.50")))
        onView(withId(R.id.checkout)).perform(click())
        onView(withId(R.id.confirmation)).check(matches(isDisplayed()))
    }
}
```

**Why violates ENG-4.1:** Tests multiple behaviors together, depends on UI framework, slow to run, difficult to identify failure cause.

---

## TDD Cycle Commands

### iOS
```bash
# RED: Run specific test, see it fail
xcodebuild test -scheme MyApp -only-testing:MyAppTests/OrderTests/test_addingItem_updatesTotal

# GREEN: Write code, run test again
xcodebuild test -scheme MyApp -only-testing:MyAppTests/OrderTests/test_addingItem_updatesTotal

# REFACTOR: Run all domain tests
xcodebuild test -scheme MyApp -only-testing:MyAppTests/Domain

# VERIFY: Check coverage and constitutional compliance
xcodebuild test -scheme MyApp -enableCodeCoverage YES
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add item addition to Order"
```

### Android
```bash
# RED: Run specific test, see it fail
./gradlew test --tests "com.example.domain.OrderTest.adding item updates total"

# GREEN: Write code, run test again
./gradlew test --tests "com.example.domain.OrderTest.adding item updates total"

# REFACTOR: Run all domain tests
./gradlew test --tests "com.example.domain.*"

# VERIFY: Check coverage and constitutional compliance
./gradlew testDebugUnitTestCoverage
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add item addition to Order"
```
