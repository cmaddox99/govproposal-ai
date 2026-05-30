---
avatar: avatar-manage-trip
law_id: PRD-1.2
law_title: "Problem-First Development"
file_type: example
---

# PRD-1.2 Problem-First Development — Manage Trip

## The Law

Before any solution is designed or scoped, the team must articulate a validated
problem statement supported by evidence. Feature work that begins with a
proposed UI or technical approach violates PRD-1.2.

---

## ✅ COMPLIANT Example — Lap Infant Addition

### Problem Statement (written before any solution work)

> "Parents who book flights and later realize they are traveling with an infant
> under age 2 currently have no self-service path to add that infant to the
> reservation. They must call the AA reservations line."

### Supporting Evidence

| Signal | Data |
|--------|------|
| Call center tagging | 23% of families attempting lap infant modification contact the call center within 48 hours of booking |
| Session recordings (FullStory, Q3 2025) | Users who tap the reservation detail screen spend avg. 3.4 min searching for an "add passenger" option before abandoning |
| App Store reviews | 47 1-star reviews in 90 days cite inability to add a lap infant without calling |
| Call center cost | Each lap infant call costs $8.40 in agent handle time; 11,200 calls/month = $94,080/month |

### Problem Statement (validated)

> Parents booking domestic flights cannot add a lap infant through the iOS app
> after completing their initial booking. This forces a phone call, increases
> support costs by ~$94K/month, and creates friction that degrades post-purchase
> satisfaction scores.

### What Happened Next (PRD-1.2 compliant sequence)

1. Problem statement reviewed and signed off at Stage A discovery gate
2. Persona research validated that the "Family Traveler" segment is the primary
   actor (confirmed: 68% of lap infant callers had booked within the past 7 days)
3. Solution design (`LapInfantViewModel`, `LapInfantInputViewModel`,
   `LapInfantEligibilityEndpoint`) was scoped only after Stage A closed

This is compliant because the problem — with quantified evidence — was fully
articulated and reviewed before any module design began.

---

## ❌ VIOLATION Example — Lap Infant Addition

### What the Team Did Instead

A product manager opened a Jira epic titled:

> "Build lap infant add-on screen in My Trips"

The epic description read:

> "We should add a screen where users can type in infant details and submit. The
> screen should match the existing passenger details UI pattern. Engineering can
> reuse the AddLapInfantEndpoint we already have. Let's get this in the next
> sprint."

No call volume data was cited. No FullStory analysis was referenced. No
problem statement was written. No Stage A gate was opened.

### Why This Violates PRD-1.2

- The epic begins with a solution ("build a screen") rather than a problem
- There is no evidence that this is the correct problem to solve, or that it is
  large enough to justify a sprint
- The team cannot measure success because no baseline was established
- If the feature ships and call volume does not drop, there is no hypothesis to
  falsify — the team cannot learn

### The Correct Correction

Before writing any spec or opening any engineering tickets:

1. Pull call center tags to quantify lap infant call volume
2. Run FullStory sessions to confirm users are searching and failing
3. Write a problem statement with a measurable impact hypothesis
4. Submit the problem statement for Stage A gate review

Only after gate approval should `LapInfantInputViewModel` or any other module
design appear in planning.
