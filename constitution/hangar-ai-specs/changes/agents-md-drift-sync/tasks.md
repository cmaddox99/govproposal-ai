# Tasks: agents-md-drift-sync

> Ref: synthesis-r2.md — APPROVED (unanimous 5-0)
> MVP scope: `mandatory-protocol` section only

## Progress: 7/7 complete ✓

---

- [x] **TASK-1** `constitution-version.txt` ✓ 503d3d3
- [x] **TASK-2** `templates/agents-md-sections/mandatory-protocol.md` ✓ 2f31552
- [x] **TASK-3** `tools/agents-md-sync/` scaffold — pyproject.toml, aa_agents_sync/__init__.py, cli.py stub, tests/ ✓ 1e5f9b9

- [x] **TASK-4** `aa-agents-sync --check` mode — detect drift (exit 0=current, exit 2=drift, exit 1=error); validate marker syntax per C5 contract ✓ c64ca3d

- [x] **TASK-5** `aa-agents-sync` safe mode — constitution path resolution (C2), git-dirty check (C1), atomic write, exit codes (0=no-op, 3=written, 1=error) ✓ 4691c5d

- [x] **TASK-6** `aa-agents-sync --legacy-mode --dry-run` — detect legacy 8-step block by exact anchor, show diff; CLI refuses --legacy-mode without --dry-run (C9); exit codes (C8) ✓ bb9bb7f

- [x] **TASK-7** `aa-constitution-lint` check A01 — FAIL if any bounded section version < constitution-version.txt; WARN if no markers present ✓ 85042bd
