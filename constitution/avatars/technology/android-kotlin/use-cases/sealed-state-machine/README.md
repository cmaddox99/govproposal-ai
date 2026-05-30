# Use Case: Boolean Flags → Sealed State Machine

**Avatar:** android-kotlin  
**Laws:** ENG-3.1 (Complexity Limits), ENG-3.2 (Immutability Law)  
**AA Evidence:** CheckInManagerV2 (13 boolean flags = 2^13 implicit states) and CheckInManagerV3 (11 flags = 2^11 implicit states). Both files ~2,000 LOC. 70% structural duplication between them.

---

## Problem

Boolean flags used to manage state transitions create an exponential state space. CheckInManagerV2 has 13 `var` flags scattered across 20+ methods — theoretically 8,192 state combinations, of which only ~15 are valid. There is no enforcement of valid transitions, no central state definition, and no way to exhaustively test all paths.

```kotlin
// ❌ VIOLATION — CheckInManagerV2 (AA androidapps)
class CheckInManagerV2 @Inject constructor(...) {
    private var agreedToHazmat = false
    private var shownCoachingScreens = false
    private var restrictionShown = false
    private var promptedToShowSeatsBeforeCheckIn = false
    private var allPaxCheckedIn = false
    private var isCheckInFlow = false
    private var tsaTouchlessScreenShowed = false
    private var ancillaryOffersFlowStarted = false
    private var lfbuOfferChecked = false
    // 4 more flags...
    // Result: 2^13 = 8,192 theoretical states; only ~15 are valid; none enforced
}
```

**Bug pattern from statechart analysis:** `tsaTouchlessScreenShowed` flag reset before async API call completes → race condition (confirmed critical bug). Boolean flags set and reset across methods with no centralized coordination make this class of bug systematic.

---

## COMPLIANT — Sealed Interface State Machine

```kotlin
// ✅ 7 explicit states — compiler enforces exhaustive handling
sealed interface CheckInState {
    data object Idle : CheckInState()
    data object ValidatingPassengers : CheckInState()
    data class AwaitingHazmatAgreement(
        val isInternational: Boolean
    ) : CheckInState()
    data object HazmatAgreed : CheckInState()
    data class AwaitingAncillaryOffers(
        val offers: List<AncillaryOffer>
    ) : CheckInState()
    data object SubmittingCheckIn : CheckInState()
    data class CheckedIn(val boardingPasses: List<BoardingPass>) : CheckInState()
    data class Failed(val reason: CheckInFailureReason) : CheckInState()
}

sealed interface CheckInFailureReason {
    data object EmptyPassengerList : CheckInFailureReason()
    data object HazmatRejected : CheckInFailureReason()
    data class ApiError(val message: String) : CheckInFailureReason()
}
```

## COMPLIANT — ViewModel Drives State

```kotlin
@HiltViewModel
class CheckInViewModel @Inject constructor(
    private val checkIn: ExecuteCheckInUseCase
) : ViewModel() {

    private val _state = MutableStateFlow<CheckInState>(CheckInState.Idle)
    val state: StateFlow<CheckInState> = _state.asStateFlow()

    fun startCheckIn(reservation: Reservation) {
        viewModelScope.launch {
            _state.value = CheckInState.ValidatingPassengers
            checkIn(reservation)
                .onSuccess { passes -> _state.value = CheckInState.CheckedIn(passes) }
                .onFailure { e -> _state.value = CheckInState.Failed(CheckInFailureReason.ApiError(e.message ?: "")) }
        }
    }

    fun agreeToHazmat() {
        check(_state.value is CheckInState.AwaitingHazmatAgreement) { "Invalid transition" }
        _state.value = CheckInState.HazmatAgreed
    }
}
```

## Testing State Transitions (ENG-4.1)

```kotlin
@Test
fun `hazmat agreement transitions from AwaitingHazmat to HazmatAgreed`() = runTest {
    // Arrange — set known state
    val vm = CheckInViewModel(fakeCheckIn)
    vm.forceState(CheckInState.AwaitingHazmatAgreement(isInternational = true))

    // Act
    vm.agreeToHazmat()

    // Assert — single transition, no flags to track
    vm.state.test {
        assertIs<CheckInState.HazmatAgreed>(awaitItem())
        cancelAndConsumeRemainingEvents()
    }
}
```

**Why this eliminates the bug class:** transition to `AwaitingHazmatAgreement` only happens after async validation completes — the state itself carries the guarantee. No flag to reset early.

---

## V2/V3 Consolidation Path

With a shared `CheckInState` sealed interface, `CheckInManagerV2` and `CheckInManagerV3` converge to a single `CheckInViewModel` — one state machine, one implementation, zero copy-paste duplication. The ~1,500 LOC of duplicated logic disappears.

**ENG-11.1 gate:** this decomposition requires an approved `PROPOSAL.md` in `hangar-ai-specs/` before implementation.
