# Registry Fix: Article XIV + ENG-12 Title Corrections

**Type:** Maintenance  
**Law:** ENG-14.1 (Law Citation Audit Gate), ENG-10.1 (Registry Completeness)  
**Priority:** P1 — unblocks PR #78 (CI gate failures)

## Problem

Three pre-existing registry drift issues were causing CI failures on all open PRs:

1. **Article XIV missing** — `ENG-14.1` and `ENG-14.2` were authored in
   `laws/engineering/citation-integrity.md` and registered in `laws/index.yaml`,
   but Article XIV was never added to `laws/engineering/_domain.yaml`. The
   governance test suite validates that every authored law appears in `_domain.yaml`.

2. **ENG-12 stale comments** — The three Article XII law titles in `_domain.yaml`
   were never updated after the laws were renamed:
   - ENG-12.1: "Agentic Feedback Loop Law" → "Agentic Phase Gate Law"
   - ENG-12.2: "Dashboard-First Development Law" → "Human-First Evidence Review Law"
   - ENG-12.3: "External Referee Law" → "Multi-Cognition Jury Referee Law"

3. **ENG-12.1 stale comment in `laws/index.yaml`** — Same title drift; cosmetic
   but creates inconsistency in tooling output.

## Changes

- `laws/engineering/_domain.yaml`:
  - Fixed ENG-12.1/12.2/12.3 inline comments to match current law titles
  - Added Article XIV section with ENG-14.1 (non-negotiable) and ENG-14.2

- `laws/index.yaml`:
  - Fixed ENG-12.1 inline comment (cosmetic; ensures consistent tooling output)

## What Is NOT Changed

- No law `.md` files modified
- No thresholds, enforcement levels, or policy text changed
- This is a pure registry synchronisation fix

## Precedent

Follows the pattern established by `hangar-ai-specs/changes/law-registry-eng-4-12-fix/`.
