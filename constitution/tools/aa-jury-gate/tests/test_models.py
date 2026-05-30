"""VS-01: Domain model tests (ENG-4.1 RED→GREEN).

All 6 test targets from phase-5-plan.md §VS-01.
"""
import dataclasses
import json
from enum import Enum

from aa_jury_gate.models import (
    AuditEntry,
    CheckItem,
    CheckResult,
    GateResult,
    GateVerdict,
    GitBinaryNotFoundError,
    GitProbeError,
    GitStatus,
    ToolError,
)


# ── Test target 1: GateVerdict.exit_code ──────────────────────────────────────

def test_gate_verdict_exit_code_pass():
    assert GateVerdict.PASS.exit_code == 0


def test_gate_verdict_exit_code_fail():
    assert GateVerdict.FAIL.exit_code == 1


def test_gate_verdict_exit_code_error():
    assert GateVerdict.ERROR.exit_code == 2


def test_gate_verdict_pass_value():
    """GateVerdict .value strings (C-P6-VS01-R1-004 mutation kill)."""
    assert GateVerdict.PASS.value == "PASS"


def test_gate_verdict_fail_value():
    assert GateVerdict.FAIL.value == "FAIL"


def test_gate_verdict_error_value():
    assert GateVerdict.ERROR.value == "ERROR"


# ── Test target 2: CheckResult values ─────────────────────────────────────────

def test_check_result_pass_value():
    assert CheckResult.PASS.value == "PASS"


def test_check_result_fail_value():
    assert CheckResult.FAIL.value == "FAIL"


def test_check_result_skip_value():
    assert CheckResult.SKIP.value == "SKIP"


def test_check_result_is_plain_enum():
    """Enum only — no str mixin (Phase 4 §5.3)."""
    assert not issubclass(CheckResult, str)


def test_gate_verdict_is_plain_enum():
    """Enum only — no str mixin (Phase 4 §5.3)."""
    assert not issubclass(GateVerdict, str)


# ── Test target 3: GitBinaryNotFoundError is subclass of ToolError ───────────

def test_git_binary_not_found_is_tool_error():
    assert issubclass(GitBinaryNotFoundError, ToolError)


def test_git_binary_not_found_is_exception():
    err = GitBinaryNotFoundError("git not found")
    assert isinstance(err, Exception)
    assert isinstance(err, ToolError)


# ── Test target 4: GitProbeError is NOT a subclass of ToolError ──────────────

def test_git_probe_error_not_tool_error():
    assert not issubclass(GitProbeError, ToolError)


def test_git_probe_error_is_exception():
    err = GitProbeError("repo state invalid")
    assert isinstance(err, Exception)
    assert not isinstance(err, ToolError)


# ── Test target 5: GitStatus values ──────────────────────────────────────────

def test_git_status_clean():
    assert GitStatus.CLEAN is not None


def test_git_status_untracked():
    assert GitStatus.UNTRACKED is not None


def test_git_status_uncommitted():
    assert GitStatus.UNCOMMITTED is not None


def test_git_status_three_members():
    assert len(GitStatus) == 3


def test_git_status_is_enum():
    assert issubclass(GitStatus, Enum)


def test_git_status_clean_value():
    """Exact .value contract per Phase 4 §2.3 (C-P6-VS01-R1-001)."""
    assert GitStatus.CLEAN.value == "CLEAN"


def test_git_status_untracked_value():
    assert GitStatus.UNTRACKED.value == "UNTRACKED"


def test_git_status_uncommitted_value():
    assert GitStatus.UNCOMMITTED.value == "UNCOMMITTED"


# ── Test target 6: GateResult instantiation ──────────────────────────────────

def test_gate_result_instantiation():
    item = CheckItem(check_id="S01", result=CheckResult.PASS, detail="ok")
    result = GateResult(
        content_sha256="abc123",
        verdict=GateVerdict.PASS,
        checks=[item],
    )
    assert result.content_sha256 == "abc123"
    assert result.verdict == GateVerdict.PASS
    assert len(result.checks) == 1
    assert result.checks[0].check_id == "S01"


def test_gate_result_default_checks_empty_list():
    """Test target 6: GateResult instantiation with defaults (C-P6-VS01-R1-002).

    Verifies the default_factory=list is correct and produces an independent
    empty list per instance — not a shared mutable default.
    """
    result = GateResult(content_sha256="abc", verdict=GateVerdict.PASS)
    assert result.checks == []
    assert isinstance(result.checks, list)
    # independent instances — not shared mutable default
    result2 = GateResult(content_sha256="def", verdict=GateVerdict.FAIL)
    result.checks.append(CheckItem(check_id="S01", result=CheckResult.PASS, detail=""))
    assert result2.checks == []


def test_check_item_dataclass():
    item = CheckItem(check_id="G01", result=CheckResult.FAIL, detail="uncommitted")
    assert dataclasses.is_dataclass(item)
    assert item.result == CheckResult.FAIL


def test_audit_entry_instantiation():
    entry = AuditEntry()
    assert entry.tool == "aa-jury-gate"
    assert entry.version == ""
    assert entry.timestamp_utc == ""
    assert entry.synthesis_path == ""
    assert entry.content_sha256 == ""
    assert entry.verdict == ""
    assert entry.allow_no_git is False
    assert entry.checks_failed == 0
    assert entry.checks_skipped == 0
    assert entry.checks == []


def test_check_item_enum_serialization():
    """Enum values require default= lambda in json.dumps (Phase 4 §6.1).

    Renamed from test_audit_entry_enum_serialization — this tests CheckItem
    serialization (C-P6-VS01-R1-005).
    """
    item = CheckItem(check_id="S01", result=CheckResult.PASS, detail="ok")
    serialized = json.dumps(
        dataclasses.asdict(item),
        default=lambda o: o.value if isinstance(o, Enum) else str(o),
    )
    data = json.loads(serialized)
    assert data["result"] == "PASS"


def test_audit_entry_enum_serialization():
    """AuditEntry serialization with Enum fields in checks list (C-P6-VS01-R1-005)."""
    item = CheckItem(check_id="S01", result=CheckResult.PASS, detail="ok")
    entry = AuditEntry(
        tool="aa-jury-gate",
        verdict="PASS",
        checks_failed=0,
        checks=[dataclasses.asdict(item)],
    )
    serialized = json.dumps(
        dataclasses.asdict(entry),
        default=lambda o: o.value if isinstance(o, Enum) else str(o),
    )
    data = json.loads(serialized)
    assert data["tool"] == "aa-jury-gate"
    assert data["verdict"] == "PASS"
