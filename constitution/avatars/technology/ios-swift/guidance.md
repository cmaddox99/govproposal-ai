# iOS (Swift / Xcode) Guidance

> **Stack:** Swift 5.9+, iOS 14.0+, UIKit (dominant) / SwiftUI (incremental), XCTest (dominant) / Swift Testing (in progress), Tuist, Carthage, fastlane.

---

## Codebase Reality

**UIKit is dominant.** Production repos (checkin-ios, booking-ios) are ~87% UIKit, ~13% SwiftUI. SwiftUI is being incrementally adopted — do not assume SwiftUI-first.

**XCTest is dominant.** ~85% XCTest, ~15% Swift Testing. Migration is in progress using `@Suite(.serialized) struct {Subject}Tests: Contextual` (where `Contextual` is an AA-internal custom protocol). Do not introduce new third-party test libraries; none of the Jon Reid libraries are in any Cartfile.

**Carthage, not SPM.** All production dependencies use Carthage + `--use-xcframeworks`. SPM is used only for `DangerDependencies` (CI tooling). Run `./Tooling/update-dependencies.sh update --mute-notifications` to update deps.

**Fastlane lives in `Tooling/fastlane/`.** Always invoke via `bundle exec fastlane`. Key lanes: `run_unit_tests`, `run_ui_tests`, `build_ios`, `setup_dependencies`, `sync_signing_assets_jenkins`.

> Full detail: see guidance-detail.md in this directory.

---

## Core Agent Behaviors

**TDD is mandatory.** Every code change follows RED → GREEN → REFACTOR (ENG-4.1). No test, no merge. Write Test Zero first — a deliberately failing test that verifies the test harness runs before writing real tests.

**Prefer value types.** Use `struct` and `let` by default (ENG-3.2). Classes are justified only for identity semantics, reference sharing, or Objective-C interop.

**Constructor injection only.** Every dependency is a protocol injected at `init`. Never use static service locators (the `CheckInEnvironment` pattern in checkin-ios is a documented antipattern — do not replicate it).

**No god classes.** Files over 200 lines are a warning; over 300 lines require extraction before adding logic. Known violations in this codebase: `BookingSearchCoordinator` (461 lines), `FareMapSearchViewModel` (470 lines), `TravelerContactInfoViewController` (918 lines), `CheckInManager` (1,186 lines). Do not add to any of these without first extracting a responsibility.

**Code signing via fastlane match.** Always use `bundle exec fastlane` — never bare `fastlane`. All secrets via CI environment variables — never in source.

---

## Non-Negotiable Laws

| Law | Requirement |
|-----|------------|
| ENG-4.1 | Atomic TDD — tests written before code |
| ENG-10.1 | `hangar-ai-specs/` present at repo root; manifest read before changes |
| ENG-11.1 | Spec entry created before feature code is written |

---

## See Also

- `examples/ENG-4.1-atomic-tdd.md` — XCTest and Swift Testing patterns, Test Zero
- `examples/ENG-3.1-complexity.md` — god class evidence and complexity limits
- `use-cases/protocol-di/` — constructor injection vs service locator (real codebase comparison)
- `use-cases/mvvm-combine/` — feature module TDD walkthrough
- `guidance-detail.md` — Jon Reid library references, full codebase stats, Fastfile lane reference
