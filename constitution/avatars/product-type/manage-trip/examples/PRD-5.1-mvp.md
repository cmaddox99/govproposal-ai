---
avatar: avatar-manage-trip
law_id: PRD-5.1
law_title: "MVP Law"
file_type: example
---

# PRD-5.1 MVP Law — Manage Trip

## The Law

An MVP must be the smallest shippable increment that validates the core
hypothesis. It must have a measurable success criterion and a defined
learning goal. An MVP that ships every anticipated feature is not an MVP —
it is a full release with renamed scope.

---

## ✅ COMPLIANT Example — Special Service Request Management

### Hypothesis to Validate

> If we expose a self-service SSR flow for the two highest-volume request types
> (wheelchair assistance and dietary restrictions), travelers will complete the
> request in-app at a rate ≥ 60%, reducing inbound SSR call volume.

### MVP Definition

**In scope:**
- Wheelchair assistance request (WCHR, WCHS, WCHC codes)
- Special meal request (VGML, KSML, DBML — 3 dietary variants)
- Entry point: single "Special Services" row added to `ReservationSummaryView`
- Backend: new `aa-ct-mobile-manage-bff` endpoint wrapping existing PSS SSR API
- Confirmation: inline success state (no separate confirmation screen)

**Explicitly out of scope for MVP:**
- Unaccompanied minor (UMNR) — requires separate eligibility logic
- Emotional support animal documentation flow
- SSR history / previously submitted requests view
- Push notification on SSR confirmation
- Remaining 9 SSR types

**Measurable success criteria:**
1. SSR completion rate (add SSR → BFF success response) ≥ 60% within 30 days
2. Inbound SSR call volume (call center tag "special services request") drops
   ≥ 10% in the 30-day post-launch window vs. 30-day pre-launch baseline
3. Error rate on the new BFF endpoint < 2%

**Learning goal:** Confirm that travelers can and will self-serve SSRs
in-app rather than calling — before investing in the full 15-SSR catalogue.

This is compliant: two SSR types, one new UI row, one BFF endpoint, three
measurable outcomes, one clear learning question.

---

## ❌ VIOLATION Example — Special Service Request Management

### What the Team Scoped as Their "MVP"

A product manager presented the following as an "MVP" in sprint planning:

> "For the MVP we'll build the full SSR management screen covering all 15
> service request types. We'll also add an SSR history tab so travelers can see
> past requests. We'll include a push notification when the airline confirms the
> SSR. And we'll add a banner on the My Trips list screen showing a reminder if
> the traveler has a flight in 7 days and hasn't submitted SSRs."
>
> "We can measure success with App Store rating after launch."

### Why This Violates PRD-5.1

- 15 SSR types is the full feature, not a minimum viable increment
- SSR history view is a separate feature with its own problem statement
- The push notification system is a distinct dependency with its own risk profile
- The reminder banner on `MyTripsView` is a new acquisition/nudge feature, not
  part of the SSR core hypothesis
- App Store rating is a lagging, low-signal metric that cannot be attributed to
  any specific SSR change

### The Harm

The team will spend 8–12 weeks building scope that is not needed to answer the
core question: will travelers self-serve SSRs? If completion rates are low, the
team has no way to isolate which of the five features caused the problem. If
completion rates are high, the extra 8 weeks were waste.

### The Correct Correction

Scope to two SSR types. Ship. Measure completion rate vs. call volume. If the
hypothesis is validated, expand to additional SSR types with evidence that
self-service works. Build SSR history only after confirming that travelers
return to view past requests.
