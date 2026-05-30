# Proposal: Register ENG-4.12 in Domain Registry

**Status:** ✅ COMPLETE
**Spec ID:** `law-registry-eng-4-12-fix`
**Triggered by:** CI governance test failures on `main` — `test_correctness_drift.py`
failing with 3 assertions after direct push `b842260` on May 8, 2026.
**Law reference:** ENG-11.1 (Hangar SDD), ENG-6.7 (Audit Trail)

---

## Problem Statement

`ENG-4.12` (Legacy Rescue Mutation Hardening Law) was authored in
`laws/engineering/testing.md` on May 8, 2026 (commit `b842260`) but was never
registered in `laws/engineering/_domain.yaml`. This caused three governance
test failures in CI on both `main` and all open PRs:

| Test | Failure message |
|------|----------------|
| `test_no_authored_law_is_missing_from_registry` | ENG-4.12: authored in testing.md but not listed in _domain.yaml |
| `test_every_authored_law_belongs_to_one_article` | ENG-4.12: authored in testing.md but not claimed by any article |
| `test_non_negotiable_flag_propagates_to_registry` | ENG-4.12: non_negotiable:true in law file testing.md but not listed in _domain.yaml Article IV non_negotiable set |

**Root cause:** `b842260` was a direct push to `main` (no PR), so CI did not
run pre-merge to catch the missing registration. The law body exists and is
correct; only the registry entry is missing.

**Principle (from `law-registry-reconciliation`):** `.md` body files are NOT
modified. All fixes go to `_domain.yaml`.

---

## Solution

Add `ENG-4.12` to `laws/engineering/_domain.yaml` Article IV:

1. Append `ENG-4.12  # Legacy Rescue Mutation Hardening Law` to the Article IV
   `laws:` list (after ENG-4.11).
2. Add `ENG-4.12` to the Article IV `non_negotiable:` list (law is marked
   NON-NEGOTIABLE in `testing.md`).

No other files require changes.

---

## Changes

| File | Change |
|------|--------|
| `laws/engineering/_domain.yaml` | Added ENG-4.12 to Article IV `laws:` list and `non_negotiable:` set |

---

## Amendment 1 — Also register ENG-4.12 in laws/index.yaml

**Status:** ✅ COMPLETE

### Problem

After the initial fix to `_domain.yaml`, the constitution lint still reported one
ENG-4.12 violation:

    ENG-4.12 has non_negotiable: true in law file but not listed in laws/index.yaml non_negotiable

`laws/index.yaml` maintains its own `non_negotiable.engineering` list and a full
law ID enumeration independently of `_domain.yaml`. Both must be updated when a
new non-negotiable law is authored.

### Changes

| File | Change |
|------|--------|
| `laws/index.yaml` | Added `ENG-4.12  # Legacy Rescue Mutation Hardening Law` to `non_negotiable.engineering` list |
| `laws/index.yaml` | Added `ENG-4.12` to the main law ID enumeration (after ENG-4.11) |

### Verification

Constitution lint: Passed 19, Failed 1 (only the unrelated missing avatar file remains).
ENG-4.12 violation fully resolved.

