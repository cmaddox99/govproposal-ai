# Account Identity & Profile Management — Avatar Guidance

## What This Avatar Owns

**account-identity** governs the complete identity lifecycle within the American Airlines iOS app:

- **Authentication**: credential sign-in, biometric login (Face ID / Touch ID), session management, sign-out, session expiry and refresh — via `AccountManager`, `UserAccountEndpoint`, and `AAFeatureUserLoginObserver`.
- **Guest vs. Authenticated State**: guest session creation (`GuestCache`, `GuestEndPoint`, `AAFeatureGuestUser`), and the conversion funnel from guest to authenticated (`GuestCache` → `AccountManager` handoff).
- **Account Profile Management**: viewing and editing contact information, travel preferences, and secure traveler details — via `AccountProfileEndpoint`, `SecureTravelerEndpoint`, `SecureTravelerSubmitEndpoint`, `UserAccountInfo`, and `AccountInfoActor`.
- **Device Trust & Validation**: device registration, device trust checks, and biometric enrollment support — via `devicevalidation-ios` (22 Swift files).
- **Session Cache**: `UserAccountCache`, `AccountCache`, and `AccountInfoActor` for local state management.

## What This Avatar Does NOT Own

- **AAdvantage Loyalty**: miles balances, status tiers, upgrade eligibility, benefits — all owned by **loyalty-aadvantage**. The AAdvantage member number appears here only as an account identifier.
- **Booking flows**: post-authentication booking and trip management are owned by **booking-core**.
- **Promotions, Summaries, Activity feeds**: `PromotionsEndpoint`, `SummariesEndpoint`, and `ActivityEndpoint` exist in the `account-ios` framework but feed into loyalty and booking surfaces.

## Web-Bridge Architecture Risk (ENG-3.1)

`MyAccountBridgedWebViewController` is a **WKWebView wrapper** — the majority of account screens (sign-in, profile editing) are rendered as web content, not native SwiftUI or UIKit views. This creates an **ENG-3.1 architectural risk**:

- Native app instrumentation does not capture web-bridge screen performance at the same fidelity as native screens.
- Web-bridge screens show 2.3× higher error rates and 1.8s longer median load times than native equivalents.
- Any feature change touching a web-bridge screen requires joint product + engineering sign-off and must be tracked in the ENG-3.1 risk register.
- Migration from WKWebView to native must be evidence-backed per **PRD-1.5** — do not migrate without performance and error-rate data.

## Key Product Considerations

**Device Trust (devicevalidation-ios):** Device registration and trusted-device flows directly affect re-authentication friction. Validate the problem (do users actually experience re-auth friction?) before building new device trust features — PRD-2.5 stage-gate required.

**Biometric Login:** Biometric data is sensitive personal data under **BUS-4.3**. Enrollment, storage, and fallback flows must satisfy data subject rights. Every biometric auth event requires an audit trail entry per **BUS-7.1**.

**Profile PII:** Every field in `AccountProfileEndpoint` and `UserAccountInfo` is PII. New fields require data classification review. Users have rights to access, correct, and delete profile data (BUS-4.3). Account data is in-scope for breach notification under **BUS-9.3**.

**Guest Conversion:** `GuestCache` → `AccountManager` is a high-leverage funnel. Fix conversion friction before adding new authenticated-only features — PRD-6.2 retention principle.
