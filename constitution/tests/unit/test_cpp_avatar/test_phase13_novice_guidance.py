"""Phase 13 — Amendment I: Novice C++ Developer Guidance tests.

Validates 5 new guidance sections, 2 skills, 2 examples, manifest anti-patterns,
retrieval triggers, and RAG entries for novice C++ developer support.
"""

import os
import pathlib
import re

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[3]
_CPP_DIR = ROOT / "avatars" / "technology" / "cpp"
MANIFEST = ROOT / "avatars" / "technology" / "cpp" / "manifest.yaml"
EXAMPLES_DIR = ROOT / "avatars" / "technology" / "cpp" / "examples"
SKILLS_DIR = ROOT / "agent-skills" / "skills-by-domain" / "platform-engineering"
RAG_INDEX = ROOT / "avatars" / "AVATAR-RAG-INDEX.yaml"


@pytest.fixture(scope="module")
def guidance_text():
    return "\n".join(p.read_text(encoding="utf-8") for p in sorted(_CPP_DIR.rglob("ref-*.md")))


@pytest.fixture(scope="module")
def manifest_text():
    return MANIFEST.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def manifest_data():
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


# ── 13.1: Mental Model Transitions ──────────────────────────────────────

class TestMentalModelTransitions:
    """Verify the Mental Model Transitions section exists with all 8 gaps."""

    def test_section_heading_exists(self, guidance_text):
        assert "## Mental Model Transitions" in guidance_text

    MENTAL_MODELS = [
        "Value Semantics vs Reference Semantics",
        "RAII vs Garbage Collection",
        "Compilation Model",
        "Undefined Behavior",
        "Pointers vs References vs Values",
        "Preprocessor",
        "Linking",
        "const Correctness",
    ]

    @pytest.mark.parametrize("model", MENTAL_MODELS)
    def test_mental_model_subsection(self, guidance_text, model):
        assert model.lower() in guidance_text.lower(), (
            f"Mental model gap '{model}' not found in guidance"
        )

    def test_section_has_law_references(self, guidance_text):
        section = _extract_section(guidance_text, "Mental Model Transitions")
        assert section, "Section not found"
        links = re.findall(r"\[ENG-\d+\.\d+\]", section)
        assert len(links) >= 2, "Section should reference at least 2 laws"

    def test_section_mentions_java_or_python(self, guidance_text):
        section = _extract_section(guidance_text, "Mental Model Transitions")
        assert section, "Section not found"
        assert "java" in section.lower() or "python" in section.lower(), (
            "Should reference common source languages"
        )


# ── 13.2: Legacy Code Smell Catalog ────────────────────────────────────

class TestLegacyCodeSmellCatalog:
    """Verify the Legacy Code Smell Catalog section with 14 smells."""

    def test_section_heading_exists(self, guidance_text):
        assert "## Legacy Code Smell Catalog" in guidance_text

    CODE_SMELLS = [
        "god class",
        "deep inheritance",
        "circular",
        "ifdef",
        "copy-paste polymorphism",
        "singleton abuse",
        "fragile base class",
        "header-only bloat",
        "rule of",
        "implicit conversion",
        "public data member",
        "output parameter",
        "mixed error handling",
        "multiple return",
    ]

    @pytest.mark.parametrize("smell", CODE_SMELLS)
    def test_code_smell_documented(self, guidance_text, smell):
        section = _extract_section(guidance_text, "Legacy Code Smell Catalog")
        assert section, "Section not found"
        assert smell.lower() in section.lower(), (
            f"Code smell '{smell}' not documented"
        )

    def test_severity_ratings_present(self, guidance_text):
        section = _extract_section(guidance_text, "Legacy Code Smell Catalog")
        assert section, "Section not found"
        for sev in ["CRITICAL", "HIGH", "MEDIUM"]:
            assert sev in section, f"Severity '{sev}' not found"

    def test_remediation_guidance(self, guidance_text):
        section = _extract_section(guidance_text, "Legacy Code Smell Catalog")
        assert section, "Section not found"
        assert section.lower().count("remediation") >= 3 or section.lower().count("fix") >= 5, (
            "Should have remediation guidance for smells"
        )


# ── 13.3: Legacy Codebase Triage Playbook ──────────────────────────────

class TestLegacyTriagePlaybook:
    """Verify the Legacy Codebase Triage Playbook section."""

    def test_section_heading_exists(self, guidance_text):
        assert "## Legacy Codebase Triage Playbook" in guidance_text

    TRIAGE_ELEMENTS = [
        "week-1",
        "sanitizer",
        "characterization test",
        "do not touch",
        "seam",
    ]

    @pytest.mark.parametrize("element", TRIAGE_ELEMENTS)
    def test_triage_element_present(self, guidance_text, element):
        section = _extract_section(guidance_text, "Legacy Codebase Triage Playbook")
        assert section, "Section not found"
        assert element.lower() in section.lower(), (
            f"Triage element '{element}' not found"
        )

    def test_day_by_day_priorities(self, guidance_text):
        section = _extract_section(guidance_text, "Legacy Codebase Triage Playbook")
        assert section, "Section not found"
        day_refs = re.findall(r"[Dd]ay[\s-]*\d", section)
        assert len(day_refs) >= 3, "Should have day-by-day priorities"

    def test_month_plan(self, guidance_text):
        section = _extract_section(guidance_text, "Legacy Codebase Triage Playbook")
        assert section, "Section not found"
        assert "month" in section.lower() or "week" in section.lower()

    def test_seam_types(self, guidance_text):
        section = _extract_section(guidance_text, "Legacy Codebase Triage Playbook")
        assert section, "Section not found"
        for seam in ["preprocessing seam", "link seam", "object seam"]:
            assert seam.lower() in section.lower(), f"Seam type '{seam}' not documented"


# ── 13.4: Survival Patterns ────────────────────────────────────────────

class TestSurvivalPatterns:
    """Verify the Survival Patterns section with phase progression."""

    def test_section_heading_exists(self, guidance_text):
        assert "## Survival Patterns" in guidance_text

    PHASES = [
        ("week 1", "reading"),
        ("month 1", "modification"),
        ("month 3", "contribut"),
        ("month 6", "modernization"),
    ]

    @pytest.mark.parametrize("phase,keyword", PHASES)
    def test_survival_phase(self, guidance_text, phase, keyword):
        section = _extract_section(guidance_text, "Survival Patterns")
        assert section, "Section not found"
        lower = section.lower()
        assert phase in lower, f"Phase '{phase}' not found"
        assert keyword in lower, f"Keyword '{keyword}' not found for phase"

    PATTERNS = [
        "sprout method",
        "wrap method",
        "extract interface",
        "raii conversion",
    ]

    @pytest.mark.parametrize("pattern", PATTERNS)
    def test_safe_modification_pattern(self, guidance_text, pattern):
        section = _extract_section(guidance_text, "Survival Patterns")
        assert section, "Section not found"
        assert pattern.lower() in section.lower(), (
            f"Safe modification pattern '{pattern}' not documented"
        )

    def test_debugger_as_reading_tool(self, guidance_text):
        section = _extract_section(guidance_text, "Survival Patterns")
        assert section, "Section not found"
        assert "debugger" in section.lower() or "gdb" in section.lower()


# ── 13.5: Object Design Rehabilitation ─────────────────────────────────

class TestObjectDesignRehabilitation:
    """Verify the Object Design Rehabilitation section with 6 vectors."""

    def test_section_heading_exists(self, guidance_text):
        assert "## Object Design Rehabilitation" in guidance_text

    DESIGN_VECTORS = [
        "diamond",
        "operator overloading",
        "implicit conversion",
        "copy semantics",
        "virtual function",
        "move semantics",
    ]

    @pytest.mark.parametrize("vector", DESIGN_VECTORS)
    def test_design_vector_documented(self, guidance_text, vector):
        section = _extract_section(guidance_text, "Object Design Rehabilitation")
        assert section, "Section not found"
        assert vector.lower() in section.lower(), (
            f"Design debt vector '{vector}' not documented"
        )

    def test_recognition_and_fix_pattern(self, guidance_text):
        section = _extract_section(guidance_text, "Object Design Rehabilitation")
        assert section, "Section not found"
        assert "recognition" in section.lower() or "recognize" in section.lower()
        assert "fix" in section.lower() or "remediation" in section.lower()

    def test_explicit_keyword(self, guidance_text):
        section = _extract_section(guidance_text, "Object Design Rehabilitation")
        assert section, "Section not found"
        assert "`explicit`" in section, "Should mention explicit keyword"


# ── 13.6–13.7: Skills ──────────────────────────────────────────────────

class TestNoviceSkills:
    """Verify skill updates and new skill file."""

    def test_legacy_navigation_skill_has_triage(self):
        path = SKILLS_DIR / "skill-cpp-legacy-code-navigation.md"
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "triage" in text.lower(), "Skill should include triage methodology"
        assert "seam" in text.lower(), "Skill should include seam identification"

    def test_legacy_navigation_skill_has_characterization(self):
        path = SKILLS_DIR / "skill-cpp-legacy-code-navigation.md"
        text = path.read_text(encoding="utf-8")
        assert "characterization" in text.lower(), "Skill should include characterization testing"

    def test_survival_patterns_skill_exists(self):
        path = SKILLS_DIR / "skill-cpp-legacy-survival-patterns.md"
        assert path.exists(), "skill-cpp-legacy-survival-patterns.md should exist"

    def test_survival_patterns_skill_frontmatter(self):
        path = SKILLS_DIR / "skill-cpp-legacy-survival-patterns.md"
        text = path.read_text(encoding="utf-8")
        assert "---" in text, "Should have YAML frontmatter"
        assert "skill:" in text.lower() or "name:" in text.lower()
        assert "ENG-" in text, "Should reference engineering laws"

    def test_survival_patterns_skill_content(self):
        path = SKILLS_DIR / "skill-cpp-legacy-survival-patterns.md"
        text = path.read_text(encoding="utf-8")
        for phase in ["week 1", "month 1", "month 3"]:
            assert phase in text.lower(), f"Skill should cover '{phase}' phase"


# ── 13.8–13.10: Manifest & RAG ─────────────────────────────────────────

class TestNoviceManifestAndRAG:
    """Verify manifest anti-patterns, triggers, and RAG entries.
    Amendment O V4: anti_patterns and retrieval_triggers removed from manifest.yaml."""

    CODE_SMELL_ANTI_PATTERNS = [
        "god-class",
        "deep-inheritance",
        "circular-include",
        "ifdef-spaghetti",
        "copy-paste-polymorphism",
        "singleton-abuse",
        "fragile-base-class",
        "header-only-bloat",
        "rule-of-three-violation",
        "implicit-conversion-abuse",
        "public-data-members",
        "output-parameter-overuse",
        "mixed-error-handling",
        "multiple-return-cleanup",
    ]

    @pytest.mark.parametrize("ap_id", CODE_SMELL_ANTI_PATTERNS)
    def test_code_smell_in_manifest(self, manifest_text, ap_id):
        pass  # Amendment O V4: anti_patterns removed from manifest (scope creep).
        # Code smells are validated in TestLegacyCodeSmellCatalog via guidance.md.

    NOVICE_TRIGGERS = [
        "mental model",
        "code smell",
        "triage",
        "survival pattern",
        "object design",
        "novice",
        "legacy onboarding",
        "characterization test",
    ]

    @pytest.mark.parametrize("trigger", NOVICE_TRIGGERS)
    def test_novice_retrieval_trigger(self, manifest_text, trigger):
        pass  # Amendment O V4: retrieval_triggers removed from manifest.
        # Novice query coverage validated in test_rag_has_novice_entries via AVATAR-RAG-INDEX.yaml.

    def test_rag_has_novice_entries(self):
        rag_text = RAG_INDEX.read_text(encoding="utf-8")
        novice_terms = ["mental model", "code smell", "triage", "novice"]
        found = sum(1 for t in novice_terms if t.lower() in rag_text.lower())
        assert found >= 3, "RAG index should have at least 3 novice-related entries"


# ── 13.11–13.12: Examples ──────────────────────────────────────────────

class TestNoviceExamples:
    """Verify 2 new example files."""

    def test_raii_conversion_example_exists(self):
        path = EXAMPLES_DIR / "ENG-3.1-code-smell-raii-conversion.md"
        assert path.exists()

    def test_raii_conversion_example_content(self):
        path = EXAMPLES_DIR / "ENG-3.1-code-smell-raii-conversion.md"
        text = path.read_text(encoding="utf-8")
        assert "raii" in text.lower()
        assert "```cpp" in text
        assert "NON-COMPLIANT" in text or "Non-Compliant" in text or "non_compliant" in text.lower()
        assert "COMPLIANT" in text

    def test_characterization_test_example_exists(self):
        path = EXAMPLES_DIR / "ENG-4.1-characterization-test-pattern.md"
        assert path.exists()

    def test_characterization_test_example_content(self):
        path = EXAMPLES_DIR / "ENG-4.1-characterization-test-pattern.md"
        text = path.read_text(encoding="utf-8")
        assert "characterization" in text.lower()
        assert "```cpp" in text
        assert "legacy" in text.lower() or "existing" in text.lower()
        assert "COMPLIANT" in text


# ── Helper ──────────────────────────────────────────────────────────────

def _extract_section(text: str, heading: str) -> str:
    """Extract a ## section from markdown text."""
    pattern = rf"^## {re.escape(heading)}.*?(?=\n## |\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return match.group(0) if match else ""
