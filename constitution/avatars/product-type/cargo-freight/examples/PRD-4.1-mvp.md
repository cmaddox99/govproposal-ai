# Example: Cargo MVP & Product-Market Fit (PRD-4.1 MVP & PMF)

**Law Reference:** [PRD-4.1: MVP & Product-Market Fit](../../../../laws/product/_domain.yaml)

**What This Example Shows:**
- How to define minimum viable cargo product to test market fit
- What features go IN MVP and what stays OUT
- How to validate market fit with early users
- How to interpret feedback and decide on next phase

---

## Context: Why This Matters for Cargo

American Airlines Cargo is entering the fast-booking market against established competitors. Rather than build complete system and hope customers use it, we define small MVP to validate 2 critical assumptions: (1) Forwarders actually care about 15-second quotes, and (2) They'll switch loyalty for it. PRD-4.1 MVP/PMF ensures we test these before investing 6-12 months of engineering.

**Key Principles from PRD-4.1:**
- Define MVP scope (in/out features)
- Identify must-validate assumptions
- Choose early-adopter customer segment
- Measure market fit signals

---

## Cargo Fast-Booking MVP

### MVP Scope: What's IN

**Must-Have (to test core hypothesis):**
1. **Quote Engine** - Get freight rate in < 15 seconds
   - Input: Shipment details (weight, dimensions, origin, destination)
   - Output: Rate options ranked by speed/price/reliability
   - Constraint: Must work for top 50 routes (80% of volume)

2. **Quick Booking** - Book in 2-3 steps (vs. current 5+)
   - Pre-fill customer info from previous bookings
   - One-click to book best option
   - Instant confirmation

3. **Pickup Scheduling** - Schedule within 1-2 steps
   - Propose available pickup times
   - Accept or propose alternative
   - Confirmation and pickup number

4. **Booking Confirmation** - Email confirmation with all details
   - Shipment reference number
   - Rate breakdown
   - Pickup time and location
   - Exception contact info

**Success Metrics for MVP:**
- Quote time: 95th percentile < 15 seconds ✓ Critical
- Booking completion: 85%+ of started bookings finish ✓ Critical
- Customer willingness to repeat: 80%+ say "yes" ✓ PMF signal
- Booking volume: 50+ bookings in pilot (4-week window)

---

### MVP Scope: What's OUT (Phase 2+)

**Nice-to-Have (excluded to keep scope small):**
- [ ] API integration (Phase 2: add APIs)
- [ ] Real-time tracking (Phase 2: add tracking)
- [ ] Pickup integration with actual dispatch system (Phase 2: integrate)
- [ ] Dynamic pricing (Phase 3: add smarter pricing)
- [ ] Mobile app (Phase 2: mobile-web first)
- [ ] Third-party carrier options (Future: multi-carrier)
- [ ] Hazmat documentation (MVP simple shipments only)
- [ ] Claims portal (Post-MVP: add claims)

**Why exclude?**
- Each adds 2+ weeks of engineering
- Complications don't change core test (speed = differentiation?)
- Can add after validating MVP

---

## MVP Validation Plan

### Customer Segment: Top 10 Forwarders

**Why these customers?**
- Account for 40% of current booking volume
- Already use our system (so baseline familiar)
- Motivated to test faster option (competitors are faster)
- Vocal enough to give clear feedback

**Pilot Participants:**
1. Alice's Global Logistics (international)
2. FastShip Express (domestic high-volume)
3. [8 other high-volume forwarders]

**Duration:** 4 weeks (Feb 16 - Mar 16, 2026)

---

### Validation Approach

**Week 1: Onboard 3 Pilot Customers**
- Live demo of MVP
- Training on quick-booking flow
- Set expectations: "This is early, we want feedback"
- Daily check-in calls to address issues

**Week 2-3: Monitor and Learn**
- Track usage (quote time, booking success rate)
- Observe behavior (which features used, which skipped?)
- Gather feedback (weekly calls with each customer)
- Collect data on satisfaction (NPS survey midpoint)

**Week 4: Analyze and Decide**
- Review metric targets vs. actuals
- Identify what worked and what didn't
- Get explicit market fit signal: "Would you use this in production?"

---

### Market Fit Validation Criteria

**Go / No-Go Decision Gates:**

| Criterion | Target | Actual | Go? |
|-----------|--------|--------|-----|
| Quote time (95th %ile) | <15s | ? | ? |
| Booking completion rate | 85%+ | ? | ? |
| NPS score | 40+ | ? | ? |
| Repeat usage | 80%+ would use again | ? | ? |
| Willingness to pay | Same price or premium | ? | ? |
| Implementation questions | <5 issues per customer | ? | ? |

**Go Decision:** 5+ criteria met → Proceed to full build (Phase 2)

**No-Go Decision:** <4 criteria met → Pivot (e.g., add API, reduce price, improve UX)

---

## Expected MVP Results

### Best Case: Market Fit Signal

```
Scenario: MVP succeeds, forwarders love it
├─ Quote time: 12 seconds (beats target)
├─ Booking: 92% completion (beats 85% target)
├─ NPS: 45 (exceeds 40 target)
├─ Repeat usage: 9/10 customers say "we'd use this daily"
└─ Alice: "Finally! This is what we've been asking for"

Decision: GREEN LIGHT - Proceed to full Phase 2 build
Next: Scale from 10 customers → 100+ by June

Business Impact:
├─ Validated 15-second quote is real differentiator
├─ Proven forwarders will switch carriers for speed
└─ Estimated $2M revenue from faster conversion in Y1
```

### Realistic Case: Good Signals with Refinement

```
Scenario: MVP works well, but UX needs improvement
├─ Quote time: 14 seconds (meets target)
├─ Booking: 81% completion (below 85% target)
├─ NPS: 38 (below 40 target)
├─ Repeat usage: 7/10 would use
└─ Alice: "It's fast, but the interface is confusing"

Decision: YELLOW LIGHT - Proceed with improvements
Next: 2-week sprint on UX, launch Phase 1.5 in March

Changes:
├─ Simplify booking form (remove confusion)
├─ Add tooltips and help context
├─ Better error messages

Results: Expected 85%+ completion, NPS 42+
```

### Risk Case: Speed Improvement Insufficient

```
Scenario: MVP is fast, but doesn't change behavior
├─ Quote time: 14 seconds (meets target)
├─ Booking: 45% completion (far below 85% target)
├─ NPS: 25 (far below 40 target)
├─ Repeat usage: 3/10 would use
└─ Alice: "It's faster, but not significantly better than competitors"

Decision: RED LIGHT - Pivot strategy
Next: Pause booking MVP, investigate other differentiators

Alternative approaches:
├─ Pivot 1: Focus on API integration (Carlos wants this)
├─ Pivot 2: Focus on real-time tracking (all personas need)
├─ Pivot 3: Focus on dynamic pricing (PALs motivated)

Learning: Speed alone isn't enough—need multiple differentiators
```

---

## MVP Lessons & Decisions

### Key Assumption: Speed is the #1 Decision Driver
**Tested in MVP:** Yes (quote time beats competitors)
**Market fit signal:** 80%+ of forwarders prioritize speed in feature choice

**If validated:** Double down on speed in Phase 2 (mobile, API, more routes)  
**If not validated:** Combine speed with other features (tracking, pricing, integrations)

---

### Key Assumption: Quick Booking Reduces Friction
**Tested in MVP:** Yes (2-step booking vs. 5-step old process)
**Market fit signal:** Completion rate 85%+ suggests UX works

**If validated:** Keep simple interface, expand features gradually  
**If not validated:** Redesign interface or add more options

---

## When to Apply PRD-4.1 for Cargo

✅ **Use this law when:**
- Launching new product or major feature (test before full build)
- Entering new market or customer segment (validate need first)
- Making significant bet (reduce risk with MVP)
- Uncertain if customers really want what we're building

❌ **Don't skip even if:**
- "We know customers want this" (validate assumptions explicitly)
- "Time to market is critical" (MVP saves time vs. wrong big build)
- "We're under budget pressure" (MVP is cheaper than wrong direction)

---

## Related Skills

**Skills that complement PRD-4.1:**
- [Executable Spec](../../../../agent-skills/skills-by-domain/product-planning/03-executable-spec.md)
- [Business Domain Modeling](../../../../agent-skills/skills-by-domain/development-practices/04-business-domain-modeling.md)

**Related Laws:**
- [PRD-3.1: Roadmap Planning](../../../../laws/product/_domain.yaml) - Decide what to build
- [PRD-5.1: Metrics](../../../../laws/product/_domain.yaml) - Measure success

---

**Token Count:** 768 tokens  
**Last Updated:** February 20, 2026  
**Author:** Cargo Product Team  
**Domain:** Cargo & Freight  
**Law:** PRD-4.1: MVP & Product-Market Fit
