"""Test 4.7: PROGRESS.md records governance sign-off section.

Scenario ID: c-plus-plus-avatar-enrichment/4.7
Law: ENG-6.7 (Audit Trail — governance decisions must be recorded)
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def test_progress_has_governance_signoffs():
    """PROGRESS.md must have a governance sign-off section with required checkpoints."""
    progress = (
        REPO_ROOT
        / "hangar-ai-specs"
        / "changes"
        / "c-plus-plus-avatar-enrichment"
        / "PROGRESS.md"
    ).read_text(encoding="utf-8")

    assert "Governance Sign-Off" in progress or "Sign-Off" in progress, \
        "PROGRESS.md must have a governance sign-off section"
    assert "ENG-4.1" in progress, "Must reference Atomic TDD compliance"
    assert "ENG-6.1" in progress, "Must reference Security by Design compliance"
    assert "ENG-10.1" in progress or "law reference" in progress.lower(), \
        "Must reference law reference validity"
