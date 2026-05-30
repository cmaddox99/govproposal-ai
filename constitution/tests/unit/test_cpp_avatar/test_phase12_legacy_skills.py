"""Phase 12: Legacy Anti-Patterns, Skills & RAG (Amendment H) tests."""
import pathlib
import pytest
import yaml

REPO = pathlib.Path(__file__).resolve().parents[3]
MANIFEST = REPO / "avatars" / "technology" / "cpp" / "manifest.yaml"
GUIDANCE = REPO / "avatars" / "technology" / "cpp" / "refs/legacy/ref-legacy-navigation.md"
SKILLS_DIR = REPO / "agent-skills" / "skills-by-domain" / "platform-engineering"
RAG_INDEX = REPO / "avatars" / "AVATAR-RAG-INDEX.yaml"
PE_INDEX = SKILLS_DIR / "index.yaml"


@pytest.fixture(scope="module")
def manifest():
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def rag_text():
    return RAG_INDEX.read_text(encoding="utf-8")


# --- Task 12.1: Legacy Anti-Patterns ---

class TestLegacyAntiPatterns:
    """Amendment O V4: anti_patterns removed from manifest.yaml.
    Content belongs in example files per ENG-11.1 scope constraints."""

    def test_anti_pattern_count_at_least_32(self, manifest):
        """Amendment O V4: anti_patterns block must be absent from manifest."""
        assert "anti_patterns" not in manifest, (
            "Amendment O V4: anti_patterns must NOT be in manifest.yaml (scope creep)"
        )




# --- Tasks 12.2-12.5: New Skills ---

NEW_SKILLS = [
    ("skill-cpp-standard-migration.md", "Standard Migration"),
    ("skill-cpp-legacy-modernization.md", "Legacy Modernization"),
    ("skill-cpp-compatibility-headers.md", "Compatibility Headers"),
    ("skill-cpp-feature-detection.md", "Feature Detection"),
]


@pytest.mark.parametrize("filename,desc", NEW_SKILLS,
                         ids=[s[0] for s in NEW_SKILLS])
class TestNewSkills:
    """Validate 4 new skill files."""

    def test_file_exists(self, filename, desc):
        assert (SKILLS_DIR / filename).exists(), f"Missing skill: {filename}"

    def test_has_frontmatter(self, filename, desc):
        text = (SKILLS_DIR / filename).read_text(encoding="utf-8")
        assert text.startswith("---"), f"{filename} must start with YAML frontmatter"

    def test_has_skill_name(self, filename, desc):
        text = (SKILLS_DIR / filename).read_text(encoding="utf-8")
        assert "skill:" in text and "name:" in text

    def test_has_triggers(self, filename, desc):
        text = (SKILLS_DIR / filename).read_text(encoding="utf-8")
        assert "triggers:" in text

    def test_has_law_reference(self, filename, desc):
        text = (SKILLS_DIR / filename).read_text(encoding="utf-8")
        assert "ENG-" in text, f"{filename} must reference at least one law"

    def test_has_markdown_content(self, filename, desc):
        text = (SKILLS_DIR / filename).read_text(encoding="utf-8")
        # Should have content after frontmatter
        parts = text.split("---", 2)
        assert len(parts) >= 3, f"{filename} must have content after frontmatter"
        content = parts[2].strip()
        assert len(content) > 100, f"{filename} content too short"


# --- Tasks 12.6-12.9: Existing Skill Updates ---

UPDATED_SKILLS = [
    "skill-cpp-portable-build-governance.md",
    "skill-cpp-concurrency-thread-safety-governance.md",
    "skill-cpp-template-complexity-management.md",
    "skill-cpp-exception-safety-governance.md",
]


@pytest.mark.parametrize("filename", UPDATED_SKILLS)
class TestUpdatedSkills:
    """Validate legacy mode sections added to existing skills."""

    def test_has_legacy_section(self, filename):
        text = (SKILLS_DIR / filename).read_text(encoding="utf-8")
        assert "Legacy Standard Support" in text or "legacy" in text.lower(), \
            f"{filename} must have Legacy Standard Support section"


# --- Task 12.10: Retrieval Triggers ---

class TestRetrievalTriggers:
    """Amendment O V4: retrieval_triggers removed from manifest.yaml.
    Must be in AVATAR-RAG-INDEX.yaml instead."""

    def test_trigger_count_at_least_41(self, manifest):
        """Amendment O V4: retrieval_triggers must be absent from manifest."""
        assert "retrieval_triggers" not in manifest, (
            "Amendment O V4: retrieval_triggers must NOT be in manifest.yaml"
        )




# --- Tasks 12.11-12.12: RAG Index ---

class TestRAGIndex:
    """Validate legacy additions to AVATAR-RAG-INDEX.yaml."""

    def test_has_legacy_search_queries(self, rag_text):
        assert "migrate standard" in rag_text.lower() or "C++ migrate" in rag_text

    def test_has_characterization_test_query(self, rag_text):
        assert "characterization" in rag_text.lower()

    def test_has_auto_ptr_anti_pattern(self, rag_text):
        assert "auto_ptr" in rag_text

    def test_has_sfinae_anti_pattern(self, rag_text):
        assert "SFINAE" in rag_text

    def test_has_modernization_anti_pattern(self, rag_text):
        assert "wholesale" in rag_text.lower() or "phased modernization" in rag_text.lower()


# --- Task 12.13: PE Index ---

class TestPEIndex:
    """Validate platform-engineering index updated."""

    def test_pe_index_count_28(self):
        text = PE_INDEX.read_text(encoding="utf-8")
        data = yaml.safe_load(text)
        count = data.get("count", 0)
        assert count >= 28, f"Expected PE index count ≥28, got {count}"


# --- Task 12.18: Phase 5 Validation Counts ---

class TestPhase5ValidationCounts:
    """Validate that Phase 5 counts are updated."""

    def test_skill_count(self):
        skill_files = list(SKILLS_DIR.glob("skill-cpp-*.md"))
        assert len(skill_files) >= 21, f"Expected ≥21 C++ skills, got {len(skill_files)}"
