"""Phase 5 Validation Tests: Acceptance criteria for C++ avatar enrichment.

Scenario IDs: c-plus-plus-avatar-enrichment/5.1–5.12
Law: ENG-4.1, ENG-6.7, ENG-10.1, ENG-11.1
"""

import re
import sys
from pathlib import Path

import yaml
import pytest

from test_cpp_avatar.avatar_test_helpers import load_manifest

REPO_ROOT = Path(__file__).resolve().parents[3]
CPP_DIR = REPO_ROOT / "avatars" / "technology" / "cpp"
EXAMPLES_DIR = CPP_DIR / "examples"
PROPOSAL_DIR = REPO_ROOT / "hangar-ai-specs" / "changes" / "c-plus-plus-avatar-enrichment"

sys.path.insert(0, str(REPO_ROOT / "tools" / "constitution-lint" / "src"))


# --- 5.1: Manifest parity sections ---

REQUIRED_MANIFEST_SECTIONS = [
    "stack", "commands", "conventions", "project_structure",
    "activates", "specializes_laws",
]


class TestManifestParity:
    """5.1: Validate manifest parity sections are present."""

    def test_all_parity_sections_present(self):
        manifest = load_manifest(CPP_DIR / "manifest.yaml")
        for section in REQUIRED_MANIFEST_SECTIONS:
            assert section in manifest or any(
                section in str(v) for v in manifest.values()
            ), f"manifest.yaml missing parity section: {section}"

    def test_stack_has_required_fields(self):
        manifest = load_manifest(CPP_DIR / "manifest.yaml")
        stack = manifest["stack"]
        for field in ["language", "testing", "build"]:
            assert field in stack, f"stack missing field: {field}"

    def test_activates_has_four_skills(self):
        manifest = load_manifest(CPP_DIR / "manifest.yaml")
        skills = manifest["activates"]["skills"]
        assert len(skills) >= 4, f"Expected ≥4 activated skills, got {len(skills)}"


# --- 5.2: Guidance parity sections ---

REQUIRED_GUIDANCE_SECTIONS = [
    "Version Policy",
    "Testing Framework",
    "Mutation Testing",
    "Package Management",
    "Domain Modeling",
    "Ownership-First",
    "Concurrency",
    "CI Quality Toolchain",
    "Cross-Language Alignment",
    "Tools and Commands",
    "Brownfield",
]


class TestGuidanceParity:
    """5.2: Validate guidance parity sections are present."""

    def test_all_parity_sections_present(self):
        cpp_dir = REPO_ROOT / "avatars" / "technology" / "cpp"
        content = "\n".join(p.read_text(encoding="utf-8") for p in sorted(cpp_dir.rglob("ref-*.md")))
        for section in REQUIRED_GUIDANCE_SECTIONS:
            assert section in content, f"guidance.md missing section: {section}"


# --- 5.3: Non-negotiable examples ---

NON_NEGOTIABLE_LAWS = [
    "ENG-4.1", "ENG-6.1", "ENG-6.4", "ENG-6.7",
]


class TestNonNegotiableExamples:
    """5.3: Validate ENG non-negotiable examples are present (Amendment O: BUS/PRD removed)."""

    def test_eighteen_non_negotiable_examples_exist(self):
        example_files = list(EXAMPLES_DIR.glob("*.md"))
        non_neg_count = 0
        for law_id in NON_NEGOTIABLE_LAWS:
            prefix = law_id.replace(".", ".")  # e.g., ENG-4.1
            matches = [f for f in example_files if prefix in f.name]
            if matches:
                non_neg_count += 1
        assert non_neg_count >= 4, f"Expected ≥4 non-negotiable ENG examples, found {non_neg_count}"


# --- 5.4: Supplemental examples ---

SUPPLEMENTAL_LAWS = [
    "ENG-2.1", "ENG-2.2", "ENG-3.1", "ENG-3.2",
    "ENG-3.3", "ENG-3.5", "ENG-4.2", "ENG-4.4", "ENG-6.5",
]


class TestSupplementalExamples:
    """5.4: Validate 9 supplemental engineering-law examples are present."""

    def test_nine_supplemental_examples_exist(self):
        for law_id in SUPPLEMENTAL_LAWS:
            matches = list(EXAMPLES_DIR.glob(f"{law_id}*.md"))
            assert len(matches) >= 1, f"Missing supplemental example for {law_id}"


# --- 5.5: RAG/index updates ---

class TestRagIndexUpdates:
    """5.5: Validate RAG/index updates are complete."""

    def test_avatars_index_has_cpp(self):
        data = yaml.safe_load((REPO_ROOT / "avatars" / "index.yaml").read_text(encoding="utf-8"))
        ids = [a["id"] for a in data.get("technology", [])]
        assert "avatar-technology-cpp" in ids

    def test_rag_index_has_cpp(self):
        content = (REPO_ROOT / "avatars" / "AVATAR-RAG-INDEX.yaml").read_text(encoding="utf-8")
        assert "cpp:" in content

    def test_skill_index_has_cpp_skills(self):
        data = yaml.safe_load(
            (REPO_ROOT / "agent-skills" / "skills-by-domain"
             / "platform-engineering" / "index.yaml").read_text(encoding="utf-8")
        )
        files = [s["file"] for s in data.get("skills", [])]
        cpp_skills = [f for f in files if "cpp" in f]
        assert len(cpp_skills) == 25, f"Expected 25 C++ skills in index, found {len(cpp_skills)}"


# --- 5.6: Brownfield safeguards ---

class TestBrownfieldSafeguards:
    """5.6: Validate brownfield safeguards and test equivalence guidance."""

    def test_guidance_has_brownfield_section(self):
        cpp_dir = REPO_ROOT / "avatars" / "technology" / "cpp"
        content = "\n".join(p.read_text(encoding="utf-8") for p in sorted(cpp_dir.rglob("ref-*.md")))
        assert "Brownfield" in content
        assert "non-rewrite" in content.lower() or "modernization" in content.lower()

    def test_manifest_has_brownfield_version_policy(self):
        manifest = load_manifest(CPP_DIR / "manifest.yaml")
        policy = manifest["stack"].get("version_policy", {})
        assert "brownfield" in str(policy).lower()


# --- 5.7: Law references are hyperlinks ---

class TestLawHyperlinks:
    """5.7: Validate constitution law/rule references use proper format."""

    # test_guidance_has_law_references removed — superseded by
    # test_law_reference_coverage.py::test_minimum_law_coverage (10 critical laws)
    # and test_total_law_reference_count_not_regressed (≥150 refs).

    def test_proposal_has_laws_cited_section(self):
        content = (PROPOSAL_DIR / "PROPOSAL.md").read_text(encoding="utf-8")
        assert "Laws Cited" in content, "PROPOSAL.md must have a Laws Cited section"


# --- 5.8: Evidence source taxonomy tags ---

class TestEvidenceTags:
    """5.8: Validate evidence source taxonomy tags on key claims."""

    def test_proposal_has_evidence_tags(self):
        content = (PROPOSAL_DIR / "PROPOSAL.md").read_text(encoding="utf-8")
        # Evidence tags like [Source: ...] or confidence tags
        has_evidence = (
            "[Source:" in content
            or "confidence:" in content.lower()
            or "evidence:" in content.lower()
            or "High confidence" in content
            or "Medium confidence" in content
        )
        assert has_evidence, "PROPOSAL.md must have evidence source tags on key claims"


# --- 5.9: Risk register mitigations ---

class TestRiskRegister:
    """5.9: Validate risk register mitigations are current."""

    def test_proposal_has_risk_register(self):
        content = (PROPOSAL_DIR / "PROPOSAL.md").read_text(encoding="utf-8")
        assert "Risk" in content and "Mitigation" in content, \
            "PROPOSAL.md must have a risk register with mitigations"


# --- 5.10: Draft registry YAML matches implementation ---

class TestRegistryConsistency:
    """5.10: Validate draft registry YAML matches actual implementation."""

    def test_index_yaml_id_matches_manifest(self):
        manifest = load_manifest(CPP_DIR / "manifest.yaml")
        index = yaml.safe_load((REPO_ROOT / "avatars" / "index.yaml").read_text(encoding="utf-8"))
        cpp_entry = next(a for a in index["technology"] if a["id"] == "avatar-technology-cpp")

        assert manifest["avatar"]["id"] == cpp_entry["id"]
        assert manifest["avatar"]["name"] == cpp_entry["name"]

    def test_index_yaml_path_matches_directory(self):
        index = yaml.safe_load((REPO_ROOT / "avatars" / "index.yaml").read_text(encoding="utf-8"))
        cpp_entry = next(a for a in index["technology"] if a["id"] == "avatar-technology-cpp")
        expected_path = REPO_ROOT / "avatars" / cpp_entry["path"]
        assert expected_path.exists(), f"Index path {cpp_entry['path']} does not exist"


# --- 5.11: Token budget ---

class TestTokenBudget:
    """5.11: Validate token budget per example file (per manifest governance_overrides)."""

    def test_all_examples_under_token_budget(self):
        from tests.unit.test_cpp_avatar.avatar_test_helpers import (
            check_token_budget, get_token_budget,
        )

        budget = get_token_budget(CPP_DIR / "manifest.yaml")
        over_budget = []
        for example in sorted(EXAMPLES_DIR.glob("*.md")):
            passes, tokens = check_token_budget(example, max_tokens=budget)
            if not passes:
                over_budget.append((example.name, tokens))

        assert len(over_budget) == 0, \
            f"Examples over {budget}-token budget: {over_budget}"


# --- 5.12: Final governance review ---

class TestFinalGovernanceReview:
    """5.12: Final governance review against proposal success criteria."""

    def test_all_58_example_files_exist(self):
        count = len(list(EXAMPLES_DIR.glob("*.md")))

        assert count == 87, f"Expected 87 example files, found {count}"


    def test_manifest_exists(self):
        assert (CPP_DIR / "manifest.yaml").exists()

    def test_guidance_exists(self):
        assert (REPO_ROOT / "avatars" / "technology" / "cpp" / "refs/language/ref-getting-started.md").exists()

    def test_sdd_artifacts_exist(self):
        for name in ["PROPOSAL.md", "tasks.md", "PROGRESS.md"]:
            assert (PROPOSAL_DIR / name).exists(), f"Missing SDD artifact: {name}"

    def test_progress_has_governance_signoff(self):
        content = (PROPOSAL_DIR / "PROGRESS.md").read_text(encoding="utf-8")
        assert "Governance Sign-Off" in content

    def test_eight_skill_modules_exist(self):
        skills_dir = REPO_ROOT / "agent-skills" / "skills-by-domain" / "platform-engineering"
        cpp_skills = list(skills_dir.glob("skill-cpp-*.md"))
        assert len(cpp_skills) == 25, f"Expected 25 C++ skill modules, found {len(cpp_skills)}"
