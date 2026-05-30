# Tasks: workflow-human-gate-enforcement

> Spec ID: `workflow-human-gate-enforcement`
> Laws: ENG-12.1 (NON-NEGOTIABLE), ENG-1.2, ENG-4.1, ENG-6.7, BUS-7.1
>
> **Problem:** ENG-12.1 human gate checkpoints in the Legacy Rescue workflow are advisory
> prose — no mechanism prevents an agent from reading the rule and then bypassing it.
> This spec adds structural enforcement: a gate-check script agents MUST run before
> starting each phase, explicit STOP directives in the workflow, and prohibited-action
> entries in AGENTS.md.

---

## Workstream 1 — `tools/gate/phase-gate-check.sh`

- [x] **T-01** `phase-gate-check.sh` exists and is executable
- [x] **T-02** `phase-gate-check_withNoApprovalFile_exitsNonZero` — exits 1 and prints gate-locked message when `.phase-N.approved` is absent
- [x] **T-03** `phase-gate-check_withApprovalFile_exitsZero` — exits 0 and prints gate-open message when `.phase-N.approved` is present
- [ ] **T-04** `phase-gate-check_withMissingArgs_exitsNonZero` — exits 1 with usage error when PHASE or SPEC_ID is omitted

---

## Workstream 2 — `workflows/legacy-rescue-refactor.md`

- [ ] **T-05** Add `## ⛔ Human Gate Protocol` section at top of workflow with explicit STOP directives for agents — cites ENG-12.1
- [ ] **T-06** Add `⛔ AGENT STOP — HUMAN GATE` block after each phase in the Phase Table, with `phase-gate-check.sh` invocation command

---

## Workstream 3 — `AGENTS.md`

- [ ] **T-07** Add `Advancing to next Legacy Rescue phase without running phase-gate-check.sh` to PROHIBITED ACTIONS table citing ENG-12.1

---

## Progress

<!-- Updated after each completed TDD cycle -->
Completed: 3 / 7
