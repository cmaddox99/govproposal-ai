---
law_id: ENG-3.1
avatar: mobile-native
---

# ENG-3.1: Complexity Limits Examples for iOS/Android Native

## COMPLIANT: Simple, Focused ViewModel

### iOS (SwiftUI)

```swift
// OrderViewModel.swift - Focused, low complexity

@MainActor
final class OrderViewModel: ObservableObject {
    @Published private(set) var items: [LineItem] = []
    @Published private(set) var total: Money = .zero
    @Published private(set) var isLoading = false
    @Published private(set) var error: OrderError?

    private let orderService: OrderService

    init(orderService: OrderService) {
        self.orderService = orderService
    }

    // Simple, single-purpose methods
    func addItem(_ item: LineItem) {
        items.append(item)
        recalculateTotal()
    }

    func removeItem(at index: Int) {
        guard items.indices.contains(index) else { return }
        items.remove(at: index)
        recalculateTotal()
    }

    func submitOrder() async {
        isLoading = true
        error = nil

        do {
            let order = Order(items: items)
            try await orderService.submit(order)
            items = []
            total = .zero
        } catch let orderError as OrderError {
            error = orderError
        } catch {
            self.error = .unknown(error)
        }

        isLoading = false
    }

    private func recalculateTotal() {
        total = items.reduce(.zero) { $0 + $1.price }
    }
}
```

### Android (Jetpack Compose)

```kotlin
// OrderViewModel.kt - Focused, low complexity

@HiltViewModel
class OrderViewModel @Inject constructor(
    private val orderService: OrderService
) : ViewModel() {

    private val _items = MutableStateFlow<List<LineItem>>(emptyList())
    val items: StateFlow<List<LineItem>> = _items.asStateFlow()

    private val _total = MutableStateFlow(Money.ZERO)
    val total: StateFlow<Money> = _total.asStateFlow()

    private val _uiState = MutableStateFlow<OrderUiState>(OrderUiState.Idle)
    val uiState: StateFlow<OrderUiState> = _uiState.asStateFlow()

    // Simple, single-purpose methods
    fun addItem(item: LineItem) {
        _items.update { it + item }
        recalculateTotal()
    }

    fun removeItem(index: Int) {
        _items.update { items ->
            items.filterIndexed { i, _ -> i != index }
        }
        recalculateTotal()
    }

    fun submitOrder() {
        viewModelScope.launch {
            _uiState.value = OrderUiState.Loading

            orderService.submit(Order(_items.value))
                .onSuccess {
                    _items.value = emptyList()
                    _total.value = Money.ZERO
                    _uiState.value = OrderUiState.Success
                }
                .onFailure { error ->
                    _uiState.value = OrderUiState.Error(error.message)
                }
        }
    }

    private fun recalculateTotal() {
        _total.value = _items.value.fold(Money.ZERO) { acc, item -> acc + item.price }
    }
}

sealed class OrderUiState {
    object Idle : OrderUiState()
    object Loading : OrderUiState()
    object Success : OrderUiState()
    data class Error(val message: String?) : OrderUiState()
}
```

**Why compliant:** Each method has single responsibility, cyclomatic complexity is low (few branches), state is clearly defined, and error handling is straightforward.

---

## VIOLATION: God ViewModel with High Complexity

```swift
// BAD: iOS ViewModel doing too much
@MainActor
class OrderViewModel: ObservableObject {
    @Published var items: [LineItem] = []
    @Published var total: Money = .zero
    @Published var discountCode: String = ""
    @Published var appliedDiscount: Discount?
    @Published var shippingAddress: Address?
    @Published var billingAddress: Address?
    @Published var useShippingAsBilling = true
    @Published var selectedPaymentMethod: PaymentMethod?
    @Published var savedCards: [SavedCard] = []
    @Published var loyaltyPoints: Int = 0
    @Published var usePoints = false
    @Published var giftCards: [GiftCard] = []
    @Published var selectedGiftCard: GiftCard?
    @Published var isLoading = false
    @Published var loadingMessage: String?
    @Published var error: Error?
    @Published var showingConfirmation = false
    // ... 20 more @Published properties

    func processOrder() async {
        // VIOLATION: 200+ line method with 15+ branches
        isLoading = true

        // Validate items
        guard !items.isEmpty else {
            error = OrderError.emptyCart
            isLoading = false
            return
        }

        // Apply discount if present
        if !discountCode.isEmpty {
            if let discount = await validateDiscount(discountCode) {
                if discount.minimumOrder <= total {
                    if discount.validCategories.isEmpty ||
                       items.allSatisfy({ discount.validCategories.contains($0.category) }) {
                        if !discount.excludedItems.contains(where: { excluded in
                            items.contains(where: { $0.id == excluded })
                        }) {
                            appliedDiscount = discount
                            recalculateTotal()
                        } else {
                            error = OrderError.discountExcludedItems
                        }
                    } else {
                        error = OrderError.discountCategoryMismatch
                    }
                } else {
                    error = OrderError.discountMinimumNotMet
                }
            } else {
                error = OrderError.invalidDiscount
            }
        }

        // Validate shipping
        guard let shipping = shippingAddress else {
            error = OrderError.missingShipping
            isLoading = false
            return
        }

        // Validate billing
        let billing = useShippingAsBilling ? shipping : billingAddress
        guard let finalBilling = billing else {
            error = OrderError.missingBilling
            isLoading = false
            return
        }

        // Handle payment - nested conditions continue for 100+ more lines
        if usePoints && loyaltyPoints > 0 {
            // Complex points logic...
        }

        if let giftCard = selectedGiftCard {
            // Complex gift card logic...
        }

        // ... continues with payment processing, inventory check,
        // fraud detection, analytics, etc. all in one method
    }
}
```

**Why violates ENG-3.1:**
- Cyclomatic complexity exceeds limits (15+ branches in single method)
- Method too long (200+ lines)
- Too many responsibilities (cart, discount, shipping, billing, payment, loyalty, gift cards)
- Deeply nested conditionals making logic hard to follow
- Should be split into focused services: CartService, DiscountService, PaymentService, etc.
