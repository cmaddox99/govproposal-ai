# Data Classification Table

**Changeset:** `build-adoption-guide-2026-001`
**Authority:** BUS-3.1 ⛔ (Data Classification Law), ENG-6.4 ⛔ (Data Protection Law)
**Status:** ✅ G6 APPROVED — Carlos Mendez APPROVE + Alexandra Pierce APPROVE (2026-05-06)
**Version:** 1.1 (2026-05-06)

---

## Classification Scheme (BUS-3.1 ⛔)

| Level | Definition |
|-------|-----------|
| **Public** | Safe for external publication; no restrictions |
| **Internal** | For American Airlines internal use; no external sharing without authorization |
| **Confidential** | Restricted to named roles; access controlled; encryption at rest required |
| **Restricted** | Highest protection; access controlled by named individual approval; encryption mandatory |

---

## Data Inventory

| Data Asset | Owner | Location | Classification | Retention | Encryption Required |
|-----------|-------|---------|---------------|-----------|-------------------|
| PROPOSAL.md | Agent / Jury | `hangar-ai-specs/changes/` | **Internal** | Minimum 3 years post-archive per BUS-2.4; deleted no earlier than 3 years after `hangar-ai-specs/archive/` move | No (internal repo) |
| tasks.md | Agent / Jury | `hangar-ai-specs/changes/` | **Internal** | Same as PROPOSAL.md — minimum 3 years post-archive | No |
| PROGRESS.md | Agent | `hangar-ai-specs/changes/` | **Internal** | Same as PROPOSAL.md — minimum 3 years post-archive | No |
| stage-a-evidence.md | Agent / Priya Kapoor | `hangar-ai-specs/changes/` | **Internal** | Same as PROPOSAL.md — minimum 3 years post-archive | No |
| stage-b through stage-f evidence | Agent / Priya Kapoor | `hangar-ai-specs/changes/` | **Internal** (de-identified interview notes) | Same as PROPOSAL.md — minimum 3 years post-archive; interview recordings (if any) are Confidential, 90 days post-study then delete | No; interview recordings are Confidential and require Yes |
| Interview recordings (if conducted) | Priya Kapoor | Secure storage — AA SharePoint/OneDrive (to be confirmed before Stage B interviews begin) | **Confidential** | 90 days post-study; delete after de-identification and transcription | Yes |
| Deliberation log (SQL session DB) | Agent / Carlos Mendez | Session database | **Internal** | Online: SDD lifecycle + 1 year; Archived: 7 years per BUS-7.1 ⛔ minimum, append-only in `hangar-ai-specs/archive/` under branch protection | No (contains only juror persona names) |
| SonarQube delta evidence | Agent / Jordan Ellis | `hangar-ai-specs/evidence/` | **Internal** | 7 years per BUS-7.1 ⛔ evidence policy (governs all compliance evidence) | No |
| compliance/ artifacts (threat model, risk register, RACI) | Carlos Mendez | `hangar-ai-specs/changes/compliance/` | **Confidential** | Minimum 3 years post-archive per BUS-2.4; threat model + risk register: 7 years per BUS-7.3 audit readiness | Recommended for threat model |
| evidence-manifest.sha256 | Carlos Mendez | `hangar-ai-specs/changes/compliance/` | **Internal** | Same as evidence files — minimum 3 years post-archive | No |
| MVP walkthrough observation forms | Priya Kapoor / Maya Chen | Secure form tool — AA SharePoint/OneDrive (to be confirmed before Stage B interviews begin) | **Internal** (de-identified; role only, no name) | 90 days post-MVP validation | No |
| Page-level analytics events (LATER horizon — NOT YET ACTIVE) | Carlos Mendez (pending PIA) | TBD (requires BUS-4.5 PIA) | **Internal / Confidential** (TBD — pending PIA) | TBD — pending PIA | TBD — pending PIA |

---

## Analytics Data (LATER Horizon)

Page-level analytics (page load events, navigation clicks, time-on-page) are classified **Internal** when no authentication context is present and **Confidential** if any user identity or session token is captured.

**HARD GATE:** No analytics feature ships until:
1. BUS-4.5 PIA completed and filed (Gate G9)
2. BUS-4.2 consent mechanism implemented
3. BUS-4.4 privacy notice published
4. BUS-4.3 ⛔ data subject rights mechanism confirmed (access, rectification, erasure, portability)

---

*Authored per BUS-3.1 ⛔ · Version 1.1 — retention periods corrected per Round 2 Carlos Mendez OBJECT-B; interview recording storage confirmed before Stage B · Requires Carlos Mendez APPROVE + Alexandra Pierce APPROVE before Stage C*
