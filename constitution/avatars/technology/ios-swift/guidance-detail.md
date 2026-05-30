# iOS Swift — Extended Guidance Detail

> Supplement to `guidance.md`. Contains codebase-grounded facts and reference material that exceed the ≤450-token guidance.md limit.

---

## Jon Reid Libraries (Recommended — Not Yet Adopted in AA Codebase)

The following libraries are recommended by Jon Reid / Quality Coding as best-in-class iOS testing tools. **As of 2026-04-30, none of these are referenced in any Cartfile across the AA iOS repos.** They are aspirational recommendations for future adoption.

| Library | URL | Purpose |
|---------|-----|---------|
| XcodeWarnings | https://github.com/jonreid/XcodeWarnings | xcconfig enabling all Xcode warnings and static analyzer — "turn up to eleven" |
| ViewControllerPresentationSpy | https://github.com/jonreid/ViewControllerPresentationSpy | Test present/dismiss of alerts, action sheets, and view controllers without running UI |
| ExpectToEventuallyEqual | https://github.com/jonreid/ExpectToEventuallyEqual | Async assertion that polls a closure — works on both XCTest and Swift Testing |
| FailKit | https://github.com/jonreid/FailKit | Unified `Fail.fail` + `FailSpy` for custom assertions — write once, run on both frameworks |
| TestableView | https://github.com/jonreid/TestableView | Hide ViewInspector boilerplate for SwiftUI unit tests |
| Xcode-TCR | https://github.com/jonreid/Xcode-TCR | test && commit \|\| revert scripts via Xcode Behaviors |

---

## AA iOS Codebase Reality (as of 2026-04-30)

Verified by scanning checkin-ios, booking-ios, corenetworking-ios, coreui-ios, and core-ios.

- **Scale:** 46+ iOS framework repos, all using Carthage + `--use-xcframeworks`
- **UI framework split:** UIKit-dominant (~87% UIKit, ~13% SwiftUI across production repos). SwiftUI is being incrementally adopted — it is not the primary UI layer.
- **Testing framework split:** ~85% XCTest, ~15% Swift Testing. Migration pattern: `@Suite(.serialized) struct {Subject}Tests: Contextual` where `Contextual` is an AA-internal custom protocol used as the base for Swift Testing suites.
- **Project generation:** Tuist (`Project.swift`) is present in most repos. iOS deployment target is `14.0` (`iOSTargetVersion = "14.0"` in Project.swift files).
- **Build tooling:** xcodebuild under the hood with xcpretty for output formatting.
- **Shared tooling:** `moduletools-ios` is cloned on demand via `update-tools.sh` into `Tooling/`. This populates `Tooling/fastlane/`, `Tooling/carthage-wrapper.sh`, and `Tooling/update-dependencies.sh`.
- **Dependency management:** Carthage is the production dependency manager. SPM is used only for `DangerDependencies` (CI/Danger tooling, dev-only).
- **Framework naming:** AA internal framework public API uses the prefix `American` — e.g., `AmericanCheckIn`, `AmericanBooking`, `AmericanCoreNetworking`.
- **Feature toggles:** `AAFeature{Name}` prefix — e.g., `AAFeatureTSATouchlessID`, `AAFeatureCheckInEligible`. Toggle files live under `Sources/{Feature}/Relevance/`.
- **Mock naming:** `Mock{Protocol}` — hand-written, no mocking framework.
- **Test simulator:** `iPhone 17` (auto-detected for latest iOS version in fastlane lanes).

---

## Fastfile Reference (Real Lanes)

Fastfile lives at `Tooling/fastlane/Fastfile` in each repo (shared from `moduletools-ios`). Always invoke via `bundle exec fastlane`.

| Lane | Description |
|------|-------------|
| `setup_dependencies` | Carthage update + clear derived data; run before building |
| `create_framework_release` | Carthage release build for framework distribution |
| `create_framework_release_beta` | Beta variant of the framework release build |
| `run_unit_tests` | Two-phase: `build-for-testing` then `test-without-building` on iPhone 17 simulator |
| `run_unit_tests_beta` | Unit tests against the beta Xcode toolchain |
| `run_ui_tests` | UI tests on the `Example` scheme |
| `build_ios` | `gym` build producing the framework bundle |
| `use_xcode_beta` | Switch CI to Xcode beta toolchain |
| `use_xcode_release` | Switch CI back to Xcode release toolchain |
| `sync_signing_assets_jenkins` | `match` from `https://github.com/AAInternal/codesign-ios.git` branch `update/xcode15` |

**Code signing repo:** `https://github.com/AAInternal/codesign-ios.git`, branch `update/xcode15`
