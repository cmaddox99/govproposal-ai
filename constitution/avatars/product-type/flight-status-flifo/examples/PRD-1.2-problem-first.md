---
avatar: avatar-flight-status-flifo
law_id: PRD-1.2
law_title: "Problem-First Development"
file_type: example
---

# PRD-1.2 Problem-First Development — Flight Status & FLIFO

## Law Summary

Before committing any engineering resources to a solution, validate that the problem is real, quantified, and well-understood. For flight status: the problem must be demonstrated with session analytics, funnel data, or support signal before proposing any UI or architecture change.

---

## ✅ COMPLIANT Example

### Problem Statement

> Session analytics (April 2026, n = 142,000 sessions) show that 41% of users who open the American Airlines app within two hours of a scheduled departure fail to reach a flight status result screen within three taps. Of these sessions, 67% abandon on the search entry screen (`FlightStatusSearchEntryViewController`). Exit surveys (n = 3,200) cite "I didn't know whether to enter a flight number or an airport" as the top confusion driver (52% of abandons). We will validate whether the city-pair search path is the primary abandonment cause before committing to any redesign work.

---

### Step 1 — Evidence (What We Observe)

- **41%** of near-departure sessions fail to reach a status result within 3 taps.
- **67%** of those failures exit on the search entry screen.
- **52%** of exit-survey respondents cite search mode confusion (flight number vs. city-pair) as the cause.
- Support contacts tagged "can't find flight status" increased 18% quarter-over-quarter.
- Session recordings show users switching between flight number and city-pair tabs an average of 1.8 times per failed session.

### Step 2 — Problem Framing

**Who:** Passengers checking in within two hours of departure — highest urgency, lowest tolerance for friction.

**What:** They cannot reliably reach flight status within 3 taps.

**Why it matters:** A passenger who cannot find their flight status may arrive at the wrong gate, miss a gate change, or call the contact center — increasing cost and reducing trust.

**Quantified impact:** At 41% failure rate across ~70,000 near-departure daily sessions, approximately 28,700 passengers per day experience this failure. Even a 10-point improvement = ~2,870 fewer friction failures daily.

### Step 3 — Hypothesis to Validate

> We hypothesize that the city-pair search tab label and placement creates mode-selection confusion that accounts for the majority of search entry abandonment. If we test a revised entry UI that defaults to flight number mode for near-departure sessions, abandonment on `FlightStatusSearchEntryViewController` will decrease by ≥ 15% within 14 days.

**Validation method:** A/B test on `FlightStatusSearchEntryViewController` entry mode default. Primary metric: search completion rate for near-departure sessions. Guardrail: city-pair search usage must not drop by more than 20% (protecting non-flight-number users).

---

## ❌ VIOLATION Example

### Violation Statement

> "Let's redesign the FLIFO search screen with a new AI-powered autocomplete that predicts the user's flight from their booking history."

### Why This Violates PRD-1.2

1. **No problem stated.** There is no evidence that the current search is causing measurable user harm. No funnel data, no session analytics, no user research cited.
2. **Solution-first framing.** The proposal begins with a technology ("AI-powered autocomplete") rather than a validated problem.
3. **Hypothesis not testable as stated.** "Predicts the user's flight" is a desired outcome, not a falsifiable hypothesis tied to a specific failure mode.
4. **Scope not bounded by evidence.** Without knowing why users fail at search, there is no basis for prioritizing autocomplete over dozens of other possible improvements.

### Compliant Reframe

Start here instead: "Session analytics show X% of users fail to find their flight at search entry. We hypothesize the cause is Y. We will validate with Z test before designing any solution."

---

*Grounded in flightinfo-ios analysis — FlightStatusSearchEntryViewController, FlightStatusSearchViewController, FlightStatusFlightNumberSearchEntryView.*
