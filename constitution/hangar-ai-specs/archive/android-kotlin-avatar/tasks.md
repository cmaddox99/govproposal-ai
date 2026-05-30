# Tasks: Android Kotlin Avatar

**Proposal:** android-kotlin-avatar  
**Status:** IN PROGRESS

---

## Phase 1: Core Avatar Files

- [ ] Create `avatars/technology/android-kotlin/manifest.yaml`
  - Kotlin 1.9+, Jetpack Compose, JUnit 5 + MockK + Turbine, Hilt, Gradle
  - fastlane lanes (test, build, supply)
  - Law specializations: ENG-4.1, ENG-4.2, ENG-3.1, ENG-3.2, ENG-2.2, ENG-6.1, ENG-6.4, ENG-6.7
  - Jeroen Mols / Philipp Hauer / Fernando Cejas / NiA references
  - Project structure: app / core / feature / data modules

- [ ] Create `avatars/technology/android-kotlin/guidance.md`
  - Jeroen Mols "everything can be tested" manifesto and isolation philosophy
  - Philipp Hauer Kotlin testing idioms (backtick names, @Nested, @TestInstance(PER_CLASS))
  - Fernando Cejas Clean Architecture layers (domain / data / presentation)
  - Google Now in Android as living reference
  - Full MockK patterns (coEvery, coVerify, slot, relaxed, spyk)
  - Full Turbine patterns (awaitItem, expectMostRecentItem, cancelAndConsumeRemainingEvents)
  - @HiltViewModel MVVM + StateFlow + Compose pattern
  - Hilt test injection (@HiltAndroidTest, @UninstallModules, @BindValue)
  - fastlane pipeline (test, bundle, supply, increment_version_code)
  - Security by design (ProGuard, Network Security Config, Android Keystore)
  - Android test pyramid (JVM unit → Robolectric → Espresso/Compose UI)
  - Commands: ./gradlew test, connectedAndroidTest, bundle exec fastlane

## Phase 2: Non-Negotiable Law Examples (required for lint)

- [ ] Create `avatars/technology/android-kotlin/examples/ENG-4.1-atomic-tdd.md`
  - Philipp Hauer Kotlin idioms: backtick names, @Nested, @TestInstance
  - RED-GREEN-REFACTOR cycle with JUnit 5 + MockK
  - Turbine Flow assertion pattern
  - Hilt injection in tests
  - COMPLIANT / VIOLATION examples

- [ ] Create `avatars/technology/android-kotlin/examples/ENG-6.1-security.md`
  - ProGuard/R8 minimum rules
  - Network Security Config XML (no cleartext, pinning config)
  - Play Integrity API attestation check pattern
  - No API keys or secrets in code (BuildConfig / env injection)
  - COMPLIANT / VIOLATION examples

- [ ] Create `avatars/technology/android-kotlin/examples/ENG-6.4-data-protection.md`
  - Android Keystore key generation and use
  - EncryptedSharedPreferences pattern (Jetpack Security)
  - Certificate pinning via OkHttp CertificatePinner or Network Security Config
  - No PII in Logcat (custom redacting type, BuildConfig.DEBUG guard)
  - Data classification table for Android
  - COMPLIANT / VIOLATION examples

- [ ] Create `avatars/technology/android-kotlin/examples/ENG-6.7-audit-trail.md`
  - fastlane increment_version_code + supply CI audit chain
  - Structured AuditEvent data class + audit logger with spy test
  - Play Store release notes with commit SHA
  - COMPLIANT / VIOLATION examples

## Phase 3: Additional Law Examples

- [ ] Create `avatars/technology/android-kotlin/examples/ENG-3.1-complexity.md`
  - Kotlin cyclomatic complexity ≤10 per function
  - ViewModel action method ≤5 preferred
  - Android Lint CyclomaticComplexity rule
  - Use-case extraction pattern

- [ ] Create `avatars/technology/android-kotlin/examples/ENG-3.2-immutability.md`
  - val over var preference
  - data class + .copy() for mutations
  - @Immutable / @Stable for Compose
  - Sealed class for UI state (immutable state machine)
  - StateFlow with private MutableStateFlow

- [ ] Create `avatars/technology/android-kotlin/examples/ENG-2.2-layers.md`
  - Domain layer: zero Android imports, use-case interfaces, repository protocols
  - Data layer: repository implementations, Room DAOs, Retrofit services
  - Presentation layer: @HiltViewModel, StateFlow, Compose
  - Dependency rule diagram
  - COMPLIANT / VIOLATION examples

## Phase 4: Registry + mobile-native Updates

- [ ] Update `avatars/index.yaml` — add `avatar-android-kotlin` entry
- [ ] Update `avatars/AVATAR-RAG-INDEX.yaml` — add `android_kotlin` under `technology_avatars`
- [ ] Update `avatars/technology/mobile-native/manifest.yaml` — add Android split notice
- [ ] Update `avatars/technology/mobile-native/guidance.md` — add Android split notice banner
- [ ] Add tc-av-020..023 to `tools/rag-eval/test-cases/avatars.yaml`

## Phase 5: Verify + Deprecate mobile-native

- [ ] Run `aa-constitution-lint .` → 0 failures
- [ ] Run RAG eval → overall PASS, android-kotlin Avatar Selection passing
- [ ] Archive `mobile-native` avatar to `hangar-ai-specs/archive/mobile-native-deprecated/`
- [ ] Remove `mobile-native` from `avatars/index.yaml` and `AVATAR-RAG-INDEX.yaml`
- [ ] Commit and push

## Progress Summary

- Completed: 0/20
- In progress: 0
- Remaining: 20
