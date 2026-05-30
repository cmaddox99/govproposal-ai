---
avatar: avatar-schedule-change-self-serve
law_id: BUS-4.3
law_title: "Data Subject Rights"
file_type: example
---

# BUS-4.3 Data Subject Rights — Schedule Change Self-Serve

## Law Summary

Passengers have the right to **access**, **erase**, and **port** their change and rebooking history, IROP compensation records, and fee waiver decisions. Agent override records affecting a passenger must also be accessible on request.

## Rights SLA Table

| Right | Scope | SLA | Notes |
|-------|-------|-----|-------|
| Access | Rebooking history, IROP records, fee waiver decisions | 30 days | Includes agent override records |
| Erasure | Historical change records (non-financial) | 30 days | Financial records retained de-identified |
| Erasure | IROP compensation records | 30 days | After applicable retention period |
| Portability | Change and disruption history | 30 days | JSON or CSV |
| Correction | Contact and preference data | 15 days | Identity verification required |

---

## ✅ COMPLIANT Example — IROP Record Access Request

**Passenger request:** "I'd like to see all the records from my flight disruption last March, including any notes about my case."

**Compliant response:**
1. Verify passenger identity
2. Locate all PNR change records, IROP eligibility decisions, fee waiver authorizations, and compensation events for the affected period
3. Include any agent override records associated with the passenger's PNR
4. Provide in structured format within 30 days

**Audit record:**
```
access_req_id: ACC-SCHED-20240315-00391
pnr_id_hash: sha256(PNR+DOB)
records_returned: [pnr_changes, irop_eligibility, fee_waiver, agent_overrides]
completion_date: 2024-04-14
```

---

## ❌ VIOLATION Example — Excluding Agent Override Records

**Scenario:** A passenger requests their full rebooking history. The response includes PNR change records but excludes agent override records because they are classified as "internal operational records."

**Why this violates BUS-4.3:** Agent override records that affect a passenger's rebooking outcome are part of that passenger's data subject rights scope. They must be included in access request responses. Classifying them as "internal only" does not exempt them from GDPR/CCPA access rights.

**Correct approach:** Access request workflows must include all records that relate to the data subject's interaction with the system, including agent override logs, eligibility decisions, and fee waiver authorizations.
