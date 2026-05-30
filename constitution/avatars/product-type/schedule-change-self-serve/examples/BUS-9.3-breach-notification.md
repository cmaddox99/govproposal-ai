---
avatar: avatar-schedule-change-self-serve
law_id: BUS-9.3
law_title: "Breach Notification"
file_type: example
---

# BUS-9.3 Breach Notification — Schedule Change Self-Serve

## Law Summary

Unauthorized exposure of IROP passenger rebooking data or PNR change history triggers breach notification requirements. BFF API credential compromise exposing passenger change history must be treated as a **high-severity incident**.

---

## ✅ COMPLIANT Example — BFF API Credential Compromise

**Scenario:** A BFF API key is found in a public code repository, potentially exposing access to passenger PNR change history and IROP eligibility records.

**Incident Response Phases:**

| Phase | Action | SLA |
|-------|--------|-----|
| Detect | Security scan alert finds API key in public repository | T+0 |
| Contain | Revoke BFF API credential immediately; issue new credential | T+30min |
| Assess | Audit BFF API access logs for unauthorized access patterns | T+4h |
| Scope | Determine which PNRs and passenger records were accessible | T+8h |
| Notify Legal | Legal/Privacy/CISO notified | T+1h |
| Notify DPA | GDPR notification if EU passenger PNR data accessed | T+72h (from confirmed exposure) |
| Notify Passengers | Affected passengers notified per applicable law | Per state law |

---

## ✅ COMPLIANT Example — IROP Data Export Anomaly

**Scenario:** Monitoring detects a large-volume export of IROP passenger records by an internal user outside normal business hours.

**Immediate actions:**
1. Suspend the user account and revoke credentials (T+0)
2. Preserve access logs and export records for forensics (T+1h)
3. Notify Legal and begin formal investigation
4. If external exposure confirmed: trigger breach notification workflow

---

## ❌ VIOLATION Example — Credential Rotation Without Scope Assessment

**Scenario:** A BFF API credential is found exposed. The team rotates the credential immediately but does not assess what data may have been accessed during the exposure window.

**Why this violates BUS-9.3:** Credential rotation is the correct containment step, but it is not sufficient for breach determination. The team must assess whether the credential was used by unauthorized parties and what data was accessible. Without scope assessment, the team cannot determine whether notification obligations have been triggered.

**Correct approach:** After containment, always perform an access log review to determine if the exposed credential was used, what API endpoints were called, and what passenger data was accessible. This assessment drives notification decisions.
