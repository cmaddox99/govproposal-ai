"""Repo-level opt-out configuration for aa-agents-sync (FIX-13)."""
from __future__ import annotations

from pathlib import Path


def is_sync_disabled(agents_md_path: Path) -> bool:
    """Return True if an agents-sync.yml at the repo root contains ``disabled: true``.

    Searches upward from *agents_md_path* for agents-sync.yml, stopping at:
    - A directory containing ``.git`` (repository boundary)
    - The filesystem root

    This prevents inheriting a parent repository's opt-out in monorepos or
    nested repo scenarios. The search is intentionally lightweight: it does
    a plain string search rather than a full YAML parse to avoid introducing
    a new dependency.
    """
    current = Path(agents_md_path).resolve().parent
    while True:
        config_file = current / "agents-sync.yml"
        if config_file.exists():
            content = config_file.read_text()
            if "disabled: true" in content:
                return True
            return False  # file exists but not disabled
        # R2-1: Stop at .git boundary to avoid inheriting parent repo opt-out
        if (current / ".git").exists():
            break
        parent = current.parent
        if parent == current:
            break
        current = parent
    return False
