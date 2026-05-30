"""auditor.py — L1 verdict logic. Pure function, no I/O.

Verdict rules (Phase 3 §2.2):
  FAIL  — law_id not in registry
  WARN  (TITLE_MISMATCH) — explicit title phrase within ±30 chars, partial_ratio < 60
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
_TITLE_WINDOW = 30
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
    args = [citations, registry, artifact_path, registry_path, law_count, draft_skipped, allow_draft, strict, timestamp, tool_version]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_audit__mutmut_orig, x_audit__mutmut_mutants, args, kwargs, None)


def x_audit__mutmut_orig(
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


def x_audit__mutmut_1(
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
        results: list[CitationResult] = None

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


def x_audit__mutmut_2(
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
            entry = None

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


def x_audit__mutmut_3(
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
            entry = registry.get(None)

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


def x_audit__mutmut_4(
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

            if entry is not None:
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


def x_audit__mutmut_5(
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
                results.append(None)
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


def x_audit__mutmut_6(
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
                    law_id=None,
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


def x_audit__mutmut_7(
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
                    verdict=None,
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


def x_audit__mutmut_8(
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
                    note=None,
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


def x_audit__mutmut_9(
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
                    context_snippet=None,
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


def x_audit__mutmut_10(
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


def x_audit__mutmut_11(
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


def x_audit__mutmut_12(
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


def x_audit__mutmut_13(
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


def x_audit__mutmut_14(
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
                break

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


def x_audit__mutmut_15(
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
            status_note = None
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


def x_audit__mutmut_16(
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
            status_note = _check_status_mismatch(None, snippet, entry)
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


def x_audit__mutmut_17(
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
            status_note = _check_status_mismatch(law_id, None, entry)
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


def x_audit__mutmut_18(
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
            status_note = _check_status_mismatch(law_id, snippet, None)
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


def x_audit__mutmut_19(
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
            status_note = _check_status_mismatch(snippet, entry)
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


def x_audit__mutmut_20(
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
            status_note = _check_status_mismatch(law_id, entry)
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


def x_audit__mutmut_21(
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
            status_note = _check_status_mismatch(law_id, snippet, )
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


def x_audit__mutmut_22(
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
                results.append(None)
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


def x_audit__mutmut_23(
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
                    law_id=None,
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


def x_audit__mutmut_24(
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
                    verdict=None,
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


def x_audit__mutmut_25(
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
                    note=None,
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


def x_audit__mutmut_26(
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
                    context_snippet=None,
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


def x_audit__mutmut_27(
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


def x_audit__mutmut_28(
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


def x_audit__mutmut_29(
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


def x_audit__mutmut_30(
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


def x_audit__mutmut_31(
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
                break

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


def x_audit__mutmut_32(
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
                title_note = None
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


def x_audit__mutmut_33(
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
                title_note = _check_title_mismatch(None, snippet, entry.title)
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


def x_audit__mutmut_34(
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
                title_note = _check_title_mismatch(law_id, None, entry.title)
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


def x_audit__mutmut_35(
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
                title_note = _check_title_mismatch(law_id, snippet, None)
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


def x_audit__mutmut_36(
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
                title_note = _check_title_mismatch(snippet, entry.title)
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


def x_audit__mutmut_37(
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
                title_note = _check_title_mismatch(law_id, entry.title)
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


def x_audit__mutmut_38(
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
                title_note = _check_title_mismatch(law_id, snippet, )
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


def x_audit__mutmut_39(
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
                    results.append(None)
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


def x_audit__mutmut_40(
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
                        law_id=None,
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


def x_audit__mutmut_41(
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
                        verdict=None,
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


def x_audit__mutmut_42(
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
                        note=None,
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


def x_audit__mutmut_43(
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
                        context_snippet=None,
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


def x_audit__mutmut_44(
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


def x_audit__mutmut_45(
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


def x_audit__mutmut_46(
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


def x_audit__mutmut_47(
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


def x_audit__mutmut_48(
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
                    break

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


def x_audit__mutmut_49(
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

            results.append(None)

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


def x_audit__mutmut_50(
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
                law_id=None,
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


def x_audit__mutmut_51(
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
                verdict=None,
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


def x_audit__mutmut_52(
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


def x_audit__mutmut_53(
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


def x_audit__mutmut_54(
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


def x_audit__mutmut_55(
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


def x_audit__mutmut_56(
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
        results.sort(key=None)

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


def x_audit__mutmut_57(
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
        results.sort(key=lambda r: None)

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


def x_audit__mutmut_58(
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
            artifact_path=None,
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


def x_audit__mutmut_59(
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
            registry_path=None,
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


def x_audit__mutmut_60(
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
            law_count=None,
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


def x_audit__mutmut_61(
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
            scanned=None,
            results=results,
            draft_skipped=draft_skipped,
            allow_draft=allow_draft,
            strict=strict,
            timestamp=timestamp,
            tool_version=tool_version,
        )
    except (KeyError, TypeError, AttributeError) as exc:
        raise AuditError(f"Internal auditor failure: {exc}") from exc


def x_audit__mutmut_62(
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
            results=None,
            draft_skipped=draft_skipped,
            allow_draft=allow_draft,
            strict=strict,
            timestamp=timestamp,
            tool_version=tool_version,
        )
    except (KeyError, TypeError, AttributeError) as exc:
        raise AuditError(f"Internal auditor failure: {exc}") from exc


def x_audit__mutmut_63(
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
            draft_skipped=None,
            allow_draft=allow_draft,
            strict=strict,
            timestamp=timestamp,
            tool_version=tool_version,
        )
    except (KeyError, TypeError, AttributeError) as exc:
        raise AuditError(f"Internal auditor failure: {exc}") from exc


def x_audit__mutmut_64(
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
            allow_draft=None,
            strict=strict,
            timestamp=timestamp,
            tool_version=tool_version,
        )
    except (KeyError, TypeError, AttributeError) as exc:
        raise AuditError(f"Internal auditor failure: {exc}") from exc


def x_audit__mutmut_65(
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
            strict=None,
            timestamp=timestamp,
            tool_version=tool_version,
        )
    except (KeyError, TypeError, AttributeError) as exc:
        raise AuditError(f"Internal auditor failure: {exc}") from exc


def x_audit__mutmut_66(
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
            timestamp=None,
            tool_version=tool_version,
        )
    except (KeyError, TypeError, AttributeError) as exc:
        raise AuditError(f"Internal auditor failure: {exc}") from exc


def x_audit__mutmut_67(
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
            tool_version=None,
        )
    except (KeyError, TypeError, AttributeError) as exc:
        raise AuditError(f"Internal auditor failure: {exc}") from exc


def x_audit__mutmut_68(
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


def x_audit__mutmut_69(
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


def x_audit__mutmut_70(
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


def x_audit__mutmut_71(
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
            results=results,
            draft_skipped=draft_skipped,
            allow_draft=allow_draft,
            strict=strict,
            timestamp=timestamp,
            tool_version=tool_version,
        )
    except (KeyError, TypeError, AttributeError) as exc:
        raise AuditError(f"Internal auditor failure: {exc}") from exc


def x_audit__mutmut_72(
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
            draft_skipped=draft_skipped,
            allow_draft=allow_draft,
            strict=strict,
            timestamp=timestamp,
            tool_version=tool_version,
        )
    except (KeyError, TypeError, AttributeError) as exc:
        raise AuditError(f"Internal auditor failure: {exc}") from exc


def x_audit__mutmut_73(
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
            allow_draft=allow_draft,
            strict=strict,
            timestamp=timestamp,
            tool_version=tool_version,
        )
    except (KeyError, TypeError, AttributeError) as exc:
        raise AuditError(f"Internal auditor failure: {exc}") from exc


def x_audit__mutmut_74(
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
            strict=strict,
            timestamp=timestamp,
            tool_version=tool_version,
        )
    except (KeyError, TypeError, AttributeError) as exc:
        raise AuditError(f"Internal auditor failure: {exc}") from exc


def x_audit__mutmut_75(
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
            timestamp=timestamp,
            tool_version=tool_version,
        )
    except (KeyError, TypeError, AttributeError) as exc:
        raise AuditError(f"Internal auditor failure: {exc}") from exc


def x_audit__mutmut_76(
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
            tool_version=tool_version,
        )
    except (KeyError, TypeError, AttributeError) as exc:
        raise AuditError(f"Internal auditor failure: {exc}") from exc


def x_audit__mutmut_77(
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
            )
    except (KeyError, TypeError, AttributeError) as exc:
        raise AuditError(f"Internal auditor failure: {exc}") from exc


def x_audit__mutmut_78(
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
        raise AuditError(None) from exc

x_audit__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_audit__mutmut_1': x_audit__mutmut_1, 
    'x_audit__mutmut_2': x_audit__mutmut_2, 
    'x_audit__mutmut_3': x_audit__mutmut_3, 
    'x_audit__mutmut_4': x_audit__mutmut_4, 
    'x_audit__mutmut_5': x_audit__mutmut_5, 
    'x_audit__mutmut_6': x_audit__mutmut_6, 
    'x_audit__mutmut_7': x_audit__mutmut_7, 
    'x_audit__mutmut_8': x_audit__mutmut_8, 
    'x_audit__mutmut_9': x_audit__mutmut_9, 
    'x_audit__mutmut_10': x_audit__mutmut_10, 
    'x_audit__mutmut_11': x_audit__mutmut_11, 
    'x_audit__mutmut_12': x_audit__mutmut_12, 
    'x_audit__mutmut_13': x_audit__mutmut_13, 
    'x_audit__mutmut_14': x_audit__mutmut_14, 
    'x_audit__mutmut_15': x_audit__mutmut_15, 
    'x_audit__mutmut_16': x_audit__mutmut_16, 
    'x_audit__mutmut_17': x_audit__mutmut_17, 
    'x_audit__mutmut_18': x_audit__mutmut_18, 
    'x_audit__mutmut_19': x_audit__mutmut_19, 
    'x_audit__mutmut_20': x_audit__mutmut_20, 
    'x_audit__mutmut_21': x_audit__mutmut_21, 
    'x_audit__mutmut_22': x_audit__mutmut_22, 
    'x_audit__mutmut_23': x_audit__mutmut_23, 
    'x_audit__mutmut_24': x_audit__mutmut_24, 
    'x_audit__mutmut_25': x_audit__mutmut_25, 
    'x_audit__mutmut_26': x_audit__mutmut_26, 
    'x_audit__mutmut_27': x_audit__mutmut_27, 
    'x_audit__mutmut_28': x_audit__mutmut_28, 
    'x_audit__mutmut_29': x_audit__mutmut_29, 
    'x_audit__mutmut_30': x_audit__mutmut_30, 
    'x_audit__mutmut_31': x_audit__mutmut_31, 
    'x_audit__mutmut_32': x_audit__mutmut_32, 
    'x_audit__mutmut_33': x_audit__mutmut_33, 
    'x_audit__mutmut_34': x_audit__mutmut_34, 
    'x_audit__mutmut_35': x_audit__mutmut_35, 
    'x_audit__mutmut_36': x_audit__mutmut_36, 
    'x_audit__mutmut_37': x_audit__mutmut_37, 
    'x_audit__mutmut_38': x_audit__mutmut_38, 
    'x_audit__mutmut_39': x_audit__mutmut_39, 
    'x_audit__mutmut_40': x_audit__mutmut_40, 
    'x_audit__mutmut_41': x_audit__mutmut_41, 
    'x_audit__mutmut_42': x_audit__mutmut_42, 
    'x_audit__mutmut_43': x_audit__mutmut_43, 
    'x_audit__mutmut_44': x_audit__mutmut_44, 
    'x_audit__mutmut_45': x_audit__mutmut_45, 
    'x_audit__mutmut_46': x_audit__mutmut_46, 
    'x_audit__mutmut_47': x_audit__mutmut_47, 
    'x_audit__mutmut_48': x_audit__mutmut_48, 
    'x_audit__mutmut_49': x_audit__mutmut_49, 
    'x_audit__mutmut_50': x_audit__mutmut_50, 
    'x_audit__mutmut_51': x_audit__mutmut_51, 
    'x_audit__mutmut_52': x_audit__mutmut_52, 
    'x_audit__mutmut_53': x_audit__mutmut_53, 
    'x_audit__mutmut_54': x_audit__mutmut_54, 
    'x_audit__mutmut_55': x_audit__mutmut_55, 
    'x_audit__mutmut_56': x_audit__mutmut_56, 
    'x_audit__mutmut_57': x_audit__mutmut_57, 
    'x_audit__mutmut_58': x_audit__mutmut_58, 
    'x_audit__mutmut_59': x_audit__mutmut_59, 
    'x_audit__mutmut_60': x_audit__mutmut_60, 
    'x_audit__mutmut_61': x_audit__mutmut_61, 
    'x_audit__mutmut_62': x_audit__mutmut_62, 
    'x_audit__mutmut_63': x_audit__mutmut_63, 
    'x_audit__mutmut_64': x_audit__mutmut_64, 
    'x_audit__mutmut_65': x_audit__mutmut_65, 
    'x_audit__mutmut_66': x_audit__mutmut_66, 
    'x_audit__mutmut_67': x_audit__mutmut_67, 
    'x_audit__mutmut_68': x_audit__mutmut_68, 
    'x_audit__mutmut_69': x_audit__mutmut_69, 
    'x_audit__mutmut_70': x_audit__mutmut_70, 
    'x_audit__mutmut_71': x_audit__mutmut_71, 
    'x_audit__mutmut_72': x_audit__mutmut_72, 
    'x_audit__mutmut_73': x_audit__mutmut_73, 
    'x_audit__mutmut_74': x_audit__mutmut_74, 
    'x_audit__mutmut_75': x_audit__mutmut_75, 
    'x_audit__mutmut_76': x_audit__mutmut_76, 
    'x_audit__mutmut_77': x_audit__mutmut_77, 
    'x_audit__mutmut_78': x_audit__mutmut_78
}
x_audit__mutmut_orig.__name__ = 'x_audit'


def _find_id_pos_in_snippet(law_id: str, snippet: str) -> int | None:
    args = [law_id, snippet]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__find_id_pos_in_snippet__mutmut_orig, x__find_id_pos_in_snippet__mutmut_mutants, args, kwargs, None)


def x__find_id_pos_in_snippet__mutmut_orig(law_id: str, snippet: str) -> int | None:
    """Return start position of law_id in snippet, or None."""
    idx = snippet.find(law_id)
    return idx if idx >= 0 else None


def x__find_id_pos_in_snippet__mutmut_1(law_id: str, snippet: str) -> int | None:
    """Return start position of law_id in snippet, or None."""
    idx = None
    return idx if idx >= 0 else None


def x__find_id_pos_in_snippet__mutmut_2(law_id: str, snippet: str) -> int | None:
    """Return start position of law_id in snippet, or None."""
    idx = snippet.find(None)
    return idx if idx >= 0 else None


def x__find_id_pos_in_snippet__mutmut_3(law_id: str, snippet: str) -> int | None:
    """Return start position of law_id in snippet, or None."""
    idx = snippet.rfind(law_id)
    return idx if idx >= 0 else None


def x__find_id_pos_in_snippet__mutmut_4(law_id: str, snippet: str) -> int | None:
    """Return start position of law_id in snippet, or None."""
    idx = snippet.find(law_id)
    return idx if idx > 0 else None


def x__find_id_pos_in_snippet__mutmut_5(law_id: str, snippet: str) -> int | None:
    """Return start position of law_id in snippet, or None."""
    idx = snippet.find(law_id)
    return idx if idx >= 1 else None

x__find_id_pos_in_snippet__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__find_id_pos_in_snippet__mutmut_1': x__find_id_pos_in_snippet__mutmut_1, 
    'x__find_id_pos_in_snippet__mutmut_2': x__find_id_pos_in_snippet__mutmut_2, 
    'x__find_id_pos_in_snippet__mutmut_3': x__find_id_pos_in_snippet__mutmut_3, 
    'x__find_id_pos_in_snippet__mutmut_4': x__find_id_pos_in_snippet__mutmut_4, 
    'x__find_id_pos_in_snippet__mutmut_5': x__find_id_pos_in_snippet__mutmut_5
}
x__find_id_pos_in_snippet__mutmut_orig.__name__ = 'x__find_id_pos_in_snippet'


def _check_status_mismatch(
    law_id: str, snippet: str, entry: RegistryEntry
) -> str | None:
    args = [law_id, snippet, entry]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__check_status_mismatch__mutmut_orig, x__check_status_mismatch__mutmut_mutants, args, kwargs, None)


def x__check_status_mismatch__mutmut_orig(
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


def x__check_status_mismatch__mutmut_1(
    law_id: str, snippet: str, entry: RegistryEntry
) -> str | None:
    """Return a WARN note if status assertion within ±50 chars contradicts registry."""
    pos = None
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


def x__check_status_mismatch__mutmut_2(
    law_id: str, snippet: str, entry: RegistryEntry
) -> str | None:
    """Return a WARN note if status assertion within ±50 chars contradicts registry."""
    pos = _find_id_pos_in_snippet(None, snippet)
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


def x__check_status_mismatch__mutmut_3(
    law_id: str, snippet: str, entry: RegistryEntry
) -> str | None:
    """Return a WARN note if status assertion within ±50 chars contradicts registry."""
    pos = _find_id_pos_in_snippet(law_id, None)
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


def x__check_status_mismatch__mutmut_4(
    law_id: str, snippet: str, entry: RegistryEntry
) -> str | None:
    """Return a WARN note if status assertion within ±50 chars contradicts registry."""
    pos = _find_id_pos_in_snippet(snippet)
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


def x__check_status_mismatch__mutmut_5(
    law_id: str, snippet: str, entry: RegistryEntry
) -> str | None:
    """Return a WARN note if status assertion within ±50 chars contradicts registry."""
    pos = _find_id_pos_in_snippet(law_id, )
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


def x__check_status_mismatch__mutmut_6(
    law_id: str, snippet: str, entry: RegistryEntry
) -> str | None:
    """Return a WARN note if status assertion within ±50 chars contradicts registry."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is not None:
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


def x__check_status_mismatch__mutmut_7(
    law_id: str, snippet: str, entry: RegistryEntry
) -> str | None:
    """Return a WARN note if status assertion within ±50 chars contradicts registry."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    # Window: 50 chars after the end of the law_id match
    id_end = None
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


def x__check_status_mismatch__mutmut_8(
    law_id: str, snippet: str, entry: RegistryEntry
) -> str | None:
    """Return a WARN note if status assertion within ±50 chars contradicts registry."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    # Window: 50 chars after the end of the law_id match
    id_end = pos - len(law_id)
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


def x__check_status_mismatch__mutmut_9(
    law_id: str, snippet: str, entry: RegistryEntry
) -> str | None:
    """Return a WARN note if status assertion within ±50 chars contradicts registry."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    # Window: 50 chars after the end of the law_id match
    id_end = pos + len(law_id)
    window = None

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


def x__check_status_mismatch__mutmut_10(
    law_id: str, snippet: str, entry: RegistryEntry
) -> str | None:
    """Return a WARN note if status assertion within ±50 chars contradicts registry."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    # Window: 50 chars after the end of the law_id match
    id_end = pos + len(law_id)
    window = snippet[id_end: id_end - _STATUS_WINDOW]

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


def x__check_status_mismatch__mutmut_11(
    law_id: str, snippet: str, entry: RegistryEntry
) -> str | None:
    """Return a WARN note if status assertion within ±50 chars contradicts registry."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    # Window: 50 chars after the end of the law_id match
    id_end = pos + len(law_id)
    window = snippet[id_end: id_end + _STATUS_WINDOW]

    asserts_non_neg = None
    asserts_strictly = bool(_STATUS_STRICT.search(window))

    if not asserts_non_neg and not asserts_strictly:
        return None  # no assertion found

    is_non_neg = entry.non_negotiable

    if asserts_non_neg and not is_non_neg:
        return f"Status mismatch: artifact asserts NON-NEGOTIABLE but registry marks {law_id} as non_negotiable=false"

    if asserts_strictly and is_non_neg:
        return f"Status mismatch: artifact asserts STRICTLY ENFORCED but registry marks {law_id} as NON-NEGOTIABLE"

    return None  # assertion matches registry → PASS


def x__check_status_mismatch__mutmut_12(
    law_id: str, snippet: str, entry: RegistryEntry
) -> str | None:
    """Return a WARN note if status assertion within ±50 chars contradicts registry."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    # Window: 50 chars after the end of the law_id match
    id_end = pos + len(law_id)
    window = snippet[id_end: id_end + _STATUS_WINDOW]

    asserts_non_neg = bool(None)
    asserts_strictly = bool(_STATUS_STRICT.search(window))

    if not asserts_non_neg and not asserts_strictly:
        return None  # no assertion found

    is_non_neg = entry.non_negotiable

    if asserts_non_neg and not is_non_neg:
        return f"Status mismatch: artifact asserts NON-NEGOTIABLE but registry marks {law_id} as non_negotiable=false"

    if asserts_strictly and is_non_neg:
        return f"Status mismatch: artifact asserts STRICTLY ENFORCED but registry marks {law_id} as NON-NEGOTIABLE"

    return None  # assertion matches registry → PASS


def x__check_status_mismatch__mutmut_13(
    law_id: str, snippet: str, entry: RegistryEntry
) -> str | None:
    """Return a WARN note if status assertion within ±50 chars contradicts registry."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    # Window: 50 chars after the end of the law_id match
    id_end = pos + len(law_id)
    window = snippet[id_end: id_end + _STATUS_WINDOW]

    asserts_non_neg = bool(_STATUS_NON_NEG.search(None))
    asserts_strictly = bool(_STATUS_STRICT.search(window))

    if not asserts_non_neg and not asserts_strictly:
        return None  # no assertion found

    is_non_neg = entry.non_negotiable

    if asserts_non_neg and not is_non_neg:
        return f"Status mismatch: artifact asserts NON-NEGOTIABLE but registry marks {law_id} as non_negotiable=false"

    if asserts_strictly and is_non_neg:
        return f"Status mismatch: artifact asserts STRICTLY ENFORCED but registry marks {law_id} as NON-NEGOTIABLE"

    return None  # assertion matches registry → PASS


def x__check_status_mismatch__mutmut_14(
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
    asserts_strictly = None

    if not asserts_non_neg and not asserts_strictly:
        return None  # no assertion found

    is_non_neg = entry.non_negotiable

    if asserts_non_neg and not is_non_neg:
        return f"Status mismatch: artifact asserts NON-NEGOTIABLE but registry marks {law_id} as non_negotiable=false"

    if asserts_strictly and is_non_neg:
        return f"Status mismatch: artifact asserts STRICTLY ENFORCED but registry marks {law_id} as NON-NEGOTIABLE"

    return None  # assertion matches registry → PASS


def x__check_status_mismatch__mutmut_15(
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
    asserts_strictly = bool(None)

    if not asserts_non_neg and not asserts_strictly:
        return None  # no assertion found

    is_non_neg = entry.non_negotiable

    if asserts_non_neg and not is_non_neg:
        return f"Status mismatch: artifact asserts NON-NEGOTIABLE but registry marks {law_id} as non_negotiable=false"

    if asserts_strictly and is_non_neg:
        return f"Status mismatch: artifact asserts STRICTLY ENFORCED but registry marks {law_id} as NON-NEGOTIABLE"

    return None  # assertion matches registry → PASS


def x__check_status_mismatch__mutmut_16(
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
    asserts_strictly = bool(_STATUS_STRICT.search(None))

    if not asserts_non_neg and not asserts_strictly:
        return None  # no assertion found

    is_non_neg = entry.non_negotiable

    if asserts_non_neg and not is_non_neg:
        return f"Status mismatch: artifact asserts NON-NEGOTIABLE but registry marks {law_id} as non_negotiable=false"

    if asserts_strictly and is_non_neg:
        return f"Status mismatch: artifact asserts STRICTLY ENFORCED but registry marks {law_id} as NON-NEGOTIABLE"

    return None  # assertion matches registry → PASS


def x__check_status_mismatch__mutmut_17(
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

    if not asserts_non_neg or not asserts_strictly:
        return None  # no assertion found

    is_non_neg = entry.non_negotiable

    if asserts_non_neg and not is_non_neg:
        return f"Status mismatch: artifact asserts NON-NEGOTIABLE but registry marks {law_id} as non_negotiable=false"

    if asserts_strictly and is_non_neg:
        return f"Status mismatch: artifact asserts STRICTLY ENFORCED but registry marks {law_id} as NON-NEGOTIABLE"

    return None  # assertion matches registry → PASS


def x__check_status_mismatch__mutmut_18(
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

    if asserts_non_neg and not asserts_strictly:
        return None  # no assertion found

    is_non_neg = entry.non_negotiable

    if asserts_non_neg and not is_non_neg:
        return f"Status mismatch: artifact asserts NON-NEGOTIABLE but registry marks {law_id} as non_negotiable=false"

    if asserts_strictly and is_non_neg:
        return f"Status mismatch: artifact asserts STRICTLY ENFORCED but registry marks {law_id} as NON-NEGOTIABLE"

    return None  # assertion matches registry → PASS


def x__check_status_mismatch__mutmut_19(
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

    if not asserts_non_neg and asserts_strictly:
        return None  # no assertion found

    is_non_neg = entry.non_negotiable

    if asserts_non_neg and not is_non_neg:
        return f"Status mismatch: artifact asserts NON-NEGOTIABLE but registry marks {law_id} as non_negotiable=false"

    if asserts_strictly and is_non_neg:
        return f"Status mismatch: artifact asserts STRICTLY ENFORCED but registry marks {law_id} as NON-NEGOTIABLE"

    return None  # assertion matches registry → PASS


def x__check_status_mismatch__mutmut_20(
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

    is_non_neg = None

    if asserts_non_neg and not is_non_neg:
        return f"Status mismatch: artifact asserts NON-NEGOTIABLE but registry marks {law_id} as non_negotiable=false"

    if asserts_strictly and is_non_neg:
        return f"Status mismatch: artifact asserts STRICTLY ENFORCED but registry marks {law_id} as NON-NEGOTIABLE"

    return None  # assertion matches registry → PASS


def x__check_status_mismatch__mutmut_21(
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

    if asserts_non_neg or not is_non_neg:
        return f"Status mismatch: artifact asserts NON-NEGOTIABLE but registry marks {law_id} as non_negotiable=false"

    if asserts_strictly and is_non_neg:
        return f"Status mismatch: artifact asserts STRICTLY ENFORCED but registry marks {law_id} as NON-NEGOTIABLE"

    return None  # assertion matches registry → PASS


def x__check_status_mismatch__mutmut_22(
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

    if asserts_non_neg and is_non_neg:
        return f"Status mismatch: artifact asserts NON-NEGOTIABLE but registry marks {law_id} as non_negotiable=false"

    if asserts_strictly and is_non_neg:
        return f"Status mismatch: artifact asserts STRICTLY ENFORCED but registry marks {law_id} as NON-NEGOTIABLE"

    return None  # assertion matches registry → PASS


def x__check_status_mismatch__mutmut_23(
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

    if asserts_strictly or is_non_neg:
        return f"Status mismatch: artifact asserts STRICTLY ENFORCED but registry marks {law_id} as NON-NEGOTIABLE"

    return None  # assertion matches registry → PASS

x__check_status_mismatch__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__check_status_mismatch__mutmut_1': x__check_status_mismatch__mutmut_1, 
    'x__check_status_mismatch__mutmut_2': x__check_status_mismatch__mutmut_2, 
    'x__check_status_mismatch__mutmut_3': x__check_status_mismatch__mutmut_3, 
    'x__check_status_mismatch__mutmut_4': x__check_status_mismatch__mutmut_4, 
    'x__check_status_mismatch__mutmut_5': x__check_status_mismatch__mutmut_5, 
    'x__check_status_mismatch__mutmut_6': x__check_status_mismatch__mutmut_6, 
    'x__check_status_mismatch__mutmut_7': x__check_status_mismatch__mutmut_7, 
    'x__check_status_mismatch__mutmut_8': x__check_status_mismatch__mutmut_8, 
    'x__check_status_mismatch__mutmut_9': x__check_status_mismatch__mutmut_9, 
    'x__check_status_mismatch__mutmut_10': x__check_status_mismatch__mutmut_10, 
    'x__check_status_mismatch__mutmut_11': x__check_status_mismatch__mutmut_11, 
    'x__check_status_mismatch__mutmut_12': x__check_status_mismatch__mutmut_12, 
    'x__check_status_mismatch__mutmut_13': x__check_status_mismatch__mutmut_13, 
    'x__check_status_mismatch__mutmut_14': x__check_status_mismatch__mutmut_14, 
    'x__check_status_mismatch__mutmut_15': x__check_status_mismatch__mutmut_15, 
    'x__check_status_mismatch__mutmut_16': x__check_status_mismatch__mutmut_16, 
    'x__check_status_mismatch__mutmut_17': x__check_status_mismatch__mutmut_17, 
    'x__check_status_mismatch__mutmut_18': x__check_status_mismatch__mutmut_18, 
    'x__check_status_mismatch__mutmut_19': x__check_status_mismatch__mutmut_19, 
    'x__check_status_mismatch__mutmut_20': x__check_status_mismatch__mutmut_20, 
    'x__check_status_mismatch__mutmut_21': x__check_status_mismatch__mutmut_21, 
    'x__check_status_mismatch__mutmut_22': x__check_status_mismatch__mutmut_22, 
    'x__check_status_mismatch__mutmut_23': x__check_status_mismatch__mutmut_23
}
x__check_status_mismatch__mutmut_orig.__name__ = 'x__check_status_mismatch'


def _check_title_mismatch(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    args = [law_id, snippet, registry_title]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__check_title_mismatch__mutmut_orig, x__check_title_mismatch__mutmut_mutants, args, kwargs, None)


def x__check_title_mismatch__mutmut_orig(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_1(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = None
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_2(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(None, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_3(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, None)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_4(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_5(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, )
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_6(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is not None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_7(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = None
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_8(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos - len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_9(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = None

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_10(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end - _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_11(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(None):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_12(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = None
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_13(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_14(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_15(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_16(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            break

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_17(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) and _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_18(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(None) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_19(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(None):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_20(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            break

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_21(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = None
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_22(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(None, registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_23(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), None)
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_24(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_25(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), )
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_26(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.upper(), registry_title.lower())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_27(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.upper())
        if score < _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None


def x__check_title_mismatch__mutmut_28(
    law_id: str, snippet: str, registry_title: str
) -> str | None:
    """Return a WARN note if explicit title phrase within ±30 chars scores < 60."""
    pos = _find_id_pos_in_snippet(law_id, snippet)
    if pos is None:
        return None

    id_end = pos + len(law_id)
    # Search 30 chars after the ID end for a title phrase
    window = snippet[id_end: id_end + _TITLE_WINDOW]

    for match in _TITLE_PHRASE_RE.finditer(window):
        # Extract whichever capture group matched
        phrase = next(g for g in match.groups() if g is not None).strip()
        if not phrase:
            continue

        # Skip if phrase looks like a status keyword (handled by status check)
        if _STATUS_NON_NEG.match(phrase) or _STATUS_STRICT.match(phrase):
            continue

        score = fuzz.partial_ratio(phrase.lower(), registry_title.lower())
        if score <= _TITLE_SCORE_THRESHOLD:
            return (
                f"Title phrase score {score}/100 < {_TITLE_SCORE_THRESHOLD} threshold: "
                f"artifact says '{phrase}', registry title is '{registry_title}'"
            )

    return None

x__check_title_mismatch__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__check_title_mismatch__mutmut_1': x__check_title_mismatch__mutmut_1, 
    'x__check_title_mismatch__mutmut_2': x__check_title_mismatch__mutmut_2, 
    'x__check_title_mismatch__mutmut_3': x__check_title_mismatch__mutmut_3, 
    'x__check_title_mismatch__mutmut_4': x__check_title_mismatch__mutmut_4, 
    'x__check_title_mismatch__mutmut_5': x__check_title_mismatch__mutmut_5, 
    'x__check_title_mismatch__mutmut_6': x__check_title_mismatch__mutmut_6, 
    'x__check_title_mismatch__mutmut_7': x__check_title_mismatch__mutmut_7, 
    'x__check_title_mismatch__mutmut_8': x__check_title_mismatch__mutmut_8, 
    'x__check_title_mismatch__mutmut_9': x__check_title_mismatch__mutmut_9, 
    'x__check_title_mismatch__mutmut_10': x__check_title_mismatch__mutmut_10, 
    'x__check_title_mismatch__mutmut_11': x__check_title_mismatch__mutmut_11, 
    'x__check_title_mismatch__mutmut_12': x__check_title_mismatch__mutmut_12, 
    'x__check_title_mismatch__mutmut_13': x__check_title_mismatch__mutmut_13, 
    'x__check_title_mismatch__mutmut_14': x__check_title_mismatch__mutmut_14, 
    'x__check_title_mismatch__mutmut_15': x__check_title_mismatch__mutmut_15, 
    'x__check_title_mismatch__mutmut_16': x__check_title_mismatch__mutmut_16, 
    'x__check_title_mismatch__mutmut_17': x__check_title_mismatch__mutmut_17, 
    'x__check_title_mismatch__mutmut_18': x__check_title_mismatch__mutmut_18, 
    'x__check_title_mismatch__mutmut_19': x__check_title_mismatch__mutmut_19, 
    'x__check_title_mismatch__mutmut_20': x__check_title_mismatch__mutmut_20, 
    'x__check_title_mismatch__mutmut_21': x__check_title_mismatch__mutmut_21, 
    'x__check_title_mismatch__mutmut_22': x__check_title_mismatch__mutmut_22, 
    'x__check_title_mismatch__mutmut_23': x__check_title_mismatch__mutmut_23, 
    'x__check_title_mismatch__mutmut_24': x__check_title_mismatch__mutmut_24, 
    'x__check_title_mismatch__mutmut_25': x__check_title_mismatch__mutmut_25, 
    'x__check_title_mismatch__mutmut_26': x__check_title_mismatch__mutmut_26, 
    'x__check_title_mismatch__mutmut_27': x__check_title_mismatch__mutmut_27, 
    'x__check_title_mismatch__mutmut_28': x__check_title_mismatch__mutmut_28
}
x__check_title_mismatch__mutmut_orig.__name__ = 'x__check_title_mismatch'
