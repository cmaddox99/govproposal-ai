# Check-In Personas — Operations Staff Detail
# Companion to personas.md | Laws: PRD-2.3, PRD-5.1

---

## Persona 3: Kevin — Gate Agent

**Role:** Ground operations, gate service representative | **Age:** 45 | **Experience:** 12 years | **Manages:** 200+ passengers/flight, 6-8 flights/day

**Goals:** Get the flight out on time. Minimise boarding exceptions. Handle problems quickly.

**Pain Points:**
- System delays: Check-in backlog means some passengers aren't in system at gate
- Overselling discovered at gate — must manage angry standbys in real time
- Scanner failures: 8% of mobile passes won't scan; must manually look up passenger (~7.5 min each)
- No advance view of accessibility needs — discovers wheelchair or language barrier at the gate
- Communication gaps: Doesn't know which passengers are on flight until gate opens

**Key Behaviour:** Starts 10 minutes before boarding reviewing manifest and known issues. Calls standby passengers 30 minutes before pushback. Makes handwritten notes because the system doesn't capture edge cases.

**Quote:** *"If the system is working, I can board 600 passengers in 35 minutes. If it's broken, we're looking at 60 minutes and angry customers."*

**JTBD:** *"When I'm managing a gate, I want to know about problems before boarding starts so I can solve them calmly instead of firefighting."*

**Current reality:** 40 manual lookups/flight × 7.5 min = 300 min of manual work per gate per day. Kevin is an operational detective who should be an operational conductor.

---

## Persona 4: Patricia — Operations Manager

**Role:** Senior airport ops manager | **Age:** 52 | **Experience:** 20 years | **Scope:** 8 gates, 30 agents, 180K+ passengers/day

**Goals:** On-time departures >82%. Boarding time <38 min. System uptime >99.5%.

**Pain Points:**
- Dashboard updates every 15 minutes — problems are always discovered too late
- No predictive data — cannot pre-emptively volunteer/bump passengers before gate
- Technology debt — check-in system built in 2015
- Staffing gaps during peak hours: 6–8am and 5–7pm create bottlenecks
- Incidents cascade: System failure → check-in backlog → gate backlog → on-time drops

**Key Behaviour:** Reviews dashboard 6am–midnight. Forecasts staffing for peak times. Calls executives if on-time drops >2%. Personally investigates major incidents.

**Quote:** *"Our on-time performance is one of the three things passengers judge us on. If I can reduce boarding time from 40 to 35 minutes, we hit 85% on-time and save $2M annually in delay costs."*

**JTBD:** *"When I'm managing daily operations, I want to see problems coming before they escalate so I can allocate resources proactively rather than reacting to crises."*

**What Patricia needs that she doesn't have:** Real-time gate dashboards. Predictive oversell alerts. Automated incident notifications with root-cause data. Patricia currently manages by radio call — she should manage by data.
