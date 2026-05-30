# Tasks — no-markers-fix

**Proposal:** aa-agents-sync No-Markers State Correctness
**Spec:** PROPOSAL.md in this directory
**Laws:** ENG-4.1, ENG-1.2, ENG-6.7

Progress: 12 / 12 tasks complete 🎉

---

## Tasks

- [x] **NM-1** — `check_drift()` returns `has_drift=True` for no-markers AGENTS.md
  - File: `tools/agents-md-sync/aa_agents_sync/checker.py`
  - Scenario: `nm-chk-01` — `has_drift = (not sections) or any(...)` fixes `any([]) == False` root cause
  - Priority: CRITICAL (root fix, all other tasks depend on this)

- [x] **NM-2** — `CheckResult` dataclass has `has_markers: bool` field
  - File: `tools/agents-md-sync/aa_agents_sync/models.py`
  - Scenario: `nm-chk-02` — new field defaults to `False`; enables syncer to distinguish insert vs. replace path

- [x] **NM-3** — `check_drift()` sets `has_markers=False` when no sections found
  - File: `tools/agents-md-sync/aa_agents_sync/checker.py`
  - Scenario: `nm-chk-03` — checker populates the new field; `has_markers=False` when `sections == []`

- [x] **NM-4** — `check_drift()` sets `has_markers=True` when sections exist
  - File: `tools/agents-md-sync/aa_agents_sync/checker.py`
  - Scenario: `nm-chk-04` — regression guard; existing AGENTS.md with markers still sets `has_markers=True`

- [x] **NM-5** — `--check AGENTS.md` (no markers) exits 2
  - File: `tools/agents-md-sync/aa_agents_sync/cli.py`
  - Scenario: `nm-cli-01` — CLI propagates `has_drift=True` (now true for no-markers) to exit 2

- [x] **NM-6** — `--check AGENTS.md` (no markers) prints `MISSING:` prefix
  - File: `tools/agents-md-sync/aa_agents_sync/cli.py`
  - Scenario: `nm-cli-02` — when `has_markers=False`, message prefix is `MISSING:` (distinct from `DRIFT:`)

- [x] **NM-7** — `sync_agents_md()` inserts canonical sections when `has_markers=False`
  - File: `tools/agents-md-sync/aa_agents_sync/syncer.py`
  - Scenario: `nm-syn-01` — new `_insert_sections_at_eof()` helper appends canonical blocks; `SyncResult.sections_updated` lists inserted names

- [x] **NM-8** — Existing AGENTS.md content preserved above inserted sections
  - File: `tools/agents-md-sync/aa_agents_sync/syncer.py`
  - Scenario: `nm-syn-02` — insertion appends (does not overwrite); original text present verbatim in result

- [x] **NM-9** — `--apply AGENTS.md` (no markers) exits 3
  - File: `tools/agents-md-sync/aa_agents_sync/cli.py`
  - Scenario: `nm-cli-03` — end-to-end: `--apply` with no-markers file → exit 3 (SYNCED)

- [x] **NM-10** — `--apply AGENTS.md` (no markers) prints `Inserted N canonical section(s)`
  - File: `tools/agents-md-sync/aa_agents_sync/cli.py`
  - Scenario: `nm-cli-04` — message distinguishes insert from update

- [x] **NM-11** — `--dry-run` with no markers shows insertion diff, exits 0
  - File: `tools/agents-md-sync/aa_agents_sync/cli.py`
  - Scenario: `nm-dry-01` — dry-run path detects `has_markers=False` and builds insertion diff (not "already current")

- [x] **NM-12** — `--legacy-mode --dry-run` (not found) message includes template path + `--apply` hint
  - File: `tools/agents-md-sync/aa_agents_sync/cli.py` (legacy_detector.py if needed)
  - Scenario: `nm-leg-01` — when no legacy block detected, message says where to find templates and to run `--apply`
