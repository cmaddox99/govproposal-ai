"""security.py — Path validation for aa-jury-gate (ENG-6.1, ENG-6.5).

Validates the synthesis path and optional log directory before any I/O.
All violations raise ToolError (→ exit 2). No exceptions escape this module.
"""

from __future__ import annotations

import os
from pathlib import Path

from aa_jury_gate.models import ToolError

_MAX_SYNTHESIS_BYTES: int = 1_048_576  # 1 MiB (Phase 4 §2.2)


def validate_synthesis_path(path: Path) -> Path:
    """Validate the synthesis file path before any YAML parsing.

    Validation sequence (Phase 4 §2.2):
      1. path.exists()      → ToolError "synthesis file not found: <path>"
      2. path.is_file()     → ToolError "synthesis path is a directory: <path>"
      3. path.is_symlink()  → ToolError "synthesis path is a symlink: <path>"
      4. size ≤ 1 MiB       → ToolError "synthesis file too large (max 1MB): <path>"

    Symlink is checked before size so a symlink to a large file fails with the
    correct (symlink) error rather than the size error.

    Returns the validated path unchanged on success.
    Raises ToolError on any violation (→ exit 2).
    """
    if not path.exists():
        raise ToolError(f"synthesis file not found: {path}")
    if not path.is_file():
        raise ToolError(f"synthesis path is a directory: {path}")
    if path.is_symlink():
        raise ToolError(f"synthesis path is a symlink: {path}")
    if path.stat().st_size > _MAX_SYNTHESIS_BYTES:
        raise ToolError(f"synthesis file too large (max 1MB): {path}")
    return path


def validate_log_dir(log_dir: str | None) -> Path:
    """Validate and resolve the log directory path.

    If `log_dir` is None (Click default), returns ``~/.aa-jury-gate/`` with no
    CWD-boundary check (C-P5-J2-R2-003).

    If `log_dir` is a caller-supplied string:
      1. Expand ``~`` via Path.expanduser()
      2. Resolve symlinks via os.path.realpath()
      3. Verify resolved path starts with CWD — raises ToolError on escape

    Returns the resolved absolute Path on success.
    Raises ToolError if the resolved path escapes the current working directory.
    """
    if log_dir is None:
        return Path("~/.aa-jury-gate/").expanduser()

    expanded = Path(log_dir).expanduser()
    resolved = Path(os.path.realpath(expanded))
    cwd = Path(os.path.realpath(os.getcwd()))

    try:
        resolved.relative_to(cwd)
    except ValueError:
        raise ToolError(
            f"--log-dir path escapes working directory boundary: {resolved}"
        ) from None
    return resolved
