# Tasks: fix-invalid-law-references

## Progress
- [x] 3 of 3 tasks complete

## Tasks

| Status | Task | File | Detail | Commit |
|--------|------|------|--------|--------|
| [x] | 1. Replace BUS-12.1 → BUS-2.3 | `docs/guides/adoption/greenfield-mvp.md` | Lines 818, 827, 860, 1223 — 4 occurrences | — |
| [x] | 2. Remove ENG-14.1 from heading | `docs/guides/avatars/law-citation-guide.md` | Line 162: `### Code Quality Phase (ENG-8.1, ENG-14.1)` → `### Code Quality Phase` | — |
| [x] | 3. Verify linter passes for active files | — | BUS-12.1 and ENG-14.1 violations resolved. Residual ENG-10.1 failures remain in `hangar-ai-specs/archive/` — historical records the linter cannot currently exclude. Tracked in follow-up proposal: `fix-linter-archive-exclusion`. | — |

## Note

The linter (`aa-constitution-lint`) has no `--exclude` option. It flags invalid law
references in `hangar-ai-specs/archive/` which are immutable historical records and
should not be modified. A follow-up proposal should add archive exclusion support to
the linter tool.

