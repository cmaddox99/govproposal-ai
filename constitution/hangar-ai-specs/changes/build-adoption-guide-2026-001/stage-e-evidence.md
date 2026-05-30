# Stage E — Validation Evidence
**Changeset:** `build-adoption-guide-2026-001`
**Author:** Adeel Ali — AI & Technical Coach, American Airlines Hangar
**Status:** v1.1 — 2026-05-07 — ✅ JURY-CLEARED 6/6 APPROVE (2 rounds). R-14/R-15 filed in risk-register.md v2.1. Stage F (Go/No-Go) may begin after 3 walkthrough sessions (WX-01/02/03) are observed and observation forms filed.
**Gate:** Stage D — ✅ CLEARED (2026-05-06, commit `d5545dd`) | IMPLEMENT — ✅ DONE (commit `9c8b430`) | SD-OBL-4 — ✅ CLEARED (commit `2ae750a`) | Stage E entry — UNBLOCKED

---

## §1 Stage Entry Criteria

| Gate | Requirement | Status |
|------|-------------|--------|
| G5 | Threat model filed and jury-cleared | ✅ CLEARED — `compliance/threat-model.md` v1.1, commit `1624648` |
| G6 | Data classification filed and jury-cleared | ✅ CLEARED — `compliance/data-classification.md` v1.1, commit `1624648` |
| G7 | Risk register filed and jury-cleared | ✅ CLEARED — `compliance/risk-register.md` v2.0, commit `1624648` |
| SD-OBL-1 | Architect path blocked until SC-OBL-2 | ✅ COMPLIANT — P1 Architect card shows "Coming Next" |
| SD-OBL-2 | P3 DC-03 Agent Role Explainer present | ✅ PRESENT — verified in IMPLEMENT jury |
| SD-OBL-3 | ENG-3.1 LOC tip absent from P3 | ✅ ABSENT — verified by IMPLEMENT jury, R-13 active |
| SD-OBL-4 | PROPOSAL.md §2 `< 20 min` → `< 60 min` amendment | ✅ CLEARED — PROPOSAL.md v2.6, commit `2ae750a` |
| IMPLEMENT | P1 + P3 + prompt-templates shipped | ✅ SHIPPED — commit `9c8b430`, 6/6 IMPLEMENT jury APPROVE |

---

## §2 Experiment Design (PRD-5.3 Reference)

Experiment type: **Concierge** — facilitator-observed walkthroughs with real Technical Coaches using the live guide (P1 → P3 → prompt-templates). Three independent sessions, one primary adopter per session, one Constitutional facilitator-observer per session.

**Primary measure:** First-successful-task time (stopwatch: landing page load → adopter declares first governed task complete without facilitator prompt).

**Baseline (control condition):** Stage B interview data — README-only entry point baseline is 2–3 hours (Jay Turpin: 2–3 hrs; Wyatt Sutherland: 1–3 hrs; Kenneth Robinson: 2 hrs). Documented in `stage-b-evidence.md §3`.

**Hypothesis under test:** P1 + P3 will reduce first-successful-task time from the 2–3 hour README baseline to < 60 minutes for ≥ 2 of 3 adopters without facilitator prompting. *(PROPOSAL.md §2 v2.6)*

---

## §3 Participant Selection Criteria

**Inclusion criteria:**
- Role: Technical Coach or Senior Architect at American Airlines
- Has adopted the Hangar AI Constitution at least once (familiarity ≥ 1 week)
- Has NOT previously seen P1 or P3 (fresh-user constraint — controls for familiarity bias)
- Has an active GitHub Copilot license and access to the constitution repository

**Exclusion criteria:**
- Engineers (Engineer path is not in MVP scope — DC-02 applies)
- Anyone who participated in Stage B interviews for this changeset (exposure bias — they shaped DC constraints)
- Adeel Ali (session author — cannot be both observer and adopter in the same session)

**Target participants:** 3 Technical Coaches. Any combination of the following roles is valid if 3 independent sessions can be observed:
- TC sessions led by coaches not listed in Stage B (Turpin, Fraser, Sutherland, Robinson)
- TC sessions with coaches who know the constitution but have not yet seen the guide

**Facilitator-observer per session:** The facilitator-observer must NOT be the adopter in the same session. The "not seen the guide" constraint applies to the **adopter** (fresh-user constraint), not to the facilitator-observer. The facilitator-observer may be any of the following, in priority order:

1. A member of the constitutional jury panel who is briefed on the observation protocol
2. A Technical Coach at AA who has reviewed the observation protocol (§4) before the session
3. Adeel Ali (session author) — permitted as facilitator-observer only; may NOT be the adopter

**Practical note:** The Stage B participants (Turpin, Fraser, Sutherland, Robinson) are excluded as **adopters** (exposure bias), but may serve as **facilitator-observers** if they confirm they have not coached any of the three walkthrough adopters in reviewing the guide. This distinction is constitutional — the exclusion targets the role being measured, not the observer role.

---

## §4 Walkthrough Protocol

### Pre-session (facilitator-observer)
1. Open the observation form (§5 below) and start a timer.
2. Confirm adopter meets inclusion criteria (role, familiarity, first-time exposure).
3. Share the landing page URL: `p1-landing.html` — no other instructions.
4. Do NOT introduce sections, explain personas, or prompt next steps until the task-time stopwatch has stopped.

### Session script
| Step | Adopter action | Observer action |
|------|---------------|-----------------|
| 0 | Receives landing page URL only | Start stopwatch |
| 1 | Navigates landing page, selects Coach persona | Record time at persona selection |
| 2 | Enters P3, reads 15-min sprint or Full Adoption Path | Note which path chosen; note any hesitation |
| 3 | Opens prompt in Teams (or Copilot CLI) and runs the adoption prompt | Note if adopter modifies prompt before running |
| 4 | Receives proposal from agent | Note adopter's immediate reaction |
| 5 | Approves or objects to proposal | Record whether adopter invokes batch-size reduction (DC-07 test) |
| 6 | Watches IMPLEMENT phase complete | Note any confusion about what the agent is doing |
| 7 | Declares task complete | **STOP stopwatch. Record elapsed time.** |
| 8 | Post-walkthrough verbal guardrail check (§5.3) | Record guardrail result |
| 9 | Retention prompt (§5.4) | Note verbal response |

**Facilitator-observer prompt (step 3 unlock):** If the adopter is completely blocked and cannot proceed after 5 minutes of genuine attempts, the observer may say: *"What does the page suggest as a next step?"* — this is the one permitted facilitation prompt. If used, record it. A session where the unlock prompt was needed is still valid if the adopter subsequently completes the task without further prompting within the 60-min window.

### Post-session
- Fill in observation form completely before end of day.
- De-identify: replace adopter name with `WX-01`, `WX-02`, `WX-03` in all filed forms.
- File observation form in `compliance/walkthrough-observations/`.

---

## §5 Observation Form

### §5.1 Timing

| Checkpoint | Time (mm:ss) | Notes |
|-----------|-------------|-------|
| Session start (landing page load) | | |
| Persona selected | | |
| Prompt sent to agent | | |
| Proposal received | | |
| Proposal approved / objected | | |
| IMPLEMENT complete | | |
| Task declared complete | | |
| **Total elapsed time** | | Pass if ≤ 60:00 |

### §5.2 Path taken

- [ ] 15-Minute Sprint path (DC-04 amber band)
- [ ] Full Adoption Path (step-by-step cards)
- [ ] Both (switched partway)

### §5.3 Guardrail check — post-walkthrough verbal

The observer reads each statement aloud and asks the adopter: *"Is this statement true or false?"*

| Statement | Expected | Adopter answer | Pass? |
|-----------|----------|---------------|-------|
| "The agent's proposal is just a suggestion — I am not required to accept all of it." | TRUE | | |
| "I can scope the adoption to one module and stop — that's a valid constitutional outcome." | TRUE | | |
| "The SonarQube gate requires me to fix all existing violations before adoption can succeed." | **FALSE** | | |
| "Once I approve a proposal, I cannot object to parts of it." | **FALSE** | | |

**Guardrail PASS:** Adopter answers all 4 correctly without coaching.
**Guardrail FAIL:** Any incorrect answer, OR adopter required coaching to reach the correct answer.

### §5.4 Retention prompt — post-walkthrough verbal

Observer: *"If you needed to do another adoption next week, would you return to this guide first, or go straight to the constitution README? Why?"*

Record response verbatim (de-identify before filing):

```
Response: ____________________________________________________________________
______________________________________________________________________________
```

Retention PASS: Adopter indicates they would return to guide before or instead of the README.

### §5.5 Session metadata (de-identified)

| Field | Value |
|-------|-------|
| Session ID | WX-0_ |
| Date | |
| Adopter role | Technical Coach / Senior Architect |
| Constitution familiarity | ≥ 1 week / ≥ 1 month / > 3 months |
| First-time guide exposure | YES / NO |
| Unlock prompt used (§4) | YES / NO — if YES, note when |
| Observer name | |

---

## §6 Data Collection and Analysis Plan

### §6.1 Primary metric — task time

| Session | Elapsed time | < 60 min? |
|---------|-------------|-----------|
| WX-01 | | |
| WX-02 | | |
| WX-03 | | |

Ship-if: ≥ 2 of 3 sessions complete in < 60 min.

### §6.2 Secondary metric — retention signal

| Session | Would return to guide? | Reason |
|---------|----------------------|--------|
| WX-01 | | |
| WX-02 | | |
| WX-03 | | |

**Data retention:** Walkthrough observation forms are classified Internal per BUS-3.1 ⛔. De-identified forms retained 90 days post-MVP validation, then deleted per PROPOSAL.md §11 data inventory.

### §6.3 Guardrail metric

| Session | All 4 guardrail checks PASS? | Any NN law misconception? |
|---------|------------------------------|--------------------------|
| WX-01 | | |
| WX-02 | | |
| WX-03 | | |

### §6.4 Qualitative observations

For each session, the observer records:
1. **Moments of confusion** — anything the adopter paused on or re-read
2. **Moments of delight** — anything that produced a positive reaction
3. **DC-07 test** — did the adopter invoke batch-size reduction at any APPROVE gate? (expected: yes, if proposal was large)
4. **Path divergence** — did the adopter skip a section? Which one?

### §6.5 Go/No-Go decision criteria (Stage F input)

| Outcome | Decision | Reference |
|---------|----------|-----------|
| ≥ 2 of 3 task time PASS AND ≥ 2 of 3 guardrail PASS | **SHIP** — proceed to Stage F with positive signal | PROPOSAL.md v2.6 §2 ship-if |
| 1 of 3 task time pass OR all task time pass but 1 guardrail fail | **ITERATE** — revise P3 and run 1 additional walkthrough before Stage F | PROPOSAL.md v2.6 §2 iterate-if |
| 0 of 3 task time pass OR ≥ 2 of 3 guardrail fail | **KILL** — re-enter Stage D, re-validate IA design | PROPOSAL.md v2.6 §2 kill-if |

---

## §7 G8 Accessibility Determination (BUS-1.1 ⛔ / BUS-2.3 ⛔)

**Scope:** P1, P2, P3, prompt-templates — all internal-facing HTML artifacts.

**Legal basis:** BUS-2.3 ⛔ (14 CFR Part 382) applies to AA customer-facing products. The adoption guide is an **internal-only** artifact used by AA Technical Coaches and Senior Architects. It is not published to the public and is not accessible to customers.

**Determination:** 14 CFR Part 382 (nondiscrimination for air travelers) does not apply to internal employee-facing tools. Section 508 of the Rehabilitation Act (29 U.S.C. §794d) applies to Federal agencies — American Airlines is a private employer, not a Federal agency; Section 508 does not apply directly. ADA Title I (employment) applies — accessible workplace tooling is required for employees with disabilities.

**WCAG 2.1 AA self-assessment (pre-walkthrough):**

| Criterion | Check | Status |
|-----------|-------|--------|
| 1.1.1 Non-text content | All functional elements are text-based; no images used; no icon-only interactive elements | ✅ PASS |
| 1.3.1 Info and relationships | Semantic HTML: `<h1>`–`<h3>`, `<details>`/`<summary>`, `<button>` | ✅ PASS |
| 1.4.3 Contrast (minimum) | AA Navy `#003366` on white background, AA Red `#cc0000` on white — both exceed 4.5:1 ratio | ✅ PASS |
| 1.4.4 Resize text | No `px` font locks on body text; `font-size` uses `px` in CSS but no viewport-only units; browser zoom works | ✅ PASS |
| 2.1.1 Keyboard accessible | Step accordion uses JS `toggleStep()` — keyboard trigger not present on card headers | ⚠️ PARTIAL — requires fix before final release |
| 2.1.2 No keyboard trap | `<details>` uses native browser keyboard support | ✅ PASS |
| 2.4.3 Focus order | Linear HTML order maintained | ✅ PASS |
| 2.4.6 Headings and labels | Section headings are descriptive | ✅ PASS |
| 3.1.1 Language of page | `lang="en"` on all pages | ✅ PASS |
| 4.1.2 Name, role, value | Copy buttons have visible label text; step cards lack `aria-expanded` | ⚠️ PARTIAL — requires fix before final release |

**G8 finding:** Two accessibility items require remediation before final public release:
1. **P3 step cards** — `toggleStep()` JS trigger must be keyboard-accessible (add `onkeydown` handler or use `<button>` element). Missing `aria-expanded` attribute.
2. **P3 copy buttons** — `aria-label` should include the content being copied, not just "Copy".

**G8 disposition:** These findings do NOT block the controlled walkthrough sessions (WX-01–WX-03) — participants are AA employees without a declared disability accommodation requirement for this research session, and the facilitator-observer is present to assist. G8 items are filed as **R-14** and **R-15** in the risk register and MUST be resolved before final public release (before Stage F go/no-go on unrestricted publishing).

---

## §8 Risk Register Updates (✅ filed in compliance/risk-register.md v2.1)

**R-14 — P3 keyboard accessibility gap (G8)** ✅ FILED
- Risk: Step card accordion (`toggleStep()`) is not keyboard-accessible; `aria-expanded` missing
- Impact: ADA Title I compliance gap for employees using keyboard navigation
- Mitigation: Convert step card headers to `<button>` elements with `onkeydown` and `aria-expanded`
- Blocking: Final public release (Stage F shipping condition)
- Owner: IMPLEMENT team

**R-15 — P3 copy button aria-label (G8)** ✅ FILED
- Risk: Copy buttons do not specify what is being copied in their accessible name
- Impact: Screen reader users cannot distinguish which prompt is being copied
- Mitigation: Add `aria-label="Copy [phase name] prompt"` to each copy button
- Blocking: Final public release (Stage F shipping condition)
- Owner: IMPLEMENT team

---

## §9 Stage E Exit Criteria

Stage E is complete and Stage F (Go/No-Go) may begin when ALL of the following hold:

| Criterion | Status |
|-----------|--------|
| 3 walkthrough observation forms filed in `compliance/walkthrough-observations/` | ⏳ PENDING |
| All forms de-identified (WX-01, WX-02, WX-03) | ⏳ PENDING |
| §6 data tables filled with observed values | ⏳ PENDING |
| §6.5 Go/No-Go decision input clear (ship/iterate/kill signal) | ⏳ PENDING |
| G8 accessibility items filed as R-14, R-15 in risk register | ✅ FILED — risk-register.md v2.1 |
| `stage-e-evidence.md` jury-cleared | ⏳ THIS JURY |

---

## §10 Law Citation Crosswalk

| Law ID | Title | Tier | Application |
|--------|-------|------|-------------|
| `PRD-2.5` | Evidence Gate Law | ⛔ NN | Stage E must be filed and jury-validated before Stage F |
| `PRD-5.1` | MVP Law | ⛔ NN | Walkthrough experiment design is the smallest valid test of the hypothesis |
| `PRD-5.2` | Build-Measure-Learn Law | Standard | Stage E data feeds Stage F BML decision |
| `PRD-5.3` | Experiment Design Law | Standard | Full observation protocol, metrics, and decision rules documented |
| `PRD-4.1` | Outcome-Based Roadmap Law | Standard | Stage E validates NOW horizon outcome |
| `BUS-1.1` | Priority Hierarchy Law | ⛔ NN | Legal first: G8 accessibility determination required |
| `BUS-2.3` | DOT Consumer Protection Law | ⛔ NN | Part 382 scope-out confirmed (internal tool); ADA Title I applies |
| `BUS-3.1` | Data Classification Law | ⛔ NN | Walkthrough observation forms: Internal; de-identified before filing |
| `BUS-4.3` | PII Minimisation Law | ⛔ NN | Adopter de-identified (WX-01/02/03); no names in filed forms |
| `BUS-7.2` | Evidence Integrity Law | Standard | SHA-256 manifest updated at Stage E gate |
| `ENG-6.1` | Security by Design Law | ⛔ NN | No new attack surfaces in walkthrough protocol |
| `ENG-10.1` | Metric Design Law | Standard | Primary/secondary/guardrail metrics specified; no PII in dimensions |
