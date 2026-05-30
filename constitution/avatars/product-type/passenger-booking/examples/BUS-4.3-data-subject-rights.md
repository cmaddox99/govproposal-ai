---
avatar: avatar-passenger-booking
law_id: BUS-4.3
law_title: "Data Subject Rights"
file_type: example
---

# BUS-4.3 Data Subject Rights — Passenger Booking

## Law Summary

Passengers have the right to **access**, **erase**, and **port** their PNR data, booking history, and fare history. EU passengers have additional rights under GDPR Article 17 for cancelled non-travelled bookings.

## Rights SLA Table

| Right | Scope | SLA | Notes |
|-------|-------|-----|-------|
| Access | All PNR data, booking history, fare applied, seat assignment | 30 days | Payment method returned masked |
| Erasure | Cancelled non-travelled booking records | 30 days | GDPR Article 17 for EU passengers |
| Erasure | PNR data after travel | 30 days | Subject to 7-year financial record exception |
| Portability | Full booking history | 30 days | JSON or CSV format |
| Correction | Name, contact details | 15 days | Requires identity verification |

---

## ✅ COMPLIANT Example — EU Passenger Erasure Request

**Passenger request:** "I cancelled my flight 3 months ago and never travelled. Please delete my booking record."

**Compliant response:**
1. Verify identity (name, PNR, date of birth)
2. Confirm booking was cancelled and passenger did not travel
3. Erase PNR personal data from booking system within 30 days
4. Retain de-identified transaction record for financial audit (7-year exception)
5. Confirm to passenger: PII erased; anonymized financial record retained per legal requirement

**Required audit record:**
```
erasure_id: ERA-PNR-20240315-04821
pnr_id_hash: sha256(PNR+DOB)
erasure_type: GDPR_ARTICLE_17_NON_TRAVELLER
completion_date: 2024-04-14
financial_record_retained: true (de-identified)
```

---

## ❌ VIOLATION Example — Refusing Erasure for Financial Records

**Scenario:** A passenger who cancelled and never travelled requests erasure. The team refuses entirely, citing the 7-year financial record retention policy.

**Why this violates BUS-4.3:** The 7-year financial record exception covers the **transaction record** (amount, date, route) — not the passenger's PII. The passenger's name, contact details, and passport data must be erased even if a de-identified transaction record is retained. Blanket refusal violates GDPR Article 17.

**Correct approach:** Erase the PII. Retain only the minimum de-identified financial record required by law. Confirm to the passenger what was erased and what was retained (and why).
