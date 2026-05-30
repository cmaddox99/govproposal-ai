"""Domain model: enums, dataclasses, and exception hierarchy.

No business logic lives here — pure data types only (Phase 4 §1.2).
Laws: ENG-6.4 (data classification), ENG-2.1 (modular design).
"""
from __future__ import annotations

import dataclasses
from enum import Enum
from typing import Any


# ── Enums (Enum only — no str mixin; Phase 4 §5.3) ───────────────────────────

class CheckResult(Enum):
    """Result of a single gate check."""
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"


class GateVerdict(Enum):
    """Overall verdict of a gate run."""
    PASS = "PASS"   # all checks PASS → exit 0
    FAIL = "FAIL"   # one or more checks FAIL → exit 1
    ERROR = "ERROR" # invocation/parse error → exit 2

    @property
    def exit_code(self) -> int:
        return {GateVerdict.PASS: 0, GateVerdict.FAIL: 1, GateVerdict.ERROR: 2}[self]


class GitStatus(Enum):
    """Return type of GitProbe.check() (Phase 4 §2.3)."""
    CLEAN = "CLEAN"           # tracked, committed, no uncommitted changes
    UNTRACKED = "UNTRACKED"   # file exists but not tracked by git
    UNCOMMITTED = "UNCOMMITTED"  # tracked but has uncommitted changes


# ── Dataclasses ───────────────────────────────────────────────────────────────

@dataclasses.dataclass
class CheckItem:
    """Result of one named check."""
    check_id: str
    result: CheckResult
    detail: str


@dataclasses.dataclass
class GateResult:
    """Complete gate run result (Phase 4 §1.2)."""
    content_sha256: str
    verdict: GateVerdict
    checks: list[CheckItem] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class AuditEntry:
    """JSON-Lines audit log entry (Phase 4 §6.1).

    Serialization: use json.dumps(dataclasses.asdict(entry),
        default=lambda o: o.value if isinstance(o, Enum) else str(o))
    The default= lambda is REQUIRED — dataclasses.asdict() does not
    auto-convert Enum members to .value (Phase 4 §6.1, C-P4-J2-NF-003-R2).
    """
    tool: str = "aa-jury-gate"
    version: str = ""
    timestamp_utc: str = ""
    synthesis_path: str = ""
    content_sha256: str = ""
    verdict: str = ""
    allow_no_git: bool = False
    checks_failed: int = 0
    checks_skipped: int = 0
    checks: list[dict[str, Any]] = dataclasses.field(default_factory=list)


# ── Exception hierarchy (Phase 4 §5.2) ───────────────────────────────────────

class ToolError(Exception):
    """Invocation/tool errors → exit 2. User-facing message included."""


class GitBinaryNotFoundError(ToolError):
    """git binary absent from PATH → exit 2 (C-P4-J4-005)."""


class GitProbeError(Exception):
    """Git repo-state failures (file not tracked, uncommitted) → G01 FAIL (exit 1).

    Distinguished from GitBinaryNotFoundError which is a tool-configuration
    error. GitProbeError intentionally does NOT extend ToolError.
    """


class GitNotInRepoError(GitProbeError):
    """Path is not inside a git repository — infrastructure gap, not a file error.

    Subclass of GitProbeError. Caught separately by check_g01 to SKIP under
    allow_no_git=True (Phase 3 §1.6: 'path not in repo' → SKIP when allow_no_git).
    File-specific errors (not tracked, uncommitted) use the base GitProbeError
    and always FAIL regardless of allow_no_git.
    """
