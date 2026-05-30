"""Data models for aa-citation-audit.

Authoritative source: Phase 3 §2.2 (APPROVED v1.1.0).
DO NOT add SKIP to Verdict — draft IDs go to AuditResult.draft_skipped.
DO NOT add skip_count or pass_rate to AuditResult — use @property.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


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
