---
domain: engineering
article: XIV
title: Citation Integrity Laws
status: PROPOSED — not yet merged; requires Phase 8 executive approval (A-P2-006)
proposed_by: citation-auditor-2026-001 Phase 4
proposed_at: 2026-05-23
laws:
  - id: ENG-14.1
    title: Law Citation Audit Gate Law
    non_negotiable: true
    summary: Every artifact with law citations MUST pass aa-citation-audit before jury; ≥1 FAIL blocks jury invocation; tool unavailability halts jury (fail-closed)
  - id: ENG-14.2
    title: Jury Citation Auditor Law
    non_negotiable: false
    summary: PRD-2.6 jury panels meeting J6 activation conditions MUST include J6 Citation Auditor (gpt-4.1); elevated to NON-NEGOTIABLE if J6 detection rate >5% per 10 phases
---

# Article XIV: Citation Integrity Laws

> Govern the integrity of constitutional law citations in all Hangar AI Constitution
> workflow artifacts. These laws operate as a pre-jury gate (ENG-14.1) and a
> conditional jury-seat enhancement (ENG-14.2).

---

## ENG-14.1: Law Citation Audit Gate Law

**Law ID:** `ENG-14.1` | **Status:** NON-NEGOTIABLE

Every artifact containing law ID patterns (`[A-Z]+-\d+\.\d+` outside code blocks) MUST
pass `aa-citation-audit` before jury invocation.

### Requirements

1. **Pre-jury mandatory scan** — `aa-citation-audit <artifact.md>` before every
   jury invocation on any artifact containing law citations.
2. **Fail-closed** — If the tool is not installed or returns exit 2, jury MUST HALT.
   Silent advisory mode is prohibited.
3. **Registry source** — `laws/index.yaml` `law_ids` arrays are authoritative.
4. **Draft law exclusion** — `--allow-draft <ids>` excludes proposed-not-yet-merged
   IDs from FAIL checks. Preferred: `draft_ids` section in index.yaml.
5. **Verdict tiers:**
   - `FAIL` = ID not in registry → blocks jury
   - `WARN` = explicit title phrase in artifact contradicts registry title
   - `PASS` = all other citations
6. **FAIL blocks jury.** Re-run after correction; confirm exit 0 before proceeding.
7. **WARN passed to jury brief** — activates J6 per ENG-14.2 conditions.
8. **CI enforcement** — CI MUST re-execute `aa-citation-audit <artifact.md>` and assert
   exit code 0. Reading `fail_count` from frontmatter is NOT acceptable CI enforcement.

---

## ENG-14.2: Jury Citation Auditor Law

**Law ID:** `ENG-14.2` | **Status:** STRICTLY ENFORCED

PRD-2.6 jury panels meeting any J6 activation condition MUST include J6 Citation Auditor.

### J6 Activation Conditions (ANY triggers J6)

- L1 audit produced ≥1 WARN
- Artifact is Stage E or Stage F in product-discovery workflow
- Artifact cites ≥5 distinct law IDs in frontmatter `law_citations`

### Requirements

1. **Conditional 6th juror** — compliant 5-juror panel when no activation condition is met.
2. **Model: `gpt-4.1`** — Distinct from J1–J5 and Judicial Synthesizer. Inter-generation
   diversity (gpt-4.x vs gpt-5.x for J3/J4/J5).
3. **J6 responsibilities:** Verify cited law accuracy; detect citation omissions; detect
   status misrepresentation; flag contextual misapplication; resolve L1 WARNs.
4. **Citation-only scope** — J6 MUST NOT evaluate content claims. Non-citation J6
   findings are advisory only; carry no blocking weight.
5. **Mandatory verdict schema:**

   ```
   J6 — Citation Auditor | gpt-4.1
   Verdict: VALIDATED | QUALIFIED | CHALLENGED

   Citations audited: N
   Citations valid: N

   Citations challenged:
     - [law ID] | artifact span: "[exact quoted text]"
       Issue: ID_NOT_IN_REGISTRY | TITLE_MISMATCH | STATUS_MISREPRESENTED | CONTEXTUAL_MISAPPLICATION
       Registry says: "[actual title/summary/status]"
       Artifact says: "[what artifact claims]"

   Citation omissions detected:
     - Substance: "[quoted artifact text]"
       Applicable law: [best-match ID and title]

   L1 WARN resolution:
     - [law ID]: RESOLVED | UNRESOLVED | JUSTIFIED — [explanation]
   ```

6. **J6 CHALLENGED verdict** carries same blocking weight as content jurors (PRD-2.6 Req 10).
7. **Round 2 cross-pass** — J6 confirms Round 1 citation challenges resolved; checks for
   new citation issues introduced by corrections.
8. **Judicial Synthesizer Citation Integrity Block** (required in synthesis):

   ```
   Citation Integrity Block:
   - L1 audit status: PASS | WARN count: N
   - J6 verdict (if invoked): VALIDATED | QUALIFIED | CHALLENGED
   - Hallucinated IDs in final artifact: 0
   - Unresolved J6 CHALLENGED verdicts: 0
   ```

### Elevation Clause

If J6 CHALLENGED verdict rate exceeds 5% across any 10 consecutive discovery phases
post-deployment (measured per ENG-10.5), ENG-14.2 elevates to NON-NEGOTIABLE via the
executive approval process (index.yaml `non_negotiable` comment + human APPROVE gate).
