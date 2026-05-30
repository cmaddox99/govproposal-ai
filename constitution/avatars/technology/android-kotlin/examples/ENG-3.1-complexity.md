---
law_id: ENG-3.1
avatar: android-kotlin
---

# ENG-3.1 — Complexity Limits (Android Kotlin)

> Cyclomatic complexity ≤10 per Kotlin function. Android Lint `CyclomaticComplexity` rule.

## AA Codebase God-Class Evidence (androidapps — March 2026)

| File | LOC | Violations |
|------|-----|------------|
| `app/.../BookingViewModel.kt` | 2,106 | 8 distinct concerns; 120+ imports; 3 reactive paradigms |
| `app/.../ChangeSeatActivity.kt` | 1,965 | Fat Activity — UI + business logic + navigation |
| `checkin_base/.../CheckInManagerV2.kt` | ~2,000 | 13 boolean flags = 2^13 implicit states; 8+ responsibilities |
| `checkin_base/.../CheckInManagerV3.kt` | ~2,000 | Copy-paste of V2; 70% structural duplication (~1,500 LOC) |
| `app/.../DataModule.kt` | 1,737 | 316 `@Provides` in one DI module |

**Pattern:** codebase composite score flat at **4.7/10** across 90 days despite 3,191 commits. Source grew +11.7%, test growth only +3.8%. God classes persist because there is no file-size guardrail enforcing this law at CI.

## VIOLATION — Exceeds Complexity Limit

```kotlin
// ❌ CheckInManagerV3 — 25+ mutable boolean flags as implicit state machine
class CheckInManagerV3 @Inject constructor(...) {
    private var agreedToHazmat = false
    private var shownCoachingScreens = false
    private var restrictionShown = false
    private var allPaxCheckedIn = false
    private var tsaTouchlessScreenShowed = false
    // ... 20 more flags — 2^25 theoretical states, ~15 valid
}
```

## COMPLIANT — Sealed Class Replaces Boolean Flags

```kotlin
// ✅ ENG-3.2 + ENG-3.1 together: sealed state machine enforces valid transitions
sealed interface CheckInState {
    data object Idle : CheckInState()
    data object ValidatingPassengers : CheckInState()
    data class AwaitingHazmatAgreement(val isInternational: Boolean) : CheckInState()
    data object HazmatAgreed : CheckInState()
    data object SubmittingCheckIn : CheckInState()
    data class CheckedIn(val boardingPasses: List<BoardingPass>) : CheckInState()
    data class Failed(val reason: CheckInFailureReason) : CheckInState()
}
// 7 explicit states — exhaustive when-expression enforces handling of all transitions
```

> Full detail with Android Lint rule config: see `ENG-3.1-complexity.md` (current file is the trim).
