# Threat Model

**Changeset:** `build-adoption-guide-2026-001`
**Authority:** ENG-6.1 ⛔ (Security by Design Law)
**Status:** DRAFT — awaiting Tomás Reyes + Alexandra Pierce APPROVE
**Version:** 1.0 (2026-05-01)

---

## System Description

The Hangar AI Constitution Adoption Guide is a set of 10 self-contained static HTML artifacts served from a governance repository. It has no server-side logic, no user authentication, and no database in MVP. The primary sensitive surfaces are the governance artifacts themselves (PROPOSAL, evidence, compliance docs), the law citation integrity, and the deliberation audit trail.

---

## Trust Boundaries

| Boundary | Inside | Outside |
|----------|--------|---------|
| Repository (`hangar-ai-specs/`) | Jury-approved artifacts, evidence files, compliance docs | Unreviewed branches, forks, external contributors without APPROVE |
| Law registry (`laws/`) | Verified law IDs and titles | External law proposals not yet approved by constitution maintainer |
| Rendered HTML pages (P1–P10) | Pages produced by `aa-artifact-render` from verified source | Browser-print PDFs, manually edited HTML not produced by the render tool |
| Deliberation log | SQL session database | Unlogged verbal deliberations, off-session communications |

---

## Threat Actors

| Actor | Motivation | Access Level |
|-------|-----------|-------------|
| Uninformed contributor | Accidental — updates PROPOSAL.md without jury approval | Write access to repo branch |
| Malicious insider | Intentional — tampers with deliberation evidence or fabricates law citations | Write access to protected branch (blocked by branch protection) |
| Stale content | Passive — guide pages not regenerated after law registry update | N/A — automated pipeline failure |
| Registry drift | Passive — `laws/index.yaml` comment labels diverge from actual law titles (confirmed: BUS-2.2, BUS-6.1 labels) | Repository maintainer |
| Analytics-before-PIA | Accidental — developer ships analytics in LATER horizon without Gate G9 | Developer with deploy access |

---

## Threat-to-Control Mapping

| Threat | Control | Law Authority |
|--------|---------|--------------|
| Unauthorized PROPOSAL.md change | Branch protection: force-push disabled, 1+ reviewer required | BUS-7.1 ⛔ |
| Fabricated law citation in guide page | Alexandra Pierce pre-release citation audit; `laws/index.yaml` diff before render | ENG-13.2, ENG-11.3 |
| Stale guide page (law registry changed) | CI/CD freshness check: max 30-day staleness; GitHub Action blocks PR if source changed | ENG-11.3 |
| Tampered evidence file | BUS-7.2 SHA-256 hash manifest updated at each stage gate; deviation detected on next manifest run | BUS-7.2 |
| Deliberation log lost or corrupted | Log persisted in SQL session database + checkpoint system; archive to git on session close | BUS-7.1 ⛔ |
| Analytics shipped without PIA | G9 hard-blocks analytics feature; LATER horizon only; reviewed by Carlos Mendez | BUS-4.5, BUS-4.3 ⛔ |
| Non-`aa-artifact-render` PDF submitted to gate review | ENG-13.3 gate: gate reviews only accept PDFs with `aa-artifact-render --pdf` provenance | ENG-13.3 |
| Registry integrity anomaly (BUS-2.2 / BUS-6.1 comment mismatch) | Tracked in risk register; escalated to constitution maintainer; not used as citation source | BUS-7.2, BUS-3.4 |

---

## Residual Risk

| Risk | Residual After Controls | Accepted By |
|------|------------------------|-------------|
| Branch protection misconfigured by repo admin | LOW — periodic audit via BUS-7.4 Internal Audit | Carlos Mendez |
| Law registry anomaly not fixed by maintainer | LOW — this proposal does not depend on mismatched comments; only uses verified IDs | Alexandra Pierce |
| Interview recordings stored insecurely | MEDIUM — action required: select compliant storage before Stage B interviews begin | Priya Kapoor |

---

*Authored per ENG-6.1 ⛔ · Requires Tomás Reyes APPROVE + Alexandra Pierce APPROVE before Stage C*
