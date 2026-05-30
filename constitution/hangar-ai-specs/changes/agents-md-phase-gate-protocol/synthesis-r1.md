---
verdict: REJECTED
round: R1
jurors:
  - J1: { model: claude-opus-4.6, verdict: QUALIFIED }
  - J2: { model: gpt-5.2, verdict: CHALLENGED }
  - J3: { model: claude-sonnet-4.6, verdict: CHALLENGED }
  - J4: { model: gpt-5.4-mini, verdict: QUALIFIED }
synthesizer: { model: claude-opus-4.5 }
blocking_issues: 7
non_blocking_issues: 4
corrections_required: true
laws_invoked:
  - ENG-12.1
  - ENG-12.3
  - ENG-14.1
  - ENG-14.2
  - PRD-2.6
change_id: agents-md-phase-gate-protocol
deliberation_date: 2025-05-27
---

# Jury Synthesis — AGENTS.md Phase Gate Protocol Modification

**Change ID:** `agents-md-phase-gate-protocol`  
**Round:** R1  
**Verdict:** REJECTED  
**Synthesizer Model:** claude-opus-4.5

---

## 1. Executive Summary

This synthesis consolidates the findings of a 4-juror PRD-2.6 multi-cognition jury deliberation on a proposed modification to `AGENTS.md` that introduces a mandatory phase gate sub-protocol (citation audit → jury → jury gate → human review).

**Outcome:** The proposal is **REJECTED** in R1 due to 7 blocking issues identified by ≥2 jurors with primary source confirmation. Two jurors (J2, J3) returned CHALLENGED verdicts, which per PRD-2.6 Req 8 prevents advancement.

The core value of the change is recognized: AGENTS.md previously had no phase gate sub-protocol, and the proposed sequence order is faithful to source laws (ENG-12.1, ENG-14.1, PRD-2.6). However, implementation defects—particularly the 4 vs 5 juror discrepancy and missing operational definitions—would cause systematic gate failures if deployed.

---

## 2. Juror Verdicts Summary

| Juror | Model | Verdict | Blocking Issues | Non-Blocking Issues |
|-------|-------|---------|-----------------|---------------------|
| J1 — Domain Sceptic | claude-opus-4.6 | QUALIFIED | 2 | 2 |
| J2 — Technical Expert | gpt-5.2 | CHALLENGED | 4 | 2 |
| J3 — Product/Strategic Lens | claude-sonnet-4.6 | CHALLENGED | 3 | 2 |
| J4 — Defense Counsel | gpt-5.4-mini | QUALIFIED | 0 (acknowledged 2 weaknesses) | 0 |

---

## 3. Individual Juror Findings

### 3.1 J1 — Domain Sceptic (claude-opus-4.6): QUALIFIED

| Severity | Finding |
|----------|---------|
| **BLOCKING** | "MINIMUM 4 jurors" contradicts ENG-12.1 (5 jurors), ENG-12.3 (5 models J1–J5), and aa-jury-gate S09 (5 jurors). AGENTS.md internally contradicts itself: says "MINIMUM 4 jurors" in Step 2 but "Validates: 5 distinct models" in Step 3. Agents following this will produce 4-juror panels that fail the gate. |
| **BLOCKING** | Installation path `tools/aa-citation-audit` does not exist. Actual directory is `tools/citation-auditor`. The pip install command will fail. |
| NON-BLOCKING | Title says "3-tool sequence" but the protocol lists 4 steps. |
| NON-BLOCKING | aa-jury-gate check summary is partial (missing S01, S03–S08, S10, B01–B02). |

### 3.2 J2 — Technical Expert (gpt-5.2): CHALLENGED

| Severity | Finding |
|----------|---------|
| **BLOCKING** | "MINIMUM 4 jurors" vs aa-jury-gate S09 enforcing 5 — systematic gate failure trap. |
| **BLOCKING** | WARN semantics for aa-citation-audit not explicit: does WARN block jury? (Answer from law: NO — WARN is non-blocking but must be included in jury brief and triggers J6). An agent could interpret WARN as blocking. |
| **BLOCKING** | aa-jury-gate exit 2 (ERROR) not mentioned — only exit 1. Both non-zero exits must block advance. |
| **BLOCKING** | No operational definition of "phase gate" — agents will over-trigger or under-trigger. |
| NON-BLOCKING | Missing anti-pattern: "Invoking jury before phase artifact is committed to hangar-ai-specs/changes/" (ENG-12.2 Req 1). |
| NON-BLOCKING | "3-tool + human" count mismatch (minor). |

### 3.3 J3 — Product/Strategic Lens (claude-sonnet-4.6): CHALLENGED

| Severity | Finding |
|----------|---------|
| **BLOCKING** | "Phase gate" never defined — no trigger criteria for agents. |
| **BLOCKING** | No recovery path when aa-jury-gate exits 1 — agent halts indefinitely or invents recovery. |
| **BLOCKING** | "3-tool sequence" vs 4-step block — Step 4 (human review) risks being treated as optional. |
| NON-BLOCKING | Two disjoint prohibited-action tables with no cross-reference. |
| NON-BLOCKING | No actionable HOW for jury invocation (which tool to use, which model IDs per ENG-12.3). |

### 3.4 J4 — Defense Counsel (gpt-5.4-mini): QUALIFIED

| Category | Finding |
|----------|---------|
| **GENUINE STRENGTH** | Core value is real: AGENTS.md had no mention of the 3-tool sequence, ENG-12.1, ENG-14.1, or PRD-2.6 before this change. The gap existed. |
| **GENUINE STRENGTH** | Sequence order (citation audit → jury → jury gate → human) is faithful to source laws. |
| **GENUINE STRENGTH** | Placement between TDD protocol and Prohibited Actions is defensible. |
| WEAKNESS ACKNOWLEDGED | Install path `tools/aa-citation-audit` is wrong; correct is `tools/citation-auditor`. |
| WEAKNESS ACKNOWLEDGED | "5 distinct models" claim in aa-jury-gate description is directionally correct but underspecified. |

---

## 4. Consolidated Findings

### 4.1 What Is Proven (No Dispute Across Jurors)

These findings are confirmed by multiple jurors with no contradicting evidence:

1. **The gap existed:** AGENTS.md had no phase gate sub-protocol before this change. J4 confirms; J1/J2/J3 do not dispute.

2. **The sequence order is correct:** Citation audit → jury → jury gate → human follows the source laws (ENG-12.1, ENG-14.1, PRD-2.6).

3. **Non-negotiable law additions are valid:** ENG-12.1, ENG-14.1, and PRD-2.6 are all genuinely non-negotiable and were correctly added to the Non-Negotiable Laws list.

4. **Installation path is wrong:** `tools/aa-citation-audit` does not exist; correct path is `tools/citation-auditor`. (J1 + J4 confirm independently.)

5. **Juror count contradiction:** "MINIMUM 4 jurors" contradicts the operational enforcement:
   - PRD-2.6 sets constitutional floor at 4
   - ENG-12.1 raises it operationally to 5
   - aa-jury-gate S09 enforces 5
   - The proposed text internally contradicts itself (J1 + J2 confirm)

6. **"Phase gate" is undefined:** No trigger criteria exist in AGENTS.md. Agents cannot determine when to invoke the protocol. (J2 + J3 confirm.)

7. **No recovery path:** When aa-jury-gate returns FAIL, no guidance exists for what the agent should do. (J3 confirms; J2 implies.)

### 4.2 What Is Inferred (Strong Signal, ≥2 Jurors, Primary Sources Support)

8. **WARN semantics are ambiguous:** An agent could interpret aa-citation-audit WARN as blocking when per ENG-14.1/ENG-14.2 it is not. WARN must be passed to jury brief and activates J6. (J2 confirmed from source; law is clear.)

9. **Exit code 2 is omitted:** aa-jury-gate exit 2 (ERROR) is not mentioned and should also block advance alongside exit 1 (FAIL). (J2 confirmed from RUNBOOK.)

10. **Step count framing is misleading:** "3-tool sequence" does not match the 4-step numbered protocol. Human review in Step 4 risks being treated as optional. (J1 + J2 + J3 all raised variants.)

### 4.3 What Is Overclaimed / Needs Correction

11. **Imprecise validation description:** The sub-protocol says aa-jury-gate "Validates: 5 distinct models" — more precisely it validates 5 jurors (S09) each with a distinct model (S11). The synthesizer is a 5th distinct entity but is separate from the jurors. This is imprecise but not blocking.

12. **Disjoint prohibited-action tables:** Two tables exist (inline in sub-protocol + main section) with no cross-reference. Coherent but potentially confusing for compliance auditing.

### 4.4 What Is Unresolved / Needs Further Validation

13. **Synthesizer counting ambiguity:** Whether the synthesizer model counts toward aa-jury-gate's "5 jurors" S09 check remains unclear. J3 noted this; primary investigation needed before R2.

---

## 5. Verdict Rationale

**VERDICT: REJECTED**

Per PRD-2.6 Req 8:

> "A stage with one or more CHALLENGED findings that have not been corrected or formally rebutted CANNOT advance."

Two jurors (J2, J3) returned **CHALLENGED** verdicts. Seven blocking issues were identified by ≥2 jurors with primary source confirmation. The proposed AGENTS.md modification cannot advance to R2 until corrections are applied.

### Blocking Issue Tally

| Issue # | Description | Raised By |
|---------|-------------|-----------|
| B1 | 4 vs 5 jurors contradiction | J1, J2 |
| B2 | Wrong installation path | J1, J4 |
| B3 | Phase gate undefined | J2, J3 |
| B4 | WARN semantics ambiguous | J2 |
| B5 | Exit code 2 omitted | J2 |
| B6 | No recovery path | J3 |
| B7 | Step count mismatch | J1, J2, J3 |

---

## 6. Required Corrections Before R2

### 6.1 MUST FIX (Blocking)

These corrections are mandatory for R2 submission:

#### C1: Juror Count — 4 vs 5

**Current text (incorrect):**
> "MINIMUM 4 jurors"

**Required correction:**
> "5 jurors (J1–J5), each on a distinct model per ENG-12.3"

**Rationale:** PRD-2.6 sets a constitutional floor of 4, but ENG-12.1 and aa-jury-gate S09 enforce 5 operationally. The current text would cause systematic gate failures.

**Law citations:** ENG-12.1, ENG-12.3, aa-jury-gate S09

---

#### C2: Installation Path

**Current text (incorrect):**
```bash
cd tools/aa-citation-audit && pip install -e .
```

**Required correction:**
```bash
cd tools/citation-auditor && pip install -e .
```

**Rationale:** Directory `tools/aa-citation-audit` does not exist. The correct path is `tools/citation-auditor`.

**Law citations:** ENG-14.1

---

#### C3: Phase Gate Definition

**Current text:** No definition exists.

**Required addition:** Insert explicit trigger definition in the sub-protocol section:

> **Phase Gate Trigger Criteria**
>
> A phase gate occurs at:
> - SDD lifecycle phase transitions: Capture → Define → Design → Plan → Build → Ship
> - Product Discovery Stage exits: A, B, C, D, E, F
>
> Individual TDD commits within a phase are **NOT** phase gates and do not require jury deliberation.

**Rationale:** Without trigger criteria, agents cannot determine when to invoke the protocol, leading to over-triggering (every commit) or under-triggering (missing required gates).

**Law citations:** ENG-12.1, ENG-11.1

---

#### C4: WARN Semantics

**Current text:** WARN behavior not specified.

**Required addition:**

> **WARN Handling:** `aa-citation-audit` WARN status does **not** block jury invocation. However:
> - WARN findings MUST be included in the jury brief
> - WARN activates J6 (Citation Auditor juror) per ENG-14.2
> - Only FAIL status blocks advancement to jury

**Rationale:** Ambiguous WARN handling could cause agents to incorrectly block on non-blocking conditions.

**Law citations:** ENG-14.1, ENG-14.2

---

#### C5: Exit Code Handling

**Current text (incomplete):**
> "exit 1 = FAIL (blocks advance)"

**Required correction:**
> "Any non-zero exit blocks advance:
> - exit 0 = PASS (advance permitted)
> - exit 1 = FAIL (blocks advance — insufficient juror consensus)
> - exit 2 = ERROR (blocks advance — structural/validation error)"

**Rationale:** Exit code 2 (ERROR) also prevents advancement but was omitted from the specification.

**Law citations:** aa-jury-gate RUNBOOK

---

#### C6: Recovery Path

**Current text:** No recovery guidance exists.

**Required addition:**

> **ON FAIL/ERROR:**
> 1. Do NOT advance to next phase
> 2. Report failure details to human reviewer
> 3. Await explicit human direction before:
>    - Applying corrections to the change proposal
>    - Re-running the gate sequence from Step 1
> 4. Document correction rationale in change directory

**Rationale:** Without recovery guidance, agents will either halt indefinitely or invent potentially non-compliant recovery procedures.

**Law citations:** PRD-2.6 Req 8, ENG-12.1

---

#### C7: Step Count Framing

**Current text (inconsistent):**
> "mandatory 3-tool sequence"

**Required correction (choose one):**
- Option A: "mandatory 4-step gate sequence"
- Option B: "mandatory 3-tool + 1 human-approval sequence"

Apply consistently to:
- Sub-protocol header
- Quick Reference section
- Any other occurrences

**Rationale:** "3-tool sequence" describing a 4-step protocol causes Step 4 (human review) to appear optional when per ENG-1.2 it is mandatory.

**Law citations:** ENG-1.2

---

### 6.2 SHOULD FIX (Non-Blocking)

These corrections are recommended but not required for R2:

#### S1: Cross-Reference Prohibited Actions

Add a cross-reference from the main PROHIBITED ACTIONS table to the Phase Gate Anti-Patterns section:

> "See also: Phase Gate Anti-Patterns (above) for jury-specific prohibitions."

---

#### S2: Model ID Quick Reference

Add a Quick Reference snippet showing ENG-12.3 model IDs for agents constructing jury panels:

```markdown
### Jury Model Assignment (per ENG-12.3)

| Role | Model ID | Purpose |
|------|----------|---------|
| J1 — Domain Sceptic | claude-opus-4.6 | Challenge assumptions |
| J2 — Technical Expert | gpt-5.2 | Validate implementation |
| J3 — Product/Strategic | claude-sonnet-4.6 | Assess business alignment |
| J4 — Defense Counsel | gpt-5.4-mini | Advocate for proposal |
| Synthesizer | claude-opus-4.5 | Consolidate verdicts |
```

---

#### S3: Missing Anti-Pattern

Add to Phase Gate Anti-Patterns:

> "Invoking jury before phase artifact is committed to `hangar-ai-specs/changes/`" (per ENG-12.2 Req 1)

---

#### S4: Complete aa-jury-gate Check Summary

Expand the partial check summary to include all checks: S01–S11, B01–B02.

---

## 7. Unresolved Questions for R2

The following question requires investigation before R2 deliberation:

**UQ1: Synthesizer Counting**

Does the synthesizer model count toward aa-jury-gate's "5 jurors" check (S09)?

- J3 raised this ambiguity
- Current understanding: S09 counts J1–J5 (the 5 jurors); the synthesizer is a separate 6th entity
- Needs: Primary source confirmation from ENG-12.3 or aa-jury-gate implementation

---

## 8. Appendix: Law Citations

| Law ID | Title | Relevance |
|--------|-------|-----------|
| ENG-12.1 | Multi-Cognition Jury Deliberation | Requires 5 jurors for phase gates |
| ENG-12.3 | Jury Model Assignment | Specifies J1–J5 model identities |
| ENG-14.1 | Citation Audit Law | Governs aa-citation-audit behavior |
| ENG-14.2 | Citation Audit J6 Activation | WARN triggers J6 juror |
| PRD-2.6 | Multi-Cognition Deliberation | Constitutional floor of 4 jurors |
| ENG-11.1 | Hangar SDD Law | Phase lifecycle definitions |
| ENG-1.2 | Human Gate Enforcement | Human approval mandatory |
| ENG-12.2 | Jury Invocation Prerequisites | Artifact must be committed first |

---

## 9. Next Steps

1. **Author applies C1–C7 corrections** to the AGENTS.md proposal
2. **Author addresses S1–S4** (recommended but optional)
3. **Author investigates UQ1** and documents finding
4. **Author resubmits** for R2 deliberation
5. **Synthesizer convenes R2 jury** with updated proposal

---

*Synthesis generated by Judicial Synthesizer per PRD-2.6*
*Round: R1 | Date: 2025-05-27*
