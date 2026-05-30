---
laws: [PRD-2.1]
avatar: [gate-management]
title: Gate Management Platform Personas
---

# Gate Management Platform Personas

**Status:** Draft — requires validation with 3+ gate agent sessions, 1–2 FLC interviews,
and 1 biometrics supervisor session per PRD-3.1. All behavioral details are experimental
until confirmed with field observation or interview evidence.

---

## Persona 1: Gate Agent — "Alex"

**Name (archetype):** Alex
**Role:** Frontline gate operations staff
**Primary systems:** GIDS gate screen, DCS boarding system, Biometrics podium,
Carry-On compliance scanner, Connect Me Teams notifications

### Goals
- Clear the gate on time without an irregular operation becoming a delay
- Know instantly when something upstream changes (gate swap, aircraft swap, late inbound)
- Make compliant boarding decisions — biometrics, carry-on, upgrades — without having to look something up
- Never have to chase information: it should arrive before the decision window closes

### Pain Points
- Display shows stale information — aircraft type says one thing, ops control says another; Alex acts on the wrong data
- Biometric non-match with no reason code — passenger is standing at the podium, other passengers are waiting, Alex has no guidance on next step
- Carry-on policy changes mid-day and the gate scanner hasn't updated — Alex is enforcing a rule that no longer applies
- A gate change fires in ops control but the Teams alert arrives 90 seconds later — Alex has already started the wrong boarding sequence
- Override decisions must be documented but the audit path is unclear; Alex makes a judgment call and moves on, knowing it may come back

### Behaviors
- Monitors GIDS display as primary situational awareness tool; trusts it until it lets them down
- Checks Teams for alert notifications but cannot leave the podium during active boarding
- Makes carry-on decisions under time pressure — the line is backing up
- Defaults to manual scan when biometric podium shows an unfamiliar error state
- Communicates gate changes verbally to passengers when digital displays lag

### Evidence Source
- (Experimental — replace with field observation notes and agent interview records)

---

## Persona 2: Ramp Crew / Ground Operations Staff — "Marcus"

**Name (archetype):** Marcus
**Role:** Ground handler — pushback, fuel, baggage, aircraft servicing
**Primary systems:** Connect Me Teams notifications, ramp movement instructions,
push/close alerts

### Goals
- Receive the push alert and weight-and-balance clearance before the window closes
- Know the actual aircraft stand and equipment type before arriving at the gate
- Not miss an early-close signal because the alert went to a device he wasn't checking

### Pain Points
- Push alerts arrive via polling (checking a shared screen) instead of being pushed — Marcus misses the 15-minute window during a high-volume rotation
- Early close signal sent; Marcus is at a different stand; alert does not reach him because Teams subscription is to the wrong gate
- Load plan version visible on his device is not the same version FLC is working from — equipment weight miscalculation risk

### Behaviors
- Works from mobile Teams on the ramp; cannot use desktop tooling during active turns
- Relies on verbal confirmation from gate agent as backup when digital channels lag
- Routes around tooling gaps with radio when time is critical

### Evidence Source
- (Experimental — replace with ramp crew observation notes)

---

## Persona 3: Flight Load Controller (FLC) — "Jordan"

**Name (archetype):** Jordan
**Role:** Load planning and weight-and-balance control for departures
**Primary systems:** Connect Me FLC workflow, load control system, aircraft weight/balance tools

### Goals
- Work from the most current load plan — version number and timestamp always visible
- Receive workflow tasks (load plan updates, weight-and-balance sign-off) without switching tools
- Close out the load plan on time so the ramp crew can push

### Pain Points
- Receives a weight-and-balance task in Teams but cannot tell if the underlying load plan is the version that was updated 4 minutes ago or the one from 40 minutes ago — no version/timestamp on the task card
- Load data in Connect Me is sourced from a batch feed that runs every 5 minutes — not real-time; Jordan approves a plan that's already stale
- Workflow task completion is not logged with enough fidelity for post-incident reconstruction (actor, version, timestamp all required)

### Behaviors
- Manages 5–8 active flights simultaneously during bank operations
- Relies on task cards in Teams as the primary action queue; does not open the load control system unless escalating
- Timestamps every manual action as personal discipline because the system doesn't always do it

### Evidence Source
- (Experimental — replace with FLC interview notes and load control system log review)

---

## Persona 4: Airport Operations Controller — "Sam"

**Name (archetype):** Sam
**Role:** Centralized operations control — gate assignments, IROP recovery, delay tracking
**Primary systems:** Operations dashboard, AOC event system, multi-GIDS display wall,
tarmac timer

### Goals
- See the live gate/aircraft/status picture across the entire concourse without switching screens
- Fire gate-change and flight-status events that propagate to all downstream systems (DSS, Connect Me, Biometrics) within seconds — not minutes
- Have a defensible audit trail for any tarmac delay event

### Pain Points
- A gate change fired from AOC does not appear on the old gate's GIDS for 45–90 seconds — passengers walk to the new gate before the display has updated
- Tarmac timer is buried in a sub-screen; Sam has to navigate away from the ops overview to check it
- Post-IROP incident reconstruction is slow because event timestamps across DSS, Connect Me, and Biometrics don't share a common reference clock

### Behaviors
- Monitors multi-GIDS wall as the primary tool; keeps AOC terminal open on a second screen
- Fires events manually when the AOC automation doesn't catch the exception case
- Keeps a personal log of IROP actions because the digital audit trail is not fully trusted

### Evidence Source
- (Experimental — replace with ops controller interview notes and AOC event log review)

---

## Persona 5: Station Manager — "Diana"

**Name (archetype):** Diana
**Role:** Ground operations oversight — policy management, staffing, compliance accountability
**Primary systems:** Carry-On bag matrix admin UI, operations summary dashboards,
compliance reporting tools

### Goals
- Update carry-on policy rules without opening a helpdesk ticket or waiting for an engineer
- See that policy changes have propagated to all gates within the required 60-second window
- Produce compliance reports on gate-check rates, override frequency, and agent decision accuracy without manual data extraction

### Pain Points
- Bag matrix rule changes require a helpdesk ticket that takes 24–48 hours — policy changes from DOT or legal cannot be applied quickly
- No visibility into which gates have received the updated rule and which are still running the old version
- Override audit log exists but is not accessible from the admin UI — Diana has to request a database extract

### Behaviors
- Manages policy at the station level; rarely at individual gate level
- Verifies policy propagation by calling a gate agent after a rule change — no automated confirmation
- Uses override frequency as a proxy for agent training gaps; tracks it manually

### Evidence Source
- (Experimental — replace with station manager interview notes and admin UI session recordings)

---

## Persona 6: Biometrics Operations Supervisor — "Chris"

**Name (archetype):** Chris
**Role:** Biometric boarding oversight — match threshold management, enrollment monitoring,
CBP compliance
**Primary systems:** Biometrics dashboard, threshold configuration UI, enrollment status tools

### Goals
- Monitor false non-match rate in real time — know immediately when it spikes above threshold
- Adjust the match threshold within CBP-permitted bounds and have the change logged and CBP notified automatically
- Confirm that the opt-out path is functioning correctly at every active gate

### Pain Points
- Match threshold changes require manual CBP notification via a separate workflow — risk of notification being forgotten under operational pressure
- False non-match spikes are visible in the dashboard retrospectively, not in real time — Chris learns about a problem after 30 passengers have been delayed
- Opt-out path availability is not monitored programmatically — Chris relies on agent self-reporting

### Behaviors
- Monitors the biometrics dashboard continuously during peak boarding windows
- Adjusts thresholds conservatively — prefers a small increase in manual checks over a false positive board
- Documents every threshold change with a reason code, even when the system doesn't require it

### Evidence Source
- (Experimental — replace with biometrics supervisor interview notes and CBP audit review)

---

## Persona 7: IT/Platform Engineer (DSS/Biometrics) — "Taylor"

**Name (archetype):** Taylor
**Role:** Platform engineer responsible for DSS event pipeline and biometrics service reliability
**Primary systems:** dss-displayhub-flightevent, dss-displayhub-gateevent, Azure Service Bus,
Application Insights, Biometrics boarding API

### Goals
- Observe display staleness end-to-end — from AOC event fire to screen render — with a single dashboard
- Diagnose a display lag incident in under 5 minutes using trace data, not log mining
- Deploy DSS changes to a single display type at one gate without touching all surfaces

### Pain Points
- Display staleness is not a single metric — it's the sum of AOC→Service Bus lag, Service Bus→DisplayHub lag, DisplayHub→GIDS render time; none of these are surfaced separately
- A biometrics boarding API incident at DFW requires cross-referencing three separate log systems before the failure surface is clear
- DSS web-GIDS and DSS web-FIDS share a deployment pipeline — a FIDS-only change requires touching the GIDS config and vice versa

### Behaviors
- Instruments everything possible with Azure Application Insights custom metrics
- Deploys behind feature flags to enable gate-level rollout control
- Treats the 5-second display staleness SLA as the primary health indicator for DSS

### Evidence Source
- (Experimental — replace with platform engineer interview notes and incident retrospective review)
