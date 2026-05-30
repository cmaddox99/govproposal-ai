"""Safe-mode syncer for aa-agents-sync — replaces stale bounded sections atomically."""
from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from .checker import check_drift, _semver_tuple
from .models import CheckResult
from .parser import parse_markers, BEGIN_RE, END_RE


@dataclass
class SyncResult:
    """Result of a sync_agents_md call."""

    sections_updated: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    was_insertion: bool = False  # nm-cli-04: True when sections were inserted (no prior markers)
    pin_written: bool = False  # r1: True when constitution-version.txt was created/updated

    @property
    def has_changes(self) -> bool:
        return bool(self.sections_updated)


def _load_canonical_sections(constitution_path: Path) -> dict[str, str]:
    """Load canonical section content from templates/agents-md-sections/*.md.

    Returns a dict mapping section name → full bounded content (BEGIN…END).
    Raises ValueError if any template file contains malformed markers.
    """
    templates_dir = constitution_path / "templates" / "agents-md-sections"
    if not templates_dir.is_dir():
        return {}

    canonical: dict[str, str] = {}
    for md_file in templates_dir.glob("*.md"):
        content = md_file.read_text()
        sections, errors = parse_markers(content)
        if errors:
            raise ValueError(
                f"Malformed template '{md_file.name}': {'; '.join(errors)}"
            )
        for section in sections:
            canonical[section.name] = section.content
    return canonical


def _replace_section_in_content(content: str, name: str, new_section_content: str) -> str:
    """Replace a bounded section in content with new_section_content.

    new_section_content is the full bounded block including BEGIN/END markers.
    """
    lines = content.splitlines(keepends=True)
    result: list[str] = []
    inside = False

    for line in lines:
        begin_match = BEGIN_RE.search(line)
        end_match = END_RE.search(line)

        if begin_match and begin_match.group(1) == name:
            inside = True
            # Inject new content in place of the old block
            result.append(new_section_content)
            continue
        elif end_match and end_match.group(1) == name and inside:
            inside = False
            continue

        if not inside:
            result.append(line)

    return "".join(result)


def _insert_sections_at_eof(content: str, canonical: dict[str, str]) -> tuple[str, list[str]]:
    """Append canonical section blocks to content (first-time injection).

    Ensures a blank line separator before each injected block.
    Returns (new_content, list_of_inserted_section_names).
    """
    inserted: list[str] = []
    result = content
    # Ensure file ends with a newline before appending
    if result and not result.endswith("\n"):
        result += "\n"
    for name, block in canonical.items():
        result += "\n" + block
        inserted.append(name)
    return result, inserted


def _atomic_write(path: Path, content: str) -> None:
    """Write content to path atomically using temp file → fsync → rename.

    Acquires exclusive non-blocking flock on the target before writing.
    Raises BlockingIOError if the file is locked by another process.
    """
    import fcntl
    parent = path.parent
    # Acquire exclusive lock on target before touching it
    with open(path, "r") as lock_fh:
        try:
            fcntl.flock(lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise BlockingIOError(
                f"Cannot acquire exclusive lock on {path}: "
                "file is locked by another process"
            )
        fd, tmp_path = tempfile.mkstemp(dir=parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(content)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, path)
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise
        finally:
            fcntl.flock(lock_fh, fcntl.LOCK_UN)


def sync_agents_md(
    agents_md_path: Path,
    constitution_path: Path,
) -> SyncResult:
    """Sync stale bounded sections in AGENTS.md from canonical templates.

    For files with existing markers: replaces stale sections in-place.
    For files with no markers (first-time injection): appends all canonical
    sections at end of file.

    Returns SyncResult with sections_updated listing which sections were replaced
    or inserted. Errors are populated if structural issues are found.
    """
    agents_md_path = Path(agents_md_path)
    constitution_path = Path(constitution_path)

    check = check_drift(agents_md_path=agents_md_path, constitution_path=constitution_path)

    if check.errors:
        return SyncResult(errors=check.errors)

    if not check.has_drift:
        try:
            pin_err = _write_version_pin(agents_md_path, check.constitution_version)
        except OSError as e:
            pin_err = str(e)
        if pin_err:
            return SyncResult(errors=[pin_err])
        return SyncResult(pin_written=True)

    canonical = _load_canonical_sections(constitution_path)
    if not canonical:
        return SyncResult(errors=["No canonical sections found in templates/agents-md-sections/"])

    content = agents_md_path.read_text()

    # nm-syn-01: no markers present — first-time injection path
    if not check.has_markers:
        new_content, inserted = _insert_sections_at_eof(content, canonical)
        if not inserted:
            return SyncResult(errors=["No canonical sections available to insert."])
        bak_path = agents_md_path.with_suffix(agents_md_path.suffix + ".bak")
        bak_path.write_text(content)
        try:
            _atomic_write(agents_md_path, new_content)
        except BlockingIOError as e:
            return SyncResult(errors=[str(e)])
        written_content = agents_md_path.read_text()
        _, verify_errors = parse_markers(written_content)
        if verify_errors:
            agents_md_path.write_text(bak_path.read_text())
            return SyncResult(
                errors=[
                    f"Post-write verification failed after insertion: {'; '.join(verify_errors)}. "
                    "AGENTS.md restored from backup."
                ]
            )
        bak_path.unlink(missing_ok=True)
        try:
            pin_err = _write_version_pin(agents_md_path, check.constitution_version)
        except OSError as e:
            pin_err = str(e)
        if pin_err:
            return SyncResult(errors=[pin_err])
        return SyncResult(sections_updated=inserted, was_insertion=True, pin_written=True)

    sections_updated: list[str] = []

    for section in check.sections:
        if section.version == check.constitution_version:
            continue
        if section.name not in canonical:
            return SyncResult(
                errors=[f"No canonical template found for section '{section.name}'"]
            )
        # FIX-10: per-section rollback guard — template must not be older than existing marker
        tmpl_sections, _ = parse_markers(canonical[section.name])
        if tmpl_sections:
            tmpl_version = tmpl_sections[0].version
            if _semver_tuple(tmpl_version) < _semver_tuple(section.version):
                return SyncResult(
                    errors=[
                        f"Version rollback rejected: template v{tmpl_version} is older "
                        f"than existing marker v{section.version} for '{section.name}'."
                    ]
                )
        content = _replace_section_in_content(content, section.name, canonical[section.name])
        sections_updated.append(section.name)

    # FIX-11: idempotency guard — skip write if computed content is identical to current file
    if content == agents_md_path.read_text():
        return SyncResult()

    # FIX-6: create backup before atomic write
    bak_path = agents_md_path.with_suffix(agents_md_path.suffix + ".bak")
    bak_path.write_text(agents_md_path.read_text())

    try:
        _atomic_write(agents_md_path, content)
    except BlockingIOError as e:
        return SyncResult(errors=[str(e)])

    # FIX-7: post-write verification — re-parse; auto-restore from .bak on error
    written_content = agents_md_path.read_text()
    _, verify_errors = parse_markers(written_content)
    if verify_errors:
        agents_md_path.write_text(bak_path.read_text())
        return SyncResult(
            errors=[
                f"Post-write verification failed: {'; '.join(verify_errors)}. "
                "AGENTS.md restored from backup."
            ]
        )
    bak_path.unlink(missing_ok=True)
    try:
        pin_err = _write_version_pin(agents_md_path, check.constitution_version)
    except OSError as e:
        pin_err = str(e)
    if pin_err:
        return SyncResult(errors=[pin_err])
    return SyncResult(sections_updated=sections_updated, pin_written=True)


def _write_version_pin(agents_md_path: Path, constitution_version: str) -> str | None:
    """Write constitution-version.txt alongside AGENTS.md in the target repo.

    Enables A01 lint rule to resolve the pinned version in CI without --constitution
    or AA_CONSTITUTION_PATH. Called after every successful sync_agents_md write.

    Returns an error string on failure, None on success.
    """
    pin_path = agents_md_path.parent / "constitution-version.txt"
    try:
        pin_path.write_text(f"{constitution_version}\n")
    except OSError as e:
        return f"Failed to write constitution-version.txt: {e}"
    return None
