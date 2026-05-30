# Example: Cargo User Journey Mapping (PRD-2.1 User Journey Mapping)

**Law Reference:** [PRD-2.1: User Journey Mapping](../../../../laws/product/_domain.yaml)

**What This Example Shows:**
- How to map the complete cargo booking and delivery journey
- Identifying key touchpoints where errors and delays happen
- Finding opportunities to improve communication and reduce exceptions
- Understanding different journeys for different personas

---

## Context: Why This Matters for Cargo

The cargo booking journey isn't just "click book"—it spans multiple days, multiple people, multiple systems, and multiple exceptions. Understanding this journey helps us identify where customers experience friction, where we lose information, and where we can add value. A forwarder's journey differs from a direct shipper's journey differs from a PAL partner's journey. Mapping each reveals different problems to solve.

**Key Principles from PRD-2.1:**
- Map end-to-end workflows from start to finish
- Identify all touchpoints (web, phone, email, API, in-person)
- Document decision points and exceptions
- Spot opportunities to improve experience

---

## Cargo Journey 1: Alice (Forwarder) - Rate Quote to Delivery

### Journey Map: Start to Finish

```
┌─ STEP 1: Get Rate (Alice's perspective) ─────────────────────┐
│ Touchpoint: Phone call with customer
│ Action: Customer tells Alice: "I have 500kg electronics, need NYC"
│ Friction: Alice manually enters data into AA Cargo website
│ Pain: Takes 45 seconds, errors in entry cause quote to be wrong
│ Opportunity: Pre-filled form, saved customer profiles
│ Law: PRD-2.1 (map booking workflow)
└────────────────────────────────────────────────────────────────┘

┌─ STEP 2: Review Options (Alice's perspective) ────────────────┐
│ Touchpoint: AA Cargo website, pricing display
│ Action: Alice sees multiple rate options, selects best price
│ Friction: Options are overwhelming, unclear what's included
│ Pain: Alice has to call customer back to confirm which option
│ Opportunity: Recommend "best for speed", "best price", "best reliability"
│ Law: PRD-2.1 (identify decision points)
└────────────────────────────────────────────────────────────────┘

┌─ STEP 3: Confirm Booking (Alice & AA Cargo) ────────────────┐
│ Touchpoint: AA Cargo website, booking form
│ Action: Alice enters shipment details, confirms booking
│ Friction: Manual entry duplicates data already entered for quote
│ Pain: Risk of data entry errors between quote and booking
│ Opportunity: Pre-fill booking with quote details, just confirm
│ Law: PRD-2.1 (reduce touchpoints)
└────────────────────────────────────────────────────────────────┘

┌─ STEP 4: Arrange Pickup (Alice, Customer & AA Cargo) ──────┐
│ Touchpoint: Email confirmation, customer coordination
│ Action: Customer arranges pickup, Alice communicates pickup time to AA
│ Friction: Manual coordination via email/phone (error-prone)
│ Pain: Missed pickups due to unclear communication
│ Opportunity: Integrate with pickup scheduling system, auto-confirmations
│ Law: PRD-2.1 (exception paths)
└────────────────────────────────────────────────────────────────┘

┌─ STEP 5: Shipment in Transit (Alice & Customer) ────────────┐
│ Touchpoint: AA Cargo tracking, customer notifications
│ Action: Customer asks Alice: "Where is my shipment?"
│ Friction: Alice has to log in to check status, info isn't real-time
│ Pain: Alice becomes middleman, increased support tickets
│ Opportunity: Real-time status updates, SMS/email to customer directly
│ Law: PRD-2.1 (communication touchpoints)
└────────────────────────────────────────────────────────────────┘

┌─ STEP 6: Delivery & Exception (varies) ─────────────────────┐
│ Touchpoint: Delivery notification or exception handling
│
│ Happy Path: On-time delivery
│ Action: Shipment arrives on time, customer receives notification
│ Outcome: Customer satisfied, likely to book again
│
│ Exception Path: Delay or problem
│ Action: Delay, routing issue, or damage discovered
│ Friction: Alice gets angry call from customer, scrambles to find info
│ Pain: Poor communication creates trust issues
│ Opportunity: Proactive notification, clear explanation, resolution offer
│ Law: PRD-2.1 (exception handling)
└────────────────────────────────────────────────────────────────┘

┌─ STEP 7: Claims (if needed) ───────────────────────────────┐
│ Touchpoint: AA Cargo claims system, email/phone with Alice
│ Action: Customer claims damage/loss, Alice files with AA
│ Friction: Slow claims process (30+ days), poor communication
│ Pain: Alice frustrated, customer unhappy, relationship damaged
│ Opportunity: Online claims tracking, faster resolution SLA
│ Law: PRD-2.1 (critical exception flow)
└────────────────────────────────────────────────────────────────┘
```

---

## Cargo Journey 2: Carlos (Direct Shipper) - System Integration

### Journey Map: ERP Integration

```
┌─ Desired Future State (Carlos's vision) ────────────────────┐
│
│ ERP System: "I have shipment ready"
│       └─→ API Call to AA Cargo
│              └─→ Auto-populated quote in 100ms
│                    └─→ Auto-book shipment (no human touchpoint)
│                         └─→ Auto-schedule pickup
│                              └─→ Auto-send tracking to customer
│
│ No manual entry, no errors, no delays
│ Current state: 5 manual steps, 15 minutes, error-prone
│ Law: PRD-2.1 (map integration touchpoints)
└────────────────────────────────────────────────────────────────┘
```

---

## Cargo Journey 3: Roberto (PAL) - Capacity & Revenue Management

### Journey Map: Daily Operations

```
Day 1 (6 days before flight):
├─ Flight scheduled in system
├─ Roberto logs in to AA Cargo
├─ Updates available capacity (2000kg, 50 CBM)
└─ Sets rate card for this flight

Days 2-6: Throughout day
├─ Bookings arrive via phone, email, API
├─ Each booking consumed from available capacity
├─ Problem: Manual tracking in spreadsheet
├─ Risk: Overselling, double-booking
│  Law: PRD-2.1 (exception path - capacity management)

Day 6 (1 day before flight):
├─ Roberto monitors fill rate
├─ ~80% capacity filled
├─ Decision: Increase rates by 10% to maximize revenue
├─ Problem: Must manually update each system
│  Law: PRD-2.1 (pricing workflow)

Day 7 (Departure):
├─ Shipments consolidated into flight
├─ Any last-minute changes create chaos
│  Law: PRD-2.1 (operations touchpoint)
```

**Opportunity:** Real-time capacity display, automatic rate adjustment, API for capacity updates

---

## Critical Exceptions in Cargo Journey

### Exception: Shipment Delayed in Transit

```
Detection Point: Tracking system shows delay
Current Process:
  1. Delay detected (24h after scheduled)
  2. AA ops calls customer (if they have number)
  3. Customer calls forwarder Alice
  4. Alice calls shipper Carlos
  5. Carlos frustrated, blames Alice
  Problem: 48+ hours delay in notification, poor communication

Improved Process (per PRD-2.1):
  1. Delay detected → Auto SMS to Alice
  2. Auto email to Carlos (if phone available)
  3. Alice can see reason for delay on platform
  4. AA offers options: reroute, delay acceptance, compensation
  5. Decision tracked and confirmed
```

**Opportunity:** Proactive notifications eliminate surprise and blame-shifting

---

## Applied Decision: Journey Mapping Led to

Based on PRD-2.1 journey mapping, we identified these priority improvements:

**High Priority (Why: Frequency × Pain):**
- Real-time tracking (all personas need this)
- Pre-filled booking forms (Alice: quote to book)
- API integration (Carlos: system-to-system)

**Medium Priority:**
- Pickup scheduling integration
- Dynamic rate updates (Roberto)
- Mobile-optimized experience

**Strategic:**
- Proactive delay/exception notifications
- Claims portal with tracking
- ROI impact analysis reporting

---

## When to Apply PRD-2.1 for Cargo

✅ **Use this law when:**
- Designing a new feature (understand full journey first)
- Improving existing flows (where do customers struggle?)
- Planning integration (API design flows from journey)
- Troubleshooting (map the broken journey to find root cause)

❌ **Don't skip even if:**
- "It's just a simple feature" (simple features can break journeys)
- "We're updating one screen" (may break flow downstream)
- "Customers didn't complain" (they might not realize better option exists)

---

## Related Skills

**Skills that complement PRD-2.1:**
- [User Journey Mapping](../../../../agent-skills/skills-by-domain/discovery-research/02-user-journey-mapping.md)
- [Business Domain Modeling](../../../../agent-skills/skills-by-domain/development-practices/04-business-domain-modeling.md)

**Related Laws:**
- [PRD-1.1: Continuous Discovery](../../../../laws/product/_domain.yaml) - Research customer needs
- [PRD-3.1: Roadmap Planning](../../../../laws/product/_domain.yaml) - Prioritize improvements

---

**Token Count:** 798 tokens  
**Last Updated:** February 20, 2026  
**Author:** Cargo Product Team  
**Domain:** Cargo & Freight  
**Law:** PRD-2.1: User Journey Mapping
