# Check-In & Boarding Personas

> **Law:** PRD-2.3 (JTBD Law) — personas ground job-to-be-done statements in real user archetypes.  
> **Detail files:** `personas-passenger.md` (Alex + Maria) · `personas-ops.md` (Kevin + Patricia)

---

## Persona Registry

| Persona | Role | Primary device | JTBD in one line |
|---------|------|---------------|-----------------|
| **Alex** | Corporate frequent traveller, 15+ flights/year | iPhone | Zero friction: board without talking to an agent |
| **Maria** | Occasional leisure traveller, 2-4 flights/year | Basic smartphone | Get on the right flight without confusion or stress |
| **Kevin** | Gate agent, 12 years, manages 200+ pax/flight | Biometric scanner + gate display | Get the flight out on time with minimal exceptions |
| **Patricia** | Senior airport ops manager, 900+ departures/day | Ops dashboard | Hit 82%+ on-time through system reliability + predictive data |

---

## Persona-Law Mapping

| Persona | PRD-1.1 Discovery | PRD-2.1 Journey | PRD-3.1 Roadmap | PRD-5.1 Metrics |
|---------|:-----------------:|:---------------:|:---------------:|:---------------:|
| Alex | Medium | High | High | High |
| Maria | High | High | High | Medium |
| Kevin | High | High | High | High |
| Patricia | High | High | High | High |

---

## Key Design Constraints

- **Alex** takes a screenshot of his boarding pass — because he doesn't trust the app will load at the gate. The app has a trust problem.
- **Maria** arrives 3 hours early to compensate for confusion. If the process were clearer, she'd arrive 90 minutes early.
- **Kevin** boards 600 passengers in 35 minutes when systems work. When they don't: 60 minutes, angry customers.
- **Patricia** discovers gate problems from radio calls, not dashboards. She is always reactive, never proactive.

