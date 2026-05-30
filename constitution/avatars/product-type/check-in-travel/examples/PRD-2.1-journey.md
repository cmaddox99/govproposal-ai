# PRD-2.1: User Journey Mapping — Check-In & Boarding

> **Law:** PRD-2.1 Journey Mapping Law  
> **Detail files:** `PRD-2.1-journey-maria.md` · `PRD-2.1-journey-ops.md`

---

## Journey 1: Alex (Digital Traveller) — Frictionless Mobile

**Pre-departure (24h before):**  
Push reminder → Opens AA app → Face ID auth → Reviews seat map → Check-in confirmed → Boarding pass received → **Screenshots as backup** (trust gap evidence)

**Day-of (airport):**  
Arrives 1h before → TSA PreCheck (10 min) → Gate area → Boarding alert → Approaches gate → Scans phone → Boards

| Step | Pain | Opportunity |
|------|------|------------|
| Seat selection | No legroom/exit data visible | SeatGuru integration |
| Boarding pass | App may fail at gate (8% rate) | Offline barcode + pre-gate validation |
| Boarding announcement | Doesn't know which group he's in | Personalised push "You're in Group 2, boards in ~3 min" |
| Gate scan | 8% of time scanner fails; 5-10 min manual recovery | Pre-validated offline barcode |

**Alex's targets:** Check-in completion 88%→95%, mobile reliability 92%→99.9%, gate boarding <30 sec, satisfaction 7→9/10.

---

## Exception Flow: Mobile Boarding Pass Fails at Gate

```
Passenger scans phone → Scanner error → Agent tries 3× → 
Passenger anxious → Agent calls customer service manually → 
10 min delay → Passenger boards → Delayed departure
```

**Fix:** Pre-gate validation 15 min before boarding. If invalid → redirect to kiosk for instant printed backup. Gate never sees the failure.

---

## Key Insights

1. Alex and Kevin have opposing trust models: Alex trusts the app; Kevin uses the gate scanner as reality check. Design for redundancy — satisfy both.
2. Maria's journey is long not because she's slow but because nobody designed for her success. Better UX halves her process time.
3. Kevin is an operational detective — discovering problems at the gate and fixing them under pressure. Real-time visibility converts him from reactive to proactive.

> **Detail files:**  
> `PRD-2.1-journey-maria.md` — Maria (Airport Traveller) + accessibility flows  
> `PRD-2.1-journey-ops.md` — Kevin (Gate Agent) + Patricia (Ops Manager) + exception flows

