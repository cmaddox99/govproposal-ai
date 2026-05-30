"""Tests for agents-md-session-preflight — TASK-1 through TASK-5."""
from pathlib import Path
import stat

REPO_ROOT = Path(__file__).parent.parent.parent


# --- TASK-1 tests ---

def test_agent_md_has_section_0_preflight():
    """Scenario: session-preflight-in-agent-md — agent-skills/base/AGENT.md must
    contain a Section 0 Constitutional Preflight block marked NON-NEGOTIABLE,
    with preflight steps covering version check, auto-repair, and fallback chain."""
    agent_md = REPO_ROOT / "agent-skills" / "base" / "AGENT.md"
    assert agent_md.exists(), "agent-skills/base/AGENT.md must exist"

    content = agent_md.read_text()

    assert "## 0." in content or "## Section 0" in content, (
        "AGENT.md must contain a Section 0 block (## 0. or ## Section 0)"
    )
    assert "NON-NEGOTIABLE" in content or "non-negotiable" in content.lower(), (
        "Section 0 must be marked NON-NEGOTIABLE"
    )
    assert "constitution-version.txt" in content, (
        "Section 0 must reference constitution-version.txt as version source of truth"
    )
    assert "aa-agents-sync" in content, (
        "Section 0 must reference aa-agents-sync as the repair tool"
    )
    assert (
        "HARD STOP" in content
        or "--check" in content
        or "explicit user approval" in content
        or "user confirmation" in content
    ), (
        "Section 0 must either specify a HARD STOP or require explicit user approval before writing"
    )


# --- TASK-4 tests ---

def test_adoption_workflow_references_sync():
    """Scenario: adoption-workflow-references-sync — workflows/adoption.md must
    reference aa-agents-sync install, A01 lint requirement, and session preflight."""
    adoption_md = REPO_ROOT / "workflows" / "adoption.md"
    assert adoption_md.exists(), "workflows/adoption.md must exist"

    content = adoption_md.read_text()

    assert "aa-agents-sync" in content, (
        "adoption.md must reference the aa-agents-sync tool"
    )
    assert "pip install" in content or "pipx install" in content, (
        "adoption.md must include aa-agents-sync install instructions"
    )
    assert "A01" in content, (
        "adoption.md must reference the A01 lint rule (AGENTS.md marker drift check)"
    )
    assert "session preflight" in content.lower() or "section 0" in content.lower(), (
        "adoption.md must reference Section 0 / session preflight behavior"
    )


# --- TASK-3 tests ---

def test_constitution_agents_md_has_versioned_markers():
    """Scenario: constitution-agents-md-has-markers — AGENTS.md at the repo root
    must contain versioned BEGIN/END markers for mandatory-protocol at the current
    constitution version (from constitution-version.txt)."""
    agents_md = REPO_ROOT / "AGENTS.md"
    version_file = REPO_ROOT / "constitution-version.txt"
    assert agents_md.exists(), "AGENTS.md must exist"
    assert version_file.exists(), "constitution-version.txt must exist"

    version = version_file.read_text().strip()
    content = agents_md.read_text()

    expected_begin = f"<!-- BEGIN hangar-ai-constitution:mandatory-protocol v{version} -->"
    expected_end = "<!-- END hangar-ai-constitution:mandatory-protocol -->"

    assert expected_begin in content, (
        f"AGENTS.md must contain '{expected_begin}'. "
        "Run: aa-agents-sync --legacy-mode --dry-run AGENTS.md to preview migration."
    )
    assert expected_end in content, (
        f"AGENTS.md must contain '{expected_end}' closing marker."
    )

    begin_pos = content.index(expected_begin)
    end_pos = content.index(expected_end)
    assert begin_pos < end_pos, "BEGIN marker must appear before END marker"

    between = content[begin_pos:end_pos]
    assert "MANDATORY AGENT PROTOCOL" in between, (
        "The mandatory-protocol section content must be between the BEGIN/END markers"
    )


# --- TASK-2 tests ---

def test_post_merge_hook_exists_and_is_executable():
    """Scenario: post-merge-hook-runs-check — .githooks/post-merge must exist,
    be executable, call aa-agents-sync --check (not --apply), and be silent on
    success (no output when tool absent or drift-free)."""
    hook = REPO_ROOT / ".githooks" / "post-merge"
    assert hook.exists(), ".githooks/post-merge must exist"

    mode = hook.stat().st_mode
    assert mode & stat.S_IXUSR, ".githooks/post-merge must be user-executable (chmod +x)"

    content = hook.read_text()
    assert "aa-agents-sync" in content, "hook must invoke aa-agents-sync"
    assert "--check" in content, "hook must use --check (not --apply) per Stage 0 policy"
    assert "--apply" not in content, "hook must NOT use --apply in Stage 0"
    assert "command -v aa-agents-sync" in content or "which aa-agents-sync" in content, (
        "hook must guard: only run if aa-agents-sync is installed"
    )


# --- TASK-5 tests ---

def test_sync_troubleshooting_guide_exists():
    """Scenario: sync-troubleshooting-guide-exists — docs/guides/adoption/
    sync-troubleshooting.md must exist and cover fallback behavior, manual
    install steps, and Stage 0 check-only behavior."""
    guide = REPO_ROOT / "docs" / "guides" / "adoption" / "sync-troubleshooting.md"
    assert guide.exists(), "docs/guides/adoption/sync-troubleshooting.md must exist"

    content = guide.read_text()

    assert "aa-agents-sync" in content, "guide must reference aa-agents-sync"
    assert "pip install" in content or "pipx install" in content, (
        "guide must include manual install steps"
    )
    assert "stage 0" in content.lower() or "check-only" in content.lower(), (
        "guide must explain Stage 0 / check-only behavior"
    )
    assert "fallback" in content.lower(), (
        "guide must cover fallback behavior (tool absent, no markers, etc.)"
    )
    assert "--dry-run" in content, (
        "guide must reference --dry-run for previewing changes"
    )
