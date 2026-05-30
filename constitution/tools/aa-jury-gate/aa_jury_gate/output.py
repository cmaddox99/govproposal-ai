"""Output writer for gate results."""
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

from aa_jury_gate import __version__
from aa_jury_gate.models import GateResult, GateVerdict, CheckResult


def append_gate_result(path: Path, result: GateResult) -> None:
    """Append jury_gate: block to synthesis file frontmatter atomically.

    Only writes on PASS/FAIL verdicts (exit 0/1). ERROR (exit 2) does NOT write (ADR-003).

    Atomic write via tempfile in path.parent + os.replace() (Phase 3 §4).
    Idempotent: overwrites existing jury_gate: block if present.
    """
    if result.verdict == GateVerdict.ERROR:
        # Never write on ERROR (ADR-003, BDD-F05)
        return

    content = path.read_text(encoding="utf-8")

    # Split frontmatter from body
    if not content.startswith("---\n"):
        msg = f"synthesis file missing frontmatter delimiter: {path}"
        raise ValueError(msg)

    parts = content.split("\n---\n", 1)
    if len(parts) != 2:  # noqa: PLR2004
        msg = f"synthesis file missing closing frontmatter delimiter: {path}"
        raise ValueError(msg)

    fm_text, body_text = parts

    # Parse existing frontmatter
    fm = yaml.safe_load(fm_text[4:])  # skip opening "---\n"
    if fm is None:
        fm = {}

    # Build jury_gate block (Phase 3 §5.1)
    checks_failed = sum(1 for c in result.checks if c.result == CheckResult.FAIL)
    checks_skipped = sum(1 for c in result.checks if c.result == CheckResult.SKIP)

    jury_block = {
        "tool": "aa-jury-gate",
        "version": __version__,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "verdict": result.verdict.value,
        "content_sha256": result.content_sha256,
        "checks_failed": checks_failed,
        "checks_skipped": checks_skipped,
        "checks": [
            {
                "check_id": c.check_id,
                "result": c.result.value,
                "detail": c.detail,
            }
            for c in result.checks
        ],
    }

    # Overwrite existing jury_gate: key (idempotent)
    fm["jury_gate"] = jury_block

    # Reconstruct frontmatter + body
    new_fm_text = yaml.dump(fm, default_flow_style=False, sort_keys=False)
    new_content = f"---\n{new_fm_text}---\n{body_text}"

    # Atomic write: tempfile in same dir + os.replace()
    fd, temp_path = tempfile.mkstemp(dir=path.parent, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(new_content)
        os.replace(temp_path, path)
    except Exception:
        # Clean up temp file on error
        try:
            os.unlink(temp_path)
        except FileNotFoundError:
            pass
        raise
