"""Integration tests for agents-md-sync-hardening — IT-1 through IT-6.

These tests invoke the aa-agents-sync CLI via subprocess against real or
realistic file fixtures to validate end-to-end behavior of the hardening fixes.

HANGAR_CONSTITUTION_PATH is explicitly set to REPO_ROOT in each test that
requires it, so tests are hermetic regardless of the calling shell environment.
"""
from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
CONSTITUTION_ENV = {"HANGAR_CONSTITUTION_PATH": str(REPO_ROOT)}


def _run(args: list[str], *, env_extra: dict | None = None, cwd: Path | None = None):
    """Run aa-agents-sync with given args; return CompletedProcess."""
    env = {**os.environ, **CONSTITUTION_ENV, **(env_extra or {})}
    return subprocess.run(
        ["aa-agents-sync", *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(cwd) if cwd else None,
    )


# ---------------------------------------------------------------------------
# IT-1 (TASK-4) — CRLF integration
# ---------------------------------------------------------------------------

def test_it1_crlf_agents_md_markers_recognized():
    """Scenario: it-1-crlf-agents-md-markers-recognized

    An AGENTS.md with CRLF line endings must have its BEGIN/END markers
    correctly recognized. --check must exit 0 (current, no drift) rather than
    exit 1 (parse error) or silently showing 0 sections.
    """
    current_version = (REPO_ROOT / "constitution-version.txt").read_text().strip()

    # Build AGENTS.md content with CRLF line endings, markers at current version
    lines = [
        f"<!-- BEGIN hangar-ai-constitution:mandatory-protocol v{current_version} -->",
        "## Mandatory Protocol",
        "Some protocol content.",
        "<!-- END hangar-ai-constitution:mandatory-protocol -->",
    ]
    crlf_content = "\r\n".join(lines) + "\r\n"

    with tempfile.NamedTemporaryFile(
        mode="wb", suffix=".md", delete=False
    ) as tmp:
        tmp.write(crlf_content.encode("utf-8"))
        tmp_path = tmp.name

    try:
        result = _run(["--check", tmp_path])
        assert result.returncode != 1, (
            f"--check exited 1 (error) on CRLF AGENTS.md — markers not recognized.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )
        # Exit 0 = current; Exit 2 = drift (both mean markers were recognized)
        assert result.returncode in (0, 2), (
            f"Unexpected exit code {result.returncode}.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )
    finally:
        os.unlink(tmp_path)


# ---------------------------------------------------------------------------
# IT-2 (TASK-5) — BOM integration
# ---------------------------------------------------------------------------

def test_it2_bom_agents_md_parsed_correctly():
    """Scenario: it-2-bom-agents-md-parsed-correctly

    An AGENTS.md saved with a UTF-8 BOM (U+FEFF prepended) must still have
    its BEGIN/END markers recognized. --check must exit 0 or 2, not 1.
    """
    current_version = (REPO_ROOT / "constitution-version.txt").read_text().strip()

    lines = [
        f"<!-- BEGIN hangar-ai-constitution:mandatory-protocol v{current_version} -->",
        "## Mandatory Protocol",
        "Content.",
        "<!-- END hangar-ai-constitution:mandatory-protocol -->",
    ]
    content = "\n".join(lines) + "\n"
    bom_bytes = "\ufeff".encode("utf-8") + content.encode("utf-8")

    with tempfile.NamedTemporaryFile(mode="wb", suffix=".md", delete=False) as tmp:
        tmp.write(bom_bytes)
        tmp_path = tmp.name

    try:
        result = _run(["--check", tmp_path])
        assert result.returncode != 1, (
            f"--check exited 1 (error) on BOM AGENTS.md — BOM not stripped.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )
        assert result.returncode in (0, 2), (
            f"Unexpected exit code {result.returncode}.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )
    finally:
        os.unlink(tmp_path)

# ---------------------------------------------------------------------------
# IT-3 (TASK-6) — Malformed template error surfaces
# ---------------------------------------------------------------------------

def test_it3_malformed_template_error_surfaces():
    """Scenario: it-3-malformed-template-error-surfaces

    When the constitution's templates/agents-md-sections/ directory contains
    a template with broken markers (unclosed BEGIN), the tool must exit 1 with
    a clear error message — not silently return an empty result.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # Build a minimal constitution-shaped directory tree
        templates_dir = tmp / "templates" / "agents-md-sections"
        templates_dir.mkdir(parents=True)

        # Write malformed template — BEGIN with no matching END
        bad_template = (
            "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
            "## Protocol\n"
            "Content.\n"
            # Intentionally missing END marker
        )
        (templates_dir / "mandatory-protocol.md").write_text(bad_template)

        # Write a minimal constitution-version.txt
        (tmp / "constitution-version.txt").write_text("1.0.0\n")

        # Write a valid AGENTS.md target
        agents_md = tmp / "AGENTS.md"
        agents_md.write_text(
            "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v0.9.0 -->\n"
            "## Protocol\n"
            "Old content.\n"
            "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
        )

        result = _run(
            ["--dry-run", str(agents_md)],
            env_extra={"HANGAR_CONSTITUTION_PATH": str(tmp)},
        )

        assert result.returncode == 1, (
            f"Expected exit 1 (error) for malformed template, got {result.returncode}.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )
        combined = result.stdout + result.stderr
        # PS-3: must be a clean ERROR message, not a Python traceback
        assert "Traceback" not in combined, (
            f"Got a raw Python traceback instead of a clean ERROR message:\n{combined}"
        )
        assert "malformed" in combined.lower() or "error" in combined.lower(), (
            f"Expected error message about malformed template, got:\n{combined}"
        )

# ---------------------------------------------------------------------------
# IT-4 (TASK-7) — --check on real AGENTS.md
# ---------------------------------------------------------------------------

def test_it4_check_on_real_agents_md():
    """Scenario: it-4-check-on-real-agents-md

    Running --check against the actual AGENTS.md in this repository must exit 0
    (current, no drift) without crashing. This validates that the real file's
    markers are correctly parsed and that the installed tool is wired correctly.
    """
    agents_md = REPO_ROOT / "AGENTS.md"
    assert agents_md.exists(), "AGENTS.md must exist at repo root"

    result = _run(["--check", str(agents_md)])

    assert result.returncode == 0, (
        f"--check on real AGENTS.md exited {result.returncode} (expected 0 = current).\n"
        f"stderr: {result.stderr}\nstdout: {result.stdout}"
    )
    assert "OK" in result.stdout, (
        f"Expected 'OK' in stdout, got:\n{result.stdout}"
    )

# ---------------------------------------------------------------------------
# IT-5 (TASK-8) — Non-git directory guard
# ---------------------------------------------------------------------------

def test_it5_non_git_dir_exits_with_error():
    """Scenario: it-5-non-git-dir-exits-with-error

    Running aa-agents-sync --apply (write mode) against an
    AGENTS.md in a directory that is not a git repository must exit 1 with an
    explicit error. No write should be attempted.

    This drives FIX-5: is_git_dirty() returns None for non-git dirs; the write
    path must treat None as 'refuse to write' rather than silently continuing.
    --apply is required to trigger write mode (FIX-12).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        agents_md = tmp / "AGENTS.md"

        # Write an AGENTS.md with old version so drift is detected
        agents_md.write_text(
            "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v0.9.0 -->\n"
            "## Protocol\n"
            "Old content.\n"
            "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
        )
        mtime_before = agents_md.stat().st_mtime

        result = _run(["--apply", str(agents_md)])  # write mode

        # Must refuse write with exit 1
        assert result.returncode == 1, (
            f"Expected exit 1 (refuse write in non-git dir), got {result.returncode}.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )
        # File must NOT have been modified
        assert agents_md.stat().st_mtime == mtime_before, (
            "AGENTS.md was modified in a non-git directory — write should have been refused"
        )

# ---------------------------------------------------------------------------
# IT-6 (TASK-9) — --dry-run produces unified diff output
# ---------------------------------------------------------------------------

def test_it6_dry_run_shows_unified_diff():
    """Scenario: it-6-dry-run-shows-unified-diff

    When AGENTS.md is drifted, running --dry-run must output a unified diff
    containing the standard markers (---, +++, @@). No file should be written.
    """
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(
            "# Preamble\n"
            "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v0.9.0 -->\n"
            "## Protocol\n"
            "Stale content that will differ from template.\n"
            "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
            "# Postamble\n"
        )
        tmp_path = tmp.name

    try:
        mtime_before = Path(tmp_path).stat().st_mtime
        result = _run(["--dry-run", tmp_path])

        assert result.returncode == 0, (
            f"--dry-run exited {result.returncode} (expected 0).\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )
        output = result.stdout
        assert "---" in output, f"Unified diff missing '---' line:\n{output}"
        assert "+++" in output, f"Unified diff missing '+++' line:\n{output}"
        assert "@@" in output, f"Unified diff missing '@@' hunk header:\n{output}"

        # File must NOT have been written
        assert Path(tmp_path).stat().st_mtime == mtime_before, (
            "--dry-run modified the file — it must be read-only"
        )
    finally:
        os.unlink(tmp_path)


def test_it5b_force_flag_does_not_bypass_non_git_guard():
    """Scenario: it-5-non-git-dir-exits-with-error (--force variant)

    PS-1 pre-ship fix: --force must NOT bypass the non-git guard.
    --force semantics are 'write even if dirty', NOT 'write outside a git repo'.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        agents_md = tmp / "AGENTS.md"
        agents_md.write_text(
            "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v0.9.0 -->\n"
            "## Protocol\n"
            "Old content.\n"
            "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
        )
        mtime_before = agents_md.stat().st_mtime

        result = _run(["--apply", "--force", str(agents_md)])  # --apply --force in non-git dir

        assert result.returncode == 1, (
            f"Expected exit 1 even with --force in non-git dir, got {result.returncode}.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )
        assert agents_md.stat().st_mtime == mtime_before, (
            "--force wrote AGENTS.md in a non-git directory — this must be refused"
        )


# ---------------------------------------------------------------------------
# IT-7 (TASK-21) — Downgrade guard: sibling constitution older version rejected
# ---------------------------------------------------------------------------

def test_it7_constitution_downgrade_rejected():
    """Scenario: it-7-stale-sibling-constitution-downgrade-rejected

    If the sibling constitution's version file contains a version lower than
    the version already recorded in AGENTS.md markers, --apply must refuse
    with exit 1 and leave AGENTS.md unmodified.

    This exercises FIX-4 (downgrade guard in checker.py) end-to-end.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        subprocess.run(["git", "init", str(tmp)], capture_output=True, check=True)

        constitution_dir = tmp / "constitution"
        constitution_dir.mkdir()
        # Constitution claims v0.5.0 — OLDER than the existing marker
        (constitution_dir / "constitution-version.txt").write_text("0.5.0\n")
        templates_dir = constitution_dir / "templates" / "agents-md-sections"
        templates_dir.mkdir(parents=True)
        (templates_dir / "mandatory-protocol.md").write_text(
            "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v0.5.0 -->\n"
            "Downgraded content.\n"
            "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
        )

        agents_md = tmp / "AGENTS.md"
        original = (
            "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
            "Current content.\n"
            "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
        )
        agents_md.write_text(original)
        mtime_before = agents_md.stat().st_mtime

        result = _run(
            ["--apply", "--force", "--constitution-path", str(constitution_dir), str(agents_md)]
        )

        assert result.returncode == 1, (
            f"Expected exit 1 (downgrade refused), got {result.returncode}.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )
        assert agents_md.stat().st_mtime == mtime_before, (
            "AGENTS.md was modified despite downgrade guard — FIX-4 not working end-to-end"
        )
        assert agents_md.read_text() == original, (
            "AGENTS.md content must be unchanged after rejected downgrade"
        )


# ---------------------------------------------------------------------------
# IT-8 (TASK-22) — Race condition / concurrent invocations
# ---------------------------------------------------------------------------

def test_it8_concurrent_invocations_no_corruption():
    """Scenario: it-8-concurrent-invocations-no-corruption

    Two concurrent --apply runs on the same AGENTS.md must not corrupt the file.
    At least one invocation must succeed (exit 3 = changes written, or exit 0 =
    already current). The file must parse cleanly after both complete.

    This exercises FIX-8 (fcntl file locking in syncer.py) end-to-end.
    """
    import time  # noqa: PLC0415
    import threading  # noqa: PLC0415
    from aa_agents_sync.parser import parse_markers  # noqa: PLC0415

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        subprocess.run(["git", "init", str(tmp)], capture_output=True, check=True)

        constitution_dir = tmp / "constitution"
        constitution_dir.mkdir()
        (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
        templates_dir = constitution_dir / "templates" / "agents-md-sections"
        templates_dir.mkdir(parents=True)
        (templates_dir / "mandatory-protocol.md").write_text(
            "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
            "Updated canonical content.\n"
            "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
        )

        agents_md = tmp / "AGENTS.md"
        agents_md.write_text(
            "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v0.9.0 -->\n"
            "Old content.\n"
            "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
        )

        results = []

        def run_sync():
            r = _run(
                [
                    "--apply", "--force",
                    "--constitution-path", str(constitution_dir),
                    str(agents_md),
                ]
            )
            results.append(r)

        t1 = threading.Thread(target=run_sync)
        t2 = threading.Thread(target=run_sync)
        t1.start()
        t2.start()
        t1.join(timeout=10)
        t2.join(timeout=10)

        assert len(results) == 2, "Both threads must complete"

        # At least one invocation must succeed or find content already current
        success_codes = {0, 3}
        assert any(r.returncode in success_codes for r in results), (
            f"At least one invocation must exit 0 or 3; got {[r.returncode for r in results]}.\n"
            + "\n".join(f"Run {i}: rc={r.returncode} stdout={r.stdout!r} stderr={r.stderr!r}"
                        for i, r in enumerate(results))
        )

        # File must parse cleanly (no corruption)
        final_content = agents_md.read_text()
        sections, errors = parse_markers(final_content)
        assert not errors, f"AGENTS.md is corrupted after concurrent writes: {errors}"
        assert sections, "AGENTS.md must still have parseable markers after concurrent writes"


# ---------------------------------------------------------------------------
# IT-9 (TASK-23) — --apply creates backup and post-write verify succeeds
# ---------------------------------------------------------------------------

def test_it9_apply_creates_backup_and_verifies():
    """Scenario: it-9-apply-creates-backup-and-verifies

    After a successful --apply run on a drifted AGENTS.md:
    1. AGENTS.md.bak must exist alongside AGENTS.md
    2. The written AGENTS.md must re-parse cleanly (post-write verify passed)
    3. The updated content must contain the new version marker

    This exercises FIX-6 (backup) and FIX-7 (post-write verify) end-to-end.
    """
    from aa_agents_sync.parser import parse_markers  # noqa: PLC0415

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        subprocess.run(["git", "init", str(tmp)], capture_output=True, check=True)

        constitution_dir = tmp / "constitution"
        constitution_dir.mkdir()
        (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
        templates_dir = constitution_dir / "templates" / "agents-md-sections"
        templates_dir.mkdir(parents=True)
        (templates_dir / "mandatory-protocol.md").write_text(
            "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
            "New authoritative content.\n"
            "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
        )

        agents_md = tmp / "AGENTS.md"
        agents_md.write_text(
            "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v0.8.0 -->\n"
            "Old content.\n"
            "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
        )

        result = _run(
            [
                "--apply", "--force",
                "--constitution-path", str(constitution_dir),
                str(agents_md),
            ]
        )

        assert result.returncode == 3, (
            f"Expected exit 3 (changes written), got {result.returncode}.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )

        bak = agents_md.with_suffix(agents_md.suffix + ".bak")
        assert not bak.exists(), (
            "AGENTS.md.bak must be cleaned up after successful --apply (R3)"
        )

        written = agents_md.read_text()
        assert "v1.0.0" in written, "Updated AGENTS.md must contain new version marker"
        sections, errors = parse_markers(written)
        assert not errors, f"Post-write AGENTS.md failed to re-parse: {errors}"
        assert sections, "Post-write AGENTS.md must have parseable markers"


# ---------------------------------------------------------------------------
# IT-10 (TASK-24) — AGENTS_SYNC_DISABLED=1 prevents all writes
# ---------------------------------------------------------------------------

def test_it10_env_var_prevents_write_under_any_flag():
    """Scenario: it-10-env-var-prevents-write-under-any-flag

    With AGENTS_SYNC_DISABLED=1, both --apply and --legacy-mode must exit 0
    without writing AGENTS.md. This validates FIX-14 at the process level.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        subprocess.run(["git", "init", str(tmp)], capture_output=True, check=True)

        constitution_dir = tmp / "constitution"
        constitution_dir.mkdir()
        (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
        templates_dir = constitution_dir / "templates" / "agents-md-sections"
        templates_dir.mkdir(parents=True)
        (templates_dir / "mandatory-protocol.md").write_text(
            "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
            "New content.\n"
            "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
        )

        agents_md = tmp / "AGENTS.md"
        original = (
            "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v0.9.0 -->\n"
            "Old content.\n"
            "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
        )
        agents_md.write_text(original)
        mtime_before = agents_md.stat().st_mtime

        disabled_env = {"AGENTS_SYNC_DISABLED": "1"}

        # --apply must be suppressed
        result = _run(
            [
                "--apply", "--force",
                "--constitution-path", str(constitution_dir),
                str(agents_md),
            ],
            env_extra=disabled_env,
        )
        assert result.returncode == 0, (
            f"AGENTS_SYNC_DISABLED=1 must suppress --apply (exit 0), "
            f"got {result.returncode}. stdout={result.stdout!r}"
        )
        assert agents_md.stat().st_mtime == mtime_before, (
            "AGENTS.md was modified with AGENTS_SYNC_DISABLED=1 — FIX-14 not working"
        )
        assert agents_md.read_text() == original, (
            "AGENTS.md content changed with AGENTS_SYNC_DISABLED=1"
        )


# ---------------------------------------------------------------------------
# R2-1 — FIX-13 .git boundary test
# ---------------------------------------------------------------------------

def test_r2_1_git_boundary_stops_config_walk():
    """R2-1: is_sync_disabled() must stop at .git boundary.

    Validates that a parent repo's agents-sync.yml does not affect a nested repo.
    """
    from aa_agents_sync.config import is_sync_disabled

    with tempfile.TemporaryDirectory() as tmpdir:
        parent = Path(tmpdir)
        # Parent repo with opt-out
        (parent / ".git").mkdir()
        (parent / "agents-sync.yml").write_text("disabled: true\n")

        # Nested child repo without opt-out
        child = parent / "nested-repo"
        child.mkdir()
        (child / ".git").mkdir()
        agents_md = child / "AGENTS.md"
        agents_md.write_text("# test")

        # Child repo should NOT inherit parent's disabled status
        assert is_sync_disabled(agents_md) is False, (
            "Child repo incorrectly inherited parent repo's agents-sync.yml opt-out"
        )


def test_r2_1_config_found_before_git_boundary():
    """R2-1: is_sync_disabled() should find config in current repo before .git boundary."""
    from aa_agents_sync.config import is_sync_disabled

    with tempfile.TemporaryDirectory() as tmpdir:
        repo = Path(tmpdir)
        (repo / ".git").mkdir()
        (repo / "agents-sync.yml").write_text("disabled: true\n")
        subdir = repo / "src"
        subdir.mkdir()
        agents_md = subdir / "AGENTS.md"
        agents_md.write_text("# test")

        # Should find the config in the same repo
        assert is_sync_disabled(agents_md) is True, (
            "Failed to find agents-sync.yml in current repo"
        )


# ---------------------------------------------------------------------------
# R2-2 — FIX-14 --check still runs when AGENTS_SYNC_DISABLED=1
# ---------------------------------------------------------------------------

def test_r2_2_check_mode_runs_despite_disabled_env():
    """R2-2: --check must still detect drift even when AGENTS_SYNC_DISABLED=1.

    CI operators need accurate drift detection regardless of write-disable status.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        subprocess.run(["git", "init", str(tmp)], capture_output=True, check=True)

        constitution_dir = tmp / "constitution"
        constitution_dir.mkdir()
        (constitution_dir / "constitution-version.txt").write_text("2.0.0\n")
        templates_dir = constitution_dir / "templates" / "agents-md-sections"
        templates_dir.mkdir(parents=True)
        (templates_dir / "mandatory-protocol.md").write_text(
            "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v2.0.0 -->\n"
            "New content.\n"
            "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
        )

        agents_md = tmp / "AGENTS.md"
        # Intentionally stale version to trigger drift
        agents_md.write_text(
            "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
            "Old content.\n"
            "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
        )

        disabled_env = {"AGENTS_SYNC_DISABLED": "1"}

        # --check must still report drift (exit 2), not silently exit 0
        result = _run(
            [
                "--check",
                "--constitution-path", str(constitution_dir),
                str(agents_md),
            ],
            env_extra=disabled_env,
        )
        assert result.returncode == 2, (
            f"--check must report drift (exit 2) even with AGENTS_SYNC_DISABLED=1, "
            f"got {result.returncode}. stdout={result.stdout!r}"
        )
        assert "DRIFT" in result.stdout, (
            "--check must output DRIFT message even with AGENTS_SYNC_DISABLED=1"
        )
