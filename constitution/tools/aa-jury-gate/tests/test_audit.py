"""Tests for audit logging (BUS-7.1)."""

import json
from pathlib import Path

import pytest

from aa_jury_gate.audit import write_audit_log
from aa_jury_gate.models import GateVerdict


class TestAuditLogging:
    """Test audit trail functionality (BUS-7.1)."""

    def test_audit_log_written(self, tmp_path: Path) -> None:
        """Test that audit log file is created and entry written."""
        log_dir = tmp_path / "logs"
        synthesis_path = tmp_path / "synthesis.md"
        synthesis_path.write_text("test content", encoding="utf-8")

        write_audit_log(
            log_dir=log_dir,
            synthesis_path=synthesis_path,
            verdict=GateVerdict.PASS,
            checks_failed=0,
            checks_skipped=0,
            content_sha256="abc123",
            tool_version="1.0.0",
            exit_code=0,
        )

        log_file = log_dir / "aa-jury-gate.jsonl"
        assert log_file.exists()
        assert log_file.is_file()

    def test_audit_log_format(self, tmp_path: Path) -> None:
        """Test audit log entry has correct JSON Lines format."""
        log_dir = tmp_path / "logs"
        synthesis_path = tmp_path / "synthesis.md"
        synthesis_path.write_text("test content", encoding="utf-8")

        write_audit_log(
            log_dir=log_dir,
            synthesis_path=synthesis_path,
            verdict=GateVerdict.FAIL,
            checks_failed=2,
            checks_skipped=1,
            content_sha256="def456",
            tool_version="1.0.0",
            exit_code=1,
        )

        log_file = log_dir / "aa-jury-gate.jsonl"
        line = log_file.read_text(encoding="utf-8").strip()
        
        # Parse JSON
        entry = json.loads(line)

        # Verify required fields
        assert "timestamp_utc" in entry
        assert entry["synthesis_path"] == str(synthesis_path.resolve())
        assert entry["verdict"] == "FAIL"
        assert entry["checks_failed"] == 2
        assert entry["checks_skipped"] == 1
        assert entry["content_sha256"] == "def456"
        assert entry["tool"] == "aa-jury-gate"
        assert entry["version"] == "1.0.0"
        assert entry["exit_code"] == 1

        # Verify timestamp is ISO 8601 format
        assert "T" in entry["timestamp_utc"]
        assert entry["timestamp_utc"].endswith("+00:00") or entry["timestamp_utc"].endswith("Z")

    def test_audit_log_dir_created(self, tmp_path: Path) -> None:
        """Test that log directory is created if it doesn't exist."""
        log_dir = tmp_path / "nested" / "logs"
        assert not log_dir.exists()

        synthesis_path = tmp_path / "synthesis.md"
        synthesis_path.write_text("test content", encoding="utf-8")

        write_audit_log(
            log_dir=log_dir,
            synthesis_path=synthesis_path,
            verdict=GateVerdict.PASS,
            checks_failed=0,
            checks_skipped=0,
            content_sha256="ghi789",
            tool_version="1.0.0",
            exit_code=0,
        )

        assert log_dir.exists()
        assert log_dir.is_dir()
        assert (log_dir / "aa-jury-gate.jsonl").exists()

    def test_audit_log_append(self, tmp_path: Path) -> None:
        """Test that multiple invocations append to log file."""
        log_dir = tmp_path / "logs"
        synthesis_path = tmp_path / "synthesis.md"
        synthesis_path.write_text("test content", encoding="utf-8")

        # First invocation
        write_audit_log(
            log_dir=log_dir,
            synthesis_path=synthesis_path,
            verdict=GateVerdict.PASS,
            checks_failed=0,
            checks_skipped=0,
            content_sha256="first",
            tool_version="1.0.0",
            exit_code=0,
        )

        # Second invocation
        write_audit_log(
            log_dir=log_dir,
            synthesis_path=synthesis_path,
            verdict=GateVerdict.FAIL,
            checks_failed=1,
            checks_skipped=0,
            content_sha256="second",
            tool_version="1.0.0",
            exit_code=1,
        )

        log_file = log_dir / "aa-jury-gate.jsonl"
        lines = log_file.read_text(encoding="utf-8").strip().split("\n")
        
        assert len(lines) == 2
        
        # Both lines are valid JSON
        entry1 = json.loads(lines[0])
        entry2 = json.loads(lines[1])
        
        assert entry1["verdict"] == "PASS"
        assert entry1["content_sha256"] == "first"
        assert entry2["verdict"] == "FAIL"
        assert entry2["content_sha256"] == "second"

    def test_audit_log_pass_verdict(self, tmp_path: Path) -> None:
        """Test audit log for PASS verdict."""
        log_dir = tmp_path / "logs"
        synthesis_path = tmp_path / "synthesis.md"
        synthesis_path.write_text("test content", encoding="utf-8")

        write_audit_log(
            log_dir=log_dir,
            synthesis_path=synthesis_path,
            verdict=GateVerdict.PASS,
            checks_failed=0,
            checks_skipped=2,
            content_sha256="pass_test",
            tool_version="1.0.0",
            exit_code=0,
        )

        log_file = log_dir / "aa-jury-gate.jsonl"
        entry = json.loads(log_file.read_text(encoding="utf-8"))
        
        assert entry["verdict"] == "PASS"
        assert entry["exit_code"] == 0
        assert entry["checks_failed"] == 0
        assert entry["checks_skipped"] == 2
