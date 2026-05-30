---
avatar: avatar-account-identity
law_id: PRD-1.5
law_title: "Evidence-Based Decision Making"
file_type: example
---

# PRD-1.5 Evidence-Based Decision Making — Example

## Law Summary

**PRD-1.5** requires that significant product decisions — especially architectural choices, platform migrations, and feature investments — are backed by observable data, not intuition or preference. Opinions may generate hypotheses; only evidence authorizes decisions.

---

## ✅ COMPLIANT Example: Decision to Migrate Account Screens from WKWebView to Native

### Decision Under Consideration

Should the team begin migrating account profile screens from the current `MyAccountBridgedWebViewController` (WKWebView) implementation to native UIKit or SwiftUI rendering?

### Evidence Assembled

**Performance monitoring data (90-day window):**

| Metric | Web-Bridge Screens (via MyAccountBridgedWebViewController) | Native Screens |
|---|---|---|
| Error rate (user-visible) | 4.6% | 2.0% |
| Median screen load time | 3.1s | 1.3s |
| 95th percentile load time | 7.8s | 2.9s |

Web-bridge screens show a **2.3× higher error rate** and **1.8s longer median load time** than native screens. This is consistent across iOS versions and device generations.

**User impact:**
- `AccountInfoActor` request failure rate is disproportionately higher on web-bridge profile screens than on `AccountManager`-backed native screens.
- Session abandonment after a profile screen error is 41% — users who hit a web-bridge error rarely retry.

**Engineering scope assessment:**
- `AccountProfileEndpoint`, `UserAccountInfo`, and `SecureTravelerEndpoint` already expose structured data models compatible with native rendering.
- `MyAccountNavigationManager` routing can be updated incrementally to route to native views without a full framework rewrite.

### Decision Authorized

The evidence supports beginning an incremental native migration, starting with the highest-traffic profile screen. The migration must be gated on each screen's individual error rate and load time improvement — not completed as a bulk rewrite.

### Evidence Gaps Acknowledged

- No A/B test data yet comparing native vs. web-bridge for the same screen with the same user cohort.
- Load time data may partially reflect network conditions, not just rendering. A controlled measurement against `UserAccountCache` hit vs. miss cohorts is needed before final migration sequencing.

---

## ❌ VIOLATION Example: WKWebView Migration Decision (Opinion-Based)

> "We think native screens will be better — let's rewrite MyAccountBridgedWebViewController."

### Why This Violates PRD-1.5

This statement substitutes **engineering preference for evidence**:

1. **"We think native screens will be better"** is an opinion, not a finding. Better by what measure? For which users? Under what conditions?
2. **No performance data is cited.** The 2.3× error rate and 1.8s load time difference are real and measurable — but they are not referenced. Without citing these figures, the decision cannot be evaluated, prioritized against competing work, or tracked for success.
3. **"Rewrite MyAccountBridgedWebViewController"** proposes a large-scope solution with no incremental validation plan. If the first migrated screen performs worse than the web-bridge version, there is no stage-gate to catch it.
4. **No evidence gaps acknowledged.** A compliant decision identifies what data is missing and what assumptions are being made.

**The compliant path:** Pull error rate and load time data from performance monitoring, segment by web-bridge vs. native surfaces, calculate user impact, and only then authorize migration — incrementally, with success criteria per screen.

---

## Application Notes for account-identity

- `MyAccountBridgedWebViewController` is the primary surface where PRD-1.5 will be tested. Any decision to change, migrate, or extend web-bridge screens requires observable performance data.
- `AccountInfoActor` failure rates and `UserAccountCache` hit/miss ratios are the most directly available data sources for account screen performance decisions.
- The ENG-3.1 risk classification of web-bridge coupling means these decisions carry architectural weight — evidence standards should be correspondingly high.
