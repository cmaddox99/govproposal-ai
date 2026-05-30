# Proposal: Product Avatar Accessibility Governance

**Status:** 🔴 BLOCKED — Awaiting governance panel ruling
**Spec ID:** `product-avatar-accessibility-governance`
**Triggered by:** `product-avatar-bus-enrichment` — `PRD-3.4-accessibility.md` split into dedicated proposal pending domain boundary ruling
**Scope:** Single file: `PRD-3.4-accessibility.md` — routing to correct artifact layer
**Parent PR:** #14 (c-plus-plus-avatar-enrichment)
**Companion to:** `product-avatar-bus-enrichment`

---

## Problem

`PRD-3.4-accessibility.md` was deleted from `avatars/technology/cpp/` as part of Amendment O (V1/V2 domain boundary violations). Its correct destination is uncertain:

**The boundary question:** Accessibility requirements straddle the tech/product divide.
- `mobile-react-native` (a **technology** avatar) already contains `PRD-3.4-accessibility.md` in its examples, establishing a precedent that accessibility may belong in technology avatars
- `passenger-booking` (a **product-type** avatar) is the primary customer-facing booking flow and a natural owner of UX accessibility requirements
- A dedicated `accessibility-governance` product avatar could also be created if accessibility is broad enough to warrant its own domain

**Governance panel ruling required:** Does `PRD-3.4` content belong in:
1. Technology avatars (precedent: mobile-react-native) — accessibility is a technical implementation concern
2. Product-type avatars (candidate: passenger-booking) — accessibility is a UX product requirement
3. A new dedicated product avatar (new: accessibility-governance) — accessibility is broad enough to stand alone

---

## Proposed Routing Options

| Option | Target | Rationale | Precedent |
|--------|--------|-----------|-----------|
| A | `avatars/technology/mobile-react-native/` | Enrich existing PRD-3.4 with web/C++ context | mobile-react-native already owns PRD-3.4 |
| B | `avatars/product-type/passenger-booking/` | Accessibility is a UX product requirement for the primary booking flow | Standard product-type placement |
| C | New `avatars/product-type/accessibility-governance/` | Accessibility is a cross-cutting concern needing its own avatar | None — new precedent |

**Recommended:** Option A (consolidate in mobile-react-native) or Option B (passenger-booking). Option C only if governance panel determines accessibility scope warrants a standalone avatar.

---

## Deliverables (post-ruling)

| Artifact | Description |
|----------|-------------|
| Governance ruling documented in this file | Update Status + chosen option above |
| `PRD-3.4-accessibility.md` placed in target | One file, one destination |
| Test contract updated | Confirm correct avatar receives the file |

---

## Success Criteria

| Criterion | Verification |
|-----------|--------------|
| Governance panel ruling received and documented | Status updated from BLOCKED → PROPOSED |
| `PRD-3.4-accessibility.md` exists in exactly one correct avatar | Manual audit |
| No duplicate `PRD-3.4-accessibility.md` across avatars | `rg PRD-3.4 avatars/` shows exactly one result |

---

## Laws Cited

| Law | Relevance |
|-----|-----------|
| [ENG-11.1](laws/engineering/spec-driven-development.md) | Domain boundary enforcement — accessibility file must live in constitutionally correct artifact layer |
| [ENG-11.2](laws/engineering/spec-driven-development.md) | Proposal Completeness — routing map required before implementation |
