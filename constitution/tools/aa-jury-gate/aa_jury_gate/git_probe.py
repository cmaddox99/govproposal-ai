"""Git probe: Protocol interface, production implementation, and test double.

Laws: ENG-2.5 (dependency inversion — GitProbe Protocol), ENG-2.1 (modular),
      ENG-6.1 (no shell=True subprocess)
Phase 4 §2.3 GitProbe design; Phase 4 §5.2 exception hierarchy.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Protocol

from aa_jury_gate.models import (
    GitBinaryNotFoundError,
    GitNotInRepoError,
    GitProbeError,
    GitStatus,
)


class GitProbe(Protocol):
    """Injectable interface for git state inspection (ENG-2.5)."""

    def check(self, path: Path) -> GitStatus: ...


class RealGitProbe:
    """Production implementation using subprocess git commands (no shell=True)."""

    def check(self, path: Path) -> GitStatus:
        """Return GitStatus.CLEAN or raise GitBinaryNotFoundError / GitProbeError.

        Steps per Phase 4 §2.3:
        1. Validate path.parent exists (avoids FileNotFoundError mis-attribution)
        2. git rev-parse --is-inside-work-tree  (repo membership)
        3. git ls-files --error-unmatch <path>  (tracked)
        4. git diff --name-only HEAD -- <path>  (no uncommitted changes)
        """
        if not path.parent.is_dir():
            raise GitProbeError(f"parent directory does not exist: {path.parent}")
        try:
            rev = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                capture_output=True,
                text=True,
                cwd=path.parent,
            )
        except FileNotFoundError:
            raise GitBinaryNotFoundError("git binary not found in PATH") from None

        if rev.returncode != 0:
            raise GitNotInRepoError(f"not a git repository: {path.parent}")

        ls = subprocess.run(
            ["git", "ls-files", "--error-unmatch", str(path)],
            capture_output=True,
            text=True,
            cwd=path.parent,
        )
        if ls.returncode != 0:
            raise GitProbeError(f"synthesis file not tracked by git: {path}")

        diff = subprocess.run(
            ["git", "diff", "--name-only", "HEAD", "--", str(path)],
            capture_output=True,
            text=True,
            cwd=path.parent,
        )
        if diff.returncode != 0:
            raise GitProbeError(f"git diff failed (possibly no HEAD commit): {path}")
        if diff.stdout.strip():
            raise GitProbeError(f"synthesis file has uncommitted changes: {path}")

        return GitStatus.CLEAN


class StubGitProbe:
    """In-process test double for unit testing without git subprocess.

    Configure with a status to return or an exception to raise.
    """

    def __init__(
        self,
        status: GitStatus = GitStatus.CLEAN,
        raises: Exception | None = None,
    ) -> None:
        self._status = status
        self._raises = raises

    def check(self, path: Path) -> GitStatus:
        if self._raises is not None:
            raise self._raises
        return self._status
