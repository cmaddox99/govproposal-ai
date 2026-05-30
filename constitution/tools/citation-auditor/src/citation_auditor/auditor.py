"""auditor.py — L1 verdict logic. Pure function, no I/O.

Verdict rules (Phase 3 §2.2):
  FAIL  — law_id not in registry
  WARN  (TITLE_MISMATCH) — explicit title phrase within windows, partial_ratio < 60
  WARN  (STATUS_MISMATCH) — NON-NEGOTIABLE/STRICTLY ENFORCED claim within 50 chars
                             contradicts registry non_negotiable flag
  PASS  — in registry, no mismatch detected

Results sorted: FAIL → WARN → PASS, then alphabetical within tier.
"""
from __future__ import annotations

import re

from rapidfuzz import fuzz

from citation_auditor.exceptions import AuditError
from citation_auditor.models import AuditResult, CitationResult, Verdict
from citation_auditor.registry import RegistryEntry

# Patterns for extracting explicit title phrases near a law ID
# Captures **bold**, "quoted", or (parenthesised) text
_TITLE_PHRASE_RE = re.compile(
    r"""(?:\*\*([^*]+)\*\*|"([^"]+)"|'([^']+)'|\(([^)]+)\))"""
)

# Status keywords that appear in parentheses near law IDs
_STATUS_NON_NEG = re.compile(r"\bNON[- ]NEGOTIABLE\b", re.IGNORECASE)
_STATUS_STRICT = re.compile(r"\bSTRICTLY\s+ENFORCED\b", re.IGNORECASE)

# Tier order for sorting
_TIER_ORDER = {Verdict.FAIL: 0, Verdict.WARN: 1, Verdict.PASS: 2}

# Title-phrase match threshold (Phase 3 §4.2)
_TITLE_SCORE_THRESHOLD = 60

# Context window for status/title checks (chars on each side of the match)
_STATUS_WINDOW = 50
_TITLE_WINDOW = 120          # was 30 — widened per Phase 4 §3.2
_TITLE_BEFORE_WINDOW = 80    # backward scan window


def audit(
    citations: list[tuple[str, str]],
    registry: dict[str, RegistryEntry],
    artifact_path: str,
    registry_path: str,
    law_count: int,
    draft_skipped: list[str],
    allow_draft: list[str],
    strict: bool,
    timestamp: str,
    tool_version: str,
) -> AuditResult:
    """Apply L1 verdict logic to *citations*. Pure function — no I/O.

    Args:
        citations: list of (law_id, context_snippet) from scanner.scan_artifact()
        registry: loaded registry from registry.load_registry()
        artifact_path, registry_path, law_count: pass-through metadata
        draft_skipped: IDs routed to draft_skipped by scanner
        allow_draft, strict, timestamp, tool_version: pass-through metadata

    Returns:
        AuditResult with sorted CitationResult list and all metadata fields.

    Raises:
        AuditError: on unexpected internal failure (caught by cli.py → exit 2).
    """
    try:
        results: list[CitationResult] = []

        for law_id, snippet in citations:
            entry = registry.get(law_id)

            if entry is None:
                results.append(CitationResult(
                    law_id=law_id,
                    verdict=Verdict.FAIL,
                    note=f"ID not in registry: {law_id}",
                    context_snippet=snippet,
                ))
                continue

            # Check STATUS_MISMATCH within ±50 chars of the law ID in snippet
            status_note = _check_status_mismatch(law_id, snippet, entry)
            if status_note:
                results.append(CitationResult(
                    law_id=law_id,
                    verdict=Verdict.WARN,
                    note=status_note,
                    context_snippet=snippet,
                ))
                continue

            # Check TITLE_MISMATCH — only when registry has a title
            if entry.title:
                title_note = _check_title_mismatch(law_id, snippet, entry.title)
                if title_note:
                    results.append(CitationResult(
                        law_id=law_id,
                        verdict=Verdict.WARN,
                        note=title_note,
                        context_snippet=snippet,
                    ))
                    continue

            results.append(CitationResult(
                law_id=law_id,
                verdict=Verdict.PASS,
                note=None,
                context_snippet=None,
            ))

        # Sort: FAIL → WARN → PASS, then alpha within tier
        results.sort(key=lambda r: (_TIER_ORDER[r.verdict], r.law_id))

        return AuditResult(
            artifact_path=artifact_path,
            registry_path=registry_path,
            law_count=law_count,
            scanned=len(citations),
            results=results,
            draft_skipped=draft_skipped,
            allow_draft=allow_draft,
            strict=strict,
            timestamp=timestamp,
            tool_version=tool_version,
        )
    except (KeyError, TypeError, AttributeError) as exc:
        raise AuditError(f"Internal auditor failure: {exc}") from exc


def _find_id_pos_in_snippet(law_id: str, snippet: str) -> int | None:
    """Return start position of law_id in snippet, or None."""
    idx = snippet.find(law_id)
    return idx if idx >= 0 else None


def _check_status_mismatch(
    law_id: str, snippet: str, entry: RegistryEntry
) -> str | None:
    """Return a WARN note if status assertion within ±50 chars contradicts registry."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    # Window: 50 chars after the end of the law_id match
    id_end = pos + len(law_id)
    window = snippet[id_end: id_end + _STATUS_WINDOW]

    asserts_non_neg = bool(_STATUS_NON_NEG.search(window))
    asserts_strictly = bool(_STATUS_STRICT.search(window))

    if not asserts_non_neg and not asserts_strictly:
        return None  # no assertion found

    is_non_neg = entry.non_negotiable

    if asserts_non_neg and not is_non_neg:
        return f"Status mismatch: artifact asserts NON-NEGOTIABLE but registry marks {law_id} as non_negotiable=false"

    if asserts_strictly and is_non_neg:
        return f"Status mismatch: artifact asserts STRICTLY ENFORCED but registry marks {law_id} as NON-NEGOTIABLE"

    return None  # assertion matches registry → PASS


def _extract_title_candidates(window: str, *, plain_text_allowed: bool) -> list[str]:
    """Return candidate title phrases from window.

    Source 1 (always): formatted phrases via _TITLE_PHRASE_RE.
    Source 2 (dual-anchor only): plain-text — only when window BOTH starts AND ends
      with a structural separator character (prevents colon-prose false WARNs).
    """
    candidates: list[str] = []
    # Source 1: formatted phrases
    for m in _TITLE_PHRASE_RE.finditer(window):
        phrase = next(g for g in m.groups() if g is not None).strip()
        if phrase:
            candidates.append(phrase)
    # Source 2: plain-text (dual-anchor guard; only when Source 1 found nothing)
    if plain_text_allowed and not candidates:
        leading = bool(re.match(r'^[\s|—–\-:()\[\]]', window))
        trailing = bool(re.search(r'[|—–\-:()\[\]]\s*$', window))
        if leading and trailing:
            plain = re.match(r'^[^A-Za-z]*([A-Za-z]\w*(?:\s+[A-Za-z]\w*){0,5})', window)
            if plain:
                candidates.append(plain.group(1).strip())
    return candidates


def _check_title_mismatch(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if a title phrase within windows scores < 60 vs registry title."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    if not registry_title:
        return None  # T-35: empty registry title — no check

    id_end = pos + len(law_id)

    # After-window: 120 chars (widened from 30)
    window_after = snippet[id_end: id_end + _TITLE_WINDOW]

    # Truncate after-window at the next law ID to avoid cross-citation noise
    _next_id = re.search(r'\b(?:ENG|PRD|BUS)-\d+\.\d+\b', window_after)
    if _next_id:
        window_after = window_after[:_next_id.start()]

    # Before-window: 80 chars — only use if window ends with structural separator
    id_start = pos
    window_before_raw = snippet[max(0, id_start - _TITLE_BEFORE_WINDOW): id_start]
    before_anchor = bool(re.search(r'[|—–\-:()\[\]]\s*$', window_before_raw))

    # Collect candidates from after-window (dual-anchor for plain-text)
    candidates = _extract_title_candidates(window_after, plain_text_allowed=True)

    # Collect candidates from before-window
    if before_anchor:
        all_before = _TITLE_PHRASE_RE.findall(window_before_raw)
        if all_before:
            # Use last (closest to ID) non-empty formatted phrase
            for groups in reversed(all_before):
                phrase = next((g for g in groups if g), None)
                if phrase:
                    candidates.append(phrase.strip())
                    break
        else:
            # Plain-text extraction: word sequence ending before trailing separator
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
