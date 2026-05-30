```yaml
use_case:
  id: uc-account-biometric-login
  name: Biometric Login (Face ID / Touch ID)
  jtbd: "When a returning AAdvantage member opens the app and has previously enrolled in biometric
    authentication, they need to sign in with Face ID or Touch ID so they can access their account
    without typing a password."
  actor: Enrolled AAdvantage Member
  laws: [PRD-1.2, PRD-5.1, BUS-4.3, BUS-7.1, BUS-9.3]
  source_modules:
    - devicevalidation-ios (device trust/validation, biometric authentication support, device registration)
    - AccountManager
    - UserAccountEndpoint
    - AAFeatureUserLoginObserver
```

---

# Use Case: Biometric Login (Face ID / Touch ID)

**Avatar:** avatar-account-identity
**Source:** devicevalidation-ios (22 Swift files) — device trust/validation, biometric authentication support, device registration

---

## Problem Statement (PRD-1.2)

34% of returning AAdvantage members fail password-based authentication on their first attempt when re-engaging with the app after a 30-day absence. 18% of those users abandon the sign-in flow entirely. `AccountManager` session telemetry and `AAFeatureUserLoginObserver` event data confirm the failure pattern is concentrated in the 30+ day re-engagement cohort.

The hypothesis: biometric login (Face ID / Touch ID) via `devicevalidation-ios` eliminates the password recall failure mode for enrolled users, reducing first-attempt failure and sign-in abandonment.

---

## Scope

This use case governs:
- Biometric enrollment: a user registers Face ID or Touch ID as an authentication method, backed by `devicevalidation-ios` device registration.
- Biometric sign-in: using enrolled biometrics to authenticate via the `devicevalidation-ios` biometric authentication support layer.
- Fallback to password: when biometric authentication fails or is unavailable, the flow falls back to credential-based sign-in via `UserAccountEndpoint`.
- Device registration state: a device with biometric enrollment is registered as a trusted device in `devicevalidation-ios`.

This use case does **not** govern PIN-based fallback (outside scope per PRD-5.1 MVP discipline), multi-device biometric management, or biometric data storage (managed by iOS Secure Enclave, not application code).

---

## Enrollment Flow

1. **Eligibility check:** `devicevalidation-ios` device trust layer evaluates whether the current device supports biometric authentication (Face ID or Touch ID capability present and not restricted by device policy).
2. **Enrollment prompt:** After a successful password-based sign-in, an enrollment prompt is presented to eligible users who have not yet enrolled. This is not shown on every sign-in — it is shown once per eligible device, per `devicevalidation-ios` enrollment state.
3. **Biometric consent:** User consents to biometric enrollment. Consent is logged as an authentication lifecycle event per BUS-7.1.
4. **Device registration:** `devicevalidation-ios` registers the device as biometric-enabled and linked to the authenticated `AccountManager` session. The device is recorded as a trusted device in the device registration store.
5. **Confirmation:** User sees enrollment confirmation. Subsequent sign-ins on this device will offer biometric authentication as the primary path.

---

## Sign-In Flow (Enrolled User)

1. **App launch:** `AAFeatureUserLoginObserver` detects an expired or absent session.
2. **Biometric check:** `devicevalidation-ios` device trust layer checks whether the current device has an active biometric enrollment linked to an account.
3. **Biometric prompt:** If enrolled, the OS biometric prompt (Face ID / Touch ID system sheet) is presented before the `MyAccountBridgedWebViewController` sign-in screen.
4. **Biometric result:**
   - **Success:** `devicevalidation-ios` issues a trust assertion. `AccountManager` establishes an authenticated session without credential submission to `UserAccountEndpoint`. Audit event logged (BUS-7.1).
   - **Failure (user cancels or biometric not recognized):** Fall back to credential sign-in via `UserAccountEndpoint` / `MyAccountBridgedWebViewController`. Biometric failure event logged (BUS-7.1).
   - **Failure (device biometric unavailable — e.g., too many failed attempts, device lockout):** Present password sign-in only. Device biometric lockout event logged (BUS-7.1). `devicevalidation-ios` enrollment state is not cleared — user can re-enroll after device lockout resolves.

---

## Security Considerations (BUS-4.3)

**Biometric data is sensitive personal data.** Under BUS-4.3, biometric identifiers receive the highest data classification level. The following requirements apply:

- **No application-layer biometric storage.** Face ID and Touch ID data is managed exclusively by the iOS Secure Enclave. `devicevalidation-ios` stores only a device registration token, not biometric templates.
- **Data subject access right:** Users can request a record of their biometric enrollment registrations. `devicevalidation-ios` device registration records must be producible in response to a data subject access request.
- **Right to deletion:** Users can unenroll biometric authentication at any time. Unenrollment must delete the `devicevalidation-ios` device registration record associated with biometric enrollment. This does not affect the device's registered-device status for non-biometric trust flows.
- **Consent:** Biometric enrollment requires explicit user consent. Consent must be logged (BUS-7.1) and must be re-obtained if biometric authentication scope changes.

---

## Audit Trail Requirements (BUS-7.1)

Every biometric-related event must be captured in the authentication audit log:

| Event | Log Required |
|---|---|
| Biometric enrollment initiated | Yes — with timestamp, device ID (anonymized), account identifier |
| Biometric enrollment completed | Yes |
| Biometric enrollment declined by user | Yes |
| Biometric sign-in success | Yes — with session token issuance |
| Biometric sign-in failure (unrecognized) | Yes — with failure count |
| Biometric sign-in failure (device lockout) | Yes |
| Biometric unenrollment by user | Yes |
| Device registration linked to biometric enrollment | Yes |

---

## Breach Notification Scope (BUS-9.3)

Biometric authentication credentials, if compromised at the application or infrastructure layer, trigger the BUS-9.3 breach notification protocol. Applicable scenarios:

- Unauthorized access to `devicevalidation-ios` device registration records that could be used to impersonate a biometric-enrolled user.
- `AccountManager` session token issuance without a valid biometric assertion (bypass vulnerability).

Note: Compromise of raw biometric data (Face ID templates) at the Secure Enclave level is an OS-level incident, not an application-layer incident — but application-layer incidents that enable account takeover via the biometric path are in scope for BUS-9.3.

---

## MVP Scope (PRD-5.1)

**MVP:** Face ID and Touch ID enrollment and sign-in for returning enrolled users on supported devices. Single device only. No multi-device enrollment management UI. No PIN fallback. Measure: biometric sign-in success rate, password fallback rate, and 30-day re-authentication frequency for enrolled vs. non-enrolled cohorts.

**Expand scope only after:** MVP data confirms biometric sign-in reduces first-attempt failure rate in the 30+ day re-engagement cohort.
