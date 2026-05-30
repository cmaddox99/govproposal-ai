---
law_id: ENG-2.2
avatar: android-kotlin
authority: Fernando Cejas — "Architecting Android Reloaded" (2018)
---

# ENG-2.2: Clean Architecture Layers for Android (Kotlin)

> **Law:** Architecture MUST enforce clear separation of concerns with defined boundaries between layers. Dependencies MUST point inward (domain has no platform dependencies).

---

## Android Clean Architecture — Three Layers

```
┌──────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  ViewModel • Compose UI • UiState • NavGraph                 │
│  Depends on: Domain                                          │
│  Android imports: YES (ViewModelScope, Compose, Context)     │
├──────────────────────────────────────────────────────────────┤
│                     Domain Layer                             │
│  UseCases • Domain Models • Repository Interfaces            │
│  Depends on: NOTHING (pure Kotlin)                           │
│  Android imports: NONE — zero android.* imports              │
├──────────────────────────────────────────────────────────────┤
│                      Data Layer                              │
│  Repository Impls • Room DAOs • Retrofit Services • DTOs     │
│  Depends on: Domain (implements domain interfaces)           │
│  Android imports: YES (Room, Retrofit, Context)              │
└──────────────────────────────────────────────────────────────┘
```

*Source: Cejas "Architecting Android Reloaded" — dependency inversion ensures domain is testable with pure JUnit 5, no emulator required.*

---

## COMPLIANT: Domain Layer — Zero Android Imports

```kotlin
// :core:domain — module has NO android.* dependency in build.gradle.kts
// build.gradle.kts
plugins { id("org.jetbrains.kotlin.jvm") }  // NOT android library — pure Kotlin
dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
}

// Domain model — pure Kotlin data class
data class Booking(
    val id: BookingId,
    val customerId: CustomerId,
    val flightNumber: FlightNumber,
    val status: BookingStatus
)

// Repository interface — defined in domain, implemented in data
interface BookingRepository {
    suspend fun getBookings(): List<Booking>
    suspend fun confirm(booking: Booking): Confirmation
}

// Use case — pure Kotlin, fully testable without Android emulator
class ConfirmBookingUseCase @Inject constructor(
    private val repository: BookingRepository
) {
    suspend operator fun invoke(booking: Booking): Result<Confirmation> =
        runCatching { repository.confirm(booking) }
}
```

---

## COMPLIANT: Data Layer — Implements Domain Interface

```kotlin
// :data module — implements BookingRepository using Room + Retrofit
class BookingRepositoryImpl @Inject constructor(
    private val api: BookingApiService,      // Retrofit
    private val dao: BookingDao,             // Room
    private val mapper: BookingMapper
) : BookingRepository {  // ← implements the domain interface

    override suspend fun getBookings(): List<Booking> =
        dao.getAllBookings().map(mapper::toDomain)

    override suspend fun confirm(booking: Booking): Confirmation {
        val request = mapper.toRequest(booking)
        val response = api.confirmBooking(request)
        dao.update(mapper.toEntity(response))
        return mapper.toConfirmation(response)
    }
}
```

---

## COMPLIANT: Presentation Layer — ViewModel Depends Only on Domain

```kotlin
// :presentation module — depends on :core:domain, NOT :data directly
class BookingListViewModel @Inject constructor(
    private val getBookings: GetBookingsUseCase,     // domain use case
    private val confirmBooking: ConfirmBookingUseCase // domain use case
) : ViewModel() {

    private val _uiState = MutableStateFlow<BookingListUiState>(BookingListUiState.Loading)
    val uiState: StateFlow<BookingListUiState> = _uiState.asStateFlow()

    fun confirmBooking(booking: Booking) {
        viewModelScope.launch {
            confirmBooking(booking)
                .onSuccess { _uiState.value = BookingListUiState.Confirmed(it) }
                .onFailure { _uiState.value = BookingListUiState.Error(it.message) }
        }
    }
}
```

---

## VIOLATION: Domain Importing Android Framework

```kotlin
// BAD: domain class imports android.content.Context
// Means domain can ONLY run on an Android device — no pure JUnit 5 tests
import android.content.Context  // ❌ never in :core:domain module

class GetFlightStatusUseCase(private val context: Context) {  // ❌
    fun execute(flightId: String): FlightStatus {
        // Uses Android resources — untestable without emulator
        val label = context.getString(R.string.flight_on_time)
        return FlightStatus(label)
    }
}

// BAD: ViewModel importing repository implementation directly
class BrokenViewModel @Inject constructor(
    private val repo: BookingRepositoryImpl  // ❌ depends on concrete data class
    // COMPLIANT alternative: inject GetBookingsUseCase or BookingRepository interface
) : ViewModel()

// BAD: data model with Android Parcelable in domain layer
import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize  // ❌ android.os dependency in domain
data class Booking(...) : Parcelable
// COMPLIANT alternative: Parcelable only in presentation DTOs; domain uses pure data class
```

**Why ENG-2.2 violated:** `Context` in domain means every unit test requires an Android emulator (10x slower, infra-dependent). Depending on `BookingRepositoryImpl` directly makes the ViewModel impossible to test without a Room database. `Parcelable` in domain contaminates the pure Kotlin module with Android framework code.
