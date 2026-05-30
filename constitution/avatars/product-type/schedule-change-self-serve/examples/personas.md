# Schedule Change Self-Serve Personas

**Status:** Draft — requires validation with 5+ passenger interviews and
1-2 airport agent sessions per PRD-3.1. All behavioral details are
experimental until confirmed.

---

## Persona 1: Leisure Traveler — "Flexible Family Planner"

**Name (archetype):** Sam  
**Segment:** Leisure, 1-4 flights per year  
**Channel preference:** AA.com, mobile app  
**Loyalty tier:** AAdvantage basic or non-member

### Goals
- Change a flight quickly when plans shift (weather, family events)
- Understand whether a change costs money or is free before committing
- Receive clear confirmation that the change worked

### Pain Points
- Does not understand why a change is blocked (ineligible without explanation)
- Confused by fare difference calculation — unclear what they will be charged
- Abandons to phone when self-serve flow stalls, leading to long hold times

### Behaviors
- Arrives at change flow from booking confirmation email link
- Tries self-serve first; escalates to phone if blocked within 2 minutes
- Checks multiple dates before committing to avoid change fees

### Evidence Source
- (Experimental — replace with interview notes)

---

## Persona 2: Business Traveler — "AAdvantage Executive"

**Name (archetype):** Jordan  
**Segment:** Frequent business traveler, 30+ flights per year  
**Channel preference:** AA mobile app  
**Loyalty tier:** AAdvantage Platinum or Executive Platinum

### Goals
- Change flights in under 60 seconds — no wizard friction
- Protect upgrade hold when changing to another flight
- Receive accurate same-day change eligibility immediately

### Pain Points
- Re-entering seat preferences after a change reverses an upgrade
- Loyalty seat protection rules are opaque during the change flow
- BFF latency makes same-day changes stressful at the airport

### Behaviors
- Changes at the gate or in the Admirals Club
- Expects the app to remember loyalty preferences across the change
- Will call AAdvantage desk if self-serve does not respect loyalty rules

### Evidence Source
- (Experimental — replace with AAdvantage UR data)

---

## Persona 3: Group Lead — "Team Travel Coordinator"

**Name (archetype):** Morgan  
**Segment:** Corporate travel coordinator, manages 5-20 PNRs simultaneously  
**Channel preference:** AA.com desktop  
**Loyalty tier:** Varies per traveler managed

### Goals
- Change multiple passengers from the same PNR atomically
- Verify all seats land on the same flight after change
- Get a single confirmation covering all passengers

### Pain Points
- Group change requires changing each PNR individually — highly repetitive
- If one passenger's change fails, the rest proceed — group splits across flights
- No visibility into which eligibility rule blocked a specific passenger in the group

### Behaviors
- Starts change attempts in the evening to avoid daytime call-center waits
- Tracks change history across PNRs using personal spreadsheet (no in-app view)
- Escalates to corporate travel desk when group splits occur

### Evidence Source
- (Experimental — replace with corporate travel partner insights)

---

## Persona 4: Airport Agent — "Schedule Change Exception Handler"

**Name (archetype):** Alex  
**Segment:** AA Customer Service Agent at hub airports  
**Channel preference:** schedule-change-ui agent console  
**Role:** Override authority for ineligible change requests

### Goals
- Resolve ineligible change requests quickly to clear the queue
- Understand the specific rule that blocked a passenger change
- Apply override without introducing booking errors or audit gaps

### Pain Points
- Agent console does not show the specific eligibility rule failure — must investigate manually
- Override process does not log reason — creates compliance gap
- Seat assignment after override sometimes conflicts with existing holds

### Behaviors
- Handles 15-30 change override requests per shift at hub airports
- Uses personal notes to track repeat ineligibility patterns (no system support)
- Escalates complex fare disputes to supervisors — unclear which authority level needed

### Evidence Source
- (Experimental — replace with agent observational session notes)

---

## Persona 5: Compliance Analyst — "Audit and Regulatory Reviewer"

**Name (archetype):** Taylor  
**Segment:** AA Compliance, Policy, and Regulatory Affairs  
**Channel preference:** Internal data/audit tooling  
**Role:** Ensures schedule change log meets DOT and internal audit requirements

### Goals
- Retrieve a complete audit trail for any eligibility decision within 24 hours
- Confirm agent override records include authority level and business reason
- Validate that PII in change requests is handled per retention policy

### Pain Points
- Change history is spread across multiple services — no single audit view
- Agent override records are incomplete or missing reason fields
- Data retention windows for failed change attempts are not consistently enforced

### Behaviors
- Reviews audit logs quarterly for DOT compliance spot checks
- Flags gaps to engineering via internal ticket; resolution turnaround is slow
- Uses separate spreadsheet to track unresolved audit gaps

### Evidence Source
- (Experimental — replace with Legal/Compliance team session)
