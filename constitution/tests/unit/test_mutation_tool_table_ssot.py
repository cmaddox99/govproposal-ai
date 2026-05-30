"""
RED test — mutation-tool-table-ssot: Skill-11 Go tool must be gremlins (not cosmic-ray).

Multi-LLM jury (2026-05-26) confirmed cosmic-ray is a Python mutation framework;
gremlins (github.com/go-gremlins/gremlins) is the correct Go mutation tool.
Workflow legacy-rescue-refactor.md already uses gremlins correctly.

Spec scenario: mutation-tool-table-ssot
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
SKILL_11 = REPO_ROOT / "agent-skills" / "skills-by-domain" / "development-practices" / "11-mutation-testing.md"
LAW_TESTING = REPO_ROOT / "laws" / "engineering" / "testing.md"
WORKFLOW_LEGACY = REPO_ROOT / "workflows" / "legacy-rescue-refactor.md"


# ---------------------------------------------------------------------------
# TASK-2: Go tool in skill-11 must be gremlins
# ---------------------------------------------------------------------------

def test_skill11_go_tool_is_gremlins():
    """Go row in skill-11 tool table must name gremlins, not cosmic-ray."""
    content = SKILL_11.read_text(encoding="utf-8")
    go_rows = [line for line in content.splitlines() if line.startswith("| Go ") or line.startswith("| Go|")]
    assert go_rows, "Go row not found in skill-11 tool table"
    assert "gremlins" in go_rows[0], f"Go tool must be gremlins; found: {go_rows[0]}"


def test_skill11_go_row_has_no_cosmic_ray():
    """cosmic-ray must not appear in the skill-11 Go row."""
    content = SKILL_11.read_text(encoding="utf-8")
    go_rows = [line for line in content.splitlines() if line.startswith("| Go ") or line.startswith("| Go|")]
    assert go_rows, "Go row not found in skill-11 tool table"
    assert "cosmic-ray" not in go_rows[0], f"cosmic-ray must not appear in Go row; found: {go_rows[0]}"


def test_skill11_go_command_is_gremlins_unleash():
    """Go command in skill-11 must be 'gremlins unleash' (no positional ./... arg)."""
    content = SKILL_11.read_text(encoding="utf-8")
    go_rows = [line for line in content.splitlines() if line.startswith("| Go ") or line.startswith("| Go|")]
    assert go_rows, "Go row not found in skill-11 tool table"
    assert "gremlins unleash" in go_rows[0], f"Go command must contain 'gremlins unleash'; found: {go_rows[0]}"
    assert "unleash ./..." not in go_rows[0], (
        "gremlins does not accept positional package args; use 'gremlins unleash' from module root"
    )


# ---------------------------------------------------------------------------
# TASK-2b: Workflow Go command must be gremlins unleash (no ./...)
# ---------------------------------------------------------------------------

def test_workflow_go_command_no_positional_args():
    """Workflow legacy-rescue Go command must not use 'gremlins unleash ./...'."""
    content = WORKFLOW_LEGACY.read_text(encoding="utf-8")
    go_rows = [line for line in content.splitlines() if "gremlins" in line and "|" in line]
    assert go_rows, "gremlins row not found in workflow Tech Stack Translation"
    for row in go_rows:
        assert "unleash ./..." not in row, (
            f"gremlins does not accept positional args; found: {row}"
        )


# ---------------------------------------------------------------------------
# TASK-3: Law must not contain tool table; must contain delegation sentence
# ---------------------------------------------------------------------------

def test_law_no_tool_selection_table():
    """ENG-4.11 law must not contain a | Language | Tool | table."""
    content = LAW_TESTING.read_text(encoding="utf-8")
    assert "| Language | Tool |" not in content, (
        "Tool selection table must be removed from laws/engineering/testing.md; "
        "skill-11 is the SSOT per mutation-tool-table-ssot proposal."
    )


def test_law_no_cosmic_ray():
    """cosmic-ray must not appear anywhere in laws/engineering/testing.md."""
    content = LAW_TESTING.read_text(encoding="utf-8")
    assert "cosmic-ray" not in content, "cosmic-ray is a Python tool; it must not appear in the Go law entry"


def test_law_delegation_references_skill11():
    """ENG-4.11 law must contain a delegation sentence referencing skill-11."""
    content = LAW_TESTING.read_text(encoding="utf-8")
    assert "11-mutation-testing.md" in content, (
        "Law must contain a delegation sentence pointing to skill-11 "
        "as the canonical source of mutation tool selection."
    )


def test_law_thresholds_preserved():
    """ENG-4.11 section must still contain the ≥70% and ≥85% mutation threshold lines."""
    content = LAW_TESTING.read_text(encoding="utf-8")
    eng4_11_section = re.search(
        r"## Section 4\.11.*?(?=## Section 4\.12|\Z)",
        content,
        re.DOTALL,
    )
    assert eng4_11_section, "## Section 4.11 not found in laws/engineering/testing.md"
    section = eng4_11_section.group(0)
    assert "≥70%" in section, "ENG-4.11 must retain ≥70% general mutation threshold"
    assert "≥85%" in section, "ENG-4.11 must retain ≥85% critical path mutation threshold"


# ---------------------------------------------------------------------------
# TASK-4: Workflow must have mutation-tool SSOT citation near Tech Stack table
# ---------------------------------------------------------------------------

def test_workflow_mutation_ssot_citation_near_tech_stack():
    """Workflow must cite skill-11 as mutation tool SSOT within the Tech Stack Translation section."""
    content = WORKFLOW_LEGACY.read_text(encoding="utf-8")
    tech_stack_idx = content.find("## Tech Stack Translation")
    assert tech_stack_idx != -1, "## Tech Stack Translation section not found in workflow"
    # Find the end of this section (next ## heading or EOF)
    next_section = content.find("\n## ", tech_stack_idx + 1)
    section_end = next_section if next_section != -1 else len(content)
    section = content[tech_stack_idx:section_end]
    assert "11-mutation-testing" in section, (
        "skill-11 citation must appear within ## Tech Stack Translation section"
    )
