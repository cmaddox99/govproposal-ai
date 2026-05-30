---
avatar: avatar-manage-trip
law_id: PRD-6.2
law_title: "Retention Over Acquisition Law"
file_type: example
---

# PRD-6.2 Retention Over Acquisition Law — Manage Trip

## The Law

When resources are constrained, teams must prioritize features that retain
and satisfy existing customers over features that acquire new ones. A broken
core journey that erodes trust in current travelers is a higher priority than
any acquisition or upsell surface.

---

## ✅ COMPLIANT Example — Trip Cancellation Experience

### Situation

Post-booking satisfaction scores for travelers who cancel a trip dropped 11
points YoY (Q3 2024 → Q3 2025). Call center tickets tagged "where is my
refund" increased 28% over the same period. The cancellation confirmation
screen (`CancelTripView` post-confirm state) shows a generic "Your trip has
been cancelled" message with no refund timeline, no refund method, and no
reference number.

A growth team proposed adding a re-booking promotional banner to the
cancellation confirmation screen ("Book your next trip — save 15%") as part
of a new acquisition campaign.

### Compliant Decision

The manage-trip team deprioritized the promotional banner and instead
invested the sprint in:

1. Surfacing the refund method explicitly on the cancellation confirmation
   screen (cash refund vs. travel credit, per DOT disclosure requirements)
2. Adding a refund timeline estimate ("Allow 7 business days for credit card
   refunds") driven by fare class and form of payment data from
   `CostSummaryViewModel`
3. Including a PNR reference number and a "Contact Support" deep link if the
   refund has not appeared within the stated window

**Expected retention outcome:** Reducing "where is my refund" calls decreases
the frustration that turns cancelled travelers into non-returning travelers.
A traveler who received a clear, accurate refund confirmation is more likely
to re-book than one who spent 20 minutes on hold asking where their money went.

**Measurement plan:** Track 90-day re-booking rate for travelers who cancelled
in the treatment cohort vs. historical baseline. Track "where is my refund"
call volume as leading indicator.

This is compliant: the team explicitly chose to fix a retention-degrading
experience before adding an acquisition surface.

---

## ❌ VIOLATION Example — Trip Cancellation Experience

### What the Team Did Instead

The growth team's request was approved. The cancellation confirmation screen
was updated to include:

> "Sorry to see you go! Book your next flight and save 15% →"

The promotional banner launched. The generic "Your trip has been cancelled"
confirmation message remained unchanged. Refund method and timeline were
still not disclosed. The "where is my refund" call volume continued to
climb.

### Why This Violates PRD-6.2

- The team added an acquisition surface (re-booking promo) before fixing the
  retention problem (refund transparency) that was actively degrading trust
- The promotional banner appears to travelers at the moment of highest
  dissatisfaction — immediately after they cancelled — without resolving the
  frustration that may have caused the cancellation
- The 11-point satisfaction drop and 28% call volume increase were known signals
  that the core experience was broken; shipping an upsell over a broken
  foundation violates the retention-first principle
- The DOT refund disclosure gap (BUS-2.3) represents regulatory exposure that
  was knowingly deferred in favor of a promotional feature

### The Harm

Travelers who cancel, see a promo banner, then spend time tracking down their
refund associate the brand with a pattern: "AA is more interested in my next
purchase than in resolving my current problem." Re-booking rates in this cohort
are predictably lower than among travelers who received a clear refund
confirmation.

### The Correct Correction

Fix refund transparency first. Measure 90-day re-booking rate. Only after the
retention signal has recovered should an acquisition surface be placed on the
cancellation confirmation screen — and even then, it should be secondary to
the refund status information.
