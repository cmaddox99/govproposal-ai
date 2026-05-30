# Example: Cargo Roadmap Planning (PRD-3.1 Roadmap Planning)

**Law Reference:** [PRD-3.1: Roadmap Planning](../../../../laws/product/_domain.yaml)

**What This Example Shows:**
- How to prioritize cargo features using customer impact × business value × effort
- How to sequence features across quarters to manage risk
- How to communicate roadmap to different stakeholders
- How discovery findings drive prioritization decisions

---

## Context: Why This Matters for Cargo

American Airlines Cargo has many potential improvements: speed, API integration, real-time tracking, dynamic pricing, mobile apps, etc. With limited engineering resources, we must prioritize ruthlessly. PRD-3.1 roadmap planning ensures we tackle highest-impact problems first, in order that maximizes learning and minimizes risk.

**Key Principles from PRD-3.1:**
- Rank by customer impact, revenue potential, and feasibility
- Create transparent roadmap aligned to business goals
- Sequence work to enable future features
- Communicate clearly to customers and teams

---

## Cargo Prioritization Framework

### Ranking Criteria

**Customer Impact (40% weight):**
- How many customers affected? (Breadth)
- How painful is the problem? (Depth)
- Would this change buying decisions? (Switching risk)

**Business Value (40% weight):**
- Revenue impact (new bookings, higher margin)
- Retention impact (churn reduction)
- Operational efficiency (cost savings)

**Engineering Effort (20% weight):**
- Development complexity (months)
- Architectural changes needed?
- Operational support required?

---

## Feature Prioritization: Cargo Q1-Q3 2026

### TIER 1: Must-Do (High Customer Impact + High Business Value + Feasible)

#### Feature 1.1: Reduce Quote Response Time (15s target)
**Customer Impact:** 94% of forwarders mention speed  
**Business Value:** Estimated 20% of quotes currently lost to competitor  
**Effort:** Medium (optimize pricing engine, caching)  
**Priority Score:** 95/100

**Why First?** 
- Solves #1 pain point for all 3 forwarder personas
- Quick engineering win (6 weeks)
- Revenue impact: +15% quote → booking conversion

**Implementation:** Optimize pricing query (from 25s to 5s), add caching, pre-fill customer data

**Success Metric:** Average quote time < 15s (target 95th percentile)

---

#### Feature 1.2: API for Programmatic Booking
**Customer Impact:** Direct shippers + programmatic partners (underserved segment)  
**Business Value:** Unlock ERP/e-commerce integrations (15-20% volume increase)  
**Effort:** High (new architecture, documentation, support)  
**Priority Score:** 88/100

**Why Early?** 
- Enables Carlos (direct shipper) to integrate fully
- High revenue potential (new customer segment)
- Foundation for future integrations

**Implementation:** REST API for quotes and bookings, webhook notifications, documentation

**Success Metric:** 10+ partners integrated, 5% of bookings via API within 6 months

---

### TIER 2: High Value (Strong Business Case + Medium Effort)

#### Feature 2.1: Real-Time Tracking with Notifications
**Customer Impact:** All personas need shipment visibility  
**Business Value:** Reduces support tickets (fewer "where is my shipment" calls)  
**Effort:** Medium (integrate with operations systems, SMS/email)  
**Priority Score:** 82/100

**Why Q2?**
- Builds on API infrastructure from 1.2
- Addresses exception handling pain
- Improves customer satisfaction

**Implementation:** Real-time status updates, SMS/email alerts, webhook notifications

**Success Metric:** NPS +5 points, support tickets -20%

---

#### Feature 2.2: Dynamic Rate Adjustment
**Customer Impact:** Roberto (PAL) needs real-time pricing  
**Business Value:** Maximize revenue per flight (2-5% margin improvement)  
**Effort:** High (pricing engine redesign, data science)  
**Priority Score:** 78/100

**Why Later?**
- Requires stable API and tracking infrastructure
- Good to combine with Feature 2.1

**Implementation:** Demand-based pricing, capacity signals, automatic rate updates

**Success Metric:** Average margin per shipment +2-3%

---

### TIER 3: Strategic (High Impact but Longer Horizon)

#### Feature 3.1: Mobile-Optimized Booking
**Customer Impact:** Alice often books from mobile (on phone with customer)  
**Business Value:** Convenience (stickiness), higher booking rate on mobile  
**Effort:** Medium  
**Priority Score:** 72/100

**Why Q3/Q4?**
- Wait for API stability and feedback
- Mobile improvements less critical than speed
- Can leverage web improvements

---

#### Feature 3.2: Claims Portal with Transparency
**Customer Impact:** Exception handling pain point  
**Business Value:** Faster resolution, improved trust  
**Effort:** High (new system, integration with claims team)  
**Priority Score:** 68/100

**Why Later?**
- Lower volume (only exception cases)
- Requires organizational change (claims process)
- Important but not urgent

---

## Roadmap by Quarter

```
Q1 2026 (Jan-Mar):
├─ Feature 1.1: Quote Speed Optimization (COMPLETE by Feb)
│  └─ Target: 15s quote time, 95th percentile
│  └─ Success: 20% reduction in lost quotes to competitor
│
├─ Feature 1.2: API Foundation (Design/Build Jan-Mar, Launch Apr)
│  └─ Parallel track: Design API contract with top 3 partners
│  └─ Success: API contracts signed, 3 pilots ready
│
└─ Feature 2.1: Tracking Infrastructure (Build Mar-Apr)
   └─ Integrate with operations systems
   └─ Success: Tracking available for 80% of shipments

Q2 2026 (Apr-Jun):
├─ Feature 1.2: API Launch (Complete integration, support)
│  └─ Partner onboarding, documentation, SDKs
│  └─ Success: 3+ partners live, 100+ API calls/day
│
├─ Feature 2.1: Real-Time Tracking (Complete, launch Jun)
│  └─ SMS/email notifications, customer portal
│  └─ Success: Real-time tracking for 90%+ shipments
│
└─ Feature 2.2: Dynamic Pricing (Design/Pilot)
   └─ Data science work, algorithm development
   └─ Success: Pilot running on 1 route

Q3 2026 (Jul-Sep):
├─ Feature 2.2: Dynamic Pricing (Complete, full launch)
│  └─ All routes, real-time adjustment
│  └─ Success: Margin +2-3% vs Q2
│
├─ Feature 3.1: Mobile Optimization (Build/Test)
│  └─ Mobile-friendly booking, Android/iOS
│  └─ Success: Mobile bookings +50%
│
└─ Platform: Internal Dashboards
   └─ KPI dashboards for product and operations teams
   └─ Success: Daily insights on speed, reliability, revenue

Q4 2026 (Oct-Dec):
├─ Feature 3.2: Claims Portal (Design/Pilot)
│  └─ Online claims tracking, self-service updates
│  └─ Success: Pilot with top 3 forwarders
│
└─ Strategic: Planning next wave
   └─ Customer interviews, competitive analysis
   └─ Success: Q1 2027 roadmap locked
```

---

## Dependencies & Sequencing Rationale

```
Order Matters: Why these sequences?

1. Speed (1.1) before APIs (1.2)?
   → Speed is easier and has immediate ROI
   → API can launch anytime, but speed is more urgent pain

2. APIs (1.2) before Tracking (2.1)?
   → Tracking needs notifications (SMS/webhook)
   → API provides webhook foundation
   → Partners can integrate tracking data

3. Tracking (2.1) before Dynamic Pricing (2.2)?
   → Pricing needs real-time operations data
   → Tracking infrastructure provides that
   → Reduces risk of pricing without visibility

4. Core features (Tier 1-2) before Mobile (3.1)?
   → Speed/API/Tracking solve core problems
   → Mobile is convenience layer
   → Can wait until core is stable
```

---

## Roadmap Communication

### For Customers (Forwarders, Shippers, PALs)
> "We're focused on speed first (your #1 need), then integrations, then visibility. We'll launch faster quoting in February, API access in April, and real-time tracking in June. Here's how each helps you."

### For Executive Leadership
> "Q1-Q3 roadmap will drive 20% increase in quote conversion (speed), open new ERP/e-commerce segment (API), reduce support costs (tracking), and improve margin 2-3% (dynamic pricing). Estimated net revenue impact: +$5M annually."

### For Engineering Team
> "Clear quarterly priorities with success metrics. Each feature has clear done-criteria and measurement. Customer interviews show we're solving real problems. Ship speed, measure impact, learn, iterate."

---

## When to Apply PRD-3.1 for Cargo

✅ **Use this law when:**
- Planning roadmap (any horizon: quarterly, annual)
- Deciding between competing features (trade-offs)
- Communicating priorities to team/customers
- Allocating resources (where to invest engineering time)

❌ **Don't skip even if:**
- "It's obvious what's most important" (prioritize explicitly)
- "Customers all want the same thing" (they don't—different personas, different needs)
- "We have unlimited resources" (you never do—prioritize anyway)

---

## Related Skills

**Skills that complement PRD-3.1:**
- [Business Domain Modeling](../../../../agent-skills/skills-by-domain/development-practices/04-business-domain-modeling.md)
- [Business Rules Definition](../../../../agent-skills/skills-by-domain/development-practices/05-business-rules.md)

**Related Laws:**
- [PRD-1.1: Continuous Discovery](../../../../laws/product/_domain.yaml) - Research to inform priorities
- [PRD-2.1: User Journey Mapping](../../../../laws/product/_domain.yaml) - Map features to journeys

---

**Token Count:** 797 tokens  
**Last Updated:** February 20, 2026  
**Author:** Cargo Product Team  
**Domain:** Cargo & Freight  
**Law:** PRD-3.1: Roadmap Planning
