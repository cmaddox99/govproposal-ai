"""
Phase 2D — E2: Mixed-repo detection edge case tests.

Per PHASE2-PROPOSAL.md (Owen Bradley / panel advisory), the version detection
logic has two untested edge cases:

1. CMakeLists.txt and *.dsp BOTH exist — detection order should pick
   CMakeLists.txt (modern build system wins), NOT treat the project as legacy
   because *.dsp is present.

2. *.props file exists but NO root *.vcxproj — a nested project scenario where
   a .props file is shared across multiple sub-projects. The avatar must not
   classify this as a legacy MSVC project when the root has no *.vcxproj.

These tests simulate the tier-detection logic described in guidance.md.
"""

import pathlib
import tempfile
import shutil
import pytest


# ── Detection logic mirroring guidance.md ──────────────────────────────────

DETECTION_ORDER = [
    # (file_glob_pattern, tier, description)
    ("CMakeLists.txt",          "transitional",   "CMake build system"),
    ("*.vcxproj",               "transitional",   "MSVC project (root-level vcxproj)"),
    ("Makefile",                "transitional",   "GNU Make"),
    ("meson.build",             "transitional",   "Meson build system"),
    ("*.dsp",                   "legacy",         "VC6 / Visual Studio legacy project"),
    ("*.props",                 "transitional",   "MSVC property sheet (sub-project)"),
]


def _detect_tier(root: pathlib.Path) -> tuple[str, str]:
    """
    Detect tier from project root using DETECTION_ORDER priority.
    Returns (tier, description) for the FIRST matching rule.
    """
    for pattern, tier, description in DETECTION_ORDER:
        if pattern.startswith("*"):
            # Glob match at root level only
            matches = list(root.glob(pattern))
        else:
            matches = [root / pattern] if (root / pattern).exists() else []
        if matches:
            return tier, description
    return "unknown", "No build system detected"


class TestMixedRepoCmakeWinsOverDsp:
    """
    When CMakeLists.txt AND *.dsp both exist, CMakeLists.txt wins.
    This ensures a project that migrated its build system away from VC6 is
    not treated as legacy just because the .dsp file wasn't deleted.
    """

    def setup_method(self):
        self.tmpdir = pathlib.Path(tempfile.mkdtemp())

    def teardown_method(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_detection_order_cmake_wins_over_dsp_in_mixed_repo(self):
        # Simulate: both build files present
        (self.tmpdir / "CMakeLists.txt").write_text("cmake_minimum_required(VERSION 3.14)\n")
        (self.tmpdir / "legacy_project.dsp").write_text(
            "# Microsoft Developer Studio Project File\n"
        )
        tier, description = _detect_tier(self.tmpdir)
        assert tier == "transitional", (
            f"CMakeLists.txt must win over .dsp; got tier='{tier}' ({description})"
        )
        assert "CMake" in description or "cmake" in description.lower() or "CMakeLists" in description, (
            f"Detection description should mention CMake, got: {description}"
        )

    def test_cmake_alone_is_transitional(self):
        (self.tmpdir / "CMakeLists.txt").write_text("cmake_minimum_required(VERSION 3.20)\n")
        tier, _ = _detect_tier(self.tmpdir)
        assert tier == "transitional"

    def test_dsp_alone_is_legacy(self):
        (self.tmpdir / "myapp.dsp").write_text("# Visual Studio legacy\n")
        tier, _ = _detect_tier(self.tmpdir)
        assert tier == "legacy"

    def test_cmake_wins_over_dsp_regardless_of_filesystem_order(self):
        """Alphabetical file-system order must not override DETECTION_ORDER priority."""
        # 'C' < 'l' in ASCII so CMakeLists.txt sorts before legacy.dsp
        # but confirm even with 'z_project.dsp' we still detect correctly
        (self.tmpdir / "CMakeLists.txt").write_text("")
        (self.tmpdir / "z_project.dsp").write_text("")
        tier, _ = _detect_tier(self.tmpdir)
        assert tier == "transitional", "Detection order, not filename order, must win"


class TestPropsFileNestedProjectScenario:
    """
    *.props exists but no root *.vcxproj — nested sub-project scenario.
    The avatar must not classify the repo as a root MSVC legacy project;
    instead, .props without a root .vcxproj triggers the props rule.
    """

    def setup_method(self):
        self.tmpdir = pathlib.Path(tempfile.mkdtemp())

    def teardown_method(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_props_without_vcxproj_is_not_legacy(self):
        (self.tmpdir / "shared.props").write_text(
            "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
        )
        # No *.vcxproj at root
        tier, description = _detect_tier(self.tmpdir)
        assert tier != "legacy", (
            "A .props file without a root .vcxproj must not classify as legacy"
        )

    def test_props_file_triggers_vcxproj_tier(self):
        """Without a root .vcxproj, .props alone routes to transitional via props rule."""
        (self.tmpdir / "shared.props").write_text("")
        tier, _ = _detect_tier(self.tmpdir)
        assert tier == "transitional", (
            ".props file alone (no .vcxproj) should map to transitional, not legacy"
        )

    def test_vcxproj_plus_props_is_transitional(self):
        (self.tmpdir / "MyApp.vcxproj").write_text("")
        (self.tmpdir / "shared.props").write_text("")
        tier, _ = _detect_tier(self.tmpdir)
        assert tier == "transitional"

    def test_no_build_files_is_unknown(self):
        # Empty directory — no build artifacts
        tier, description = _detect_tier(self.tmpdir)
        assert tier == "unknown", (
            "Empty repo with no build files must return 'unknown' tier"
        )
        assert "No build" in description or "unknown" in description.lower()


class TestDetectionOrderPriorityRules:
    """Verify the DETECTION_ORDER contract covers all expected patterns."""

    def test_detection_order_has_cmake_first(self):
        assert DETECTION_ORDER[0][0] == "CMakeLists.txt", (
            "CMakeLists.txt must be first in DETECTION_ORDER"
        )

    def test_detection_order_dsp_after_vcxproj(self):
        patterns = [p for p, _, _ in DETECTION_ORDER]
        dsp_idx   = patterns.index("*.dsp")
        vcxproj_idx = patterns.index("*.vcxproj")
        assert vcxproj_idx < dsp_idx, (
            "*.vcxproj (modern MSVC) must be detected before *.dsp (legacy VC6)"
        )

    def test_detection_order_cmake_before_dsp(self):
        patterns = [p for p, _, _ in DETECTION_ORDER]
        assert patterns.index("CMakeLists.txt") < patterns.index("*.dsp")
