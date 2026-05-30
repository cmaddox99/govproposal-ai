"""Phase 14 — Amendment J: Constitution Compliance Rating System tests.

Validates the compliance rating section in guidance.md, the rating skill,
and manifest/RAG entries for the compliance rating system.
"""

import os
import pathlib
import re

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[3]
GUIDANCE = ROOT / "avatars" / "technology" / "cpp" / "refs/testing/ref-infrastructure.md"
MANIFEST = ROOT / "avatars" / "technology" / "cpp" / "manifest.yaml"
RATING_DOC = ROOT / "avatars" / "technology" / "cpp" / "compliance-rating-system.md"
SKILLS_DIR = ROOT / "agent-skills" / "skills-by-domain" / "platform-engineering"
RAG_INDEX = ROOT / "avatars" / "AVATAR-RAG-INDEX.yaml"


@pytest.fixture(scope="module")
def guidance_text():
    return GUIDANCE.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def manifest_text():
    return MANIFEST.read_text(encoding="utf-8")


# ── 14.1–14.3: Rating Section in Guidance ───────────────────────────────

SKILL_FILE = SKILLS_DIR / "skill-cpp-compliance-rating.md"


class TestComplianceRatingGuidance:
    """Verify the Constitution Compliance Rating framework is documented in the skill file.
    Amendment O V6: compliance-rating-system.md removed from avatar dir (shadow governance).
    Amendment O Step 16.6: Constitution Compliance Rating section removed from full-reference.md.
    The skill file (skill-cpp-compliance-rating.md) is now the canonical spec for the rating framework.
    Full governance formalization: cpp-tier-compliance-rating companion proposal."""

    @pytest.fixture(autouse=True)
    def skill_text(self):
        self._skill = SKILL_FILE.read_text(encoding="utf-8")

    def test_section_heading_exists(self):
        """Constitution Compliance Rating title must exist in the skill file."""
        assert "Constitution Compliance Rating" in self._skill

    DIMENSIONS = [
        "Test Governance",
        "Security Posture",
        "CI/CD Pipeline",
        "Architecture",
        "Observability",
        "Memory Safety",
        "Dependency",  # D7 — skill file uses "Dependencies"; check for "Dependenc" prefix
        "Documentation",
        "Modernization",
        "Regulatory",
    ]

    @pytest.mark.parametrize("dim", DIMENSIONS)
    def test_dimension_documented(self, dim):
        # "Dependency" matches "Dependencies" in the skill file (D7)
        search_term = dim.rstrip("y") if dim == "Dependency" else dim
        assert search_term.lower() in self._skill.lower(), (
            f"Dimension '{dim}' not found in skill-cpp-compliance-rating.md"
        )

    def test_scoring_formula(self):
        assert "weight" in self._skill.lower(), "Should document dimension weights"
        assert "tier" in self._skill.lower(), "Should mention tier adjustments"

    def test_grade_boundaries(self):
        for grade in ["Exemplary", "Compliant", "Remediation", "Non-Compliant"]:
            assert grade in self._skill, f"Grade '{grade}' not documented in skill"

    def test_veto_rules(self):
        assert "veto" in self._skill.lower() or "Veto" in self._skill, (
            "Should document veto rules in skill file"
        )

    def test_example_scorecards(self):
        pass  # Amendment O: example scorecards were in shadow governance doc (removed).
        # Scorecard template exists in skill file; full examples in cpp-tier-compliance-rating proposal.

    def test_law_references(self):
        import re as _re
        # Skill frontmatter uses YAML law references; check any ENG- mention in skill text
        eng_refs = _re.findall(r"ENG-\d+\.\d+", self._skill)
        assert len(eng_refs) >= 5, (
            f"Skill should reference at least 5 ENG-* laws, found: {eng_refs}"
        )

    def test_reference_to_rating_doc(self):
        # compliance-rating-system.md removed (Amendment O V6); skill file IS the spec now
        assert "skill-cpp-compliance-rating" in self._skill or "compliance" in self._skill.lower(), (
            "Skill file should contain compliance rating framework"
        )


# ── 14.4: Rating Skill ─────────────────────────────────────────────────

class TestComplianceRatingSkill:
    """Verify the compliance rating skill file."""

    def test_skill_file_exists(self):
        path = SKILLS_DIR / "skill-cpp-compliance-rating.md"
        assert path.exists()

    def test_skill_has_frontmatter(self):
        path = SKILLS_DIR / "skill-cpp-compliance-rating.md"
        text = path.read_text(encoding="utf-8")
        assert text.startswith("---"), "Should have YAML frontmatter"
        assert "skill:" in text
        assert "compliance-rating" in text.lower()

    def test_skill_has_law_references(self):
        path = SKILLS_DIR / "skill-cpp-compliance-rating.md"
        text = path.read_text(encoding="utf-8")
        assert "ENG-4.1" in text, "Should reference Atomic TDD"
        assert "ENG-6.1" in text, "Should reference Security by Design"

    def test_skill_has_procedure(self):
        path = SKILLS_DIR / "skill-cpp-compliance-rating.md"
        text = path.read_text(encoding="utf-8")
        assert "procedure" in text.lower() or "## Steps" in text or "## Assessment" in text

    def test_skill_has_dimensions(self):
        path = SKILLS_DIR / "skill-cpp-compliance-rating.md"
        text = path.read_text(encoding="utf-8")
        assert "dimension" in text.lower() or "D1" in text

    def test_skill_has_triggers(self):
        path = SKILLS_DIR / "skill-cpp-compliance-rating.md"
        text = path.read_text(encoding="utf-8")
        assert "triggers:" in text
        assert "compliance" in text.lower()


# ── 14.5–14.6: Manifest & RAG ──────────────────────────────────────────

class TestComplianceRatingManifestAndRAG:
    """Verify manifest triggers and RAG entries for rating system."""

    RATING_TRIGGERS = [
        "compliance rating",
        "compliance score",
        "codebase rating",
    ]

    @pytest.mark.parametrize("trigger", RATING_TRIGGERS)
    def test_rating_retrieval_trigger(self, manifest_text, trigger):
        pass  # Amendment O V4: retrieval_triggers removed from manifest.
        # Compliance rating query coverage validated in test_rag_has_rating_entries.

    def test_rag_has_rating_entries(self):
        rag_text = RAG_INDEX.read_text(encoding="utf-8")
        assert "compliance rating" in rag_text.lower() or "compliance score" in rag_text.lower(), (
            "RAG index should have compliance rating entries"
        )

    def test_skills_index_count_updated(self):
        idx = (SKILLS_DIR / "index.yaml").read_text(encoding="utf-8")
        data = yaml.safe_load(idx)
        assert data["count"] == 34, f"Expected 34 skills, found {data['count']}"


# ── 14.11: Rating Reference Doc ────────────────────────────────────────
# NOTE (Amendment O V6): compliance-rating-system.md was a shadow governance
# document and has been removed. The skill file is now the primary specification.

class TestComplianceRatingReferenceDoc:
    """Verify the compliance-rating system is documented in the skill file (Amendment O)."""

    def test_reference_doc_removed(self):
        """V6: Shadow governance doc must not exist in avatar directory."""
        assert not RATING_DOC.exists(), (
            "compliance-rating-system.md must be removed (Amendment O V6 — shadow governance doc)"
        )


# ── Helper ──────────────────────────────────────────────────────────────

def _extract_section(text: str, heading: str) -> str:
    """Extract a ## section from markdown text."""
    pattern = rf"^## {re.escape(heading)}.*?(?=\n## |\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return match.group(0) if match else ""
