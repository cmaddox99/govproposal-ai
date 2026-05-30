"""Console output formatter - human readable."""

from aa_constitution_lint.domain.models import EvaluationResult, LintResult


class ConsoleFormatter:
    """Format LintResult for human-readable console output."""

    def format(self, result: LintResult) -> str:
        """
        Format lint result for console display.

        Args:
            result: The LintResult to format.

        Returns:
            Human-readable string output.
        """
        lines = []
        lines.append("AA Constitution Lint Results")
        lines.append("=" * 40)
        lines.append("")

        # Show each evaluation
        for evaluation in result.evaluations:
            if evaluation.result == EvaluationResult.PASS:
                status = "✓ PASS"
            elif evaluation.result == EvaluationResult.WARNING:
                status = "⚠ WARN"
            else:
                status = "✗ FAIL"
            message = evaluation.context.get("message", "")
            lines.append(f"{status} [{evaluation.law_id}] {message}")

        lines.append("")
        lines.append("-" * 40)

        # Show violations if any
        if result.violations:
            lines.append("Violations:")
            for violation in result.violations:
                lines.append(f"  • [{violation.law_id}] {violation.message}")
                if violation.file_path:
                    loc = f"    at {violation.file_path}"
                    if violation.line_number:
                        loc += f":{violation.line_number}"
                    lines.append(loc)
            lines.append("")

        # Summary
        summary_parts = [f"{result.summary.passed} passed"]
        if result.summary.warnings > 0:
            summary_parts.append(f"{result.summary.warnings} warnings")
        summary_parts.append(f"{result.summary.failed} failed")
        summary_parts.append(f"{result.summary.skipped} skipped")
        lines.append(f"Summary: {', '.join(summary_parts)}")

        return "\n".join(lines)
