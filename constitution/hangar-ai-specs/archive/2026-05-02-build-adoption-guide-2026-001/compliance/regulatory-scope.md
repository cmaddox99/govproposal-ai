# Regulatory Scope Declaration

**Changeset:** `build-adoption-guide-2026-001`
**Authority:** BUS-2.1 ⛔, BUS-2.2 ⛔, BUS-2.3 ⛔, BUS-2.4
**Status:** DRAFT — awaiting Carlos Mendez + Alexandra Pierce APPROVE
**Version:** 1.0 (2026-05-01)

---

## BUS-2.1 ⛔ FAA Compliance Law

**Scope Decision:** OUT OF SCOPE for the adoption guide artifact itself.

**Rationale:** The adoption guide is a governance documentation artifact. It does not directly control, schedule, or certify any flight-critical or crew-scheduling software system. FAR Part 25, FAR Part 117 (crew duty limits), and DO-178C (avionics software) do not apply to a documentation guide.

**Downstream obligation:** Any engineering team that uses the adoption guide to govern a project that produces avionics-adjacent or crew-scheduling software remains bound by FAR Part 117 and DO-178C through their own SDD proposal. The guide must not falsely imply FAA exemption for such projects.

---

## BUS-2.2 ⛔ Control Framework Law

**Scope Decision:** IN SCOPE.

**Controls documented and mapped:**

| Control | Description | Mapped Requirement |
|---------|-------------|-------------------|
| Jury unanimous approval | No task advances without all-6-juror APPROVE | ENG-11.1 ⛔, BUS-7.1 ⛔ |
| Alexandra Pierce VETO | Blocking veto on any NN violation | ENG-11.1 ⛔ |
| Branch protection policy | Force-push disabled; no deletion; signed commits; 1+ reviewer | BUS-7.1 ⛔ |
| Stage gate sequencing | No stage begins without prior stage exit artifact filed | PRD-2.5 ⛔ |
| Rendering gate | No deliberation before HTML + PDF rendered | ENG-13.1 ⛔, ENG-13.3 |
| SonarQube gate | Human reviews dashboard before any phase advances | ENG-12.1 ⛔ |
| Evidence manifest | SHA-256 hashes of all stage evidence files | BUS-7.2 |

---

## BUS-2.3 ⛔ DOT Consumer Protection Law

**Scope Decision:** ACCESSIBILITY IN SCOPE; other DOT provisions OUT OF SCOPE.

**Accessibility (14 CFR Part 382 — Nondiscrimination for Air Travelers with Disabilities):**
American Airlines is subject to 14 CFR Part 382. Although the adoption guide is an internal artifact (not a public-facing consumer product), the BUS-1.1 ⛔ Priority Hierarchy places Legal above all other concerns. AA Legal guidance is required to confirm whether Part 382 applies to internal digital tooling. WCAG 2.1 AA compliance is required as Gate G8 before final release in any case.

**Action required:** Obtain written ADA / Section 508 / 14 CFR Part 382 determination from AA Legal before final release (Gate G8).

**Out of scope:**
- Fare transparency requirements (guide contains no ticket pricing)
- Denied boarding compensation rules (guide has no passenger booking function)
- Refund obligation rules (guide has no commercial transaction)
- Baggage fee disclosure (not applicable)

---

## BUS-2.4 Evidence Collection Law

**Scope Decision:** IN SCOPE.

Compliance evidence is retained in `hangar-ai-specs/` per ENG-11.1 ⛔. Stage evidence files (stage-a through stage-f), deliberation logs, SonarQube delta files, and jury approvals are all retained and SHA-256 hashed per BUS-7.2. Archive path: `hangar-ai-specs/archive/YYYY-MM-DD-build-adoption-guide-2026-001/`.

---

*Authored per BUS-2.x · Requires Carlos Mendez APPROVE + Alexandra Pierce APPROVE before Stage C*
