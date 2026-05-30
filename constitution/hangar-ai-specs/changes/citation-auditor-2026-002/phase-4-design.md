---
phase: 4
title: "Design — Citation Auditor v0.2.0: HTML Support + L2 Context Detection"
project: citation-auditor-2026-002
workflow: greenfield-development
version: v1.2.0
status: APPROVED — Judicial Synthesis claude-opus-4.5 2026-05-25
judicial_synthesis:
  synthesizer: claude-opus-4.5
  verdict: APPROVED
  citations_verified: 18/18
  hallucinated_ids: 0
  j6_invoked: true
  j6_activation: "≥5 distinct law IDs in frontmatter — 14 IDs"
  unmitigated_high_threats: 0
  contested_p0_p1_resolved: "15/15 across 2 rounds (28 total findings)"
  phase_7_conditions: [C7-001 pinned regression fixtures, C7-002 RUNBOOK L2 section, C7-003 33 tests green ≥95%/≥85%]
  gate: UNLOCKED
author: Hangar AI (claude-sonnet-4.6)
date: 2026-05-25
law_citations: [PRD-2.6, ENG-3.4, ENG-4.3, ENG-4.9, ENG-4.11, ENG-6.1, ENG-6.4, ENG-6.5, ENG-11.1, ENG-11.2, ENG-12.1, ENG-14.1, ENG-14.2, BUS-7.1]
preceding_change: citation-auditor-2026-001 (v0.1.0 ACTIVE — Phase 8 Ship 2026-05-25)
tool_version_target: v0.2.0
r1_corrections:
  - C-P4-001-J2: _SEPARATOR_RE widened — add "(", ")", "[", "]" to character class
  - C-P4-002-J2: CamelCase fix — [A-Za-z][a-z]* → [A-Za-z]\w* in both plain_match and before_match patterns
  - C-P4-003-J2: Before-window extraction — re.findall()[-1] replaces re.search(...$) to return phrase closest to ID
  - C-P4-004-J2J5: Structural separator guard added — plain-text extraction only when window is separator-anchored; Pattern 5 plain prose updated to PASS (known limitation → J6)
  - C-P4-005-J3: T-10 revised — _strip_html() wrapped in except Exception→AuditError
  - C-P4-006-J3: T-14 added — unclosed script/style at EOF raises AuditError
  - C-P4-007-J4: BDD scenarios added for L2 WARN/PASS patterns
  - C-P4-008-J4: --strict + HTML test added to §5
  - C-P4-009-J4: --output append + HTML test added to §5
  - C-P4-010-J4: STATUS_MISMATCH regression test added to §5
  - C-P4-011-J4: Synthetic pinned fixtures specified (not real disc-2026-004 files)
  - C-P4-012-J4: Test count enumerated to ≥30; coverage tooling (coverage.py, mutmut) added to §5
  - C-P4-013-J4: HTML entity near law ID test added to §5
  - C-P4-014-J6: ENG-1.5 removed from law_citations (not cited in body)
  - C-P4-015-J6: ENG-10.1 removed from law_citations (not cited in body)
  - C-P4-016-J1: Explicit success criteria table added to §0
  - C-P4-017-J1: ENG-14.1/ENG-14.2 WARN-only boundary explicitly stated in §2 ADR-CA2-002
  - C-P4-018-J3: <template> policy documented in §3.1
  - C-P4-019-J5: Empty post-strip HTML behavior documented in §3.1 + test added
  - C-P4-020-J5: BUS-2.1/BUS-2.3 fixture added to regression tests
  - C-P4-021-J2: HTMLParser __init__ explicitly specified in §3.1
  - C-P4-025-J3: "visible text only" → "all text nodes" policy in §3.1/<template> section
  - C-P4-026-J4: pytest-bdd runner stated in §5 (already in project, no new dependency)
  - C-P4-027-J4: test_mismatch_phrase_exactly_4_chars_accepted added to §5 (at-threshold boundary)
  - C-P4-028-J2: Dual-anchor guard in _extract_title_candidates — require BOTH leading AND trailing separator in after-window for Source 2 plain-text extraction; eliminates "ENG-6.4: prose" colon false WARN
---

# Phase 4 — Design: Citation Auditor v0.2.0

**Jury focus (greenfield-development.md §Per-Phase Jury Focus):**
"Architecture tradeoffs; threat model completeness; unmitigated risks"

**Constitutional gate:** No unmitigated HIGH threats.

---

## 0. Problem / Solution / Success Criteria (ENG-11.2)

### Problem

Two gaps in `aa-citation-audit` v0.1.0 were confirmed by Jason's post-delivery citation error report (disc-2026-004):

**Gap 1 — HTML not natively supported (ENG-14.1 enforcement gap):**
`cli.py` Surface 1 enforces `.md`-only (line 246: `if artifact_path.suffix.lower() != ".md"`). Workflow phases generate **both** `.md` and `.html` artifacts. Which one the coding agent runs through the pre-jury gate is operationally undefined. Agents may skip the `.md` file if only the `.html` is present (e.g., `em-package/` delivery artifacts). The RUNBOOK workaround (temp-file trick) requires human awareness and is error-prone.

**Gap 2 — L2 contextual misapplication not detected:**
v0.1.0 `_check_title_mismatch` in `auditor.py`:
- Looks only **30 chars AFTER** the law ID
- Matches only **formatted phrases** (`**bold**`, `"quoted"`, `(parens)`)
- Misses plain-text descriptions in markdown table cells (`| ENG-6.4 | No God Classes |`), inline separators (`ENG-6.4 — No God Classes`), and the "description-before-ID" pattern (`God classes decomposed (ENG-6.4)`)

**Confirmed false-PASS incidents (disc-2026-004):**
| Citation | Contextual claim in artifact | Actual law title | Correct law |
|----------|------------------------------|------------------|-------------|
| ENG-6.4 | "No God Classes", "SRP", "≤300 Lines" | Data Protection Law | ENG-3.4 (Single Responsibility Principle) |
| ENG-4.3 | "WireMock consumer-provider contracts" | Test Quality Law (FIRST) | ENG-4.9 (Contract Testing Law) |

Both appeared as **PASS** under v0.1.0. The jury for disc-2026-004 Stage D caught ENG-4.3 verbally but did not correct the artifact citations. ENG-6.4 was not flagged by jury at all.

### Solution

`aa-citation-audit` v0.2.0 adds:

1. **Native HTML scanning** — stdlib `html.parser` (no new deps); auto-detects `.html`/`.htm` extension; strips `<script>`/`<style>` content, all HTML tags, decodes entities; then applies existing markdown pass unchanged.

2. **Widened L2 title-context detection** — three changes to `_check_title_mismatch` in `auditor.py`:
   - **Window after**: 30 → 120 chars
   - **Window before**: new 80-char backward window (catches description-before-ID pattern)
   - **Plain-text extraction**: alongside existing `_TITLE_PHRASE_RE` (bold/quote/parens), add separator stripping (`|`, `—`, `–`, `-`, `:`) then extract first 1–6 word sequence adjacent to the ID

### Success Criteria (ENG-11.2)

| Criterion | Measure | Target |
|-----------|---------|--------|
| HTML parity | `.html` scanned identically to extracted-then-scanned `.md` equivalent | 100% across fixture suite |
| L2 catch rate — separator-anchored patterns | ENG-6.4 table-cell + dash-separator + parens-before-ID patterns detected as WARN | 100% (3 confirmed patterns) |
| L2 plain-prose limitation (known) | `ENG-4.3 WireMock consumer contracts` (no separator) → PASS; J6 handles | Documented, tested |
| False positive rate (plain-text extraction) | WARNs on correctly-cited laws with structural separators | 0 in fixture suite |
| Regression: 218 existing tests | All v0.1.0 tests pass unmodified | 100% |
| Regression: corpus PASS/FAIL delta | v0.2.0 re-run on constitution artifacts — no existing PASS flips to WARN | 0 new false WARNs |
| Test coverage (ENG-4.11, coverage.py) | Statement coverage | ≥95% |
| Mutation score (ENG-4.11, mutmut) | killed/(killed+survived) | ≥85% |
| Exit code compatibility | All existing exit code contracts unchanged for .md, .html, .htm | 100% |

---

## 1. Scope

### In scope
- `tools/citation-auditor/src/citation_auditor/scanner.py` — HTML stripping pass
- `tools/citation-auditor/src/citation_auditor/cli.py` — Surface 1 extension check
- `tools/citation-auditor/src/citation_auditor/auditor.py` — widened L2 title check
- `tools/citation-auditor/RUNBOOK.md` — update: remove HTML workaround, add HTML native section
- `tools/citation-auditor/tests/` — new unit + BDD + integration tests for both gaps
- `.github/workflows/citation-audit.yml` — no change needed (passes artifact path; extension now accepted)

### Out of scope
- LLM-based semantic citation verification (prohibitively expensive for CI gate; J6 juror persona ENG-14.2 remains the semantic layer)
- Cross-law subject-matter disambiguation (e.g., detecting that ENG-6.4 context text would better match ENG-3.4 — requires all-law similarity ranking; deferred)
- `aviation_non_negotiable` registry gap (8 false WARNs on BUS-2.1/2.3) — separate patch
- Changes to audit log schema (BUS-7.1)
- Changes to exit codes

---

## 2. Architecture Decisions

### ADR-CA2-001: HTML stripping — stdlib `html.parser` over regex or third-party

**Options considered:**
| Option | Pros | Cons |
|--------|------|------|
| `html.parser` (stdlib) | No new dep; handles malformed HTML gracefully; battle-tested | No CSS selector support (not needed) |
| `regex`-based tag stripping | Zero-overhead | ReDoS risk on pathological input; misses nested comments, CDATA |
| `BeautifulSoup` / `lxml` | Most capable | New dependency; violates lean-dep posture established in v0.1.0 |

**Decision:** `html.parser`. Subclass `HTMLParser`, accumulate non-tag text in a buffer, skip `<script>` and `<style>` content entirely. Apply `html.unescape()` for entity decoding. No new dependencies (ENG-6.5 lean dependency principle preserved).

**Placement in scanner.py:** New `_strip_html(text: str) -> str` function. Called before `_FENCE_RE` pass when extension is `.html`/`.htm`.

### ADR-CA2-002: L2 detection approach — keyword extraction over LLM/embedding

**Options considered:**
| Option | Accuracy | Cost | CI-compatible |
|--------|----------|------|---------------|
| LLM call per citation | ~95% | ~$0.01/call | No (latency + cost) |
| Vector embedding similarity | ~85% | Requires model | No (infra) |
| Rule-based keyword extraction (chosen) | ~70% on confirmed patterns; 100% on explicit title phrases | ~0ms | Yes |

**Decision:** Rule-based. Extend existing `fuzz.partial_ratio` check. Widen windows, add plain-text extraction. LLM-quality L2 detection remains J6's responsibility (ENG-14.2). This closes the gap for **explicit separator-anchored title phrases** (the confirmed incident pattern) without pretending to solve general semantic misapplication.

**ENG-14.1 / ENG-14.2 boundary (C-P4-017):** L2 title-mismatch findings emit **WARN only** — never FAIL. This preserves ENG-14.2 J6 authority for semantic adjudication. The tool flags potential misapplication; the human jury (with J6) makes the final determination. The tool does not FAIL/REJECT on contextual mismatch.

**Why this is sufficient:** Both confirmed incidents had explicit plain-text descriptions adjacent to the misapplied ID in table-cell format (`| ENG-6.4 | No God Classes |`) or dash-separated format (`ENG-6.4 — No God Classes`). These are **separator-anchored patterns** that this design catches. Pure contextual prose reference (`"ENG-4.3 WireMock consumer contracts"` with only a space separator) remains correctly routed to J6 — this is a known, documented limitation.

### ADR-CA2-003: Window sizes — 120 chars after, 80 chars before

**Rationale:**
- 30-char after (v0.1.0): too narrow for table cells — `| ENG-6.4 |` is 10 chars, leaving only 20 for content
- 120-char after: covers `| No God Classes | 7 services fail |` and `— Single Responsibility Principle (must decompose)` reliably
- 80-char before: covers `God classes decomposed (` and `SRP violation — no class may exceed 300 lines (` patterns observed in disc-2026-004
- Bounded by the existing ±150 char context snippet from scanner — no scanner changes needed (snippet is already large enough)

**Risk:** Wider windows increase false-positive surface. Mitigated by:
1. Plain-text extraction still requires a **structured separator** or **adjacent position** relative to the ID — random prose does not trigger the rule
2. `fuzz.partial_ratio` threshold of 60 unchanged — casual word overlap does not score above threshold

---

## 3. Detailed Design

### 3.1 scanner.py changes

**`_strip_html(text: str) -> str`** — `html.parser.HTMLParser` subclass (C-P4-021 adds explicit `__init__`):

```python
from html.parser import HTMLParser
import html as html_module

class _HTMLStripper(HTMLParser):
    _SKIP_TAGS = {"script", "style"}

    def __init__(self):
        super().__init__()
        self._buf: list[str] = []
        self._skip: bool = False

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() in self._SKIP_TAGS:
            self._skip = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in self._SKIP_TAGS:
            self._skip = False

    def handle_data(self, data: str) -> None:
        if not self._skip:
            self._buf.append(data)

    def get_text(self) -> str:
        return html_module.unescape(" ".join(self._buf))


def _strip_html(text: str) -> str:
    """Strip HTML tags; skip <script>/<style> content; decode entities.

    Raises AuditError on any parser failure (C-P4-005).
    Raises AuditError if EOF reached while inside a skipped block (C-P4-006 / T-14).
    """
    try:
        stripper = _HTMLStripper()
        stripper.feed(text)
        stripper.close()
        if stripper._skip:
            raise AuditError(
                "Unclosed <script> or <style> tag in HTML artifact — "
                "subsequent content may have been suppressed (T-14)"
            )
        return stripper.get_text()
    except AuditError:
        raise
    except Exception as exc:
        raise AuditError(f"HTML stripping failed: {exc}") from exc
```

**`<template>` and text-node policy (C-P4-025):** The tool scans **all text nodes** emitted by `handle_data()` — not just visible/rendered content. `<template>` is not in `_SKIP_TAGS`; Python's stdlib `HTMLParser` emits template body content, so it IS scanned. This is the correct behavior: a law citation in a `<template>` is still a citation in the artifact. HTML comments, attribute values, and CSS-generated pseudo-content are excluded (not emitted by `handle_data()`) and do not satisfy citation requirements.

**Empty post-strip HTML (C-P4-019):** If all HTML content is inside `<script>` or `<style>` blocks, the stripped text will be empty or whitespace only. `_LAW_ID_RE` will find zero matches → 0 citations → PASS (exit 0). This is correct: a document with no visible text has no citations to audit.

**`scan_artifact()` changes:**
- After size + encoding guards, detect extension: `if artifact_path.suffix.lower() in {".html", ".htm"}:` → call `_strip_html(text)` → reassign `text`
- Existing `_FENCE_RE` and `_INLINE_CODE_RE` passes then apply unchanged to the stripped text

### 3.2 cli.py changes

Surface 1 (line 246):
```python
# Before (v0.1.0)
if artifact_path.suffix.lower() != ".md":
    _exit2(f"Artifact must have .md extension: {artifact}")

# After (v0.2.0)
_SUPPORTED_EXTENSIONS = {".md", ".html", ".htm"}
if artifact_path.suffix.lower() not in _SUPPORTED_EXTENSIONS:
    _exit2(f"Artifact must have .md, .html, or .htm extension: {artifact}")
```

No other cli.py changes. Exit codes, output modes, audit log, atomic write all unchanged.

### 3.3 auditor.py changes

Constants (C-P4-001, C-P4-002):
```python
_TITLE_WINDOW = 120          # was 30 — chars after ID for title phrase search
_TITLE_BEFORE_WINDOW = 80    # NEW — chars before ID for description-before-ID pattern

# C-P4-001: Added ()[] to separator set
_SEPARATOR_RE = re.compile(r'[\s|—–\-:()\[\]]+')
```

**`_extract_title_candidates(window: str) -> list[str]`** — new helper (C-P4-002, C-P4-004):

```python
def _extract_title_candidates(window: str) -> list[str]:
    """Extract title-phrase candidates from a context window.

    Source 1 (always): Formatted phrases — **bold**, "quoted", (parens).
    Source 2 (dual-anchor only): Plain-text — only extracted when the window
    BOTH starts AND ends with a structural separator (|—–-:()[]).
    This ensures we're in a labelled zone (table cell: "| title |"),
    not arbitrary prose or colon-prefixed sentences (C-P4-028).
    """
    candidates: list[str] = []

    # Source 1: formatted phrases (existing logic)
    for match in _TITLE_PHRASE_RE.finditer(window):
        phrase = next(g for g in match.groups() if g is not None).strip()
        if phrase:
            candidates.append(phrase)

    # Source 2: plain-text — dual-anchor guard (C-P4-028)
    # Requires BOTH leading AND trailing structural separator
    if (re.match(r'^\s*[|—–\-:()\[\]]', window) and
            re.search(r'[|—–\-:()\[\]]', window[1:])):  # at least one more separator
        stripped = _SEPARATOR_RE.sub(" ", window).strip()
        # C-P4-002: [A-Za-z]\w* allows CamelCase words like "WireMock"
        plain_match = re.match(r'^([A-Za-z]\w*(?:\s+[A-Za-z]\w*){1,5})', stripped)
        if plain_match:
            phrase = plain_match.group(1).strip()
            if len(phrase) >= 4:
                candidates.append(phrase)

    return candidates
```

**`_check_title_mismatch()` updated** (C-P4-003 — findall[-1] for before window):

```python
def _check_title_mismatch(law_id: str, snippet: str, registry_title: str) -> str | None:
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)

    # After-window (widened to 120 chars)
    window_after = snippet[id_end: id_end + _TITLE_WINDOW]

    # Before-window (NEW — 80 chars before ID)
    window_before_raw = snippet[max(0, pos - _TITLE_BEFORE_WINDOW): pos]

    candidates: list[str] = []

    # After-window candidates (formatted + separator-anchored plain-text)
    candidates.extend(_extract_title_candidates(window_after))

    # Before-window plain-text: only when window ends with a structural separator
    # (e.g., "God classes decomposed (" → "(" is a separator before the "(ENG-6.4)")
    # C-P4-003: use findall[-1] to get phrase closest to ID, not leftmost
    if re.search(r'[|—–\-:()\[\]]\s*$', window_before_raw):
        before_stripped = _SEPARATOR_RE.sub(" ", window_before_raw).strip()
        all_before = re.findall(r'([A-Za-z]\w*(?:\s+[A-Za-z]\w*){1,5})', before_stripped)
        if all_before:
            phrase = all_before[-1].strip()
            if len(phrase) >= 4:
                candidates.append(phrase)

    for phrase in candidates:
        if not phrase:
            continue
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue
        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact context '{phrase[:60]}', registry title is '{registry_title}'"
            )

    return None
```

### 3.4 Simulation — confirmed incident patterns

| Pattern | Window used | Extracted phrase | Registry title | Score | Verdict |
|---------|------------|-----------------|----------------|-------|---------|
| `\| ENG-6.4 \| No God Classes \|` | After 120; starts with `\|` → separator-anchored | "No God Classes" | "Data Protection Law" | ~0 | **WARN** ✅ |
| `ENG-6.4 — No God Classes (≤300 Lines)` | After 120; starts with ` —` → separator-anchored | "No God Classes" | "Data Protection Law" | ~0 | **WARN** ✅ |
| `God classes decomposed (ENG-6.4)` | Before 80; ends with `(` → separator-anchored; findall[-1]="God classes decomposed" | "God classes decomposed" | "Data Protection Law" | ~0 | **WARN** ✅ |
| `ENG-4.3 WireMock consumer contracts` | After 120; starts with space only → NOT separator-anchored; formatted phrases: none | (no candidate) | N/A | N/A | **PASS** ⚠️ known limitation → J6 |
| `\| ENG-6.4 \| Data Protection \|` | After 120; separator-anchored | "Data Protection" | "Data Protection Law" | ~95 | **PASS** ✅ |
| `ENG-3.4 (Single Responsibility)` | After 120; `(Single Responsibility)` via _TITLE_PHRASE_RE | "Single Responsibility" | "Single Responsibility Principle" | ~96 | **PASS** ✅ |
| `see ENG-6.4` | After 120: no separator → plain-text skipped; before 80: "see" ends with space only → skipped | (no candidate) | N/A | N/A | **PASS** ✅ |
| `ENG-6.4: This requirement mandates...` | After 120: starts with `:` but no trailing separator → dual-anchor FAILS | (no candidate) | N/A | N/A | **PASS** ✅ (no false WARN, C-P4-028) |

**Known limitation (C-P4-004):** Plain prose descriptions with only a space separator between description and law ID (e.g., `"ENG-4.3 WireMock consumer contracts"`) are not caught by the plain-text extraction path. The formatted-phrase path (`**bold**`, `"quoted"`, `(parens)`) still applies for these cases if the author used formatting. Plain prose misapplication without any formatting is a J6 responsibility per ENG-14.2.

---

## 4. Threat Model Delta (ENG-6.1)

Threats T-01 through T-09 carried from v0.1.0 unchanged. New threats introduced by v0.2.0:

| ID | Threat | Severity | Mitigation |
|----|--------|----------|------------|
| T-10 | HTMLParser callback raises exception → scan fails ungracefully | HIGH | Entire `_strip_html()` call wrapped in `except Exception → AuditError`; does not silently skip (C-P4-005). Unit test with purposely malformed HTML. Note: `HTMLParser.feed()` is tolerant of malformed markup but callbacks can raise; the outer catch ensures consistent error handling. |
| T-11 | `<script>` tag contains law ID pattern → false citation | HIGH | `_skip = True` during script/style content (case-insensitive: `tag.lower()`). Unit test confirms script content with law IDs not returned. Inline event handlers (`onclick=`) are HTML attributes — not emitted via `handle_data()` → excluded by default. |
| T-12 | Plain-text extraction emits false-positive WARN on correctly-cited law in descriptive prose | MEDIUM | Structural separator guard: plain-text extraction only when window starts/ends with `[|—–-:()\[\]]` separator (C-P4-004). Random prose without structural separator skips plain-text path entirely. Acceptance tests for correctly-cited laws in prose. |
| T-13 | HTML attribute values containing law IDs (e.g., `data-law="ENG-6.4"`) → false citation | LOW | `handle_data()` only emits text nodes, not attribute values → excluded by design. Confirmed correct. |
| T-14 | Unclosed `<script>` or `<style>` tag at EOF → `_skip=True` → all subsequent law IDs in document suppressed (false negative / evasion) | HIGH | After `HTMLParser.feed()` + `.close()`, check `stripper._skip`; if `True` → raise `AuditError` (fail closed). This surfaces the malformed-HTML condition rather than silently producing a false-clean result. (C-P4-006) |

**Visible-text-only policy (C-P4-018, C-P4-003-J3):** HTML comments (`<!-- ... -->`), attribute values, and CSS-generated content are not emitted by `handle_data()` and are therefore excluded. Law citations in these locations do not count for audit purposes. If an artifact author places a law ID only in a comment, the audit correctly does not detect it — enforcement applies to visible content. This policy is explicit: **only visible text nodes are scanned.**

**No unmitigated HIGH threats.**

---

## 5. Test Plan (ENG-4.11)

**Coverage tooling (C-P4-024):** `coverage.py` for statement coverage (≥95%); `mutmut` for mutation score (≥85% killed/(killed+survived)). Both validated in Phase 6 build and Phase 7 review.

**BDD framework (C-P4-026):** `html_scanning.feature` runs under `pytest-bdd` — already in project from v0.1.0 Phase 6 build. No new dependency.

**Fixtures (C-P4-011):** All new tests use **pinned synthetic fixture files** in `tests/fixtures/` — not real disc-2026-004 artifacts. Fixtures are Phase 6 build deliverables specified here; Phase 7 Review verifies delivery.

### Unit tests — scanner.py (10 tests, `tests/unit/test_scanner_html.py`)
1. `test_strip_html_removes_tags` — plain text preserved, tags removed
2. `test_strip_html_removes_script_content` — `<script>` body not in output
3. `test_strip_html_removes_style_content` — `<style>` body not in output
4. `test_strip_html_decodes_entities` — `&amp;` → `&`, `&lt;` → `<`
5. `test_strip_html_malformed_survives` — malformed HTML does not silently skip (AuditError raised or clean text returned)
6. `test_scan_artifact_html_extension_accepted` — `.html` file scanned successfully (exit 0)
7. `test_scan_artifact_htm_extension_accepted` — `.htm` file scanned successfully
8. `test_strip_html_script_law_id_not_extracted` — law ID inside `<script>` not returned as citation (T-11)
9. `test_strip_html_unclosed_script_raises` — unclosed `<script>` at EOF raises AuditError (T-14, C-P4-006)
10. `test_strip_html_empty_result_is_zero_citations` — all-script HTML → 0 citations → PASS (C-P4-019)

### Unit tests — auditor.py (12 tests, `tests/unit/test_auditor_l2.py`)
11. `test_title_mismatch_table_cell_after` — `| ENG-6.4 | No God Classes |` → WARN
12. `test_title_mismatch_dash_separator_after` — `ENG-6.4 — No God Classes` → WARN
13. `test_title_mismatch_description_before_parens` — `God classes decomposed (ENG-6.4)` → WARN
14. `test_no_mismatch_correct_plain_text` — `| ENG-6.4 | Data Protection |` → PASS
15. `test_no_mismatch_prose_no_separator_after` — `ENG-4.3 WireMock consumer contracts` (no separator) → PASS (known limitation)
16. `test_no_mismatch_prose_no_separator_before` — `must review ENG-3.4` (no separator) → PASS (no false WARN)
17. `test_no_mismatch_single_word_after` — `ENG-6.4 see` (1 word only, below 2-word min) → PASS
18. `test_no_mismatch_short_phrase_below_min` — extracted phrase exactly 3 chars → PASS (below 4-char minimum)
19. `test_camelcase_extraction` — `| ENG-4.3 | WireMock contracts |` → WARN (CamelCase fix, C-P4-002)
20. `test_status_mismatch_still_detected` — existing STATUS_MISMATCH check unaffected by v0.2.0 changes (regression, C-P4-010)
21. `test_html_entity_near_law_id` — law ID adjacent to HTML entity text (`&amp;No God Classes`) → title extracted correctly after unescape (C-P4-013)
22. `test_bus_21_no_new_false_warn` — BUS-2.1 citation in typical constitution context → no new false WARNs from window widening (C-P4-020)
23. `test_mismatch_phrase_exactly_4_chars_accepted` — extracted phrase of exactly 4 chars meets minimum and is scored (C-P4-027)

### BDD scenarios (new feature file: `tests/bdd/html_scanning.feature`) — 6 scenarios (C-P4-007, C-P4-008)
```gherkin
Feature: HTML artifact scanning

  Scenario: HTML file accepted at Surface 1
    Given an HTML artifact with valid law citations
    When I run aa-citation-audit on the HTML file
    Then exit code is 0 and citations are reported

  Scenario: Script tag content excluded
    Given an HTML artifact with ENG-6.4 inside a <script> block only
    When I run aa-citation-audit on the HTML file
    Then ENG-6.4 is not reported as a citation

  Scenario: Unsupported extension rejected
    Given an artifact with .txt extension
    When I run aa-citation-audit
    Then exit code is 2 with "must have .md, .html, or .htm extension"

  Scenario: L2 table-cell mismatch detected in HTML
    Given an HTML artifact with a table cell "| ENG-6.4 | No God Classes |"
    When I run aa-citation-audit on the HTML file
    Then ENG-6.4 verdict is WARN with title phrase score < 60

  Scenario: L2 correct title passes in HTML
    Given an HTML artifact with a table cell "| ENG-6.4 | Data Protection |"
    When I run aa-citation-audit on the HTML file
    Then ENG-6.4 verdict is PASS

  Scenario: --strict flag exits 1 on WARN from HTML artifact (C-P4-008)
    Given an HTML artifact with a title-mismatch WARN
    When I run aa-citation-audit --strict on the HTML file
    Then exit code is 1
```

### Integration tests — 3 tests (C-P4-009)
23. `test_integration_html_table_mismatch` — synthetic fixture with `| ENG-6.4 | No God Classes |` → WARN
24. `test_integration_html_table_correct` — same fixture with `| ENG-3.4 | Single Responsibility |` → PASS
25. `test_integration_output_append_html` — `--output append` mode with `.html` artifact writes frontmatter block (C-P4-009)

### Regression tests
- All existing 218 unit/BDD/integration tests pass unmodified (exit 0)
- `test_regression_constitution_artifacts` — run v0.2.0 on 10 pinned constitution `.md` artifacts: expect 0 new false WARNs from window widening

**Total new tests: 26 unit (10+13+3 integration) + 6 BDD + 1 regression = 33 new tests.** Target ≥30 met.

---

## 6. Deliverables

| Deliverable | File | Notes |
|-------------|------|-------|
| HTML stripping | `scanner.py` `_strip_html()` | stdlib only; no new deps; T-14 EOF guard |
| Extension update | `cli.py` Surface 1 | `.html`/`.htm` accepted |
| L2 widened check | `auditor.py` `_check_title_mismatch()` + `_extract_title_candidates()` | 120/80 windows + separator-anchored plain-text |
| New tests | `tests/unit/test_scanner_html.py`, `tests/unit/test_auditor_l2.py`, `tests/bdd/html_scanning.feature` | 32 new tests |
| Pinned fixtures | `tests/fixtures/html/`, `tests/fixtures/l2/` | Synthetic; not real discovery artifacts |
| RUNBOOK update | `RUNBOOK.md` | Remove HTML workaround; add native HTML section; add deprecation note (C-P4-022) |
| Version bump | `__init__.py` | `0.1.0` → `0.2.0` |

**RUNBOOK deprecation note (C-P4-022):** The old "HTML workaround" (temp-file trick) documented in v0.1.0 RUNBOOK §HTML Scanning is superseded by v0.2.0 native support. The workaround section will be replaced with a "⚠️ Deprecated workaround (v0.1.0)" callout noting that `.html`/`.htm` files are now accepted directly.

---

## 7. Constitution Compliance

| Law | Compliance |
|-----|------------|
| ENG-14.1 | Strengthened: HTML artifacts now covered by L1 gate — enforcement gap closed |
| ENG-14.2 | J6 role unchanged. L2 title-mismatch emits **WARN only** — J6 retains authority for semantic adjudication. Plain-prose descriptions without structural separators (known limitation) remain J6's domain. (C-P4-017) |
| ENG-4.11 | ≥95% statement coverage (coverage.py) + ≥85% mutation score (mutmut) targets maintained; validated Phase 6+7 |
| ENG-6.1 | Threat model delta in §4: T-10 through T-14; no unmitigated HIGH threats |
| ENG-6.5 | No new runtime dependencies — stdlib `html.parser` only |
| ENG-11.1 | This design is the spec that Phase 6 Build will implement |
| ENG-11.2 | §0 includes problem/solution/success criteria (C-P4-016) |
| ENG-12.1 | CI pipeline unchanged; no `--allow-draft` needed; `.github/workflows/citation-audit.yml` unmodified |
| ENG-14.1 | This document is the pre-jury artifact; `aa-citation-audit` run on it: 14 citations, 0 FAIL, 0 WARN |
| PRD-2.6 | This document is the Phase 4 jury gate artifact |
| BUS-7.1 | Reviewed for compliance — audit log schema unchanged, no impact. (Citation is a compliance-scope confirmation, not a governing change.) (C-P4-023) |
