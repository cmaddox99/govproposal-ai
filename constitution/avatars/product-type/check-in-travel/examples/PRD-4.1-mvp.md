# PRD-4.1: MVP & Product-Market Fit — Check-In

> **Law:** PRD-4.1 MVP & Product-Market Fit Law  
> **Detail file:** `PRD-4.1-mvp-results.md` (MVPs 2-3 + gate ops dashboard validation)

---

## Why MVP Discipline Matters for Check-In

Check-in touches 900K+ daily passengers. A rushed rollout at full scale causes cascading gate delays. Every significant feature starts as a scoped beta — 2-3 hubs, 30 days — before broad launch. The cost of getting it wrong is too high to skip validation.

---

## MVP 1: Mobile Offline Barcode

**Hypothesis:** Offline barcode support reduces 8% mobile failure rate to <1%.

**IN scope:**
- Barcode generated locally, cached on device — works without network
- Pre-gate validation 15 min before boarding with pass/fail alert
- Instant printed backup at any kiosk if validation fails

**OUT scope (next phases):**
- Biometric boarding, Apple/Google Wallet deep integration, multi-pax offline, real-time flight updates offline

**Beta:** 100K passengers · DEN, DFW, MIA · 30 days

| Criterion | Target | Actual | Go? |
|-----------|--------|--------|-----|
| Mobile failure rate | <1% | 0.9% | ✅ |
| Offline adoption | ≥60% | 61% | ✅ |
| Gate scan success | ≥99% | 99.1% | ✅ |
| Passenger confidence | ≥8/10 | 8.3/10 | ✅ |
| Gate agent satisfaction | ≥8/10 | 9.1/10 | ✅ |
| Recovery time on failure | <1 min | 45 sec | ✅ |

**Decision: GO** — All 6 criteria met. Minor refinement: improve international device compatibility before broad launch.

---

## MVP 3: Kiosk UX Simplification

**Hypothesis:** Simplifying kiosk from 8 screens to 3 raises completion from 60% to ≥75%.

**IN scope:** 3-screen flow (Identify → Confirm → Print), scan ID or confirmation code, one-tap bag add-on, large text + high-contrast accessibility design  
**OUT scope:** Seat selection at kiosk, upgrade payment, multilingual voice guidance

**Beta:** 200 kiosks, A/B test (old vs. new UX)

| Metric | Old UX | New UX | Target | Go? |
|--------|--------|--------|--------|-----|
| Completion rate | 60% | 76% | ≥75% | ✅ |
| Time to complete | 5.5 min | 3.2 min | <4 min | ✅ |
| Accessibility rating | 4/10 | 7.5/10 | ≥7/10 | ✅ |
| Counter diversion rate | 40% | 24% | <30% | ✅ |
| Maria satisfaction | 5/10 | 7.8/10 | ≥7/10 | ✅ |

**Decision: GO** — Roll out new UX to all kiosks Q3. Maria: *"I didn't need to ask for help this time."*

---

## When to Apply PRD-4.1 for Check-In

✅ Use when: Changing any passenger-facing flow, adding operational tools for agents, modifying kiosk or mobile experience, deploying new scanning hardware.  
❌ Don't skip even if: "It's just a UI change" (UI at 900K pax/day has outsized impact) · "Gate agents asked for it" (validate it helps, not just requested) · "We need to hit on-time targets" (rushed rollout causes more delays than MVP).

