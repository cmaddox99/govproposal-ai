---
law_id: ENG-6.7
avatar: android-kotlin
non_negotiable: true
---

# ENG-6.7 — Audit Trail (Android Kotlin)

> fastlane monotonic versionCode per CI run. Play Store build traceable to git commit SHA.

## COMPLIANT — fastlane Audit Chain

```ruby
# fastlane/Fastfile
lane :beta do
  # AUDIT: monotonic versionCode = unique build identifier per CI run
  increment_version_code(
    gradle_file_path: "app/build.gradle.kts",
    version_code: ENV["BUILD_NUMBER"].to_i
  )
  gradle(task: "bundle", build_type: "Release", print_command: false)  # ENG-6.1: never log signing args
  # AUDIT: version_name contains commit SHA → Play Store build traceable to commit
  supply(
    track: "internal",
    aab: lane_context[SharedValues::GRADLE_AAB_OUTPUT_PATH],
    version_name: "#{ENV['BUILD_NUMBER']}.0 (#{ENV['GITHUB_SHA'][0,8]})",
    skip_upload_apk: true
  )
end
```

Chain: `Play Store build ← AAB artifact ← CI run (BUILD_NUMBER) ← git commit (GITHUB_SHA)`

## COMPLIANT — Runtime Audit Event

```kotlin
data class AuditEvent(
    val operation: String,      // "booking.confirm", "checkin.submit"
    val entityId: String,
    val result: AuditResult,    // SUCCESS | FAILURE
    val errorMessage: String? = null,
    val timestampMs: Long = System.currentTimeMillis()
)

class PlaceOrderUseCase @Inject constructor(
    private val repository: OrderRepository,
    private val audit: AuditLogger         // emits to server-side sink, not Logcat
) {
    suspend operator fun invoke(orderId: OrderId): Result<Order> = runCatching {
        val order = repository.getOrder(orderId) ?: throw OrderNotFoundException(orderId)
        val placed = order.place()
        repository.save(placed)
        audit.log(AuditEvent("order.place", orderId.value, AuditResult.SUCCESS))
        placed
    }.onFailure { audit.log(AuditEvent("order.place", orderId.value, AuditResult.FAILURE, it.message)) }
}
```

## VIOLATION

```kotlin
// ❌ No build traceability — versionCode hardcoded, not CI-incremented
android { defaultConfig { versionCode = 42 } }

// ❌ Audit to Logcat only — not observable in production
Log.i("BookingAudit", "Order placed: $orderId")
```

> Full detail with Gradle versionCode automation: see `ENG-6.7-audit-trail-detail.md`.
