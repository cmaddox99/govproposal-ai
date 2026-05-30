---
law_id: ENG-4.2
avatar: ios-swift
type: deliberation
parent: ENG-4.2-test-pyramid.md
authority: Jon Reid / Quality Coding (qualitycoding.org)
---

# ENG-4.2: Test Pyramid — Ensemble Deliberation

Four perspectives were weighed to establish the iOS-specific pyramid ratios.

---

## Jon Reid (Quality Coding — iOS TDD authority)

> "UI tests touch the app from the **outside** — they cannot use DI, they are slow,
> and give very general feedback. Unit tests call from the **inside** using DI —
> they are fast and specific. The iOS community's over-reliance on XCUITest is the
> single biggest obstacle to sustainable TDD.
>
> My recommendation: **≥75% unit, ~20% integration, ≤5% UI.** I've shipped
> production apps with zero UI tests and high confidence because the ViewModel layer
> had comprehensive coverage. If ViewModels are well-tested, the SwiftUI View layer
> is a thin declarative binding that rarely breaks."

**Key contribution:** Push unit tests higher than the generic pyramid. ViewModels are
the dominant test target. Favor `ViewControllerPresentationSpy` and
`ExpectToEventuallyEqual` over UI tests for async presentation behavior.

---

## Martin Fowler (Test Pyramid originator)

> "The pyramid is about **speed and cost**, not platform. The iOS wrinkle is simulator
> boot time — even 'integration' tests that hit URLSession stubs pay a startup tax.
>
> Keep the integration layer healthy at **~20%** rather than squeezing it down. Real
> wiring bugs — JSON decoding mismatches, Keychain access policies, Core Data schema
> migrations — only surface in integration tests. The unit/integration boundary is
> the protocol seam: above a protocol is unit-testable; below it (real URLSession,
> real Keychain) is integration."

**Key contribution:** Define the integration boundary precisely at the protocol seam.
Keep integration at ~20% to catch real wiring bugs.

---

## Kent Beck (TDD creator)

> "I care less about exact percentages and more about **feedback speed**. Can you
> run the relevant tests in under 2 seconds after every edit? If yes, your pyramid
> is healthy. If you wait 45 seconds for a simulator to verify a business rule,
> your pyramid is upside down.
>
> Swift compiles fast enough to give sub-second unit test feedback via
> `xcodebuild test -only-testing:`. Protect that speed at all costs."

**Key contribution:** Optimize for feedback speed, not ratio compliance. Sub-second
unit tests are achievable on iOS — protect that property as a hard invariant.

---

## AA iOS Staff Engineer (airline production experience)

> "We run **~500 unit tests in 8 seconds**, ~80 integration tests in 25 seconds, and
> ~12 UI tests in 3 minutes. The UI tests are the ones that break on every Xcode update.
>
> Lock XCUITest to **≤10 scenarios** covering revenue-critical and safety-critical
> happy paths. Use ViewInspector for SwiftUI snapshot-style assertions at unit-test
> level — much faster than XCUITest and catches layout regressions without a simulator."

**Key contribution:** Real-world AA ratio confirms the pyramid. Cap XCUITest by
scenario count (not just percentage). ViewInspector as a speed multiplier for SwiftUI.

---

## Synthesis

All four perspectives converge: Unit ≥75%, Integration ~20%, UI ≤5% (≤10 scenarios).
The ratios in `ENG-4.2-test-pyramid.md` reflect this consensus.
