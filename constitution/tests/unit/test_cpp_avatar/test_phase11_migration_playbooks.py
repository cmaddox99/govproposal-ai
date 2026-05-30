"""Phase 11: Migration Playbooks & Examples (Amendment G) tests."""
import pathlib
import pytest

REPO = pathlib.Path(__file__).resolve().parents[3]
GUIDANCE = REPO / "avatars" / "technology" / "cpp" / "refs/legacy/ref-migration-pre-cpp17.md"
EXAMPLES_DIR = REPO / "avatars" / "technology" / "cpp" / "examples"


@pytest.fixture(scope="module")
def guidance_text():
    return GUIDANCE.read_text(encoding="utf-8")


# --- Tasks 11.1-11.4: Migration Playbooks ---

class TestMigrationPlaybooks:
    """Validate all 4 migration playbooks exist in guidance.md."""

    def test_cpp98_to_cpp11_playbook(self, guidance_text):
        assert "## Migration Playbook: C++98/03" in guidance_text

    def test_cpp98_to_cpp11_has_feature_sequence(self, guidance_text):
        assert "nullptr" in guidance_text and "override" in guidance_text

    def test_cpp98_to_cpp11_has_pitfalls(self, guidance_text):
        assert "auto_ptr" in guidance_text
        assert "GCC 5.1 ABI" in guidance_text or "ABI break" in guidance_text

    def test_cpp11_to_cpp14_playbook(self, guidance_text):
        assert "## Migration Playbook: C++11" in guidance_text

    def test_cpp11_to_cpp14_has_make_unique(self, guidance_text):
        assert "make_unique" in guidance_text

    def test_cpp14_to_cpp17_playbook(self, guidance_text):
        assert "## Migration Playbook: C++14" in guidance_text

    def test_cpp14_to_cpp17_has_string_view_warning(self, guidance_text):
        assert "string_view" in guidance_text

    def test_cpp14_to_cpp17_mentions_removed_features(self, guidance_text):
        assert "random_shuffle" in guidance_text or "auto_ptr" in guidance_text

    def test_cpp17_to_cpp20_playbook(self, guidance_text):
        assert "## Migration Playbook: C++17" in guidance_text

    def test_cpp17_to_cpp20_has_adoption_sequence(self, guidance_text):
        # Should mention span, concepts, ranges in sequence
        assert "std::span" in guidance_text
        assert "Concepts" in guidance_text or "concepts" in guidance_text

    def test_cpp17_to_cpp20_warns_about_modules(self, guidance_text):
        assert "Modules" in guidance_text or "modules" in guidance_text


# --- Task 11.5: Dual-Toolchain ---

class TestDualToolchain:
    """Validate dual-toolchain governance section."""

    def test_dual_toolchain_section_exists(self, guidance_text):
        assert "## Dual-Toolchain Governance" in guidance_text

    def test_mentions_target_compile_features(self, guidance_text):
        assert "target_compile_features" in guidance_text

    def test_mentions_ci_matrix(self, guidance_text):
        assert "CI" in guidance_text and ("matrix" in guidance_text.lower() or "both compilers" in guidance_text.lower())


# --- Task 11.6: Dependency Mismatch ---

class TestDependencyMismatch:
    """Validate dependency standard mismatch guidance."""

    def test_dependency_mismatch_section(self, guidance_text):
        assert "Dependency Standard Mismatch" in guidance_text or "dependency standard" in guidance_text.lower()

    def test_mentions_adapter_library(self, guidance_text):
        assert "adapter" in guidance_text.lower() or "wrapper" in guidance_text.lower()

    def test_mentions_vcpkg_triplet(self, guidance_text):
        assert "triplet" in guidance_text.lower()


# --- Task 11.7: Writing New Code for Legacy ---

class TestWritingNewCodeForLegacy:
    """Validate writing new code for legacy standards section."""

    def test_section_exists(self, guidance_text):
        assert "Writing New Code for Legacy" in guidance_text or "New Code for Legacy" in guidance_text

    def test_has_feature_availability_table(self, guidance_text):
        # Should show what's available at each tier
        assert "C++11" in guidance_text and "C++14" in guidance_text

    def test_mentions_polyfill(self, guidance_text):
        assert "polyfill" in guidance_text.lower() or "Polyfill" in guidance_text

    def test_mentions_gsl_span(self, guidance_text):
        assert "gsl::span" in guidance_text


# --- Tasks 11.8-11.14: Example Files ---

MIGRATION_EXAMPLES = [
    ("ENG-5.2-cmake-mixed-standard.md", "ENG-5.2"),
    ("ENG-6.1-auto-ptr-migration.md", "ENG-6.1"),
    ("ENG-6.1-smart-pointer-migration.md", "ENG-6.1"),
    ("ENG-6.1-raii-c-api-wrapper.md", "ENG-6.1"),
    ("ENG-6.1-thread-migration.md", "ENG-6.1"),
    ("ENG-3.1-feature-detection.md", "ENG-3.1"),
    ("ENG-6.1-legacy-modernization-before-after.md", "ENG-6.1"),
]


@pytest.mark.parametrize("filename,law_id", MIGRATION_EXAMPLES,
                         ids=[e[0] for e in MIGRATION_EXAMPLES])
class TestMigrationExamples:
    """Validate each migration example file."""

    def test_file_exists(self, filename, law_id):
        path = EXAMPLES_DIR / filename
        assert path.exists(), f"Missing example: {filename}"

    def test_has_title(self, filename, law_id):
        text = (EXAMPLES_DIR / filename).read_text(encoding="utf-8")
        # Strip optional YAML frontmatter before checking for title
        content = text
        if content.startswith("---"):
            end = content.index("---", 3)
            content = content[end + 3:].lstrip("\n")
        assert content.startswith("#"), f"{filename} must start with # title"

    def test_references_law(self, filename, law_id):
        text = (EXAMPLES_DIR / filename).read_text(encoding="utf-8")
        assert law_id in text, f"{filename} must reference {law_id}"

    def test_has_code_block(self, filename, law_id):
        text = (EXAMPLES_DIR / filename).read_text(encoding="utf-8")
        assert "```" in text, f"{filename} must contain code blocks"

    def test_under_token_budget(self, filename, law_id):
        text = (EXAMPLES_DIR / filename).read_text(encoding="utf-8")
        word_count = len(text.split())
        estimated_tokens = int(word_count * 1.3)
        assert estimated_tokens <= 850, f"{filename} exceeds 850-token budget: ~{estimated_tokens}"
