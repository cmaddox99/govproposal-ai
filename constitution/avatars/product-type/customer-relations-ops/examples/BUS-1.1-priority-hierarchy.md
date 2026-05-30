---
avatar: avatar-customer-relations-ops
law_id: BUS-1.1
law_title: "Priority Hierarchy Law"
file_type: example
---

# BUS-1.1 Priority Hierarchy — Customer Relations Ops

## Law Summary

Decisions MUST follow: **Legal > Safety > Privacy > Security > Business Continuity > Efficiency**. Higher-priority concerns win WITHOUT EXCEPTION.

| Priority | Level | CR Domain Example |
|----------|-------|------------------|
| 1 | Legal | DOT/legal compliance overrides LLM efficiency — prohibited-words enforcement is non-negotiable |
| 2 | Safety | Medical/ADA data requires highest protection tier regardless of impact on draft quality |
| 3 | Privacy | PII never crosses LLM boundary — not for any draft quality improvement |
| 4 | Security | LLM API credentials vault-managed; no shortcuts for model swapping speed |
| 5 | Business Continuity | Fallback to manual drafting when LLM pipeline is unavailable |
| 6 | Efficiency | Draft generation speed — pursued only after all compliance requirements are met |

---

## ✅ COMPLIANT Example 1 — Prohibited-Words Enforcement

**Scenario:** An LLM draft contains the word "guarantee" in a flight delay response. An engineer proposes allowing the draft through with a soft warning instead of hard rejection to improve draft acceptance rate.

**Decision:** REJECTED. Prohibited-words are a Legal compliance requirement — "guarantee" in a delay response creates legal liability. Hard rejection is mandatory. Legal > Efficiency, unconditionally.

**Required approach:** Drafts that contain prohibited words must be rejected by the compliance pipeline, not soft-warned. The draft acceptance rate metric must never be optimized at the expense of compliance.

---

## ✅ COMPLIANT Example 2 — PII Redaction Before LLM

**Scenario:** A product manager proposes allowing complaint text with masked (but not removed) PII to pass to the LLM to improve context and draft quality.

**Decision:** REJECTED. PII must be fully redacted before any LLM call. Masking is not sufficient if the original PII can be inferred from context. Privacy > Draft Quality — no exception.

---

## ❌ VIOLATION Example 1 — DOT Compensation Skipped

**Scenario:** The LLM suggests a compensation amount lower than the DOT-required minimum. An agent accepts the draft to avoid editing it.

**Why this violates BUS-1.1:** DOT compensation minimums are Legal requirements. Accepting a draft that undercompensates a DOT-covered incident is a compliance violation. The compensation validation step must run before draft generation, not be left to agent judgment.

---

## ❌ VIOLATION Example 2 — Medical Data in LLM Prompt

**Scenario:** An engineer includes a medical accommodation complaint's full text in the LLM prompt, reasoning that the context improves the draft's empathy.

**Why this violates BUS-1.1:** Medical data is RESTRICTED. It must never be included in LLM payloads regardless of potential draft quality improvement. Safety/Privacy > Efficiency. A less empathetic draft is always preferable to a Privacy violation.
