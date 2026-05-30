"""scanner.py — Pass 1/2 code-block stripping + citation extraction.

ADR-003: Fenced blocks stripped first (re.DOTALL), then inline code, then regex scan.
T-09 guards: 10 MB size limit, UTF-8 decode with errors='replace', 1000-match cap.
"""
from __future__ import annotations

import re
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
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


def scan_artifact(
    artifact_path: Path,
    registry: dict[str, RegistryEntry],
    allow_draft: list[str],
) -> tuple[list[tuple[str, str]], list[str]]:
    args = [artifact_path, registry, allow_draft]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_scan_artifact__mutmut_orig, x_scan_artifact__mutmut_mutants, args, kwargs, None)


def x_scan_artifact__mutmut_orig(
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


def x_scan_artifact__mutmut_1(
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
        size = None
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


def x_scan_artifact__mutmut_2(
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
        raise AuditError(None) from exc

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


def x_scan_artifact__mutmut_3(
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

    if size >= _MAX_BYTES:
        raise AuditError(
            f"Artifact exceeds 10 MB size limit ({size} bytes): {artifact_path}"
        )

    # T-09: encoding guard
    try:
        raw = artifact_path.read_bytes()
    except OSError as exc:
        raise AuditError(f"Cannot read artifact: {artifact_path}: {exc}") from exc

    text = raw.decode("utf-8", errors="replace")

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


def x_scan_artifact__mutmut_4(
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
            None
        )

    # T-09: encoding guard
    try:
        raw = artifact_path.read_bytes()
    except OSError as exc:
        raise AuditError(f"Cannot read artifact: {artifact_path}: {exc}") from exc

    text = raw.decode("utf-8", errors="replace")

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


def x_scan_artifact__mutmut_5(
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
        raw = None
    except OSError as exc:
        raise AuditError(f"Cannot read artifact: {artifact_path}: {exc}") from exc

    text = raw.decode("utf-8", errors="replace")

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


def x_scan_artifact__mutmut_6(
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
        raise AuditError(None) from exc

    text = raw.decode("utf-8", errors="replace")

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


def x_scan_artifact__mutmut_7(
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

    text = None

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


def x_scan_artifact__mutmut_8(
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

    text = raw.decode(None, errors="replace")

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


def x_scan_artifact__mutmut_9(
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

    text = raw.decode("utf-8", errors=None)

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


def x_scan_artifact__mutmut_10(
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

    text = raw.decode(errors="replace")

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


def x_scan_artifact__mutmut_11(
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

    text = raw.decode("utf-8", )

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


def x_scan_artifact__mutmut_12(
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

    text = raw.decode("XXutf-8XX", errors="replace")

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


def x_scan_artifact__mutmut_13(
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

    text = raw.decode("UTF-8", errors="replace")

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


def x_scan_artifact__mutmut_14(
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

    text = raw.decode("utf-8", errors="XXreplaceXX")

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


def x_scan_artifact__mutmut_15(
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

    text = raw.decode("utf-8", errors="REPLACE")

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


def x_scan_artifact__mutmut_16(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = None

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


def x_scan_artifact__mutmut_17(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub(None, text)

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


def x_scan_artifact__mutmut_18(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub("", None)

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


def x_scan_artifact__mutmut_19(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub(text)

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


def x_scan_artifact__mutmut_20(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub("", )

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


def x_scan_artifact__mutmut_21(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub("XXXX", text)

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


def x_scan_artifact__mutmut_22(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub("", text)

    # Pass 2: strip inline code
    stripped = None

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


def x_scan_artifact__mutmut_23(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub("", text)

    # Pass 2: strip inline code
    stripped = _INLINE_CODE_RE.sub(None, stripped)

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


def x_scan_artifact__mutmut_24(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub("", text)

    # Pass 2: strip inline code
    stripped = _INLINE_CODE_RE.sub("", None)

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


def x_scan_artifact__mutmut_25(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub("", text)

    # Pass 2: strip inline code
    stripped = _INLINE_CODE_RE.sub(stripped)

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


def x_scan_artifact__mutmut_26(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub("", text)

    # Pass 2: strip inline code
    stripped = _INLINE_CODE_RE.sub("", )

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


def x_scan_artifact__mutmut_27(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub("", text)

    # Pass 2: strip inline code
    stripped = _INLINE_CODE_RE.sub("XXXX", stripped)

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


def x_scan_artifact__mutmut_28(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub("", text)

    # Pass 2: strip inline code
    stripped = _INLINE_CODE_RE.sub("", stripped)

    # Build allow_draft set for O(1) lookup
    allow_draft_set = None

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


def x_scan_artifact__mutmut_29(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub("", text)

    # Pass 2: strip inline code
    stripped = _INLINE_CODE_RE.sub("", stripped)

    # Build allow_draft set for O(1) lookup
    allow_draft_set = set(None)

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


def x_scan_artifact__mutmut_30(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub("", text)

    # Pass 2: strip inline code
    stripped = _INLINE_CODE_RE.sub("", stripped)

    # Build allow_draft set for O(1) lookup
    allow_draft_set = set(allow_draft)

    citations: list[tuple[str, str]] = None
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


def x_scan_artifact__mutmut_31(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub("", text)

    # Pass 2: strip inline code
    stripped = _INLINE_CODE_RE.sub("", stripped)

    # Build allow_draft set for O(1) lookup
    allow_draft_set = set(allow_draft)

    citations: list[tuple[str, str]] = []
    draft_skipped: list[str] = None
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


def x_scan_artifact__mutmut_32(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub("", text)

    # Pass 2: strip inline code
    stripped = _INLINE_CODE_RE.sub("", stripped)

    # Build allow_draft set for O(1) lookup
    allow_draft_set = set(allow_draft)

    citations: list[tuple[str, str]] = []
    draft_skipped: list[str] = []
    seen: set[str] = None

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


def x_scan_artifact__mutmut_33(
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

    # Pass 1: strip fenced code blocks (ADR-003, DOTALL so multi-line blocks are removed)
    stripped = _FENCE_RE.sub("", text)

    # Pass 2: strip inline code
    stripped = _INLINE_CODE_RE.sub("", stripped)

    # Build allow_draft set for O(1) lookup
    allow_draft_set = set(allow_draft)

    citations: list[tuple[str, str]] = []
    draft_skipped: list[str] = []
    seen: set[str] = set()

    for match in _LAW_ID_RE.finditer(None):
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


def x_scan_artifact__mutmut_34(
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
        law_id = None

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


def x_scan_artifact__mutmut_35(
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
        law_id = match.group(None)

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


def x_scan_artifact__mutmut_36(
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
        law_id = match.group(1)

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


def x_scan_artifact__mutmut_37(
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

        if law_id not in seen:
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


def x_scan_artifact__mutmut_38(
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
            break  # dedup: first-occurrence wins

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


def x_scan_artifact__mutmut_39(
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

        seen.add(None)

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


def x_scan_artifact__mutmut_40(
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
        if law_id not in allow_draft_set:
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


def x_scan_artifact__mutmut_41(
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
            draft_skipped.append(None)
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


def x_scan_artifact__mutmut_42(
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
            break

        # Build context snippet ±150 chars
        start = max(0, match.start() - _CONTEXT_WINDOW)
        end = min(len(stripped), match.end() + _CONTEXT_WINDOW)
        snippet = stripped[start:end]

        citations.append((law_id, snippet))

        # T-09: cap at 1000 unique citations
        if len(citations) >= _MAX_MATCHES:
            break

    return citations, draft_skipped


def x_scan_artifact__mutmut_43(
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
        start = None
        end = min(len(stripped), match.end() + _CONTEXT_WINDOW)
        snippet = stripped[start:end]

        citations.append((law_id, snippet))

        # T-09: cap at 1000 unique citations
        if len(citations) >= _MAX_MATCHES:
            break

    return citations, draft_skipped


def x_scan_artifact__mutmut_44(
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
        start = max(None, match.start() - _CONTEXT_WINDOW)
        end = min(len(stripped), match.end() + _CONTEXT_WINDOW)
        snippet = stripped[start:end]

        citations.append((law_id, snippet))

        # T-09: cap at 1000 unique citations
        if len(citations) >= _MAX_MATCHES:
            break

    return citations, draft_skipped


def x_scan_artifact__mutmut_45(
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
        start = max(0, None)
        end = min(len(stripped), match.end() + _CONTEXT_WINDOW)
        snippet = stripped[start:end]

        citations.append((law_id, snippet))

        # T-09: cap at 1000 unique citations
        if len(citations) >= _MAX_MATCHES:
            break

    return citations, draft_skipped


def x_scan_artifact__mutmut_46(
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
        start = max(match.start() - _CONTEXT_WINDOW)
        end = min(len(stripped), match.end() + _CONTEXT_WINDOW)
        snippet = stripped[start:end]

        citations.append((law_id, snippet))

        # T-09: cap at 1000 unique citations
        if len(citations) >= _MAX_MATCHES:
            break

    return citations, draft_skipped


def x_scan_artifact__mutmut_47(
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
        start = max(0, )
        end = min(len(stripped), match.end() + _CONTEXT_WINDOW)
        snippet = stripped[start:end]

        citations.append((law_id, snippet))

        # T-09: cap at 1000 unique citations
        if len(citations) >= _MAX_MATCHES:
            break

    return citations, draft_skipped


def x_scan_artifact__mutmut_48(
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
        start = max(1, match.start() - _CONTEXT_WINDOW)
        end = min(len(stripped), match.end() + _CONTEXT_WINDOW)
        snippet = stripped[start:end]

        citations.append((law_id, snippet))

        # T-09: cap at 1000 unique citations
        if len(citations) >= _MAX_MATCHES:
            break

    return citations, draft_skipped


def x_scan_artifact__mutmut_49(
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
        start = max(0, match.start() + _CONTEXT_WINDOW)
        end = min(len(stripped), match.end() + _CONTEXT_WINDOW)
        snippet = stripped[start:end]

        citations.append((law_id, snippet))

        # T-09: cap at 1000 unique citations
        if len(citations) >= _MAX_MATCHES:
            break

    return citations, draft_skipped


def x_scan_artifact__mutmut_50(
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
        end = None
        snippet = stripped[start:end]

        citations.append((law_id, snippet))

        # T-09: cap at 1000 unique citations
        if len(citations) >= _MAX_MATCHES:
            break

    return citations, draft_skipped


def x_scan_artifact__mutmut_51(
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
        end = min(None, match.end() + _CONTEXT_WINDOW)
        snippet = stripped[start:end]

        citations.append((law_id, snippet))

        # T-09: cap at 1000 unique citations
        if len(citations) >= _MAX_MATCHES:
            break

    return citations, draft_skipped


def x_scan_artifact__mutmut_52(
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
        end = min(len(stripped), None)
        snippet = stripped[start:end]

        citations.append((law_id, snippet))

        # T-09: cap at 1000 unique citations
        if len(citations) >= _MAX_MATCHES:
            break

    return citations, draft_skipped


def x_scan_artifact__mutmut_53(
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
        end = min(match.end() + _CONTEXT_WINDOW)
        snippet = stripped[start:end]

        citations.append((law_id, snippet))

        # T-09: cap at 1000 unique citations
        if len(citations) >= _MAX_MATCHES:
            break

    return citations, draft_skipped


def x_scan_artifact__mutmut_54(
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
        end = min(len(stripped), )
        snippet = stripped[start:end]

        citations.append((law_id, snippet))

        # T-09: cap at 1000 unique citations
        if len(citations) >= _MAX_MATCHES:
            break

    return citations, draft_skipped


def x_scan_artifact__mutmut_55(
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
        end = min(len(stripped), match.end() - _CONTEXT_WINDOW)
        snippet = stripped[start:end]

        citations.append((law_id, snippet))

        # T-09: cap at 1000 unique citations
        if len(citations) >= _MAX_MATCHES:
            break

    return citations, draft_skipped


def x_scan_artifact__mutmut_56(
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
        snippet = None

        citations.append((law_id, snippet))

        # T-09: cap at 1000 unique citations
        if len(citations) >= _MAX_MATCHES:
            break

    return citations, draft_skipped


def x_scan_artifact__mutmut_57(
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

        citations.append(None)

        # T-09: cap at 1000 unique citations
        if len(citations) >= _MAX_MATCHES:
            break

    return citations, draft_skipped


def x_scan_artifact__mutmut_58(
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
        if len(citations) > _MAX_MATCHES:
            break

    return citations, draft_skipped


def x_scan_artifact__mutmut_59(
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
            return

    return citations, draft_skipped

x_scan_artifact__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_scan_artifact__mutmut_1': x_scan_artifact__mutmut_1, 
    'x_scan_artifact__mutmut_2': x_scan_artifact__mutmut_2, 
    'x_scan_artifact__mutmut_3': x_scan_artifact__mutmut_3, 
    'x_scan_artifact__mutmut_4': x_scan_artifact__mutmut_4, 
    'x_scan_artifact__mutmut_5': x_scan_artifact__mutmut_5, 
    'x_scan_artifact__mutmut_6': x_scan_artifact__mutmut_6, 
    'x_scan_artifact__mutmut_7': x_scan_artifact__mutmut_7, 
    'x_scan_artifact__mutmut_8': x_scan_artifact__mutmut_8, 
    'x_scan_artifact__mutmut_9': x_scan_artifact__mutmut_9, 
    'x_scan_artifact__mutmut_10': x_scan_artifact__mutmut_10, 
    'x_scan_artifact__mutmut_11': x_scan_artifact__mutmut_11, 
    'x_scan_artifact__mutmut_12': x_scan_artifact__mutmut_12, 
    'x_scan_artifact__mutmut_13': x_scan_artifact__mutmut_13, 
    'x_scan_artifact__mutmut_14': x_scan_artifact__mutmut_14, 
    'x_scan_artifact__mutmut_15': x_scan_artifact__mutmut_15, 
    'x_scan_artifact__mutmut_16': x_scan_artifact__mutmut_16, 
    'x_scan_artifact__mutmut_17': x_scan_artifact__mutmut_17, 
    'x_scan_artifact__mutmut_18': x_scan_artifact__mutmut_18, 
    'x_scan_artifact__mutmut_19': x_scan_artifact__mutmut_19, 
    'x_scan_artifact__mutmut_20': x_scan_artifact__mutmut_20, 
    'x_scan_artifact__mutmut_21': x_scan_artifact__mutmut_21, 
    'x_scan_artifact__mutmut_22': x_scan_artifact__mutmut_22, 
    'x_scan_artifact__mutmut_23': x_scan_artifact__mutmut_23, 
    'x_scan_artifact__mutmut_24': x_scan_artifact__mutmut_24, 
    'x_scan_artifact__mutmut_25': x_scan_artifact__mutmut_25, 
    'x_scan_artifact__mutmut_26': x_scan_artifact__mutmut_26, 
    'x_scan_artifact__mutmut_27': x_scan_artifact__mutmut_27, 
    'x_scan_artifact__mutmut_28': x_scan_artifact__mutmut_28, 
    'x_scan_artifact__mutmut_29': x_scan_artifact__mutmut_29, 
    'x_scan_artifact__mutmut_30': x_scan_artifact__mutmut_30, 
    'x_scan_artifact__mutmut_31': x_scan_artifact__mutmut_31, 
    'x_scan_artifact__mutmut_32': x_scan_artifact__mutmut_32, 
    'x_scan_artifact__mutmut_33': x_scan_artifact__mutmut_33, 
    'x_scan_artifact__mutmut_34': x_scan_artifact__mutmut_34, 
    'x_scan_artifact__mutmut_35': x_scan_artifact__mutmut_35, 
    'x_scan_artifact__mutmut_36': x_scan_artifact__mutmut_36, 
    'x_scan_artifact__mutmut_37': x_scan_artifact__mutmut_37, 
    'x_scan_artifact__mutmut_38': x_scan_artifact__mutmut_38, 
    'x_scan_artifact__mutmut_39': x_scan_artifact__mutmut_39, 
    'x_scan_artifact__mutmut_40': x_scan_artifact__mutmut_40, 
    'x_scan_artifact__mutmut_41': x_scan_artifact__mutmut_41, 
    'x_scan_artifact__mutmut_42': x_scan_artifact__mutmut_42, 
    'x_scan_artifact__mutmut_43': x_scan_artifact__mutmut_43, 
    'x_scan_artifact__mutmut_44': x_scan_artifact__mutmut_44, 
    'x_scan_artifact__mutmut_45': x_scan_artifact__mutmut_45, 
    'x_scan_artifact__mutmut_46': x_scan_artifact__mutmut_46, 
    'x_scan_artifact__mutmut_47': x_scan_artifact__mutmut_47, 
    'x_scan_artifact__mutmut_48': x_scan_artifact__mutmut_48, 
    'x_scan_artifact__mutmut_49': x_scan_artifact__mutmut_49, 
    'x_scan_artifact__mutmut_50': x_scan_artifact__mutmut_50, 
    'x_scan_artifact__mutmut_51': x_scan_artifact__mutmut_51, 
    'x_scan_artifact__mutmut_52': x_scan_artifact__mutmut_52, 
    'x_scan_artifact__mutmut_53': x_scan_artifact__mutmut_53, 
    'x_scan_artifact__mutmut_54': x_scan_artifact__mutmut_54, 
    'x_scan_artifact__mutmut_55': x_scan_artifact__mutmut_55, 
    'x_scan_artifact__mutmut_56': x_scan_artifact__mutmut_56, 
    'x_scan_artifact__mutmut_57': x_scan_artifact__mutmut_57, 
    'x_scan_artifact__mutmut_58': x_scan_artifact__mutmut_58, 
    'x_scan_artifact__mutmut_59': x_scan_artifact__mutmut_59
}
x_scan_artifact__mutmut_orig.__name__ = 'x_scan_artifact'
