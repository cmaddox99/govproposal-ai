"""Constitution path resolver for aa-agents-sync.

Resolution order (per approved proposal C2):
1. Explicit --constitution-path CLI flag
2. HANGAR_CONSTITUTION_PATH environment variable
3. Sibling directory named 'hangar-ai-constitution' relative to project root
   (derived from the AGENTS.md file path, not CWD)
4. Returns None (caller must abort with error)
"""
from __future__ import annotations

import os
from pathlib import Path


def resolve_constitution_path(
    explicit: str | None = None,
    agents_md_path: Path | None = None,
) -> Path | None:
    """Resolve the hangar-ai-constitution root directory.

    Resolution order:
    1. explicit CLI flag
    2. HANGAR_CONSTITUTION_PATH env var
    3. Sibling dir relative to agents_md_path's parent (project root)
    4. Returns None
    """
    # 1. Explicit flag
    if explicit is not None:
        candidate = Path(explicit)
        if candidate.is_dir():
            return candidate
        return None

    # 2. Environment variable
    env_val = os.environ.get("HANGAR_CONSTITUTION_PATH")
    if env_val:
        candidate = Path(env_val)
        if candidate.is_dir():
            return candidate
        return None

    # 3. Sibling directory relative to project root (AGENTS.md parent)
    project_root = (
        Path(agents_md_path).parent if agents_md_path is not None else Path.cwd()
    )
    sibling = project_root.parent / "hangar-ai-constitution"
    if sibling.is_dir():
        return sibling

    # 4. Installed package data (pip-installed aa-agents-sync)
    try:
        import importlib.resources as pkg_resources  # noqa: PLC0415
        package_data = pkg_resources.files("aa_agents_sync")
        candidate = Path(str(package_data)).parent.parent / "hangar-ai-constitution"
        if candidate.is_dir():
            return candidate
    except Exception:  # noqa: BLE001
        pass

    return None


def validate_constitution_path(path: Path) -> str | None:
    """Validate that path looks like a real hangar-ai-constitution root.

    Returns None if valid, or an error string describing the problem.
    A valid constitution must have constitution-version.txt AND at least one
    .md template under templates/agents-md-sections/.
    """
    path = Path(path)
    if not (path / "constitution-version.txt").exists():
        return (
            f"constitution-version.txt not found in '{path}'. "
            "This may not be a hangar-ai-constitution directory."
        )
    templates_dir = path / "templates" / "agents-md-sections"
    if not templates_dir.is_dir() or not any(templates_dir.glob("*.md")):
        return (
            f"No section templates found in '{templates_dir}'. "
            "This may not be a valid hangar-ai-constitution directory."
        )
    return None
