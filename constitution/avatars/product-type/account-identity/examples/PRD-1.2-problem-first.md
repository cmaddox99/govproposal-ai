---
avatar: avatar-account-identity
law_id: PRD-1.2
law_title: "Problem-First Development"
file_type: example
---

# PRD-1.2 Problem-First Development — Example

## Law Summary

**PRD-1.2** requires that every product initiative starts with a clearly defined, evidence-backed problem statement — not a solution. Features may not be scoped until the problem is validated with data.

---

## ✅ COMPLIANT Example: Biometric Login Initiative

### Problem Statement

**Observation:** Session analytics from `AccountManager` show that **34% of returning AAdvantage members fail password-based login on their first attempt** when returning to the app after a 30-day absence. Of those who fail the first attempt, **18% abandon the sign-in flow entirely** without completing authentication.

**Impact:** An 18% abandonment rate on re-authentication directly suppresses booking frequency among high-value members — users who authenticate successfully have a 3.4× higher booking rate over the following 30 days.

**Root Cause Hypothesis:** Password recall degrades for infrequent users. The current `UserAccountEndpoint` credential flow offers no low-friction recovery path on the sign-in screen rendered via `MyAccountBridgedWebViewController`. Users who experience friction give up rather than recover.

**Evidence Sources:**
- `AccountManager` session telemetry: first-attempt failure rate by days-since-last-session cohort
- `UserAccountEndpoint` error response distribution: credential error vs. network error vs. other
- Funnel analysis: `AAFeatureUserLoginObserver` sign-in start event → authenticated session confirmed event

**Problem Validated:** Yes. Data confirms the failure pattern is concentrated in the 30+ day re-engagement cohort, not new users or daily active users.

### Hypothesis for Solution Direction

Adding biometric authentication (Face ID / Touch ID) via `devicevalidation-ios` for enrolled returning members will reduce the first-attempt failure rate and the abandonment rate in the 30+ day re-engagement cohort, because biometric authentication eliminates the password recall failure mode.

**This is a hypothesis, not a commitment.** A PRD-2.5 stage-gate is required before engineering scoping begins.

---

## ❌ VIOLATION Example: Biometric Login Initiative (Solution-First)

> "Build biometric login with Face ID, Touch ID, and a new PIN-based fallback system."

### Why This Violates PRD-1.2

This statement **starts with a solution**, not a problem. It specifies three distinct mechanisms (Face ID, Touch ID, PIN fallback) without establishing:

1. **What problem is being solved.** Is this about authentication failure rates? User preference? Security posture? We don't know.
2. **Who is affected and how severely.** No cohort data, no failure rate, no abandonment metric.
3. **Why these three specific mechanisms.** PIN fallback in particular implies an assumption that biometric failure is common — but there is no evidence cited.
4. **Whether the problem exists at a scale that justifies investment.** Building Face ID + Touch ID + PIN fallback is a substantial engineering scope in `devicevalidation-ios`. Without problem validation, this could be solving a problem affecting 2% of users while neglecting higher-impact issues.

**The compliant path:** Establish the sign-in failure rate from `AccountManager` analytics, validate that the failure mode is password recall (not network errors, not account lockouts), and only then scope the biometric solution.

---

## Application Notes for account-identity

- Always start with `AccountManager` session telemetry when hypothesizing authentication improvements.
- The web-bridge rendering via `MyAccountBridgedWebViewController` makes it harder to instrument sign-in screen interactions at the field level — factor this into evidence collection. Consider what signals are available before declaring a problem validated.
- `AAFeatureUserLoginObserver` provides the entry event; `AccountManager` session state provides the outcome — these two together are the minimum instrumentation for any sign-in problem statement.
