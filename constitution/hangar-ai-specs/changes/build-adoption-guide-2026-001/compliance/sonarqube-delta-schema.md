# SonarQube Delta Schema

**Changeset:** `build-adoption-guide-2026-001`
**Authority:** ENG-12.1 ⛔ (Agentic Feedback Loop Law), Gates G10 and G11
**Status:** ACTIVE — governs every `hangar-ai-specs/evidence/sonarqube-delta.md` filing
**Version:** 1.0 (2026-05-01)

---

## Purpose

Every session-end `sonarqube-delta.md` filing under Gate G11 MUST conform to this schema. A filing that omits any required field does not satisfy G11 — the gate remains open until all fields are present and a human reviewer has signed off.

This schema was created per Jordan Ellis Round 2 OBJECT-17: the absence of a defined schema made G10/G11 unverifiable and gameable.

---

## Required Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `scan-id` | UUID (string) | ✅ Yes | Unique identifier for this SonarQube scan run. Copy from the SonarQube UI "Analysis ID" field or generate via `uuidgen`. |
| `timestamp` | ISO 8601 datetime | ✅ Yes | Date and time the scan was executed. Format: `YYYY-MM-DDTHH:MM:SSZ` |
| `gate-result` | `PASS` or `FAIL` | ✅ Yes | The SonarQube quality gate verdict. Must match the dashboard display exactly — do not self-certify. |
| `delta-summary` | Structured dict | ✅ Yes | Changes vs. the previous scan. See sub-fields below. |
| `delta-summary.coverage-pct` | Float | ✅ Yes | Current line coverage percentage (e.g., `87.4`) |
| `delta-summary.coverage-delta` | Float (signed) | ✅ Yes | Change in coverage since last scan (e.g., `+2.1` or `-0.5`) |
| `delta-summary.new-issues` | Integer | ✅ Yes | Number of new issues introduced since last scan |
| `delta-summary.resolved-issues` | Integer | ✅ Yes | Number of issues resolved since last scan |
| `delta-summary.code-smells-added` | Integer | ✅ Yes | New code smells added |
| `delta-summary.code-smells-removed` | Integer | ✅ Yes | Code smells resolved |
| `delta-summary.security-hotspots` | Integer | ✅ Yes | Open security hotspots requiring human review |
| `human-reviewer` | String (name) | ✅ Yes | Full name of the person who opened the SonarQube dashboard and reviewed the results. The agent cannot be the human reviewer — this field requires a real human action. |
| `sign-off` | Boolean | ✅ Yes | `true` if the human reviewer confirms results were reviewed and the gate outcome is accepted. Must be `true` for G11 to be satisfied. |
| `sign-off-timestamp` | ISO 8601 datetime | ✅ Yes | Date and time the human reviewer signed off. |
| `session-context` | String | ✅ Yes | Brief description of which phase/task was in progress at time of scan (e.g., `"Phase 4 MVP — P1 Landing Page TDD pass"`) |
| `dashboard-url` | URL string | Recommended | Direct URL to the SonarQube project dashboard for this scan. Enables quick verification. |
| `notes` | String | Optional | Any reviewer observations, anomalies, or follow-up actions identified during dashboard review. |

---

## Example Filing

```yaml
scan-id: "a3f7c92e-1b44-4d8e-bf12-9c3e5f7a2001"
timestamp: "2026-05-01T21:30:00Z"
gate-result: PASS
delta-summary:
  coverage-pct: 89.2
  coverage-delta: +4.1
  new-issues: 0
  resolved-issues: 3
  code-smells-added: 0
  code-smells-removed: 2
  security-hotspots: 0
human-reviewer: "Jordan Ellis"
sign-off: true
sign-off-timestamp: "2026-05-01T21:35:00Z"
session-context: "Phase 4 MVP — P4 Laws Reference search JS TDD complete (T5.3a–T5.3i passed)"
dashboard-url: "https://sonarqube.aa.com/dashboard?id=adoption-guide-2026-001"
notes: "Coverage improvement from P4 TDD pass. Zero new issues. Gate PASS confirmed on dashboard."
```

---

## Validation Checklist (for human reviewer)

Before signing off, the human reviewer MUST:

- [ ] Open the SonarQube dashboard directly (not rely on CI log output alone)
- [ ] Confirm the gate-result matches the dashboard display
- [ ] Review all new issues (if any) — none may be critical or blocker severity
- [ ] Confirm security hotspot count matches dashboard
- [ ] Verify scan-id matches the "Analysis ID" shown in the dashboard
- [ ] Record their name as `human-reviewer` — the agent or CI system cannot sign off on this field

---

*Authored per ENG-12.1 ⛔ · Jordan Ellis Round 2 OBJECT-17 remediation · v1.0 (2026-05-01)*
