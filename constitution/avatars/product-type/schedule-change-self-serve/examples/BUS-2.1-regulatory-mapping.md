---
law: BUS-2.1
avatar: avatar-schedule-change-self-serve
title: "Regulatory Mapping — DOT Schedule Change Compliance"
---

# BUS-2.1 Regulatory Mapping — Schedule Change Self-Serve

## Applicable Regulations

| Regulation | Scope | Key Rule |
|-----------|-------|---------|
| DOT 14 CFR Part 250 | Airline-initiated schedule changes causing denied boarding | IDB compensation tiers by delay length |
| DOT 14 CFR Part 260 | Refund rights when passenger rejects airline change | Prompt refund within 7 days (credit card) |
| ATPCO Fare Rules | Change fee and exchange eligibility | Fare basis determines change fee or no-fee status |

## ✅ COMPLIANT Example — Eligibility with Regulatory Citation

```java
// In ReshopEligibilityBuilder.java — buildReshopEligibilityRequest populates record locator,
// header (clientId, transactionId), and search criteria.
// RuleResult returned by the downstream reshop service must carry a regulatory reference:

RuleResult ruleResult = new RuleResult();
ruleResult.setEligible(false);
ruleResult.setReasonCode("CODESHARE_RESTRICTION");
ruleResult.setRegulatoryRef("DOT 14 CFR Part 250 — IDB applies only to mainline-operated flights");
ruleResult.setFareRuleRef("ATPCO fare basis Y26 — no same-day change permitted");

// ChangeTripController.java maps this via ReshopEligibilityBuilder
// into ChangeTripEligibilityResponse before returning to the iOS client.
```

## ❌ NON-COMPLIANT Example

```java
// RuleResult with no regulatory or fare rule reference
RuleResult ruleResult = new RuleResult();
ruleResult.setEligible(false);
ruleResult.setReasonCode("INELIGIBLE");
// Missing: regulatoryRef and fareRuleRef — violates BUS-2.1 audit requirement
```

## iOS Surface (changetrip-ios)

`SelectFlightViewModel.swift` must propagate the `reasonCode` and `regulatoryRef` fields
from the BFF `ChangeTripEligibilityResponse` to the UI. Passengers should see the
plain-language reason; the regulatory citation is stored for audit log only.

## Audit Requirement

Every eligibility determination — especially for airline-initiated IROPs — must include
a `regulatory_ref` field citing the applicable DOT regulation or fare rule.
This is required for DOT audit response per BUS-7.1.
The `EligibilityEndpointTest.java` in `src/test/java/com/aa/change/bff/api/controller/changetrip/`
must cover IROP ineligible scenarios with assert on `regulatoryRef` presence.
