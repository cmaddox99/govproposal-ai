"""VS-04: Tests for security.py path validation (ENG-4.1, ENG-6.1)."""

from __future__ import annotations

from pathlib import Path

import pytest

from aa_jury_gate.models import ToolError
from aa_jury_gate.security import validate_log_dir, validate_synthesis_path


# ── validate_synthesis_path ───────────────────────────────────────────────────

class TestValidateSynthesisPath:
    def test_pass_valid_file(self, tmp_path: Path) -> None:
        f = tmp_path / "synthesis.md"
        f.write_text("content")
        result = validate_synthesis_path(f)
        assert result == f

    def test_returns_path(self, tmp_path: Path) -> None:
        f = tmp_path / "synthesis.md"
        f.write_text("x")
        assert isinstance(validate_synthesis_path(f), Path)

    def test_fail_not_exists(self, tmp_path: Path) -> None:
        missing = tmp_path / "missing.md"
        with pytest.raises(ToolError) as exc:
            validate_synthesis_path(missing)
        assert str(exc.value).startswith("synthesis file not found")

    def test_fail_is_directory(self, tmp_path: Path) -> None:
        d = tmp_path / "subdir"
        d.mkdir()
        with pytest.raises(ToolError) as exc:
            validate_synthesis_path(d)
        assert str(exc.value).startswith("synthesis path is a directory")

    def test_fail_is_symlink(self, tmp_path: Path) -> None:
        target = tmp_path / "real.md"
        target.write_text("real content")
        link = tmp_path / "link.md"
        link.symlink_to(target)
        with pytest.raises(ToolError) as exc:
            validate_synthesis_path(link)
        assert str(exc.value).startswith("synthesis path is a symlink")

    def test_symlink_checked_before_size(self, tmp_path: Path) -> None:
        # A symlink to a large file should fail with symlink error, not size error
        target = tmp_path / "large.md"
        target.write_bytes(b"x" * (1024 * 1024 + 1))
        link = tmp_path / "link.md"
        link.symlink_to(target)
        with pytest.raises(ToolError) as exc:
            validate_synthesis_path(link)
        assert str(exc.value).startswith("synthesis path is a symlink")

    def test_fail_too_large(self, tmp_path: Path) -> None:
        f = tmp_path / "big.md"
        f.write_bytes(b"x" * (1024 * 1024 + 1))  # 1MB + 1 byte
        with pytest.raises(ToolError) as exc:
            validate_synthesis_path(f)
        assert str(exc.value).startswith("synthesis file too large")

    def test_pass_exactly_1mb(self, tmp_path: Path) -> None:
        f = tmp_path / "boundary.md"
        f.write_bytes(b"x" * (1024 * 1024))  # exactly 1MB → PASS
        result = validate_synthesis_path(f)
        assert result == f

    def test_fail_not_exists_error_message(self, tmp_path: Path) -> None:
        missing = tmp_path / "no.md"
        with pytest.raises(ToolError) as exc:
            validate_synthesis_path(missing)
        assert str(exc.value).startswith("synthesis file not found")

    def test_fail_directory_error_message(self, tmp_path: Path) -> None:
        with pytest.raises(ToolError) as exc:
            validate_synthesis_path(tmp_path)
        assert str(exc.value).startswith("synthesis path is a directory")


# ── validate_log_dir ──────────────────────────────────────────────────────────

class TestValidateLogDir:
    def test_none_returns_default(self) -> None:
        result = validate_log_dir(None)
        assert isinstance(result, Path)
        assert result == Path("~/.aa-jury-gate/").expanduser()

    def test_none_does_not_raise(self) -> None:
        # Default path is never subject to CWD-boundary check
        result = validate_log_dir(None)
        assert result is not None

    def test_dot_slash_logs_passes(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = validate_log_dir("./logs")
        assert isinstance(result, Path)
        assert result.is_absolute()

    def test_relative_subdir_passes(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = validate_log_dir("logs")
        assert isinstance(result, Path)
        assert str(result).startswith(str(tmp_path))

    def test_traversal_raises(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        with pytest.raises(ToolError) as exc:
            validate_log_dir("../../etc")
        assert str(exc.value).startswith("--log-dir path escapes")

    def test_absolute_outside_cwd_raises(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        with pytest.raises(ToolError):
            validate_log_dir("/etc")

    def test_sibling_prefix_dir_raises(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # /tmp/work-evil should not pass when CWD is /tmp/work
        # (old startswith check was bypassable; relative_to() is not)
        monkeypatch.chdir(tmp_path)
        sibling = tmp_path.parent / (tmp_path.name + "-evil")
        sibling.mkdir(exist_ok=True)
        with pytest.raises(ToolError) as exc:
            validate_log_dir(str(sibling))
        assert str(exc.value).startswith("--log-dir path escapes")

    def test_accepts_string_input(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        # Click passes str, not Path — must accept str
        monkeypatch.chdir(tmp_path)
        result = validate_log_dir("./logs")
        assert isinstance(result, Path)

    def test_tilde_expansion(self) -> None:
        # Caller-supplied "~/logs" — expands ~ before realpath
        # This will resolve to something outside CWD in most envs → ToolError
        # unless CWD happens to be home. Just confirm it doesn't crash with AttributeError.
        try:
            validate_log_dir("~/logs")
        except ToolError:
            pass  # Expected — outside CWD

    def test_returns_absolute_path(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = validate_log_dir("./logs")
        assert result.is_absolute()

    def test_error_message_on_traversal(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        with pytest.raises(ToolError) as exc:
            validate_log_dir("../../etc")
        assert str(exc.value).startswith("--log-dir path escapes")
