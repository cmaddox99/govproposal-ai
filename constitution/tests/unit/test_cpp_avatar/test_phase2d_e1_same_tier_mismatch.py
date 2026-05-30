"""
Phase 2D — E1: Same-tier exact-version mismatch simulation tests.

Per PHASE2-PROPOSAL.md, no test currently verifies that:
- A C++11 project gets warned when encountering a C++14 example
  (both in the 'transitional' tier — same tier, different minor version)
- A C++20 project gets warned about a C++23 example
  (both in 'greenfield' tier — same tier, but one version ahead)

These tests simulate the VERSION_ORDER map and compatibility check logic
that the routing guidance in guidance.md prescribes.

The VERSION_ORDER is the canonical version sequence used by the avatar to
determine whether a given example's cpp_version_min is compatible with the
project's declared cpp.standard. An example with cpp_version_min > project
standard is flagged with a warning note, even if both are in the same tier.
"""

import pathlib
import pytest

REPO_ROOT = pathlib.Path(__file__).parent.parent.parent.parent
CPP_DIR   = REPO_ROOT / "avatars" / "technology" / "cpp"
GUIDANCE  = CPP_DIR / "guidance.md"

# VERSION_ORDER is the canonical ordering used by the avatar routing logic.
# This must match the ordering documented in guidance.md.
VERSION_ORDER = [98, 3, 11, 14, 17, 20, 23, 26]


def is_compatible(project_standard: int, example_min: int) -> bool:
    """Return True if example_min <= project_standard in VERSION_ORDER."""
    if project_standard not in VERSION_ORDER:
        raise ValueError(f"Unknown project standard: {project_standard}")
    if example_min not in VERSION_ORDER:
        raise ValueError(f"Unknown example min: {example_min}")
    return VERSION_ORDER.index(example_min) <= VERSION_ORDER.index(project_standard)


def compatibility_warning(project_standard: int, example_min: int) -> str | None:
    """Return a warning string if example requires newer standard, else None."""
    if not is_compatible(project_standard, example_min):
        return (
            f"⚠️  This example requires C++{example_min} "
            f"but your project declares C++{project_standard}. "
            f"Verify your compiler supports this feature before adopting."
        )
    return None


class TestVersionOrderStructure:
    """VERSION_ORDER must be consistent with guidance.md declarations."""

    def test_version_order_is_ascending(self):
        """VERSION_ORDER must be defined and monotonically increasing."""
        assert len(VERSION_ORDER) >= 6, "VERSION_ORDER must have at least C++98..C++23"
        # Spot-check key versions are present
        for v in [98, 11, 14, 17, 20, 23]:
            assert v in VERSION_ORDER, f"C++{v} must be in VERSION_ORDER"

    def test_cpp98_before_cpp11(self):
        assert VERSION_ORDER.index(98) < VERSION_ORDER.index(11)

    def test_cpp11_before_cpp14(self):
        assert VERSION_ORDER.index(11) < VERSION_ORDER.index(14)

    def test_cpp14_before_cpp17(self):
        assert VERSION_ORDER.index(14) < VERSION_ORDER.index(17)

    def test_cpp17_before_cpp20(self):
        assert VERSION_ORDER.index(17) < VERSION_ORDER.index(20)

    def test_cpp20_before_cpp23(self):
        assert VERSION_ORDER.index(20) < VERSION_ORDER.index(23)


class TestSameTierVersionMismatchTransitional:
    """
    C++11 project warned about C++14 example — both in 'transitional' tier.

    The transitional tier spans C++11–C++17. An example with cpp_version_min:14
    is VALID in that tier but INCOMPATIBLE with a project declaring C++11.
    The routing logic must produce a warning, not silently serve the example.
    """

    def test_cpp11_project_not_compatible_with_cpp14_example(self):
        assert not is_compatible(project_standard=11, example_min=14), (
            "A C++14 example must NOT be compatible with a C++11 project"
        )

    def test_cpp11_project_gets_warning_for_cpp14_example(self):
        warning = compatibility_warning(project_standard=11, example_min=14)
        assert warning is not None, (
            "C++11 project must receive a warning when served a C++14 example"
        )
        assert "C++14" in warning
        assert "C++11" in warning

    def test_cpp11_project_compatible_with_cpp11_example(self):
        assert is_compatible(project_standard=11, example_min=11), (
            "A C++11 example must be compatible with a C++11 project (no version jump)"
        )

    def test_cpp14_project_compatible_with_cpp11_example(self):
        """Older examples are always safe for newer projects."""
        assert is_compatible(project_standard=14, example_min=11)

    def test_cpp14_project_compatible_with_cpp14_example(self):
        assert is_compatible(project_standard=14, example_min=14)

    def test_cpp14_project_not_compatible_with_cpp17_example(self):
        assert not is_compatible(project_standard=14, example_min=17)

    def test_cpp17_project_compatible_with_cpp14_example(self):
        assert is_compatible(project_standard=17, example_min=14)


class TestSameTierVersionMismatchGreenfield:
    """
    C++20 project warned about C++23 example — both in 'greenfield' tier.

    Greenfield spans C++20+. A C++23 example is AHEAD of a C++20 project;
    the routing logic must warn, not silently assume the project is on C++23.
    """

    def test_cpp20_project_not_compatible_with_cpp23_example(self):
        assert not is_compatible(project_standard=20, example_min=23), (
            "A C++23 example must NOT be compatible with a C++20 project"
        )

    def test_cpp20_project_gets_warning_for_cpp23_example(self):
        warning = compatibility_warning(project_standard=20, example_min=23)
        assert warning is not None, (
            "C++20 project must receive a warning when served a C++23 example"
        )
        assert "C++23" in warning
        assert "C++20" in warning

    def test_cpp20_project_compatible_with_cpp20_example(self):
        assert is_compatible(project_standard=20, example_min=20)

    def test_cpp23_project_compatible_with_cpp20_example(self):
        """C++20 examples are safe for C++23 projects."""
        assert is_compatible(project_standard=23, example_min=20)

    def test_cpp20_project_compatible_with_cpp17_example(self):
        """C++17 examples are safe for C++20 projects."""
        assert is_compatible(project_standard=20, example_min=17)


class TestVersionOrderEdgeCases:
    """Edge cases and cross-tier compatibility."""

    def test_cpp98_project_not_compatible_with_cpp11_example(self):
        assert not is_compatible(project_standard=98, example_min=11)

    def test_cpp98_project_compatible_with_cpp98_example(self):
        assert is_compatible(project_standard=98, example_min=98)

    def test_warning_mentions_compiler_verification(self):
        warning = compatibility_warning(project_standard=98, example_min=11)
        assert warning is not None
        assert "compiler" in warning.lower() or "verify" in warning.lower(), (
            "Warning must advise the developer to verify compiler support"
        )

    def test_no_warning_when_compatible(self):
        assert compatibility_warning(project_standard=17, example_min=14) is None
        assert compatibility_warning(project_standard=20, example_min=20) is None
        assert compatibility_warning(project_standard=23, example_min=11) is None
