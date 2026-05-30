---
avatar: avatar-customer-relations-ops
law_id: BUS-9.3
law_title: "Breach Notification"
file_type: example
---

# BUS-9.3 Breach Notification — Customer Relations Ops

## Law Summary

Exposure of complaint records containing **medical/ADA data** is highest sensitivity. PII in LLM payloads (redaction failure) is a breach. CCPA-covered California resident complaint data requires state-specific notification.

---

## ✅ COMPLIANT Example — Redaction Pipeline Failure

**Scenario:** Automated monitoring detects that PII (passenger names and booking references) appeared in LLM API call payloads for a 2-hour window due to a redaction pipeline bug.

**Incident Response Phases:**

| Phase | Action | SLA |
|-------|--------|-----|
| Detect | Automated PII scanner on LLM payload logs alerts | T+0 |
| Contain | Disable LLM pipeline; revert to manual drafting | T+15min |
| Assess | Determine scope: which complaints, which PII fields, LLM provider data retention | T+4h |
| Notify Legal | Legal, Privacy, CISO notified immediately | T+1h |
| LLM Provider | Request deletion of affected payloads from LLM provider | T+8h |
| Notify DPA | GDPR notification if EU passenger PII in payloads | T+72h |
| Notify Passengers | CCPA notification for CA resident complaint PII exposure | Per CCPA timing |

**Medical/ADA-specific escalation:**
If any ADA/medical complaint text was in LLM payloads:
- Escalate to Chief Privacy Officer immediately
- Assess HIPAA-adjacent notification obligations
- Medical data exposure triggers highest-severity incident classification

---

## ✅ COMPLIANT Example — Complaint Database Unauthorized Export

**Scenario:** Audit monitoring detects a bulk export of complaint records outside normal business hours by an external contractor account.

**Immediate actions:**
1. Revoke contractor account immediately (T+0)
2. Preserve export logs for forensics
3. Determine if export included medical/ADA complaints
4. If yes: treat as highest-severity; notify CPO within 1 hour
5. CCPA notification for California residents within required timeframes

---

## ❌ VIOLATION Example — No LLM Provider Notification

**Scenario:** PII reaches an LLM provider due to a redaction bug. The team patches the bug and notifies regulators but does not contact the LLM provider to request deletion of payloads.

**Why this violates BUS-9.3:** The LLM provider is a data processor. Passenger PII in their systems due to a processing error must be reported to them and deletion must be requested. The breach response is incomplete without notifying the data processor.

**Correct approach:** Breach response for LLM-related incidents must include contacting the LLM provider, requesting payload deletion, and confirming deletion within the provider's stated SLA.
