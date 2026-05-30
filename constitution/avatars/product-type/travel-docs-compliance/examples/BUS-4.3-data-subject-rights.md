---
avatar: avatar-product-travel-docs-compliance
law_id: BUS-4.3
law_title: "Data Subject Rights"
file_type: example
---

# BUS-4.3 Data Subject Rights — Travel Docs Compliance

## Law Summary

Passengers have data subject rights over their document verification records and travel readiness history. However, **government-mandated records** (APIS/CBP data) may have mandatory retention requirements that limit or delay erasure. This intersection must be documented clearly for each data category.

## Rights SLA Table — With Government Retention Notes

| Right | Data Category | SLA | Government Exception |
|-------|--------------|-----|---------------------|
| Access | Passport verification records | 30 days | None — AA-held records |
| Access | APIS transmission records | 30 days | Government copy may be retained by DHS/CBP |
| Erasure | AA-held passport scan copies | 30 days | Government-transmitted data: CBP/DHS retention requirements apply |
| Erasure | Document readiness history | 30 days | Transaction record retained de-identified |
| Portability | Document check history | 30 days | JSON format |

---

## ✅ COMPLIANT Example — Erasure Request with Government Retention Exception

**Passenger request:** "Please delete all my passport data from your systems."

**Compliant response:**
1. Verify identity
2. Erase AA-held passport scan copies within 30 days
3. Erase document readiness history (passenger-facing records)
4. Notify passenger that APIS transmission records sent to CBP/DHS are subject to government retention requirements and cannot be erased by AA
5. Provide written explanation of which records were erased, which records are retained by government obligation, and the legal basis

**Audit record:**
```
erasure_id: ERA-DOCS-20240315-00192
passenger_id_hash: sha256(PNR+DOB)
aa_passport_scan_erased: true
government_retention_exception: CBP/DHS APIS records — per 19 CFR 122.49a
notification_sent: true
```

---

## ❌ VIOLATION Example — Refusing All Erasure Citing Government Records

**Scenario:** A passenger requests erasure of passport data. The team refuses all erasure, citing government data sharing requirements.

**Why this violates BUS-4.3:** The government retention exception applies only to records that were transmitted to and retained by government agencies. AA-held copies of passport scans, document check event logs, and document readiness history are AA-controlled data and must be erased on request. Blanket refusal citing government requirements is a misapplication of the exception.

**Correct approach:** Distinguish AA-held records (must be erased) from government-mandated retained records (explain the exception). Passengers must receive a clear written explanation of what was erased and why retention applies to the remaining records.
