---
law: PRD-1.2
avatar: avatar-product-travel-docs-compliance
title: "Problem-First: Reducing False-Positive Document Blocks"
---

# PRD-1.2 Problem-First — Travel Docs Compliance

## Law Summary

Validate the root cause before adding new checks. More verification is not always better — in this domain, false positives have direct operational and passenger experience costs.

---

## ✅ COMPLIANT Example

### Stated Request

> "Add stricter document verification to reduce the risk of passengers boarding with non-compliant travel documents."

### Research Conducted

90-day analysis of document verification outcomes at 12 hub stations (DFW, CLT, MIA, ORD, LAX, PHX, PHL, DCA, JFK, BOS, LGA, SFO), gate agent intervention logs, and TIMATIC query analysis.

| Finding | Value | Source |
|---------|-------|--------|
| Current false-block rate (passengers incorrectly flagged) | 1.8% | Document verification outcome log |
| Passengers/day affected by false blocks | ~340 | Calculated: 19K daily pax × 1.8% |
| Average gate agent intervention time per false block | 8 minutes | Gate agent observation (n=12 events) |
| Total gate agent minutes/day on false-block resolution | ~2,720 minutes | Calculated |
| Departure delay caused by false-block resolution | 14% of false-block events | Delay cause code analysis |
| Genuine non-compliance block rate | 0.3% | Document verification outcome log |
| False-block rate / genuine block rate ratio | 6:1 | Calculated |
| Top 3 false-block causes | Expired passport (but valid for trip dates), missing visa (visa-on-arrival not recognized), name mismatch (nickname vs. legal name) | TIMATIC error analysis |

**Root cause:** The verification system does not handle 3 specific document edge cases (visa-on-arrival eligibility, future-dated passport expiry, minor name variations) correctly. Stricter verification will increase the false-block rate further, causing more passenger harm, not less. The problem is **false positive reduction**, not stricter checks.

### Validated Problem Statement

> The travel document verification system incorrectly flags 1.8% of compliant passengers (340/day), requiring 8-minute gate agent interventions that cause departure delays in 14% of cases. The 6:1 false-block-to-genuine-block ratio indicates the system is over-triggering. Stricter verification will worsen this ratio. The problem is 3 specific false-positive causes that can be addressed with targeted rule fixes.

### Correct Solution Direction

Fix the top-3 false-block document types (expired passport for trips within validity, visa-on-arrival destinations, minor name variations). Target: reduce false-block rate from 1.8% to 0.9%.

---

## ❌ VIOLATION Example

> "Add additional verification checks for all document types to ensure maximum compliance rigor."

**Why this violates PRD-1.2:**
- "Maximum compliance rigor" increases true positive rate but also increases false positive rate.
- No investigation into why 1.8% of correct passengers are being blocked.
- The genuine non-compliance rate (0.3%) is already very low — the problem is false positives, not genuine violations.
- Stricter checks will increase 340/day → 500+/day gate agent interventions.
- Correct first step: analyze the false-block rate and identify specific error causes before any new verification logic.
