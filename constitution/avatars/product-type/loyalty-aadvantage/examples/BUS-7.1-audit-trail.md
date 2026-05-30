---
avatar: avatar-loyalty-aadvantage
law_id: BUS-7.1
law_title: "Audit Trail Law (Business)"
file_type: example
---

# BUS-7.1 Audit Trail — AAdvantage Loyalty

## Law Summary

Every points earn/burn event, elite status change, partner transaction, and win-back campaign send must be recorded in an **append-only audit log**, immutable and retained **7 years** per financial record obligations.

## Audit Schema (DDL-style)

```sql
CREATE TABLE loyalty_audit_log (
  audit_id        VARCHAR(36) PRIMARY KEY,      -- UUID
  member_id_hash  VARCHAR(64) NOT NULL,          -- SHA-256 of member_num + DOB
  event_type      VARCHAR(50) NOT NULL,          -- POINTS_EARN | POINTS_BURN | ELITE_STATUS_CHANGE | PARTNER_TRANSACTION | CAMPAIGN_SEND
  points_delta    INTEGER,                       -- positive for earn, negative for burn
  source_partner  VARCHAR(50),                   -- NULL for AA-earned events
  event_detail    JSONB NOT NULL,
  timestamp       TIMESTAMP NOT NULL,
  created_at      TIMESTAMP DEFAULT NOW()
);
-- Append-only. Erasure handled via member_id_hash anonymization only.
```

## BUS-7.1 Field Mapping

| Event Type | Required event_detail fields |
|------------|------------------------------|
| POINTS_EARN | flight_number, fare_class, miles_flown, bonus_reason |
| POINTS_BURN | redemption_type, award_ref, miles_redeemed, cash_copay |
| ELITE_STATUS_CHANGE | old_tier, new_tier, qualifying_miles, qualifying_segments |
| PARTNER_TRANSACTION | partner_id, transaction_ref, earn_rate, partner_category |
| CAMPAIGN_SEND | campaign_id, channel, offer_type, member_tier |

---

## ✅ COMPLIANT Example — Elite Status Qualification Audit

```json
{
  "audit_id": "elite-qual-20240315-00847",
  "member_id_hash": "c4a9b2d1...",
  "event_type": "ELITE_STATUS_CHANGE",
  "points_delta": 0,
  "source_partner": null,
  "event_detail": {
    "old_tier": "GOLD",
    "new_tier": "PLATINUM",
    "qualifying_miles": 75000,
    "qualifying_segments": 60,
    "qualification_date": "2024-03-15",
    "effective_date": "2024-03-16"
  },
  "timestamp": "2024-03-15T23:59:00Z"
}
```

---

## ❌ VIOLATION Example — Missing Partner Transaction Reference

**Scenario:** Hotel partner transactions are logged to the audit table, but the partner_transaction_ref field is left null because the partner API doesn't return a reference number.

**Why this violates BUS-7.1:** Each partner transaction must be traceable back to the partner's source record. Without a transaction reference, disputes cannot be resolved and the audit trail is incomplete. Partner API integration must require a reference number; if the partner cannot provide one, the integration is non-compliant.

**Correct approach:** Require transaction_ref as a mandatory field in the partner earn API contract. If a partner cannot provide it, escalate to the partner relationship team before processing transactions.
