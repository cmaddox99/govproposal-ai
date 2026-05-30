---
avatar: avatar-manage-trip
law_id: PRD-2.5
law_title: "Discovery Stage-Gate Law"
file_type: example
---

# PRD-2.5 Discovery Stage-Gate Law — Manage Trip

## The Law

Discovery must proceed through sequential, reviewable stages. Each stage
produces a defined artifact that must be reviewed and approved before the next
stage begins. Skipping stages or running them in parallel violates PRD-2.5.

---

## ✅ COMPLIANT Example — Reservation Contact Update Feature

### Feature: Allow travelers to update phone/email on an existing reservation

**Stage A — Problem Research** *(must complete before Stage B opens)*

Artifact produced: Problem Statement Document

> Travelers who change their phone number or email address after booking have no
> self-service way to update contact details on their reservation. AA's
> notification systems (flight status, gate change alerts) use the contact
> details stored on the PNR. Stale contact data causes missed notifications.
>
> Evidence:
> - 4,200 calls/month tagged "update contact info" in call center system
> - 9.1% of push notification delivery failures trace to mismatched email/phone
>   (Adobe Analytics, 90-day window)
> - `ReservationSummaryView` (trips-ios) displays contact info read-only — no
>   edit affordance exists today

Gate A review: Problem Statement approved by Product Lead and Legal (data
privacy review initiated for contact mutation endpoint).

---

**Stage B — Solution Design** *(opens only after Gate A approval)*

Artifact produced: Solution Brief

> Proposed approach: Add an "Edit Contact Info" entry point to
> `ReservationSummaryView`. Route mutations through `Mobile-Update-Reservation`
> BFF. Store updates via `mobile-reservation-bff` write endpoint.
>
> Out of scope for this solution: passport data, TSA Known Traveler Number,
> AAdvantage profile (those live in separate identity systems).

Gate B review: Solution Brief approved. Architecture review confirms
`Mobile-Update-Reservation` can handle the write without PSS direct dependency.

---

**Stage C — Spec & Acceptance Criteria** *(opens only after Gate B approval)*

Artifact produced: Executable spec with BDD scenarios covering:
- Happy path: valid email update persisted to PNR
- Validation: malformed email rejected client-side before BFF call
- Conflict: PNR locked by active check-in — graceful error shown
- Audit: mutation logged per BUS-7.1 requirements

Gate C review: Spec signed off. Engineering ticket created referencing spec SHA.

This is compliant: each stage produced a reviewable artifact; no engineering
work began until Stage C was approved.

---

## ❌ VIOLATION Example — Reservation Contact Update Feature

### What the Team Did Instead

On Monday, a customer complaint arrived in the team Slack:

> "I changed my phone number and missed my gate change alert. Why can't I update
> this in the app?"

By Thursday, the PM had added three stories to the active sprint:

> - "Add edit button to contact section of reservation detail"
> - "Wire edit button to PUT /reservation/contact endpoint"
> - "Show success toast after update"

No problem statement was written. No Stage A gate was opened. No solution brief
was reviewed. No spec with acceptance criteria existed when the first PR was
opened.

### Why This Violates PRD-2.5

- A single customer complaint is anecdotal, not a validated problem signal
- Jumping from complaint to sprint planning collapses Stages A, B, and C into zero
- The solution was assumed (an edit button) rather than derived from research
- No architecture review occurred — the team may be writing to a PSS endpoint
  that requires a change freeze waiver
- No BUS-7.1 audit logging was specified — the mutation will ship without an
  immutable record

### The Correct Correction

1. Open Stage A: quantify call volume, pull notification failure data
2. Only after Gate A approval: write a solution brief for Stage B
3. Only after Gate B: write executable spec for Stage C
4. Engineering sprint begins only after Gate C sign-off
