"""Diagnostic module — reports install state, source location, library versions.

Spec: hangar-ai-specs/changes/renderer-determinism-and-diagnose/PROPOSAL.md
Law:  ENG-13.1 (Artifact Rendering, NON-NEG), BUS-7.1 (Audit Trail, NON-NEG).

Single-shot CLI helper invoked via `aa-artifact-render --diagnose`.
Surfaces the kind of install drift that silently produces stale renders
(editable install bound to wrong checkout, multiple Python envs, etc.).
"""
from __future__ import annotations

import datetime as _dt
import shutil
import subprocess
import sys
from importlib.metadata import PackageNotFoundError, version as _pkg_version
from pathlib import Path
from typing import Any

_TRACKED_LIBS = ("click", "Jinja2", "markdown-it-py", "PyYAML", "playwright")


def _safe_version(name: str) -> str:
    try:
        return _pkg_version(name)
    except PackageNotFoundError:
        return "not installed"


def _git(repo_dir: Path, *args: str) -> str:
    if not (repo_dir / ".git").exists() and not _is_inside_git_worktree(repo_dir):
        return "not-a-git-repo"
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if out.returncode != 0:
            return "git-error"
        return out.stdout.strip() or "(empty)"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return "git-unavailable"


def _is_inside_git_worktree(p: Path) -> bool:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=p,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        return out.returncode == 0 and out.stdout.strip() == "true"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def collect() -> dict[str, Any]:
    """Collect a structured snapshot of the renderer install state."""
    pkg_version = _safe_version("aa-artifact-render")

    # Source location: the package __init__ tells us where this install loads from
    import aa_artifact_render as _self
    install_location = Path(_self.__file__).resolve().parent

    # Walk up to find the package root (where pyproject.toml lives)
    pkg_root = install_location
    for parent in [install_location, *install_location.parents]:
        if (parent / "pyproject.toml").exists():
            pkg_root = parent
            break

    git_sha = _git(pkg_root, "rev-parse", "--short", "HEAD")
    git_branch = _git(pkg_root, "rev-parse", "--abbrev-ref", "HEAD")
    git_status_raw = _git(pkg_root, "status", "--porcelain")
    git_status = "clean" if git_status_raw in ("", "(empty)") else "dirty"

    templates_dir = install_location / "templates"
    templates: list[str] = []
    if templates_dir.exists():
        templates = sorted(p.stem for p in templates_dir.glob("*.html"))

    libraries = {name: _safe_version(name) for name in _TRACKED_LIBS}

    cli_path = shutil.which("aa-artifact-render") or "(not on PATH)"

    drift: list[tuple[str, bool, str]] = []
    drift.append(
        (
            "install location is inside a git repo",
            git_sha not in ("not-a-git-repo", "git-error", "git-unavailable"),
            f"sha={git_sha}",
        )
    )
    drift.append(
        (
            "source git working tree clean",
            git_status == "clean",
            f"status={git_status}",
        )
    )
    drift.append(
        (
            "playwright installed (PDF available)",
            libraries["playwright"] != "not installed",
            f"playwright={libraries['playwright']}",
        )
    )

    return {
        "timestamp": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "package_version": pkg_version,
        "install_location": str(install_location),
        "package_root": str(pkg_root),
        "git_sha": git_sha,
        "git_branch": git_branch,
        "git_status": git_status,
        "cli_path": cli_path,
        "python_executable": sys.executable,
        "python_version": sys.version.split()[0],
        "templates_dir": str(templates_dir),
        "templates": templates,
        "libraries": libraries,
        "drift_checks": drift,
    }


def format_text(snapshot: dict[str, Any]) -> str:
    """Pretty-print the diagnostic snapshot for terminal display."""
    lines: list[str] = []
    lines.append(f"aa-artifact-render diagnostic — {snapshot['timestamp']}")
    lines.append("─" * 60)
    lines.append(f"Package version:                   {snapshot['package_version']}")
    lines.append(f"Install location:                  {snapshot['install_location']}")
    lines.append(f"Source git SHA (HEAD):             {snapshot['git_sha']}")
    lines.append(f"Source git branch:                 {snapshot['git_branch']}")
    lines.append(f"Source git status:                 {snapshot['git_status']}")
    lines.append(f"CLI executable:                    {snapshot['cli_path']}")
    lines.append(
        f"Python interpreter:                {snapshot['python_executable']}"
        f" ({snapshot['python_version']})"
    )
    lines.append(f"Templates dir:                     {snapshot['templates_dir']}")
    lines.append(
        f"Available templates ({len(snapshot['templates'])}): "
        f"{', '.join(snapshot['templates']) if snapshot['templates'] else '(none)'}"
    )
    lines.append("Library versions:")
    for name, ver in snapshot["libraries"].items():
        lines.append(f"  {name:<30} {ver}")
    lines.append("─" * 60)
    lines.append("Drift checks:")
    for desc, ok, detail in snapshot["drift_checks"]:
        marker = "✓" if ok else "⚠"
        lines.append(f"  {marker} {desc}  ({detail})")
    lines.append("─" * 60)
    return "\n".join(lines)


def has_drift(snapshot: dict[str, Any]) -> bool:
    """True if any non-warn-only drift check failed."""
    # Currently treat dirty git as a drift signal; missing playwright is a warning,
    # not a failure (PDF is optional). Adjust if policy changes.
    return snapshot["git_status"] == "dirty"
