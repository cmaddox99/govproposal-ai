---
avatar: avatar-product-marketing-personalization
law_id: BUS-4.3
law_title: "Data Subject Rights"
file_type: example
---

# BUS-4.3 Data Subject Rights — Marketing Personalization

## Law Summary

Customers have the right to opt out of targeting, request erasure of their offer history,
and access a record of what offers were shown to them and why. These rights must be
honored with documented processes, SLAs, and audit trails.

---

## ✅ COMPLIANT Example

### Right 1 — Opt-Out (Right to Object to Processing for Marketing)

**Trigger:** Customer unsubscribes, updates preferences, or submits opt-out via aa.com privacy portal.

| Step | SLA | Verification |
|------|-----|--------------|
| Opt-out recorded in `marketing.opt_out_log` | Immediate | Append-only entry with timestamp |
| Customer removed from targeting segments | ≤ 24 hours | `customer_profile.opted_out_at` populated; row-level security excludes from all queries |
| In-flight campaigns halted | ≤ 24 hours | Suppression service picks up on next batch run (every 4 hours) |
| Propagated to Marigold, Cassandra, Ventana | ≤ 24 hours | Preference sync audit log confirmed |
| Excluded from model training data | ≤ 30 days | `opted_out_at IS NOT NULL` filter in training notebook |

**Known gap:** Preference center only supports "unsubscribe all"—no granular category opt-out. Remediation on Q4 2026 roadmap.

---

### Right 2 — Erasure (GDPR Article 17)

**Trigger:** Customer submits erasure request via aa.com portal or Legal/Privacy team receives written request.

| Step | SLA | What Gets Erased |
|------|-----|-----------------|
| Identity verified; scope confirmed | Day 0 | — |
| Offer history anonymized via Delta MERGE | ≤ 72 hours | `customer_id_hash` replaced with `'ERASED'` sentinel value |
| Customer profile PII fields set to NULL | ≤ 72 hours | email_hash, loyalty_id_hash, and all identifying fields |
| `training_excluded = true` flag set | ≤ 72 hours | Excluded from all future model training runs |
| Downstream systems notified | ≤ 72 hours | Marigold, Cassandra, Ventana via privacy sync API |
| Confirmation sent to customer | ≤ 30 days | Includes scope and any retention exceptions |

**Retention exceptions:** Financial records retained per tax law (7 years, de-linked from identity); fraud prevention records retained up to 1 year.

---

### Right 3 — Access Request ("What Offers Was I Shown and Why?")

**Trigger:** Customer submits access request via aa.com privacy portal.

**Process:** Identity verified → offer history report generated from `marketing.offer_decisions_audit` → reviewed for completeness → delivered via secure encrypted link within 30 days.

The `decision_reason` field provides a human-readable explanation for each offer:
> `"Destination affinity: top historical route JFK-LHR; model version top_offer_ranking_v2; score 0.84"`

---

## ❌ VIOLATION Example

### Violation 1 — No Granular Opt-Out

The preference center offers only "receive all marketing" or "unsubscribe from all." Customers cannot opt out of domestic leisure offers while retaining flight status alerts—the all-or-nothing choice causes unnecessary permanent removal from the targetable pool.

**Why this violates BUS-4.3:** GDPR Recital 70 requires opt-out to apply to "specific purposes." Customers must be able to object to marketing profiling without losing all communications.

**Remediation:** Granular category opt-out on Q4 2026 roadmap.

### Violation 2 — PII Retained in Model Training Snapshots After Erasure

Erasure requests anonymize live Unity Catalog rows, but frozen Databricks training snapshots are NOT updated. The customer's loyalty_id_hash, booking history, and offer engagement data remain in those snapshots indefinitely, continuing to influence future model predictions.

**Why this violates BUS-4.3:** GDPR Article 17(1) requires erasure from processing, not just the live system. The `training_excluded` flag must be respected for historical snapshots used in retraining.

**Remediation:** Training pipeline must filter `training_excluded = true` customers from all snapshots at the start of every training run.
