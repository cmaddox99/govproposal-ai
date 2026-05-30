---
avatar: avatar-ancillary-upsell
law_id: PRD-6.2
law_title: "Retention Before Expansion"
file_type: example
---

# PRD-6.2 — Retention Before Expansion

## Law Summary

Fix what breaks trust and retention before expanding the product surface. Adding new features to an experience with known, unresolved trust or usability failures does not grow the product — it distributes the damage across a larger footprint.

---

## ✅ COMPLIANT Example

### Situation

Post-purchase support analysis of the instant upsell flow identifies a recurring complaint pattern: passengers who completed a cabin upgrade are confused by the "total due" figure shown before confirmation. The displayed amount does not visually separate the base upgrade price from taxes and fees. Passengers later see a charge on their card that doesn't match the number they remember seeing, generating disputes and support contacts.

**Evidence:**
- Post-upgrade support contact rate: 11% of upgraders contact support within 48 hours of purchase.
- Root cause categorization: 63% of those contacts cite confusion about the charge amount.
- NPS delta: passengers who upgrade and then contact support have an NPS 28 points lower than passengers who upgrade without a support contact.
- Repeat ancillary purchase rate: passengers who contacted support after their first upgrade are 44% less likely to attempt a second ancillary purchase.

**The unresolved problem:** The instant upsell price display does not show a tax breakdown. The equivalent of a `TaxesAndFeesViewModel` that exists in other purchase flows is absent from the `UpgradeYourTripView` / `UpgradeYourTripViewModel` rendering path.

### Compliant Decision

**Fix transparent pricing first.** Add itemized tax and fees display to the instant upsell price confirmation screen before adding any new ancillary offer types to the post-booking surface.

**Rationale under PRD-6.2:**
- The existing feature has a measured trust defect: 11% post-purchase support rate, 44% reduction in repeat ancillary purchase.
- Expanding to new offer types (e.g., preferred seats, in-flight meals) while this trust defect is unresolved means new offer types will inherit the same display pattern, spreading the problem.
- Transparent pricing (BUS-3.6) directly drives repeat ancillary purchase — the primary revenue retention metric for this avatar.
- Fixing the display is also a BUS-3.6 compliance correction: exact price display with tax breakdown is a law requirement, not an enhancement.

**What this enables:** Once transparent pricing is in place and the support contact rate drops to baseline, expansion to new ancillary types lands into an experience that passengers trust. That trust is what drives the retention and repeat purchase rate that makes expansion valuable.

---

## ❌ VIOLATION Example

### Proposed Roadmap

> "We have a backlog of 5 new ancillary offer types to add to the post-booking screen: preferred seat selection, in-flight meal pre-order, lounge day pass, priority boarding, and Wi-Fi purchase. We know the total-due display is confusing, but we want to get these offer types live first to hit our ancillary revenue targets. We'll fix the display issue in a later sprint."

### Why This Violates PRD-6.2

This roadmap explicitly acknowledges a known trust defect and then deprioritizes its fix in favor of feature expansion. PRD-6.2 is violated directly.

**Three compounding failures:**

1. **Trust debt multiplied across five surfaces.** Each new offer type added to the post-booking screen uses the same pricing display infrastructure. Without fixing the tax breakdown display first, all five new offer types will have the same confusing "total due" presentation. The support contact problem doesn't stay at 11% — it scales with offer volume.

2. **Revenue target logic is inverted.** Adding new offer types to an experience with a 44% repeat-purchase suppression effect does not compound ancillary revenue — it dilutes it. Passengers who have a bad first experience with one ancillary are less likely to engage with any ancillary offer. Fixing retention first yields more lifetime ancillary revenue than adding offer types to a leaky retention base.

3. **BUS-3.6 is not a backlog item.** Exact price display with tax breakdown is a law in force for this avatar. Scheduling a compliance correction as "later sprint" work is not a valid tradeoff — it is a compliance deferral. New offer types added before the fix are also non-compliant at launch.

**Correct path:** Fix the tax breakdown display in `UpgradeYourTripView`. Measure support contact rate. Confirm it drops. Then expand to new offer types with confidence that the pricing infrastructure is trustworthy and compliant.
