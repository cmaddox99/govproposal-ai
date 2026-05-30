# Proposal: Android Kotlin Avatar — Dedicated Android Avatar with Jeroen Mols / Philipp Hauer Principles

**Proposal ID:** android-kotlin-avatar  
**Submitted:** 2026-04-08  
**Status:** PROPOSED  
**Proposed by:** Hangar Labs

---

## Problem

The current `avatar-mobile-native` (`avatars/technology/mobile-native/`) conflates iOS (Swift/Xcode) and Android (Kotlin/Gradle) into a single avatar. The iOS split has already been completed via the `ios-swift` avatar (commit 0a0c451). The Android half now needs the same treatment.

The remaining `mobile-native` avatar is Android content without a dedicated identity. It cannot cite the Android community's accepted authorities on TDD and design patterns — the **Jeroen Mols / Philipp Hauer / Fernando Cejas body of knowledge** — and it lacks all Android-specific treatment of the non-negotiable security and audit trail laws (ENG-6.1, ENG-6.4, ENG-6.7), which have platform-specific Android implementations (Android Keystore, Network Security Config, Play Store build audit).

### Missing Android Knowledge

| Gap | Current State | Required State |
|-----|--------------|----------------|
| Jeroen Mols TDD principles | Not referenced | "Everything can be tested" manifesto; isolating Android framework from business logic; TestDouble patterns |
| Philipp Hauer Kotlin idioms | Not referenced | Backtick test names, `@TestInstance(PER_CLASS)`, `@Nested` suites, MockK over Mockito |
| Fernando Cejas Clean Architecture | Not referenced | Three-part "Architecting Android" canon: domain / data / presentation layers in Kotlin |
| Google Now in Android (NiA) | Not referenced | 2024–2025 reference app: Compose + Hilt + Room + Turbine + modular testing |
| Android Keystore | Not referenced | Hardware-backed key storage for at-rest data (ENG-6.4) |
| EncryptedSharedPreferences | Not referenced | Encrypted local storage via Jetpack Security (ENG-6.4) |
| Network Security Config | Not referenced | Certificate pinning via XML manifest config (ENG-6.4) |
| Play Integrity API | Not referenced | Runtime app attestation (ENG-6.1) |
| ProGuard / R8 | Not referenced | Code shrinking hides class/method names from reverse engineering (ENG-6.1) |
| Play Store build audit | Not referenced | `fastlane supply`, `versionCode` from CI = audit trail per build (ENG-6.7) |
| Gradle Managed Devices | Not referenced | CI device testing without physical devices (ENG-4.2) |
| Coroutine testing | Not referenced | `runTest`, `TestCoroutineDispatcher`, `advanceUntilIdle` patterns |
| Turbine for Flow | Partially present | Full Turbine assertion patterns: `awaitItem`, `expectMostRecentItem`, cancellation |
| MockK idiomatic use | Partially present | `coEvery`/`coVerify`, slot capturing, `relaxed = true`, `spyk` patterns |
| Hilt test injection | Not referenced | `@HiltAndroidTest`, `@UninstallModules`, `@BindValue` for replacing deps in tests |

---

## Solution

Create a dedicated `avatar-android-kotlin` (`avatars/technology/android-kotlin/`) that:

1. **Grounds Android TDD guidance in the Jeroen Mols body of knowledge** — jeroenmols.com, Google Developer Expert, "Testing Made Sweet with a Mockito" talk, "everything can be tested" philosophy with practical isolation techniques.

2. **Adopts Philipp Hauer's Kotlin testing idioms** — the authoritative KotlinConf 2018 reference for idiomatic Kotlin unit tests: backtick names, `@Nested` classes, JUnit 5 `@TestInstance(PER_CLASS)`, MockK DSL over Mockito.

3. **Grounds architecture in Fernando Cejas' "Architecting Android — Reloaded"** — the three-layer Kotlin Clean Architecture (domain / data / presentation), use-case (interactor) pattern, and the principle that domain logic must have zero Android framework imports.

4. **References Google's Now in Android (NiA) sample** as the official 2024–2025 living reference for Jetpack Compose + Hilt + Room + Turbine + modular testing.

5. **Applies non-negotiable laws with Android-specific implementations:**
   - ENG-4.1: JUnit 5 + MockK atomic TDD cycle, Turbine for Flow assertions
   - ENG-6.1: ProGuard/R8, Play Integrity API, Network Security Config, no secrets in code
   - ENG-6.4: Android Keystore + EncryptedSharedPreferences at-rest, certificate pinning in-transit, no PII in Logcat
   - ENG-6.7: `fastlane supply` + `versionCode` from CI = every Play Store build traceable to commit SHA

6. **Deprecates `mobile-native`** — once this avatar ships, `mobile-native` is fully superseded. iOS is covered by `ios-swift`; Android by `android-kotlin`. The mobile-native avatar will be archived.

---

## Thought Leader Sources

### Jeroen Mols — Primary TDD Authority
> **Site:** [jeroenmols.com](https://jeroenmols.com) | **GitHub:** [JeroenMols](https://github.com/JeroenMols) | **Role:** Android GDE, Plaid

Key insights for this avatar:
- **"Everything can be tested"** — the foundational claim. Android's tight coupling to the framework is an excuse, not a barrier; DI solves it.
- **Isolate Android from business logic** — use repository/use-case patterns so that `ViewModel` and domain code can be unit-tested on the JVM without Robolectric.
- **Mockito/MockK for isolation** — hand-written test doubles for domain protocols; MockK for Android framework seams.
- **Testing pyramid discipline** — resist the temptation to write Espresso tests for business logic; push coverage down into fast JVM unit tests.
- Conference talks: *"Testing Made Sweet with a Mockito"* (Devoxx, Droidcon), demonstrating practical TDD cycle on real Android codebases.

### Philipp Hauer — Kotlin Testing Idioms Authority
> **Site:** [phauer.com](https://phauer.com) | **Talk:** [KotlinConf 2018 — Best Practices for Unit Testing in Kotlin](https://www.youtube.com/watch?v=RX_g65J14H0)

Canonical Kotlin test idioms adopted in this avatar:
- **Backtick test names** — `fun \`adding item updates total\`()` for human-readable failure messages
- **`@TestInstance(Lifecycle.PER_CLASS)`** — single test instance; enables non-static `@BeforeAll`/`@AfterAll` and `val` mocks declared as fields
- **`@Nested` inner classes** — group related tests (e.g., `inner class WhenOrderIsEmpty`, `inner class WhenOrderHasItems`)
- **MockK over Mockito** — first-class Kotlin support: mocks final classes, Kotlin coroutines (`coEvery`/`coVerify`), suspend functions, objects/companions
- **Assertion libraries** — Kotest assertions or AssertJ for expressive, readable failure messages over plain `assertEquals`

### Fernando Cejas — Clean Architecture Authority
> **Site:** [fernandocejas.com](https://fernandocejas.com) | **GitHub:** [android10](https://github.com/android10/Android-CleanArchitecture-Kotlin)

The three-part "Architecting Android" canon:
1. *"The clean way?"* (2014) — layers, dependency rule, use cases
2. *"The evolution."* (2015) — RxJava reactive patterns
3. *"Reloaded."* (2019) — Kotlin, coroutines, sealed classes, functional patterns

Key principle: **"The domain layer must have zero Android imports."** Business rules are plain Kotlin; the Android framework is an implementation detail of the infrastructure layer.

### Google Now in Android — Official Living Reference
> **GitHub:** [android/nowinandroid](https://github.com/android/nowinandroid)

The 2024–2025 reference for:
- Jetpack Compose UI + Compose Testing APIs
- Hilt dependency injection with `@HiltAndroidTest` for instrumented tests
- Room + Paging 3 for local data
- Turbine for Flow stream testing
- Full modularization: feature modules, core modules, test fixtures modules

### Philipp Hauer / MockK Ecosystem
> **MockK:** [mockk.io](https://mockk.io) | **Turbine:** [cash.app/turbine](https://github.com/cashapp/turbine)

- MockK (5,737 ⭐) — Kotlin-native mocking: `mockk<T>()`, `every { } returns`, `coEvery { } returns`, `verify { }`, `coVerify { }`, slot capturing, relaxed mocks
- Turbine (2,817 ⭐) — Flow testing: `flow.test { awaitItem(); awaitComplete() }`, error assertion

---

## Fastlane for Android CI/CD

`fastlane` covers both iOS and Android. The Android lanes relevant to this avatar:

| Lane | Purpose | ENG Law |
|------|---------|---------|
| `gradle(task: "test")` | Run all JVM unit tests | ENG-4.1 |
| `gradle(task: "connectedAndroidTest")` | Run instrumented tests | ENG-4.2 |
| `gradle(task: "bundle", build_type: "Release")` | Build AAB for Play Store | ENG-6.7 |
| `supply` | Upload AAB to Play Store (alpha/beta/production) | ENG-6.7 |
| `gradle(task: "lint")` | Android Lint check | ENG-3.1 |
| `increment_version_code` | Monotonic `versionCode` from CI = build audit trail | ENG-6.7 |

The `versionCode` from `increment_version_code` + CI commit SHA in release notes creates a traceable chain: Play Store build ← AAB artifact ← CI run ← git commit. This is the Android equivalent of the iOS `increment_build_number` + TestFlight audit chain.

---

## Relationship to Existing Avatars

| Avatar | Relationship |
|--------|-------------|
| `ios-swift` | Sibling — same proposal pattern, different platform |
| `mobile-native` | **To be deprecated** once this avatar ships; add split notice on creation |
| `java-spring` | Structural reference only — JUnit 5 test structure mirrors Android, but Spring/Maven/Mockito differ |

### Migration from mobile-native

The `mobile-native/guidance.md` Android section (lines ~195–420) contains reusable baseline content:
- JUnit 5 + MockK + Turbine test structure ✅ migrate
- Kotlin entity / value object patterns ✅ migrate
- `@HiltViewModel` MVVM + `StateFlow` + Compose ✅ migrate + expand
- Turbine Flow assertion examples ✅ migrate + expand

Content to add (not in mobile-native):
- Jeroen Mols TDD principles and isolation philosophy
- Philipp Hauer `@Nested`, `@TestInstance(PER_CLASS)`, backtick names
- Fernando Cejas layered architecture Kotlin specifics
- ENG-6.1: ProGuard/R8, Play Integrity API, Network Security Config
- ENG-6.4: Android Keystore, EncryptedSharedPreferences, no PII in Logcat
- ENG-6.7: fastlane supply + versionCode CI audit chain
- Hilt test injection patterns (`@HiltAndroidTest`)
- Gradle Managed Devices for CI

---

## Files to Create

| File | Purpose | Non-Negotiable? |
|------|---------|----------------|
| `avatars/technology/android-kotlin/manifest.yaml` | Stack config, Kotlin 1.9+, Gradle, MockK, Turbine, Hilt, law specializations | — |
| `avatars/technology/android-kotlin/guidance.md` | Mols/Hauer/Cejas principles, full testing patterns, Compose + Flow, fastlane pipeline, security | — |
| `examples/ENG-4.1-atomic-tdd.md` | JUnit 5 + MockK TDD cycle; Philipp Hauer idioms; Turbine for Flow; Hilt injection | ⛔ NON-NEGOTIABLE |
| `examples/ENG-6.1-security.md` | ProGuard/R8, Network Security Config, Play Integrity, no secrets in code, Kotlin coroutine safety | ⛔ NON-NEGOTIABLE |
| `examples/ENG-6.4-data-protection.md` | Android Keystore at-rest, EncryptedSharedPreferences, certificate pinning, no PII in Logcat | ⛔ NON-NEGOTIABLE |
| `examples/ENG-6.7-audit-trail.md` | fastlane supply + versionCode CI audit chain, structured operation logging, audit spy test | ⛔ NON-NEGOTIABLE |
| `examples/ENG-3.1-complexity.md` | Kotlin cyclomatic complexity limits, ViewModel action complexity, use-case extraction | — |
| `examples/ENG-3.2-immutability.md` | Kotlin `val` preference, data class + copy(), `@Immutable` Compose, sealed class state | — |
| `examples/ENG-2.2-layers.md` | Domain / Data / Presentation; zero Android imports in domain; repository pattern | — |

## Files to Modify

| File | Change |
|------|--------|
| `avatars/index.yaml` | Add `avatar-android-kotlin` entry |
| `avatars/AVATAR-RAG-INDEX.yaml` | Add `android_kotlin` under `technology_avatars` |
| `avatars/technology/mobile-native/manifest.yaml` | Add Android split notice (iOS notice already added) |
| `avatars/technology/mobile-native/guidance.md` | Add Android split notice banner |
| `tools/rag-eval/test-cases/avatars.yaml` | Add tc-av-020..023 for Android Kotlin |

## Files to Deprecate (after this avatar ships)

| File | Action |
|------|--------|
| `avatars/technology/mobile-native/` | Archive to `hangar-ai-specs/archive/` — fully superseded by `ios-swift` + `android-kotlin` |

---

## Law Coverage

| Law | ⛔ Non-Neg? | Android Specialization | Example File |
|-----|-----------|----------------------|-------------|
| **ENG-4.1** Atomic TDD Law | ⛔ YES | JUnit 5 backtick names, MockK, Turbine, one test per RED-GREEN-REFACTOR cycle | `examples/ENG-4.1-atomic-tdd.md` |
| **ENG-6.1** Security by Design | ⛔ YES | ProGuard/R8, Network Security Config, Play Integrity API, no secrets in code, no PII in Logcat | `examples/ENG-6.1-security.md` |
| **ENG-6.4** Data Protection Law | ⛔ YES | Android Keystore at-rest, EncryptedSharedPreferences, certificate pinning, data classification | `examples/ENG-6.4-data-protection.md` |
| **ENG-6.7** Audit Trail Law | ⛔ YES | fastlane `increment_version_code` + Play Store traceable to commit SHA; structured operation logging | `examples/ENG-6.7-audit-trail.md` |
| **ENG-11.1** Hangar SDD Law | ⛔ YES | Every Android project adopting the constitution must include `hangar-ai-specs/`; in manifest | — |
| **ENG-4.2** Test Pyramid | — | Android pyramid: JVM unit (MockK, ≥70%) > Robolectric (integration) > Espresso/Compose UI (≤10%) | — |
| **ENG-3.1** Complexity Limits | — | Kotlin cyclomatic complexity ≤10; ViewModel action ≤5; Android Lint `CyclomaticComplexity` rule | `examples/ENG-3.1-complexity.md` |
| **ENG-3.2** Immutability Law | — | `val` preference; `data class` + `.copy()` for mutations; `@Immutable` Compose; sealed class UI state | `examples/ENG-3.2-immutability.md` |
| **ENG-2.2** Layered Architecture | — | Domain (zero Android) / Data (repo impl) / Presentation (ViewModel + Compose) | `examples/ENG-2.2-layers.md` |

---

## Acceptance Criteria

- [ ] `aa-constitution-lint` passes 0 failures after all files created
- [ ] RAG eval overall score ≥ 85% with android-kotlin test cases passing
- [ ] All 4 non-negotiable law example files exist with COMPLIANT + VIOLATION Swift examples
- [ ] `avatars/index.yaml` contains `avatar-android-kotlin`
- [ ] `AVATAR-RAG-INDEX.yaml` contains `android_kotlin` with all 9 example files referenced
- [ ] `mobile-native` has Android split notice matching iOS split notice style
- [ ] Proposal archived to `hangar-ai-specs/archive/android-kotlin-avatar/` on completion
- [ ] `mobile-native` avatar deprecated and archived on completion
