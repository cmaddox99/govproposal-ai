---
law: PRD-5.1
avatar: avatar-product-customer-relations-ops
title: "MVP: AI Draft for Delayed Baggage Complaints Only"
---

# PRD-5.1 MVP Law — Customer Relations Operations

## Law Summary

The smallest experiment that validates the draft quality hypothesis is the correct first investment. Prove AI draft quality in one complaint category before expanding.

---

## ✅ COMPLIANT Example — MVP Canvas

### Hypothesis

> AI-generated drafts for delayed baggage complaints will be accepted by CR Reps without rewrite at a rate ≥ 80%, reducing draft time from 45 minutes to ≤ 10 minutes per complaint, with zero compliance violations.

### Riskiest Assumption

AI-generated drafts for delayed baggage complaints will be policy-compliant (correct DOT language, correct compensation calculations, no prohibited trademark or liability language) without requiring supervisor review on every response.

### Why Delayed Baggage First

- Highest volume complaint category: 34% of all CR complaints
- Most rule-based: compensation is deterministic (DOT 14 CFR Part 254, bag delay policy)
- Template coverage: existing delayed baggage templates have highest draft acceptance rate (74%)
- Lowest judgment risk: resolution is typically miles credit or expense reimbursement — no goodwill discretion required

### MVP Scope

**In scope:**
- AI draft assistance for delayed baggage complaints only
- CR Rep reviews and approves each draft before sending (no auto-send)
- Draft must include: apology language, compensation calculation per policy, claim reference number
- Pilot: 6 CR Reps, 4-week measurement period

**Out of scope:**
- All other complaint categories (flight delays, service failures, disability accommodation)
- Auto-send without CR Rep review (never in scope)
- Real-time complaint intake triggers
- Integration with compensation issuance systems (CR Rep manually issues per approved draft)

### Acceptance Criteria

```gherkin
Scenario: CR Rep receives AI draft for delayed baggage complaint
  Given a delayed baggage complaint is submitted (bag delayed ≥ 24 hours)
  And the system retrieves customer record and flight details
  When the AI draft is generated
  Then the draft includes the correct compensation per bag delay policy
  And the draft uses DOT-compliant language with no prohibited terms
  And the CR Rep can approve and send in ≤ 2 minutes
  And the draft is logged in the audit trail with model_version and run_id
```

### Success Criteria (4-Week Pilot)

| Metric | Target | Fail Gate |
|--------|--------|-----------|
| Draft acceptance rate (no rewrite) | ≥ 80% | < 60% → pause, investigate quality |
| Compliance violation rate | 0% | > 0% → immediate halt |
| Draft time per complaint | ≤ 10 minutes | > 15 minutes → investigate UX friction |
| CR Rep satisfaction with draft quality | ≥ 4.0/5.0 | < 3.5 → investigate training data quality |

### Expansion Gate

Other complaint categories (flight delays, service failures) begin only after: 4-week pilot shows draft acceptance rate ≥ 80% AND compliance violation rate = 0%.

---

## ❌ VIOLATION Example

> "AI drafts for all complaint categories, automatically sent on approval, with real-time triggers from the complaint intake system."

**Why this violates PRD-5.1:**
- All complaint categories bundled: each has different policy complexity, compensation logic, and compliance risk.
- "Automatically sent" removes the CR Rep review that prevents compliance violations.
- Real-time triggers add integration complexity before draft quality is proven.
- Correct approach: 4-week pilot on one category (delayed baggage), ≥ 80% acceptance rate, zero violations. Then expand.
