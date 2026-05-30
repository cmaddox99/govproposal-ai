---
law: BUS-2.1
avatar: avatar-loyalty-aadvantage
title: "Regulatory Mapping — AAdvantage Member Compliance"
---

# BUS-2.1 Regulatory Mapping — Loyalty AAdvantage

## Applicable Regulations

| Regulation | Scope | Key Obligation |
|-----------|-------|--------------|
| CCPA | California member PII and redemption history | Right to know, delete, opt-out of sale |
| GDPR Article 6 | EU member enrollment and program participation | Lawful basis documented (contract performance) |
| IRS de minimis rules | Award redemptions above threshold | 1099-MISC filing for high-value awards |
| FCRA | Credit-related partner offers | Fair credit reporting compliance for Citi/Barclays |

## ✅ COMPLIANT Example

```java
// MemberProgramService.java — EU member registration with documented lawful basis
MemberRecord record = MemberRecord.builder()
    .memberId(memberId)
    .legalBasis(LegalBasis.CONTRACT_PERFORMANCE)  // GDPR Art 6(1)(b)
    .dataProcessingRef("AAdvantage-Program-Terms-v2024")
    .retentionPolicy(RetentionPolicy.LIFETIME_PLUS_7_YEARS)
    .marketingConsent(false)  // separate explicit opt-in required
    .build();
```

## ❌ NON-COMPLIANT

```java
// Missing legal basis for EU member processing
member.save();  // No GDPR lawful basis documented
```

## Audit Requirement (BUS-7.1)
All member enrollment events must include `legal_basis` and `data_processing_ref` fields
for GDPR Article 30 records of processing activities (RoPA).
