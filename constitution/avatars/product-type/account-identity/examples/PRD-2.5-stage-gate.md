---
avatar: avatar-account-identity
law_id: PRD-2.5
law_title: "Discovery Stage-Gate Law"
file_type: example
---

# PRD-2.5 Discovery Stage-Gate Law — Example

## Law Summary

**PRD-2.5** requires that significant features pass through a structured discovery stage-gate before engineering commits to a solution. The gate sequence validates the problem, then the solution direction, before any production implementation begins. No stage may be skipped.

---

## ✅ COMPLIANT Example: Device Trust Feature (devicevalidation-ios)

### Feature Under Consideration

Add a "trusted device" flow powered by `devicevalidation-ios` that remembers verified devices and reduces re-authentication friction for returning users.

---

### Stage A — Problem Validation

**Question:** Do returning users actually experience re-authentication friction at a rate that justifies a device trust investment?

**Method:**
- Analyze `AccountManager` session telemetry to identify users who re-authenticate within a 60-day window. Segment by days-since-last-session.
- Measure re-authentication attempt counts per user per 60-day period using `AAFeatureUserLoginObserver` events.
- Identify what percentage of re-authentication events result in failure or abandonment.

**Success threshold for Stage A:** At least 25% of 30–60-day returning users encounter two or more re-authentication events per month, with an abandonment rate above 10%.

**Stage A Gate Decision:** Only if the above threshold is met does the team proceed to Stage B. If re-authentication friction is low, the device trust feature is deprioritized.

---

### Stage B — Solution Direction Validation

**Question:** Will a trusted-device model actually reduce re-authentication events, and is `devicevalidation-ios` the right mechanism?

**Method:**
- Prototype device registration flow with `devicevalidation-ios` in a limited internal build.
- Measure whether users who register a device show a measurable reduction in re-authentication prompts in the 30-day window following registration.
- Assess engineering feasibility: does `devicevalidation-ios` device registration integrate with `AccountManager` session state without requiring changes to `UserAccountEndpoint`?

**Success threshold for Stage B:** Prototype demonstrates ≥40% reduction in re-authentication prompts for registered-device users vs. control group.

---

### Stage C — Device Registration Prototype

**Scope:** Build a minimal device registration flow. Users can register one device. No multi-device management. No migration of existing sessions. Measure completion rate of the registration flow and reduction in re-authentication friction over 30 days.

**Gate Decision for Production:** Proceed to production only if Stage C prototype meets the Stage B success threshold in a real-user pilot.

---

## ❌ VIOLATION Example: Device Trust Feature (Stage-Gate Skipped)

> "Ship the trusted device feature to production. Device trust is a standard pattern — users obviously want to avoid re-authenticating. Let's build device registration in devicevalidation-ios and roll it out."

### Why This Violates PRD-2.5

1. **Problem validation skipped (Stage A).** "Users obviously want to avoid re-authenticating" is an assumption, not a finding. The actual re-authentication frequency and abandonment rate for the American Airlines app's user base has not been measured. It is possible that the majority of users authenticate infrequently enough that device trust provides negligible benefit.

2. **Solution direction not validated (Stage B).** Even if re-authentication friction is confirmed, it does not follow that device registration is the right solution. Biometric login (Face ID / Touch ID) via `devicevalidation-ios` might address the same friction with lower implementation risk and no persistent device state to manage.

3. **No success criteria defined.** "Ship it" provides no way to evaluate whether the feature succeeded. Without a defined metric (re-authentication reduction rate, abandonment improvement), the team cannot make a go/no-go decision after launch.

4. **`devicevalidation-ios` integration risk ignored.** Device registration requires coordination between `devicevalidation-ios` state, `AccountManager` session management, and `UserAccountCache`. Skipping prototype validation increases the risk of shipping a feature that conflicts with existing session lifecycle behavior.

---

## Application Notes for account-identity

- Any feature touching `devicevalidation-ios` — device registration, biometric enrollment, trusted-device session management — requires a Stage A problem validation before engineering scoping begins.
- Stage A evidence must come from `AccountManager` telemetry and `AAFeatureUserLoginObserver` event data. Do not rely on generic industry benchmarks as a substitute for in-app measurement.
