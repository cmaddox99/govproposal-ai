# Journey: Account Sign-In (Authenticated vs. Guest)
# Avatar: avatar-account-identity | Law: PRD-2.5 Discovery Stage-Gate Law
# Grounded in: account-ios analysis — 358 source files, AmericanAccount framework
# Source modules: AccountManager, MyAccountBridgedWebViewController, UserAccountEndpoint, GuestCache

```yaml
journey:
  id: journey-account-sign-in
  name: Account Sign-In (Authenticated vs. Guest)
  persona: Returning AAdvantage member opening the app after 30-day absence
  laws: [PRD-2.5, PRD-1.2, BUS-4.3, BUS-7.1, BUS-9.3]
  source_evidence: account-ios source analysis (2026-04-30)
```

---

## Overview

This journey traces the full sign-in lifecycle for a returning AAdvantage member who has not used the app for 30 days. It covers app launch, session validation, cache consultation, sign-in screen rendering via the web-bridge architecture, credential submission, device trust validation, profile load, and navigation to the account hub.

This journey is the entry path for the majority of account-identity product work. Every feature that touches authentication — biometric login, device trust, guest conversion — flows through this sequence.

---

## Journey Steps

### Step 1 — App Launch: Session State Check
**Module:** `AAFeatureUserLoginObserver`

On app launch, `AAFeatureUserLoginObserver` evaluates whether a prior authenticated session is active or has expired. This is the first branch point: a live session bypasses the sign-in screen entirely; an expired or absent session triggers the cache consultation path.

**Product consideration (PRD-1.2):** Any investment in reducing sign-in friction must begin here — measuring what percentage of launches result in session miss vs. session hit. This is the top-of-funnel signal.

---

### Step 2 — Session Retrieval: AccountManager
**Module:** `AccountManager`, `AccountManager_Notifications`

`AccountManager` attempts to retrieve a valid session token. If a valid token exists, the user proceeds directly to account home. If the token is absent, expired, or invalid, `AccountManager` emits a session-expired notification via `AccountManager_Notifications` and initiates the cache consultation sequence.

**BUS-7.1 (Audit Trail):** Session validation outcomes — active, expired, invalidated — must be logged as authentication lifecycle events. Session expiry events are audit-relevant particularly when expiry is policy-triggered vs. user-initiated sign-out.

---

### Step 3 — Cache Consultation: GuestCache / UserAccountCache
**Modules:** `GuestCache`, `UserAccountCache`, `AccountCache`

On session miss, the app consults `UserAccountCache` and `AccountCache` for stored identity state. If a prior authenticated identity is found in cache, it is offered as a pre-fill for the sign-in screen. If no authenticated identity is found, `GuestCache` initializes a guest session via `GuestEndPoint`, and `AAFeatureGuestUser` activates the guest experience.

**Product consideration (PRD-6.2):** The branch where `GuestCache` activates instead of presenting sign-in is the primary conversion funnel gap. Users who land in guest state and are not re-prompted to authenticate are the 77% non-conversion population.

---

### Step 4 — Sign-In Screen Rendering: Web-Bridge
**Module:** `MyAccountBridgedWebViewController`, `MyAccountSpinnerController`, `MyAccountSpinnerView`

The sign-in screen is rendered via `MyAccountBridgedWebViewController`, a WKWebView wrapper. `MyAccountSpinnerController` and `MyAccountSpinnerView` manage the loading state while the web content initializes.

> ⚠️ **ENG-3.1 Architectural Risk:** The sign-in screen is a web-bridge surface. It has a 4.6% user-visible error rate — 2.3× higher than native screens — and a 1.8s longer median load time. Any product change to the sign-in screen UI requires joint product + engineering coordination and must be tracked in the ENG-3.1 risk register. Native instrumentation does not capture field-level interaction on web-bridge screens.

**BUS-4.3 (PII):** The sign-in screen collects AAdvantage number and password — identity credentials that are personal data. The web-bridge rendering layer must maintain TLS session continuity; credentials must never be logged or cached in plaintext in `UserAccountCache`.

---

### Step 5 — Credential Submission: Authentication
**Module:** `UserAccountEndpoint`

The user submits credentials. `UserAccountEndpoint` sends the authentication request to the backend. On success, a session token is returned. On failure, an error response is returned and displayed. Credential validation errors should surface a password recovery path; network errors should provide a retry affordance.

**BUS-7.1 (Audit Trail):** Every credential submission attempt — success, credential failure, network failure, account lockout — must be captured as an authentication event with timestamp and outcome. This is required for security audit and anomaly detection.

**BUS-9.3 (Breach Notification):** If `UserAccountEndpoint` returns indicators of credential compromise (e.g., locked account due to brute force detection), the breach notification protocol must be triggered. Account lockout events are in-scope for BUS-9.3 notification assessment.

---

### Step 6 — Device Trust Check: devicevalidation-ios
**Module:** `devicevalidation-ios` (device trust/validation, device registration, biometric authentication support)

After credential authentication, `devicevalidation-ios` evaluates whether the current device is registered as a trusted device for this account. If trusted, the session proceeds without additional verification. If the device is unregistered, the user may be prompted to register or to complete an additional verification step.

**PRD-2.5 (Stage-Gate):** Any change to the device trust check logic — new trust signals, modified registration criteria, reduced re-authentication frequency — requires a Stage A problem validation before engineering work begins.

**BUS-4.3 (PII):** Device identifiers used in trust evaluation are linked to an authenticated identity and constitute personal data. Device registration data is subject to data subject access and deletion rights.

---

### Step 7 — Profile Load: Account Data Assembly
**Modules:** `UserAccountInfo`, `AAdvantageUser_Summaries`, `AccountInfoActor`, `SummariesEndpoint`

Following authentication and device trust confirmation, `AccountInfoActor` orchestrates profile data retrieval. `UserAccountInfo` loads the core account record. `AAdvantageUser_Summaries` loads the AAdvantage member identifier and summary data (note: miles, tier status, and benefits are owned by **loyalty-aadvantage** — this step loads identifiers only, not loyalty rewards data).

**BUS-4.3 (PII):** Profile load assembles PII — name, contact information, AAdvantage number. This data must be handled per data classification requirements and must not be logged or cached without authorization.

---

### Step 8 — Account Home: Navigation
**Module:** `MyAccountNavigationManager`

`MyAccountNavigationManager` routes the authenticated user to the account hub. From account home, users can access profile editing, secure traveler details, and loyalty summary links (which hand off to loyalty-aadvantage surfaces).

---

## Law Applications Summary

| Law | Application in This Journey |
|---|---|
| PRD-2.5 | Stage-gate required for any change to device trust check logic (Step 6) or session expiry policy (Step 2) |
| PRD-1.2 | Authentication failure rate (Step 5) and session miss rate (Step 1–2) are the primary problem signals |
| BUS-4.3 | Credentials (Step 5), device identifiers (Step 6), and profile data (Step 7) are all PII subject to data subject rights |
| BUS-7.1 | Authentication events at Steps 2, 5, and 6 must all be captured in the audit trail |
| BUS-9.3 | Account lockout and credential compromise signals at Step 5 trigger breach notification assessment |

---

## Web-Bridge Risk Register Entry

> **Surface:** Sign-In Screen (Step 4)
> **Module:** `MyAccountBridgedWebViewController`
> **Risk Class:** ENG-3.1 — Web-bridge coupling
> **Metrics:** 4.6% error rate, 3.1s median load time, limited field-level instrumentation
> **Coordination Required:** Joint product + engineering sign-off for any sign-in screen UI change
