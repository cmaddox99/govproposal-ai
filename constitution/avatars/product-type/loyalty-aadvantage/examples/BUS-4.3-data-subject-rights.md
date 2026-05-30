---
avatar: avatar-loyalty-aadvantage
law_id: BUS-4.3
law_title: "Data Subject Rights"
file_type: example
---

# BUS-4.3 Data Subject Rights — AAdvantage Loyalty

## Law Summary

AAdvantage members have the right to **access**, **rectify**, **erase**, and **port** their loyalty data including miles balance, travel history, elite status, and partner transaction records.

## Rights SLA Table

| Right | Scope | SLA | Notes |
|-------|-------|-----|-------|
| Access | Miles history, elite status, partner transactions, offer history | 30 days | Full transaction detail |
| Erasure | Member PII from AA systems | 30 days | Financial records retained de-identified (7-year) |
| Erasure | Partner transaction PII | 30 days | Must propagate to partner systems |
| Portability | Miles history, transaction history | 30 days | Structured format (JSON/CSV) |
| Correction | Name, contact, travel preferences | 15 days | Identity verification required |

---

## ✅ COMPLIANT Example — Member Erasure with Financial Exception

**Member request:** "I want to close my AAdvantage account and delete all my data."

**Compliant response:**
1. Verify member identity (member number, name, date of birth)
2. Erase member PII (name, contact, travel preferences) from all AA systems
3. De-link member PII from transaction records — retain anonymized earn/burn history for financial audit
4. Propagate erasure to partner systems (banks, hotels, car rental) with documented confirmation
5. Confirm to member what was erased, what de-identified record remains, and the legal basis for retention

**Audit record required:**
```
erasure_id: ERA-LOYALTY-20240315-02241
member_id_hash: sha256(member_num+DOB)
pii_erased: true
financial_records_retained: de-identified (7yr)
partner_propagation: [CITI_CONFIRMED, HILTON_CONFIRMED, HERTZ_PENDING]
```

---

## ❌ VIOLATION Example — Partner Data Not Propagated

**Scenario:** A member requests full erasure. AA deletes the member's PII from internal systems but does not propagate the erasure to the airline's hotel and car rental partners.

**Why this violates BUS-4.3:** Erasure must propagate to all data processors. Partner systems that hold member transaction data processed on AA's behalf must receive and honor the erasure request. Incomplete propagation means the member's data still exists in the AA partner ecosystem.

**Correct approach:** The erasure workflow must include a step for each active data sharing partner, with confirmation tracking. The request is not complete until all partners confirm or fail explicitly (which then triggers escalation).
