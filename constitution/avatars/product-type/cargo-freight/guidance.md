# Cargo & Freight Product Guidance

Welcome to the American Airlines Cargo & Freight product avatar! This guide helps you apply the Hangar AI Constitution to cargo product decisions.

---

## What We Do

American Airlines Cargo provides international and domestic freight logistics services. We compete on speed, reliability, and integration. Our key differentiators are:

- **Speed:** Quote and booking faster than competitors (target: <15 seconds)
- **Reliability:** On-time delivery, minimal claims, transparent process
- **Integration:** API connectivity for ERP/e-commerce systems
- **Expertise:** Specialized handling for high-value, hazmat, perishable goods

---

## Product Laws for Cargo

> **Full PRD law definitions** are in the [PRD Laws Reference](../../../docs/guides/avatars/prd-laws-reference.md). This section shows cargo-specific applications.

### 1. PRD-1.1: Continuous Discovery

**Reference:** [PRD-1.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-11-continuous-discovery)

**For Cargo specifically:**
- Interview freight forwarders about quote/booking pain points (monthly)
- Analyze shipper requirements for integration and automation
- Monitor competitor capabilities (features, speed, pricing)
- Study exception patterns (delays, claims, mishandled shipments)

**Example:** We discovered forwarders want <15 second quotes because customers call with cargo ready to ship. If quote takes >30 seconds, they call competitor.

---

### 2. PRD-2.1: User Journey Mapping

**Reference:** [PRD-2.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-21-user-journey-mapping)

**For Cargo specifically:**
- Map quote → booking → pickup → delivery → (exception or claim) journey for each persona
- Identify handoff points where errors happen (60% of delays occur at handoffs)
- Track communication channels (phone, web, API, email, SMS)
- Document exception flows (delays, oversells, damage claims)

**Example:** Alice books cargo while on phone with customer. Current flow takes 30 minutes (manual entry errors). We improved to <5 minutes with auto-fill—reducing her booking workload by 40%.

### 3. PRD-3.1: Roadmap Planning

**Reference:** [PRD-3.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-31-roadmap-planning)

**For Cargo specifically:**
- Rank features by customer impact (speed = acquisition, reliability = retention, API = scale)
- Evaluate revenue per feature: Speed (+$2M/year from faster quote), API (+$5M/year from direct integration)
- Assess engineering effort: Speed optimization (6 weeks), API (14 weeks), tracking (8 weeks)
- Sequence to build foundations: Speed first (Q1 2026), then API (Q2 2026), then tracking (Q3 2026)

**Example:** We prioritized speed optimization before API because: (a) speed wins new customers, (b) 80% of pilots are speed-driven, (c) API depends on fast backend infrastructure. Sequence is data-driven, not arbitrary.

---

### 4. PRD-4.1: MVP & Product-Market Fit

**Reference:** [PRD-4.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-41-mvp--product-market-fit)

**For Cargo specifically:**
- Define MVP scope rigorously: In (quote engine ≥13s, booking form, email confirmation) | Out (API, tracking, mobile app)
- Choose pilot customers strategically: 3 high-volume forwarders (500+ bookings/month each) representing different segments
- Measure 4-week pilot using market-fit signals: NPS 40+, repeat rate 80%+, completion rate 85%+, quote speed <15s
- Define decision gates: NPS > 42 → scale to 10 customers | NPS 35-42 → iterate 2 weeks | NPS < 35 → pivot

**Example:** Feb 2026 pilot with Alice, Carlos, Roberto (3 forwarders, 1,800 bookings total). Results: 13.8s quotes, 83% completion, NPS 42. Decision: Scale to 10 customers by April, parallel API development for May launch.

---

### 5. PRD-5.1: Metrics & Success Definition

**Reference:** [PRD-5.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-51-metrics--success-definition)

**For Cargo specifically:**

**Tier 1: Customer Outcomes (Leading Indicators)**
- Quote speed (95th %ile): 13.8s → 12s (30% faster than competitors)
- Booking completion: 83% → 90% (reduce drop-offs)
- NPS: 42 → 50+ (promoter territory)
- Time-to-book: 30 min → 5 min (for forwarders)

**Tier 2: Product Performance (Predictive)**
- Booking error rate: <1% (root cause analysis on all errors)
- Claims rate: <0.2% (damage/loss during handling)
- Support tickets per booking: <0.05 (proactive problem prevention)
- System uptime: 99.9%+ (booking engine reliability)

**Tier 3: Business Impact (Lagging Indicators)**
- Booking volume: 12,000/month (Q1 2026) → 25,000/month (Q3 2026)
- Gross booking revenue: $7.5M/year → $15M/year
- Margin per booking: $500 → $600 (scale efficiencies)
- Customer acquisition cost: <$5K per forwarder
- Lifetime value: $180K per forwarder (3-year retention)
- ROI: 5.2x year 1, 8.1x year 2

---

## For Each Persona: Where to Start

### Alice (Freight Forwarder)

Your journey: Quote → Booking → Pickup → Delivery Tracking → (Exception or Claim)

**Where PRD laws help:**
1. Start with [PRD-1.1 Discovery](examples/PRD-1.1-discovery.md) - understand what you need from us
2. Then [PRD-2.1 Journey](examples/PRD-2.1-journey.md) - see your workflow mapped out
3. Use [PRD-5.1 Metrics](examples/PRD-5.1-metrics.md) - track your experience (NPS, quote time)

**Core need:** Speed (quote) + Reliability (delivery) + Communication (tracking)

---

### Carlos (Direct Shipper)

Your journey: ERP System → Rate → Book → Schedule Pickup → Track → Receive

**Where PRD laws help:**
1. Start with [PRD-2.1 Journey](examples/PRD-2.1-journey.md) - see integration opportunities
2. Then [PRD-3.1 Roadmap](examples/PRD-3.1-roadmap.md) - understand what's coming (API)
3. Use [PRD-5.1 Metrics](examples/PRD-5.1-metrics.md) - understand our reliability

**Core need:** Integration (API) + Automation (system-to-system) + Visibility (tracking)

---

### Roberto (Partner Airline)

Your journey: Flight Scheduled → Update Capacity → Accept Bookings → Optimize Pricing → Departure

**Where PRD laws help:**
1. Start with [PRD-2.1 Journey](examples/PRD-2.1-journey.md) - see capacity workflow
2. Then [PRD-3.1 Roadmap](examples/PRD-3.1-roadmap.md) - real-time capacity updates
3. Use [PRD-5.1 Metrics](examples/PRD-5.1-metrics.md) - track revenue impact

**Core need:** Real-time capacity visibility + Dynamic pricing + Revenue maximization

---

### Diana (Cargo PM - Internal)

Your role: Understand market, prioritize features, measure success

**Where PRD laws help:**
1. Start with [PRD-1.1 Discovery](examples/PRD-1.1-discovery.md) - what do customers really need?
2. Then [PRD-3.1 Roadmap](examples/PRD-3.1-roadmap.md) - prioritize based on impact
3. Then [PRD-5.1 Metrics](examples/PRD-5.1-metrics.md) - measure everything, iterate

**Core need:** Customer insights + Data-driven prioritization + Alignment to business goals

---

## Common Questions

**Q: When do I use PRD-1.1 vs PRD-2.1?**  
A: PRD-1.1 is "why" (what do customers need?). PRD-2.1 is "how" (what's their workflow?). Use 1.1 first to understand needs, then 2.1 to map how you'll serve them.

**Q: Can I skip any laws?**  
A: No. Each law solves a different problem. Skip 1.1 and you build wrong thing. Skip 2.1 and features don't fit workflow. Skip 5.1 and you don't know if you're winning.

**Q: How long does each law take?**  
A: PRD-1.1 (discovery): 2-4 weeks | PRD-2.1 (journey mapping): 1 week | PRD-3.1 (roadmap): 1 week | PRD-4.1 (MVP): 4-8 weeks | PRD-5.1 (metrics): ongoing

**Q: My feature doesn't fit the laws—what do I do?**  
A: It does. Every feature serves a customer need (1.1), fits into workflow (2.1), competes for resources (3.1), has MVP scope (4.1), and has success metrics (5.1). If it doesn't, rethink it.

---

## Related Documentation

**Laws:**
- [PRD-1.1: Continuous Discovery](../../../laws/product/_domain.yaml)
- [PRD-2.1: User Journey Mapping](../../../laws/product/_domain.yaml)
- [PRD-3.1: Roadmap Planning](../../../laws/product/_domain.yaml)
- [PRD-4.1: MVP & Product-Market Fit](../../../laws/product/_domain.yaml)
- [PRD-5.1: Metrics & Success Definition](../../../laws/product/_domain.yaml)

**Personas:**
- [All Cargo Personas](examples/personas.md)

**Use Cases:**
- [Booking Workflow](use-cases/booking-workflow/README.md) - Core journey (Speed optimization)
- [Claims Processing](use-cases/claims-processing/README.md) - Exception handling (Trust)
- [Rate Optimization](use-cases/rate-optimization/README.md) - Revenue maximization (Margin)

**Skills:**
- [Discovery & Research Domain](../../../agent-skills/skills-by-domain/discovery-research/)
- [Product Planning Domain](../../../agent-skills/skills-by-domain/product-planning/)

---

**Last Updated:** February 20, 2026  
**Product:** Cargo & Freight  
**Contact:** Product Team  
**Next Steps:** Review personas, pick your persona journey, read that PRD-N.N example
