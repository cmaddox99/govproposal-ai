# Tasks: mutation-tool-table-ssot

## Progress: 4 / 4 active tasks complete (TASK-1 eliminated; see note)

---

> **Note (2026-05-26 pre-implementation jury):**
> TASK-1 eliminated — jury found it redundant: TASK-3 removes the entire table,
> which would delete the row TASK-1 fixes and break TASK-1's test. TASK-3 absorbs
> TASK-1's `cosmic-ray` absence acceptance criteria. TASK-2b added: workflow Go row
> also has incorrect command (`gremlins unleash ./...` → `gremlins unleash`) per
> Gremlins official docs.

- [~] ~~**TASK-1**~~ *(eliminated — subsumed by TASK-3; see note above)*

- [x] **TASK-2** Fix Go tool `cosmic-ray` → `gremlins` in `agent-skills/skills-by-domain/development-practices/11-mutation-testing.md`
  - Scenario: Step 1 tool selection table; same error as law file
  - Acceptance: `gremlins` appears for Go row; `cosmic-ray` does not; command is `gremlins unleash` (from module root); notes mention module root requirement

- [x] **TASK-2b** Fix Go command + notes in `workflows/legacy-rescue-refactor.md` Tech Stack Translation table
  - Scenario: `gremlins unleash ./...` is not a valid Gremlins invocation; JSON output requires `--output` flag
  - Acceptance: Go command is `gremlins unleash`; notes updated to reflect module-root requirement and optional JSON via `--output=gremlins.json`

- [x] **TASK-3** Remove ENG-4.11 tool selection table from `laws/engineering/testing.md`; replace with delegation sentence to skill-11
  - Scenario: Law should specify thresholds and principles, not operational tool details; also absorbs TASK-1
  - Acceptance: Tool table removed; `cosmic-ray` does not appear anywhere in file; delegation sentence present referencing skill-11 path and section; explicit conflict-resolution ("if any workflow table conflicts, follow the skill") included; threshold percentages (≥70%, ≥85%) remain in law; `### Tool Selection` heading retained with normative paragraph (not blockquote)

- [x] **TASK-4** Add scoped Mutation Tool SSOT citation to `workflows/legacy-rescue-refactor.md`
  - Scenario: Workflow table is procedural; engineers should know skill-11 is the canonical source for mutation tools specifically
  - Acceptance: One-line note placed directly above `### Mutation Testing Tools` subsection; citation scoped to mutation testing (not all workflow tools); references skill-11 path
