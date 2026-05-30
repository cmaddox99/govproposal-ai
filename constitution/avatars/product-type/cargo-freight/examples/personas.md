# Personas: American Airlines Cargo

## Persona 1: Alice, International Freight Forwarder

**Role:** Freight Forwarder Operations Manager  
**Organization:** Global Logistics (mid-size international forwarder)  
**Experience Level:** Advanced (15+ years in freight)  
**Company Size:** 50 employees, $10M annual revenue

**Goals:**
- Get cargo rate quotes in < 30 seconds (currently 45-120 seconds average)
- Book multiple shipments efficiently (50+ bookings/week)
- Access reliable inventory/capacity information before quoting
- Minimize booking errors and claims through clear documentation

**Pain Points:**
- Current system requires phone calls for rate quotes (slow, expensive)
- Web booking interface is complex and requires 5+ steps
- Cannot see real-time capacity or get transparent routing options
- Claims process takes 30+ days with poor communication

**Key Behaviors:**
- Uses mobile phone while on customer calls to get quotes
- Books during high-volume periods (Mon/Wed afternoons)
- Switches to competitors when quoting takes >2 minutes
- Frequently has to call back to confirm or modify bookings

**Example Quote:**
> "If I can't get a quote in the time my customer is on the phone, they'll call our competitor. Speed is literally the only thing that matters when someone has cargo ready to ship."

**Relevant Laws:**
- PRD-1.1 (Continuous Discovery): Understanding forwarder workflow and bottlenecks
- PRD-2.1 (User Journey Mapping): Mapping quote→book→pickup workflow
- PRD-3.1 (Roadmap Planning): Prioritizing speed improvements
- PRD-5.1 (Metrics): Measuring quote time and booking success rate

---

## Persona 2: Carlos, Direct Shipper

**Role:** Logistics Coordinator  
**Organization:** Tech Hardware Manufacturer  
**Experience Level:** Intermediate (5 years in shipping)  
**Company Size:** 500 employees, manufacturing facility with regular export

**Goals:**
- Ship regular product shipments reliably and on-schedule
- Control freight costs through competitive rate shopping
- Get predictable delivery times with minimal exceptions
- Resolve claims quickly when issues occur

**Pain Points:**
- Rates vary wildly; hard to forecast monthly shipping costs
- Limited visibility into shipment status after booking
- Exception handling (delays, routing changes) happens without notification
- Lacks integration with manufacturing/ERP systems for automated booking

**Key Behaviors:**
- Books shipments monthly or weekly based on production schedule
- Compares rates across 3-4 carriers before deciding
- Calls customer service when shipment is delayed or problem occurs
- Would prefer API/integration but currently uses web booking

**Example Quote:**
> "We want to work with AA Cargo, but if I can't integrate it with our system and have to manually re-enter data each time, we'll stick with our current carrier. Plus, the lack of visibility means my boss asks me about shipments 3 times a day."

**Relevant Laws:**
- PRD-1.1 (Continuous Discovery): Understanding manufacturer shipping patterns
- PRD-2.1 (User Journey Mapping): Integration touchpoints and exception flows
- PRD-3.1 (Roadmap Planning): API/integration features
- PRD-5.1 (Metrics): On-time delivery rate, exception resolution speed

---

## Persona 3: Roberto, Partner Airline (PAL) Operations Manager

**Role:** Cargo Manager  
**Organization:** Partner Airline (PAL) - operates regional flights  
**Experience Level:** Advanced (20+ years in airline operations)  
**Company Size:** Regional carrier, 300+ employees

**Goals:**
- Maximize revenue from available belly capacity on flights
- Minimize operational complexity in cargo handling
- Maintain service level commitments to freight partners
- Integrate cargo operations with flight schedules seamlessly

**Pain Points:**
- Manual process for updating available capacity (affects pricing)
- No real-time visibility into accepted vs. available weight/volume
- Overselling risk when capacity changes due to flight modifications
- Complex PAL application process and rate card negotiations

**Key Behaviors:**
- Updates available capacity 2-3 times per day as flights sell out
- Monitors bookings to prevent oversells
- Negotiates rate cards quarterly with AA Cargo
- Escalates exceptions to operations team (lost shipments, delays)

**Example Quote:**
> "We need to be able to see exactly what capacity is available on each flight, in real-time, and have our rates automatically reflect demand. Right now our team spends hours managing capacity manually, which is error-prone."

**Relevant Laws:**
- PRD-2.1 (User Journey Mapping): Complex operational workflows
- PRD-3.1 (Roadmap Planning): Automation and real-time features
- PRD-5.1 (Metrics): Capacity utilization, revenue per flight

---

## Persona 4: Diana, Cargo Operations Manager (AA Internal)

**Role:** Cargo Product Manager  
**Organization:** American Airlines Cargo Division  
**Experience Level:** Advanced (12 years in cargo operations)  
**Company Size:** Cargo team of 50+ staff

**Goals:**
- Maximize cargo revenue and fill rates on AA flights
- Reduce operational costs and manual handling
- Improve customer satisfaction and retention
- Provide data-driven insights for capacity and pricing decisions

**Pain Points:**
- Limited visibility into why customers choose competitors
- Manual reporting makes it hard to track KPIs in real-time
- Difficulty A/B testing pricing or feature changes
- Claims and exceptions create operational burden

**Key Behaviors:**
- Reviews daily dashboard of bookings, fill rates, revenue
- Meets weekly with operations to address exceptions
- Analyzes customer trends (which forwarders are booking, which aren't)
- Advocates for system improvements to leadership

**Example Quote:**
> "I know we're losing business to competitors on booking speed, but I don't have hard data on how much or which customers. I need better visibility and the ability to test improvements quickly."

**Relevant Laws:**
- PRD-1.1 (Continuous Discovery): Market research and competitive analysis
- PRD-3.1 (Roadmap Planning): Feature prioritization based on data
- PRD-5.1 (Metrics): Real-time KPI dashboards

---

## Persona Journeys

### Alice (Freight Forwarder): Rate Quote to Booking

```
Step 1: Customer calls with cargo details
  └─ Need: Get rate in < 2 minutes while on phone
  └─ Law: PRD-1.1 (Discovery: forwarders need fast quotes)

Step 2: Search for rates and available capacity
  └─ Need: See real-time pricing and inventory
  └─ Law: PRD-2.1 (Journey: quote search experience)

Step 3: Book the shipment
  └─ Need: Simple 2-3 step booking process
  └─ Law: PRD-3.1 (Roadmap: prioritize booking UX)

Step 4: Confirm with customer
  └─ Need: Get confirmation details immediately
  └─ Law: PRD-5.1 (Metrics: booking completion rate)

Outcome: Booking confirmed, customer satisfied, rate competitive
```

---

### Carlos (Shipper): Shipment Tracking & Issue Resolution

```
Step 1: Submit shipment for pickup
  └─ Need: Integrate with ERP system, minimal manual entry
  └─ Law: PRD-2.1 (Journey: integration touchpoints)

Step 2: Track shipment in transit
  └─ Need: Real-time location and status updates
  └─ Law: PRD-2.1 (Journey: visibility and communication)

Step 3: Receive shipment at destination
  └─ Need: Proactive notification of delivery
  └─ Law: PRD-5.1 (Metrics: on-time delivery tracking)

Step 4: If issue: Resolve exception quickly
  └─ Need: Know immediately, get resolution
  └─ Law: PRD-2.1 (Journey: exception handling flows)

Outcome: Shipment delivered on time or issue resolved within SLA
```

---

### Roberto (PAL): Capacity Management & Revenue

```
Step 1: Flight scheduled (3-7 days before departure)
  └─ Need: Update available capacity on system
  └─ Law: PRD-1.1 (Discovery: PAL operational patterns)

Step 2: Accept bookings throughout day
  └─ Need: Real-time capacity tracking, no oversells
  └─ Law: PRD-2.1 (Journey: capacity workflow)

Step 3: Monitor fill rate
  └─ Need: View utilization and revenue per flight
  └─ Law: PRD-5.1 (Metrics: fill rate, revenue per flight)

Step 4: Adjust rates if needed
  └─ Need: Dynamic pricing as capacity fills
  └─ Law: PRD-3.1 (Roadmap: automated pricing)

Outcome: Maximum revenue, zero oversells, operational efficiency
```

---

## Persona-Law Mapping

| Persona | PRD-1.1 | PRD-2.1 | PRD-3.1 | PRD-4.1 | PRD-5.1 |
|---------|---------|---------|---------|---------|---------|
| Alice (Forwarder) | ✅ Critical | ✅ Critical | ✅ Important | ⚠️ Nice to Have | ✅ Important |
| Carlos (Shipper) | ⚠️ Nice to Have | ✅ Critical | ⚠️ Nice to Have | ✅ Critical | ✅ Critical |
| Roberto (PAL) | ✅ Important | ✅ Critical | ✅ Important | ⚠️ Nice to Have | ✅ Critical |
| Diana (PM) | ✅ Critical | ⚠️ Nice to Have | ✅ Critical | ⚠️ Nice to Have | ✅ Critical |

**Legend:**
- ✅ Critical: Cannot do their job without this law
- ✅ Important: Law significantly improves their effectiveness
- ⚠️ Nice to Have: Law is helpful but not essential

---

**Last Updated:** February 20, 2026  
**Product:** Cargo & Freight  
**Research Date:** Validated with customer interviews Q1 2026
