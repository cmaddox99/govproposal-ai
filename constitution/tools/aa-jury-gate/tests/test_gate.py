"""Tests for GateRunner orchestration."""

import pytest

from aa_jury_gate.gate import GateRunner, _compute_sha256
from aa_jury_gate.git_probe import StubGitProbe
from aa_jury_gate.models import CheckResult, GateVerdict, GitStatus


class TestGateRunner:
    """Test GateRunner check orchestration."""

    def test_valid_synthesis_pass(self, synthesis_factory, tmp_path):
        """Test valid APPROVED synthesis in git repo → PASS verdict."""
        path = synthesis_factory()
        stub_probe = StubGitProbe(GitStatus.CLEAN)
        runner = GateRunner(git_probe=stub_probe)

        result = runner.run(path, allow_no_git=False)

        assert result.verdict == GateVerdict.PASS
        assert len(result.checks) == 16  # S01-S11 (S08a+S08b) + B01-B03 + G01
        assert all(c.result in (CheckResult.PASS, CheckResult.SKIP) for c in result.checks)

        # Body checks must be PASS (not SKIP) on valid synthesis
        for check_id in ["B01", "B02", "B03"]:
            c = next(check for check in result.checks if check.check_id == check_id)
            assert c.result == CheckResult.PASS

        assert result.content_sha256 == _compute_sha256(path.read_text())

    def test_schema_fail_s05(self, synthesis_factory, tmp_path):
        """Test invalid synthesis (S06 juror_count/jurors mismatch) → FAIL verdict."""
        path = synthesis_factory(juror_count=5)  # Creates 5 jurors
        # Manually edit to break juror_count
        content = path.read_text()
        content = content.replace("juror_count: 5", "juror_count: 3")
        path.write_text(content)

        stub_probe = StubGitProbe(GitStatus.CLEAN)
        runner = GateRunner(git_probe=stub_probe)

        result = runner.run(path, allow_no_git=False)

        assert result.verdict == GateVerdict.FAIL
        s06 = next(c for c in result.checks if c.check_id == "S06")
        assert s06.result == CheckResult.FAIL
        assert "juror_count is 3; expected 5" in s06.detail

    def test_schema_fast_fail_s01(self, tmp_path):
        """Test S01-S04 fast-fail: stops at first FAIL."""
        path = tmp_path / "nonexistent.md"
        # File does not exist — S01 should FAIL

        stub_probe = StubGitProbe(GitStatus.CLEAN)
        runner = GateRunner(git_probe=stub_probe)

        result = runner.run(path, allow_no_git=False)

        assert result.verdict == GateVerdict.FAIL
        # Should have S01 only (fast-fail)
        assert len(result.checks) == 1
        assert result.checks[0].check_id == "S01"
        assert result.checks[0].result == CheckResult.FAIL

    def test_unreadable_file_error(self, tmp_path):
        """Test file exists but is a directory → S01 FAIL."""
        path = tmp_path  # tmp_path is a directory, not a file

        stub_probe = StubGitProbe(GitStatus.CLEAN)
        runner = GateRunner(git_probe=stub_probe)

        result = runner.run(path, allow_no_git=False)

        assert result.verdict == GateVerdict.FAIL
        assert len(result.checks) == 1
        assert result.checks[0].check_id == "S01"
        assert result.checks[0].result == CheckResult.FAIL
        assert "directory" in result.checks[0].detail

    def test_s11_fail_skips_body_checks(self, synthesis_factory, tmp_path):
        """Test S11 FAIL → B01-B03 all SKIP (BDD scenario 11)."""
        path = synthesis_factory(verdict="INVALID")  # Bad verdict → S11 FAIL
        stub_probe = StubGitProbe(GitStatus.CLEAN)
        runner = GateRunner(git_probe=stub_probe)

        result = runner.run(path, allow_no_git=False)

        assert result.verdict == GateVerdict.FAIL
        s11 = next(c for c in result.checks if c.check_id == "S11")
        assert s11.result == CheckResult.FAIL

        # B01-B03 should all be SKIP
        for check_id in ["B01", "B02", "B03"]:
            c = next(check for check in result.checks if check.check_id == check_id)
            assert c.result == CheckResult.SKIP
            assert c.detail == "S11 FAIL"

    def test_git_probe_error_allow_no_git_false(self, synthesis_factory, tmp_path):
        """Test GitBinaryNotFoundError with allow_no_git=False → raises ToolError."""
        from aa_jury_gate.models import GitBinaryNotFoundError

        path = synthesis_factory()

        # Stub that raises GitBinaryNotFoundError
        class ErrorProbe:
            def check(self, path):
                raise GitBinaryNotFoundError("git not found")

        runner = GateRunner(git_probe=ErrorProbe())

        with pytest.raises(GitBinaryNotFoundError):
            runner.run(path, allow_no_git=False)

    def test_git_probe_skip_allow_no_git_true(self, synthesis_factory, tmp_path):
        """Test GitNotInRepoError with allow_no_git=True → G01 SKIP."""
        from aa_jury_gate.models import GitNotInRepoError

        path = synthesis_factory()

        # Stub that raises GitNotInRepoError (infrastructure error)
        class SkipProbe:
            def check(self, path):
                raise GitNotInRepoError("not in repo")

        runner = GateRunner(git_probe=SkipProbe())

        result = runner.run(path, allow_no_git=True)

        g01 = next(c for c in result.checks if c.check_id == "G01")
        assert g01.result == CheckResult.SKIP
        assert result.verdict == GateVerdict.PASS  # No FAILs

    def test_content_sha256_computed(self, synthesis_factory, tmp_path):
        """Test content_sha256 matches file content."""
        path = synthesis_factory()
        content = path.read_text()
        expected_sha = _compute_sha256(content)

        stub_probe = StubGitProbe(GitStatus.CLEAN)
        runner = GateRunner(git_probe=stub_probe)

        result = runner.run(path, allow_no_git=False)

        assert result.content_sha256 == expected_sha

    def test_body_checks_run_when_s11_pass_despite_other_fail(self, synthesis_factory):
        """Test B01-B03 run when S11 PASS even if other checks fail (kills mutation 407).

        Mutation 407: line 113 `and` → `or` in s11_failed logic.
        With `or`, s11_failed is always True (S11 always in checks list), so B01-B03 always SKIP.
        This test ensures B01-B03 run when S11 PASS, even if S06 FAIL (juror_count mismatch).
        """
        # Create synthesis with juror_count=3 but 5 jurors → S06 will FAIL
        # But verdict=APPROVED → S11 will PASS
        path = synthesis_factory(juror_count=3)

        stub_probe = StubGitProbe(GitStatus.CLEAN)
        runner = GateRunner(git_probe=stub_probe)
        result = runner.run(path, allow_no_git=False)

        # Gate should FAIL due to S06
        assert result.verdict == GateVerdict.FAIL

        # S06 should FAIL (juror_count mismatch)
        s06 = next(c for c in result.checks if c.check_id == "S06")
        assert s06.result == CheckResult.FAIL

        # S11 should PASS (verdict is APPROVED)
        s11 = next(c for c in result.checks if c.check_id == "S11")
        assert s11.result == CheckResult.PASS

        # Body checks should RUN and PASS (not SKIP) because S11 passed
        for check_id in ["B01", "B02", "B03"]:
            c = next(check for check in result.checks if check.check_id == check_id)
            assert c.result == CheckResult.PASS, f"{check_id} should PASS, not SKIP (mutation 407)"


def test_compute_sha256():
    """Test SHA256 computation (ADR-002 formula)."""
    content = "test content\n"
    expected = "a1fff0ffefb9eace7230c24e50731f0a91c62f9cefdfe77121c2f607125dffae"
    assert _compute_sha256(content) == expected
