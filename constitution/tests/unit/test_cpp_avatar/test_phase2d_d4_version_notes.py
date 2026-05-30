"""
Phase 2D — D4: Inline version callout boxes in 4 ref files.

Each file must have ★ C++NN markers on the sections that only apply
to specific C++ versions, helping users quickly identify what
is/isn't available in their declared project standard.

Target sections (from PHASE2-PROPOSAL.md):
- ref-core-modern-idioms.md : designated initializers (C++20), std::any (C++17)
- ref-advanced-patterns.md  : PMR allocators (C++17), std::span (C++20)
- ref-safety-memory-lifetime.md : std::pmr (C++17)
- ref-templates-metaprogramming.md : Concepts (C++20) vs SFINAE (C++11)
"""

import pathlib
import pytest

REPO_ROOT = pathlib.Path(__file__).parent.parent.parent.parent
REFS_DIR  = REPO_ROOT / "avatars" / "technology" / "cpp" / "refs"

CORE_IDIOMS  = REFS_DIR / "language" / "ref-core-modern-idioms.md"
ADV_PATTERNS = REFS_DIR / "language" / "ref-advanced-patterns.md"
MEM_LIFETIME = REFS_DIR / "safety" / "ref-safety-memory-lifetime.md"
TEMPLATES    = REFS_DIR / "language" / "ref-templates-metaprogramming.md"


class TestD4CoreModernIdioms:
    """D4a: ref-core-modern-idioms.md must annotate version-specific sections."""

    def test_designated_initializers_has_cpp20_callout(self):
        content = CORE_IDIOMS.read_text(encoding="utf-8")
        # The designated-initializers section or its header must indicate C++20
        assert "designated" in content.lower(), "Expected designated initializer content"
        # Check for a C++20 marker near the designated initializer text
        idx = content.lower().find("designated")
        window = content[max(0, idx - 200): idx + 600]
        assert "C++20" in window or "★ C++20" in window, (
            "Designated initializers section must have ★ C++20 callout"
        )

    def test_std_any_has_cpp17_callout(self):
        content = CORE_IDIOMS.read_text(encoding="utf-8")
        assert "std::any" in content, "Expected std::any in ref-core-modern-idioms.md"
        idx = content.find("std::any")
        window = content[max(0, idx - 200): idx + 600]
        assert "C++17" in window or "★ C++17" in window, (
            "std::any section must have ★ C++17 callout"
        )


class TestD4AdvancedPatterns:
    """D4b: ref-advanced-patterns.md must annotate PMR and std::span."""

    def test_pmr_has_cpp17_callout(self):
        content = ADV_PATTERNS.read_text(encoding="utf-8")
        assert "pmr" in content.lower(), "Expected PMR content in ref-advanced-patterns.md"
        idx = content.lower().find("pmr")
        window = content[max(0, idx - 200): idx + 600]
        assert "C++17" in window or "★ C++17" in window, (
            "PMR section must have ★ C++17 callout"
        )

    def test_span_has_cpp20_callout(self):
        content = ADV_PATTERNS.read_text(encoding="utf-8")
        assert "std::span" in content, "Expected std::span in ref-advanced-patterns.md"
        idx = content.find("std::span")
        window = content[max(0, idx - 200): idx + 600]
        assert "C++20" in window or "★ C++20" in window, (
            "std::span section must have ★ C++20 callout"
        )


class TestD4MemoryLifetime:
    """D4c: ref-safety-memory-lifetime.md must annotate std::pmr."""

    def test_pmr_has_cpp17_callout(self):
        content = MEM_LIFETIME.read_text(encoding="utf-8")
        assert "pmr" in content.lower(), "Expected std::pmr in ref-safety-memory-lifetime.md"
        idx = content.lower().find("pmr")
        window = content[max(0, idx - 200): idx + 600]
        assert "C++17" in window or "★ C++17" in window, (
            "std::pmr section must have ★ C++17 callout"
        )


class TestD4TemplatesMetaprogramming:
    """D4d: ref-templates-metaprogramming.md must annotate Concepts vs SFINAE."""

    def test_concepts_has_cpp20_callout(self):
        content = TEMPLATES.read_text(encoding="utf-8")
        assert "concept" in content.lower(), "Expected Concepts content"
        idx = content.lower().find("concept")
        window = content[max(0, idx - 200): idx + 600]
        assert "C++20" in window or "★ C++20" in window, (
            "Concepts section must have ★ C++20 callout"
        )

    def test_sfinae_has_cpp11_callout(self):
        content = TEMPLATES.read_text(encoding="utf-8")
        assert "sfinae" in content.lower() or "enable_if" in content.lower(), (
            "Expected SFINAE or enable_if content in templates ref"
        )
        lower = content.lower()
        idx = lower.find("sfinae") if "sfinae" in lower else lower.find("enable_if")
        window = content[max(0, idx - 200): idx + 600]
        assert "C++11" in window or "★ C++11" in window, (
            "SFINAE/enable_if section must have ★ C++11 callout"
        )
