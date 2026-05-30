```yaml
use_case:
  id: uc-ancillary-bag-purchase
  name: Bag Purchase Post-Booking
  jtbd: "When a traveler realizes they need checked bags after booking, they need to purchase bag allowance through the app so they avoid higher airport bag fees."
  actor: Booked Traveler
  laws: [PRD-1.2, PRD-1.5, BUS-2.3, BUS-3.6, BUS-4.3, BUS-7.1]
  source_modules: bags-ios (213 swift files)
```

---

# Use Case: Bag Purchase Post-Booking

## Overview

A booked traveler who did not purchase checked bag allowance at booking time needs to add bags through the app before traveling. The primary value proposition is avoiding the higher at-airport bag fee. The flow must present accurate pricing with taxes, comply with DOT consumer protection requirements for payment and refund disclosure, protect payment card data under PCI scope minimization, and produce an auditable purchase record.

**Source:** `bags-ios` (213 swift files) — bag selection, pricing, payment, confirmation.

**BFF:** `mobile-ancillary-bff` (bag purchase and management), `mobile-offers-bff` (bag offer eligibility and pricing).

---

## Actor

**Booked Traveler.** Must have a confirmed booking with a departure that has not yet occurred. The traveler may or may not have an AAdvantage account (bag purchase is not gated on loyalty status, though AAdvantage status may affect price or allowance).

---

## Pre-Conditions

- Traveler has a confirmed booking.
- The flight is eligible for pre-purchase bag allowance (not all fare classes or routes support pre-purchase bags — eligibility is determined by `mobile-offers-bff`).
- Traveler is authenticated in the app.
- Departure has not yet occurred and the bag purchase window is open.

---

## Flow

### 1. Bag Purchase Entry Point

The traveler accesses the bag purchase flow from:

- My Trips / trip management screen (trip detail → Add Bags).
- Proactive in-app prompt or push notification (delivered by `mobile-offers-bff` when the traveler is in the bag purchase window).
- Pre-departure checklist within the app.

**PRD-1.2 note:** The entry point must reflect the problem the traveler has, not a generic upsell prompt. Passengers who have already purchased bags must not see the bag purchase prompt. Passengers who are ineligible for pre-purchase bags must see a clear explanation, not a broken flow.

### 2. Bag Selection

The traveler selects the number of checked bags per segment. `bags-ios` renders a bag selection surface showing:

- Number of bags selectable (1 to max allowance for fare class).
- Per-bag fee for each increment (first bag, second bag, etc.) displayed as exact decimal with currency.
- At-airport comparison price for each bag (e.g., "$35 in app vs. $40 at the airport") — price anchoring to address the documented abandonment problem at price display.
- Segment selector for multi-segment itineraries (bags may be purchased per-segment independently, depending on carrier rules).

**PRD-1.5 note:** The at-airport comparison price display is an evidence-backed design decision. Funnel analytics show 52% abandonment at price display; exit surveys attribute this to lack of price reference. The comparison framing is not decorative — it is the hypothesis-driven response to a measured problem.

**BUS-3.6 (mandatory):** Per-bag prices and the at-airport comparison price must be exact decimal values. Do not display rounded prices (e.g., "$35" when the actual price is "$35.00" with additional taxes not yet shown). Taxes and fees must be shown before the traveler proceeds to payment, not revealed only at the confirmation screen.

### 3. Pricing Display

Before the traveler enters payment, the pricing screen shows:

- Selected bags: quantity and segments.
- Per-bag fee line items.
- Tax and fees breakdown (itemized).
- Total due (sum of all line items — must equal the subsequent charge exactly).
- Refund eligibility statement: whether the bag purchase is refundable, and under what conditions (e.g., "Refundable if cancelled more than 24 hours before departure").

**BUS-2.3 (mandatory):** The refund policy must be visible on the pricing screen before payment entry. The traveler must be able to make an informed purchase decision knowing whether the bag fee is refundable. This is not a terms-and-conditions footnote — it must be prominently displayed.

**BUS-3.6 (mandatory):** The total displayed here is the total that will be charged. If the total changes for any reason between this display and the charge (e.g., pricing update, session timeout with price change), the traveler must be shown the new total and must re-confirm. Silent price increases are a law violation.

### 4. Payment Entry

The traveler selects or enters a payment method. `bags-ios` renders the payment entry surface.

**BUS-4.3 (mandatory — PCI scope minimization):**
- Full card numbers must never be displayed or logged in the app.
- Card data entered by the traveler must be tokenized at the point of entry (before any app-layer processing). `bags-ios` must pass raw card data directly to the payment processor SDK — it must not pass through app logic, be stored in memory in unencrypted form beyond the tokenization call, or be logged.
- The payment surface must display only the last four digits of stored cards for selection.
- `mobile-ancillary-bff` must never receive or store full card numbers; it receives payment tokens only.
- Compliance with BUS-4.3 is not a backlog item — a bag purchase flow that handles card data outside PCI-compliant patterns must not be shipped.

**UX requirement:** The selected payment method and charge amount must both be visible on the payment confirmation screen. The traveler must see "Your Visa ending in 4242 will be charged $XX.XX" — not just a confirm button.

### 5. Purchase Confirmation

The traveler taps confirm. `bags-ios` submits the purchase request to `mobile-ancillary-bff`. On success:

- Bag allowance is added to the traveler's booking.
- Confirmation screen displays: bags purchased, segments covered, total charged (exact decimal, matches pricing screen), transaction reference number.
- Confirmation is sent via email as a durable receipt.

**BUS-7.1 (mandatory):** A purchase audit record must be written at this step containing: traveler/passenger ID, booking reference, flight/segment, bags purchased, amount charged per bag, taxes, total charged, payment token (last 4 only — not full card), timestamp, and transaction reference number. This is the authoritative record for dispute resolution.

**BUS-3.6:** The amount on the confirmation screen must match the amount charged. If a discrepancy exists, the flow has a data integrity defect, not a display bug.

### 6. Receipt and Booking Update

After confirmation:

- The traveler's trip detail in My Trips is updated to reflect the purchased bag allowance.
- The receipt is accessible from the trip detail view (not only from email).
- The transaction reference number from BUS-7.1 is displayed in the receipt.

**BUS-4.3:** The receipt must not display full card numbers. Last 4 digits only, or a card type reference (e.g., "Visa ending in 4242").

### 7. Refund Eligibility

If the traveler's fare or bag purchase qualifies for a refund (e.g., flight cancellation, voluntary cancellation within the refund window), the refund must be:

- Initiated to the original payment method (not as travel credit unless the passenger affirmatively chooses travel credit).
- Initiated within the timeline disclosed at purchase (BUS-2.3).
- Accompanied by a refund confirmation with reference number.

**BUS-2.3:** The refund policy disclosed at purchase (Step 3) governs the refund behavior. The app must execute the refund per that disclosure. If a change in circumstances creates a discrepancy (e.g., a policy change after purchase), the policy in force at the time of purchase governs the traveler's entitlement.

**BUS-7.1:** The refund — if initiated — must be appended to the original purchase audit record, with: refund initiation timestamp, refund amount, refund method, and refund reference number.

---

## Boundary Notes

- **Initial booking bags:** If the traveler is in the booking flow and attempts to add bags, that flow is owned by `passenger-booking`. `bags-ios` handles post-booking bag addition only.
- **Bag allowance from AAdvantage status:** Status-based complimentary bag allowance is managed by the loyalty/AAdvantage domain. `bags-ios` presents the purchased bag allowance layer only; it reads status-based allowance as an input but does not own it.
- **Bag drop and airport bag operations:** Out of scope. This avatar ends at digital purchase confirmation.

---

## Compliance Summary

| Law | Requirement |
|---|---|
| PRD-1.2 | At-airport comparison pricing addresses documented abandonment problem at price display |
| PRD-1.5 | Price anchoring design decision backed by funnel analytics and exit survey data |
| BUS-2.3 | Refund policy shown at pricing screen before payment; refund to original method within disclosed timeline |
| BUS-3.6 | Per-bag prices and total as exact decimals with tax breakdown before payment entry |
| BUS-4.3 | Card data tokenized at entry; no full card numbers in app logic, logs, or BFF; last 4 only in UI |
| BUS-7.1 | Audit record at purchase with full transaction detail; updated at refund if applicable |
