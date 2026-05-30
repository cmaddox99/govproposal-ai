---
id: loyalty-legacy-rescue-2026-004
title: AA AAdvantage Loyalty Platform — Legacy Rescue
status: PROPOSED
workflow: legacy-rescue-refactor
phase: 2
date: 2026-05-05
project_key: aa-loyalty-legacy
codebase: aa-loyalty-legacy — Java 21 Spring Boot Monolith
laws: [ENG-3.1, ENG-4.10, ENG-4.11, ENG-4.12, ENG-6.1, ENG-6.7, ENG-12.1, ENG-12.3, BUS-2.1, BUS-7.1]
---

## Problem Statement

The `aa-loyalty-legacy` codebase is a Java 21 Spring Boot monolith serving the AAdvantage Loyalty Platform. It was developed without constitutional governance and presents P0 security violations (hardcoded production credentials, wildcard CORS, unauthenticated PII endpoints), a god class with cyclomatic complexity ~35, zero test coverage across all 27 classes, and dual regulatory exposure (PCI-DSS, GDPR/CCPA).

No changes can be made safely until characterization tests lock existing behavior.

## Scope

### Bounded Contexts
| Context | Classes | Priority |
|---------|---------|----------|
| Miles Accrual | MileageService, MileageCalculator, MileageAccount, MileageTransaction | HIGH — PCI + DOT |
| Award Redemption | RedemptionService, RedemptionController, Redemption | HIGH — PCI |
| Member Profile | MemberService, MemberController, Member | HIGH — GDPR/CCPA |
| Partner Integration | PartnerService, PartnerController, Partner | MEDIUM |
| Tier Calculation | TierService, TierCalculator, TierController | MEDIUM |
| Notifications | NotificationService | LOW — no external data |
| Config / Infra | DatabaseConfig, AppConfig, Application | P0 — must remediate first |

### Characterization Scope Registry (Phase 3)
| Class | Status | Rationale |
|-------|--------|-----------|
| MileageService | IN_SCOPE | God class — highest risk |
| MileageCalculator | IN_SCOPE | CC ~35 — highest complexity |
| MileageAccount | IN_SCOPE | Domain object — core business rules |
| MemberService | IN_SCOPE | PII + GDPR scope |
| RedemptionService | IN_SCOPE | PCI scope |
| TierService | IN_SCOPE | Calculation logic |
| TierCalculator | IN_SCOPE | Elite bonus duplication |
| PartnerService | IN_SCOPE | External integration boundary |
| NotificationService | IN_SCOPE | Exception swallowing |
| MemberController | IN_SCOPE | Unauthenticated PII endpoints |
| MileageController | IN_SCOPE | Admin endpoint — no auth |
| DatabaseConfig | EXCLUDED | Config-only; remediated in Phase 4, no behavioral test needed |
| AppConfig | EXCLUDED | Config-only; CORS fix in Phase 4 |
| Application | EXCLUDED | Bootstrap class, no logic |
| All DTOs / Entities | EXCLUDED | Value objects, no logic to characterize |
| All Repositories | EXCLUDED | Spring Data interfaces, no logic |

## Phase Plan

| Phase | Name | Gate |
|-------|------|------|
| 1 | Assess | ✅ COMPLETE — 10 violations, baseline captured |
| 2 | Govern | This document |
| 3 | Characterize | SonarQube HARD_BLOCK: coverage ≥95% on IN_SCOPE classes |
| 4 | Remediate | SonarQube HARD_BLOCK: vulnerabilities=0, security_rating=A |
| 5 | Refactor | SonarQube HARD_BLOCK: new_coverage ≥95%, smells must not increase |
| 6 | Certify | Full gate: all thresholds met, delta report committed |
| 7 | Harden — Mutation | HARD_BLOCK: mutation score ≥90% (ENG-4.12) |

## Regulatory Compliance Confirmation (BUS-2.1)
- **PCI-DSS** — Miles redemption + partner billing. Hardcoded credentials are a PCI scope violation requiring immediate remediation in Phase 4.
- **GDPR/CCPA** — Member profile PII. Unauthenticated endpoints violate data protection obligations.
- **DOT** — Frequent flyer obligations require auditable calculation logic. Silent failures in accrual are non-compliant.

## Risk Classification
- **Constitutional risk:** CRITICAL — P0 violations across security, coverage, and complexity
- **Remediation risk:** MEDIUM — No existing tests means Phase 3 must be completed before any code changes
- **Regulatory risk:** HIGH — PCI + GDPR exposure in current state

## Sign-off Required (ENG-12.1 ⛔)
This proposal must be reviewed and approved by a human lead before Phase 3 begins.
