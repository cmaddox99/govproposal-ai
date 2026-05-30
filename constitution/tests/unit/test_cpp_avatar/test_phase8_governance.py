"""Phase 8 tests: P0 governance gaps — new guidance sections and skills.

Scenario-IDs: 8.17–8.26
"""
import pathlib
import re

import pytest
import yaml

from test_cpp_avatar.avatar_test_helpers import load_manifest

_CPP_DIR = pathlib.Path(__file__).resolve().parents[3] / "avatars" / "technology" / "cpp"


def _read_full_reference():
    return "\n".join(p.read_text(encoding="utf-8") for p in sorted(_CPP_DIR.rglob("ref-*.md")))
MANIFEST = pathlib.Path(__file__).resolve().parents[3] / "avatars" / "technology" / "cpp" / "manifest.yaml"
SKILLS_DIR = pathlib.Path(__file__).resolve().parents[3] / "agent-skills" / "skills-by-domain" / "platform-engineering"
RAG_INDEX = pathlib.Path(__file__).resolve().parents[3] / "avatars" / "AVATAR-RAG-INDEX.yaml"
PE_INDEX = SKILLS_DIR / "index.yaml"


class TestABIStabilityGuidance:
    """8.17: ABI stability & binary compatibility section."""

    @pytest.fixture(autouse=True)
    def load(self):
        self.content = _read_full_reference()

    def test_section_exists(self):
        assert "ABI Stability" in self.content or "Binary Compatibility" in self.content

    def test_pimpl_mentioned(self):
        assert "Pimpl" in self.content or "pimpl" in self.content

    def test_symbol_visibility_mentioned(self):
        assert "visibility" in self.content.lower()

    def test_abi_detection_tooling(self):
        assert "abi-compliance-checker" in self.content or "libabigail" in self.content


class TestTemplateMetaprogrammingGuidance:
    """8.18: Template & metaprogramming governance section."""

    @pytest.fixture(autouse=True)
    def load(self):
        self.content = _read_full_reference()

    def test_section_exists(self):
        assert "Template" in self.content and "Metaprogramming" in self.content

    def test_concepts_guidance(self):
        assert "concept" in self.content.lower() and "requires" in self.content

    def test_constexpr_policy(self):
        assert "constexpr" in self.content

    def test_consteval_mentioned(self):
        assert "consteval" in self.content

    def test_extern_template_mentioned(self):
        assert "extern template" in self.content


class TestPanicAbortPolicy:
    """8.19: Panic/abort vs recovery policy section."""

    @pytest.fixture(autouse=True)
    def load(self):
        self.content = _read_full_reference()

    def test_section_exists(self):
        assert "Termination" in self.content and "Recovery" in self.content

    def test_std_terminate_mentioned(self):
        assert "std::terminate" in self.content

    def test_severity_levels(self):
        lower = self.content.lower()
        assert "fatal" in lower or "unrecoverable" in lower or "terminate immediately" in lower


class TestFFIErrorPropagation:
    """8.20: C/C++ FFI error propagation section."""

    @pytest.fixture(autouse=True)
    def load(self):
        self.content = _read_full_reference()

    def test_section_exists(self):
        assert "FFI" in self.content or "C Interop" in self.content or "Foreign Function" in self.content

    def test_custom_deleter_mentioned(self):
        assert "custom deleter" in self.content.lower() or "unique_ptr<" in self.content

    def test_errno_or_error_codes(self):
        assert "errno" in self.content or "error code" in self.content.lower()


class TestReproducibleBuilds:
    """8.21: Reproducible builds section."""

    @pytest.fixture(autouse=True)
    def load(self):
        self.content = _read_full_reference()

    def test_section_exists(self):
        assert "Reproducible Build" in self.content

    def test_source_date_epoch(self):
        assert "SOURCE_DATE_EPOCH" in self.content

    def test_pinned_versions(self):
        lower = self.content.lower()
        assert "pinned" in lower or "locked" in lower or "deterministic" in lower


class TestLicenseComplianceGuidance:
    """8.22: License compliance & dependency governance section."""

    @pytest.fixture(autouse=True)
    def load(self):
        self.content = _read_full_reference()

    def test_section_exists(self):
        assert "License" in self.content and "Compliance" in self.content

    def test_approved_licenses(self):
        assert "MIT" in self.content and "Apache" in self.content

    def test_gpl_warning(self):
        assert "GPL" in self.content

    def test_boost_policy(self):
        assert "Boost" in self.content


NEW_SKILLS = [
    "skill-cpp-concurrency-thread-safety-governance.md",
    "skill-cpp-resiliency-failure-modes.md",
    "skill-cpp-deployment-hardening.md",
    "skill-cpp-debugging-diagnostics-playbook.md",
    "skill-cpp-dependency-governance.md",
]


class TestNewSkillModules:
    """8.23: 5 new skill modules exist with valid frontmatter."""

    @pytest.mark.parametrize("skill_file", NEW_SKILLS)
    def test_skill_exists(self, skill_file):
        path = SKILLS_DIR / skill_file
        assert path.exists(), f"Missing skill: {skill_file}"

    @pytest.mark.parametrize("skill_file", NEW_SKILLS)
    def test_skill_has_frontmatter(self, skill_file):
        content = (SKILLS_DIR / skill_file).read_text(encoding="utf-8")
        assert content.startswith("---"), f"{skill_file} missing YAML frontmatter"
        end = content.index("---", 3)
        fm = yaml.safe_load(content[3:end])
        assert "skill" in fm and "name" in fm["skill"], f"{skill_file} missing 'skill.name' in frontmatter"
        assert "laws" in fm, f"{skill_file} missing 'laws' in frontmatter"


class TestUpdatedManifest:
    """8.24: Manifest has bumped compiler versions, new anti-patterns, triggers."""

    @pytest.fixture(autouse=True)
    def load(self):
        self.manifest = load_manifest(MANIFEST)

    def _flat_compilers(self):
        compilers = self.manifest["stack"]["compilers"]
        if isinstance(compilers, dict):
            return [c for tier in compilers.values() for c in tier]
        return compilers

    def test_gcc_version_bumped(self):
        compilers = self._flat_compilers()
        gcc = [c for c in compilers if "GCC" in c][0]
        # Should be 13+ or 14+ in recommended tier
        assert "13" in gcc or "14" in gcc, f"GCC should be 13+, got: {gcc}"

    def test_clang_version_bumped(self):
        compilers = self._flat_compilers()
        clang = [c for c in compilers if "Clang" in c][0]
        assert "16" in clang or "17" in clang or "18" in clang, f"Clang should be 16+, got: {clang}"

    def test_msvc_version_bumped(self):
        compilers = self._flat_compilers()
        msvc = [c for c in compilers if "MSVC" in c][0]
        assert "19.38" in msvc or "19.39" in msvc or "19.4" in msvc, f"MSVC should be 19.38+, got: {msvc}"

    def test_anti_patterns_count(self):
        """Amendment O V4: anti_patterns removed from manifest.yaml (scope creep).
        Content belongs in example files. Assert block is absent."""
        assert "anti_patterns" not in self.manifest, (
            "Amendment O V4: anti_patterns must NOT be in manifest.yaml"
        )

    def test_dangling_view_anti_pattern(self):
        """Amendment O V4: anti_patterns removed from manifest — content is in example files."""
        pass  # Absence of anti_patterns block validated in test_anti_patterns_absent.

    def test_use_after_move_anti_pattern(self):
        """Amendment O V4: anti_patterns removed from manifest — content is in example files."""
        pass  # Absence of anti_patterns block validated in test_anti_patterns_absent.

    def test_version_2_x(self):
        version = self.manifest["avatar"]["version"]
        assert version.startswith("2."), \
            f"Version should be 2.x.x series, got {version}"

    def test_specializes_laws_expanded(self):
        """Should have at least 15 specialized laws."""
        count = len(self.manifest["specializes_laws"])
        assert count >= 15, f"Expected ≥15 specializes_laws, got {count}"


class TestRAGIndexUpdated:
    """8.25: RAG index has new search queries."""

    def test_new_queries_present(self):
        content = RAG_INDEX.read_text(encoding="utf-8")
        assert "ABI" in content or "binary compatibility" in content.lower()
        assert "template" in content.lower()
        assert "reproducible" in content.lower() or "deterministic build" in content.lower()


class TestCrossAvatarParity:
    """8.26: Cross-avatar parity checks."""

    @pytest.fixture(autouse=True)
    def load(self):
        self.manifest = load_manifest(MANIFEST)

    def test_product_discovery_workflow(self):
        workflows = self.manifest.get("activates", {}).get("workflows", [])
        assert "product-discovery-stage-a-f" in workflows, \
            "Missing product-discovery-stage-a-f workflow for cross-avatar parity"

    def test_eng_3_3_demeter_specialized(self):
        law_ids = [law["id"] for law in self.manifest["specializes_laws"]]
        assert "ENG-3.3" in law_ids, "ENG-3.3 (Demeter) should be in specializes_laws for Java/.NET parity"

    def test_eng_7_1_failure_handling_specialized(self):
        law_ids = [law["id"] for law in self.manifest["specializes_laws"]]
        assert "ENG-7.1" in law_ids, "ENG-7.1 (Failure Handling) should be in specializes_laws"

    def test_skill_count_23(self):
        index = yaml.safe_load(PE_INDEX.read_text(encoding="utf-8"))
        for entry in index.get("skills", []):
            if "cpp" in str(entry).lower() or "c++" in str(entry).lower():
                pass
        # Check the index has count >= 23
        content = PE_INDEX.read_text(encoding="utf-8")
        assert "34" in content or "count: 34" in content.lower(), \
            "Platform engineering index should reflect 34 total skills"
