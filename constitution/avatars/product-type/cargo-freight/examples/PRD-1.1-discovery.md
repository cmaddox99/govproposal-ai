# Example: Cargo Discovery Research (PRD-1.1 Continuous Discovery)

**Law Reference:** [PRD-1.1: Continuous Discovery](../../../../laws/product/_domain.yaml)

**What This Example Shows:**
- How to research cargo customer needs through interviews and data analysis
- How speed-of-booking is the #1 differentiator for freight forwarders
- How to validate that competitors are winning on quote/booking time
- How discovery findings drive roadmap prioritization

---

## Context: Why This Matters for Cargo

American Airlines Cargo operates in a highly competitive market where freight forwarders can easily switch to competitors. Speed of booking isn't a nice-to-have feature—it's a make-or-break differentiator. Alice (freight forwarder) has customers calling with cargo ready to ship. If our quote takes 45 seconds and competitor's takes 15 seconds, Alice will book with competitor. Discovery research quantifies this pain and validates that investing in speed is the right call.

**Key Principles from PRD-1.1:**
- Research customer workflows and pain points
- Validate assumptions with real customer data
- Synthesize findings into actionable insights
- Use research to inform prioritization

---

## Cargo-Specific Discovery: Rate Quote Speed

### Research Approach

We conducted discovery across 3 customer segments over 4 weeks:

**Interviews (Primary):**
- 8 freight forwarders (international and domestic)
- 5 direct shippers (e-commerce and manufacturing)
- 3 partner airlines (regional carriers)

**Data Analysis (Secondary):**
- Competitor benchmark: visit 5 competitors' websites, time quote process
- Usage data: analyze current booking system logs (dropout rates, average time)
- Survey: 50+ forwarders on booking preferences

**Competitive Analysis:**
- Chart quote time for top 5 competitors
- Document features that drive speed (pre-filled info, saved preferences)
- Identify gaps in our offering

---

## Key Discovery Findings

### Finding 1: Quote Speed is #1 Pain Point (94% of forwarders mention)

```
Discovery Method: In-depth interviews with 8 forwarders
Finding: Quote/booking speed mentioned as #1 problem
Example Quote from Alice:
  "If I can't get a quote in 30 seconds while my customer is on the 
   phone, I'll call our second carrier. Speed is everything."

Business Impact:
- Estimated 20% of quote requests result in lost bookings (competitor wins)
- Each lost booking = $500-2000 revenue opportunity
- Forwarders actively switching to faster competitors
```

### Finding 2: Current Process Takes 45-60 Seconds (2-4x slower than competitors)

```
Current AA Cargo Process:
  1. Visit website (5 sec)
  2. Enter shipment details (15 sec)
  3. Wait for pricing (25 sec)
  4. Review options (5 sec)
  5. Navigate to booking (5-10 sec)
  Total: 55-60 seconds

Competitor Benchmarks:
  - Competitor A: 20 seconds (pre-filled form, cached pricing)
  - Competitor B: 35 seconds (API integration with forwarder systems)
  - Competitor C: 25 seconds (simplified form, limited options)

Why We're Slower:
- No pre-filled customer info (each entry manual)
- Pricing engine queries live inventory (slow)
- Complex form with many optional fields
- Each browser refresh requires new session
```

### Finding 3: Forwarders Want API Integration

```
Discovery Method: Questions in 8 interviews + survey of 50 forwarders
Finding: 6/8 interviewed said "we'd switch to you if you had an API"
         40/50 survey respondents said API integration would be deciding factor

Use Case: Carlos (direct shipper) explicitly mentioned:
  "We want to work with AA Cargo, but if I can't integrate it with our 
   system, we won't use it. Manual data entry is too error-prone."

Business Implication:
- API development could unlock new customer segment (direct shippers with ERP systems)
- Would reduce booking time to near-instant (system-to-system)
- Could increase volume by 15-20% per customer (easier to use)
```

---

## Applied Decision: What This Meant for Our Roadmap

Based on PRD-1.1 discovery research, we made these prioritization decisions:

**Immediate (Q1 2026):**
- Reduce quote response time from 45s to 15s (optimize pricing engine)
- Pre-fill customer information for returning users
- Simplify booking form (hide optional fields behind "advanced")

**Near-term (Q2 2026):**
- Implement API for programmatic booking
- Build mobile-optimized quote interface
- Add saved preferences for faster quoting

**Strategic (Q2-Q3 2026):**
- Real-time capacity visibility
- Dynamic pricing with demand signals

---

## When to Apply PRD-1.1 for Cargo

✅ **Use this law when:**
- Starting a new cargo feature (why do forwarders need this?)
- Making a roadmap decision (validate with customer research first)
- Evaluating competitive features (how do competitors solve this?)
- Changing pricing or booking process (will this help or hurt?)

❌ **Don't skip this law even if:**
- You "know" what customers want (validate with research)
- You're under time pressure (bad assumptions cost more later)
- Your engineering team has ideas (test with customers first)

---

## Related Skills

**Skills that complement PRD-1.1:**
- [User Journey Mapping](../../../../agent-skills/skills-by-domain/discovery-research/02-user-journey-mapping.md)

**Related Laws:**
- [PRD-2.1: User Journey Mapping](../../../../laws/product/_domain.yaml) - Map the booking workflow
- [PRD-3.1: Roadmap Planning](../../../../laws/product/_domain.yaml) - Prioritize based on findings

---

## Questions to Ask

When applying PRD-1.1 to cargo product decisions, ask:

1. **Did we validate this with customers?** (Not assumed or guessed)
2. **Which persona benefits most?** (Forwarder? Shipper? PAL?)
3. **What's the business impact?** (Revenue, retention, volume)
4. **Are we solving the real problem or symptom?** (Speed vs. accuracy vs. reliability)

---

**Token Count:** 745 tokens  
**Last Updated:** February 20, 2026  
**Author:** Cargo Product Team  
**Domain:** Cargo & Freight  
**Law:** PRD-1.1: Continuous Discovery
