"""Git utilities for aa-agents-sync."""
from __future__ import annotations

import subprocess
from pathlib import Path


def is_git_dirty(path: Path) -> bool | None:
    """Return True if the git repo containing path has uncommitted changes.

    Returns None if path is not inside a git repository.
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=path if path.is_dir() else path.parent,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return None
        return bool(result.stdout.strip())
    except FileNotFoundError:
        return None
