# Risk Register

**Changeset:** `build-adoption-guide-2026-001`
**Authority:** BUS-6.1 ⛔ (Risk Assessment Law), BUS-6.2 (Risk Register Law)
**Status:** DRAFT — awaiting Carlos Mendez + Alexandra Pierce APPROVE
**Version:** 1.0 (2026-05-01)

---

## Risk Scoring

**Likelihood:** HIGH (likely to occur) / MEDIUM (may occur) / LOW (unlikely) / CONFIRMED (already observed)
**Impact:** CRITICAL (project-stopping, legal, or safety impact) / HIGH (significant rework or compliance failure) / MEDIUM (delay or deficiency) / LOW (minor)

---

## Risk Register

| ID | Risk | Likelihood | Impact | Controls | Owner | Status |
|----|------|-----------|--------|---------|-------|--------|
| R-01 | WEAK evidence prevents Stage C advancement; Stage B interviews reveal problem is not as stated → MVP scope invalid | HIGH | HIGH | Stage B gate (G3) hard-blocks Stage C; minimum 3 interviews required; pivot criteria defined in §2 (PRD-5.2) | Priya Kapoor | OPEN |
| R-02 | P4 search JS or P6 wizard JS ships untested code paths | MEDIUM | HIGH | ENG-4.1 ⛔ TDD gate (G4); mutation test ≥ 70% before ship | Tomás Reyes | OPEN |
| R-03 | Analytics feature shipped without PIA | MEDIUM | CRITICAL | G9 hard-blocks analytics; all analytics in LATER horizon; Carlos Mendez sign-off required | Carlos Mendez | OPEN |
| R-04 | Law registry staleness causes incorrect citations in guide | MEDIUM | HIGH | ENG-11.3 generation pipeline; CI freshness check on every PR; max 30-day staleness | Jordan Ellis | OPEN |
| R-05 | Jury deliberation log tampered or lost | LOW | HIGH | BUS-7.2 SHA-256 manifest; branch protection; SQL checkpoint archive | Carlos Mendez | OPEN |
| R-06 | Accessibility defect discovered post-release | LOW | HIGH | G8 pre-release: WCAG 2.1 AA audit + ADA/Part 382 legal determination (not deferred) | Carlos Mendez | OPEN |
| R-07 | Constitution amendment during IMPLEMENT causes guide staleness | MEDIUM | MEDIUM | ENG-11.3 freshness trigger; 30-day window; CI blocks stale PR | Jordan Ellis | OPEN |
| R-08 | **Registry integrity anomaly** — `laws/index.yaml` comments do not match actual law titles in 5 cases (BUS-2.2, BUS-3.1, BUS-6.1, ENG-10.1, ENG-11.1) and BUS-3.6 absent from `law_ids.business` | CONFIRMED | MEDIUM | Escalated to constitution maintainer; this proposal uses only verified law IDs (not comment labels); tracked here pending fix | Carlos Mendez | ESCALATED — awaiting maintainer response |
| R-09 | Branch protection not configured on repository | MEDIUM | HIGH | BUS-7.1 ⛔ requirement: repo admin must confirm branch protection before Phase 3 IMPLEMENT | Carlos Mendez | OPEN — confirmation required |
| R-10 | Interview recordings stored in non-compliant location before Stage B | MEDIUM | MEDIUM | Action required: select compliant secure storage before Stage B interviews begin | Priya Kapoor | OPEN — pre-Stage B action |
| R-11 | SonarQube instance not provisioned before Phase 3 IMPLEMENT | MEDIUM | HIGH | G2 blocks Phase 3 until Jordan Ellis confirms SonarQube provisioned and dashboard reachable | Jordan Ellis | OPEN |
| R-12 | ENG-4.11 mutation test score not achieved for P4 or P6 JS | MEDIUM | MEDIUM | TDD process (ENG-4.1 ⛔) + mutation testing gate before ship | Tomás Reyes | OPEN |

---

## Escalations

| Escalation | Target | Raised By | Date | Status |
|-----------|--------|-----------|------|--------|
| Registry integrity anomaly: `laws/index.yaml` stale comments — (1) BUS-2.2 reads "TSA Security Requirements" (actual: Control Framework Law); (2) BUS-3.1 reads "PNR Data Retention (7 years)" (actual: Data Classification Law); (3) BUS-6.1 reads "Dangerous Goods Compliance" (actual: Risk Assessment Law) — confirmed R2 by Alexandra Pierce, Carlos Mendez. (4) BUS-3.6 present in `non_negotiable.business` and `_domain.yaml` Article III but absent from `law_ids.business` — confirmed R3 Carlos Mendez FINDING-F. (5) ENG-10.1 comment reads "Constitution Governance Law" (actual title confirmed in `laws/engineering/governance.md`: Constitution Metrics Collection Law) — confirmed R4 Alexandra Pierce NEW-01. (6) ENG-11.1 comment reads "Spec-Driven Development Law" (actual title confirmed in `laws/engineering/spec-driven-development.md`: Hangar SDD Law) — confirmed R4 Alexandra Pierce NEW-02. (7) ENG-12.x series absent from `law_ids.engineering` cross-validation list despite ENG-12.1 being in `non_negotiable.engineering` — confirmed R5 Alexandra Pierce observation. All PROPOSAL titles are correct; defects are in `index.yaml` comments only. | Constitution maintainer | Carlos Mendez (R2–R5 progressive findings) | 2026-05-01 | OPEN — awaiting maintainer response |

---

*Authored per BUS-6.1 ⛔ · Requires Carlos Mendez APPROVE + Alexandra Pierce APPROVE before Stage C*
