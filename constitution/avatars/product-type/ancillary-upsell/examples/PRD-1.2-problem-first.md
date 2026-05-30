---
avatar: avatar-ancillary-upsell
law_id: PRD-1.2
law_title: "Problem-First Development"
file_type: example
---

# PRD-1.2 — Problem-First Development

## Law Summary

Define and validate the problem before designing a solution. The problem statement must include who is affected, what the friction is, and why it matters to the business. Solution design follows; it does not precede.

---

## ✅ COMPLIANT Example

### Context

The bag purchase post-booking flow in `bags-ios` (213 swift files) shows a confirmed pattern of high abandonment at the price display step.

### Problem Statement

**52% of passengers who initiate bag purchase post-booking abandon the flow after the price is shown.** Exit surveys and session recordings indicate that passengers are surprised by the displayed price. Funnel analytics show that the abandonment spike occurs specifically on the screen where the bag fee is displayed, not at the payment entry step.

**Root cause hypothesis:** The bag purchase screen displays only the app price (e.g., $35 per bag) without contextual anchoring against the at-airport price ($40 per bag at check-in counter). Passengers who don't know the at-airport price have no reference point to evaluate whether the app price is a deal or a penalty. Without that comparison, a $35 fee triggers hesitation rather than conversion.

**Supporting evidence:**
- Funnel analytics: 52% drop-off at price display step over trailing 90 days, across all fare classes.
- Session recordings: median time-on-screen before abandon is 12 seconds — consistent with price shock, not deliberation.
- Exit survey (n=1,240): 38% of abandoners cited "didn't know if the price was fair" as primary reason.
- Competitive benchmark: Three peer airlines display at-airport comparison pricing on their bag purchase screens; their post-booking bag attach rates are 15–22 points higher than current baseline.

**Business impact:** Post-booking bag purchase is a $X ancillary revenue line. A 10-point improvement in conversion translates to approximately $Y incremental annual revenue (internal model, available in data room).

### Proposed Direction (follows from problem)

Investigate adding at-airport price comparison framing to the `bags-ios` pricing display surface ("$35 in app vs. $40 at the airport"). Validate the hypothesis in a controlled experiment before full rollout. Do not change the price — change the context.

**What this is not:** This is not a pricing strategy change, a recommendation engine, or a personalization initiative. It is a contextual anchoring test grounded in the measured abandonment problem.

---

## ❌ VIOLATION Example

### Proposed Initiative

> "Build a bag purchase recommendation engine with personalized pricing for the post-booking flow. Use passenger history, route demand, and AAdvantage tier to surface dynamic bag price offers."

### Why This Violates PRD-1.2

This proposal begins with a solution — a recommendation engine with personalized/dynamic pricing — without articulating any validated problem. There is no evidence of what passenger pain point this addresses. There is no measurement of current abandonment, no diagnosis of why passengers are or are not buying bags, and no hypothesis connecting personalized pricing to an identified friction.

Starting with the solution inverts the product development process. Building a recommendation engine to solve an undefined problem risks:

1. Engineering investment in infrastructure that doesn't move the target metric.
2. Complexity debt in `bags-ios` and `mobile-ancillary-bff` that must be maintained regardless of outcome.
3. BUS-3.6 risk: personalized pricing surfaces must still show exact, tax-inclusive prices — a constraint that dynamic pricing architectures frequently violate in their first iteration.
4. No baseline to measure against, so the team cannot know if the initiative worked.

**Correct path:** Identify the specific problem (e.g., abandonment at price display), gather evidence, form a hypothesis, then evaluate whether personalized pricing is the right solution for that specific problem.
