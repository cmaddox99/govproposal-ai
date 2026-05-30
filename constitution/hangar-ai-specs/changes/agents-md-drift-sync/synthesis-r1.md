---
schema_version: 1
verdict: REJECTED
juror_count: 5
jurors:
  - id: J1
    model: claude-opus-4.6
    verdict: CHALLENGED
  - id: J2
    model: claude-sonnet-4.6
    verdict: CHALLENGED
  - id: J3
    model: gpt-5.4
    verdict: CHALLENGED
  - id: J4
    model: gpt-5.2
    verdict: CHALLENGED
  - id: J5
    model: gpt-5.4-mini
    verdict: CHALLENGED
synthesizer: claude-opus-4.5
rounds:
  r1_completed: true
  r2_completed: false
---

# Synthesis R1 — agents-md-drift-sync Build→Ship

## R1 Jury Verdicts

| Juror | Model             | Verdict    |
|-------|-------------------|------------|
| J1    | claude-opus-4.6   | CHALLENGED |
| J2    | claude-sonnet-4.6 | CHALLENGED |
| J3    | gpt-5.4           | CHALLENGED |
| J4    | gpt-5.2           | CHALLENGED |
| J5    | gpt-5.4-mini      | CHALLENGED |

## Synthesis Verdict: REJECTED

All five jurors returned CHALLENGED verdicts citing blocking defects in the implementation against the approved PROPOSAL.md. After deduplication and cross-referencing, **seven distinct blocking corrections** remain. The most severe include inverted exit codes in legacy mode (directly contradicting PROPOSAL lines 117 and 199), misattribution of `law_id` in the A01 rule, missing section-name enum validation (a C5 requirement), and sibling path resolution anchored to CWD rather than project root. The `--dry-run` flag in safe mode is declared but not honored, creating data-loss risk. These defects collectively prevent Build→Ship gate passage.

## Blocking Corrections

### C-1: Legacy Mode Exit Codes Inverted
**Source:** J1
**Issue:** PROPOSAL lines 117 and 199 specify: exit 0 = pattern found (and written), exit 2 = pattern NOT detected. Implementation in `cli.py` lines 74-79 does the opposite: exits 0 when no legacy pattern found ("OK: No legacy protocol block found"), exits 2 when legacy IS found ("LEGACY: Unversioned protocol block detected").
**Required fix:** Invert the exit codes in legacy-mode path to match PROPOSAL: `sys.exit(0)` when `result.has_legacy` is True (detected + diff shown), `sys.exit(2)` when legacy pattern NOT detected.

### C-2: A01 Rule law_id Misattributed
**Source:** J2
**Issue:** `AgentsMdDriftRule.law_id` returns `"ENG-4.1"` (Atomic TDD). Per PROPOSAL frontmatter `laws: [ENG-1.2, ENG-10.1, ENG-11.1]`, the primary law for AGENTS.md currency is ENG-1.2 (AGENTS.md required and must be current).
**Required fix:** Change line 40 in `agents_md_sync.py` from `return "ENG-4.1"` to `return "ENG-1.2"`.

### C-3: Section-Name Enum Validation Absent
**Source:** J2, J3, J4, J5
**Issue:** PROPOSAL C5/C7 mandates: "Section names must match the enum exactly (unrecognized names → error)". Valid enum for MVP is `["mandatory-protocol"]` only. Neither `AgentsMdDriftRule` nor `aa-agents-sync` validates that parsed section names belong to the valid enum. Arbitrary section names pass silently.
**Required fix:** Add enum validation to both `AgentsMdDriftRule.evaluate()` and `aa-agents-sync` checker/syncer. Emit FAIL/error for any section name not in `VALID_SECTION_NAMES = {"mandatory-protocol"}`.

### C-4: Sibling Path Resolution Anchored to CWD Not Project Root
**Source:** J3, J4, J5
**Issue:** PROPOSAL C2 item 3 specifies: "Sibling directory named `hangar-ai-constitution` relative to the **project root**". Implementation in `resolver.py` lines 36-38 uses `Path.cwd().parent`, which resolves relative to current working directory, not the project root (AGENTS.md parent or git root).
**Required fix:** Change resolution to use the parent of the target AGENTS.md file path, or the git repository root, rather than CWD. Pass `agents_md_path` into `resolve_constitution_path()` and derive sibling from its parent.

### C-5: A01 Rule constitution_path Wiring Incorrect
**Source:** J3, J4
**Issue:** In `cli.py` line 119, `AgentsMdDriftRule(constitution_path=project_path)` passes `project_path` (the lint target) as constitution_path instead of the actual resolved constitution path. The `constitution_path` parameter from `get_default_rules(project_path, constitution_path)` is ignored.
**Required fix:** Change line 119 to `AgentsMdDriftRule(constitution_path=constitution_path)` to wire the resolved constitution path correctly.

### C-6: --dry-run Flag Not Honored in Safe Mode
**Source:** J4
**Issue:** When `--dry-run` is passed without `--legacy-mode` or `--check`, the CLI falls through to safe mode and calls `sync_agents_md()` unconditionally (line 92), ignoring the dry_run flag. This creates data-loss risk.
**Required fix:** In safe mode (the else branch starting line 81), check `if dry_run:` and emit a diff without writing, then exit 0. Only call `sync_agents_md()` when `dry_run` is False.

### C-7: Installed Package Fallback Missing
**Source:** J4
**Issue:** PROPOSAL C2 item 4 specifies fallback to "Installed package data (if `aa-constitution-lint` is pip-installed)". `resolver.py` returns None after checking sibling; no package data fallback exists.
**Required fix:** Add step 4 in `resolve_constitution_path()`: attempt to locate constitution data via `importlib.resources` or `pkg_resources` if pip-installed, before returning None.

## Dismissed Findings

### J3-C4: Same-Version Content Drift Not Detected — DISMISSED
**Rationale:** The approved PROPOSAL design explicitly uses version-marker comparison for drift detection. If body content changes within the same version, the constitution's `constitution-version.txt` must be bumped (CI-enforced per C6). Detecting content hash drift is not required by the PROPOSAL; version-based detection is the intended design.

### J3-C6 / J4-C2: Exit Code 2 Overloaded — DISMISSED
**Rationale:** PROPOSAL line 116 explicitly defines exit 2 with different semantics per mode: `--check` mode uses exit 2 for "drift detected", `--legacy-mode` uses exit 2 for "pattern not detected". This is intentional modal overloading documented in the approved PROPOSAL, not a violation of C8. The semantics are unambiguous within each mode context.

## Body

### Overview

The agents-md-drift-sync implementation achieves the core architectural goals but fails on seven specific compliance points against the approved PROPOSAL.md. The most critical defect (C-1) directly inverts documented exit code semantics, which would cause CI pipelines and adoption workflows to misinterpret legacy detection results. The law_id misattribution (C-2) undermines audit trail integrity per ENG-6.7.

### Enum Validation Gap (C-3)

The PROPOSAL's Marker Syntax Contract (C5) is explicit: "Section names must match the enum exactly (unrecognized names → error)". MVP scope (C7) defines exactly one valid section name: `mandatory-protocol`. The current implementation uses regex capture groups to extract section names but never validates them against the approved enum. This allows arbitrary section names like `<!-- BEGIN hangar-ai-constitution:foo v1.0.0 -->` to pass without error, violating C5.

### Path Resolution Defects (C-4, C-5, C-7)

Three jurors independently identified the sibling resolution bug: using `Path.cwd()` instead of project root means running `aa-agents-sync /other/project/AGENTS.md` from a different directory will look for the constitution sibling in the wrong location. The A01 wiring bug (C-5) compounds this: even when a correct `constitution_path` is passed to `get_default_rules()`, it's discarded in favor of `project_path`. The missing package fallback (C-7) breaks the "pip install" deployment model.

### Safe Mode --dry-run (C-6)

The flag is declared in the CLI but the safe mode code path ignores it entirely. A user expecting `aa-agents-sync ./AGENTS.md --dry-run` to preview changes without writing will instead get their file overwritten. This is a data-loss risk that violates the principle of least surprise and the PROPOSAL's "never silently overwrites" guarantee.

### Resolution Path

All seven corrections are surgical and do not require architectural changes. Estimated effort: 2-3 hours of implementation + test updates. Recommend R2 re-review after fixes are applied.
