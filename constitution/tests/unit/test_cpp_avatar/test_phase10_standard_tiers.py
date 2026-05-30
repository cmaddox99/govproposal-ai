"""Phase 10: Standard-Tier Governance Foundation (Amendment F) tests.

Validates that standard_tiers exist in the example file (ENG-5.2-cmake-mixed-standard.md),
tiered compilers in manifest.yaml, and parameterized lint commands.
Validates that full-reference.md has per-tier governance sections.
"""
import pathlib
import pytest
import yaml

REPO = pathlib.Path(__file__).resolve().parents[3]
MANIFEST = REPO / "avatars" / "technology" / "cpp" / "manifest.yaml"
GUIDANCE = REPO / "avatars" / "technology" / "cpp" / "refs/legacy/ref-brownfield-adoption.md"
GUIDANCE_CONFIG = REPO / "avatars" / "technology" / "cpp" / "refs/legacy/ref-brownfield-project-config.md"
TIERS_EXAMPLE = REPO / "avatars" / "technology" / "cpp" / "examples" / "ENG-5.2-cmake-mixed-standard.md"


@pytest.fixture(scope="module")
def manifest():
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def guidance_text():
    return GUIDANCE.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def guidance_config_text():
    return GUIDANCE_CONFIG.read_text(encoding="utf-8")


# --- Task 10.1: standard_tiers block ---

class TestStandardTiers:
    """Validate standard tier content in ENG-5.2-cmake-mixed-standard.md.

    Content routed from manifest.yaml per avatar-model-schema §3 allowlist.
    standard_tiers is not an allowed manifest block; the constitutionally
    correct location is the ENG-5.2 example file.
    """

    @pytest.fixture(scope="class")
    def tiers_text(self):
        return TIERS_EXAMPLE.read_text(encoding="utf-8")

    def test_standard_tiers_exists(self, tiers_text):
        assert "C++ Standard Tiers" in tiers_text, \
            "ENG-5.2-cmake-mixed-standard.md must have C++ Standard Tiers section"

    def test_has_five_tiers(self, tiers_text):
        tier_names = ["Recommended", "Required Minimum", "Active Brownfield",
                      "Legacy Supported", "Legacy Frozen"]
        for name in tier_names:
            assert name in tiers_text, f"Missing tier: {name}"

    @pytest.mark.parametrize("tier_name", [
        "Recommended", "Required Minimum", "Active Brownfield",
        "Legacy Supported", "Legacy Frozen"
    ])
    def test_tier_exists(self, tiers_text, tier_name):
        assert tier_name in tiers_text, f"Missing tier: {tier_name}"

    def test_recommended_tier_has_cpp23(self, tiers_text):
        assert "C++23" in tiers_text

    def test_required_minimum_has_cpp20(self, tiers_text):
        assert "C++20" in tiers_text

    def test_active_brownfield_has_cpp14_cpp17(self, tiers_text):
        assert "C++14" in tiers_text and "C++17" in tiers_text

    def test_legacy_supported_has_cpp11(self, tiers_text):
        assert "C++11" in tiers_text

    def test_legacy_frozen_has_cpp98_cpp03(self, tiers_text):
        assert "C++98" in tiers_text and "C++03" in tiers_text

    def test_each_tier_has_required_fields(self, tiers_text):
        """Each tier row must have status, applies-to, and governance columns."""
        for keyword in ["greenfield", "brownfield", "maintenance only"]:
            assert keyword in tiers_text.lower(), f"Tiers table missing: {keyword}"

    def test_compiler_minimums_have_gcc_clang_msvc(self, tiers_text):
        assert "Minimum Compiler Versions" in tiers_text
        assert "GCC" in tiers_text
        assert "Clang" in tiers_text
        assert "MSVC" in tiers_text


# --- Task 10.2: Tiered compilers ---

class TestTieredCompilers:
    """Validate tiered compiler structure in manifest.yaml."""

    def test_compilers_has_tiers(self, manifest):
        compilers = manifest["stack"]["compilers"]
        assert isinstance(compilers, dict), "compilers should be a dict with tiers, not a flat list"

    @pytest.mark.parametrize("tier", [
        "recommended", "required_greenfield", "active_brownfield", "legacy", "frozen"
    ])
    def test_compiler_tier_exists(self, manifest, tier):
        assert tier in manifest["stack"]["compilers"], f"Missing compiler tier: {tier}"

    def test_recommended_mentions_gcc14(self, manifest):
        recommended = manifest["stack"]["compilers"]["recommended"]
        assert any("GCC 14" in c for c in recommended)

    def test_legacy_mentions_gcc48(self, manifest):
        legacy = manifest["stack"]["compilers"]["legacy"]
        assert any("4.8" in c for c in legacy)


# --- Task 10.3: Anti-patterns by tier ---

class TestAntiPatternsByTier:
    """Amendment O V4: anti_patterns_by_tier removed from manifest.yaml (scope creep).
    These tests verify the block is absent."""

    def test_anti_patterns_by_tier_exists(self, manifest):
        """Amendment O V4: anti_patterns_by_tier must NOT be in manifest.yaml."""
        assert "anti_patterns_by_tier" not in manifest, (
            "Amendment O V4: anti_patterns_by_tier must be removed from manifest.yaml"
        )


# --- Task 10.4: Parameterized lint ---

class TestParameterizedLint:
    """Validate lint command has per-tier options."""

    def test_lint_has_cpp17(self, manifest):
        lint = manifest["commands"]["lint"]
        assert "check_cpp17" in lint

    def test_lint_has_cpp14(self, manifest):
        lint = manifest["commands"]["lint"]
        assert "check_cpp14" in lint

    def test_lint_has_cpp11(self, manifest):
        lint = manifest["commands"]["lint"]
        assert "check_cpp11" in lint


# --- Tasks 10.5-10.11: Guidance sections ---

class TestGuidancePerTierSections:
    """Validate all new guidance sections exist."""

    def test_clang_tidy_config_section(self, guidance_text):
        assert "## Per-Tier clang-tidy Configuration" in guidance_text

    def test_clang_tidy_has_cpp11_tier(self, guidance_text):
        assert "C++11 Tier" in guidance_text

    def test_clang_tidy_has_cpp20_tier(self, guidance_text):
        assert "C++20+ Tier" in guidance_text

    def test_testing_framework_matrix(self, guidance_text):
        assert "## Per-Tier Testing Framework Matrix" in guidance_text

    def test_testing_matrix_mentions_boost_test(self, guidance_text):
        assert "Boost.Test" in guidance_text

    def test_testing_matrix_mentions_googletest_112(self, guidance_text):
        assert "1.12" in guidance_text

    def test_code_review_criteria_section(self, guidance_text):
        assert "## Per-Tier Code Review Criteria" in guidance_text

    def test_code_review_has_cpp98_section(self, guidance_text):
        assert "C++98/03 (Frozen)" in guidance_text

    def test_code_review_has_cpp11_section(self, guidance_text):
        assert "C++11 (Sunset)" in guidance_text

    def test_abi_boundary_section(self, guidance_text):
        assert "## Cross-Standard ABI Boundaries" in guidance_text

    def test_abi_mentions_gcc_dual_abi(self, guidance_text):
        assert "_GLIBCXX_USE_CXX11_ABI" in guidance_text

    def test_feature_detection_section(self, guidance_text):
        assert "## Feature-Detection Macro Governance" in guidance_text

    def test_feature_detection_has_cplusplus_table(self, guidance_text):
        assert "199711L" in guidance_text  # C++98 value
        assert "202002L" in guidance_text  # C++20 value

    def test_feature_detection_has_sd6(self, guidance_text):
        assert "__cpp_lib_optional" in guidance_text or "__cpp_concepts" in guidance_text

    def test_compiler_flag_progression(self, guidance_config_text):
        assert "## Compiler Flag Progression During Migration" in guidance_config_text

    def test_flag_progression_has_six_phases(self, guidance_config_text):
        # Check for phase markers
        assert "Baseline" in guidance_config_text
        assert "Tighten" in guidance_config_text
        assert "Enforce core" in guidance_config_text

    def test_sanitizer_availability_section(self, guidance_config_text):
        assert "## Sanitizer Availability by Compiler Version" in guidance_config_text

    def test_sanitizer_matrix_has_valgrind_fallback(self, guidance_config_text):
        assert "Valgrind" in guidance_config_text

    def test_sanitizer_matrix_has_gcc_versions(self, guidance_config_text):
        # Should mention specific GCC minimums for sanitizers
        assert "4.8" in guidance_config_text or "4.9" in guidance_config_text
