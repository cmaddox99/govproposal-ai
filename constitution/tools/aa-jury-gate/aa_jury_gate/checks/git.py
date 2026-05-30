"""Git check G01: synthesis file committed with no uncommitted changes.

Laws: ENG-2.1 (modular), ENG-2.5 (dependency inversion via GitProbe Protocol)
Phase 3 §1.6 allow-no-git matrix; Phase 4 §5.2 exception routing.

SKIP logic (infrastructure-unavailable only):
- GitBinaryNotFoundError + allow_no_git=True  → SKIP (git not installed)
- GitBinaryNotFoundError + allow_no_git=False → re-raise (exit 2 via ToolError)
- GitNotInRepoError      + allow_no_git=True  → SKIP (path not in a repo)
- GitNotInRepoError      + allow_no_git=False → FAIL with probe error message

File-integrity errors always FAIL regardless of allow_no_git (Phase 3 §1.6):
- GitProbeError (untracked / uncommitted / diff failed) → FAIL in all cases
"""
from __future__ import annotations

from pathlib import Path

from aa_jury_gate.git_probe import GitProbe
from aa_jury_gate.models import (
    CheckItem,
    CheckResult,
    GitBinaryNotFoundError,
    GitNotInRepoError,
    GitProbeError,
    GitStatus,
)


def check_g01(probe: GitProbe, path: Path, *, allow_no_git: bool) -> CheckItem:
    """G01 — synthesis file is tracked by git with no uncommitted changes."""
    try:
        status = probe.check(path)
    except GitBinaryNotFoundError:
        if allow_no_git:
            return CheckItem("G01", CheckResult.SKIP, "")
        raise
    except GitNotInRepoError as exc:
        if allow_no_git:
            return CheckItem("G01", CheckResult.SKIP, "")
        return CheckItem("G01", CheckResult.FAIL, str(exc))
    except GitProbeError as exc:
        # File-integrity errors (untracked, uncommitted, diff failure) always FAIL
        # regardless of allow_no_git — Phase 3 §1.6
        return CheckItem("G01", CheckResult.FAIL, str(exc))

    if status == GitStatus.CLEAN:
        return CheckItem("G01", CheckResult.PASS, "")
    # UNTRACKED or UNCOMMITTED returned directly by stub (not raised)
    detail = (
        "synthesis file not tracked by git"
        if status == GitStatus.UNTRACKED
        else "synthesis file has uncommitted changes"
    )
    return CheckItem("G01", CheckResult.FAIL, detail)
