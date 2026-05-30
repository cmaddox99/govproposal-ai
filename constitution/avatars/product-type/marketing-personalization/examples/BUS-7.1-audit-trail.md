---
avatar: avatar-product-marketing-personalization
law_id: BUS-7.1
law_title: "Audit Trail Law (Business)"
file_type: example
---

# BUS-7.1 Audit Trail — Marketing Personalization

## Law Summary

Every offer decision made by TOP must be recorded in an append-only audit log with
sufficient detail to reconstruct who received what offer, why it was selected, what
model made the decision, and what the outcome was. The audit log must be tamper-evident
and retained for 7 years.

---

## ✅ COMPLIANT Example — Offer Decision Audit Schema

### DDL

```sql
CREATE TABLE IF NOT EXISTS marketing.offer_decisions_audit (
  audit_id                   STRING NOT NULL,
  customer_id_hash           STRING NOT NULL,  -- SHA-256(loyalty_id); NEVER raw loyalty number
  offer_id                   STRING NOT NULL,
  model_version              STRING NOT NULL,  -- e.g. "top_offer_ranking_v2"
  mlflow_run_id              STRING,
  eligibility_rules_version  STRING,
  score                      DOUBLE,           -- Propensity score 0.0–1.0; NULL for rule-based
  channel                    STRING NOT NULL,  -- email | app | web | loyalty
  campaign_id                STRING NOT NULL,
  decision_reason            STRING,           -- Human-readable: "Destination affinity JFK-LHR; score 0.84"
  delivered_at               TIMESTAMP,
  impression_at              TIMESTAMP,
  click_at                   TIMESTAMP,
  conversion_at              TIMESTAMP,
  revenue_attributed         DOUBLE,
  opt_out_triggered_at       TIMESTAMP,
  created_at                 TIMESTAMP NOT NULL DEFAULT current_timestamp()
)
USING DELTA
TBLPROPERTIES (
  'delta.appendOnly'                       = 'true',
  'delta.logRetentionDuration'             = 'interval 7 years',
  'delta.deletedFileRetentionDuration'     = 'interval 7 years'
);
```

### BUS-7.1 Field Mapping (Who/What/When/Where/Why/Outcome)

| BUS-7.1 Element | Field(s) | Description |
|-----------------|----------|-------------|
| **Who** | `customer_id_hash` | Hashed identity (never raw PII) |
| **What** | `offer_id`, `campaign_id` | Offer and campaign selected |
| **When** | `delivered_at` … `created_at` | Full timestamp chain from decision to outcome |
| **Where** | `channel` | email, app, web, or loyalty |
| **Why** | `model_version`, `mlflow_run_id`, `score`, `decision_reason` | Complete model/ruleset audit |
| **Outcome** | `conversion_at`, `revenue_attributed`, `opt_out_triggered_at` | Conversion and opt-out tracking |

### Append-Only Enforcement

`delta.appendOnly = 'true'` prevents any UPDATE or DELETE operations. For erasure requests (BUS-4.3), use a MERGE that replaces `customer_id_hash` with sentinel `'ERASED'`—the only permitted modification pattern (works via INSERT under the hood via Delta CDC).

### 7-Year Retention

Delta's transaction log records every mutation as an immutable JSON entry. Combined with the 7-year retention setting, this makes the audit log tamper-evident: any attempt to modify or delete historical records leaves a detectable trace.

---

## ❌ VIOLATION Example

### Violation 1 — Relying on Marigold Logs (No AA-Controlled Audit Table)

Offer records exist only in Marigold. Compliance inquiries require manual platform exports. Marigold retains logs for only 13 months (vendor default), does not capture model version, and is vendor-controlled—AA has no tamper-evidence guarantee.

### Violation 2 — Records Overwritten Instead of Appended

```sql
-- Anti-pattern: overwrites history, violates BUS-7.1
UPDATE marketing.campaign_results
SET converted = true, conversion_at = CURRENT_TIMESTAMP()
WHERE customer_id = 12345 AND offer_id = 'OFF-JFK-LHR-2026';
```

Compliant pattern: INSERT a new row with the updated conversion status. Never UPDATE or DELETE existing rows. The `delta.appendOnly = 'true'` property prevents this at the storage layer.

### Violation 3 — No Model Version Recorded

Legacy `campaign_results` records customer_id, offer_id, and delivered_at—but not `model_version` or `mlflow_run_id`. The "why" element of BUS-7.1 is unsatisfied. If a model produces a discriminatory recommendation, there is no way to identify the responsible version or reproduce the scoring.

**Remediation:** All offer decisions must record `model_version` and `mlflow_run_id` before writing to the audit table.
