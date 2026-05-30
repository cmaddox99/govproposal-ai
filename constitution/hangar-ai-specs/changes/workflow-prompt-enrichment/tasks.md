# Tasks: Workflow Prompt Enrichment

> **Change:** workflow-prompt-enrichment
> **Proposal:** `hangar-ai-specs/changes/workflow-prompt-enrichment/PROPOSAL.md`
> **Status:** Not Started
> **Lint/RAG baseline:** lint 15/17 PASS (2 pre-existing failures), RAG 90.4% PASS

---

## Phase 1 — Housekeeping: Fix Pre-existing Lint Failures

- [ ] 1.1 Add `ENG-12.1` to `laws/index.yaml` non_negotiable array
- [ ] 1.2 Verify no other pre-existing lint failures
- [ ] 1.3 Run `aa-constitution-lint .` → confirm 17/17 PASS before proceeding
- [ ] 1.4 Run RAG eval → confirm baseline ≥ 90.4% PASS
- [ ] 1.5 Commit: `fix(laws): add ENG-12.1 to index.yaml non_negotiable list (ENG-10.1)`

---

## Phase 2 — `skill-workflow-authoring` (Define the Contract First)

- [ ] 2.1 Create `agent-skills/skills-by-domain/development-practices/skill-workflow-authoring.md`
  - Required frontmatter schema (workflow.id, name, avatar_context, laws, skills, preceded_by)
  - Mandatory sections: Prerequisites, Phase Table, Per-Phase Detail, Failure Modes
  - Copilot prompt block format (environment setup → per-phase → evidence → recovery)
  - Evidence artifact template format (YAML frontmatter, required fields)
  - How to register in `workflows/README.md`
  - How to write the SDD proposal for a new workflow
  - COMPLIANT / VIOLATION examples
- [ ] 2.2 Add `skill-workflow-authoring` entry to `agent-skills/skills-by-domain/development-practices/index.yaml`
- [ ] 2.3 Run `aa-constitution-lint .` → still 17/17 PASS
- [ ] 2.4 Commit: `feat(skills): add skill-workflow-authoring — canonical workflow authoring contract (ENG-11.1)`

---

## Phase 3 — Enrich `legacy-rescue-decision-track.md`

Per `skill-workflow-authoring` contract. Each phase gets: step-by-step, Copilot prompts, evidence template, failure recovery.

- [ ] 3.1 Phase 1 (Archaeology): step-by-step + bounded-context-map evidence template + Copilot prompt
- [ ] 3.2 Phase 2 (Govern): step-by-step + proposal scaffold prompt + hangar-ai-specs/ structure
- [ ] 3.3 Phase 3 (Deliberate): step-by-step + REFACTOR/REWRITE deliberation prompts + SonarQube decision-input guidance + ADR template
- [ ] 3.4 Phase 4 (Extract): step-by-step + first vertical slice prompt (ENG-4.1 reference)
- [ ] 3.5 Phase 5 (Document): step-by-step + pattern library prompt + maintenance guidelines template
- [ ] 3.6 Phase 6 (Certify): step-by-step + certification evidence template + sonarqube-delta.md prompt
- [ ] 3.7 Add Failure Modes table (≥5 modes: no bounded context boundary, SonarQube baselines incomparable, deadlocked deliberation, ENG-12.1 dashboard not open, ADR missing law citations)
- [ ] 3.8 Run `aa-constitution-lint .` → 17/17 PASS; RAG eval → ≥ 90.4% PASS
- [ ] 3.9 Commit: `feat(workflows): enrich legacy-rescue-decision-track with per-phase guidance + Copilot prompts (ENG-11.1)`

---

## Phase 4 — Enrich `legacy-rescue-refactor.md`

- [ ] 4.1 Phase 1 (Assess): step-by-step + constitution audit prompt + violation-inventory evidence template
- [ ] 4.2 Phase 2 (Govern): step-by-step + remediation proposal scaffold + avatar activation prompt
- [ ] 4.3 Phase 3 (Characterize): step-by-step + atomic TDD characterization prompts + coverage evidence template + SonarQube ≥50%/mutation ≥70% gate
- [ ] 4.4 Phase 4 (Remediate): step-by-step + violation-priority prompts (Security > Correctness > Reliability) + SonarQube HARD_BLOCK recovery guidance
- [ ] 4.5 Phase 5 (Refactor): step-by-step + Boy Scout commit prompts + complexity reduction verification + sonarqube new_coverage ≥90%
- [ ] 4.6 Phase 6 (Certify): step-by-step + compliance report prompt + audit evidence package template (BUS-7.1)
- [ ] 4.7 Add Build Cycle Template (analogous to rewrite track — adapted for refactoring context)
- [ ] 4.8 Add Failure Modes table (≥5 modes: characterization reveals unknown behavior, P0 violations block refactor, CC won't reduce, mutation gate failure, security HARD_BLOCK)
- [ ] 4.9 Run `aa-constitution-lint .` → 17/17 PASS; RAG eval → ≥ 90.4% PASS
- [ ] 4.10 Commit: `feat(workflows): enrich legacy-rescue-refactor with per-phase guidance + Copilot prompts (ENG-11.1)`

---

## Phase 5 — Enrich `legacy-rescue-rewrite.md`

- [ ] 5.1 Phase 1 (Assess): step-by-step + violation inventory + behavioral contract discovery prompts
- [ ] 5.2 Phase 2 (Govern): step-by-step + rewrite proposal scaffold + parity test plan template
- [ ] 5.3 Phase 3 (Extract Spec): step-by-step + specification extraction prompts + golden-file generation guide
- [ ] 5.4 Phase 4 (Build): extend existing Build Cycle Template with Copilot prompt examples + SonarQube cycle gate guidance
- [ ] 5.5 Phase 5 (Validate Parity): step-by-step + parity report template + intentional divergence documentation format
- [ ] 5.6 Phase 6 (Certify): step-by-step + regulatory documentation prompts + decommission plan template
- [ ] 5.7 Add Failure Modes table (≥5 modes: golden-file mismatch >5%, intentional divergence disagreement, legacy blocked from decommission, parity regression, regulatory gap)
- [ ] 5.8 Run `aa-constitution-lint .` → 17/17 PASS; RAG eval → ≥ 90.4% PASS
- [ ] 5.9 Commit: `feat(workflows): enrich legacy-rescue-rewrite with per-phase guidance + Copilot prompts (ENG-11.1)`

---

## Phase 6 — Registry Updates + RAG Test Cases

- [ ] 6.1 Update `workflows/README.md`:
  - Add **Workflow File Format** section (canonical structure from `skill-workflow-authoring`)
  - Add note that prompts are embedded inline in each workflow file
  - Update table entries with law counts now reflecting ENG-12.1/12.2/12.3 additions
- [ ] 6.2 Create or update `tools/rag-eval/test-cases/workflows.yaml` — add tc-wf-001..tc-wf-006:
  - tc-wf-001: "How do I assess a legacy codebase for refactor vs rewrite?" → legacy-rescue-decision-track
  - tc-wf-002: "What Copilot prompts should I use for characterization tests on legacy Java?" → legacy-rescue-refactor
  - tc-wf-003: "How do I generate golden-file parity tests for a legacy rewrite?" → legacy-rescue-rewrite
  - tc-wf-004: "What SonarQube gate thresholds apply during a legacy refactor?" → legacy-rescue-refactor, ENG-4.11
  - tc-wf-005: "How do I file an ADR for a REFACTOR vs REWRITE decision?" → legacy-rescue-decision-track, BUS-7.1
  - tc-wf-006: "What evidence artifacts does the rewrite workflow require?" → legacy-rescue-rewrite, ENG-11.1
- [ ] 6.3 Run `aa-constitution-lint .` → 17/17 PASS
- [ ] 6.4 Run RAG eval → ≥ 90.4% PASS (target: improve workflow routing scores)
- [ ] 6.5 Commit: `feat(rag): add workflow routing test cases tc-wf-001..tc-wf-006 (ENG-11.1)`

---

## Phase 7 — Final Verification + Archive

- [ ] 7.1 Run full `aa-constitution-lint .` → 17/17 PASS
- [ ] 7.2 Run RAG eval → ≥ 90.4% PASS; document final scores
- [ ] 7.3 Update this tasks.md with final commit hashes and scores
- [ ] 7.4 Archive: move `hangar-ai-specs/changes/workflow-prompt-enrichment/` → `hangar-ai-specs/archive/workflow-prompt-enrichment/`
- [ ] 7.5 Commit: `feat(archive): workflow-prompt-enrichment complete — archive proposal (BUS-7.1)`
- [ ] 7.6 Push

---

## Progress Summary

| Phase | Total | Done | Remaining |
|-------|-------|------|-----------|
| 1. Housekeeping | 5 | 0 | 5 |
| 2. skill-workflow-authoring | 4 | 0 | 4 |
| 3. decision-track enrichment | 9 | 0 | 9 |
| 4. refactor enrichment | 10 | 0 | 10 |
| 5. rewrite enrichment | 9 | 0 | 9 |
| 6. Registry + RAG | 5 | 0 | 5 |
| 7. Final + Archive | 6 | 0 | 6 |
| **Total** | **48** | **0** | **48** |
