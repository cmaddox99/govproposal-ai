# Build Artifact: agents-md-drift-sync

> Phase Gate: Build→Ship
> Ref: PROPOSAL.md (APPROVED — unanimous 5-0, synthesis-r2.md)
> Implementation: TASK-1 through TASK-7 (all complete)

---

## What Was Built

The `agents-md-drift-sync` change implements a versioned-marker system to prevent
AGENTS.md drift in all hangar-ai-constitution adopting repositories. Per ENG-4.1,
all production code was written test-first (28 tests, all passing).

---

## Deliverables

### 1. `constitution-version.txt` (TASK-1)

Semver file at repo root (`1.0.0`). CI-enforced source of truth for the current
constitution template version. All tooling reads this file.

**Satisfies**: Proposal §"Version Source of Truth" and correction C6.

---

### 2. `templates/agents-md-sections/mandatory-protocol.md` (TASK-2)

Canonical embeddable block for the 8-step Mandatory Agent Protocol, bounded by
BEGIN/END markers at `v1.0.0`:

```
<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->
...8-step MANDATORY AGENT PROTOCOL (Per ENG-4.1 — NON-NEGOTIABLE)...
<!-- END hangar-ai-constitution:mandatory-protocol -->
```

**Satisfies**: Proposal §"Marker Syntax Contract" (C5), MVP scope (`mandatory-protocol`
section only per C7).

---

### 3. `tools/agents-md-sync/` — `aa-agents-sync` CLI tool (TASK-3–6)

Python package `aa-agents-sync v1.0.0`. Modules:

| Module | Responsibility |
|--------|---------------|
| `models.py` | `MarkerSection`, `CheckResult`, dataclasses |
| `parser.py` | `parse_markers()` — BEGIN/END regex, C5 structural validation |
| `resolver.py` | `resolve_constitution_path()` — CLI flag → env var → sibling dir (C2) |
| `checker.py` | `check_drift()` — version comparison, error propagation |
| `git_utils.py` | `is_git_dirty()` — git status check (C1) |
| `syncer.py` | `sync_agents_md()` — canonical template load, `_atomic_write()` (C1) |
| `legacy_detector.py` | `detect_legacy()` — ENG-4.1 anchor scan, unified diff |
| `cli.py` | Click entrypoint, all modes wired |

**CLI modes and exit codes (per C8, C9):**

| Mode | Flag | Exit 0 | Exit 1 | Exit 2 | Exit 3 |
|------|------|--------|--------|--------|--------|
| Check | `--check` | current | error | drift | — |
| Safe | (default) | no-op | error | — | written |
| Legacy | `--legacy-mode --dry-run` | no anchor | error | anchor found | — |

**Constitution path resolution order (C2):**
1. `--constitution-path` CLI flag
2. `HANGAR_CONSTITUTION_PATH` environment variable
3. Sibling directory named `hangar-ai-constitution`

**Atomic write (C1):** `tempfile.mkstemp(dir=parent)` → `fsync` → `os.replace`.
`--force` bypasses git dirty check.

**Marker syntax (C5):**
- BEGIN: `<!-- BEGIN hangar-ai-constitution:([a-z][a-z0-9-]+) v(\d+\.\d+\.\d+) -->`
- END:   `<!-- END hangar-ai-constitution:([a-z][a-z0-9-]+) -->`
- END name MUST match BEGIN name; mismatch → error, exit 1

---

### 4. `tools/constitution-lint/` — A01 rule (TASK-7)

`AgentsMdDriftRule` added to `aa-constitution-lint`:

| State | Result |
|-------|--------|
| Markers present and current | PASS |
| Markers present and stale | FAIL |
| No markers (legacy) | WARNING — run `--legacy-mode --dry-run` |
| `constitution-version.txt` not found | SKIP |
| No AGENTS.md | (no evaluation — not adopted) |

Registered in `get_default_rules()` in `cli.py`. Runs on every `aa-constitution-lint`
invocation.

---

## Test Coverage

28 unit tests, all passing. Per ENG-4.2:

| Test Group | Tests | Coverage |
|------------|-------|----------|
| TASK-1: version file | 2 | exists, valid semver |
| TASK-2: template file | 5 | exists, BEGIN/END, version match, ENG-4.1 anchor |
| TASK-3: scaffold | 7 | pyproject, entrypoint, module structure |
| TASK-4: --check mode | 5 | current/drift/exit-0/exit-2/syntax-error |
| TASK-5: safe mode | 3 | no-op/exit-3-sync/dirty-tree-refused |
| TASK-6: --legacy-mode | 3 | refuses-no-dry-run/exit-2-anchor/exit-0-clean |
| TASK-7: A01 rule | 3 | FAIL/WARN/PASS |

---

## Deviations from PROPOSAL.md

None. All approved corrections (C1–C10) implemented as specified.

MVP scope respected: only `mandatory-protocol` section in scope (C7). Sections
`phase-gate-subprotocol`, `rag-retrieval-protocol`, `quick-reference`,
`aviation-requirements` deferred to v1.1.

---

## Compliance Checklist

- [x] Tests written before code (ENG-4.1)
- [x] Atomic write implemented (C1)
- [x] Path resolution 3-tier (C2)
- [x] Legacy detection by exact anchor (C3)
- [x] Adoption workflow integration noted (C4 — A01 is the hard gate)
- [x] Marker syntax regex contract (C5)
- [x] `constitution-version.txt` at repo root (C6)
- [x] MVP scope = `mandatory-protocol` only (C7)
- [x] Exit code 2 = drift (non-overloaded) (C8)
- [x] `--legacy-mode` requires `--dry-run` at CLI level (C9)
- [x] END name matches BEGIN name enforced (C10)

---

## Commits

| Commit | Task | Summary |
|--------|------|---------|
| `503d3d3` | TASK-1 | constitution-version.txt |
| `2f31552` | TASK-2 | mandatory-protocol.md template |
| `1e5f9b9` | TASK-3 | aa-agents-sync scaffold |
| `c64ca3d` | TASK-4 | --check mode |
| `4691c5d` | TASK-5 | safe mode |
| `bb9bb7f` | TASK-6 | --legacy-mode --dry-run |
| `85042bd` | TASK-7 | A01 lint check |
