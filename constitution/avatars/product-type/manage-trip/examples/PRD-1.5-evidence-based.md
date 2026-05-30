---
avatar: avatar-manage-trip
law_id: PRD-1.5
law_title: "Evidence-Based Decision Law"
file_type: example
---

# PRD-1.5 Evidence-Based Decision Law — Manage Trip

## The Law

Every significant product decision must be backed by observable, specific
evidence — quantitative data, user research, or documented system behavior.
Decisions based on assumption, intuition, or unverified belief violate PRD-1.5.

---

## ✅ COMPLIANT Example — Cancellation Flow Redesign Decision

### Decision Under Consideration

> Should we redesign the trip cancellation flow to reduce drop-off before
> the confirmation step?

### Evidence Gathered

**Funnel analysis (Amplitude, Q3 2025 — domestic cancellations)**

| Step | Users Reached | Drop-off |
|------|--------------|---------|
| Tap "Cancel Trip" (`CancelTripView`) | 100% | — |
| Eligibility result displayed | 97% | 3% |
| Terms & fees review screen (`TaxesAndFeesViewModel`, `CostSummaryViewModel`) | 61% | 36% |
| Confirmation tap (`CancelReservationCoordinator`) | 58% | 3% |
| Confirmation screen shown | 58% | — |

The 36-point drop at the terms screen is the largest loss in the funnel.

**Session recordings (FullStory, 200 sessions sampled)**

- 74% of users who dropped at the terms screen scrolled back up at least once
- 41% tapped the "Taxes and Fees" expansion chevron but closed it within 2 seconds
- Qualitative annotation: users appear confused by refund method labeling
  ("Original Form of Payment" vs. "Travel Voucher" vs. "eVoucher")

**Support ticket tagging (Salesforce, 30-day window)**

- 1,840 tickets tagged "cancel confusion" — 63% cite refund method uncertainty
- Average handle time for cancel-related tickets: 9.2 minutes

### Decision (evidence-backed)

> Redesign the refund method disclosure section of `CostSummaryViewModel` and
> the terms label copy in `TaxesAndFeesViewModel`. Hypothesize that clarifying
> refund method language will recover ≥15 points of the 36-point drop. Measure
> against the funnel baseline above in a 4-week A/B test post-launch.

This is compliant: the decision identifies a specific, measured problem, cites
the exact screens involved, and sets a falsifiable success hypothesis.

---

## ❌ VIOLATION Example — Cancellation Flow Redesign Decision

### What the Team Did Instead

In a product review meeting, a PM stated:

> "The cancellation flow feels old and clunky. Users probably want a simpler,
> cleaner UI — fewer words, bigger buttons. Let's redesign the whole flow to be
> more modern and see if satisfaction goes up."

An engineering ticket was opened:

> "Redesign cancel trip UX — modernize all screens, simplify copy, increase
> button sizes. Measure NPS after launch."

### Why This Violates PRD-1.5

- "Feels old and clunky" is a subjective impression, not evidence
- "Users probably want" is assumption, not user research
- No funnel data was referenced; the 36-point drop at the terms screen is unknown
  to the team making this decision
- NPS is a lagging, low-resolution metric — it cannot attribute changes to the
  specific UI decisions being made
- A full-flow redesign scoped from an opinion cannot be evaluated for ROI

### Consequences of This Approach

- Engineering may spend 3 sprints reskinning screens that are not the source of
  drop-off
- If cancellation completion rates do not improve, the team has no diagnostic
  signal — they cannot distinguish "wrong problem" from "wrong solution"
- BUS-2.3 DOT compliance language may be inadvertently altered during a
  cosmetic copy simplification pass, creating regulatory exposure

### The Correct Correction

Pull the Amplitude funnel data. Sample FullStory sessions on the terms screen.
Tag Salesforce tickets. Identify the specific friction point with data before
scoping any redesign. Then write a decision document citing those sources.
