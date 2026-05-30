# PRD-2.1: User Journey Mapping — Schedule Change Self-Serve

**Law Reference:** [PRD-2.1: User Journey Mapping](../../../../laws/product/journey.md)  
**Avatar:** schedule-change-self-serve  
**Status:** Experimental — journeys require validation with UX research and session recordings

---

## Three Core Change Paths

### Path A: Mobile/Web Self-Serve (Primary)

```
Entry (Confirmation email / App deep link)
  │
  ▼
PNR Lookup + Passenger Auth
  │
  ▼
Eligibility Check (schedule-change-eligibility-service)
  ├── ELIGIBLE ──► Flight Selection UI
  │                    │
  │                    ▼
  │               Fare Difference Calculation
  │                    │
  │                    ▼
  │               Seat Selection
  │                    │
  │                    ▼
  │               Confirmation + Rebooking (drss-schedule-change-reservation-service)
  │                    │
  │                    ▼
  │               Confirmation Email / Push Notification
  │
  └── INELIGIBLE ──► Reason Code Display
                       │
                       ├── Customer understands → Abandons or calls
                       └── Customer confused  → Calls agent (escalation)
```

### Path B: Agent Console (Exception Path)

```
Passenger approaches agent with ineligible change request
  │
  ▼
Agent opens schedule-change-ui console
  │
  ▼
Agent reviews eligibility block + rule match
  │
  ▼
Agent determines override authority level
  │
  ├── Within authority ──► Override + Remarks logged (drss-remarks-service)
  │                              │
  │                              ▼
  │                         Rebooking executed
  │
  └── Above authority ──► Escalate to supervisor
```

### Path C: Proactive Disruption Offer (Future State)

```
AA Ops detects IRROPs or schedule change affecting PNR
  │
  ▼
Eligibility evaluated proactively
  │
  ▼
Push notification / Email: "Your flight changed — here are your options"
  │
  ▼
Passenger selects offered alternative
  │
  ▼
One-tap confirmation
```

---

## Journey Stage Analysis

| Stage | What Passenger Needs | Key Failure Mode | Latency Target |
|-------|---------------------|-----------------|----------------|
| PNR Lookup | Fast, accurate auth | Auth timeout, PNR not found | <1s |
| Eligibility Check | Binary result + clear reason | Opaque error code, latency spike | <2s |
| Flight Selection | Available alternatives near original | No alternatives shown for eligible change | <1s render |
| Fare Difference | Transparent cost breakdown | Complex fare math confuses passenger | <500ms |
| Seat Selection | Respect existing preferences / upgrades | Upgrade hold dropped silently | <1s |
| Confirmation | Atomic success signal | Partially-executed rebooking, no rollback | <3s total |
| Post-change Comms | Email + push within 60s | Delayed or missing confirmation | <60s |

---

## Exception Flow Inventory

| Scenario | Current Handling | Gap |
|----------|-----------------|-----|
| Codeshare segment in itinerary | Ineligibility returned — no reason | No partner-segment reason code |
| Group PNR (multiple passengers) | Each PNR must be changed individually | No atomic group change support |
| Loyalty upgrade hold on original flight | Upgrade dropped silently after change | No upgrade-preservation prompt |
| Fare basis blocks change (advance purchase) | Ineligibility returned — no bypass | No agent escalation path in UI |
| Same-day change within 2 hours | Time-window eligibility check varies by airport | No airport-specific rule surfacing |
