"""Drift checker for aa-agents-sync."""
from pathlib import Path
from .models import CheckResult
from .parser import parse_markers


def _semver_tuple(v: str) -> tuple[int, int, int]:
    """Parse 'X.Y.Z' into a comparable tuple. Non-semver returns (0,0,0)."""
    try:
        parts = v.strip().split(".")
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    except (ValueError, IndexError):
        return (0, 0, 0)


def check_drift(agents_md_path: Path, constitution_path: Path) -> CheckResult:
    """Check whether the AGENTS.md markers are current with constitution-version.txt.

    Returns a CheckResult with has_drift=False if all marker versions match,
    has_drift=True if any are stale, or errors populated on structural failures.
    """
    agents_md_path = Path(agents_md_path)
    constitution_path = Path(constitution_path)

    errors: list[str] = []

    # Read constitution version
    version_file = constitution_path / "constitution-version.txt"
    if not version_file.exists():
        return CheckResult(
            errors=[f"constitution-version.txt not found at {version_file}"]
        )
    constitution_version = version_file.read_text().strip()

    # Read and parse AGENTS.md
    if not agents_md_path.exists():
        return CheckResult(
            errors=[f"AGENTS.md not found at {agents_md_path}"]
        )
    content = agents_md_path.read_text()
    sections, parse_errors = parse_markers(content)
    errors.extend(parse_errors)

    if errors:
        return CheckResult(errors=errors, constitution_version=constitution_version)

    # nm-chk-01: no markers present is a drift state — any([]) == False is the root bug
    has_drift = (not sections) or any(s.version != constitution_version for s in sections)

    # FIX-4: downgrade guard — reject if constitution is older than any existing marker
    const_tuple = _semver_tuple(constitution_version)
    for section in sections:
        sec_tuple = _semver_tuple(section.version)
        if const_tuple < sec_tuple:
            return CheckResult(
                sections=sections,
                constitution_version=constitution_version,
                errors=[
                    f"Downgrade rejected: constitution v{constitution_version} is older "
                    f"than existing marker v{section.version} for '{section.name}'. "
                    "Sync a newer constitution or use --check to inspect."
                ],
            )

    return CheckResult(
        sections=sections,
        constitution_version=constitution_version,
        has_drift=has_drift,
        has_markers=bool(sections),
    )
