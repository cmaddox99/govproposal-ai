---
id: fix-invalid-law-references
title: Fix Invalid Law References Flagged by Constitution Linter
status: proposed
submitted: 2026-04-07
author: willemlarsen
laws:
  - ENG-10.1  # Amendment Process Law
  - ENG-11.2  # Proposal Completeness Law
---

# Fix Invalid Law References Flagged by Constitution Linter

## Problem

Running `aa-constitution-lint .` produces one failing check (ENG-10.1):

> Invalid law references found: BUS-12.1 (×4), ENG-14.1 (×1)

These law IDs do not exist in any domain registry. They are stale or invented
citations that cause the linter to fail and mislead agents and engineers who
rely on law IDs to navigate the constitution.

| Invalid ID | Occurrences | File | Context |
|---|---|---|---|
| `BUS-12.1` | 4 | `docs/guides/adoption/greenfield-mvp.md` | "DOT fare transparency compliance" |
| `ENG-14.1` | 1 | `docs/guides/avatars/law-citation-guide.md` | "Code Quality Phase" heading example |

## Solution

Replace each invalid law ID with the correct existing law:

| Invalid ID | Correct Replacement | Rationale |
|---|---|---|
| `BUS-12.1` | `BUS-2.3` | BUS-2.3 is the DOT Consumer Protection Law — the correct citation for DOT fare transparency requirements |
| `ENG-14.1` | *(remove)* | The heading `### Code Quality Phase (ENG-8.1, ENG-14.1)` already had ENG-8.1 removed; ENG-14.1 never existed. The heading should stand alone without law citations. |

## Deliverables

1. `docs/guides/adoption/greenfield-mvp.md` — 4 occurrences of `BUS-12.1` replaced with `BUS-2.3`
2. `docs/guides/avatars/law-citation-guide.md` — `ENG-14.1` reference removed from heading
3. `aa-constitution-lint .` passes with 5/5 checks green

## Success Criteria

- `aa-constitution-lint .` exits with code 0 and `0 failed`
- No other files modified beyond the two listed above

## References

- ENG-10.1: Amendment Process Law — law citations must reference valid, registered law IDs
- ENG-11.2: Proposal Completeness Law — this proposal includes all required sections
