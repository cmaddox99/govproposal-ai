---
avatar: avatar-ancillary-upsell
law_id: PRD-2.5
law_title: "Discovery Stage-Gate Law"
file_type: example
---

# PRD-2.5 — Discovery Stage-Gate Law

## Law Summary

New product capabilities must pass through defined discovery stages before solution-building begins. Each stage must produce a specific output that gates entry to the next stage. Skipping stages to accelerate delivery is a law violation, not a tradeoff.

---

## ✅ COMPLIANT Example

### Feature Under Development

Upgrade Bid/Auction — allowing economy passengers to submit a bid for a premium cabin upgrade when the full-price instant upsell price is above their willingness to pay. Grounded in `auction-ios` (86 swift files).

### Stage-Gate Plan

**Stage A — Problem & Comprehension Validation (Gate: research output)**

*Question to answer:* Do passengers understand what a bid auction is and how it works in the context of a flight upgrade?

*Activities:*
- Unmoderated usability sessions (n=16 participants, economy passengers with upcoming travel).
- Concept test: show participants a static prototype of the bid submission screen. Measure: can they explain back — in their own words — what will happen to their money if they win? If they lose?
- Specific comprehension tests: (a) "Your bid may not be accepted — do you understand what happens to the charge on your card?" (b) "If your bid loses, when do you get your money back?"

*Gate output required:* ≥75% of participants correctly understand bid mechanics and refund timeline before proceeding to Stage B. If below threshold, iterate on framing/copy before advancing.

**Stage B — Solution Design (Gate: reviewed design + compliance sign-off)**

*Activities:*
- Design the bid submission, bid management, and result notification flows within `auction-ios`.
- Define bid floor/ceiling logic with Revenue Management.
- Document BUS-2.3 compliance: where and how refund policy for losing bids is shown before bid submission (not after).
- Document BUS-3.6 compliance: bid amounts display as exact decimal values with applicable taxes shown.
- Legal and compliance review of auction mechanics (BUS-9.3 — AAdvantage program rules interaction).

*Gate output required:* Signed design spec with compliance annotations. Legal sign-off on bid/refund flow.

**Stage C — Limited Cohort Prototype (Gate: conversion and comprehension metrics)**

*Activities:*
- Ship `auction-ios` bid placement flow to a 5% cohort of eligible economy passengers on select routes.
- Measure: bid submission rate, bid win rate, bid loss refund completion rate, post-loss support contact rate (proxy for confusion).
- Measure: does comprehension at real-money bid submission match the Stage A research target?

*Gate output required:* Conversion data and support-contact rate below defined threshold. Only then expand rollout.

---

## ❌ VIOLATION Example

### Proposed Approach

> "The auction-ios repo already exists with 86 swift files. Engineering wants to ship the full bid/auction feature this quarter. Let's skip discovery and go straight to build — we can learn from real usage."

### Why This Violates PRD-2.5

Building the full auction system without Stage A comprehension validation creates three compounding risks:

1. **Passenger confusion at real-money transactions.** If passengers don't understand that their bid is a charge — not a price lock — they will dispute charges, generate support volume, and potentially trigger regulatory review under DOT consumer protection rules (BUS-2.3). Stage A exists specifically to validate comprehension before money is involved.

2. **BUS-2.3 refund disclosure risk.** Skipping Stage B means the refund policy for losing bids may not be surfaced before submission. This is not a UX gap — it is a federal consumer protection requirement. Building without the compliance review in Stage B embeds the risk into shipped code.

3. **No learning structure.** "We'll learn from real usage" is not a stage-gate; it is uncontrolled experimentation with a live financial product. Learning from real usage is valid only after Stage C defines what metrics constitute a passing gate.

The existence of `auction-ios` source files does not constitute discovery completion. Code existing is a supply-side fact; passenger comprehension is a demand-side question that code cannot answer.
