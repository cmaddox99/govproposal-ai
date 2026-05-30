"""
Domain models for aa-constitution-lint.

These models define the core data structures used throughout the linter.
Output schema complies with ENG-10.1 (Constitution Metrics Collection Law).
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel


class EvaluationResult(str, Enum):
    """Result of evaluating a law."""

    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    SKIP = "skip"


class Severity(str, Enum):
    """Severity level of a violation."""

    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class LawEvaluation(BaseModel):
    """
    Single law evaluation result (ENG-10.1 compliant).

    Attributes:
        law_id: The law being evaluated (e.g., "ENG-4.1")
        result: pass/fail/skip
        evaluation_point: Where evaluation occurred (e.g., "aa-constitution-lint")
        timestamp: When evaluation occurred (ISO 8601)
        context: Additional context (file_path, rule, etc.)
    """

    law_id: str
    result: EvaluationResult
    evaluation_point: str
    timestamp: datetime
    context: dict[str, Any]


class Violation(BaseModel):
    """
    Violation details when evaluation result is FAIL.

    Attributes:
        law_id: The violated law
        severity: critical/warning/info
        message: Human-readable description
        file_path: Optional file where violation occurred
        line_number: Optional line number
    """

    law_id: str
    severity: Severity
    message: str
    file_path: str | None = None
    line_number: int | None = None


class Summary(BaseModel):
    """Aggregated evaluation counts."""

    total: int
    passed: int
    failed: int
    warnings: int = 0
    skipped: int


class LintResult(BaseModel):
    """
    Complete lint output (ENG-10.1 schema compliant).

    Attributes:
        evaluations: List of law evaluations
        violations: List of violation details
        summary: Aggregated counts
        metadata: Version, duration, etc.
    """

    evaluations: list[LawEvaluation]
    violations: list[Violation]
    summary: Summary
    metadata: dict[str, Any]

    def has_failures(self) -> bool:
        """Return True if any evaluations failed."""
        return self.summary.failed > 0
