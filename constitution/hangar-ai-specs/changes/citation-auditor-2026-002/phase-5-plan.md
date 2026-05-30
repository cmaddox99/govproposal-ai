---
phase: 5
title: "Plan — aa-citation-audit v0.2.0 (HTML + L2 Widened Detection)"
project: citation-auditor-2026-002
workflow: greenfield-development
version: v1.2.0
status: APPROVED — Judicial Synthesis claude-opus-4.5 2026-05-25
judicial_synthesis:
  synthesizer: claude-opus-4.5
  verdict: APPROVED
  citations_verified: 21/21
  hallucinated_ids: 0
  j6_invoked: true
  p0_raised: 2
  p0_resolved: 2
  p1_raised: 10
  p1_resolved: 10
  phase_7_mandatory: [mutation-boundary-score-59-60-test, coverage-95pct-verified-pytest-cov]
  phase_7_advisory: [rapidfuzz-preexisting-P3, _skip-counter-semantics-P3]
  gate: UNLOCKED
author: Hangar AI (claude-sonnet-4.6)
date: 2026-05-25
law_citations: [PRD-2.6, ENG-1.5, ENG-2.2, ENG-2.3, ENG-3.4, ENG-3.7, ENG-4.1, ENG-4.6, ENG-4.9, ENG-4.11, ENG-6.5, ENG-10.1, ENG-10.2, ENG-12.1, ENG-14.1, ENG-14.2, BUS-7.1]
preceding_phase_approved: "phase-4-design.md v1.2.0 (APPROVED claude-opus-4.5 2026-05-25)"
j6_activation: "17 distinct law IDs — ENG-14.2 condition 3 ≥5; J6 advisory"
phase_7_conditions_from_synthesis: [C7-001 pinned regression fixtures, C7-002 RUNBOOK L2 section, C7-003 36 tests ≥95%/≥85%]
r1_corrections:
  - C-P5-001: Dependency graph redrawn — S-04 now depends on S-01+S-02+S-03 (T-29 requires widened auditor); S-02 → S-05 edge added; critical path is max(S-01,S-02) → S-03 → S-04 → S-05 → S-06
  - C-P5-002: T-30/T-31 reassigned from scanner to auditor unit tests; pyramid counts updated (scanner 8, auditor 15, total 36)
  - C-P5-003: P0 algorithm fix — plain-text extraction added to before-window branch in _check_title_mismatch(); else clause with re.search trailing-anchor plain-text pattern; T-11 WARN now fires for "God classes decomposed (ENG-6.4)"
  - C-P5-004: "from html.parser import HTMLParser" import added to S-01 scanner.py changes
  - C-P5-005: attrs annotation corrected from object to list[tuple[str, str | None]]
  - C-P5-006: S-04 deliverable clarified as test_bdd_html.py following CliRunner pattern; no Gherkin/features/ directory (none exists in project)
  - C-P5-007: T-34 added (.md file does NOT invoke _strip_html()); total updated to 34
  - C-P5-008: Dead _SEPARATOR_RE constant removed from S-02 constants list
  - C-P5-009: ENG-4.1 RED→GREEN per-slice statement added to §1 preamble
  - C-P5-010: T-35 (empty registry_title short-circuits), T-36 (unclosed <p> HTML still scans); total 36 tests; C7-003 updated
  - C-P5-011: ENG-11.1 removed — HTML extension is additive/backward-compatible, no feature flag required
  - C-P5-012: ENG-4.6 cited for ≥95% branch coverage target; ENG-4.11 retained for mutation ≥85% only; ENG-4.9 added for regression fixture contract-testing rationale
  - C-P5-013: S-02 complexity note added (highest-risk slice, may require intra-slice checkpointing)
r2_corrections:
  - C-P5-014: Spurious S-02→S-03 edge removed — S-03 depends only on S-01; S-02 runs fully parallel to S-01 and S-03; critical path corrected to S-01→S-03→S-04→S-05→S-06 with S-02 parallel prerequisite for S-04/S-05; S-02 SP 5→6 (owns T-30/T-31 + T-35 assertions); S-05 SP 2→1 (fixtures + RUNBOOK only)
  - C-P5-015: J2 P3 advisory logged — re.search is leftmost-first; code comment "rightmost word sequence" is technically inaccurate; corrected comment to "word sequence ending before trailing separator"; non-blocking
---

# Phase 5 — Plan: aa-citation-audit v0.2.0

**Jury focus (greenfield-development.md §Per-Phase Jury Focus):**
"Slice independence; dependency accuracy; test pyramid balance; estimate realism"

**Constitutional gate:** Implementation proposal approved in `hangar-ai-specs/changes/` before Phase 6 Build begins.

**ENG-4.1 NON-NEGOTIABLE per-slice constraint (C-P5-009):** Each slice follows strict RED→GREEN→REFACTOR. No implementation line is written until its covering test(s) exist and fail on v0.1.0 code. This applies to every test T-01 through T-36.

---

## 0. Problem / Solution Recap (ENG-11.2)

`aa-citation-audit` v0.1.0 has two confirmed enforcement gaps reported by Jason (post-delivery):

1. **HTML not supported** — `cli.py` line 246 enforces `.md`-only extension. All HTML workflow artifacts (`exec-deck.html`, stage discovery pages) are ungated by the auditor.
2. **L2 contextual misapplication not detected** — `_check_title_mismatch()` scans only 30 chars after the law ID using `_TITLE_PHRASE_RE` (bold/quoted/parens). It misses:
   - Table cells: `| ENG-6.4 | No God Classes |`
   - Em-dash patterns: `ENG-6.4 — No God Classes`
   - Description-before-ID: `God classes decomposed (ENG-6.4)`

Phase 4 Design (APPROVED v1.2.0) specifies two enhancements that close these gaps:

- **`_HTMLStripper`** — stdlib `html.parser` subclass; strips `<script>`/`<style>` tags; T-14 unclosed-tag guard; no new dependencies (ENG-6.5).
- **Widened `_check_title_mismatch()`** — 120-char after-window, 80-char before-window, `_SEPARATOR_RE` structural separator guard (dual-anchor for after-window; trailing-anchor for before-window), `_extract_title_candidates()` plain-text extraction, `findall[-1]` closest-match.

Phase 5 decomposes the approved design into 6 independent vertical slices for atomic TDD delivery (ENG-4.1 NON-NEGOTIABLE).

---

## 1. Vertical Slice Definitions

### S-01: `scanner.py` — HTML stripping

| Field | Value |
|-------|-------|
| Slice ID | S-01 |
| Complexity | 3 story points |
| Depends on | None (additive to existing `scan_artifact()`) |
| Layer | scanner.py |

**Files modified:**
```
tools/citation-auditor/src/citation_auditor/scanner.py
```

**Files added:**
```
tools/citation-auditor/tests/fixtures/scanner/artifact_html_basic.html
tools/citation-auditor/tests/fixtures/scanner/artifact_html_script_strip.html
tools/citation-auditor/tests/fixtures/scanner/artifact_html_unclosed_script.html
tools/citation-auditor/tests/fixtures/scanner/artifact_html_table_ids.html
tools/citation-auditor/tests/fixtures/scanner/artifact_html_empty.html
```

**Changes to `scanner.py`:**

1. Add import (C-P5-004):
```python
from html.parser import HTMLParser
```

2. Add `_HTMLStripper` class (stdlib only — ENG-6.5; C-P5-005 attrs annotation fix):
```python
class _HTMLStripper(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip: bool = False
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style"}:
            self._skip = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style"}:
            self._skip = False

    def handle_data(self, data: str) -> None:
        if not self._skip:
            self._buf.append(data)

    def get_text(self) -> str:
        return " ".join(self._buf)
```

2. Add `_strip_html(text: str) -> str` function:
```python
def _strip_html(text: str) -> str:
    """Strip HTML tags and return plain text. Raises AuditError on unclosed script/style."""
    try:
        stripper = _HTMLStripper()
        stripper.feed(text)
        stripper.close()
        if stripper._skip:
            raise AuditError("Unclosed <script> or <style> tag in HTML artifact (T-14)")
        return stripper.get_text()
    except AuditError:
        raise
    except Exception as exc:
        raise AuditError(f"HTML parse failure: {exc}") from exc
```

3. Modify `scan_artifact()` — detect `.html`/`.htm` and apply `_strip_html()` before Pass 1/2:
```python
suffix = artifact_path.suffix.lower()
if suffix in {".html", ".htm"}:
    text = _strip_html(text)
# existing Pass 1/2 (fenced code + inline code stripping) unchanged
```

**Unit tests added to `tests/unit/test_scanner.py`:**

| Test ID | Description |
|---------|-------------|
| T-01 | `artifact_html_basic.html` — basic HTML IDs extracted correctly |
| T-02 | `artifact_html_script_strip.html` — IDs inside `<script>` block NOT extracted |
| T-03 | `artifact_html_script_strip.html` — IDs inside `<style>` block NOT extracted |
| T-04 | `artifact_html_unclosed_script.html` — raises `AuditError` (T-14) |
| T-05 | `artifact_html_table_ids.html` — IDs in `<table><td>` extracted |
| T-06 | `artifact_html_empty.html` — empty body returns empty citations list |
| T-07 | `_strip_html()` returns plain text, HTML attributes not extracted |
| T-08 | HTML comments (`<!-- ENG-6.4 -->`) — IDs NOT extracted (not in `handle_data`) |
| T-34 | `scan_artifact()` on `.md` file does NOT invoke `_strip_html()` — regression guard (C-P5-007) |

**Synthetic fixture content:**

`artifact_html_basic.html`:
```html
<html><body><p>This satisfies ENG-3.4 requirements.</p></body></html>
```
Expected: `ENG-3.4` found.

`artifact_html_script_strip.html`:
```html
<html><body>
<p>See ENG-3.4.</p>
<script>var x = "ENG-6.4";</script>
<style>.cls { /* ENG-6.5 */ }</style>
</body></html>
```
Expected: only `ENG-3.4` found; `ENG-6.4` and `ENG-6.5` excluded.

`artifact_html_unclosed_script.html`:
```html
<html><body><script>var x = "ENG-3.4";
</body></html>
```
Expected: `AuditError` raised (T-14).

`artifact_html_table_ids.html`:
```html
<html><body><table>
<tr><td>ENG-6.4</td><td>No God Classes</td></tr>
</table></body></html>
```
Expected: `ENG-6.4` found.

`artifact_html_empty.html`:
```html
<html><body></body></html>
```
Expected: empty citations list.

---

### S-02: `auditor.py` — Widened L2 detection

| Field | Value |
|-------|-------|
| Slice ID | S-02 |
| Complexity | 6 story points |
| Depends on | S-01 (no import dependency — pure logic; parallel build safe) |
| Layer | auditor.py |

**Files modified:**
```
tools/citation-auditor/src/citation_auditor/auditor.py
```

**Changes to `auditor.py`:**

> **S-02 complexity note (C-P5-013):** This is the highest-risk slice. The rewrite introduces 4 new constructs (extended windows, dual-anchor guard, plain-text extraction, before-window scan). Intra-slice checkpointing recommended: implement constants + `_extract_title_candidates()` first (T-18/T-19/T-20), then rewrite `_check_title_mismatch()` (T-09–T-17), then add T-21 boundary test.

1. Add/modify constants (C-P5-008 — `_SEPARATOR_RE` removed as it was dead code):
```python
_TITLE_WINDOW = 120          # was 30 — widened per Phase 4 §3.2
_TITLE_BEFORE_WINDOW = 80    # new — backward scan window
```

2. Add `_extract_title_candidates(window: str, *, plain_text_allowed: bool) -> list[str]`:
```python
def _extract_title_candidates(window: str, *, plain_text_allowed: bool) -> list[str]:
    """Return candidate title phrases from window.

    Source 1 (always): formatted phrases via _TITLE_PHRASE_RE.
    Source 2 (dual-anchor only): plain-text extraction — only when window BOTH
      starts AND ends with a structural separator character (e.g. `| title |`).
    """
    candidates: list[str] = []
    # Source 1: formatted phrases
    for m in _TITLE_PHRASE_RE.finditer(window):
        phrase = next(g for g in m.groups() if g is not None).strip()
        if phrase:
            candidates.append(phrase)
    # Source 2: plain-text (dual-anchor guard)
    if plain_text_allowed:
        leading  = bool(re.match(r'^[\s|—–\-:()\[\]]', window))
        trailing = bool(re.search(r'[\s|—–\-:()\[\]]\s*$', window))
        if leading and trailing:
            plain = re.match(r'^[^A-Za-z]*([A-Za-z]\w*(?:\s+[A-Za-z]\w*){1,5})', window)
            if plain:
                candidates.append(plain.group(1).strip())
    return candidates
```

3. Rewrite `_check_title_mismatch()`:
```python
def _check_title_mismatch(law_id: str, snippet: str, registry_title: str) -> str | None:
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None
    id_end = pos + len(law_id)

    # After-window: 120 chars (widened)
    window_after = snippet[id_end: id_end + _TITLE_WINDOW]

    # Before-window: 80 chars — only use if ends with structural separator
    id_start = pos
    window_before_raw = snippet[max(0, id_start - _TITLE_BEFORE_WINDOW): id_start]
    before_anchor = bool(re.search(r'[|—–\-:()\[\]]\s*$', window_before_raw))

    # Collect candidates from after-window (dual-anchor for plain-text)
    candidates = _extract_title_candidates(window_after, plain_text_allowed=True)

    # Collect candidates from before-window (trailing-anchor only; use findall[-1])
    # C-P5-003 P0 fix: adds plain-text extraction when no formatted phrase found
    if before_anchor:
        all_before = _TITLE_PHRASE_RE.findall(window_before_raw)
        if all_before:
            # findall returns tuples of groups; find last non-empty (closest to ID)
            for groups in reversed(all_before):
                phrase = next((g for g in groups if g), None)
                if phrase:
                    candidates.append(phrase.strip())
                    break
        else:
            # Plain-text extraction from before-window: extract word sequence ending
            # before the trailing separator (catches "God classes decomposed (ENG-6.4)")
            plain = re.search(
                r'([A-Za-z]\w*(?:\s+[A-Za-z]\w*){1,5})\s*[|:()\[\]\s]*$',
                window_before_raw,
            )
            if plain:
                candidates.append(plain.group(1).strip())

    # Score all candidates against registry title
    for phrase in candidates:
        if not phrase:
            continue
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue
        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )
    return None
```

**Unit tests added to `tests/unit/test_auditor.py`:**

| Test ID | Description |
|---------|-------------|
| T-09 | `\| ENG-6.4 \| No God Classes \|` → WARN (table cell, dual-anchor) |
| T-10 | `ENG-6.4 — No God Classes` → WARN (em-dash separator) |
| T-11 | `God classes decomposed (ENG-6.4)` → WARN (before-window trailing `(`) |
| T-12 | `ENG-4.3 WireMock consumer contracts` → PASS (plain prose, no anchors) |
| T-13 | `\| ENG-6.4 \| Data Protection \|` → PASS (correct title in table) |
| T-14 | `ENG-3.4 (Single Responsibility)` → PASS (correct title in parens) |
| T-15 | `see ENG-6.4` → PASS (no mismatch phrase present) |
| T-16 | `must review ENG-3.4` → PASS (no false WARN from prose) |
| T-17 | `ENG-6.4: This requirement must not...` → PASS (colon-prose — dual-anchor prevents false WARN; only leading separator, no trailing) |
| T-18 | `_extract_title_candidates` with dual-anchor `\| title \|` → plain-text extracted |
| T-19 | `_extract_title_candidates` with colon-only prefix `ENG-6.4: prose` → plain-text NOT extracted |
| T-20 | before-window `findall[-1]` picks closest phrase to ID |
| T-21 | phrase exactly 4 chars accepted (`test_mismatch_phrase_exactly_4_chars_accepted`) |
| T-30 | `artifact_regression_disc2026004_eng64.md` — `| ENG-6.4 | No God Classes |` → WARN (reassigned from scanner — C-P5-002) |
| T-31 | `artifact_regression_disc2026004_eng43.md` — `ENG-4.3 WireMock consumer contracts` → PASS known limitation (reassigned from scanner — C-P5-002) |
| T-35 | Empty/blank `registry_title` — `_check_title_mismatch()` short-circuits, no WARN (C-P5-010) |

---

### S-03: `cli.py` — Surface 1 extension update

| Field | Value |
|-------|-------|
| Slice ID | S-03 |
| Complexity | 1 story point |
| Depends on | S-01 (scanner must handle HTML before cli allows it) |
| Layer | cli.py |

**Files modified:**
```
tools/citation-auditor/src/citation_auditor/cli.py
```

**Change (line 246):**
```python
# Before:
if artifact_path.suffix.lower() != ".md":
    _exit2(f"Artifact must have .md extension: {artifact}")

# After:
_ALLOWED_SUFFIXES = {".md", ".html", ".htm"}
if artifact_path.suffix.lower() not in _ALLOWED_SUFFIXES:
    _exit2(f"Artifact must have .md, .html, or .htm extension: {artifact}")
```

**Unit tests added to `tests/unit/test_cli.py`:**

| Test ID | Description |
|---------|-------------|
| T-22 | `.html` extension accepted at Surface 1 |
| T-23 | `.htm` extension accepted at Surface 1 |
| T-24 | `.txt` extension rejected with exit(2) |
| T-25 | `.HTML` (uppercase) accepted (`.lower()` normalises) |

---

### S-04: `test_bdd_html.py` — HTML scanning end-to-end

| Field | Value |
|-------|-------|
| Slice ID | S-04 |
| Complexity | 3 story points |
| Depends on | S-01, S-02, S-03 (HTML scan + widened auditor + cli gate must all be live — C-P5-001) |
| Layer | tests/bdd/ |

**Files added:**
```
tools/citation-auditor/tests/bdd/test_bdd_html.py
tools/citation-auditor/tests/fixtures/bdd/artifact_html_valid.html
tools/citation-auditor/tests/fixtures/bdd/artifact_html_script_ids.html
tools/citation-auditor/tests/fixtures/bdd/artifact_html_unclosed_tag.html
```

**Pattern:** Follow existing CliRunner pattern in `tests/bdd/test_bdd_core.py` — no Gherkin/pytest-bdd (C-P5-006: no `.feature` file infrastructure exists in project).

**Test scenarios in `test_bdd_html.py`:**

| Test ID | Description |
|---------|---------|
| T-26 | `.html` file with valid citations → exit 0, ENG-3.4 shows PASS |
| T-27 | `<script>` block IDs → not extracted (ENG-6.4 absent from output) |
| T-28 | Unclosed `<script>` tag → exit 2, stderr contains "Unclosed" |
| T-29 | HTML table cell `<td>ENG-6.4</td><td>No God Classes</td>` with wrong registry title → WARN with "Title phrase score" in note (requires S-02 widened auditor) |

**Fixture content:**

`artifact_html_valid.html`:
```html
<!DOCTYPE html><html><body><p>This satisfies ENG-3.4 requirements.</p></body></html>
```

`artifact_html_script_ids.html`:
```html
<html><body><p>See ENG-3.4.</p><script>var x = "ENG-6.4";</script></body></html>
```

`artifact_html_unclosed_tag.html`:
```html
<html><body><script>var x = "ENG-3.4";
</body></html>
```

---

### S-05: Regression fixtures + RUNBOOK.md update

| Field | Value |
|-------|-------|
| Slice ID | S-05 |
| Complexity | 1 story point |
| Depends on | S-01, S-02, S-03 (must be built before RUNBOOK documents behavior) |
| Layer | docs + tests/fixtures/ |

**Files modified:**
```
tools/citation-auditor/RUNBOOK.md
```

**Files added:**
```
tools/citation-auditor/tests/fixtures/scanner/artifact_regression_disc2026004_eng64.md
tools/citation-auditor/tests/fixtures/scanner/artifact_regression_disc2026004_eng43.md
```

**RUNBOOK.md additions:**

Section: `## HTML Artifact Scanning (v0.2.0+)` — covering:
- Supported extensions: `.md`, `.html`, `.htm`
- How `_HTMLStripper` works: text nodes extracted, `<script>`/`<style>` stripped
- Limitations: HTML comments and CSS pseudo-content not scanned (by design)
- `AuditError` on unclosed `<script>`/`<style>`: add `</script>` or `</style>` to fix

Section: `## L2 Contextual Mismatch (v0.2.0+)` — covering:
- What WARN means for title mismatch
- Dual-anchor guard: when WARNs fire vs. do not fire
- False-WARN triage for colon patterns (`ENG-X.Y: This...` → PASS by design)
- Known limitation: pure-prose misapplication (`ENG-4.3 WireMock contracts`) not caught → jury is required (J6)
- ENG-4.3 WireMock example as explicit RUNBOOK entry

**Regression tests (C-P5-002 — reassigned to `tests/unit/test_auditor.py`, not scanner):**

| Test ID | Description |
|---------|-------------|
| T-36 | `artifact_html_unclosed_p.html` — unclosed `<p>` (benign malformed) still scans IDs normally (C-P5-010) |

Note: T-30 and T-31 (WARN/PASS behavioral assertions on regression fixtures) are owned by S-02 (`test_auditor.py`). S-05 provides the fixture files; assertions live with the auditor unit tests.

**Synthetic fixture content:**

`artifact_regression_disc2026004_eng64.md` (representative of Jason's error):
```markdown
---
law_citations: [ENG-6.4]
---
# Stage D — Architecture

| Law | Requirement |
|-----|-------------|
| ENG-6.4 | No God Classes |
```

`artifact_regression_disc2026004_eng43.md` (prose case — expected PASS):
```markdown
---
law_citations: [ENG-4.3]
---
# Contract Testing

ENG-4.3 WireMock consumer contracts verify service boundaries.
```

`artifact_html_unclosed_p.html` (benign malformed — T-36):
```html
<html><body><p>See ENG-3.4.<p>Also see ENG-4.9.</body></html>
```
Expected: `ENG-3.4` and `ENG-4.9` found (unclosed `<p>` is not a guard tag — only `<script>`/`<style>` trigger AuditError).

---

### S-06: Version bump `0.1.0` → `0.2.0`

| Field | Value |
|-------|-------|
| Slice ID | S-06 |
| Complexity | 1 story point |
| Depends on | S-01, S-02, S-03, S-04, S-05 (all slices must be complete) |
| Layer | __init__.py + pyproject.toml |

**Files modified:**
```
tools/citation-auditor/src/citation_auditor/__init__.py
tools/citation-auditor/pyproject.toml
```

**Changes:**
```python
# __init__.py
__version__ = "0.2.0"
```

```toml
# pyproject.toml
version = "0.2.0"
```

**Tests added to `tests/unit/test_cli.py`:**

| Test ID | Description |
|---------|-------------|
| T-32 | `aa-citation-audit --version` outputs `aa-citation-audit, version 0.2.0` |
| T-33 | `citation_auditor.__version__ == "0.2.0"` |

---

## 2. Dependency Graph (ENG-2.3)

```
S-01 ──────────────────────────┐
      ↘ (parallel)              ↓
       S-02 (parallel)        S-03 (depends on S-01 only — C-P5-014)
             ↘                   ↓
              └───────────────→ S-04 (needs S-01+S-02+S-03)
                                  ↓
                                 S-05 (needs S-01+S-02+S-03)
                                  ↓
                                 S-06
```

**Critical path:** S-01 → S-03 → S-04 → S-05 → S-06 (S-02 runs in parallel; must complete before S-04)  
**Parallel build:** S-01, S-02, S-03 may all build concurrently after S-01 completes — S-02 has no dependency on S-03 and vice versa (C-P5-014).  
**Merge sequencing:** S-03 merges AFTER S-01; S-02 merges independently at any time.  
**S-04 prerequisite:** Needs S-01 (HTML scan) + S-02 (widened auditor for T-29 WARN) + S-03 (cli accepts .html).
---

## 3. Test Pyramid Strategy (ENG-4.1 NON-NEGOTIABLE)

| Layer | File | New Tests | Scope |
|-------|------|-----------|-------|
| Unit — scanner | `tests/unit/test_scanner.py` | T-01–T-08, T-34, T-36 (10) | `_HTMLStripper`, `_strip_html()`, HTML extension routing, .md bypass guard, benign-malformed HTML |
| Unit — auditor | `tests/unit/test_auditor.py` | T-09–T-21, T-30, T-31, T-35 (16) | `_extract_title_candidates()`, widened `_check_title_mismatch()`, 9-pattern table, regression, empty-title guard |
| Unit — cli | `tests/unit/test_cli.py` | T-22–T-25, T-32–T-33 (6) | Surface 1 extension guard, version string |
| BDD | `tests/bdd/test_bdd_html.py` | T-26–T-29 (4) | CliRunner HTML scanning scenarios (no Gherkin — C-P5-006) |

**Total new tests: 36** (C-P5-007/C-P5-010; updated from Phase 4 §5 base of 33)  
**Coverage target:** ≥95% branch coverage on modified modules (ENG-4.6 — C-P5-012)  
**Mutation testing:** mutmut ≥85% critical-path kill rate on `scanner.py` + `auditor.py` (ENG-4.11 — C-P5-012)

**ENG-4.1 atomic TDD constraint:** Each test written RED before implementation. Tests in each slice must fail on v0.1.0 code and pass on completed slice.

---

## 4. Acceptance Criteria (Phase 4 §0 Success Criteria)

| Criterion | Verification |
|-----------|-------------|
| `.html` and `.htm` files scanned without `--html` flag | S-03 T-22/T-23 |
| `<script>`/`<style>` content excluded | S-01 T-02/T-03, S-04 T-27 |
| Unclosed `<script>`/`<style>` → exit 2 | S-01 T-04, S-04 T-28 |
| Table-cell pattern `\| ENG-X.Y \| Wrong Title \|` → WARN | S-02 T-09 |
| Em-dash pattern `ENG-X.Y — Wrong Title` → WARN | S-02 T-10 |
| Before-ID parens `Wrong Title (ENG-X.Y)` → WARN | S-02 T-11 |
| Colon prose `ENG-X.Y: This requirement...` → PASS (no false WARN) | S-02 T-17 |
| Pure prose `ENG-4.3 WireMock contracts` → PASS (known limitation) | S-05 T-31 |
| Correct title in table `\| ENG-6.4 \| Data Protection \|` → PASS | S-02 T-13 |
| Version string updated to 0.2.0 | S-06 T-32/T-33 |
| ≥95% branch coverage on scanner.py + auditor.py | C7-003 |
| RUNBOOK L2 troubleshooting section present | C7-002 |

---

## 5. Phase 7 Review Conditions (from Judicial Synthesis)

Per judicial synthesis verdict (claude-opus-4.5 2026-05-25), Phase 8 Release is blocked unless:

| ID | Condition |
|----|-----------|
| C7-001 | `tests/fixtures/` contains pinned synthetic corpus (regression fixtures) |
| C7-002 | `RUNBOOK.md` updated with L2 dual-anchor false-WARN triage section |
| C7-003 | 36 new tests passing under `pytest --strict`; coverage ≥95%/≥85% on modified modules |

---

## 6. Deliverables Summary

| Slice | Primary Deliverable | Story Points |
|-------|--------------------|----|
| S-01 | `scanner.py` HTML stripping + 5 fixtures | 3 |
| S-02 | `auditor.py` widened L2 detection | 6 |
| S-03 | `cli.py` Surface 1 extension guard | 1 |
| S-04 | `test_bdd_html.py` (CliRunner) + 3 fixtures | 3 |
| S-05 | RUNBOOK.md + 3 regression/edge fixtures | 1 |
| S-06 | Version bump | 1 |
| **Total** | | **15 SP** |

Phase 6 produces: 36 new tests, 5 modified source files, 11 new fixture files, updated RUNBOOK.
