"""Folly GTest Enrichment Tests — Folly-Grounded GoogleTest Patterns.

Scenario IDs: FOLLY-01 through FOLLY-08
Law: ENG-4.1, ENG-11.1
Proposal: hangar-ai-specs/changes/folly-gtest-enrichment/PROPOSAL.md

Validates that the C++ avatar is grounded in GoogleTest patterns observed
in facebook/folly/tree/main/folly/test — standalone TEST(), fixtures,
exception assertions, template helpers, concurrency, and migration guidance.
"""

import pytest
from pathlib import Path


# ---------------------------------------------------------------------------
# FOLLY-01: manifest has googletest_canonical_patterns conventions
# ---------------------------------------------------------------------------

def test_manifest_has_googletest_canonical_patterns(manifest_data):
    """Scenario FOLLY-01: conventions block must contain googletest_canonical_patterns
    key grounding the avatar in Folly-observed GTest usage."""
    conventions = manifest_data.get("conventions", {})
    assert "googletest_canonical_patterns" in conventions, (
        "conventions block is missing 'googletest_canonical_patterns' — "
        "needed to guide transition from ActiveTest.h to GoogleTest"
    )
    patterns = conventions["googletest_canonical_patterns"]
    # Standalone TEST macro (not just TEST_F) must be referenced
    test_macro = str(patterns).lower()
    assert "test" in test_macro, (
        "googletest_canonical_patterns must reference the TEST() macro"
    )


def test_manifest_gtest_patterns_includes_expect_assert_policy(manifest_data):
    """Scenario FOLLY-01: googletest_canonical_patterns must document the
    EXPECT_* vs ASSERT_* decision policy (EXPECT for non-fatal, ASSERT to abort)."""
    conventions = manifest_data.get("conventions", {})
    patterns = conventions.get("googletest_canonical_patterns", {})
    patterns_str = str(patterns).lower()
    assert "expect" in patterns_str and "assert" in patterns_str, (
        "googletest_canonical_patterns must reference both EXPECT_* and ASSERT_*"
    )


def test_manifest_gtest_patterns_includes_exception_testing(manifest_data):
    """Scenario FOLLY-01: googletest_canonical_patterns must mention exception
    testing macros (EXPECT_THROW, EXPECT_ANY_THROW) observed in Folly."""
    conventions = manifest_data.get("conventions", {})
    patterns = conventions.get("googletest_canonical_patterns", {})
    patterns_str = str(patterns).lower()
    assert "throw" in patterns_str or "exception" in patterns_str, (
        "googletest_canonical_patterns must reference exception testing macros"
    )


# ---------------------------------------------------------------------------
# FOLLY-02: full-reference.md has GTest Core Macro Reference section
# ---------------------------------------------------------------------------

def test_full_reference_has_gtest_core_macro_section(cpp_full_reference):
    """Scenario FOLLY-02: full-reference.md must have a GTest Core Macro Reference
    section covering TEST vs TEST_F distinction."""
    assert "GoogleTest Core Macro Reference" in cpp_full_reference, (
        "full-reference.md missing 'GoogleTest Core Macro Reference' section"
    )


def test_gtest_core_macro_section_covers_expect_assert_table(cpp_full_reference):
    """Scenario FOLLY-02: Core Macro section must show EXPECT_EQ, EXPECT_TRUE,
    ASSERT_EQ — the fundamental assertion macros from Folly tests."""
    assert "EXPECT_EQ" in cpp_full_reference, "missing EXPECT_EQ in macro reference"
    assert "EXPECT_TRUE" in cpp_full_reference, "missing EXPECT_TRUE in macro reference"
    assert "ASSERT_EQ" in cpp_full_reference, "missing ASSERT_EQ in macro reference"


def test_gtest_core_macro_section_covers_add_failure(cpp_full_reference):
    """Scenario FOLLY-02: Core Macro section must mention ADD_FAILURE() — Folly
    uses it in ConvTest.cpp catch blocks."""
    assert "ADD_FAILURE" in cpp_full_reference, (
        "full-reference.md missing ADD_FAILURE() — used in Folly's ConvTest.cpp catch blocks"
    )


# ---------------------------------------------------------------------------
# FOLLY-03: full-reference.md has GTest Exception Testing section
# ---------------------------------------------------------------------------

def test_full_reference_has_gtest_exception_section(cpp_full_reference):
    """Scenario FOLLY-03: full-reference.md must have a GTest Exception Testing
    section with EXPECT_THROW, EXPECT_ANY_THROW, EXPECT_NO_THROW."""
    assert "GTest Exception Testing" in cpp_full_reference, (
        "full-reference.md missing 'GTest Exception Testing' section"
    )


def test_gtest_exception_section_covers_throw_macros(cpp_full_reference):
    """Scenario FOLLY-03: Exception section must show all three exception macros."""
    assert "EXPECT_THROW" in cpp_full_reference, "missing EXPECT_THROW"
    assert "EXPECT_ANY_THROW" in cpp_full_reference, "missing EXPECT_ANY_THROW"
    assert "EXPECT_NO_THROW" in cpp_full_reference, "missing EXPECT_NO_THROW"


def test_gtest_exception_section_references_calp_exception(cpp_full_reference):
    """Scenario FOLLY-03: The GTest Exception Testing section must reference
    CALPException hierarchy for IOC_ALP migration context.

    Amendment W-03: The prior OR-based assertion passed vacuously because
    'exception hierarchy' appeared in unrelated sections. This test extracts
    the GTest Exception Testing section and checks for CALPException within it."""
    section_marker = "GTest Exception Testing"
    start = cpp_full_reference.find(section_marker)
    assert start != -1, f"Section '{section_marker}' not found in any ref-*.md file"
    # Extract from section header to the next top-level section (##)
    after_header = cpp_full_reference[start + len(section_marker):]
    next_section = after_header.find("\n## ")
    section_content = after_header if next_section == -1 else after_header[:next_section]
    assert "CALPException" in section_content, (
        "The 'GTest Exception Testing' section must reference CALPException — "
        "IOC_ALP migration engineers need to see the CALPException hierarchy "
        "specifically in this section, not just somewhere in the combined ref content"
    )


# ---------------------------------------------------------------------------
# FOLLY-04: full-reference.md has GTest Template Test Helper Pattern section
# ---------------------------------------------------------------------------

def test_full_reference_has_gtest_template_helper_section(cpp_full_reference):
    """Scenario FOLLY-04: full-reference.md must have a GTest Template Test Helper
    Pattern section describing the Folly ArenaSmartPtrTest pattern."""
    assert "GTest Template Test Helper Pattern" in cpp_full_reference, (
        "full-reference.md missing 'GTest Template Test Helper Pattern' section"
    )


def test_gtest_template_helper_shows_template_function_called_from_test(cpp_full_reference):
    """Scenario FOLLY-04: section must show a template helper function called from
    a TEST() macro (Folly's ArenaSmartPtrTest pattern)."""
    assert "template" in cpp_full_reference and "testFoo" in cpp_full_reference or \
           "template" in cpp_full_reference and "helper" in cpp_full_reference.lower(), (
        "Template helper section must show template function called from TEST()"
    )


# ---------------------------------------------------------------------------
# FOLLY-05: full-reference.md has GTest Fixture Deep Dive section
# ---------------------------------------------------------------------------

def test_full_reference_has_gtest_fixture_section(cpp_full_reference):
    """Scenario FOLLY-05: full-reference.md must have a GTest Fixture Deep Dive
    section with SetUp/TearDown patterns."""
    assert "GTest Fixture Deep Dive" in cpp_full_reference, (
        "full-reference.md missing 'GTest Fixture Deep Dive' section"
    )


def test_gtest_fixture_section_covers_setup_teardown(cpp_full_reference):
    """Scenario FOLLY-05: Fixture section must cover SetUp() and TearDown()."""
    assert "SetUp" in cpp_full_reference and "TearDown" in cpp_full_reference, (
        "GTest Fixture Deep Dive must cover SetUp() and TearDown()"
    )


# ---------------------------------------------------------------------------
# FOLLY-06: full-reference.md has GTest Concurrency Testing section
# ---------------------------------------------------------------------------

def test_full_reference_has_gtest_concurrency_section(cpp_full_reference):
    """Scenario FOLLY-06: full-reference.md must have a GTest Concurrency Testing
    section with std::thread patterns from Folly."""
    assert "GTest Concurrency Testing" in cpp_full_reference, (
        "full-reference.md missing 'GTest Concurrency Testing' section"
    )


def test_gtest_concurrency_section_covers_thread_join(cpp_full_reference):
    """Scenario FOLLY-06: Concurrency section must show std::thread + join pattern
    as seen in Folly's CancellationTokenTest and ConcurrentLazyTest."""
    assert "std::thread" in cpp_full_reference and ".join()" in cpp_full_reference, (
        "GTest Concurrency section must show std::thread and .join()"
    )


# ---------------------------------------------------------------------------
# FOLLY-07: full-reference.md has ActiveTest.h to GTest Migration Playbook
# ---------------------------------------------------------------------------

def test_full_reference_has_activetest_migration_section(cpp_full_reference):
    """Scenario FOLLY-07: full-reference.md must have ActiveTest.h to GoogleTest
    Migration Playbook section for IOC_ALP transition."""
    assert "ActiveTest" in cpp_full_reference and "Migration" in cpp_full_reference, (
        "full-reference.md missing ActiveTest.h migration playbook section"
    )


def test_activetest_migration_section_has_mapping_table(cpp_full_reference):
    """Scenario FOLLY-07: Migration section must include a macro mapping table
    (ACTIVE_TEST → TEST_F or equivalent)."""
    # Must have both a table format marker and mention TEST_F in migration context
    migration_idx = cpp_full_reference.find("ActiveTest")
    migration_context = cpp_full_reference[migration_idx:migration_idx + 3000]
    assert "|" in migration_context, (
        "ActiveTest migration section must include a mapping table with | delimiters"
    )


# ---------------------------------------------------------------------------
# FOLLY-08: new example ENG-4.1-googletest-migration.md
# ---------------------------------------------------------------------------

def test_googletest_migration_example_exists():
    """Scenario FOLLY-08: avatars/technology/cpp/examples/ must contain
    ENG-4.1-googletest-migration.md."""
    example_path = Path("avatars/technology/cpp/examples/ENG-4.1-googletest-migration.md")
    assert example_path.exists(), (
        "ENG-4.1-googletest-migration.md does not exist — "
        "required for GTest migration guidance"
    )


def test_googletest_migration_example_has_frontmatter():
    """Scenario FOLLY-08: example must have valid YAML frontmatter."""
    example_path = Path("avatars/technology/cpp/examples/ENG-4.1-googletest-migration.md")
    content = example_path.read_text(encoding="utf-8")
    assert content.startswith("---"), "missing YAML frontmatter"
    assert "law_id:" in content, "frontmatter missing law_id"
    assert "avatar:" in content, "frontmatter missing avatar"


def test_googletest_migration_example_within_token_budget():
    """Scenario FOLLY-08: example must be within 600-token budget."""
    from tests.unit.test_cpp_avatar.avatar_test_helpers import check_token_budget
    example_path = Path("avatars/technology/cpp/examples/ENG-4.1-googletest-migration.md")
    check_token_budget(example_path)


def test_googletest_migration_example_has_compliant_noncompliant():
    """Scenario FOLLY-08: example must have COMPLIANT and NON-COMPLIANT sections."""
    example_path = Path("avatars/technology/cpp/examples/ENG-4.1-googletest-migration.md")
    content = example_path.read_text(encoding="utf-8")
    assert "COMPLIANT" in content, "missing COMPLIANT section"
    assert "NON-COMPLIANT" in content, "missing NON-COMPLIANT section"
