# Cargo Use Case: Booking Workflow

**Overview:**  
The complete cargo booking workflow from rate quote through pickup confirmation, demonstrating how PRD-1.1 through PRD-5.1 apply to the most common customer journey.

**Personas Involved:**
- Alice (Freight Forwarder)
- Customer shipper
- AA Cargo operations

**Value Delivered:**
- Forwarder can quote and book cargo in < 5 minutes (vs. 30+ minutes currently)
- Shipper gets pickup time confirmation instantly
- AA Cargo captures booking with high accuracy

---

## Workflow Phases

### Phase 1: Discovery (PRD-1.1 & PRD-2.1)

**Objective:** Understand what forwarders and shippers need from a booking experience

**Key Research Findings:**
- 94% of forwarders mention quote speed as #1 pain point
- Current booking process requires 5+ steps and 30+ minutes
- Competitors offer 15-30 second quotes + 2-step booking
- Shipper needs pickup confirmation within 2 minutes of booking

**Skills Applied:**
- [User Journey Mapping](../../../../../agent-skills/skills-by-domain/discovery-research/02-user-journey-mapping.md)

**Output:** PRD-1.1-discovery.md and PRD-2.1-journey.md in examples/

---

### Phase 2: Planning & Design (PRD-3.1 & PRD-4.1)

**Objective:** Define MVP booking feature and roadmap for scaling

**Roadmap Decisions:**
- Q1 2026: Optimize quote speed to <15s (Priority 1.1)
- Q2 2026: Launch API for direct integration (Priority 1.2)
- Q3 2026: Add real-time tracking (Priority 2.1)

**MVP Definition:**
- Quote engine: <15s response, top 50 routes
- 2-step booking: pre-filled form + confirm
- Pickup scheduling: select from available times
- Success criteria: 85%+ booking completion, 40+ NPS

**Skills Applied:**
- [Executable Spec](../../../../../agent-skills/skills-by-domain/product-planning/03-executable-spec.md)
- [Business Domain Modeling](../../../../../agent-skills/skills-by-domain/development-practices/04-business-domain-modeling.md)

**Output:** PRD-3.1-roadmap.md and PRD-4.1-mvp.md

---

### Phase 3: Implementation (ENG-6.1 TDD, ENG-7.1 Vertical Slice)

**Objective:** Build MVP booking feature with high quality and fast delivery

**Vertical Slice:** Complete "quote to booking" with real end-to-end functionality
- Quote API returns price in <15s ✓
- Booking form simplified to 2 steps ✓
- Data persists and flows to operations ✓
- Email confirmation sent ✓

**Testing Approach:**
- Unit tests: pricing logic, form validation
- Integration tests: quote → booking → email flow
- User acceptance tests: 3 pilot forwarders trial MVP

**Skills Applied:**
- [Atomic TDD](../../../../../agent-skills/skills-by-domain/development-practices/06-atomic-tdd.md)
- [Vertical Slice Development](../../../../../agent-skills/skills-by-domain/development-practices/07-vertical-slice-dev.md)
- [Code Review](../../../../../agent-skills/skills-by-domain/development-practices/08-code-review.md)

**Timeline:** 6 weeks (Jan 16 - Feb 27, 2026)

**Quality Gates:**
- 95%+ test coverage on quote/booking logic
- Zero critical bugs in pilot phase
- Quote response time <15s at 95th percentile
- Booking completion rate 85%+

---

### Phase 4: Launch & Measure (PRD-5.1)

**Objective:** Release to production, measure success metrics, iterate

**Launch Plan:**
- Week 1: Pilot with 3 forwarders, daily check-ins
- Week 2-3: Expand to 10 high-volume forwarders
- Week 4+: General availability with GA support

**Success Metrics:**
- Quote time: <15s (95th %ile) ✅ Target achieved
- Booking completion: 85%+
- NPS: 40+
- Repeat usage: 80%+ of pilots use weekly
- Support tickets: <5 per 100 bookings

**Monitoring & Iteration:**
- Daily dashboard: speed, completion rate, errors
- Weekly customer calls: feedback and issues
- Bi-weekly product review: metrics vs. targets
- Monthly retrospective: learnings for next feature

**Go/No-Go Decision (End of Pilot):**
- If all success metrics met: Launch to all customers
- If some metrics missed: Fix and re-pilot
- If MVP assumption wrong: Pivot to alternative

---

## Real Example: First Week of Cargo Booking MVP

**Monday, Feb 16:**
- Launch MVP with Alice (Global Logistics)
- Demo: "Quote in <15s, book in 2 steps"
- Alice books first test shipment successfully
- Quote time: 13.2 seconds ✅
- Time to booking: 1 minute 45 seconds ✅

**Tuesday, Feb 17:**
- Alice uses MVP for 5 real customer quotes
- Quote times: 12.8s, 14.1s, 13.9s, 12.5s, 14.6s (all <15s ✅)
- 4 of 5 quoted shipments converted to bookings
- Completion rate: 80% (target 85%)
- Feedback: "Great speed! One more step could be simpler"

**Wednesday, Feb 18:**
- UX improvement: Combine shipping address + pickup info into one step
- New flow: 1.5-minute average booking time
- Completion rate: 83% (getting closer to 85%)

**Thursday, Feb 19:**
- Add "Save shipment template" feature for repeat routes
- Alice books 3 weekly shipments to NYC, each takes 30 seconds (pre-filled)
- NPS feedback: 8/10 - "Much faster, very smooth"

**Friday, Feb 20:**
- Week 1 summary to Alice: Quote speed excellent, booking smooth, NPS high
- Alice: "Roll this out to all our staff, we'll use it exclusively"
- Early indication: Market fit is strong ✅

---

## Use Case Success Criteria

| Criterion | Target | Actual | Status |
|-----------|--------|--------|--------|
| Quote time (95th %ile) | <15s | 13.8s | ✅ PASS |
| Booking completion | 85%+ | 83% | ⚠️ CLOSE |
| NPS score | 40+ | 42 | ✅ PASS |
| Error rate | <3% | 1.2% | ✅ PASS |
| Support tickets | <0.1/booking | 0.08/booking | ✅ PASS |
| Repeat usage | 80%+ | 9/10 | ✅ PASS |
| **OVERALL** | | | **✅ SUCCESS** |

---

## Lessons Learned

### What Worked
- MVP scope was right: focused on quote + booking, excluded extras
- Speed optimization paid off: every customer mentioned it
- Pilot customer approach: Alice gave daily feedback, caught issues early
- Vertical slice delivery: worked end-to-end from day 1

### What We'd Change
- Booking completion rate slightly below target: could have simpler form
- Mobile experience didn't work well: should have tested earlier
- Pickup scheduling had confusion: tooltips helped but redesign needed

### What's Next
- Expand pilot from 3 to 10 customers (Week of Feb 23)
- Monitor metrics daily (dashboard up and running)
- API integration parallel track (start Feb 23)
- Real-time tracking starting March (Phase 2)

---

## Related Documentation

**Laws Applied:**
- [PRD-1.1: Continuous Discovery](../../../../../laws/product/_domain.yaml)
- [PRD-2.1: User Journey Mapping](../../../../../laws/product/_domain.yaml)
- [PRD-3.1: Roadmap Planning](../../../../../laws/product/_domain.yaml)
- [PRD-4.1: MVP & Product-Market Fit](../../../../../laws/product/_domain.yaml)
- [PRD-5.1: Metrics & Success Definition](../../../../../laws/product/_domain.yaml)

**Related Skills:**
- [Discovery & Research Domain](../../../../../agent-skills/skills-by-domain/discovery-research/)
- [Product Planning Domain](../../../../../agent-skills/skills-by-domain/product-planning/)
- [Development Practices Domain](../../../../../agent-skills/skills-by-domain/development-practices/)

**Similar Use Cases:**
- [Claims Processing Use Case](../claims-processing/README.md)
- [Rate Optimization Use Case](../rate-optimization/README.md)

---

**Last Updated:** February 20, 2026  
**Product:** Cargo & Freight  
**Use Case:** Booking Workflow (Core Journey)  
**Status:** ✅ MVP Complete, Expanding to 10 Customers
