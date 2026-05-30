---
avatar: avatar-product-marketing-personalization
law_id: BUS-9.3
law_title: "Breach Notification"
file_type: example
---

# BUS-9.3 Breach Notification — Marketing Personalization

## Law Summary

Any unauthorized exposure of customer targeting data (offer history, propensity scores,
segmentation data, email addresses) must be detected, contained, assessed, and reported
to Legal, affected customers, and (if GDPR applies) the relevant Data Protection Authority
(DPA) within documented SLAs.

---

## ✅ COMPLIANT Example — Incident Response Runbook

**Scope:** Applies to unauthorized access to `marketing.offer_decisions_audit`, `marketing.customer_profile`, `marketing.campaign_results`, Marigold exports, Databricks model training datasets, or any system containing customer_id_hash, email addresses, or offer history.

### Phase 1 — Detection (Automated SLA: < 15 minutes)

| Detection Signal | Alert Destination |
|-----------------|-------------------|
| Mass export > 10,000 rows from `marketing.*` | InfoSec on-call + Privacy team |
| Service principal used outside business hours | InfoSec on-call |
| Databricks job accessing customer tables outside approved workflow | InfoSec on-call |
| Marigold export API called with > 50k contacts | Campaign Manager + InfoSec |

Manual discovery: analysts must report immediately upon finding customer data in any unapproved location.

### Phase 2 — Containment (Within 1 Hour)

| Action | Responsible |
|--------|-------------|
| Create P1 incident ticket in JIRA | First responder |
| Revoke service principal access to affected schema (Unity Catalog) | InfoSec engineer |
| Suspend all active campaign deliveries (pause Marigold queue) | Campaign Manager on-call |
| Isolate affected Databricks pipelines; terminate running jobs | InfoSec engineer |
| Notify privacy@aa.com and legal-privacy@aa.com | First responder |
| Rotate all secrets for affected service principals (Azure Key Vault) | InfoSec engineer |

All actions must be documented with timestamps and actor names in the P1 ticket.

### Phase 3 — Assessment (Within 4 Hours)

Determine: what data was accessed, which fields, how many customers were affected, whether data was exfiltrated (check network egress/VPC Flow Logs), and whether GDPR applies (EU/UK records involved?).

**Output:** Incident assessment report with exposure scope, exfiltration likelihood, GDPR applicability determination, and affected customer list.

### Phase 4 — Notification SLAs

| Recipient | SLA | Basis |
|-----------|-----|-------|
| Legal/Privacy team | Within 1 hour | Internal policy |
| DPA (if GDPR applies) | Within 72 hours | GDPR Article 33 |
| Affected customers (if high risk) | Within 72 hours | GDPR Article 34 |
| AA executive team | Within 24 hours if > 10,000 affected | Internal policy |

**Pre-approved customer notification template:**
> "We are writing to inform you that on [date] we became aware of an incident that may have exposed your American Airlines marketing preferences and offer history. No financial or payment card data was involved. We have [containment actions taken]. Contact privacy@aa.com for details or to request information about what was involved."

---

## ❌ VIOLATION Example

### Violation 1 — No Documented Breach Response Plan

If an analyst discovers customer offer history in a shared S3 bucket, the response is ad hoc: email manager → manager calls InfoSec → InfoSec may not know the 72-hour GDPR deadline. No defined roles, no SLAs, no containment checklist, no audit trail of response actions.

**Why this violates BUS-9.3:** No first responder defined; 72-hour GDPR notification deadline will likely be missed. GDPR fines reach up to 4% of global annual turnover for failure to notify within 72 hours.

### Violation 2 — No DLP Monitoring on Marketing Schema

No Unity Catalog DLP alerting means a mass SELECT of 500,000 customer records by a compromised service principal goes undetected for days—by which point the 72-hour GDPR notification clock has expired. Unity Catalog audit logs exist but are not monitored for anomalous patterns.

**Remediation:** Pre-approve breach notification template with Legal. Document the customer identification query. Configure DLP alerts on the marketing schema. Run an annual breach tabletop exercise to validate the end-to-end process against the 72-hour SLA.
