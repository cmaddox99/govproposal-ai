---
avatar: avatar-product-marketing-personalization
file_type: personas
law_ids: []
---

# Marketing Personalization — Personas

These personas represent the primary stakeholders of the TOP (Targeted Offer Platform)
and AA marketing personalization ecosystem.

---

## Alex Chen — Campaign Manager

**Role:** Owns campaign P&L, manages end-to-end campaign lifecycle for AA marketing.

**Goals:**
- Maximize campaign conversion rate while protecting customer experience
- Reduce customer fatigue without sacrificing reach
- Launch campaigns on schedule with minimal engineering dependency

**Pain Points:**
- Manual targeting rules break silently when upstream data schemas change—discovered during campaign flight, not before
- A/B test setup requires a 3-week engineering ticket; cannot rapidly iterate on hypotheses
- No real-time performance visibility during campaign flight; reports arrive 2 weeks after the campaign ends

**Quote:**
> "I need to know if a campaign is working within 48 hours, not two weeks after it ends."

---

## Dr. Priya Patel — Data Scientist

**Role:** Builds propensity models and feature engineering pipelines that power offer ranking in TOP.

**Goals:**
- Build high-lift models (AUC > 0.80) that measurably improve offer relevance
- Achieve fast retraining cycles (< 4 hours end-to-end) to stay current with customer behavior
- Produce SHAP-based explanations that Campaign Managers can understand and trust

**Pain Points:**
- Feature store is fragmented across three systems; joins are manual and error-prone
- No automated model monitoring in production; discovers data drift only when CTR declines
- Retraining cycle takes 48 hours due to manual approval steps

**Quote:**
> "I build a model, it goes into production, and three months later nobody knows if it still works."

---

## Marcus Williams — CRM Analyst

**Role:** Builds customer segments and targeting rules; manages suppression lists and opt-out enforcement.

**Goals:**
- Build high-precision audiences (> 90%) to reduce wasted offer delivery
- Keep opt-out rates low by ensuring customers receive only relevant communications
- Maintain audit-ready suppression lists for legal and compliance inquiries

**Pain Points:**
- Segment overlap causes the same customer to receive duplicate offers across multiple campaigns simultaneously
- Audience data is 48–72 hours stale by delivery time; recent bookers remain in "lapsed" segments
- No opt-out audit trail; compliance inquiries require manually searching five different systems

**Quote:**
> "We got a compliance inquiry asking which campaigns a customer was in. I had to manually search five different systems."

---

## Sarah Kim — Marketing Strategist

**Role:** Sets offer strategy, channel mix, and loyalty tier targeting priorities.

**Goals:**
- Grow customer LTV through more relevant, better-timed offers
- Prioritize retention of high-value AAdvantage members over broad acquisition
- Differentiate offer content, timing, and channel by loyalty tier

**Pain Points:**
- Attribution is unclear; no holdout group to measure whether offers drive incremental bookings
- No single cross-channel offer history view; email, app, web, and Ventana tracked separately
- Channel conflicts: the same offer delivered simultaneously via email, app push, and web banner

**Quote:**
> "We're spending millions on offers and I can't tell you if they're actually driving incremental revenue."

---

## Jamie Rodriguez — Customer (Traveler)

**Role:** AAdvantage Gold member, leisure traveler, 4–6 flights/year on transatlantic routes (JFK–LHR, JFK–CDG).

**Goals:**
- Receive offers for destinations he actually wants to visit (Europe, not domestic leisure)
- Control communication frequency—does not want daily emails
- Easy offer redemption: discount applies automatically at checkout, no promo code hunt

**Pain Points:**
- Regularly receives Miami, Cancún, and Orlando offers despite exclusively booking to London and Paris
- Cannot selectively opt out of domestic leisure offers without losing all communications including flight status alerts
- Offer discount does not auto-apply at checkout, causing booking abandonment

**Quote:**
> "Just show me offers for the places I want to go. How hard can that be?"
