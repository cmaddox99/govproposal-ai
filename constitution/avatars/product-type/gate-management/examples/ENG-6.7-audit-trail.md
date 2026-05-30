---
avatar: avatar-product-gate-management
law: ENG-6.7
title: "Audit Trail Law"
---

# ENG-6.7 — Audit Trail Law: Gate Management Application

**What this law requires:** All compliance-relevant events must be immutable, append-only, PII-protected, and retained per applicable regulation.

---

## Retention Policy

| Domain | Retention | Regulatory Basis | Storage |
|---|---|---|---|
| Biometric boarding events | 7 years | CBP/TSA | Azure Blob (WORM immutable) |
| Gate event transitions | 2 years | FAA operational audit | Azure SQL (append-only) |
| Carry-on compliance decisions | 1 year | DOT consumer protection | Azure SQL (append-only) |
| Connect Me workflow completions | 90 days | Internal ops | Azure Table Storage |

---

## Immutability — Biometric Events (Azure Blob WORM)

```
Azure Blob Storage
  Container: biometric-audit-logs
  Immutability policy: time-based (7 years), LOCKED
  Access: Read-only for audit consumers; Write via audit service only
  Integrity: SHA-256 hash of each log batch stored in separate container
```
- No UPDATE or DELETE — append blobs only
- Immutability policy must be **locked** (not just configured) before going live

---

## Append-Only — Gate + Carry-On Events (PostgreSQL)

```sql
CREATE TABLE gate_event_audit_log (
  event_id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
  -- ... event fields ...
);

CREATE OR REPLACE FUNCTION prevent_mutation()
RETURNS TRIGGER AS $$
BEGIN
  RAISE EXCEPTION 'Audit log is append-only. Updates and deletes prohibited.';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_append_only
  BEFORE UPDATE OR DELETE ON gate_event_audit_log
  FOR EACH ROW EXECUTE FUNCTION prevent_mutation();
```

---

## PII Protection

- **Biometric templates**: Never in audit log — vault reference (`biometric_template_ref`) only
- **PNR data**: Tokenized at ingestion — raw PNR not persisted in any log
- **Passenger names**: Not required — PNR token + flight_id sufficient for audit

---

## Acceptance Criteria
- [ ] Blob immutability policy is locked (not just set) — verified in Azure Portal
- [ ] Gate event table rejects UPDATE/DELETE — trigger test passing in CI
- [ ] Carry-on log rejects UPDATE/DELETE — trigger test passing in CI
- [ ] No raw biometric template in any audit table — verified by automated scan
- [ ] Automated purge/archive triggers confirmed for 7yr / 2yr / 1yr boundaries
