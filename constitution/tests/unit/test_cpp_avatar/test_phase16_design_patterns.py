"""Phase 16 — Design Pattern Governance and Architectural Defaults tests.

Validates 6 high-value additions: object slicing, DI pattern, safe observer,
configuration management, health checks, and project type archetypes.
"""

import pathlib
import re

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[3]
_CPP_DIR = ROOT / "avatars" / "technology" / "cpp"
MANIFEST = ROOT / "avatars" / "technology" / "cpp" / "manifest.yaml"


@pytest.fixture(scope="module")
def guidance_text():
    return "\n".join(p.read_text(encoding="utf-8") for p in sorted(_CPP_DIR.rglob("ref-*.md")))


@pytest.fixture(scope="module")
def manifest_text():
    return MANIFEST.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def manifest_data():
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


# ── 16.1: Object Slicing Anti-Pattern ──────────────────────────────────

class TestObjectSlicing:
    """Verify object slicing is documented as anti-pattern + guidance."""

    def test_slicing_in_manifest(self, manifest_text):
        pass  # Amendment O V4: anti_patterns removed from manifest.
        # Object slicing coverage validated in test_slicing_in_guidance.

    def test_slicing_in_guidance(self, guidance_text):
        assert "slicing" in guidance_text.lower(), (
            "Object slicing should be discussed in guidance"
        )

    def test_slicing_mentions_pass_by_value(self, guidance_text):
        # Object slicing happens when passing derived by value to base
        lower = guidance_text.lower()
        slicing_area = lower[lower.find("slicing"):][:2000]
        assert "value" in slicing_area or "copy" in slicing_area


# ── 16.2: Dependency Injection Pattern ─────────────────────────────────

class TestDependencyInjection:
    """Verify DI pattern is codified in guidance."""

    def test_section_exists(self, guidance_text):
        assert "Dependency Injection" in guidance_text

    def test_constructor_injection(self, guidance_text):
        section = _extract_section(guidance_text, "Dependency Injection")
        assert section, "DI section not found"
        assert "constructor" in section.lower()

    def test_composition_root(self, guidance_text):
        section = _extract_section(guidance_text, "Dependency Injection")
        assert section, "DI section not found"
        assert "composition root" in section.lower() or "main" in section.lower()

    def test_interface_ownership(self, guidance_text):
        section = _extract_section(guidance_text, "Dependency Injection")
        assert section, "DI section not found"
        assert "unique_ptr" in section or "Interface" in section

    def test_law_reference(self, guidance_text):
        section = _extract_section(guidance_text, "Dependency Injection")
        assert section, "DI section not found"
        assert "[ENG-2" in section, "Should reference architecture law"

    def test_code_example(self, guidance_text):
        section = _extract_section(guidance_text, "Dependency Injection")
        assert section, "DI section not found"
        assert "```cpp" in section, "Should have a code example"


# ── 16.3: Safe Observer Pattern ────────────────────────────────────────

class TestSafeObserver:
    """Verify safe observer pattern with weak_ptr."""

    def test_observer_in_guidance(self, guidance_text):
        assert "observer" in guidance_text.lower()

    def test_weak_ptr_deregistration(self, guidance_text):
        lower = guidance_text.lower()
        # Find the "Safe Observer" anti-pattern section specifically
        obs_start = lower.find("safe observer")
        if obs_start < 0:
            obs_start = lower.find("observer with raw")
        if obs_start < 0:
            obs_start = lower.find("### safe observer")
        assert obs_start >= 0, "Safe Observer section not found"
        obs_area = lower[obs_start:][:3000]
        assert "weak_ptr" in obs_area or "weak" in obs_area, (
            "Safe observer should use weak_ptr"
        )

    def test_dangling_prevention(self, guidance_text):
        lower = guidance_text.lower()
        obs_start = lower.find("safe observer")
        if obs_start < 0:
            obs_start = lower.find("observer with raw")
        assert obs_start >= 0, "Safe Observer section not found"
        obs_area = lower[obs_start:][:3000]
        assert "dangling" in obs_area or "deregist" in obs_area or "automatic" in obs_area


# ── 16.4: Configuration Management ─────────────────────────────────────

class TestConfigurationManagement:
    """Verify configuration management guidance."""

    def test_section_exists(self, guidance_text):
        assert "Configuration Management" in guidance_text or "Configuration Loading" in guidance_text

    def test_library_options(self, guidance_text):
        section = _extract_section(guidance_text, "Configuration")
        assert section, "Configuration section not found"
        lower = section.lower()
        options = sum(1 for lib in ["yaml-cpp", "toml", "json", "libconfig"]
                      if lib in lower)
        assert options >= 2, "Should mention at least 2 config library options"

    def test_validation_mentioned(self, guidance_text):
        section = _extract_section(guidance_text, "Configuration")
        assert section, "Configuration section not found"
        assert "validat" in section.lower(), "Should mention validation"


# ── 16.5: Health Check / Readiness Probe ───────────────────────────────

class TestHealthCheck:
    """Verify health check / readiness probe guidance."""

    def test_health_check_in_guidance(self, guidance_text):
        lower = guidance_text.lower()
        assert "health check" in lower or "readiness probe" in lower or "health endpoint" in lower

    def test_kubernetes_context(self, guidance_text):
        lower = guidance_text.lower()
        assert "kubernetes" in lower or "k8s" in lower or "liveness" in lower

    def test_dependency_checks(self, guidance_text):
        lower = guidance_text.lower()
        health_start = max(lower.find("health check"), lower.find("readiness"))
        if health_start < 0:
            pytest.fail("Health check section not found")
        health_area = lower[health_start:][:2000]
        assert "dependency" in health_area or "database" in health_area or "downstream" in health_area


# ── 16.6: Project Type Archetype Matrix ────────────────────────────────

class TestProjectArchetypes:
    """Verify project type archetypes in ref-infrastructure.md.

    Content routed from manifest.yaml per avatar-model-schema §3 (forbidden block).
    """

    def test_archetypes_in_full_reference(self, guidance_text):
        assert "Project Archetypes" in guidance_text

    PROJECT_TYPES = ["service", "pipeline", "cli", "library"]

    @pytest.mark.parametrize("ptype", PROJECT_TYPES)
    def test_project_type_defined(self, guidance_text, ptype):
        assert ptype.lower() in guidance_text.lower(), (
            f"Project type '{ptype}' not in ref-infrastructure.md archetypes"
        )


# ── Helper ──────────────────────────────────────────────────────────────

def _extract_section(text: str, heading: str) -> str:
    """Extract a ## section from markdown text."""
    pattern = rf"^## .*{re.escape(heading)}.*?(?=\n## |\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return match.group(0) if match else ""
