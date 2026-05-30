# Prompt: Avatar Workflow Validate Mode — C++ Technology Avatar

> **Purpose:** Use this prompt to invoke the `avatar-workflow.md` Validate Mode
> on the C++ avatar after PR #14 merges. The output is a structured PASS/BLOCKED
> review comment incorporating both schema and RAG validation.
>
> **Workflow:** `workflows/avatar-workflow.md`
> **Mode:** 3 — Validate (read-only; no files modified)
> **Avatar:** `avatars/technology/cpp/`

---

## The Prompt

```
I need you to perform a full Avatar Workflow Validate Mode assessment of the
C++ technology avatar.

Workflow to follow: workflows/avatar-workflow.md
Mode: Mode 3 — Validate
Avatar path: avatars/technology/cpp/
Avatar type: technology

Follow the avatar-workflow exactly. Do not skip any phase or step. Run the
following phases in order:

PHASE 1 — IDENTIFY
  Confirm mode = Validate, type = technology, domain = cpp.
  Confirm avatar exists at avatars/technology/cpp/.

PHASE 2 — SCAN (all 5 safeguards)
  2.1 — Schema Completeness Check
    - manifest.yaml: all required fields present? version? activates.skills
      (≥2 entries, each skill file exists)? activates.workflows (each workflow
      file exists in /workflows/)? specializes_laws (≥1 non-negotiable)?
      all example_file references resolve to existing files on disk?
      CRITICAL: estimate manifest.yaml token count — budget is ≤150 tokens.
    - guidance.md: present? Non-Negotiable Laws section? token count ≤450?
    - examples/: directory present? one file per law in specializes_laws?
      each file ≤850 tokens?
  2.2 — Law Domain Boundary (Safeguard 2)
    For each entry in specializes_laws, verify ENG-* only (technology avatar).
    Any PRD-* or BUS-* entry = BLOCKING.
    For each file in examples/, verify no BUS-*.md or PRD-*.md filenames.
  2.3 — Law ID Validity (Safeguard 4)
    Each law ID in specializes_laws must exist in laws/engineering/_domain.yaml.
  2.4 — Shadow Governance (Safeguard 5)
    Scan all avatar files for: invented law IDs, ungrounded "must"/"required"
    without law citation, embedded skill definitions, law overrides/self-approval,
    unknown manifest blocks.
  2.5 — activates.skills Existence (Safeguard 5)
    Each skill in activates.skills must resolve to a file in agent-skills/.
    Inverse: any new skill files in examples/ not referenced in any avatar
    activates.skills = orphaned skill warning.
  2.6 — Blast Radius
    For any BLOCKING law boundary violation found in 2.2, identify all other
    technology avatars referencing the same law.

Commit your gap report to hangar-ai-specs/evidence/avatar-scan-cpp.md
(update the existing file with today's date and new findings).

PHASE 5 — RAG VALIDATE
  Define or use these 5 canonical queries for the cpp avatar:
    Q1: "How do I write a GoogleTest for a C++ class with RAII ownership?"
    Q2: "What is the correct way to handle errors in C++ without exceptions?"
    Q3: "How do I migrate from raw pointers to unique_ptr in a C++03 brownfield codebase?"
    Q4: "What sanitizers are mandatory in CI for C++ under this constitution?"
    Q5: "How does the compliance rating score a C++ project for safety-critical posture?"

  For each query:
    a) List every avatar file the RAG pipeline would load (manifest routing +
       specializes_laws example_file + guidance.md)
    b) Estimate total tokens for all loaded files combined
    c) Confirm the query is answerable from those files alone
    d) Flag any query where total tokens > 3,500 as FAIL

  Do NOT include full-reference.md in any query's loaded file set unless it is
  explicitly the only way to answer a query (it should be marked on_demand_only).

  Record results in hangar-ai-specs/evidence/avatar-rag-cpp.md.

OUTPUT FORMAT
  Produce a structured review comment using the PR Review template from the
  avatar-workflow (Phase PR.4). Even though this is Validate mode (read-only),
  use the same structured format so the output can be directly referenced in
  the Phase 18 remediation proposal. Include:

  ## Avatar Workflow Assessment — C++ Technology Avatar
  > Assessed against: docs/guides/avatar-model-schema.md
  > Mode: Validate (read-only)

  ### Verdict: ✅ PASS / 🔴 BLOCKED

  ## Safeguard 1 — Deduplication: [result]
  ## Safeguard 2 — Law Domain Boundary: [result with violation table if failed]
  ## Safeguard 3 — Product Taxonomy: N/A (technology avatar)
  ## Safeguard 4 — Law ID Validity: [result]
  ## Safeguard 5 — Shadow Governance & Skills Existence: [result]
  ## RAG Validation: [query table with token estimates]
  ## Required Changes Before Merge: [table if BLOCKED]

  After the structured review, append a section:
  ## Comparison with Panel Review
  Note any findings the panel review caught that the workflow missed, and
  any findings the workflow catches that the panel review missed. Pay
  particular attention to manifest.yaml token budget and activates.workflows
  reference validity.

IMPORTANT CONSTRAINTS
  - This is Mode 3 (Validate): do NOT modify any files except the two evidence
    files (avatar-scan-cpp.md and avatar-rag-cpp.md).
  - Cite workflow phase and step number for every finding (e.g., "Phase 2.1").
  - Use the severity levels from the workflow: 🔴 BLOCKING, 🟡 WARNING, 🟢 ADVISORY.
  - Do NOT merge findings from the panel review into the workflow output —
    they are separate assessments. Report them in the Comparison section only.

Context already known (do not re-investigate):
  - B-1 (broken RAG index path) was fixed in Phase 17, commit c4ab135.
  - B-2 (token overflow) has been identified but not yet fixed — it is Phase 1
    of the cpp-avatar-phase18-remediation proposal.
  - The existing avatar-scan-cpp.md documents Amendment O corrections (April 11).
    Today's scan should be a fresh scan of the post-Phase-17 state.
```

---

## What to Do with the Output

After running this prompt:

1. **Save the structured review comment** to
   `hangar-ai-specs/changes/c-plus-plus-avatar-enrichment/review/workflow-validate-report.md`
   (do not modify `panel-review.md`).

2. **Compare with the Phase 18 proposal** — the proposal's `PROPOSAL.md` already
   contains a Workflow vs Panel Analysis section. Update that section with any
   new findings surfaced by the workflow run.

3. **Key things to look for in the workflow output:**
   - Did manifest.yaml fail the 150-token budget? (expected: YES — ~1,500 tokens)
   - Did any activates.workflows entry fail existence check? (expected: `brownfield-adoption`)
   - Did Phase 5 RAG validation pass all 5 queries under 3,500 tokens each?
   - Were any orphaned skills flagged (Phase 2.5 inverse check)?
   - Were any shadow governance patterns found that the panel review missed?

4. **W-4 separate PR:** If the workflow confirms the manifest token budget failure,
   use the stub in `hangar-ai-specs/changes/cpp-avatar-manifest-restructure/PROPOSAL.md`
   (created in Phase 18 task 0.11) as the basis for the manifest restructure proposal.
