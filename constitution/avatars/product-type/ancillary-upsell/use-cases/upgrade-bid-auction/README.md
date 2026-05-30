```yaml
use_case:
  id: uc-ancillary-upgrade-bid-auction
  name: Upgrade Bid Auction
  jtbd: "When an economy passenger wants a better seat but the full-price upgrade is too expensive, they need to place a bid for an upgrade so they can secure a better experience at a price they choose."
  actor: Economy Passenger with AAdvantage account
  laws: [PRD-1.2, PRD-5.1, PRD-6.2, BUS-2.3, BUS-3.6, BUS-7.1]
  source_modules: auction-ios (86 swift files)
```

---

# Use Case: Upgrade Bid Auction

## Overview

The upgrade bid auction allows economy passengers who find the full instant upsell price above their willingness to pay to submit a bid for a premium cabin upgrade. Bids are evaluated against available inventory and competing bids. Winning passengers are upgraded; losing passengers receive a full refund of the bid amount. The flow must be transparent on bid mechanics, compliant with DOT consumer protection rules for payments and refunds, and produce an auditable record for every bid transaction.

**Source:** `auction-ios` (86 swift files) — bid placement, bid management, and bid status tracking.

**BFF:** `mobile-ancillary-bff` (bid submission and status), `mobile-offers-bff` (offer eligibility and bid window delivery).

---

## Actor

**Economy Passenger with AAdvantage account.** Must have an active booking in an eligible fare class on a route with available bid-upgrade inventory. The AAdvantage account is required for bid mechanics (the bid is tied to the passenger's profile) and for BUS-9.3 AAdvantage program rule compliance.

---

## Pre-Conditions

- Passenger has a confirmed economy booking on a bid-eligible flight.
- `mobile-offers-bff` has delivered a bid offer to the passenger (within the bid window, typically 72–24 hours before departure).
- Full instant upsell price is either unavailable or was declined by the passenger.
- Passenger is authenticated.

---

## Flow

### 1. Bid Offer Presentation

The passenger receives notification (push or in-app) that they are eligible to bid on a cabin upgrade. The bid offer screen displays:

- The cabin being bid on (e.g., Business Class).
- The bid floor (minimum acceptable bid) and bid ceiling (maximum bid accepted), displayed as exact decimal values with currency.
- The bid window (how long the offer is open).
- A clear statement that **the bid is a charge at submission** — the passenger's card is charged when they submit the bid, not if they win.

**BUS-2.3 (mandatory):** The refund policy for losing bids must be shown on this screen, before the passenger enters any bid amount. Specifically: "If your bid is not selected, the full amount will be refunded to your original payment method within [X] business days." This is a federal consumer protection requirement; it is not UX copy that can be deferred to a confirmation email.

**BUS-3.6:** Bid floor and ceiling must be displayed as exact decimals with applicable taxes included. Do not show a bid range that excludes taxes — the displayed range must represent what the passenger will actually be charged.

### 2. Bid Submission

The passenger enters their bid amount within the floor/ceiling range. The bid submission screen displays:

- Entered bid amount (exact decimal).
- Tax breakdown on the bid amount.
- Total charge at submission (bid + taxes).
- Refund policy restatement (condensed) directly adjacent to the submit button.
- Payment method on file or option to add payment.

On submit: `auction-ios` bid placement module sends the bid to `mobile-ancillary-bff`. The passenger's card is charged the full bid amount immediately.

**BUS-7.1 (mandatory):** A bid submission audit record must be written at this point, containing: passenger ID, flight/segment, cabin bid on, bid amount, taxes, total charged, payment method token (not full card), timestamp, bid offer ID, and bid window expiry. This record is the authoritative reference for any dispute about whether a bid was placed and what was charged.

**BUS-3.6:** The amount charged must equal the total displayed to the passenger at submission. Any discrepancy is a law violation. If the bid amount calculation changes between display and charge (e.g., due to a tax rate update), the passenger must be shown the new total and must re-confirm.

### 3. Bid Confirmation

After successful bid submission, the passenger receives:

- Bid confirmation screen with bid amount, charge confirmation, and bid reference number.
- Explicit reminder of the refund policy (in full) for losing bids.
- Expected notification timeline for bid result.

The bid confirmation is also sent via email/push as a durable receipt. **BUS-7.1:** The bid reference number must appear on both the in-app confirmation and any outbound notification so the passenger has an auditable reference for the transaction.

### 4. Bid Management

The passenger can view their active bids in the bid management surface (within `auction-ios` bid management module). This surface shows:

- Active bids with bid amount, cabin, flight, and bid status (pending evaluation).
- Bid window remaining.
- The option to cancel a bid before the evaluation window closes (if cancellation is supported per program rules — see BUS-9.3).

**BUS-9.3:** AAdvantage program rules govern whether a bid can be modified or cancelled after submission. The bid management surface must accurately reflect program rules. Do not show a "Cancel Bid" button if cancellation is not permitted for the applicable fare class or bid window state.

**BUS-2.3:** If bid cancellation is permitted and the passenger cancels, the refund must be initiated immediately. The refund timeline must be shown at the moment of cancellation.

### 5. Bid Status Tracking

`auction-ios` bid status tracking module polls `mobile-ancillary-bff` for bid result updates. The bid evaluation typically occurs 24 hours before departure. Status states:

- **Pending:** Bid is in the evaluation queue.
- **Won:** Passenger's bid was selected; upgrade is confirmed.
- **Lost:** Passenger's bid was not selected; refund is being processed.
- **Expired:** Bid window closed without evaluation (edge case — treat as lost with full refund).

The passenger is notified via push notification when status transitions to Won or Lost.

### 6. Bid Result — Won

The passenger receives upgrade confirmation:

- New cabin assignment.
- Seat assignment (if applicable).
- Updated itinerary.
- Confirmation that the bid charge is the final amount paid (no additional charge).

**BUS-7.1:** The bid audit record is updated with the win outcome, new cabin, and seat assignment.

### 7. Bid Result — Lost (Refund)

The passenger receives:

- Notification that their bid was not selected.
- Confirmation that a full refund of the bid amount (including taxes) has been initiated.
- Refund timeline (matches what was disclosed at bid submission — BUS-2.3).

**BUS-2.3 (mandatory):** The refund must be initiated to the original payment method within the timeline disclosed at bid submission. This is not optional. If the payment processor cannot initiate the refund within the disclosed window, the passenger must be proactively notified of the revised timeline.

**BUS-7.1:** The bid audit record is updated with the lost outcome and refund initiation timestamp. The refund confirmation (including refund reference number) must be available in the bid management surface for the passenger to reference.

---

## PRD-5.1 Note — MVP Scoping

The bid/auction MVP should cover a single cabin tier on a single route cluster before expanding to the full network. Critical assumption to test: do passengers submit bids at a rate that justifies the inventory management complexity of running auctions? A minimum viable auction tests that question with one cabin and one route cluster, using `auction-ios` bid placement and status tracking modules against a constrained inventory pool.

---

## PRD-6.2 Note — Retention Before Expansion

Before expanding bid/auction to additional cabin tiers or routes, measure: (1) bid submission rate, (2) bid loss support contact rate, (3) repeat bid submission rate. If passengers who lose bids do not submit future bids, the refund experience or result notification has a retention defect that must be resolved before expanding auction surface.

---

## Compliance Summary

| Law | Requirement |
|---|---|
| BUS-2.3 | Refund policy for losing bids shown before bid submission; refund initiated within disclosed timeline |
| BUS-3.6 | Bid floor/ceiling and total charge shown as exact decimals with taxes; no rounding |
| BUS-7.1 | Audit record at bid submission; updated at bid result; refund confirmation auditable |
| BUS-9.3 | AAdvantage program rules govern cancellation eligibility and miles interaction |
| PRD-1.2 | Bid/auction solves a defined problem: willingness-to-pay gap for full instant upsell price |
| PRD-5.1 | MVP scoped to single cabin/route cluster to test bid submission hypothesis |
| PRD-6.2 | Measure retention (repeat bid rate) before expanding auction surface |
