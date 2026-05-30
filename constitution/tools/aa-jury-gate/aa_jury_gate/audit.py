"""
Audit logging for aa-jury-gate (BUS-7.1).

Logs gate invocations to JSON Lines format for audit trail compliance.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from aa_jury_gate.models import GateVerdict


def write_audit_log(
    log_dir: Path,
    synthesis_path: Path,
    verdict: GateVerdict,
    checks_failed: int,
    checks_skipped: int,
    content_sha256: str,
    tool_version: str,
    exit_code: int,
) -> None:
    """
    Write audit log entry to JSON Lines file.

    Args:
        log_dir: Directory for audit logs
        synthesis_path: Path to synthesis file that was validated
        verdict: Gate verdict (PASS or FAIL)
        checks_failed: Number of checks that failed
        checks_skipped: Number of checks that were skipped
        content_sha256: SHA256 of synthesis content (before jury_gate block)
        tool_version: aa-jury-gate version string
        exit_code: Exit code (0=PASS, 1=FAIL, 2=ERROR)

    The log entry is appended to {log_dir}/aa-jury-gate.jsonl in JSON Lines format.
    Each line is a complete JSON object for easy parsing by log aggregation systems.
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "aa-jury-gate.jsonl"

    entry = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "synthesis_path": str(synthesis_path.resolve()),
        "verdict": verdict.value,
        "checks_failed": checks_failed,
        "checks_skipped": checks_skipped,
        "content_sha256": content_sha256,
        "tool": "aa-jury-gate",
        "version": tool_version,
        "exit_code": exit_code,
    }

    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
