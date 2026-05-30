# mobile-native Deprecated

This avatar has been split into two dedicated platform avatars:

- **iOS**: `avatars/technology/ios-swift/` (avatar ID: `avatar-ios-swift`)
- **Android**: `avatars/technology/android-kotlin/` (avatar ID: `avatar-android-kotlin`)

## Why

The original `mobile-native` avatar mixed iOS and Android concerns into a single file, making it impossible to give platform-specific guidance on:
- Distinct testing frameworks (XCTest vs JUnit 5 + MockK)
- Distinct security patterns (Keychain vs Android Keystore; ATS vs Network Security Config)
- Distinct CI/CD pipelines (fastlane pilot vs fastlane supply)
- Distinct architecture idioms (Swift 6 `@MainActor` vs Hilt + ViewModel)

## Migration

| Old reference | New reference |
|---------------|---------------|
| `avatar: mobile-native` | `avatar: ios-swift` (iOS) or `avatar: android-kotlin` (Android) |
| `mobile_native` RAG key | `ios_swift` or `android_kotlin` |

## Archived

Archived: 2026-04-08
Proposal: `hangar-ai-specs/changes/android-kotlin-avatar/PROPOSAL.md`
