# Proposal: iOS Swift Avatar — Dedicated iOS Avatar with Jon Reid / Quality Coding Principles

**Proposal ID:** ios-swift-avatar  
**Submitted:** 2026-04-08  
**Status:** PROPOSED  
**Proposed by:** Hangar Labs

---

## Problem

The current `avatar-mobile-native` (`avatars/technology/mobile-native/`) conflates iOS (Swift/Xcode) and Android (Kotlin/Gradle) into a single avatar. These are fundamentally different platforms with distinct:

- **Languages:** Swift (iOS) vs. Kotlin (Android)
- **Testing frameworks:** XCTest + Swift Testing (iOS) vs. JUnit 5 + MockK + Turbine (Android)
- **Build tooling:** Xcode/`xcodebuild` (iOS) vs. Gradle (Android)
- **CI/CD pipelines:** fastlane + App Store Connect + TestFlight (iOS) vs. Gradle + Google Play (Android)
- **Code signing:** Apple Developer Program certificates, provisioning profiles, Match (iOS) vs. Android keystore (Android)
- **TDD culture:** Jon Reid / Quality Coding body of knowledge (iOS) vs. Android-specific patterns
- **Architecture:** UIKit + SwiftUI with @MainActor, ObservableObject, Combine (iOS) vs. Jetpack Compose + Flow (Android)

The mixed avatar gives agents insufficient precision when working on iOS projects. It cannot cite the **Jon Reid / Quality Coding.org iOS TDD canon** — which is the definitive reference for test-first, safe iOS development — and it misses the entire **fastlane/App Store CI/CD pipeline** that governs how iOS apps are built, signed, and shipped in an enterprise context.

### Missing iOS Knowledge

| Gap | Current State | Required State |
|-----|--------------|----------------|
| Jon Reid's TDD principles | Not referenced | XCTest + Swift Testing atomic TDD, test isolation via DI, "Test Zero" discipline |
| Swift Testing (new Apple framework) | Not referenced | `@Test`, `#expect`, dual XCTest/Swift Testing custom assertions via FailKit |
| Async test assertions | Not referenced | `ExpectToEventuallyEqual` for async code awaiting UI updates |
| ViewController presentation testing | Not referenced | `ViewControllerPresentationSpy` for alerts and action sheets |
| SwiftUI unit testing | Not referenced | `TestableView` to avoid ViewInspector boilerplate |
| TCR workflow | Not referenced | `Xcode-TCR` (test && commit || revert) for Xcode behaviors |
| Xcode compiler hardening | Not referenced | `XcodeWarnings.xcconfig` — all warnings enabled + static analyzer |
| fastlane CI/CD | Not referenced | `scan`, `gym`, `match`, `pilot`, `deliver`, `cert`/`sigh` lanes |
| App Store Connect | Not referenced | `upload_to_testflight`, `upload_to_app_store`, screenshot automation |
| Code signing automation | Not referenced | `fastlane match` for certificate/profile management in CI |
| Swift 6 concurrency safety | Not referenced | `@MainActor`, `Sendable`, data-race safety as ENG-6.1 concern |
| Functional core / imperative shell | Not referenced | Jon Reid's "you don't need advanced architecture to start testing" |

---

## Solution

Create a dedicated `avatar-ios-swift` (`avatars/technology/ios-swift/`) that:

1. **Grounds iOS TDD guidance in the Jon Reid / Quality Coding body of knowledge** — the definitive iOS testing authority, with 20+ years of Apple platform TDD experience and the book _iOS Unit Testing by Example_.

2. **Distinguishes XCTest from Swift Testing**, showing when to use each and how to write custom assertions (via FailKit) that work on both frameworks.

3. **Encodes fastlane as the primary iOS CI/CD tool**, with explicit lanes for testing (`scan`), building (`gym`), code signing (`match`), TestFlight (`pilot`), and App Store (`deliver`).

4. **Applies ENG-4.1 Atomic TDD** with iOS-specific patterns: one test per cycle, XCTest assertions, Dependency Injection via initializer injection, and mock protocols (not third-party mock libraries).

5. **Splits `mobile-native`** by adding an `ios_split_notice` to the existing avatar pointing agents toward `ios-swift` for iOS work, and retaining `mobile-native` as the Android-Native avatar (with a rename recommendation).

---

## Jon Reid / Quality Coding: Source of Truth

The `ios-swift` avatar is **grounded in published expert knowledge** from Jon Reid at [qualitycoding.org](https://qualitycoding.org) and his GitHub projects at [github.com/jonreid](https://github.com/jonreid). Key principles extracted:

### TDD Philosophy (Quality Coding Manifesto)
> *"You can only be as agile as your code lets you be."*
> — Jon Reid, Quality Coding Manifesto

- The cornerstone of software agility is **refactoring**, which requires **unit tests** as a prerequisite.
- TDD isn't "test-after" — tests written after code lock down structure and guard against change rather than guiding toward better design.
- The goal of TDD is not test coverage; it is **enabling continuous refactoring**.
- iOS has a cultural problem: Apple's sample code rarely shows testable code. Jon Reid's mission is to close that gap.

### Test Isolation Principles
- Unit tests call code from the **inside** using Dependency Injection — enabling test doubles that bypass slow/non-deterministic dependencies.
- UI Tests touch the app from the **outside** and are slow, fragile, and give general feedback. Unit tests give fast, specific feedback **while you code**.
- Avoid third-party mock frameworks — use **protocol-based mocks** (hand-written conformances) for simpler, safer isolation.

### "Test Zero" Discipline
- Every new test file starts with a deliberately failing "Test Zero" that verifies test infrastructure before adding meaningful tests.
- Comes from _iOS Unit Testing by Example_: *"Take a small step, get feedback."*

### XCTest Naming Convention
- Test methods: `func test_<scenario>_<expectedBehavior>()`
- Arrange-Act-Assert (AAA) structure as explicit comments
- `XCTAssertEqual`, `XCTAssertThrowsError`, `XCTUnwrap` as primary assertions

### Swift Testing (New Apple Framework — Xcode 16+)
- `@Test` function annotation, `#expect(...)` macro
- Test suites as `final class ... @unchecked Sendable` (not struct — allows mutable spy properties, `deinit` teardown)
- Custom assertions bridged via `FailKit` — write once, run on both XCTest and Swift Testing

### Jon Reid's GitHub Libraries (Original, Non-Fork)
| Library | Purpose |
|---------|---------|
| [XcodeWarnings](https://github.com/jonreid/XcodeWarnings) | xcconfig enabling all Xcode warnings + static analyzer |
| [ViewControllerPresentationSpy](https://github.com/jonreid/ViewControllerPresentationSpy) | Test `present`/`dismiss` of alerts, action sheets, and view controllers |
| [ExpectToEventuallyEqual](https://github.com/jonreid/ExpectToEventuallyEqual) | Async assertion (polls closure) for both XCTest and Swift Testing |
| [FailKit](https://github.com/jonreid/FailKit) | Unified `Fail.fail` + `FailSpy` for custom assertions on XCTest and Swift Testing |
| [TestableView](https://github.com/jonreid/TestableView) | Hides ViewInspector boilerplate for SwiftUI unit tests |
| [Xcode-TCR](https://github.com/jonreid/Xcode-TCR) | TCR (test && commit \|\| revert) scripts via Xcode Behaviors |

---

## fastlane: iOS CI/CD Tool of Record

[fastlane](https://fastlane.tools) is the industry-standard iOS automation framework. It is referenced here per **ENG-6.7** (audit trail via consistent build pipelines) and relevant CI/CD laws.

### Core fastlane Actions for iOS

| Action | Purpose |
|--------|---------|
| `scan` | Run XCTest/Swift Testing suite via `xcodebuild test` |
| `gym` | Build `.ipa` via `xcodebuild archive` + export |
| `match` | Certificate and provisioning profile management (git-backed or S3) |
| `pilot` / `upload_to_testflight` | Upload `.ipa` to TestFlight for beta distribution |
| `deliver` / `upload_to_app_store` | Submit to App Store with metadata and screenshots |
| `snapshot` | Automated App Store screenshot generation |
| `cert` + `sigh` | Certificate and provisioning profile download (alternative to `match`) |
| `increment_build_number` | Auto-increment CFBundleVersion for CI builds |

### Recommended Fastfile Structure

```ruby
lane :test do
  scan(scheme: "MyApp", devices: ["iPhone 16"])
end

lane :beta do
  increment_build_number
  gym(scheme: "MyApp", export_method: "app-store")
  upload_to_testflight
end

lane :release do
  increment_build_number
  snapshot
  gym(scheme: "MyApp", export_method: "app-store")
  deliver(submit_for_review: true)
  slack(message: "Version #{lane_context[SharedValues::VERSION_NUMBER]} submitted!")
end
```

---

## Files to Create

### New: `avatars/technology/ios-swift/`

| File | Description | Non-Negotiable? |
|------|-------------|-----------------|
| `manifest.yaml` | Stack config: Swift 5.9+, SwiftUI/UIKit, XCTest + Swift Testing, fastlane, SPM | — |
| `guidance.md` | Jon Reid TDD principles, testing patterns, fastlane CI/CD lanes, code signing | — |
| `examples/ENG-4.1-atomic-tdd.md` | iOS TDD cycle with XCTest + Swift Testing, Test Zero, ViewController spy | ⛔ NON-NEGOTIABLE |
| `examples/ENG-6.1-security.md` | Threat modeling, no secrets in code, ATS, Swift 6 @MainActor data-race safety | ⛔ NON-NEGOTIABLE |
| `examples/ENG-6.4-data-protection.md` | Keychain for data at rest, ATS + certificate pinning for in transit, data classification, no PII in logs | ⛔ NON-NEGOTIABLE |
| `examples/ENG-6.7-audit-trail.md` | fastlane build number audit chain, structured operation logging, immutable audit records, TestFlight traceability | ⛔ NON-NEGOTIABLE |
| `examples/ENG-3.1-complexity.md` | Swift complexity limits: cyclomatic limits in domain logic, ViewModel | — |
| `examples/ENG-3.2-immutability.md` | Swift `struct` value types, `let` preference, mutation via copy-on-write | — |
| `examples/ENG-2.2-layers.md` | iOS layered arch: Domain / Application / Infrastructure / Presentation (SwiftUI) | — |

### Modified: `avatars/technology/mobile-native/`

| File | Change |
|------|--------|
| `manifest.yaml` | Add `ios_split_notice` pointing agents to `ios-swift` for iOS work |
| `guidance.md` | Add iOS split notice banner at top |

### Modified: `avatars/index.yaml`

| Change |
|--------|
| Add `avatar-ios-swift` entry |
| Update `avatar-mobile-native` with `see_also: ios-swift` note |

### Modified: `avatars/AVATAR-RAG-INDEX.yaml`

| Change |
|--------|
| Add `ios_swift` entry under `technology_avatars` |

---

## Law Citations

| Law | Non-Negotiable? | Relevance | Example File |
|-----|----------------|-----------|--------------|
| **ENG-4.1** Atomic TDD Law | ⛔ YES | Every code change follows RED-GREEN-REFACTOR. iOS: XCTest cycle, Test Zero, one test at a time | `examples/ENG-4.1-atomic-tdd.md` |
| **ENG-6.1** Security by Design | ⛔ YES | Threat modeling at design time, security requirements in ACs, no security bolted on after | `examples/ENG-6.1-security.md` |
| **ENG-6.4** Data Protection Law | ⛔ YES | Keychain for data at rest; ATS + certificate pinning for in-transit; no PII in logs; data classification | `examples/ENG-6.4-data-protection.md` |
| **ENG-6.7** Audit Trail Law | ⛔ YES | fastlane `increment_build_number` ties every build to CI; structured operation logs; immutable audit records; TestFlight traceability to commit SHA | `examples/ENG-6.7-audit-trail.md` |
| **ENG-11.1** Hangar SDD Law | ⛔ YES | Every iOS project adopting the constitution must include `hangar-ai-specs/`; referenced in manifest | — |
| **ENG-4.2** Test Pyramid | — | iOS pyramid: unit (XCTest/Swift Testing, ≥70%) > integration (URLSession stubs) > UI (XCUITest, ≤10%) | — |
| **ENG-3.1** Complexity Limits | — | Max cyclomatic complexity per Swift method; ViewModels ≤ 10 branches | `examples/ENG-3.1-complexity.md` |
| **ENG-3.2** Immutability Law | — | Prefer `struct` + `let`; mutations in domain entities via `mutating func`; `@Published` wrapped in `private(set)` | `examples/ENG-3.2-immutability.md` |
| **ENG-2.2** Layered Architecture | — | Domain / Application / Infrastructure / Presentation layers, no cross-layer leaks | `examples/ENG-2.2-layers.md` |

---

## Success Criteria

| Criterion | Target |
|-----------|--------|
| `ios-swift` avatar fully created | All 7 files present and constitution-lint passing |
| Jon Reid principles cited in guidance | ≥5 named principles with source URLs |
| fastlane documented | ≥4 lanes with working Fastfile snippet |
| TDD examples runnable | ENG-4.1 example uses real XCTest + Swift Testing syntax |
| mobile-native split notice added | iOS agents route to ios-swift, Android agents remain on mobile-native |
| index.yaml updated | `avatar-ios-swift` appears in registry |
| RAG index updated | ios_swift entry in technology_avatars |
| constitution-lint passes | `aa-constitution-lint .` returns zero violations |

---

## Dependencies

- No external team dependencies — all knowledge sourced from public domain (qualitycoding.org, github.com/jonreid, fastlane.tools)
- No breaking changes to `mobile-native` — split notice is additive
- Hangar Labs capacity: 1 autonomous implementation cycle

## References

- [Quality Coding Manifesto](https://qualitycoding.org/manifesto/) — Jon Reid's philosophy
- [iOS Unit Testing Guide](https://qualitycoding.org/ios-unit-testing/) — Jon Reid
- [iOS TDD Guide](https://qualitycoding.org/ios-tdd/) — Jon Reid
- [XcodeWarnings](https://github.com/jonreid/XcodeWarnings) — Compiler hardening
- [ViewControllerPresentationSpy](https://github.com/jonreid/ViewControllerPresentationSpy) — VC testing
- [ExpectToEventuallyEqual](https://github.com/jonreid/ExpectToEventuallyEqual) — Async assertions
- [FailKit](https://github.com/jonreid/FailKit) — Dual-framework custom assertions
- [Xcode-TCR](https://github.com/jonreid/Xcode-TCR) — TCR workflow for Xcode
- [fastlane documentation](https://docs.fastlane.tools/) — iOS CI/CD automation
- [fastlane iOS setup](https://docs.fastlane.tools/getting-started/ios/setup/) — iOS pipeline setup
- [Existing mobile-native avatar](../../../avatars/technology/mobile-native/) — Base to split from
