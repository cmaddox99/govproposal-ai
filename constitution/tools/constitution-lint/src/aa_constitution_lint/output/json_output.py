"""JSON output formatter - machine readable for CI/CD integration."""

import json

from aa_constitution_lint.domain.models import LintResult


class JsonFormatter:
    """Format LintResult as JSON for machine consumption (ENG-10.1 compliant)."""

    def format(self, result: LintResult) -> str:
        """
        Format lint result as JSON.

        Args:
            result: The LintResult to format.

        Returns:
            JSON string with ENG-10.1 compliant schema:
            {
                "evaluations": [...],
                "violations": [...],
                "summary": {...},
                "metadata": {...}
            }
        """
        output = {
            "evaluations": [
                {
                    "law_id": evaluation.law_id,
                    "result": evaluation.result.value,
                    "evaluation_point": evaluation.evaluation_point,
                    "timestamp": evaluation.timestamp.isoformat(),
                    "context": evaluation.context,
                }
                for evaluation in result.evaluations
            ],
            "violations": [
                {
                    "law_id": violation.law_id,
                    "severity": violation.severity.value,
                    "message": violation.message,
                }
                for violation in result.violations
            ],
            "summary": {
                "total": result.summary.total,
                "passed": result.summary.passed,
                "failed": result.summary.failed,
                "skipped": result.summary.skipped,
            },
            "metadata": result.metadata,
        }

        return json.dumps(output, indent=2)
