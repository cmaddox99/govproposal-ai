# Incident Response Plan

**Changeset:** `build-adoption-guide-2026-001`
**Authority:** BUS-9.1 (Incident Classification), BUS-9.2 (Incident Response), BUS-9.3 ⛔ (Breach Notification), BUS-9.4 (Post-Incident Review)
**Status:** DRAFT — awaiting Carlos Mendez + Alexandra Pierce APPROVE
**Version:** 1.0 (2026-05-01)

---

## Incident Classification (BUS-9.1)

| Severity | Definition | Response SLA | Example for This Project |
|----------|-----------|-------------|--------------------------|
| **P1 — Critical** | Data breach; NN law violation in shipped artifact; audit trail corruption | Immediate — page SonarQube on-call; DPO within 1 hour | Personal data exposed in analytics; fabricated law in published guide |
| **P2 — High** | Standard law violation in shipped artifact; stale guide > 30 days; accessibility blocker post-release | 4 hours | Search JS untested in P4; guide not regenerated after law registry change |
| **P3 — Medium** | Compliance document outdated; evidence file hash mismatch; deliberation log gap | 24 hours | risk-register.md not updated after constitution amendment; SHA-256 mismatch detected |
| **P4 — Low** | Minor citation discrepancy (not fabricated); style/rendering issue not affecting compliance | 72 hours | Tooltip showing truncated law summary |

---

## Incident Response Process (BUS-9.2)

1. **Preparation** — This plan is in effect from the moment any Phase 3 IMPLEMENT work begins. Carlos Mendez is the designated Incident Response Coordinator. DPO contact chain below.
2. **Detection** — Incidents may be detected by: automated CI checks, SonarQube alerts, jury review, or external report.
3. **Containment** — P1/P2: immediately stop deployment; revert to last-known-good commit; notify Alexandra Pierce within 1 hour.
4. **Eradication** — Root cause identified; impacted artifacts remediated; jury re-deliberation if NN violation involved.
5. **Recovery** — Re-deploy only after Alexandra Pierce APPROVE (P1) or Carlos Mendez APPROVE (P2/P3/P4).
6. **Lessons Learned** — All incidents ≥ P2 require a post-incident review per BUS-9.4. Findings fed into `compliance/risk-register.md`.

---

## Breach Notification — DPO Contact Chain (BUS-9.3 ⛔)

**72-hour GDPR reporting window starts from the moment a data breach is confirmed.**

| Role | Responsibility | Contact |
|------|---------------|---------|
| Incident Response Coordinator | First responder; classifies incident; triggers notification chain | Carlos Mendez (jury Compliance Officer) |
| Data Protection Officer (DPO) | Assess breach; determine notification obligation (GDPR Art. 33/34) | AA DPO — **contact must be confirmed with AA Legal before Stage B interviews begin** (not Phase 3 — Stage B constitutes PII processing) |
| Legal counsel | Advise on regulatory obligations | AA Legal — **contact must be confirmed before Stage B interviews begin** |
| Affected individuals (if required) | Notification per GDPR Art. 34 (undue delay, where high risk) | Via AA communication channel TBD |

> **⛔ Action required — BLOCKING before Stage B:** DPO contact and AA Legal contact MUST be confirmed and recorded here before any Stage B interviews begin. Stage B involves structured interviews with real American Airlines employees (technical coaches, senior architects). Interview recordings are planned as Confidential PII per `compliance/data-classification.md`. If a breach of Stage B interview data occurs before the DPO chain is documented, the 72-hour GDPR notification clock cannot be honored. This is a **hard pre-condition for BUS-9.3 ⛔ compliance at Stage B** — not Phase 3.
>
> **Interview recording policy decision (required before Stage B):** The team MUST commit to one of the following before any interview is conducted:
> - Option A: **No recordings** — written de-identified notes only. Eliminates PII risk from recordings; reduces Confidential data surface.
> - Option B: **Recordings permitted** — requires: (1) DPO chain confirmed above, (2) interviewee consent obtained per BUS-4.2, (3) storage in AA SharePoint/OneDrive confirmed compliant, (4) 90-day deletion schedule enforced.
>
> Decision: *(to be documented by Carlos Mendez before G3 / Stage B interview T2.2b)*

---

## Notification Template (GDPR Art. 33)

When a breach must be notified to the supervisory authority, the notification must include:
1. Nature of the breach (categories and approximate number of data subjects / records)
2. Name and contact details of DPO or other point of contact
3. Likely consequences of the breach
4. Measures taken or proposed to address the breach and mitigate its effects

---

*Authored per BUS-9.1, BUS-9.2, BUS-9.3 ⛔, BUS-9.4 · Version 1.1 — DPO timing corrected to Stage B per Round 2 Carlos Mendez OBJECT-C; interview recording policy decision required before Stage B · Requires Carlos Mendez APPROVE + Alexandra Pierce APPROVE before Stage B*
