"""CLI entrypoint for aa-agents-sync."""
from __future__ import annotations

import difflib
import os
import sys
from pathlib import Path

import click

from aa_agents_sync import __version__
from aa_agents_sync.checker import check_drift
from aa_agents_sync.git_utils import is_git_dirty
from aa_agents_sync.legacy_detector import detect_legacy
from aa_agents_sync.config import is_sync_disabled
from aa_agents_sync.resolver import resolve_constitution_path, validate_constitution_path
from aa_agents_sync.syncer import _load_canonical_sections, _replace_section_in_content, _insert_sections_at_eof, sync_agents_md


@click.command()
@click.version_option(__version__, prog_name="aa-agents-sync")
@click.argument("agents_md", type=click.Path(exists=False))
@click.option("--constitution-path", type=click.Path(), default=None,
              help="Path to hangar-ai-constitution root.")
@click.option("--dry-run", is_flag=True, default=False,
              help="Show diff without writing (same as the safe default; use --apply to write).")
@click.option("--check", is_flag=True, default=False,
              help="Detect drift only; exit 2 if drift found.")
@click.option("--apply", is_flag=True, default=False,
              help="Write changes to AGENTS.md. Required to make any modifications.")
@click.option("--force", is_flag=True, default=False,
              help="Write even if git working tree is dirty (only meaningful with --apply).")
@click.option("--legacy-mode", is_flag=True, default=False,
              help="Detect and migrate legacy AGENTS.md (requires --dry-run).")
def main(
    agents_md: str,
    constitution_path: str | None,
    dry_run: bool,
    check: bool,
    apply: bool,
    force: bool,
    legacy_mode: bool,
) -> None:
    """Sync AGENTS.md canonical sections with hangar-ai-constitution."""
    # FIX-14: process-level kill-switch — checked before any I/O
    # R2-2: Allow --check mode through even when disabled, since it's read-only
    # and CI operators need accurate drift detection regardless of write-disable
    if os.environ.get("AGENTS_SYNC_DISABLED") == "1" and not check:
        click.echo("OK: AGENTS_SYNC_DISABLED=1 — sync is disabled by environment variable.")
        sys.exit(0)
    resolved = resolve_constitution_path(
        explicit=constitution_path,
        agents_md_path=Path(agents_md),
    )
    if resolved is None:
        click.echo("ERROR: Cannot resolve constitution path.", err=True)
        sys.exit(1)

    # FIX-9: integrity check only for modes that load templates
    if not check and not legacy_mode and apply:
        integrity_error = validate_constitution_path(resolved)
        if integrity_error:
            click.echo(f"ERROR: {integrity_error}", err=True)
            sys.exit(1)

    if check:
        result = check_drift(agents_md_path=Path(agents_md), constitution_path=resolved)
        if result.errors:
            for err in result.errors:
                click.echo(f"ERROR: {err}", err=True)
            sys.exit(1)
        if result.has_drift:
            if not result.has_markers:
                click.echo(
                    f"MISSING: AGENTS.md has no constitution markers. "
                    f"Run: aa-agents-sync --apply AGENTS.md "
                    f"to insert canonical sections (constitution v{result.constitution_version})"
                )
            else:
                click.echo(
                    f"DRIFT: {len(result.sections)} section(s) behind "
                    f"constitution v{result.constitution_version}"
                )
                for section in result.sections:
                    if section.version != result.constitution_version:
                        click.echo(
                            f"  - {section.name}: v{section.version} → "
                            f"v{result.constitution_version}"
                        )
            sys.exit(2)
        click.echo(f"OK: AGENTS.md is current with constitution v{result.constitution_version}")
        sys.exit(0)

    if legacy_mode:
        if not dry_run:
            click.echo("ERROR: --legacy-mode requires --dry-run.", err=True)
            sys.exit(1)
        result = detect_legacy(agents_md_path=Path(agents_md), constitution_path=resolved)
        if result.errors:
            for err in result.errors:
                click.echo(f"ERROR: {err}", err=True)
            sys.exit(1)
        if result.has_legacy:
            click.echo("LEGACY: Unversioned protocol block detected. Migration diff:")
            click.echo(result.diff)
            sys.exit(0)  # 0 = legacy found (pattern detected, diff shown)
        click.echo(
            "WARN: No legacy protocol block found.\n"
            "This file has no markers and no detectable legacy block.\n"
            "To auto-insert canonical sections, run:\n"
            f"  aa-agents-sync --apply --constitution-path {resolved} AGENTS.md"
        )
        sys.exit(2)  # 2 = pattern NOT detected

    # Safe mode (default) — show diff unless --apply is passed
    if not apply:
        dry_run = True  # treat no-apply as dry-run

    # FIX-13: repo-level opt-out via agents-sync.yml
    if apply and is_sync_disabled(Path(agents_md)):
        click.echo("OK: agents-sync.yml opt-out is active — sync disabled for this repo.")
        sys.exit(0)

    if not dry_run and apply:
        # PS-1: non-git guard is ALWAYS enforced in write mode — --force does not bypass it.
        # --force only suppresses the dirty-working-tree check.
        dirty = is_git_dirty(Path(agents_md))
        if dirty is None:
            click.echo(
                "ERROR: Not inside a git repository. "
                "aa-agents-sync write mode requires a git working tree. "
                "Use --dry-run or --check for read-only operations.",
                err=True,
            )
            sys.exit(1)
        if not force and dirty is True:  # C-8: --force bypasses dirty-tree only
            click.echo(
                "ERROR: Git working tree is dirty. Commit or stash changes first, "
                "or use --force to bypass.",
                err=True,
            )
            sys.exit(1)

    if dry_run:
        # C-9: show unified diff of what would change without writing
        drift = check_drift(agents_md_path=Path(agents_md), constitution_path=resolved)
        if drift.errors:
            for err in drift.errors:
                click.echo(f"ERROR: {err}", err=True)
            sys.exit(1)
        if not drift.has_drift:
            click.echo("DRY-RUN: AGENTS.md is already current. No changes needed.")
            sys.exit(0)
        try:
            canonical = _load_canonical_sections(resolved)
        except ValueError as e:
            click.echo(f"ERROR: {e}", err=True)
            sys.exit(1)
        current_text = Path(agents_md).read_text()
        new_text = current_text

        # nm-dry-01: no markers — show insertion diff
        if not drift.has_markers:
            new_text, inserted_names = _insert_sections_at_eof(new_text, canonical)
            diff_lines = list(difflib.unified_diff(
                current_text.splitlines(keepends=True),
                new_text.splitlines(keepends=True),
                fromfile=f"{agents_md} (current)",
                tofile=f"{agents_md} (after inserting v{drift.constitution_version} sections)",
            ))
            click.echo(f"DRY-RUN: {len(inserted_names)} section(s) would be inserted:")
            click.echo("".join(diff_lines))
            sys.exit(0)

        for section in drift.sections:
            if section.version != drift.constitution_version:
                if section.name not in canonical:
                    click.echo(f"ERROR: No canonical template for section '{section.name}'", err=True)
                    sys.exit(1)
                new_text = _replace_section_in_content(new_text, section.name, canonical[section.name])
        diff_lines = list(difflib.unified_diff(
            current_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile=f"{agents_md} (current)",
            tofile=f"{agents_md} (after sync to v{drift.constitution_version})",
        ))
        click.echo(f"DRY-RUN: {len(drift.sections)} section(s) would be updated:")
        click.echo("".join(diff_lines))
        sys.exit(0)

    try:
        result = sync_agents_md(agents_md_path=Path(agents_md), constitution_path=resolved)
    except ValueError as e:
        click.echo(f"ERROR: {e}", err=True)
        sys.exit(1)
    if result.errors:
        for err in result.errors:
            click.echo(f"ERROR: {err}", err=True)
        sys.exit(1)

    if result.has_changes:
        if result.was_insertion:
            click.echo(f"SYNCED: Inserted {len(result.sections_updated)} canonical section(s):")
        else:
            click.echo(f"SYNCED: Updated {len(result.sections_updated)} section(s):")
        for name in result.sections_updated:
            click.echo(f"  - {name}")
        if result.pin_written:
            click.echo("PINNED: Wrote constitution-version.txt")
        sys.exit(3)

    if result.pin_written:
        click.echo("OK: AGENTS.md already current. PINNED: Wrote constitution-version.txt")
        sys.exit(0)

    click.echo("OK: AGENTS.md is already current. No changes needed.")
    sys.exit(0)


if __name__ == "__main__":
    main()


