---
law_id: ENG-3.2
avatar: android-kotlin
---

# ENG-3.2: Immutability by Default Examples for Android (Kotlin)

> **Law:** All data structures SHOULD be immutable by default. Mutation MUST be explicit and justified. Mutable state MUST be encapsulated and minimised.

---

## COMPLIANT: Kotlin `val`, `data class`, and `.copy()`

```kotlin
// COMPLIANT: immutable domain model — val everywhere, data class for .copy()
data class Booking(
    val id: BookingId,
    val customerId: CustomerId,
    val flightNumber: FlightNumber,
    val status: BookingStatus = BookingStatus.PENDING,
    val passengerCount: Int,
    val total: Money
)

// COMPLIANT: state transitions via .copy() — original preserved, new instance returned
fun Booking.confirm(): Booking = copy(status = BookingStatus.CONFIRMED)
fun Booking.cancel(): Booking = copy(status = BookingStatus.CANCELLED)
```

---

## COMPLIANT: Encapsulated Mutable State (MVVM + StateFlow)

```kotlin
class BookingListViewModel @Inject constructor(
    private val repository: BookingRepository
) : ViewModel() {

    // COMPLIANT: mutable state is private — external consumers see read-only StateFlow
    private val _uiState = MutableStateFlow<BookingListUiState>(BookingListUiState.Loading)
    val uiState: StateFlow<BookingListUiState> = _uiState.asStateFlow()

    init { loadBookings() }

    private fun loadBookings() {
        viewModelScope.launch {
            runCatching { repository.getBookings() }
                .onSuccess { _uiState.value = BookingListUiState.Success(it) }
                .onFailure { _uiState.value = BookingListUiState.Error(it.message) }
        }
    }
}

// COMPLIANT: sealed interface UI state — each state is an immutable data class
sealed interface BookingListUiState {
    data object Loading : BookingListUiState
    data class Success(val bookings: List<Booking>) : BookingListUiState
    data class Error(val message: String?) : BookingListUiState
}
```

---

## COMPLIANT: `@Immutable` in Jetpack Compose

```kotlin
// COMPLIANT: @Immutable tells Compose this class won't change after composition
@Immutable
data class BookingCardUiModel(
    val bookingReference: String,
    val flightNumber: String,
    val departureCity: String,
    val arrivalCity: String,
    val status: String
)

@Composable
fun BookingCard(uiModel: BookingCardUiModel) {
    // Compose can skip recomposition if uiModel reference hasn't changed — correct because @Immutable
    Card {
        Column {
            Text(uiModel.flightNumber)
            Text("${uiModel.departureCity} → ${uiModel.arrivalCity}")
            Text(uiModel.status)
        }
    }
}
```

---

## VIOLATION: Unnecessary Mutation

```kotlin
// BAD: var where val suffices — unclear when value might change
var bookingId: String = ""  // ❌ use val bookingId: String = generateId()

// BAD: mutable list escapes as public API — callers can modify internal state
class BookingRepository {
    val bookings = mutableListOf<Booking>()  // ❌ public mutable list
}

// BAD: MutableStateFlow exposed publicly — external code can push state
class BrokenViewModel : ViewModel() {
    val uiState = MutableStateFlow<UiState>(UiState.Loading)  // ❌ should be StateFlow
}

// BAD: regular class for UI state — Compose can't skip recomposition safely
data class MutableUiModel(   // ❌ no @Immutable, has var fields
    var title: String,
    var isLoading: Boolean
)
```

**Why ENG-3.2 violated:** Public mutable lists allow callers to corrupt internal state invisibly. Exposed `MutableStateFlow` breaks encapsulation — any class can push invalid states. Classes without `@Immutable` cause Compose to conservatively recompose on every state change, degrading performance.
