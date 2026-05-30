"""Test ESE-00.3: PROGRESS.md records governance sign-off for cpp-external-sources-enrichment.

Scenario ID: cpp-external-sources-enrichment/ESE-00.3
Law: ENG-6.7 (Audit Trail — governance decisions must be recorded)
     ENG-11.1 (Hangar SDD — change proposals require execution artifacts)
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
PROGRESS = (
    REPO_ROOT
    / "hangar-ai-specs"
    / "changes"
    / "cpp-external-sources-enrichment"
    / "PROGRESS.md"
)


def test_ese_progress_md_exists_with_governance_signoff():
    """PROGRESS.md must exist and contain a governance sign-off section (ENG-6.7)."""
    assert PROGRESS.exists(), (
        "PROGRESS.md not found in hangar-ai-specs/changes/cpp-external-sources-enrichment/ — "
        "required by ENG-6.7 (Audit Trail) and ENG-11.1 (Hangar SDD)"
    )
    content = PROGRESS.read_text(encoding="utf-8")

    assert "Sign-Off" in content or "Governance" in content, \
        "PROGRESS.md must contain a governance sign-off section"
    assert "CBF" in content or "cpp-brownfield-first" in content, \
        "PROGRESS.md must confirm the CBF prerequisite was merged"
    assert "ENG-4.1" in content, \
        "PROGRESS.md must confirm Atomic TDD compliance (ENG-4.1)"
    assert "ENG-6.7" in content, \
        "PROGRESS.md must reference Audit Trail law (ENG-6.7)"
    assert "C++20" in content, \
        "PROGRESS.md must include version annotation summary (C++20 count)"
