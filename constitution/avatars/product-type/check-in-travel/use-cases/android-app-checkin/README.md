# Use Case: Android App Check-In — Implementation Risk & Decomposition Path
# Avatar: avatar-check-in-travel | Laws: PRD-1.1, PRD-3.1, PRD-4.1, ENG-6.4, ENG-6.7
# Grounded in: androidapps code-quality-analysis.md + statechart analysis (March 2026)

use_case:
  id: uc-cit-android-app-checkin
  name: Android App Check-In — Implementation Risk
  jtbd: "When a passenger checks in on the AA Android app, the flow must complete reliably without crashing, with boarding passes issued and no data loss."
  actor: Passenger (Android app) + Engineering team
  laws: [PRD-1.1, PRD-3.1, PRD-4.1, ENG-6.4, ENG-6.7]

---

## Why This Use Case Exists

The Android app check-in flow is governed by two classes — `CheckInManagerV2` and `CheckInManagerV3` — both approximately 2,000 LOC. Statechart analysis (March 2026) found **3 confirmed critical bugs** in these files. These are product risks, not just code quality concerns. Any roadmap work that adds check-in features is building on a foundation with known crash paths and race conditions.

**This use case exists to make that risk visible to product and inform prioritisation.**

---

## Current Implementation Risk (androidapps — March 2026)

| File | LOC | Boolean Flags | Implicit States |
|------|-----|---------------|----------------|
| `CheckInManagerV2.kt` | ~2,000 | 13 | 2^13 = **8,192** |
| `CheckInManagerV3.kt` | ~2,000 | 11 | 2^11 = **2,048** |
| **Valid states (total)** | — | — | **~15** |

**Structural duplication:** V3 is a copy-paste-modify of V2 (~1,500 LOC, 70% identical). Every bug fixed in V3 must be re-applied to V2. V3 was created within the last 60 days and is already 2,000 LOC.

---

## Confirmed Critical Bugs (Statechart Analysis)

| # | Severity | Bug | Impact |
|---|----------|-----|--------|
| 1 | 🔴 CRITICAL | **Race condition:** `tsaTouchlessScreenShowed` flag reset before async API call completes → potential infinite re-trigger loop in TSA eligibility | TSA eligible passengers may loop or miss the touchless screen |
| 2 | 🔴 CRITICAL | **Crash path:** empty-traveler error dialog shown but execution continues to `checkPassengerDetailRequired()` which iterates an empty list | App crash on check-in attempts with empty passenger list |
| 3 | 🔴 HIGH | **Missing `return true`:** `REQUEST_BASIC_ECONOMY_RESTRICTIONS` handler falls through → caller told the result was NOT handled | Basic Economy restriction screen silently skipped |

**Pattern:** All 3 bugs are a direct consequence of 13 boolean flags with no centralized state machine — no single place to enforce valid transitions or guard against null/empty states.

---

## Product Impact

- **Crash path (Bug 2)** is reachable in production for any check-in attempt where the passenger list is unexpectedly empty (e.g. data load failure, network timeout before the list is populated).
- **TSA race condition (Bug 1)** means TSA Pre-check passengers may see incorrect or repeated eligibility screens — a confusing experience on a time-sensitive airport flow.
- **V2/V3 duplication** means any new check-in feature must be implemented twice, doubling the risk surface.

---

## Roadmap Implication (PRD-3.1)

**Before adding new check-in features (bag drop, biometric, lounge access) on Android, the following must be addressed:**

1. **Resolve V2/V3 duplication** — converge to a single `CheckInViewModel` with a sealed class state machine (see `android-kotlin` tech avatar: `use-cases/sealed-state-machine/`)
2. **Fix the 3 confirmed bugs** — all are trivial fixes once the state machine is in place
3. **ENG-11.1 gate:** decomposition of V2/V3 requires an approved `PROPOSAL.md` in `hangar-ai-specs/` before implementation

> ENG-6.4: passenger PII (passport, TSA Known Traveler, DOB) flows through CheckInManagerV3. Until the race condition is resolved, there is a risk of PII being passed to the wrong screen state.
