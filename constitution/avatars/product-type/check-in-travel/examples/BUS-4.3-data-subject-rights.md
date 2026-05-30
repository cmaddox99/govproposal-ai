---
avatar: avatar-check-in-travel
law_id: BUS-4.3
law_title: "Data Subject Rights"
file_type: example
---

# BUS-4.3 Data Subject Rights — Check-In & Travel

## Law Summary

Passengers have the right to **access**, **correct**, **erase**, and **port** their check-in data including biometric data, TSA PreCheck enrollment, and boarding pass history. Requests must be fulfilled within documented SLAs.

## Rights SLA Table

| Right | Scope | SLA | Notes |
|-------|-------|-----|-------|
| Access | All check-in data, biometric records, boarding history | 30 days | Includes facial match data retained |
| Erasure | Facial match/biometric data | 30 days | Must propagate to CBP vendor systems |
| Erasure | Boarding pass history | 30 days | Subject to 7-year financial record exception |
| Portability | Boarding pass history, TSA PreCheck records | 30 days | Machine-readable format (JSON/CSV) |
| Correction | Name, contact, TSA PreCheck number | 15 days | Requires identity verification |

---

## ✅ COMPLIANT Example — Biometric Erasure Request

**Passenger request:** "Please delete my facial recognition data from American Airlines systems."

**Compliant response:**
1. Verify passenger identity (name, booking reference, date of birth)
2. Locate facial match data in biometric store — search by passenger_id_hash
3. Delete from AA biometric store within 30 days
4. Propagate erasure request to CBP biometric vendor per data sharing agreement
5. Send written confirmation to passenger with deletion timestamp and partner propagation status

**Audit log entry required:**
```
erasure_id: ERA-20240315-00847
passenger_id_hash: sha256(PNR+DOB)
data_type: facial_match_biometric
deletion_timestamp: 2024-03-15T14:32:00Z
partner_propagation: CBP_VENDOR_CONFIRMED
```

---

## ❌ VIOLATION Example — Incomplete Erasure

**Scenario:** A passenger requests deletion of biometric data. The product team deletes from the AA production database but does not propagate the erasure to the CBP biometric vendor.

**Why this violates BUS-4.3:** The passenger's biometric data still exists in a downstream government partner system. Erasure must be complete — including propagation to all data processors. Partial erasure violates GDPR Article 17.

**Correct approach:** Erasure workflow must include a step for partner/vendor propagation with confirmation, and the audit log must record propagation status before the request is marked complete.
