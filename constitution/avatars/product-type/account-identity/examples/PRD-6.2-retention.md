---
avatar: avatar-account-identity
law_id: PRD-6.2
law_title: "Retention Over Acquisition"
file_type: example
---

# PRD-6.2 Retention Over Acquisition — Example

## Law Summary

**PRD-6.2** requires that product investment prioritizes retaining and deepening engagement with existing users before acquiring new ones. When a known retention or conversion problem exists, adding new acquisition features ahead of fixing that problem violates this law.

---

## ✅ COMPLIANT Example: Fix Guest-to-Authenticated Conversion Before Adding New Sign-In Methods

### The Retention Problem

Analytics on the `GuestCache` → `AccountManager` transition reveal a significant conversion gap:

- **62% of app sessions begin in guest state** (`GuestEndPoint` initializes a guest session, `AAFeatureGuestUser` is active).
- Of those guest sessions, **only 23% result in a successful authenticated session** within the same app session — the remaining 77% never trigger `AccountManager` authentication.
- Among guests who do authenticate, **booking frequency is 3.4× higher** in the 30 days following first authentication compared to users who remain in guest state.

**Friction points identified in the `GuestCache` → `AccountManager` funnel:**
1. The sign-in prompt is shown only once per app session; dismissed guests do not see a second prompt even after high-intent actions (e.g., reaching checkout).
2. The sign-in screen rendered via `MyAccountBridgedWebViewController` has a 4.6% error rate — one in twenty-two sign-in attempts fails before the user even submits credentials.
3. Password recovery is not surfaced on the sign-in screen; users who fail `UserAccountEndpoint` credential validation see only a generic error with no recovery path.

### Compliant Investment Decision

**Before building any new sign-in method, fix the three identified funnel friction points:**

1. Show a re-authentication prompt after high-intent guest actions (post-checkout-attempt).
2. Instrument and reduce the `MyAccountBridgedWebViewController` error rate for the sign-in screen.
3. Add a visible password recovery link on `UserAccountEndpoint` credential failure.

**Projected impact:** Modeling the 77% non-conversion rate and 3.4× booking lift suggests that a 10-point improvement in guest-to-authenticated conversion would recover more booking revenue than adding social login to a fully-converting user base.

**Measurement:** Track `GuestCache` session start → `AccountManager` authenticated session confirmed conversion rate, segmented by funnel intervention applied.

---

## ❌ VIOLATION Example: Add Social Login Before Fixing Conversion Funnel

> "Let's add social login (Facebook, Google) to make it easier for new users to sign up. This will bring more users into the authenticated funnel."

### Why This Violates PRD-6.2

1. **Acquisition before retention.** The primary problem is not that new users lack sign-in options — it is that 77% of existing guest users are not converting to authenticated accounts through the current flow. Adding Facebook and Google sign-in does not address any of the three identified friction points.

2. **The funnel is broken, not missing.** Social login assumes the conversion problem is "sign-in method mismatch." The data shows the actual problems are error rates, prompt frequency, and recovery path absence in the existing `MyAccountBridgedWebViewController` + `UserAccountEndpoint` flow. Adding a new entry point to a broken funnel creates a third path that inherits the same downstream friction.

3. **Opportunity cost is high.** Engineering effort required to integrate OAuth-based social login — including `AccountManager` identity federation, `UserAccountCache` session mapping, and `devicevalidation-ios` device trust extension — is substantial. That same effort applied to the three retention friction points would produce measurable conversion lift faster.

4. **3.4× booking lift is the existing retention signal.** The data already shows that authenticated users outperform guest users by 3.4× on bookings. The highest-leverage move is converting more of the 62% guest-session users — all of whom already have the app — not acquiring net-new users who may never convert.

**The compliant path:** Measure and fix the `GuestCache` → `AccountManager` conversion funnel. Set a conversion rate target (e.g., 35% within 90 days). Only after reaching that target does social login become a candidate investment.

---

## Application Notes for account-identity

- The `GuestCache` / `GuestEndPoint` / `AAFeatureGuestUser` stack represents the entry point for a majority of app sessions. Any investment in new sign-in mechanisms must first demonstrate that the existing guest-to-authenticated conversion funnel is performing at an acceptable rate.
- `MyAccountBridgedWebViewController` error rates are the most immediate lever on funnel conversion — every web-bridge error is a potential conversion loss. Monitor error rates as a leading indicator before PRD-6.2 investment decisions.
