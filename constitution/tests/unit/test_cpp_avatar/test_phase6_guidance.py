"""Phase 6 tests: Advanced C++20+ governance guidance sections.

Scenario IDs: c-plus-plus-avatar-enrichment/6.12–6.16
Law: ENG-6.1, ENG-3.1, ENG-6.7, ENG-2.2, ENG-5.1
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
GUIDANCE_PATH = REPO_ROOT / "avatars" / "technology" / "cpp" / "guidance.md"
CPP_DIR = REPO_ROOT / "avatars" / "technology" / "cpp"


def _guidance():
    return "\n".join(p.read_text(encoding="utf-8") for p in sorted(CPP_DIR.rglob("ref-*.md")))


class TestExceptionSafetyGuidance:
    """6.12: Exception safety & error handling governance."""

    def test_section_exists(self):
        assert "Exception Safety" in _guidance()

    def test_covers_guarantee_levels(self):
        content = _guidance()
        assert "nothrow" in content.lower() or "no-throw" in content.lower()
        assert "strong guarantee" in content.lower() or "strong exception" in content.lower()

    def test_covers_noexcept(self):
        assert "noexcept" in _guidance()

    def test_covers_expected_or_error_codes(self):
        content = _guidance()
        assert "std::expected" in content or "error code" in content.lower()


class TestCoroutinesGuidance:
    """6.13: Coroutines governance."""

    def test_section_exists(self):
        assert "Coroutines" in _guidance() or "coroutine" in _guidance()

    def test_covers_co_await(self):
        assert "co_await" in _guidance() or "co_yield" in _guidance()

    def test_covers_cancellation(self):
        content = _guidance().lower()
        assert "cancellation" in content or "cancel" in content


class TestLoggingGuidance:
    """6.14: Structured logging & diagnostics governance."""

    def test_section_exists(self):
        assert "Logging" in _guidance() or "Diagnostics" in _guidance()

    def test_covers_spdlog(self):
        assert "spdlog" in _guidance()

    def test_covers_pii_redaction(self):
        content = _guidance().lower()
        assert "pii" in content and ("redact" in content or "mask" in content)

    def test_covers_log_levels(self):
        content = _guidance()
        assert "INFO" in content or "WARN" in content or "ERROR" in content


class TestModulesGuidance:
    """6.15: C++20 modules governance."""

    def test_section_exists(self):
        content = _guidance()
        assert "Modules" in content or "module" in content

    def test_covers_import_export(self):
        content = _guidance()
        assert "import" in content and ("export" in content or "module" in content.lower())

    def test_covers_cmake_modules(self):
        content = _guidance().lower()
        assert "cmake" in content and "module" in content


class TestAllocatorGuidance:
    """6.16: Allocator governance."""

    def test_section_exists(self):
        content = _guidance().lower()
        assert "allocator" in content

    def test_covers_pmr(self):
        content = _guidance()
        assert "pmr" in content.lower() or "polymorphic_allocator" in content

    def test_covers_arena(self):
        content = _guidance().lower()
        assert "arena" in content or "monotonic" in content or "pool" in content
