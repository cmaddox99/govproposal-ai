"""Phase 15 — Quick-Start, MISRA/DO-178C, and Re-Rating Schedule tests.

Validates three high-value additions to the C++ avatar guidance.
"""

import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[3]
_CPP_DIR = ROOT / "avatars" / "technology" / "cpp"
MANIFEST = ROOT / "avatars" / "technology" / "cpp" / "manifest.yaml"


@pytest.fixture(scope="module")
def guidance_text():
    return "\n".join(p.read_text(encoding="utf-8") for p in sorted(_CPP_DIR.rglob("ref-*.md")))


@pytest.fixture(scope="module")
def manifest_text():
    return MANIFEST.read_text(encoding="utf-8")


# ── Quick-Start Cheat Sheet ────────────────────────────────────────────

class TestQuickStartCheatSheet:
    """Verify the Quick-Start section exists near the top of guidance.md."""

    def test_section_heading_exists(self, guidance_text):
        assert "## Quick-Start" in guidance_text

    def test_appears_before_version_policy(self, guidance_text):
        qs_pos = guidance_text.find("## Quick-Start")
        vp_pos = guidance_text.find("## C++ Version Policy")
        assert qs_pos < vp_pos, "Quick-Start should appear before Version Policy"

    def test_greenfield_path(self, guidance_text):
        section = _extract_section(guidance_text, "Quick-Start")
        assert section, "Section not found"
        assert "greenfield" in section.lower()

    def test_brownfield_path(self, guidance_text):
        section = _extract_section(guidance_text, "Quick-Start")
        assert section, "Section not found"
        assert "brownfield" in section.lower()

    def test_novice_path(self, guidance_text):
        section = _extract_section(guidance_text, "Quick-Start")
        assert section, "Section not found"
        lower = section.lower()
        assert "new to c++" in lower or "novice" in lower or "new developer" in lower

    def test_links_to_key_sections(self, guidance_text):
        section = _extract_section(guidance_text, "Quick-Start")
        assert section, "Section not found"
        links = re.findall(r"\[.*?\]\(#.*?\)", section)
        assert len(links) >= 3, "Should link to at least 3 sections"


# ── MISRA C++ / DO-178C ────────────────────────────────────────────────

class TestMISRADO178C:
    """Verify the MISRA C++ and DO-178C safety-critical guidance."""

    def test_section_heading_exists(self, guidance_text):
        assert "MISRA" in guidance_text and "DO-178" in guidance_text

    def test_misra_rules_referenced(self, guidance_text):
        section = _extract_section(guidance_text, "Safety-Critical")
        if not section:
            section = _extract_section(guidance_text, "MISRA")
        assert section, "MISRA/Safety-Critical section not found"
        assert "misra" in section.lower()

    def test_do178c_levels(self, guidance_text):
        section = _extract_section(guidance_text, "Safety-Critical")
        if not section:
            section = _extract_section(guidance_text, "MISRA")
        assert section, "Section not found"
        # DO-178C has Design Assurance Levels A through E
        assert "dal" in section.lower() or "level a" in section.lower() or "assurance" in section.lower()

    def test_maps_to_constitutional_laws(self, guidance_text):
        section = _extract_section(guidance_text, "Safety-Critical")
        if not section:
            section = _extract_section(guidance_text, "MISRA")
        assert section, "Section not found"
        links = re.findall(r"\[(?:ENG|BUS)-\d+\.\d+\]", section)
        assert len(links) >= 3, "Should map to at least 3 constitutional laws"

    def test_faa_referenced(self, guidance_text):
        section = _extract_section(guidance_text, "Safety-Critical")
        if not section:
            section = _extract_section(guidance_text, "MISRA")
        assert section, "Section not found"
        assert "faa" in section.lower()

    MISRA_TOPICS = [
        "dynamic memory",
        "exception",
        "rtti",
    ]

    @pytest.mark.parametrize("topic", MISRA_TOPICS)
    def test_misra_topic_covered(self, guidance_text, topic):
        section = _extract_section(guidance_text, "Safety-Critical")
        if not section:
            section = _extract_section(guidance_text, "MISRA")
        assert section, "Section not found"
        assert topic.lower() in section.lower(), f"MISRA topic '{topic}' not covered"

    def test_manifest_has_safety_critical_trigger(self, manifest_text):
        pass  # Amendment O V4: retrieval_triggers removed from manifest.
        # MISRA/safety-critical query coverage validated in TestMISRADO178C guidance tests.


# ── Periodic Re-Rating Schedule ────────────────────────────────────────

class TestPeriodicReRating:
    """Verify the re-rating schedule governance."""

    def test_section_heading_exists(self, guidance_text):
        lower = guidance_text.lower()
        assert "re-rating" in lower or "periodic rating" in lower or "rating cadence" in lower

    def test_quarterly_cadence(self, guidance_text):
        pass  # Amendment O Step 16.6: Re-rating cadence section removed (shadow governance).
        # Quarterly cadence governance moves to cpp-tier-compliance-rating companion proposal.

    def test_improvement_targets(self, guidance_text):
        section = _extract_rating_section(guidance_text)
        assert section, "Re-rating section not found"
        lower = section.lower()
        assert "target" in lower or "improvement" in lower or "goal" in lower

    def test_escalation_path(self, guidance_text):
        section = _extract_rating_section(guidance_text)
        assert section, "Re-rating section not found"
        lower = section.lower()
        assert "escalat" in lower or "review" in lower or "approval" in lower

    def test_references_compliance_rating(self, guidance_text):
        section = _extract_rating_section(guidance_text)
        assert section, "Re-rating section not found"
        assert "compliance" in section.lower()


# ── Helper ──────────────────────────────────────────────────────────────

def _extract_section(text: str, heading: str) -> str:
    """Extract a ## section from markdown text."""
    pattern = rf"^## .*{re.escape(heading)}.*?(?=\n## |\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return match.group(0) if match else ""


def _extract_rating_section(text: str) -> str:
    """Extract the re-rating/periodic rating section."""
    for heading in ["Re-Rating", "Periodic Rating", "Rating Cadence",
                    "Compliance Rating Cadence", "Re-rating"]:
        section = _extract_section(text, heading)
        if section:
            return section
    # Fallback: look within the Constitution Compliance Rating section
    section = _extract_section(text, "Constitution Compliance Rating")
    if section and ("re-rat" in section.lower() or "quarterly" in section.lower()):
        return section
    return ""
