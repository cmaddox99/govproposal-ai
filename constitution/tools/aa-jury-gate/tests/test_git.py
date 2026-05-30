"""Tests for git_probe.py and checks/git.py (G01).

Laws: ENG-4.1 (TDD), ENG-4.6 (coverage ≥ 90%), ENG-4.11 (mutation ≥ 85%),
      ENG-2.5 (dependency inversion via GitProbe Protocol)
Phase 3 §1.6 allow-no-git matrix; Phase 4 §2.3 GitProbe design; Phase 4 §5.2 exception hierarchy.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from aa_jury_gate.checks.git import check_g01
from aa_jury_gate.git_probe import RealGitProbe, StubGitProbe
from aa_jury_gate.models import (
    CheckResult,
    GitBinaryNotFoundError,
    GitNotInRepoError,
    GitProbeError,
    GitStatus,
)


# ── StubGitProbe unit tests ───────────────────────────────────────────────────

class TestStubGitProbe:
    def test_returns_clean_status(self, tmp_path: Path) -> None:
        stub = StubGitProbe(status=GitStatus.CLEAN)
        assert stub.check(tmp_path / "file.md") == GitStatus.CLEAN

    def test_returns_untracked_status(self, tmp_path: Path) -> None:
        stub = StubGitProbe(status=GitStatus.UNTRACKED)
        assert stub.check(tmp_path / "file.md") == GitStatus.UNTRACKED

    def test_raises_git_not_in_repo_error(self, tmp_path: Path) -> None:
        stub = StubGitProbe(raises=GitNotInRepoError("not a git repository"))
        with pytest.raises(GitNotInRepoError):
            stub.check(tmp_path / "file.md")

    def test_raises_git_probe_error(self, tmp_path: Path) -> None:
        stub = StubGitProbe(raises=GitProbeError("not a git repository"))
        with pytest.raises(GitProbeError):
            stub.check(tmp_path / "file.md")

    def test_raises_git_binary_not_found(self, tmp_path: Path) -> None:
        stub = StubGitProbe(raises=GitBinaryNotFoundError("git not in PATH"))
        with pytest.raises(GitBinaryNotFoundError):
            stub.check(tmp_path / "file.md")


# ── RealGitProbe unit tests ───────────────────────────────────────────────────

class TestRealGitProbe:
    def test_git_binary_absent_raises(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """RealGitProbe raises GitBinaryNotFoundError when git not in PATH."""
        original_run = subprocess.run

        def fake_run(args, **kwargs):  # type: ignore[override]
            if args[0] == "git":
                raise FileNotFoundError("git not found")
            return original_run(args, **kwargs)

        monkeypatch.setattr(subprocess, "run", fake_run)
        probe = RealGitProbe()
        with pytest.raises(GitBinaryNotFoundError) as exc:
            probe.check(tmp_path / "file.md")
        assert str(exc.value) == "git binary not found in PATH"

    def test_path_not_in_git_repo_raises(self, tmp_path: Path) -> None:
        """RealGitProbe raises GitNotInRepoError when path is not in a git repo."""
        probe = RealGitProbe()
        isolated = tmp_path / "not_a_repo"
        isolated.mkdir()
        (isolated / "test.md").write_text("content")
        with pytest.raises(GitNotInRepoError) as exc:
            probe.check(isolated / "test.md")
        assert str(exc.value).startswith("not a git repository")

    def test_clean_file_returns_clean(self, tmp_path: Path) -> None:
        """RealGitProbe returns CLEAN for a committed, unmodified file."""
        # Set up a real git repo
        subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@test.com"],
            check=True, capture_output=True, cwd=tmp_path,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"],
            check=True, capture_output=True, cwd=tmp_path,
        )
        synthesis = tmp_path / "synthesis.md"
        synthesis.write_text("---\nverdict: APPROVED\n---\n\n## R1\n\n## R2\n\n## Synthesis\n")
        subprocess.run(
            ["git", "add", str(synthesis)],
            check=True, capture_output=True, cwd=tmp_path,
        )
        subprocess.run(
            ["git", "commit", "-m", "add synthesis"],
            check=True, capture_output=True, cwd=tmp_path,
        )
        probe = RealGitProbe()
        assert probe.check(synthesis) == GitStatus.CLEAN

    def test_untracked_file_raises(self, tmp_path: Path) -> None:
        """RealGitProbe raises GitProbeError when file is untracked."""
        subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@test.com"],
            check=True, capture_output=True, cwd=tmp_path,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"],
            check=True, capture_output=True, cwd=tmp_path,
        )
        # Create an initial commit so HEAD exists
        init_file = tmp_path / "init.txt"
        init_file.write_text("init")
        subprocess.run(["git", "add", str(init_file)], check=True, capture_output=True, cwd=tmp_path)  # noqa: E501
        subprocess.run(
            ["git", "commit", "-m", "init"],
            check=True, capture_output=True, cwd=tmp_path,
        )
        untracked = tmp_path / "untracked.md"
        untracked.write_text("not tracked")
        probe = RealGitProbe()
        with pytest.raises(GitProbeError) as exc:
            probe.check(untracked)
        assert str(exc.value).startswith("synthesis file not tracked by git")

    def test_uncommitted_file_raises(self, tmp_path: Path) -> None:
        """RealGitProbe raises GitProbeError when file has uncommitted changes."""
        subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@test.com"],
            check=True, capture_output=True, cwd=tmp_path,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"],
            check=True, capture_output=True, cwd=tmp_path,
        )
        synthesis = tmp_path / "synthesis.md"
        synthesis.write_text("---\nverdict: APPROVED\n---\n\n## Synthesis\n")
        subprocess.run(
            ["git", "add", str(synthesis)],
            check=True, capture_output=True, cwd=tmp_path,
        )
        subprocess.run(
            ["git", "commit", "-m", "add synthesis"],
            check=True, capture_output=True, cwd=tmp_path,
        )
        # Modify the file without committing
        synthesis.write_text("---\nverdict: APPROVED\n---\n\n## Synthesis\nmodified\n")
        probe = RealGitProbe()
        with pytest.raises(GitProbeError) as exc:
            probe.check(synthesis)
        assert str(exc.value).startswith("synthesis file has uncommitted changes")

    def test_parent_dir_not_exist_raises(self, tmp_path: Path) -> None:
        """RealGitProbe raises GitProbeError when path.parent does not exist."""
        probe = RealGitProbe()
        with pytest.raises(GitProbeError) as exc:
            probe.check(tmp_path / "nonexistent_dir" / "file.md")
        assert str(exc.value).startswith("parent directory does not exist")

    def test_empty_repo_no_commits_raises(self, tmp_path: Path) -> None:
        """RealGitProbe raises GitProbeError for a repo with no commits (no HEAD).

        The exact message depends on git version:
        - git ≥2.30: ls-files --error-unmatch passes for staged files → diff HEAD fails
          → "git diff failed (possibly no HEAD commit)"
        - older git: ls-files may exit non-zero for staged-only files
          → "synthesis file not tracked by git"
        Both paths correctly raise GitProbeError (never CLEAN).
        """
        subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@test.com"],
            check=True, capture_output=True, cwd=tmp_path,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"],
            check=True, capture_output=True, cwd=tmp_path,
        )
        synthesis = tmp_path / "synthesis.md"
        synthesis.write_text("content")
        subprocess.run(
            ["git", "add", str(synthesis)],
            check=True, capture_output=True, cwd=tmp_path,
        )
        # Staged but not committed — no HEAD exists
        probe = RealGitProbe()
        # ls-files --error-unmatch passes (file is staged/tracked)
        # git diff HEAD fails (no HEAD) → GitProbeError
        with pytest.raises(GitProbeError) as exc:
            probe.check(synthesis)
        msg = str(exc.value)
        assert msg.startswith("git diff failed") or msg.startswith("synthesis file not tracked")


# ── check_g01 unit tests (all via StubGitProbe) ──────────────────────────────

class TestCheckG01:
    def test_pass_clean_file(self, tmp_path: Path) -> None:
        stub = StubGitProbe(status=GitStatus.CLEAN)
        item = check_g01(stub, tmp_path / "s.md", allow_no_git=False)
        assert item.result == CheckResult.PASS
        assert item.check_id == "G01"
        assert item.detail == ""

    def test_fail_outside_repo_no_allow(self, tmp_path: Path) -> None:
        """allow_no_git=False + outside repo (GitNotInRepoError) → FAIL."""
        stub = StubGitProbe(raises=GitNotInRepoError("not a git repository"))
        item = check_g01(stub, tmp_path / "s.md", allow_no_git=False)
        assert item.result == CheckResult.FAIL
        assert item.check_id == "G01"
        assert "not a git repository" in item.detail

    def test_skip_no_git_binary_with_allow(self, tmp_path: Path) -> None:
        """allow_no_git=True + no git binary (GitBinaryNotFoundError) → SKIP."""
        stub = StubGitProbe(raises=GitBinaryNotFoundError("git not in PATH"))
        item = check_g01(stub, tmp_path / "s.md", allow_no_git=True)
        assert item.result == CheckResult.SKIP
        assert item.check_id == "G01"
        assert item.detail == ""

    def test_skip_outside_repo_with_allow(self, tmp_path: Path) -> None:
        """allow_no_git=True + not in repo (GitNotInRepoError) → SKIP (Phase 3 §1.6)."""
        stub = StubGitProbe(raises=GitNotInRepoError("not a git repository"))
        item = check_g01(stub, tmp_path / "s.md", allow_no_git=True)
        assert item.result == CheckResult.SKIP
        assert item.check_id == "G01"
        assert item.detail == ""

    def test_pass_inside_repo_with_allow(self, tmp_path: Path) -> None:
        """allow_no_git=True + inside repo, clean file → PASS (BDD-F06)."""
        stub = StubGitProbe(status=GitStatus.CLEAN)
        item = check_g01(stub, tmp_path / "s.md", allow_no_git=True)
        assert item.result == CheckResult.PASS

    def test_reraise_no_git_binary_no_allow(self, tmp_path: Path) -> None:
        """allow_no_git=False + no git binary → re-raise GitBinaryNotFoundError (exit 2)."""
        stub = StubGitProbe(raises=GitBinaryNotFoundError("git not in PATH"))
        with pytest.raises(GitBinaryNotFoundError):
            check_g01(stub, tmp_path / "s.md", allow_no_git=False)

    def test_fail_untracked_file(self, tmp_path: Path) -> None:
        stub = StubGitProbe(raises=GitProbeError("synthesis file not tracked by git"))
        item = check_g01(stub, tmp_path / "s.md", allow_no_git=False)
        assert item.result == CheckResult.FAIL
        assert item.detail.startswith("synthesis file not tracked by git")

    def test_fail_uncommitted_changes(self, tmp_path: Path) -> None:
        stub = StubGitProbe(raises=GitProbeError("synthesis file has uncommitted changes"))
        item = check_g01(stub, tmp_path / "s.md", allow_no_git=False)
        assert item.result == CheckResult.FAIL
        assert item.detail.startswith("synthesis file has uncommitted changes")

    def test_fail_untracked_even_with_allow_no_git(self, tmp_path: Path) -> None:
        """allow_no_git=True does NOT mask untracked files — Phase 3 §1.6 MUST FAIL."""
        stub = StubGitProbe(raises=GitProbeError("synthesis file not tracked by git"))
        item = check_g01(stub, tmp_path / "s.md", allow_no_git=True)
        assert item.result == CheckResult.FAIL
        assert item.check_id == "G01"

    def test_fail_uncommitted_even_with_allow_no_git(self, tmp_path: Path) -> None:
        """allow_no_git=True does NOT mask uncommitted changes — Phase 3 §1.6 MUST FAIL."""
        stub = StubGitProbe(raises=GitProbeError("synthesis file has uncommitted changes"))
        item = check_g01(stub, tmp_path / "s.md", allow_no_git=True)
        assert item.result == CheckResult.FAIL
        assert item.check_id == "G01"

    def test_fail_status_untracked_direct(self, tmp_path: Path) -> None:
        # GitStatus.UNTRACKED returned directly (not raised) — e.g. from extended stub
        stub = StubGitProbe(status=GitStatus.UNTRACKED)
        item = check_g01(stub, tmp_path / "s.md", allow_no_git=False)
        assert item.result == CheckResult.FAIL
        assert item.check_id == "G01"
        assert item.detail == "synthesis file not tracked by git"

    def test_fail_status_uncommitted_direct(self, tmp_path: Path) -> None:
        from aa_jury_gate.models import GitStatus as GS
        stub = StubGitProbe(status=GS.UNCOMMITTED)
        item = check_g01(stub, tmp_path / "s.md", allow_no_git=False)
        assert item.result == CheckResult.FAIL
        assert item.check_id == "G01"
        assert item.detail == "synthesis file has uncommitted changes"
