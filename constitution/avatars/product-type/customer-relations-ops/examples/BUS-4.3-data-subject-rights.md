---
avatar: avatar-customer-relations-ops
law_id: BUS-4.3
law_title: "Data Subject Rights"
file_type: example
---

# BUS-4.3 Data Subject Rights — Customer Relations Ops

## Law Summary

Complaint records containing passenger PII — including medical/disability information for ADA complaints — are subject to CCPA rights for California residents and GDPR rights for EU passengers. Passengers may access their complaint records, LLM drafts, and compensation decisions.

## Rights SLA Table

| Right | Scope | SLA | Notes |
|-------|-------|-----|-------|
| Access | Complaint text, LLM draft, compensation, resolution | 30 days | Medical/ADA complaints: RESTRICTED handling |
| Erasure | Complaint PII | 45 days | Complex cases — LLM log anonymization required |
| Erasure | Downstream CRM records | 45 days | Must propagate |
| Portability | Complaint history | 30 days | JSON format |
| Correction | Contact details, complaint classification | 15 days | Identity verification required |

---

## ✅ COMPLIANT Example — CCPA Access Request Including LLM Draft

**Passenger request (California resident):** "Please send me everything you have on my complaint from February."

**Compliant response:**
1. Verify California residency and identity
2. Locate complaint record, associated LLM drafts, compliance check results, compensation decision
3. Flag if complaint involves ADA/medical data — apply RESTRICTED handling (redact diagnosis details from response)
4. Deliver complete package within 30 days
5. Log access request fulfillment in audit trail

**Audit record:**
```
access_req_id: ACC-CR-20240315-00128
complaint_id_hash: sha256(complaint_id+DOB)
ccpa_request: true
medical_data_present: false
records_returned: [complaint_text, llm_draft, compliance_check, compensation_decision]
completion_date: 2024-04-14
```

---

## ❌ VIOLATION Example — Refusing LLM Draft Access

**Scenario:** A passenger requests their complaint records. The team provides the complaint text and resolution letter but refuses to include the LLM draft, citing it as "internal system output."

**Why this violates BUS-4.3:** LLM drafts generated about a passenger's complaint are that passenger's data. Under CCPA's right to know, the passenger can request all personal information — including system-generated outputs about them. Treating LLM drafts as "internal only" mischaracterizes their nature.

**Correct approach:** Include LLM draft in access request scope. If the draft contains information about other passengers, redact that before delivery.
