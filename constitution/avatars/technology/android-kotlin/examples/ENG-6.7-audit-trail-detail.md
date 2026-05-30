---
law_id: ENG-6.7
avatar: android-kotlin
non_negotiable: true
---

# ENG-6.7: Audit Trail Examples for Android (Kotlin)

> **Law:** All sensitive operations SHALL be logged with immutable audit records. Audit records MUST capture: who, what, when, where, result, and context.

---

## Android Audit Trail Architecture

Two levels of audit trail are required:

1. **Build pipeline** — every build is traced to a commit SHA via Gradle `-PbuildNumber` and a CI-written build manifest
2. **Runtime operations** — sensitive in-app actions emit structured `AuditEvent`s to the AA observability platform (server-side, not Logcat)

---

## COMPLIANT: Build Pipeline Audit Chain (Gradle + CI)

```bash
# CI build script (buildall.sh pattern — no fastlane in AA Android repo)
./gradlew app:assembleRelease \
  --no-daemon \
  -Papp.isJenkins=true \
  -PbuildNumber=$BUILD_NUMBER \
  -Papp.writeToRemoteCache=true

# versionCode is set in app/build.gradle from -PbuildNumber, ensuring
# each CI run produces a unique, monotonically increasing versionCode
```

```groovy
// app/build.gradle — versionCode sourced from CI property
def buildNumber = project.findProperty('buildNumber')?.toInteger() ?: 1
android {
    defaultConfig {
        versionCode buildNumber   // AUDIT: every build uniquely identified
        versionName "1.0.${buildNumber}"
    }
}
```

```yaml
# .github/workflows/android-ci.yml
- name: Write build manifest (ENG-6.7)
  run: |
    echo "BUILD_NUMBER=${{ github.run_number }}" >> build-manifest.txt
    echo "COMMIT_SHA=${{ github.sha }}" >> build-manifest.txt
    echo "TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> build-manifest.txt

- name: Archive build artifacts (ENG-6.7)
  uses: actions/upload-artifact@v4
  with:
    name: build-${{ github.sha }}
    path: |
      app/build/outputs/bundle/release/*.aab
      app/build/outputs/mapping/release/mapping.txt
      app/build/reports/
    retention-days: 90
```

---

## COMPLIANT: Runtime Sensitive Operation Logging

```kotlin
// Audit event structure — matches ENG-6.7 required fields
data class AuditEvent(
    val eventId: String = UUID.randomUUID().toString(),  // WHO + WHAT identifier
    val operation: String,          // WHAT: "booking.confirm", "payment.submit"
    val actorId: String,            // WHO: anonymised user ID (not name/email)
    val timestamp: Instant = Instant.now(),  // WHEN
    val sessionId: String,          // WHERE: session context
    val deviceModel: String = Build.MODEL,   // WHERE: "Pixel 6"
    val result: AuditResult,        // RESULT: success / failure / denied
    val resourceId: String? = null, // CONTEXT: booking ref, flight number, etc.
    val errorCode: String? = null   // CONTEXT: error code on failure
)

enum class AuditResult { SUCCESS, FAILURE, DENIED }

// Audit logger — emits to server-side observability (NOT Logcat)
interface AuditLogger {
    suspend fun log(event: AuditEvent)
}

class RemoteAuditLogger @Inject constructor(
    private val auditApi: AuditApi
) : AuditLogger {
    override suspend fun log(event: AuditEvent) {
        // Fire-and-forget — non-blocking; server stores the immutable record
        try { auditApi.emit(event) } catch (_: Exception) { /* non-critical */ }
    }
}

// Usage in booking confirmation use case
class ConfirmBookingUseCase @Inject constructor(
    private val bookingRepository: BookingRepository,
    private val auditLogger: AuditLogger,
    private val session: SessionContext
) {
    suspend operator fun invoke(booking: Booking): Result<Confirmation> {
        val startTime = Instant.now()
        return runCatching {
            val confirmation = bookingRepository.confirm(booking)
            auditLogger.log(AuditEvent(
                operation = "booking.confirm",
                actorId = session.anonymisedUserId,
                timestamp = startTime,
                sessionId = session.id,
                result = AuditResult.SUCCESS,
                resourceId = confirmation.bookingReference
            ))
            confirmation
        }.onFailure { error ->
            auditLogger.log(AuditEvent(
                operation = "booking.confirm",
                actorId = session.anonymisedUserId,
                timestamp = startTime,
                sessionId = session.id,
                result = AuditResult.FAILURE,
                resourceId = booking.flightNumber,
                errorCode = error::class.simpleName
            ))
        }
    }
}
```

---

## COMPLIANT: Testing the Audit Trail (ENG-4.1 + ENG-6.7)

```kotlin
import io.mockk.coVerify
import io.mockk.mockk
import io.mockk.slot
import kotlinx.coroutines.test.runTest
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class ConfirmBookingUseCaseAuditTest {

    @get:Rule
    val coroutineRule = TestCoroutineRule()

    private val bookingRepository = mockk<BookingRepository>()
    private val auditLogger = mockk<AuditLogger>(relaxed = true)
    private val session = FakeSessionContext(anonymisedUserId = "user-anon-abc")
    private lateinit var sut: ConfirmBookingUseCase

    @Before
    fun setUp() {
        sut = ConfirmBookingUseCase(bookingRepository, auditLogger, session)
    }

    @Test
    fun `confirming booking emits success audit event with booking reference`() = runTest {
        val booking = Booking.stub()
        val confirmation = Confirmation.stub(bookingReference = "AA-XYZ-123")
        coEvery { bookingRepository.confirm(booking) } returns confirmation

        val slot = slot<AuditEvent>()
        coEvery { auditLogger.log(capture(slot)) } just runs

        sut(booking)

        val event = slot.captured
        assertEquals("booking.confirm", event.operation)
        assertEquals(AuditResult.SUCCESS, event.result)
        assertEquals("AA-XYZ-123", event.resourceId)
        assertEquals("user-anon-abc", event.actorId)
        assertTrue(event.eventId.isNotBlank())
    }

    @Test
    fun `confirming booking on repository failure emits failure audit event`() = runTest {
        val booking = Booking.stub()
        coEvery { bookingRepository.confirm(any()) } throws IOException("timeout")

        val slot = slot<AuditEvent>()
        coEvery { auditLogger.log(capture(slot)) } just runs

        sut(booking)

        assertEquals(AuditResult.FAILURE, slot.captured.result)
        assertEquals("IOException", slot.captured.errorCode)
    }
}
```

---

## VIOLATION: Missing or Mutable Audit Records

```kotlin
// BAD: no audit event on payment — most sensitive operation has no record
suspend fun submitPayment(payment: Payment): Receipt {
    // VIOLATION: payment processed with no audit trail
    return paymentService.submit(payment)
}

// BAD: audit written to Logcat — mutable, not immutable, accessible to third parties
fun bookFlight(booking: Booking) {
    // VIOLATION: Logcat is not an immutable audit record
    Log.i("Booking", "Booking submitted: ${booking.flightNumber}")
    api.post("/book", booking)
}

// BAD: versionCode not sourced from CI — every build has same versionCode
android {
    defaultConfig {
        versionCode 1  // ❌ hardcoded — no audit trail between builds
    }
}

// BAD: audit event missing required fields
data class BadAuditEvent(
    val action: String,     // ❌ missing: actorId, sessionId, timestamp, result, resourceId
    val success: Boolean
)
```

**Why ENG-6.7 violated:** Logcat is mutable (log rotation, device wipe, third-party access). No audit on payment means zero post-incident forensics. A build without an incremented `versionCode` cannot be traced from Play Store back to a commit, breaking the CI/CD audit chain. Audit events missing required fields are non-compliant with the "who, what, when, where, result, context" mandate.
