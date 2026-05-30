"""Linter - orchestrates rule evaluation."""

from __future__ import annotations

import time
from pathlib import Path
from typing import TYPE_CHECKING

from aa_constitution_lint import __version__
from aa_constitution_lint.domain.models import (
    EvaluationResult,
    LintResult,
    Severity,
    Summary,
    Violation,
)
from aa_constitution_lint.domain.rules.base import Rule

if TYPE_CHECKING:
    from aa_constitution_lint.config import Config


class Linter:
    """Orchestrates constitution lint rules and aggregates results."""

    def __init__(self, rules: list[Rule], config: Config | None = None) -> None:
        """
        Initialize linter with rules and optional config.

        Args:
            rules: List of Rule instances to evaluate.
            config: Optional Config instance for rule enablement.
        """
        self._rules = rules
        self._config = config

    def lint(self, project_path: Path) -> LintResult:
        """
        Lint a project by running all rules.

        Args:
            project_path: Path to project root.

        Returns:
            LintResult with all evaluations, violations, and summary.
        """
        start_time = time.time()
        all_evaluations = []
        violations = []

        for rule in self._rules:
            # Skip disabled rules if config is provided
            if self._config is not None and not self._config.is_rule_enabled(rule.id):
                continue

            evaluations = rule.evaluate(project_path)
            all_evaluations.extend(evaluations)

            # Collect violations from failed evaluations
            for eval in evaluations:
                if eval.result == EvaluationResult.FAIL:
                    violations.append(
                        Violation(
                            law_id=eval.law_id,
                            severity=Severity.WARNING,  # Default severity
                            message=eval.context.get("message", f"Rule {rule.id} failed"),
                            file_path=eval.context.get("file_path"),
                            line_number=eval.context.get("line_number"),
                        )
                    )

        # Compute summary
        passed = sum(1 for e in all_evaluations if e.result == EvaluationResult.PASS)
        failed = sum(1 for e in all_evaluations if e.result == EvaluationResult.FAIL)
        warnings = sum(1 for e in all_evaluations if e.result == EvaluationResult.WARNING)
        skipped = sum(1 for e in all_evaluations if e.result == EvaluationResult.SKIP)

        duration_ms = int((time.time() - start_time) * 1000)

        return LintResult(
            evaluations=all_evaluations,
            violations=violations,
            summary=Summary(
                total=len(all_evaluations),
                passed=passed,
                failed=failed,
                warnings=warnings,
                skipped=skipped,
            ),
            metadata={
                "version": __version__,
                "duration_ms": duration_ms,
            },
        )
