"""scanner.py — Pass 1/2 code-block stripping + citation extraction.

ADR-003: Fenced blocks stripped first (re.DOTALL), then inline code, then regex scan.
T-09 guards: 10 MB size limit, UTF-8 decode with errors='replace', 1000-match cap.
"""
from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

from citation_auditor.exceptions import AuditError
from citation_auditor.registry import RegistryEntry

_MAX_BYTES = 10 * 1024 * 1024  # T-09: 10 MB limit
_MAX_MATCHES = 1000  # T-09: cap total unique citations

# Law ID pattern — word-boundary anchored
_LAW_ID_RE = re.compile(r"\b(ENG|PRD|BUS)-\d+\.\d+\b")

# Fenced code blocks: backtick or tilde fences (ADR-003, re.DOTALL)
_FENCE_RE = re.compile(r"(?:```|~~~).*?(?:```|~~~)", re.DOTALL)

# Inline code: single backtick spans (non-greedy, no newlines)
_INLINE_CODE_RE = re.compile(r"`[^`\n]+`")

_CONTEXT_WINDOW = 150  # ±150 chars around match


class _HTMLStripper(HTMLParser):
    """Strip HTML tags, exclude <script>/<style> content. ENG-6.5: stdlib only."""

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


def _strip_html(text: str) -> str:
    """Strip HTML tags; raise AuditError on unclosed script/style (T-14)."""
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


def scan_artifact(
    artifact_path: Path,
    registry: dict[str, RegistryEntry],
    allow_draft: list[str],
) -> tuple[list[tuple[str, str]], list[str]]:
    """Scan *artifact_path* for law citation IDs.

    Returns:
        citations: list of (law_id, context_snippet) — deduplicated, first-occurrence wins.
        draft_skipped: law IDs found that are in *allow_draft* (skipped from citations).
    """
    # T-09: size guard (pre-read)
    try:
        size = artifact_path.stat().st_size
    except OSError as exc:
        raise AuditError(f"Cannot stat artifact: {artifact_path}: {exc}") from exc

    if size > _MAX_BYTES:
        raise AuditError(
            f"Artifact exceeds 10 MB size limit ({size} bytes): {artifact_path}"
        )

    # T-09: encoding guard
    try:
        raw = artifact_path.read_bytes()
    except OSError as exc:
        raise AuditError(f"Cannot read artifact: {artifact_path}: {exc}") from exc

    text = raw.decode("utf-8", errors="replace")

    # HTML stripping: apply before fenced-code stripping (Pass 1/2)
    suffix = artifact_path.suffix.lower()
    if suffix in {".html", ".htm"}:
        text = _strip_html(text)

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub("", text)

    # Pass 2: strip inline code
    stripped = _INLINE_CODE_RE.sub("", stripped)

    # Build allow_draft set for O(1) lookup
    allow_draft_set = set(allow_draft)

    citations: list[tuple[str, str]] = []
    draft_skipped: list[str] = []
    seen: set[str] = set()

    for match in _LAW_ID_RE.finditer(stripped):
        law_id = match.group(0)

        if law_id in seen:
            continue  # dedup: first-occurrence wins

        seen.add(law_id)

        # Draft filtering: if ID is in allow_draft list, skip to draft_skipped
        if law_id in allow_draft_set:
            draft_skipped.append(law_id)
            continue

        # Build context snippet ±150 chars
        start = max(0, match.start() - _CONTEXT_WINDOW)
        end = min(len(stripped), match.end() + _CONTEXT_WINDOW)
        snippet = stripped[start:end]

        citations.append((law_id, snippet))

        # T-09: cap at 1000 unique citations
        if len(citations) >= _MAX_MATCHES:
            break

    return citations, draft_skipped
