---
avatar: android-kotlin
version: "1.3.0"
skills:
  - 06-atomic-tdd
  - 07-vertical-slice-dev
  - 08-code-review
  - 25-ux-design
---

# Android / Kotlin Guidance

> **Purpose:** Stack-specific agent behaviors for Android/Kotlin applications at AA — Jetpack Compose, Dagger 2, JUnit 4 + MockK, Gradle CI.

## Overview

Android Kotlin at AA is a 3,226-file / 289K LOC brownfield monorepo with MVVM + Clean Architecture,
Dagger 2 DI (Hilt migration pending), and JUnit 4 dominant testing. See `guidance-detail.md`.

## Non-Negotiable Laws

### ENG-4.1 — Atomic TDD Law
- **Requires:** Every Kotlin function written test-first; one RED-GREEN-REFACTOR cycle per function.
- **Violates:** Production code before a failing JUnit 4 test; batching multiple functions per commit.
- **Note:** JUnit 4 + MockK; backtick test names; Turbine for Flow assertions.

### ENG-6.1 — Security by Design Law
- **Requires:** No secrets in source; Play Integrity API for attestation; Network Security Config blocks cleartext.
- **Violates:** Hardcoded API keys in Kotlin source or `BuildConfig` checked into version control.
- **Note:** Inject secrets via CI environment variables; ProGuard/R8 minification required for release.

### ENG-6.4 — Data Protection Law
- **Requires:** PII stored only in Android Keystore or EncryptedSharedPreferences; no PII in Logcat.
- **Violates:** Credentials in plain `SharedPreferences`; logging user data without `BuildConfig.DEBUG` guard.
- **Note:** `androidx.security:security-crypto`; OkHttp `CertificatePinner` for certificate pinning.

### ENG-6.7 — Audit Trail Law
- **Requires:** Every release build traceable to a CI run, git commit, and versionCode increment.
- **Violates:** Manual builds without `-PbuildNumber`; releasing without a structured `AuditEvent` sink.
- **Note:** `./gradlew app:bundleRelease -PbuildNumber=$BUILD_NUMBER -Papp.isJenkins=true`.

## Key Patterns

- `val` over `var` · `data class + .copy()` · sealed interface UI state
- Use cases: `class ...UseCase { operator fun invoke(...) }` — zero Android imports in domain
- `RepositoryImpl @Inject constructor` in data; interface in domain

## Anti-Patterns to Avoid

- **God classes** — every decomposition of files >500 LOC requires an approved `PROPOSAL.md` (ENG-11.1)
- **Mixed reactive paradigms** — new code must use Coroutines/Flow only; do not add RxJava to new classes
- **Android imports in domain layer** — `android.*` imports in domain classes violate Clean Architecture
