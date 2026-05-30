"""Test suite for cpp-ref-file-rightsizing (Phases 2-15).

Each test asserts that a split output file exists and is within the
3,500-token budget (where token = len(text) // 4).

Scenario ID: cpp-ref-file-rightsizing
Law: ENG-4.1 (Atomic TDD), ENG-6.7 (Audit Trail)
"""
from pathlib import Path

CPP_DIR = Path(__file__).resolve().parents[3] / "avatars" / "technology" / "cpp"


# ---------------------------------------------------------------------------
# Phase 2: ref-testing-ci.md → 3-way split
# ---------------------------------------------------------------------------

def test_ref_testing_ci_policy_exists_and_within_budget():
    f = CPP_DIR / "refs/testing/ref-testing-ci-policy.md"
    assert f.exists(), "ref-testing-ci-policy.md does not exist — Phase 2 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-testing-ci-policy.md exceeds 3500 token budget"


def test_ref_testing_gtest_core_exists_and_within_budget():
    f = CPP_DIR / "refs/testing/ref-testing-gtest-core.md"
    assert f.exists(), "ref-testing-gtest-core.md does not exist — Phase 2 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-testing-gtest-core.md exceeds 3500 token budget"


def test_ref_testing_gtest_advanced_exists_and_within_budget():
    f = CPP_DIR / "refs/testing/ref-testing-gtest-advanced.md"
    assert f.exists(), "ref-testing-gtest-advanced.md does not exist — Phase 2 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-testing-gtest-advanced.md exceeds 3500 token budget"


# ---------------------------------------------------------------------------
# Phase 3: ref-brownfield-config.md → 2-way split
# ---------------------------------------------------------------------------

def test_ref_brownfield_adoption_exists_and_within_budget():
    f = CPP_DIR / "refs/legacy/ref-brownfield-adoption.md"
    assert f.exists(), "ref-brownfield-adoption.md does not exist — Phase 3 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-brownfield-adoption.md exceeds 3500 token budget"


def test_ref_brownfield_project_config_exists_and_within_budget():
    f = CPP_DIR / "refs/legacy/ref-brownfield-project-config.md"
    assert f.exists(), "ref-brownfield-project-config.md does not exist — Phase 3 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-brownfield-project-config.md exceeds 3500 token budget"

# ---------------------------------------------------------------------------
# Phase 4: ref-migration-playbooks.md -> 2-way split
# ---------------------------------------------------------------------------

def test_ref_migration_pre_cpp17_exists_and_within_budget():
    f = CPP_DIR / "refs/legacy/ref-migration-pre-cpp17.md"
    assert f.exists(), "ref-migration-pre-cpp17.md does not exist - Phase 4 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-migration-pre-cpp17.md exceeds 3500 token budget"


def test_ref_migration_cpp17_plus_exists_and_within_budget():
    f = CPP_DIR / "refs/legacy/ref-migration-cpp17-plus.md"
    assert f.exists(), "ref-migration-cpp17-plus.md does not exist - Phase 4 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-migration-cpp17-plus.md exceeds 3500 token budget"

# ---------------------------------------------------------------------------
# Phase 5: ref-concurrency.md -> 2-way split
# ---------------------------------------------------------------------------

def test_ref_concurrency_threading_exists_and_within_budget():
    f = CPP_DIR / "refs/safety/ref-concurrency-threading.md"
    assert f.exists(), "ref-concurrency-threading.md does not exist - Phase 5 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-concurrency-threading.md exceeds 3500 token budget"


def test_ref_concurrency_async_exists_and_within_budget():
    f = CPP_DIR / "refs/safety/ref-concurrency-async.md"
    assert f.exists(), "ref-concurrency-async.md does not exist - Phase 5 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-concurrency-async.md exceeds 3500 token budget"

# ---------------------------------------------------------------------------
# Phase 6: ref-object-design.md -> 2-way split (H3 split at L334)
# ---------------------------------------------------------------------------

def test_ref_object_design_rehabilitation_exists_and_within_budget():
    f = CPP_DIR / "refs/language/ref-object-design-rehabilitation.md"
    assert f.exists(), "ref-object-design-rehabilitation.md does not exist - Phase 6 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-object-design-rehabilitation.md exceeds 3500 token budget"


def test_ref_object_design_patterns_exists_and_within_budget():
    f = CPP_DIR / "refs/language/ref-object-design-patterns.md"
    assert f.exists(), "ref-object-design-patterns.md does not exist - Phase 6 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-object-design-patterns.md exceeds 3500 token budget"

# ---------------------------------------------------------------------------
# Phase 7: ref-advanced-cpp.md -> 2-way split
# ---------------------------------------------------------------------------

def test_ref_templates_metaprogramming_exists_and_within_budget():
    f = CPP_DIR / "refs/language/ref-templates-metaprogramming.md"
    assert f.exists(), "ref-templates-metaprogramming.md does not exist - Phase 7 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-templates-metaprogramming.md exceeds 3500 token budget"


def test_ref_advanced_patterns_exists_and_within_budget():
    f = CPP_DIR / "refs/language/ref-advanced-patterns.md"
    assert f.exists(), "ref-advanced-patterns.md does not exist - Phase 7 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-advanced-patterns.md exceeds 3500 token budget"

# ---------------------------------------------------------------------------
# Phase 8: ref-core-language.md -> 2-way split
# ---------------------------------------------------------------------------

def test_ref_core_type_safety_exists_and_within_budget():
    f = CPP_DIR / "refs/language/ref-core-type-safety.md"
    assert f.exists(), "ref-core-type-safety.md does not exist - Phase 8 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-core-type-safety.md exceeds 3500 token budget"


def test_ref_core_modern_idioms_exists_and_within_budget():
    f = CPP_DIR / "refs/language/ref-core-modern-idioms.md"
    assert f.exists(), "ref-core-modern-idioms.md does not exist - Phase 8 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-core-modern-idioms.md exceeds 3500 token budget"

# ---------------------------------------------------------------------------
# Phase 9: ref-domain-modeling.md -> 2-way split
# ---------------------------------------------------------------------------

def test_ref_domain_patterns_exists_and_within_budget():
    f = CPP_DIR / "refs/language/ref-domain-patterns.md"
    assert f.exists(), "ref-domain-patterns.md does not exist - Phase 9 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-domain-patterns.md exceeds 3500 token budget"


def test_ref_domain_quality_exists_and_within_budget():
    f = CPP_DIR / "refs/language/ref-domain-quality.md"
    assert f.exists(), "ref-domain-quality.md does not exist - Phase 9 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-domain-quality.md exceeds 3500 token budget"

# ---------------------------------------------------------------------------
# Phase 10: ref-legacy-smells.md -> 2-way split (H3 split at L165)
# ---------------------------------------------------------------------------

def test_ref_legacy_smells_structural_exists_and_within_budget():
    f = CPP_DIR / "refs/legacy/ref-legacy-smells-structural.md"
    assert f.exists(), "ref-legacy-smells-structural.md does not exist - Phase 10 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-legacy-smells-structural.md exceeds 3500 token budget"


def test_ref_legacy_smells_patterns_exists_and_within_budget():
    f = CPP_DIR / "refs/legacy/ref-legacy-smells-patterns.md"
    assert f.exists(), "ref-legacy-smells-patterns.md does not exist - Phase 10 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-legacy-smells-patterns.md exceeds 3500 token budget"

# ---------------------------------------------------------------------------
# Phase 11: ref-legacy-mental-models.md -> 2-way split (H3 split at L189)
# ---------------------------------------------------------------------------

def test_ref_mental_models_memory_exists_and_within_budget():
    f = CPP_DIR / "refs/legacy/ref-mental-models-memory.md"
    assert f.exists(), "ref-mental-models-memory.md does not exist - Phase 11 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-mental-models-memory.md exceeds 3500 token budget"


def test_ref_mental_models_lang_exists_and_within_budget():
    f = CPP_DIR / "refs/legacy/ref-mental-models-lang.md"
    assert f.exists(), "ref-mental-models-lang.md does not exist - Phase 11 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-mental-models-lang.md exceeds 3500 token budget"

# ---------------------------------------------------------------------------
# Phase 12: ref-build-toolchain.md -> 2-way split
# ---------------------------------------------------------------------------

def test_ref_build_packages_exists_and_within_budget():
    f = CPP_DIR / "refs/testing/ref-build-packages.md"
    assert f.exists(), "ref-build-packages.md does not exist - Phase 12 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-build-packages.md exceeds 3500 token budget"


def test_ref_build_ubsan_msvc_exists_and_within_budget():
    f = CPP_DIR / "refs/testing/ref-build-ubsan-msvc.md"
    assert f.exists(), "ref-build-ubsan-msvc.md does not exist - Phase 12 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-build-ubsan-msvc.md exceeds 3500 token budget"

# ---------------------------------------------------------------------------
# Phase 13: ref-safety-aviation.md -> 2-way split
# ---------------------------------------------------------------------------

def test_ref_safety_jni_abi_exists_and_within_budget():
    f = CPP_DIR / "refs/safety/ref-safety-jni-abi.md"
    assert f.exists(), "ref-safety-jni-abi.md does not exist - Phase 13 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-safety-jni-abi.md exceeds 3500 token budget"


def test_ref_safety_far117_cwr_exists_and_within_budget():
    f = CPP_DIR / "refs/safety/ref-safety-far117-cwr.md"
    assert f.exists(), "ref-safety-far117-cwr.md does not exist - Phase 13 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-safety-far117-cwr.md exceeds 3500 token budget"

# ---------------------------------------------------------------------------
# Phase 14: ref-safety-memory.md -> 2-way split
# ---------------------------------------------------------------------------

def test_ref_safety_misra_do178_exists_and_within_budget():
    f = CPP_DIR / "refs/safety/ref-safety-misra-do178.md"
    assert f.exists(), "ref-safety-misra-do178.md does not exist - Phase 14 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-safety-misra-do178.md exceeds 3500 token budget"


def test_ref_safety_memory_lifetime_exists_and_within_budget():
    f = CPP_DIR / "refs/safety/ref-safety-memory-lifetime.md"
    assert f.exists(), "ref-safety-memory-lifetime.md does not exist - Phase 14 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-safety-memory-lifetime.md exceeds 3500 token budget"

# ---------------------------------------------------------------------------
# Phase 15: ref-legacy-navigation.md -> 2-way truncation
# ---------------------------------------------------------------------------

def test_ref_legacy_navigation_within_budget():
    f = CPP_DIR / "refs/legacy/ref-legacy-navigation.md"
    assert f.exists(), "ref-legacy-navigation.md does not exist"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-legacy-navigation.md exceeds 3500 token budget"


def test_ref_legacy_triage_playbook_exists_and_within_budget():
    f = CPP_DIR / "refs/legacy/ref-legacy-triage-playbook.md"
    assert f.exists(), "ref-legacy-triage-playbook.md does not exist - Phase 15 split not done"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-legacy-triage-playbook.md exceeds 3500 token budget"

# ---------------------------------------------------------------------------
# ESE budget fix: ref-brownfield-survival.md split — Coplien section extracted
# ---------------------------------------------------------------------------

def test_ref_brownfield_survival_within_budget():
    f = CPP_DIR / "refs/legacy/ref-brownfield-survival.md"
    assert f.exists(), "ref-brownfield-survival.md does not exist"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, \
        "ref-brownfield-survival.md exceeds 3500 token budget — Coplien section must stay in ref-brownfield-coplien.md"


def test_ref_brownfield_coplien_exists_and_within_budget():
    f = CPP_DIR / "refs/legacy/ref-brownfield-coplien.md"
    assert f.exists(), "ref-brownfield-coplien.md does not exist — Coplien-era patterns must be extracted from ref-brownfield-survival.md"
    assert len(f.read_text(encoding='utf-8')) // 4 <= 3500, "ref-brownfield-coplien.md exceeds 3500 token budget"
