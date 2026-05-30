---
avatar: avatar-product-marketing-personalization
law_id: BUS-2.1
law_title: "Regulatory Mapping"
file_type: example
---

# BUS-2.1 Regulatory Mapping — Marketing Personalization

## Regulatory Landscape

| Regulation | Scope | AA Marketing Obligation |
|------------|-------|------------------------|
| CAN-SPAM Act | Commercial email to US customers | Unsubscribe mechanism, physical address, no deceptive subject lines |
| GDPR Art. 6(1)(a) | EU passengers | Explicit consent required before marketing communications |
| GDPR Art. 21 | EU passengers | Right to object to direct marketing — must suppress immediately |
| CCPA § 1798.120 | California customers | "Do Not Sell or Share" opt-out must suppress from targeted advertising |
| TCPA | SMS marketing (US) | Explicit written consent required before SMS campaign sends |

---

## ✅ COMPLIANT Patterns

### CAN-SPAM Compliance

```
Every EMFT/Marigold email campaign must include:
- Physical mailing address in footer
- One-click unsubscribe link
- Non-deceptive subject line (no "RE:" or "FWD:" prefixes)
- Unsubscribe processed within 10 business days
```

**Enforcement in mobile-offers-bff / aa-ct-mobile-airship:**
- `CPSRulesEngineResponse` (aa-ct-mobile-airship `com.aa.ct.airship.bff.dto.cps`) returns
  `opted_out = true` for any customer who has unsubscribed — `MMXOffersServiceImpl` must
  gate on this before constructing `MMXResponse`.
- `ChubErasureFlow.md` documents how CHUB erasure events suppress customers from
  all targeting via `KafkaConfig` consumer in aa-ct-mobile-airship.

### GDPR Consent Gating

```
EU customers (identified by country_code in PaxInfo): require
Art. 6(1)(a) consent record before any marketing send.
Consent withdrawal via AirshipController preference update
must suppress customer from all EMFT and Cassandra channels.
```

### CCPA Lookalike Suppression

```
California customers who exercise "Do Not Sell or Share":
- Suppress from lookalike audience segments in Unity Catalog
- Remove from Cassandra offer history used for targeting
- OffersConnector must not include opted-out customers
  in propensity score batches sent to TOP scoring API
```

---

## ❌ VIOLATION Pattern

> "We re-subscribed a customer to email campaigns after they clicked an offer link, assuming
> that click constitutes re-consent."

**Why this violates BUS-2.1 (CAN-SPAM):**
- CAN-SPAM: once unsubscribed, cannot re-add without explicit new consent request
- A click on a pre-existing offer link is NOT consent to re-subscribe
- `CPSRulesEngineResponse.opted_out` must remain `true` until customer actively opts back in
- Violation risk: FTC enforcement + $51,744 per email fine

---

## Compliance Checklist

| Gate | System | Enforcement |
|------|--------|-------------|
| CAN-SPAM unsubscribe honored | `MMXOffersServiceImpl` + CPS check | `CPSRulesEngineResponse.opted_out` gate |
| GDPR consent verified | `AirshipController` preference service | CPS subscription record check |
| CCPA opt-out suppressed | Unity Catalog row security | `opted_out_at IS NULL` filter on all segment queries |
| TCPA SMS consent | Campaign Manager pre-launch checklist | Written consent record in CPS |
