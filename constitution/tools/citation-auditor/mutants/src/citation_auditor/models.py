"""Data models for aa-citation-audit.

Authoritative source: Phase 3 §2.2 (APPROVED v1.1.0).
DO NOT add SKIP to Verdict — draft IDs go to AuditResult.draft_skipped.
DO NOT add skip_count or pass_rate to AuditResult — use @property.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
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


class Verdict(Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    # Draft IDs are NOT added to results as CitationResult entries.
    # They are tracked in AuditResult.draft_skipped (list[str]).


@dataclass
class CitationResult:
    law_id: str
    verdict: Verdict
    note: str | None            # human-readable reason for WARN/FAIL; None for PASS
    context_snippet: str | None  # ±150 chars from match_start in stripped body; None for PASS


@dataclass
class AuditResult:
    artifact_path: str
    registry_path: str
    law_count: int              # total laws in registry
    scanned: int                # unique IDs found in stripped body
    results: list[CitationResult]  # sorted: FAIL→WARN→PASS, then alpha within tier
    draft_skipped: list[str]    # IDs skipped due to --allow-draft
    allow_draft: list[str]
    strict: bool
    timestamp: str              # YYYY-MM-DDTHH:MM:SSZ
    tool_version: str

    @property
    def fail_count(self) -> int:
        return sum(1 for r in self.results if r.verdict == Verdict.FAIL)

    @property
    def warn_count(self) -> int:
        return sum(1 for r in self.results if r.verdict == Verdict.WARN)

    @property
    def pass_count(self) -> int:
        return sum(1 for r in self.results if r.verdict == Verdict.PASS)

    @property
    def audit_exit_code(self) -> int:
        """Returns 0 or 1 only. Exit 2 is cli.py's responsibility."""
        if self.fail_count > 0:
            return 1
        if self.strict and self.warn_count > 0:
            return 1
        return 0
