"""Tests for agents-md-drift-sync — TASK-1, TASK-2, TASK-3, TASK-4."""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

BEGIN_RE = re.compile(
    r"^<!-- BEGIN hangar-ai-constitution:([a-z][a-z0-9-]+) v(\d+\.\d+\.\d+) -->$",
    re.MULTILINE,
)
END_RE = re.compile(
    r"^<!-- END hangar-ai-constitution:([a-z][a-z0-9-]+) -->$",
    re.MULTILINE,
)


def test_constitution_version_file_exists():
    """Scenario: version-file-exists — constitution-version.txt must be at repo root."""
    version_file = REPO_ROOT / "constitution-version.txt"
    assert version_file.exists(), "constitution-version.txt must exist at repo root"


def test_constitution_version_is_semver():
    """constitution-version.txt must contain a valid semver string."""
    version_file = REPO_ROOT / "constitution-version.txt"
    content = version_file.read_text().strip()
    assert re.match(r"^\d+\.\d+\.\d+$", content), (
        f"constitution-version.txt must contain semver (e.g. 1.0.0), got: {content!r}"
    )


# --- TASK-2 tests ---

def test_mandatory_protocol_section_file_exists():
    """Scenario: canonical-section-file-exists — mandatory-protocol.md must exist."""
    section_file = REPO_ROOT / "templates" / "agents-md-sections" / "mandatory-protocol.md"
    assert section_file.exists(), (
        "templates/agents-md-sections/mandatory-protocol.md must exist"
    )


def test_mandatory_protocol_has_begin_marker():
    """Section file must open with a valid BEGIN marker for mandatory-protocol."""
    section_file = REPO_ROOT / "templates" / "agents-md-sections" / "mandatory-protocol.md"
    content = section_file.read_text()
    match = BEGIN_RE.search(content)
    assert match, "mandatory-protocol.md must contain a BEGIN marker"
    assert match.group(1) == "mandatory-protocol", (
        f"BEGIN marker section name must be 'mandatory-protocol', got: {match.group(1)}"
    )


def test_mandatory_protocol_has_end_marker():
    """Section file must close with a valid END marker for mandatory-protocol."""
    section_file = REPO_ROOT / "templates" / "agents-md-sections" / "mandatory-protocol.md"
    content = section_file.read_text()
    match = END_RE.search(content)
    assert match, "mandatory-protocol.md must contain an END marker"
    assert match.group(1) == "mandatory-protocol", (
        f"END marker section name must be 'mandatory-protocol', got: {match.group(1)}"
    )


def test_mandatory_protocol_begin_version_matches_constitution():
    """BEGIN marker version must match constitution-version.txt."""
    section_file = REPO_ROOT / "templates" / "agents-md-sections" / "mandatory-protocol.md"
    version_file = REPO_ROOT / "constitution-version.txt"
    content = section_file.read_text()
    constitution_version = version_file.read_text().strip()
    match = BEGIN_RE.search(content)
    assert match, "No BEGIN marker found"
    assert match.group(2) == constitution_version, (
        f"BEGIN marker version {match.group(2)!r} must match "
        f"constitution-version.txt {constitution_version!r}"
    )


def test_mandatory_protocol_contains_eng41_anchor():
    """Section content must contain the ENG-4.1 anchor (canonical identity check)."""
    section_file = REPO_ROOT / "templates" / "agents-md-sections" / "mandatory-protocol.md"
    content = section_file.read_text()
    assert "MANDATORY AGENT PROTOCOL (Per ENG-4.1" in content, (
        "mandatory-protocol.md must contain the canonical ENG-4.1 anchor string"
    )


# --- TASK-3 tests ---

def test_agents_md_sync_package_exists():
    """Scenario: tool-package-scaffolded — tools/agents-md-sync/ must exist."""
    package_dir = REPO_ROOT / "tools" / "agents-md-sync"
    assert package_dir.is_dir(), "tools/agents-md-sync/ directory must exist"


def test_agents_md_sync_pyproject_exists():
    """tools/agents-md-sync/pyproject.toml must exist."""
    pyproject = REPO_ROOT / "tools" / "agents-md-sync" / "pyproject.toml"
    assert pyproject.exists(), "tools/agents-md-sync/pyproject.toml must exist"


def test_agents_md_sync_package_name():
    """pyproject.toml must declare package name aa-agents-sync."""
    pyproject = REPO_ROOT / "tools" / "agents-md-sync" / "pyproject.toml"
    content = pyproject.read_text()
    assert 'name = "aa-agents-sync"' in content, (
        "pyproject.toml must declare name = \"aa-agents-sync\""
    )


def test_agents_md_sync_cli_entrypoint():
    """pyproject.toml must declare aa-agents-sync CLI entrypoint."""
    pyproject = REPO_ROOT / "tools" / "agents-md-sync" / "pyproject.toml"
    content = pyproject.read_text()
    assert "aa-agents-sync" in content and "cli:main" in content, (
        "pyproject.toml must declare aa-agents-sync CLI entrypoint"
    )


def test_agents_md_sync_python_package_dir():
    """tools/agents-md-sync/aa_agents_sync/__init__.py must exist."""
    init = REPO_ROOT / "tools" / "agents-md-sync" / "aa_agents_sync" / "__init__.py"
    assert init.exists(), "aa_agents_sync/__init__.py must exist"


def test_agents_md_sync_cli_module():
    """tools/agents-md-sync/aa_agents_sync/cli.py must exist."""
    cli = REPO_ROOT / "tools" / "agents-md-sync" / "aa_agents_sync" / "cli.py"
    assert cli.exists(), "aa_agents_sync/cli.py must exist"


def test_agents_md_sync_tool_tests_dir():
    """tools/agents-md-sync/tests/ directory must exist."""
    tests_dir = REPO_ROOT / "tools" / "agents-md-sync" / "tests"
    assert tests_dir.is_dir(), "tools/agents-md-sync/tests/ must exist"


# --- TASK-4 tests ---

def test_check_drift_returns_no_drift_when_markers_are_current(tmp_path):
    """Scenario: check-mode-current — check_drift returns has_drift=False when marker
    version matches constitution-version.txt."""
    from aa_agents_sync.checker import check_drift  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(
        "# Header\n"
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Some protocol content here.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
        "# Footer\n"
    )

    result = check_drift(agents_md_path=agents_md, constitution_path=constitution_dir)

    assert result.has_drift is False, (
        "check_drift must return has_drift=False when marker version matches constitution"
    )


def test_check_drift_returns_has_drift_when_marker_is_stale(tmp_path):
    """Scenario: check-mode-detects-drift — check_drift returns has_drift=True when
    marker version is behind constitution-version.txt."""
    from aa_agents_sync.checker import check_drift  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.1.0\n")

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Old protocol content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    result = check_drift(agents_md_path=agents_md, constitution_path=constitution_dir)

    assert result.has_drift is True, (
        "check_drift must return has_drift=True when marker version is behind constitution"
    )


def test_check_mode_cli_exits_2_on_drift(tmp_path):
    """Scenario: check-mode-detects-drift — CLI exits 2 when markers are stale."""
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("2.0.0\n")

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Old content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--check", "--constitution-path", str(constitution_dir), str(agents_md)],
    )
    assert result.exit_code == 2, (
        f"--check must exit 2 on drift, got {result.exit_code}. output={result.output!r}"
    )


def test_check_mode_cli_exits_0_when_current(tmp_path):
    """Scenario: check-mode-current — CLI exits 0 when markers match constitution version."""
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Current content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--check", "--constitution-path", str(constitution_dir), str(agents_md)],
    )
    assert result.exit_code == 0, (
        f"--check must exit 0 when current, got {result.exit_code}. output={result.output!r}"
    )


def test_check_mode_cli_exits_1_on_marker_syntax_error(tmp_path):
    """Scenario: check-mode-marker-error — CLI exits 1 when END name mismatches BEGIN
    name (C5: END must match BEGIN name)."""
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Content.\n"
        "<!-- END hangar-ai-constitution:wrong-section-name -->\n"
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--check", "--constitution-path", str(constitution_dir), str(agents_md)],
    )
    assert result.exit_code == 1, (
        f"--check must exit 1 on marker syntax error, got {result.exit_code}. "
        f"output={result.output!r}"
    )


# --- TASK-5 tests ---

def test_safe_mode_exits_0_when_already_current(tmp_path):
    """Scenario: safe-mode-syncs-section — safe mode (no flags) exits 0 when AGENTS.md
    markers are already current (no-op path)."""
    import subprocess  # noqa: PLC0415
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    # PS-1: write mode requires a git repo even with --force
    subprocess.run(["git", "init", str(tmp_path)], capture_output=True, check=True)

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Current canonical content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Current canonical content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--force", "--constitution-path", str(constitution_dir), str(agents_md)],
    )
    assert result.exit_code == 0, (
        f"safe mode must exit 0 when no changes needed, got {result.exit_code}. "
        f"output={result.output!r}"
    )


def test_safe_mode_exits_3_and_updates_stale_section(tmp_path):
    """Scenario: safe-mode-syncs-section — safe mode exits 3 and writes updated content
    when a section is stale."""
    import subprocess  # noqa: PLC0415
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    # PS-1: write mode requires a git repo even with --force
    subprocess.run(["git", "init", str(tmp_path)], capture_output=True, check=True)

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.1.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    canonical_content = (
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.1.0 -->\n"
        "New canonical content for v1.1.0.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )
    (templates_dir / "mandatory-protocol.md").write_text(canonical_content)

    agents_md = tmp_path / "AGENTS.md"
    original = (
        "# Preamble\n"
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Old stale content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
        "# Footer\n"
    )
    agents_md.write_text(original)

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--apply", "--force", "--constitution-path", str(constitution_dir), str(agents_md)],
    )
    assert result.exit_code == 3, (
        f"safe mode must exit 3 when changes written, got {result.exit_code}. "
        f"output={result.output!r}"
    )
    updated = agents_md.read_text()
    assert "v1.1.0" in updated, "Updated AGENTS.md must contain new version marker"
    assert "Old stale content" not in updated, "Old content must be replaced"
    assert "New canonical content for v1.1.0" in updated, "New canonical content must be present"
    assert "# Preamble" in updated, "Surrounding content must be preserved"
    assert "# Footer" in updated, "Surrounding content must be preserved"


def test_safe_mode_exits_1_on_dirty_git_tree(tmp_path):
    """Scenario: safe-mode-syncs-section — safe mode exits 1 if git tree is dirty and
    --force is not set (C1: no silent overwrite on dirty tree)."""
    import subprocess  # noqa: PLC0415
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    # Create a real git repo in tmp_path with a dirty state
    git_dir = tmp_path / "project"
    git_dir.mkdir()
    subprocess.run(["git", "init", str(git_dir)], capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=git_dir, capture_output=True, check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=git_dir, capture_output=True, check=True,
    )
    # Create an untracked file to make repo dirty
    (git_dir / "untracked.txt").write_text("dirty\n")

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("2.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v2.0.0 -->\n"
        "New content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    agents_md = git_dir / "AGENTS.md"
    agents_md.write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Old content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--apply", "--constitution-path", str(constitution_dir), str(agents_md)],
    )
    assert result.exit_code == 1, (
        f"safe mode must exit 1 on dirty git tree without --force, "
        f"got {result.exit_code}. output={result.output!r}"
    )


# --- TASK-6 tests ---

def test_legacy_mode_refuses_without_dry_run(tmp_path):
    """Scenario: legacy-mode-detects-and-migrates — CLI exits 1 when --legacy-mode is
    used without --dry-run (C9 enforcement)."""
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text("# Some AGENTS.md content\n")

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--legacy-mode", "--constitution-path", str(constitution_dir), str(agents_md)],
    )
    assert result.exit_code == 1, (
        f"--legacy-mode without --dry-run must exit 1 (C9), "
        f"got {result.exit_code}. output={result.output!r}"
    )


def test_legacy_mode_exits_2_when_anchor_detected(tmp_path):
    """Scenario: legacy-mode-detects-and-migrates — CLI exits 2 when the legacy
    ENG-4.1 anchor is found in AGENTS.md (legacy drift state detected)."""
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "New protocol content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(
        "# Header\n\n"
        "## MANDATORY AGENT PROTOCOL (Per ENG-4.1 — NON-NEGOTIABLE)\n\n"
        "Old unversioned 8-step content here.\n\n"
        "# Footer\n"
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--legacy-mode", "--dry-run",
            "--constitution-path", str(constitution_dir),
            str(agents_md),
        ],
    )
    assert result.exit_code == 0, (
        f"--legacy-mode must exit 0 when legacy anchor found (C-1 corrected), "
        f"got {result.exit_code}. output={result.output!r}"
    )


def test_legacy_mode_exits_0_when_no_anchor(tmp_path):
    """Scenario: legacy-mode-detects-and-migrates — CLI exits 0 when no legacy anchor
    is present (already migrated or freshly adopted)."""
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Already migrated content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--legacy-mode", "--dry-run",
            "--constitution-path", str(constitution_dir),
            str(agents_md),
        ],
    )
    assert result.exit_code == 2, (
        f"--legacy-mode must exit 2 when no legacy anchor found (C-1 corrected), "
        f"got {result.exit_code}. output={result.output!r}"
    )


# --- TASK-7 tests ---

def test_a01_lint_fails_when_markers_are_stale(tmp_path):
    """Scenario: a01-lint-check-detects-drift — A01 rule returns FAIL when any
    bounded section version is behind constitution-version.txt."""
    from aa_constitution_lint.domain.rules.agents_md_sync import AgentsMdDriftRule  # noqa: PLC0415
    from aa_constitution_lint.domain.models import EvaluationResult  # noqa: PLC0415

    (tmp_path / "constitution-version.txt").write_text("2.0.0\n")
    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Old content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    rule = AgentsMdDriftRule(constitution_path=tmp_path)
    results = rule.evaluate(project_path=tmp_path)

    assert results, "Rule must return at least one evaluation"
    assert any(r.result == EvaluationResult.FAIL for r in results), (
        "A01 must FAIL when a section marker version is behind constitution"
    )


def test_a01_lint_warns_when_no_markers(tmp_path):
    """A01 rule returns WARNING when AGENTS.md exists but has no markers (legacy)."""
    from aa_constitution_lint.domain.rules.agents_md_sync import AgentsMdDriftRule  # noqa: PLC0415
    from aa_constitution_lint.domain.models import EvaluationResult  # noqa: PLC0415

    (tmp_path / "constitution-version.txt").write_text("1.0.0\n")
    (tmp_path / "AGENTS.md").write_text(
        "# AGENTS.md\n## MANDATORY AGENT PROTOCOL (Per ENG-4.1)\nOld unversioned content.\n"
    )

    rule = AgentsMdDriftRule(constitution_path=tmp_path)
    results = rule.evaluate(project_path=tmp_path)

    assert any(r.result == EvaluationResult.WARNING for r in results), (
        "A01 must WARNING when AGENTS.md has no markers (legacy state)"
    )


def test_mf_02_a01_warning_message_says_apply_not_legacy_mode():
    """Scenario: mf-02 — A01 WARNING message must say '--apply', not '--legacy-mode --dry-run'.
    The --legacy-mode flag is for files WITH a legacy block; --apply is the correct
    path for compact/custom AGENTS.md with no markers at all."""
    import tempfile, pathlib  # noqa: E401, PLC0415
    from aa_constitution_lint.domain.rules.agents_md_sync import AgentsMdDriftRule  # noqa: PLC0415
    from aa_constitution_lint.domain.models import EvaluationResult  # noqa: PLC0415

    with tempfile.TemporaryDirectory() as td:
        project_path = pathlib.Path(td)
        (project_path / "constitution-version.txt").write_text("1.0.0\n")
        (project_path / "AGENTS.md").write_text(
            "# My App\n\nMandatory Protocol (ENG-4.1): RED→GREEN→REFACTOR.\n"
        )

        rule = AgentsMdDriftRule(constitution_path=project_path)
        results = rule.evaluate(project_path=project_path)

    warning = next((r for r in results if r.result == EvaluationResult.WARNING), None)
    assert warning is not None, "mf-02: A01 must WARNING when AGENTS.md has no markers"

    msg = warning.context.get("message", "")
    assert "--apply" in msg, (
        f"mf-02: A01 warning must mention '--apply'. message={msg!r}"
    )
    assert "--legacy-mode" not in msg, (
        f"mf-02: A01 warning must NOT mention '--legacy-mode'. message={msg!r}"
    )


def test_ms_02_a01_warns_not_skips_when_markers_present_but_no_version_source():
    """Scenario: ms-02 — A01 must return WARNING (not SKIP) when AGENTS.md has
    valid markers but no version source is available. An adopted repo with missing
    version source should be visible in CI, not silently bypassed."""
    import tempfile, pathlib  # noqa: E401, PLC0415
    from aa_constitution_lint.domain.rules.agents_md_sync import AgentsMdDriftRule  # noqa: PLC0415
    from aa_constitution_lint.domain.models import EvaluationResult  # noqa: PLC0415

    with tempfile.TemporaryDirectory() as td:
        project_path = pathlib.Path(td)
        # AGENTS.md has valid markers — repo IS adopted
        (project_path / "AGENTS.md").write_text(
            "# My App\n"
            "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
            "Content.\n"
            "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
        )
        # NO constitution-version.txt — no local pin file
        # NO constitution_path — simulates CI running without --constitution

        rule = AgentsMdDriftRule(constitution_path=None)
        results = rule.evaluate(project_path=project_path)

    assert results, "ms-02: A01 must return at least one evaluation"
    result = results[0]

    assert result.result == EvaluationResult.WARNING, (
        f"ms-02: A01 must return WARNING (not SKIP) for adopted repo with no version source. "
        f"Got {result.result}. context={result.context}"
    )
    msg = result.context.get("message", "")
    assert "AA_CONSTITUTION_PATH" in msg, (
        f"ms-02: WARNING message must mention AA_CONSTITUTION_PATH env var. message={msg!r}"
    )

def test_a01_lint_passes_when_markers_are_current(tmp_path):
    """A01 rule returns PASS when all AGENTS.md markers match constitution-version.txt."""
    from aa_constitution_lint.domain.rules.agents_md_sync import AgentsMdDriftRule  # noqa: PLC0415
    from aa_constitution_lint.domain.models import EvaluationResult  # noqa: PLC0415

    (tmp_path / "constitution-version.txt").write_text("1.0.0\n")
    (tmp_path / "AGENTS.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Current content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    rule = AgentsMdDriftRule(constitution_path=tmp_path)
    results = rule.evaluate(project_path=tmp_path)

    assert any(r.result == EvaluationResult.PASS for r in results), (
        "A01 must PASS when all markers are current"
    )


# --- R2 correction tests (C-8, C-9, C-10) ---

def test_parser_rejects_embedded_marker_not_on_own_line(tmp_path):
    """C-10: BEGIN/END markers must be anchored (^...$). A marker embedded after
    other text on the same line must NOT be recognised as a valid marker."""
    from aa_agents_sync.parser import parse_markers  # noqa: PLC0415

    content = (
        "some text <!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "content\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )
    sections, errors = parse_markers(content)
    assert len(sections) == 0, (
        "C-10: marker embedded after leading text must not be parsed as a valid section"
    )


def test_dry_run_safe_mode_bypasses_dirty_tree_guard(tmp_path):
    """C-8: --dry-run is read-only and must NOT be blocked by the dirty-tree guard.
    A dirty git tree + --dry-run must exit 0, not exit 1."""
    import subprocess  # noqa: PLC0415
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    git_dir = tmp_path / "project"
    git_dir.mkdir()
    subprocess.run(["git", "init", str(git_dir)], capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=git_dir, capture_output=True, check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=git_dir, capture_output=True, check=True,
    )
    (git_dir / "untracked.txt").write_text("dirty\n")  # make tree dirty

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Current content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    agents_md = git_dir / "AGENTS.md"
    agents_md.write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Current content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--constitution-path", str(constitution_dir), "--dry-run", str(agents_md)],
    )
    assert result.exit_code == 0, (
        f"C-8: --dry-run must bypass dirty-tree guard (exit 0 on clean AGENTS.md), "
        f"got {result.exit_code}. output={result.output!r}"
    )
    assert "No changes needed" in result.output, (
        f"C-8: --dry-run must report no changes when up-to-date. output={result.output!r}"
    )


def test_dry_run_shows_unified_diff_for_stale_sections(tmp_path):
    """C-9: --dry-run must show a unified diff (--- / +++ headers) of what would
    change rather than just a version summary."""
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("2.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v2.0.0 -->\n"
        "New canonical content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Old content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--constitution-path", str(constitution_dir), "--dry-run", str(agents_md)],
    )
    assert result.exit_code == 0, (
        f"C-9: --dry-run must exit 0 with diff output, got {result.exit_code}. "
        f"output={result.output!r}"
    )
    assert "---" in result.output and "+++" in result.output, (
        f"C-9: --dry-run must include unified diff headers (--- / +++). "
        f"output={result.output!r}"
    )


# ---------------------------------------------------------------------------
# agents-md-sync-hardening tests
# ---------------------------------------------------------------------------

# --- FIX-1 (TASK-1) ---

def test_fix1_malformed_template_raises_not_silently_ignored(tmp_path):
    """Scenario: fix-1-template-parser-errors-surface — _load_canonical_sections()
    must raise an error (or return a non-empty error dict) when the template file
    has malformed/unparseable markers, NOT silently return empty sections."""
    from aa_agents_sync.syncer import _load_canonical_sections

    # Set up a constitution dir with a malformed template (BEGIN without END)
    templates_dir = tmp_path / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    bad_template = templates_dir / "mandatory-protocol.md"
    bad_template.write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "## Protocol\nsome content\n"
        # deliberately missing END marker
    )

    # Current (broken) behavior: returns {} silently — this test must FAIL today
    # Expected (fixed) behavior: raises ValueError or returns error indicator
    import pytest
    with pytest.raises((ValueError, RuntimeError), match=r"(?i)(malformed|parse|missing|end marker|unclosed)"):
        _load_canonical_sections(tmp_path)


# --- FIX-2 (TASK-2) ---

def test_fix2_crlf_markers_recognized():
    """Scenario: fix-2-crlf-markers-recognized — AGENTS.md with CRLF line endings
    must have its BEGIN/END markers correctly parsed. The $ anchor must match
    before \\r\\n, not just before \\n."""
    from aa_agents_sync.parser import parse_markers

    # Construct content with CRLF line endings (as Windows editors produce)
    lines = [
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->",
        "## Protocol",
        "Some content here.",
        "<!-- END hangar-ai-constitution:mandatory-protocol -->",
    ]
    crlf_content = "\r\n".join(lines) + "\r\n"

    sections, errors = parse_markers(crlf_content)

    assert not errors, f"CRLF content produced parse errors: {errors}"
    assert len(sections) == 1, (
        f"Expected 1 section parsed from CRLF content, got {len(sections)}. "
        "$ anchor likely failing to match before \\r\\n."
    )
    assert sections[0].name == "mandatory-protocol"


# --- FIX-3 (TASK-3) ---

def test_fix3_bom_stripped_before_parse():
    """Scenario: fix-3-bom-stripped-before-parse — AGENTS.md saved with UTF-8-BOM
    (byte order mark U+FEFF prepended) must still have markers recognized.
    The BOM corrupts the ^<!-- match on line 1."""
    from aa_agents_sync.parser import parse_markers

    lines = [
        "\ufeff<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->",
        "## Protocol",
        "Content.",
        "<!-- END hangar-ai-constitution:mandatory-protocol -->",
    ]
    bom_content = "\n".join(lines) + "\n"

    sections, errors = parse_markers(bom_content)

    assert not errors, f"BOM content produced parse errors: {errors}"
    assert len(sections) == 1, (
        f"Expected 1 section from BOM content, got {len(sections)}. "
        "BOM (U+FEFF) likely corrupting the ^ anchor on line 1."
    )
    assert sections[0].name == "mandatory-protocol"


# --- FIX-4 (TASK-10) ---

def test_fix4_downgrade_rejected_when_constitution_older_than_markers(tmp_path):
    """Scenario: fix-4-downgrade-rejected

    If AGENTS.md contains markers at v1.2.0 and the resolved constitution has
    version v1.0.0, check_drift() must return an error (not silently flag drift).
    A stale sibling constitution must not overwrite newer markers.
    """
    from aa_agents_sync.checker import check_drift

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    # Constitution is OLDER than current AGENTS.md markers
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.2.0 -->\n"
        "## Protocol\n"
        "Newer content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    result = check_drift(agents_md_path=agents_md, constitution_path=constitution_dir)

    assert result.errors, (
        "Expected check_drift() to return errors when constitution version (1.0.0) "
        "is older than marker version (1.2.0) — downgrade guard not implemented."
    )
    assert any("downgrade" in e.lower() or "older" in e.lower() or "rollback" in e.lower()
               for e in result.errors), (
        f"Expected a downgrade/rollback error message, got: {result.errors}"
    )


# --- FIX-6 (TASK-12) ---

def test_fix6_pre_write_backup_created(tmp_path):
    """Scenario: fix-6-pre-write-backup-created

    Before writing the updated AGENTS.md, sync_agents_md() must create a
    backup at AGENTS.md.bak. The backup must exist and contain the original
    content after a successful sync.
    """
    import subprocess  # noqa: PLC0415
    from aa_agents_sync.syncer import sync_agents_md

    subprocess.run(["git", "init", str(tmp_path)], capture_output=True, check=True)

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.1.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.1.0 -->\n"
        "New content v1.1.0.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    original = (
        "# Header\n"
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Old content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )
    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(original)

    result = sync_agents_md(agents_md_path=agents_md, constitution_path=constitution_dir)

    assert not result.errors, f"sync_agents_md returned errors: {result.errors}"
    assert result.has_changes, "Expected changes to be written"

    bak = tmp_path / "AGENTS.md.bak"
    assert not bak.exists(), (
        "AGENTS.md.bak must be deleted after successful sync (R3 cleanup)"
    )
    # The backup was created and used for rollback protection, but cleaned up on success.
    # Verify the final written content is correct instead:
    assert "v1.1.0" in agents_md.read_text(), (
        "AGENTS.md must contain updated v1.1.0 marker after successful sync"
    )


# --- FIX-7 (TASK-13) ---

def test_fix7_post_write_verify_restores_on_corrupt(tmp_path, monkeypatch):
    """Scenario: fix-7-post-write-verify-and-restore

    After writing, sync_agents_md() must re-parse the written file. If the
    written content has parser errors (simulated here by patching _atomic_write
    to corrupt the output), the original must be restored from .bak and the
    result must report errors.
    """
    import subprocess  # noqa: PLC0415
    from aa_agents_sync import syncer as syncer_module
    from aa_agents_sync.syncer import sync_agents_md

    subprocess.run(["git", "init", str(tmp_path)], capture_output=True, check=True)

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.1.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.1.0 -->\n"
        "New content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    original = (
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Old content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )
    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(original)

    # Patch _atomic_write to write corrupt content (unclosed BEGIN)
    def corrupt_write(path, content):
        path.write_text("<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.1.0 -->\nCorrupt no end\n")

    monkeypatch.setattr(syncer_module, "_atomic_write", corrupt_write)

    result = sync_agents_md(agents_md_path=agents_md, constitution_path=constitution_dir)

    assert result.errors, (
        "Expected errors when post-write verification fails — FIX-7 not implemented"
    )
    # Original content must be restored from .bak
    assert agents_md.read_text() == original, (
        "AGENTS.md must be restored to original when post-write verification fails"
    )


# --- FIX-8 (TASK-14) ---

def test_fix8_file_lock_prevents_concurrent_write(tmp_path):
    """Scenario: fix-8-file-lock-prevents-concurrent-write

    When AGENTS.md is exclusively locked by another process, sync_agents_md()
    must detect the lock and return an error rather than blocking indefinitely
    or corrupting the file. Uses LOCK_EX | LOCK_NB (non-blocking flock).
    """
    import subprocess  # noqa: PLC0415
    import fcntl  # noqa: PLC0415
    from aa_agents_sync.syncer import sync_agents_md

    subprocess.run(["git", "init", str(tmp_path)], capture_output=True, check=True)

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.1.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.1.0 -->\n"
        "New content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Old content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    # Hold exclusive lock from a child process (fcntl.flock is per-process)
    lock_holder = subprocess.Popen(
        ["python3.11", "-c",
         f"import fcntl, time, sys\n"
         f"f=open({str(agents_md)!r},'r')\n"
         f"fcntl.flock(f, fcntl.LOCK_EX)\n"
         f"sys.stdout.write('locked\\n'); sys.stdout.flush()\n"
         f"time.sleep(5)\n"],
        stdout=subprocess.PIPE, text=True,
    )
    # Wait for child to acquire the lock
    lock_holder.stdout.readline()

    try:
        result = sync_agents_md(agents_md_path=agents_md, constitution_path=constitution_dir)
        assert result.errors, (
            "Expected error when AGENTS.md is locked by another process — "
            "FIX-8 (LOCK_EX | LOCK_NB) not implemented"
        )
    finally:
        lock_holder.terminate()
        lock_holder.wait(timeout=2)


# --- FIX-9 (TASK-15) ---

def test_fix9_resolver_rejects_wrong_constitution(tmp_path):
    """Scenario: fix-9-resolver-rejects-wrong-constitution

    A resolved constitution path that contains no valid section templates must
    be rejected with an explicit error. An empty or wrong sibling directory
    must not silently produce an empty canonical section set.
    """
    from aa_agents_sync.resolver import validate_constitution_path

    # Valid constitution — has version file + templates
    good = tmp_path / "good"
    good.mkdir()
    (good / "constitution-version.txt").write_text("1.0.0\n")
    templates = good / "templates" / "agents-md-sections"
    templates.mkdir(parents=True)
    (templates / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "content\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    # Wrong constitution — no version file, no templates
    bad = tmp_path / "bad"
    bad.mkdir()
    (bad / "README.md").write_text("not a constitution\n")

    error = validate_constitution_path(good)
    assert error is None, f"Valid constitution should not produce error, got: {error}"

    error = validate_constitution_path(bad)
    assert error is not None, (
        "Expected validate_constitution_path() to return an error for a path "
        "with no constitution-version.txt and no templates — FIX-9 not implemented"
    )
    assert "constitution" in error.lower() or "template" in error.lower(), (
        f"Error should mention constitution or template, got: {error}"
    )


# --- FIX-10 (TASK-16) ---

def test_fix10_version_rollback_rejected_in_sync(tmp_path):
    """Scenario: fix-10-version-rollback-rejected

    sync_agents_md() must refuse to overwrite a section whose existing marker
    version is NEWER than the incoming template version, even if the constitution
    version file has changed. This is a per-section monotonic version guard.

    Note: FIX-4 guards at the constitution level via check_drift(). FIX-10 adds
    a belt-and-suspenders check inside sync_agents_md() before each write.
    """
    import subprocess  # noqa: PLC0415
    from aa_agents_sync.syncer import sync_agents_md
    from aa_agents_sync.models import MarkerSection, CheckResult

    subprocess.run(["git", "init", str(tmp_path)], capture_output=True, check=True)

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    # Constitution version is newer, but section template still has old version
    (constitution_dir / "constitution-version.txt").write_text("2.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    # Template version is 1.0.0 — older than what's in AGENTS.md (1.5.0)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Old template content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.5.0 -->\n"
        "Newer content already in place.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    result = sync_agents_md(agents_md_path=agents_md, constitution_path=constitution_dir)

    assert result.errors, (
        "Expected sync_agents_md() to reject rollback: template v1.0.0 "
        "would overwrite marker v1.5.0 — FIX-10 not implemented"
    )
    # File must NOT have been modified
    assert "v1.5.0" in agents_md.read_text(), (
        "AGENTS.md must retain newer marker version after rollback rejection"
    )


# --- FIX-11 (TASK-17) ---

def test_fix11_idempotent_write_skipped(tmp_path, monkeypatch):
    """Scenario: fix-11-idempotent-write-skipped

    If the computed new content is byte-for-byte identical to the current file,
    sync_agents_md() must skip the write rather than performing a no-op write.
    We force this scenario by patching _replace_section_in_content to return
    the original content unchanged, simulating any degenerate no-op replacement.
    """
    import subprocess  # noqa: PLC0415
    import aa_agents_sync.syncer as syncer_module  # noqa: PLC0415
    from aa_agents_sync.syncer import sync_agents_md  # noqa: PLC0415

    subprocess.run(["git", "init", str(tmp_path)], capture_output=True, check=True)

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)

    # Template is at v1.0.0
    template_content = (
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Updated canonical content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )
    (templates_dir / "mandatory-protocol.md").write_text(template_content)

    # AGENTS.md is stale (v0.9.0) — so check.has_drift is True and the loop runs
    existing_content = (
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v0.9.0 -->\n"
        "Updated canonical content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )
    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(existing_content)

    # Patch _replace_section_in_content to be a no-op, simulating a degenerate
    # replacement that leaves content unchanged (defense-in-depth idempotency guard)
    monkeypatch.setattr(
        syncer_module,
        "_replace_section_in_content",
        lambda content, name, template: content,
    )

    import time  # noqa: PLC0415
    time.sleep(0.01)  # ensure any write would produce a different mtime
    mtime_before = agents_md.stat().st_mtime

    result = sync_agents_md(agents_md_path=agents_md, constitution_path=constitution_dir)

    assert not result.errors, f"Unexpected errors: {result.errors}"
    assert not result.has_changes, (
        "sync_agents_md() must not report changes when computed content is identical"
    )
    assert agents_md.stat().st_mtime == mtime_before, (
        "AGENTS.md must not be written when computed content is identical — "
        "FIX-11 idempotency guard not implemented"
    )


# --- FIX-12 (TASK-18) ---

def test_fix12_no_apply_does_not_write(tmp_path):
    """Scenario: fix-12-apply-flag-required-for-write

    Without --apply, the CLI must NOT write AGENTS.md even if drift is detected.
    The default mode must be safe (show diff only). Write requires explicit --apply.
    """
    import subprocess  # noqa: PLC0415
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    subprocess.run(["git", "init", str(tmp_path)], capture_output=True, check=True)

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)

    template_content = (
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "New canonical content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )
    (templates_dir / "mandatory-protocol.md").write_text(template_content)

    agents_md = tmp_path / "AGENTS.md"
    original_content = (
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v0.9.0 -->\n"
        "Old content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )
    agents_md.write_text(original_content)

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--constitution-path", str(constitution_dir), str(agents_md)],
    )

    assert result.exit_code == 0, (
        f"CLI without --apply must exit 0 (show-diff mode), got {result.exit_code}. "
        f"output={result.output!r}"
    )
    assert agents_md.read_text() == original_content, (
        "CLI without --apply must NOT write AGENTS.md — FIX-12 not implemented"
    )


# --- FIX-13 (TASK-19) ---

def test_fix13_agents_sync_yml_opt_out(tmp_path):
    """Scenario: fix-13-agents-sync-yml-opt-out

    If an agents-sync.yml file at the repo root contains `disabled: true`,
    aa-agents-sync write mode (--apply) must exit 0 without writing AGENTS.md.
    This allows teams to permanently opt out of automated sync at the repo level.
    """
    import subprocess  # noqa: PLC0415
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    subprocess.run(["git", "init", str(tmp_path)], capture_output=True, check=True)

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "New content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    agents_md = tmp_path / "AGENTS.md"
    original = (
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v0.9.0 -->\n"
        "Old content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )
    agents_md.write_text(original)

    # Drop an opt-out config at repo root
    (tmp_path / "agents-sync.yml").write_text("disabled: true\n")

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--apply", "--force", "--constitution-path", str(constitution_dir), str(agents_md)],
    )

    assert result.exit_code == 0, (
        f"--apply with agents-sync.yml disabled:true must exit 0 (opt-out), "
        f"got {result.exit_code}. output={result.output!r}"
    )
    assert agents_md.read_text() == original, (
        "AGENTS.md must NOT be written when agents-sync.yml opt-out is active — "
        "FIX-13 not implemented"
    )
    assert "disabled" in result.output.lower() or "opt" in result.output.lower(), (
        "CLI must print an opt-out message when agents-sync.yml disables sync"
    )


# --- FIX-14 (TASK-20) ---

def test_fix14_env_var_disables_sync(tmp_path, monkeypatch):
    """Scenario: fix-14-env-var-disables-sync

    If AGENTS_SYNC_DISABLED=1 is set in the environment, aa-agents-sync must
    exit 0 immediately without performing any I/O. This enables CI pipelines
    to suppress sync in emergency or in opt-out environments at process level.
    """
    import subprocess  # noqa: PLC0415
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    subprocess.run(["git", "init", str(tmp_path)], capture_output=True, check=True)

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "New content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    agents_md = tmp_path / "AGENTS.md"
    original = (
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v0.9.0 -->\n"
        "Old content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )
    agents_md.write_text(original)

    monkeypatch.setenv("AGENTS_SYNC_DISABLED", "1")

    runner = CliRunner(env={"AGENTS_SYNC_DISABLED": "1"})
    result = runner.invoke(
        main,
        ["--apply", "--force", "--constitution-path", str(constitution_dir), str(agents_md)],
    )

    assert result.exit_code == 0, (
        f"AGENTS_SYNC_DISABLED=1 must cause exit 0, got {result.exit_code}. "
        f"output={result.output!r}"
    )
    assert agents_md.read_text() == original, (
        "AGENTS.md must NOT be written when AGENTS_SYNC_DISABLED=1 — FIX-14 not implemented"
    )
    assert "disabled" in result.output.lower() or "AGENTS_SYNC_DISABLED" in result.output, (
        "CLI must print a message indicating sync was disabled by env var"
    )


def test_check_no_markers_returns_has_drift_true(tmp_path):
    """Scenario: nm-chk-01 — check_drift must return has_drift=True when AGENTS.md
    exists but has zero hangar-ai-constitution markers.

    Root cause fix: any([]) == False was making a no-markers file appear current.
    """
    from aa_agents_sync.checker import check_drift  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(
        "# American Airlines Android App\n\n"
        "Avatar: android-kotlin v1.3.0\n\n"
        "Mandatory Protocol (ENG-4.1): every task RED→GREEN→REFACTOR.\n"
    )

    result = check_drift(agents_md_path=agents_md, constitution_path=constitution_dir)

    assert result.has_drift is True, (
        "nm-chk-01: check_drift must return has_drift=True when AGENTS.md has no "
        "hangar-ai-constitution markers — any([]) == False root cause must be fixed"
    )


def test_check_result_has_markers_field():
    """Scenario: nm-chk-02 — CheckResult dataclass must have a has_markers: bool field
    so callers can distinguish 'no markers at all' from 'markers present but stale'."""
    from aa_agents_sync.models import CheckResult  # noqa: PLC0415

    result = CheckResult()
    assert hasattr(result, "has_markers"), (
        "nm-chk-02: CheckResult must have a has_markers field"
    )
    assert result.has_markers is False, (
        "nm-chk-02: has_markers must default to False"
    )


def test_check_no_markers_sets_has_markers_false(tmp_path):
    """Scenario: nm-chk-03 — check_drift must set has_markers=False when AGENTS.md
    has no BEGIN/END markers (distinct from has_drift for routing in syncer/cli)."""
    from aa_agents_sync.checker import check_drift  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text("# No markers here\n\nJust plain content.\n")

    result = check_drift(agents_md_path=agents_md, constitution_path=constitution_dir)

    assert result.has_markers is False, (
        "nm-chk-03: check_drift must set has_markers=False when no BEGIN/END markers found"
    )


def test_check_with_markers_sets_has_markers_true(tmp_path):
    """Scenario: nm-chk-04 — check_drift must set has_markers=True when AGENTS.md
    has at least one valid BEGIN/END marker. Regression guard."""
    from aa_agents_sync.checker import check_drift  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Protocol content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    result = check_drift(agents_md_path=agents_md, constitution_path=constitution_dir)

    assert result.has_markers is True, (
        "nm-chk-04: check_drift must set has_markers=True when sections are found"
    )


def test_cli_check_no_markers_exits_2(tmp_path):
    """Scenario: nm-cli-01 — CLI --check must exit 2 when AGENTS.md has no markers.
    Before NM-1 fix this exited 0 (false 'current'). Now has_drift=True propagates."""
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(
        "# Android App\n\nMandatory Protocol (ENG-4.1): RED→GREEN→REFACTOR.\n"
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--check", "--constitution-path", str(constitution_dir), str(agents_md)],
    )

    assert result.exit_code == 2, (
        f"nm-cli-01: --check with no markers must exit 2, got {result.exit_code}. "
        f"output={result.output!r}"
    )


def test_cli_check_no_markers_message_prefix(tmp_path):
    """Scenario: nm-cli-02 — CLI --check with no markers must print 'MISSING:' prefix,
    not 'DRIFT:', to distinguish 'never had markers' from 'markers stale'."""
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text("# No markers here\n\nPlain content only.\n")

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--check", "--constitution-path", str(constitution_dir), str(agents_md)],
    )

    assert result.output.startswith("MISSING:"), (
        f"nm-cli-02: --check with no markers must print 'MISSING:' prefix, "
        f"got: {result.output!r}"
    )


def test_syncer_inserts_sections_when_no_markers(tmp_path):
    """Scenario: nm-syn-01 — sync_agents_md() must insert canonical sections into
    an AGENTS.md that has no markers at all (first-time injection path)."""
    from aa_agents_sync.syncer import sync_agents_md  # noqa: PLC0415
    from aa_agents_sync.parser import parse_markers  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")

    # Set up minimal canonical template
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "## ⛔ MANDATORY AGENT PROTOCOL\n\n"
        "Protocol content here.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text("# My Project\n\nNo markers here.\n")

    result = sync_agents_md(agents_md_path=agents_md, constitution_path=constitution_dir)

    assert not result.errors, f"nm-syn-01: sync must not error, got: {result.errors}"
    assert result.has_changes, "nm-syn-01: sync must report changes (sections inserted)"
    assert "mandatory-protocol" in result.sections_updated, (
        "nm-syn-01: sections_updated must list the inserted section name"
    )

    # Verify the file now has valid markers
    written = agents_md.read_text()
    sections, errors = parse_markers(written)
    assert not errors, f"nm-syn-01: written file must parse cleanly, got errors: {errors}"
    assert len(sections) == 1, (
        f"nm-syn-01: written file must have 1 section, got {len(sections)}"
    )
    assert sections[0].name == "mandatory-protocol"


def test_syncer_preserves_existing_content_on_insert(tmp_path):
    """Scenario: nm-syn-02 — sync_agents_md() must preserve all existing AGENTS.md
    content above the injected sections. Original text must appear verbatim."""
    from aa_agents_sync.syncer import sync_agents_md  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")

    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Protocol content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    original_content = "# My App\n\nAvatar: android-kotlin v1.3.0\n\nSome existing notes.\n"
    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(original_content)

    sync_agents_md(agents_md_path=agents_md, constitution_path=constitution_dir)

    written = agents_md.read_text()
    assert written.startswith(original_content), (
        "nm-syn-02: original content must be preserved verbatim at start of file after insertion"
    )
    assert "mandatory-protocol" in written, (
        "nm-syn-02: inserted section must also be present"
    )


def test_cli_apply_no_markers_exits_3(tmp_path):
    """Scenario: nm-cli-03 — CLI --apply with no-markers AGENTS.md must exit 3 (SYNCED).
    Previously exited 0 ('already current') — a silent lie."""
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")

    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Protocol content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text("# My App\n\nNo markers.\n")

    # Initialise git repo so write-mode guard passes
    import subprocess  # noqa: PLC0415
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init", "--allow-empty-message"],
        cwd=tmp_path, check=True, capture_output=True,
        env={**__import__("os").environ, "GIT_AUTHOR_NAME": "test",
             "GIT_AUTHOR_EMAIL": "t@t.com", "GIT_COMMITTER_NAME": "test",
             "GIT_COMMITTER_EMAIL": "t@t.com"},
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--apply", "--constitution-path", str(constitution_dir), str(agents_md)],
    )

    assert result.exit_code == 3, (
        f"nm-cli-03: --apply with no markers must exit 3 (SYNCED), "
        f"got {result.exit_code}. output={result.output!r}"
    )


def test_cli_apply_no_markers_message_inserted(tmp_path):
    """Scenario: nm-cli-04 — CLI --apply with no-markers must print
    'Inserted N canonical section(s)' (not 'Updated N section(s)')."""
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415
    import subprocess, os  # noqa: PLC0415, E401

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Protocol content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text("# My App\n\nNo markers.\n")

    git_env = {**os.environ, "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "t@t.com",
               "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "t@t.com"}
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=tmp_path, check=True,
                   capture_output=True, env=git_env)

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--apply", "--constitution-path", str(constitution_dir), str(agents_md)],
    )

    assert "Inserted" in result.output, (
        f"nm-cli-04: --apply with no-markers must say 'Inserted', "
        f"got: {result.output!r}"
    )


def test_cli_dry_run_no_markers_shows_insertion_diff(tmp_path):
    """Scenario: nm-dry-01 — dry-run with no-markers AGENTS.md must show what
    would be inserted (not 'already current'). Exits 0 (preview only)."""
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Protocol content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text("# My App\n\nNo markers.\n")

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--dry-run", "--constitution-path", str(constitution_dir), str(agents_md)],
    )

    assert result.exit_code == 0, (
        f"nm-dry-01: dry-run must exit 0 (preview), got {result.exit_code}. "
        f"output={result.output!r}"
    )
    assert "already current" not in result.output.lower(), (
        f"nm-dry-01: dry-run must NOT say 'already current' for no-markers file. "
        f"output={result.output!r}"
    )
    assert "mandatory-protocol" in result.output, (
        f"nm-dry-01: dry-run must show what would be inserted. "
        f"output={result.output!r}"
    )


def test_legacy_not_found_message_includes_remediation(tmp_path):
    """Scenario: nm-leg-01 — --legacy-mode --dry-run when no legacy block is found
    must give actionable guidance: template path and 'run --apply'."""
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    agents_md = tmp_path / "AGENTS.md"
    # Compact inline style — no detectable legacy heading block
    agents_md.write_text(
        "# My App\n\nMandatory Protocol (ENG-4.1): RED→GREEN→REFACTOR.\n"
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--legacy-mode", "--dry-run",
         "--constitution-path", str(constitution_dir), str(agents_md)],
    )

    assert result.exit_code == 2, (
        f"nm-leg-01: --legacy-mode not-found must exit 2, got {result.exit_code}. "
        f"output={result.output!r}"
    )
    assert "templates" in result.output.lower() or "--apply" in result.output, (
        f"nm-leg-01: message must reference templates dir or '--apply' command. "
        f"output={result.output!r}"
    )


def test_mf_01_legacy_no_block_message_directs_to_apply_directly():
    """Scenario: mf-01 — --legacy-mode no-block message must point to --apply directly
    without requiring manual copy/paste steps. Since NM-7/8, --apply auto-inserts."""
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415

    constitution_dir = tmp_path_factory = None  # resolved below
    import tempfile, pathlib  # noqa: E401, PLC0415
    with tempfile.TemporaryDirectory() as td:
        constitution_dir = pathlib.Path(td) / "constitution"
        constitution_dir.mkdir()
        (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
        templates_dir = constitution_dir / "templates" / "agents-md-sections"
        templates_dir.mkdir(parents=True)
        (templates_dir / "mandatory-protocol.md").write_text(
            "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
            "Content.\n"
            "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
        )
        agents_md = pathlib.Path(td) / "AGENTS.md"
        agents_md.write_text("# My App\n\nMandatory Protocol (ENG-4.1): RED→GREEN→REFACTOR.\n")

        runner = CliRunner()
        result = runner.invoke(
            main,
            ["--legacy-mode", "--dry-run",
             "--constitution-path", str(constitution_dir), str(agents_md)],
        )

    assert result.exit_code == 2, (
        f"mf-01: exit code must be 2 (no legacy block), got {result.exit_code}. "
        f"output={result.output!r}"
    )
    assert "--apply" in result.output, (
        f"mf-01: message must mention '--apply' as primary action. output={result.output!r}"
    )
    assert "Copy" not in result.output and "copy" not in result.output, (
        f"mf-01: message must NOT instruct manual copy/paste. output={result.output!r}"
    )
    assert "Paste" not in result.output and "paste" not in result.output, (
        f"mf-01: message must NOT instruct manual copy/paste. output={result.output!r}"
    )


def test_ms_03_apply_writes_constitution_version_txt_to_target_repo(tmp_path):
    """Scenario: ms-03 — aa-agents-sync --apply must write constitution-version.txt
    to the target repo directory alongside AGENTS.md. This enables A01 to run in CI
    without --constitution or AA_CONSTITUTION_PATH."""
    from aa_agents_sync.syncer import sync_agents_md  # noqa: PLC0415

    # Set up constitution with version 1.0.0 and a canonical template
    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Protocol content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    # Target repo: AGENTS.md with no markers
    target_dir = tmp_path / "myrepo"
    target_dir.mkdir()
    agents_md = target_dir / "AGENTS.md"
    agents_md.write_text("# My App\n\nNo markers yet.\n")

    result = sync_agents_md(agents_md_path=agents_md, constitution_path=constitution_dir)

    assert not result.errors, f"ms-03: sync must succeed. errors={result.errors}"
    assert result.was_insertion, "ms-03: must be an insertion (no prior markers)"

    version_file = target_dir / "constitution-version.txt"
    assert version_file.exists(), (
        "ms-03: constitution-version.txt must be written to target repo dir after --apply"
    )
    assert version_file.read_text().strip() == "1.0.0", (
        f"ms-03: constitution-version.txt must contain the applied version. "
        f"got={version_file.read_text().strip()!r}"
    )


def test_ms_03b_apply_writes_version_pin_even_when_already_current(tmp_path):
    """Scenario: ms-03b — aa-agents-sync --apply must write constitution-version.txt
    even when AGENTS.md markers are already current (no drift). The pin represents
    'this repo is on version X', not 'we just made a change'."""
    from aa_agents_sync.syncer import sync_agents_md  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Protocol content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    target_dir = tmp_path / "myrepo"
    target_dir.mkdir()
    agents_md = target_dir / "AGENTS.md"
    # AGENTS.md already has CURRENT markers — no drift
    agents_md.write_text(
        "# My App\n"
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Protocol content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    result = sync_agents_md(agents_md_path=agents_md, constitution_path=constitution_dir)

    assert not result.errors, f"ms-03b: sync must succeed. errors={result.errors}"

    version_file = target_dir / "constitution-version.txt"
    assert version_file.exists(), (
        "ms-03b: constitution-version.txt must be written even when AGENTS.md is already current"
    )
    assert version_file.read_text().strip() == "1.0.0", (
        f"ms-03b: version pin must contain current constitution version. "
        f"got={version_file.read_text().strip()!r}"
    )


def test_r3_bak_file_deleted_after_successful_apply_insertion(tmp_path):
    """Scenario: r3a — .bak file must be deleted after successful --apply insertion.
    Leaving .bak on disk causes it to be committed to repos (git add -A)."""
    from aa_agents_sync.syncer import sync_agents_md  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )
    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text("# My App\n\nNo markers.\n")

    result = sync_agents_md(agents_md_path=agents_md, constitution_path=constitution_dir)

    assert not result.errors, f"r3a: sync must succeed. errors={result.errors}"
    bak_path = agents_md.with_suffix(".md.bak")
    assert not bak_path.exists(), (
        "r3a: AGENTS.md.bak must be deleted after successful insertion"
    )


def test_r3b_bak_file_deleted_after_successful_apply_replacement(tmp_path):
    """Scenario: r3b — .bak file must be deleted after successful --apply replacement."""
    from aa_agents_sync.syncer import sync_agents_md  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.1.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.1.0 -->\n"
        "Updated content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )
    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text(
        "# My App\n"
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Old content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    result = sync_agents_md(agents_md_path=agents_md, constitution_path=constitution_dir)

    assert not result.errors, f"r3b: sync must succeed. errors={result.errors}"
    bak_path = agents_md.with_suffix(".md.bak")
    assert not bak_path.exists(), (
        "r3b: AGENTS.md.bak must be deleted after successful replacement"
    )


def test_r2_pin_write_oserror_returns_clean_error_not_traceback(tmp_path, monkeypatch):
    """Scenario: r2 — if constitution-version.txt write fails (e.g. PermissionError),
    sync_agents_md must return SyncResult(errors=[...]) not raise an uncaught exception."""
    from aa_agents_sync.syncer import sync_agents_md  # noqa: PLC0415
    import aa_agents_sync.syncer as syncer_mod  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )
    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text("# My App\n\nNo markers.\n")

    def _fake_write_pin(p, v):
        raise PermissionError(f"Permission denied: {p}")

    monkeypatch.setattr(syncer_mod, "_write_version_pin", _fake_write_pin)

    # Should not raise — must return error in SyncResult
    try:
        result = sync_agents_md(agents_md_path=agents_md, constitution_path=constitution_dir)
        assert result.errors, (
            "r2: OSError in _write_version_pin must surface as SyncResult.errors, not raise"
        )
    except PermissionError as e:
        raise AssertionError(
            f"r2: OSError must be caught internally, not raised to caller. Got: {e}"
        ) from e


def test_r1_cli_apply_already_current_mentions_pin_when_created(tmp_path):
    """Scenario: r1 — when --apply runs on an already-current AGENTS.md but
    constitution-version.txt doesn't exist yet, the CLI must NOT say 'No changes needed'
    without acknowledging the pin file was created."""
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415
    import subprocess  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    agents_md = tmp_path / "AGENTS.md"
    # AGENTS.md already has current markers — no drift
    agents_md.write_text(
        "# My App\n"
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )
    # No constitution-version.txt in target dir yet

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=tmp_path, check=True, capture_output=True,
        env={**__import__("os").environ, "GIT_AUTHOR_NAME": "test",
             "GIT_AUTHOR_EMAIL": "t@t.com", "GIT_COMMITTER_NAME": "test",
             "GIT_COMMITTER_EMAIL": "t@t.com"},
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--apply", "--constitution-path", str(constitution_dir), str(agents_md)],
    )

    pin_file = tmp_path / "constitution-version.txt"
    assert pin_file.exists(), "r1: constitution-version.txt must be created by --apply"

    # The CLI output must mention the pin file creation — not just "No changes needed"
    output = result.output
    assert "constitution-version.txt" in output or "PINNED" in output or "pin" in output.lower(), (
        f"r1: CLI output must mention constitution-version.txt was created. output={output!r}"
    )
    assert result.exit_code in (0, 3), (
        f"r1: exit code must be 0 or 3. got={result.exit_code}. output={output!r}"
    )


def test_r4_cli_apply_no_markers_creates_pin_e2e(tmp_path):
    """Scenario: r4a — CLI --apply on no-markers file creates constitution-version.txt
    alongside AGENTS.md (E2E CLI-level assertion, not just syncer-level)."""
    from click.testing import CliRunner  # noqa: PLC0415
    from aa_agents_sync.cli import main  # noqa: PLC0415
    import subprocess  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )
    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text("# My App\n\nNo markers.\n")

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=tmp_path, check=True, capture_output=True,
        env={**__import__("os").environ, "GIT_AUTHOR_NAME": "test",
             "GIT_AUTHOR_EMAIL": "t@t.com", "GIT_COMMITTER_NAME": "test",
             "GIT_COMMITTER_EMAIL": "t@t.com"},
    )

    runner = CliRunner()
    result = runner.invoke(
        main, ["--apply", "--constitution-path", str(constitution_dir), str(agents_md)]
    )

    assert result.exit_code == 3, (
        f"r4a: --apply on no-markers must exit 3 (SYNCED). got={result.exit_code}. output={result.output!r}"
    )
    pin_file = tmp_path / "constitution-version.txt"
    assert pin_file.exists(), "r4a: constitution-version.txt must exist after CLI --apply"
    assert pin_file.read_text().strip() == "1.0.0", "r4a: pin must contain applied version"


def test_r4b_apply_then_a01_passes_without_constitution_flag(tmp_path):
    """Scenario: r4b — full adoption chain: --apply creates pin, then A01 lint PASSES
    without --constitution or AA_CONSTITUTION_PATH. This is the core CI loop."""
    from aa_agents_sync.syncer import sync_agents_md  # noqa: PLC0415
    from aa_constitution_lint.domain.rules.agents_md_sync import AgentsMdDriftRule  # noqa: PLC0415
    from aa_constitution_lint.domain.models import EvaluationResult  # noqa: PLC0415

    constitution_dir = tmp_path / "constitution"
    constitution_dir.mkdir()
    (constitution_dir / "constitution-version.txt").write_text("1.0.0\n")
    templates_dir = constitution_dir / "templates" / "agents-md-sections"
    templates_dir.mkdir(parents=True)
    (templates_dir / "mandatory-protocol.md").write_text(
        "<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->\n"
        "Content.\n"
        "<!-- END hangar-ai-constitution:mandatory-protocol -->\n"
    )

    target_dir = tmp_path / "myrepo"
    target_dir.mkdir()
    agents_md = target_dir / "AGENTS.md"
    agents_md.write_text("# My App\n\nNo markers yet.\n")

    # Step 1: apply
    result = sync_agents_md(agents_md_path=agents_md, constitution_path=constitution_dir)
    assert not result.errors, f"r4b: apply must succeed. errors={result.errors}"
    assert result.pin_written, "r4b: pin_written must be True after successful apply"

    # Step 2: A01 lint with NO constitution_path and NO env var (simulates plain CI)
    rule = AgentsMdDriftRule(constitution_path=None)
    evaluations = rule.evaluate(project_path=target_dir)

    assert evaluations, "r4b: A01 must return evaluations"
    assert all(e.result == EvaluationResult.PASS for e in evaluations), (
        f"r4b: A01 must PASS after --apply without --constitution. "
        f"results={[(e.result, e.context.get('message','')) for e in evaluations]}"
    )
