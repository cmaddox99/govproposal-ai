"""Tests for output.py append_gate_result."""

import pytest
import yaml

from aa_jury_gate.models import CheckItem, CheckResult, GateResult, GateVerdict
from aa_jury_gate.output import append_gate_result


def test_append_pass_verdict(synthesis_factory, tmp_path):
    """Test PASS verdict writes jury_gate: block."""
    path = synthesis_factory()
    result = GateResult(
        verdict=GateVerdict.PASS,
        checks=[
            CheckItem(check_id="S01", result=CheckResult.PASS, detail=""),
        ],
        content_sha256="abc123",
    )

    append_gate_result(path, result)

    # Read and verify
    content = path.read_text()
    assert "jury_gate:" in content
    fm = yaml.safe_load(content.split("---\n", 1)[1].split("\n---\n")[0])
    assert fm["jury_gate"]["verdict"] == "PASS"
    assert fm["jury_gate"]["content_sha256"] == "abc123"
    assert len(fm["jury_gate"]["checks"]) == 1


def test_append_fail_verdict(synthesis_factory, tmp_path):
    """Test FAIL verdict writes jury_gate: block."""
    path = synthesis_factory()
    result = GateResult(
        verdict=GateVerdict.FAIL,
        checks=[
            CheckItem(check_id="S05", result=CheckResult.FAIL, detail="mismatch"),
        ],
        content_sha256="def456",
    )

    append_gate_result(path, result)

    content = path.read_text()
    fm = yaml.safe_load(content.split("---\n", 1)[1].split("\n---\n")[0])
    assert fm["jury_gate"]["verdict"] == "FAIL"
    assert fm["jury_gate"]["checks"][0]["result"] == "FAIL"
    assert fm["jury_gate"]["checks"][0]["detail"] == "mismatch"


def test_error_verdict_does_not_write(synthesis_factory, tmp_path):
    """Test ERROR verdict does NOT write (BDD-F05)."""
    path = synthesis_factory()
    original_content = path.read_text()

    result = GateResult(
        verdict=GateVerdict.ERROR,
        checks=[],
        content_sha256="",
    )

    append_gate_result(path, result)

    # File should be unchanged
    assert path.read_text() == original_content
    assert "jury_gate:" not in path.read_text()


def test_idempotent_overwrite(synthesis_factory, tmp_path):
    """Test writing twice replaces block (not duplicated), but timestamp changes."""
    path = synthesis_factory()
    result = GateResult(
        verdict=GateVerdict.PASS,
        checks=[CheckItem(check_id="S01", result=CheckResult.PASS, detail="")],
        content_sha256="abc123",
    )

    # Write first time
    append_gate_result(path, result)
    first_content = path.read_text()
    first_fm = yaml.safe_load(first_content.split("---\n", 2)[1])

    # Write second time with same result
    append_gate_result(path, result)
    second_content = path.read_text()
    second_fm = yaml.safe_load(second_content.split("---\n", 2)[1])

    # Should have exactly one jury_gate block (not duplicated)
    assert first_content.count("jury_gate:") == 1
    assert second_content.count("jury_gate:") == 1

    # Structure should be identical except timestamp_utc
    assert first_fm["jury_gate"]["verdict"] == second_fm["jury_gate"]["verdict"]
    assert first_fm["jury_gate"]["content_sha256"] == second_fm["jury_gate"]["content_sha256"]
    # timestamp_utc will be different between writes (that's OK)


def test_atomic_write_same_dir(synthesis_factory, tmp_path, monkeypatch):
    """Test atomic replace — temp file created in path.parent (BDD scenario 6)."""
    path = synthesis_factory()
    result = GateResult(
        verdict=GateVerdict.PASS,
        checks=[],
        content_sha256="xyz",
    )

    # Track mkstemp calls
    temp_dirs = []
    original_mkstemp = __import__("tempfile").mkstemp

    def tracked_mkstemp(dir=None, **kwargs):
        temp_dirs.append(dir)
        return original_mkstemp(dir=dir, **kwargs)

    monkeypatch.setattr("tempfile.mkstemp", tracked_mkstemp)

    append_gate_result(path, result)

    # Verify temp file was created in path.parent
    assert len(temp_dirs) == 1
    assert temp_dirs[0] == path.parent


def test_preserves_body_text(synthesis_factory, tmp_path):
    """Test body text is preserved after frontmatter update."""
    path = synthesis_factory(body="\n# Custom Body\n\nTest content here.\n")
    original_body = path.read_text().split("\n---\n", 1)[1]

    result = GateResult(
        verdict=GateVerdict.PASS,
        checks=[],
        content_sha256="test",
    )

    append_gate_result(path, result)

    new_body = path.read_text().split("\n---\n", 1)[1]
    assert new_body == original_body


def test_missing_frontmatter_raises(tmp_path):
    """Test file without frontmatter raises ValueError."""
    path = tmp_path / "bad.md"
    path.write_text("No frontmatter here")

    result = GateResult(verdict=GateVerdict.PASS, checks=[], content_sha256="x")

    with pytest.raises(ValueError, match="missing frontmatter delimiter"):
        append_gate_result(path, result)


def test_unclosed_frontmatter_raises(tmp_path):
    """Test file with unclosed frontmatter raises ValueError."""
    path = tmp_path / "bad.md"
    path.write_text("---\nkey: value\n\nNo closing delimiter")

    result = GateResult(verdict=GateVerdict.PASS, checks=[], content_sha256="x")

    with pytest.raises(ValueError, match="missing closing frontmatter delimiter"):
        append_gate_result(path, result)
