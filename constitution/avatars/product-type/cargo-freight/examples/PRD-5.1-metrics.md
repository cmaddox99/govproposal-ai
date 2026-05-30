# Example: Cargo Metrics & Success Definition (PRD-5.1 Metrics & Success)

**Law Reference:** [PRD-5.1: Metrics & Success Definition](../../../../laws/product/_domain.yaml)

**What This Example Shows:**
- How to define KPIs for cargo product across customer, operational, and financial dimensions
- What good metrics look like (measurable, actionable, business-aligned)
- How to establish baselines and targets
- How to use metrics to guide product decisions

---

## Context: Why This Matters for Cargo

Diana (Cargo PM) can't answer "Are we winning?" without clear metrics. Is 15-second quote time good if nobody books? Is high NPS good if revenue is declining? PRD-5.1 metrics ensure we measure what actually matters: did we solve customer problems AND grow business?

**Key Principles from PRD-5.1:**
- Define success across multiple dimensions (customer, operational, financial)
- Choose metrics that drive decisions
- Establish clear baselines and targets
- Monitor regularly and act on signals

---

## Cargo Product Metrics Framework

### Tier 1: Customer/Product Metrics (Most Important)

**Quote Speed (Primary KPI)**
- Metric: Quote response time, 95th percentile
- Current Baseline: 45-60 seconds
- Target: <15 seconds (Q1 2026)
- Why? Speed is #1 forwarder pain point
- Measurement: Server logs, quote request timestamps
- Action Threshold: If >20s, escalate to engineering

**Booking Completion Rate**
- Metric: % of quote-to-booking conversion
- Current Baseline: 35% (many quotes don't convert)
- Target: 60% (Q2 2026)
- Why? More quotes should convert to bookings (easier, faster)
- Measurement: Analytics tracking quote view → booking action
- Action Threshold: If <50%, debug booking friction (survey users)

**Customer NPS (Net Promoter Score)**
- Metric: % Promoters - % Detractors (scale -100 to +100)
- Current Baseline: 25 (forwarders moderately satisfied)
- Target: 45 (Q2 2026)
- Why? NPS correlates with retention and word-of-mouth
- Measurement: Monthly survey, 1-2 questions
- Action Threshold: If stagnant >30 days, investigate reasons

**Repeat Booking Rate**
- Metric: % of forwarders who book again within 30 days
- Current Baseline: 60% (repeat users, but not frequent)
- Target: 80% (Q2 2026)
- Why? Frequency = loyalty = revenue growth
- Measurement: User tracking, bookings per forwarder per month
- Action Threshold: If declining, diagnose why (bad experience? competitor?)

**On-Time Delivery Rate**
- Metric: % of shipments delivered within promised time
- Current Baseline: 92% (operations baseline)
- Target: 98% (Q3 2026)
- Why? Reliability is essential (shipper trust, claims reduction)
- Measurement: Delivery timestamp vs. promised time
- Action Threshold: If <95%, escalate to operations

---

### Tier 2: Operational Metrics (Enable Success)

**Booking Error Rate**
- Metric: % of bookings with errors (wrong route, weight, special handling)
- Current Baseline: 8% (manual entry errors)
- Target: 1% (API + better UX, Q2 2026)
- Why? Errors → rework → delays → claims
- Action Threshold: If >3%, debug form UX or API validation

**Claims Rate (per Shipment)**
- Metric: % of shipments resulting in claim
- Current Baseline: 0.5% (industry standard, ~$5K cost per claim)
- Target: 0.2% (better handling, communication, Q3 2026)
- Why? Claims destroy profit, relationship
- Action Threshold: If >0.3%, investigate top claim reasons

**Customer Support Tickets per Booking**
- Metric: Average support tickets per shipment
- Current Baseline: 0.15 tickets/booking
- Target: 0.05 tickets/booking (Q2 2026)
- Why? More self-service, fewer calls = cost savings + better experience
- Action Threshold: If >0.08, debug top ticket reasons (tracking, pickups, claims)

**API Integration Count**
- Metric: # of customers with active API integrations
- Current Baseline: 0 (MVP starting Feb 2026)
- Target: 10+ by June 2026, 50+ by Dec 2026
- Why? API integrations are strategic (channel to direct shippers)
- Action Threshold: If <3 by May, investigate API issues

---

### Tier 3: Business Metrics (Revenue & Growth)

**Gross Booking Revenue**
- Metric: Total $ value of cargo booked via AA Cargo
- Current Baseline: $5M/year (2025 estimated)
- Target: $7.5M/year (Q4 2026, +50% growth)
- Why? Revenue directly tied to business success
- Measurement: Booking database, rate × weight
- Action Threshold: If trending <$6M run-rate in Q2, diagnose

**Booking Volume**
- Metric: # of shipments booked per month
- Current Baseline: 8,000 bookings/month
- Target: 12,000 bookings/month (Q4 2026, +50%)
- Why? Volume growth + margin improvements = profit
- Action Threshold: If stagnant, investigate competition, pricing

**Average Margin per Booking**
- Metric: (Revenue - Operating Cost) / Booking
- Current Baseline: $400/booking
- Target: $500/booking (Q3 2026, better pricing + lower cost)
- Why? Margin directly impacts profit
- Components: Rate - operations cost - customer support
- Action Threshold: If declining, investigate cost drivers

**Customer Lifetime Value (LTV)**
- Metric: Total expected revenue from average customer - service cost
- Current Baseline: $8,000 LTV (estimated 20 bookings over 2 years)
- Target: $12,000 LTV (Q4 2026, more bookings + retention)
- Why? LTV guides customer acquisition budget
- Measurement: Cohort analysis, track customers over time

**Customer Acquisition Cost (CAC)**
- Metric: Marketing/sales spend per new customer acquired
- Current Baseline: $500 CAC (referral-based, low spend)
- Target: <$400 CAC (Q3 2026, focus efficiency)
- Why? LTV/CAC ratio should be >3:1 for healthy business
- Action Threshold: If >$600, reduce spend or improve conversion

---

## Real-Time Monitoring Dashboard

**Diana (PM) sees every morning:**

```
┌─────────────────────────────────────────────────────────┐
│ Cargo Product Dashboard (Daily View)                    │
├─────────────────────────────────────────────────────────┤
│ Quote Speed                                             │
│  Current: 14.2s (95th %ile) ✅ Target: <15s            │
│  Trend: ↓ -2.1s vs last week (good!)                   │
│                                                         │
│ Booking Completion Rate                                 │
│  Current: 52% ⚠️ Target: 60%                            │
│  Trend: ↑ +3% vs last week                              │
│  Action: Still below target, debug form friction       │
│                                                         │
│ NPS Score                                               │
│  Current: 38 ⚠️ Target: 45                              │
│  Trend: ↑ +2 pts vs last month                          │
│  Comments: "Faster quoting!" "Still no tracking"       │
│                                                         │
│ Daily Bookings                                          │
│  Current: 280 bookings/day (est. $112K revenue/day)   │
│  Target Pace: $3.3M/month → $39.6M/year                │
│  Trend: On pace for 12,000/month goal ✅              │
│                                                         │
│ Critical Alerts                                         │
│  ⚠️ Booking errors up to 3.2% (was 2.1%)              │
│  ⚠️ Claims spike on hazmat (investigate)               │
│  ⚠️ 1 major customer delayed payment                   │
└─────────────────────────────────────────────────────────┘
```

---

## Decision Framework: How Metrics Guide Action

### When to Celebrate
- Quote speed hitting targets consistently
- NPS trending upward (customers happier)
- Repeat booking rate strong (loyalty working)
- Revenue pacing ahead of forecast

### When to Investigate
- Booking completion rate declining (UX problem?)
- Support tickets spiking (broken feature?)
- Claims rate increasing (operational issue?)
- LTV declining (retention problem?)

### When to Pivot
- NPS stuck at 30 despite features shipping (wrong priorities?)
- Booking volume declining despite marketing spend (competitive threat?)
- Margin eroding despite price increases (cost problem?)

---

## Quarterly Review: How to Use Metrics

**End of Q1 (March 31):**
1. Compare actual metrics to Q1 targets
2. Analyze discrepancies (why are we ahead/behind?)
3. Celebrate wins and learn from misses
4. Adjust Q2 roadmap based on learnings

**Example Q1 Retrospective:**
```
What We Planned     | What Happened      | Lesson
─────────────────────────────────────────────────────────
Quote speed <15s    | Achieved 14.2s ✅ | Great! Optimization paid off
Booking comp 60%    | Got to 52% ⚠️      | UX friction too high, need redesign
API integrations 3+ | Got 0 so far ⚠️    | API slower to launch, adjust timeline
On-time delivery %  | Maintained 92% ✅  | Operations stable
```

---

## When to Apply PRD-5.1 for Cargo

✅ **Use this law when:**
- Launching new feature (define success metrics first)
- Making product decision (what data matters?)
- Quarterly/annual planning (reset targets based on learnings)
- Explaining success to leadership (use metrics, not opinions)

❌ **Don't skip even if:**
- "Success is obvious" (define metrics anyway for clarity)
- "We don't have time for dashboards" (metrics guide direction)
- "Engineering doesn't need metrics" (they do—helps prioritize)

---

## Related Skills

**Skills that complement PRD-5.1:**
- [Business Domain Modeling](../../../../agent-skills/skills-by-domain/development-practices/04-business-domain-modeling.md)
- [Business Rules Definition](../../../../agent-skills/skills-by-domain/development-practices/05-business-rules.md)

**Related Laws:**
- [PRD-3.1: Roadmap Planning](../../../../laws/product/_domain.yaml) - Use metrics to prioritize
- [PRD-4.1: MVP](../../../../laws/product/_domain.yaml) - Metrics validate market fit

---

**Token Count:** 791 tokens  
**Last Updated:** February 20, 2026  
**Author:** Cargo Product Team  
**Domain:** Cargo & Freight  
**Law:** PRD-5.1: Metrics & Success Definition
