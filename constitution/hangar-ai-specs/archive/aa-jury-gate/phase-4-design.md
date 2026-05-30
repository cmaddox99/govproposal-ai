---
author: Hangar AI (claude-sonnet-4.6)
citation_audit:
  allow_draft: []
  draft_skipped: []
  exit_code: 0
  fail_count: 0
  law_count: 125
  pass_count: 16
  registry: /Users/979925/Repos/governance/hangar-ai-constitution/laws/index.yaml
  scanned: 16
  strict: false
  timestamp: '2026-05-26T02:11:59Z'
  tool: aa-citation-audit
  verdicts:
  - context_snippet: null
    id: BUS-7.1
    verdict: PASS
  - context_snippet: null
    id: ENG-1.5
    verdict: PASS
  - context_snippet: null
    id: ENG-10.1
    verdict: PASS
  - context_snippet: null
    id: ENG-11.1
    verdict: PASS
  - context_snippet: null
    id: ENG-12.1
    verdict: PASS
  - context_snippet: null
    id: ENG-2.1
    verdict: PASS
  - context_snippet: null
    id: ENG-2.5
    verdict: PASS
  - context_snippet: null
    id: ENG-3.5
    verdict: PASS
  - context_snippet: null
    id: ENG-3.7
    verdict: PASS
  - context_snippet: null
    id: ENG-4.4
    verdict: PASS
  - context_snippet: null
    id: ENG-6.1
    verdict: PASS
  - context_snippet: null
    id: ENG-6.4
    verdict: PASS
  - context_snippet: null
    id: ENG-6.5
    verdict: PASS
  - context_snippet: null
    id: ENG-6.7
    verdict: PASS
  - context_snippet: null
    id: PRD-2.6
    verdict: PASS
  - context_snippet: null
    id: PRD-5.1
    verdict: PASS
  version: 0.2.0
  warn_count: 0
date: 2026-05-25
law_citations:
- ENG-1.5
- ENG-2.1
- ENG-2.5
- ENG-3.5
- ENG-3.7
- ENG-6.1
- ENG-6.4
- ENG-6.5
- ENG-6.7
- ENG-10.1
- ENG-11.1
- ENG-12.1
- PRD-2.6
- PRD-5.1
- BUS-7.1
phase: 4
project: aa-jury-gate
status: APPROVED
title: Design — aa-jury-gate CLI
workflow: greenfield-development
---





# Phase 4 — Design: aa-jury-gate CLI

> **Phase focus (greenfield-development.md §Phase 4):**
> Architecture decisions (ENG-2.1); security threat model (ENG-6.1);
> ADRs filed; module decomposition; dependency injection design (ENG-2.5).
>
> **Inputs:** Phase 3 Define (CLI contract, BDD, data model, 14 checks)
> **Output:** Architecture blueprint + 4 ADRs + threat model

---

## 0. Environment Constraints (C-P4-J2-003, C-P4-J1-008)

| Constraint | Value | Rationale |
|-----------|-------|-----------|
| `python_requires` | `>=3.10` | `str \| None` union syntax (PEP 604); `list[T]` built-in generic (PEP 585). **Note:** AA CI must provide Python 3.10+. If CI is pinned to 3.9, backport requires `from __future__ import annotations` and `typing.Union`/`typing.List`. |
| `click` | `>=8.1` | `CliRunner` isolation; consistent with `citation-auditor` |
| `PyYAML` | `>=6.0` | `yaml.safe_load` — AC-SEC-01 mandatory |
| Platform | Linux, macOS | `os.replace()` atomicity; local POSIX filesystem assumed |

---

## 1. Module Architecture (ENG-2.1 — Modular Design)

### 1.1 Package Layout (11 modules — C-P4-J3-001, C-P4-J5-007)

```
aa_jury_gate/
├── __init__.py           # version sourced here via importlib.metadata
├── cli.py                # Click entry point; wires DI container; ENG-1.5
├── gate.py               # GateRunner — orchestrates all 14 checks; PRD-2.6
├── extractor.py          # YAML frontmatter extraction + strip_jury_gate()
├── models.py             # Enums + dataclasses: CheckResult, GateVerdict,
│                         #   CheckItem, GitStatus, GateResult, ToolError; ENG-6.4
├── checks/
│   ├── __init__.py
│   ├── schema.py         # S01–S11 surface 1-3 checks
│   ├── body.py           # B01–B03 surface 4 body checks
│   └── git.py            # G01 git probe check
├── output.py             # stdout table renderer + --output append writer; ENG-13.1
├── audit.py              # JSON-Lines audit logger; ENG-6.7, BUS-7.1
├── git_probe.py          # GitProbe Protocol + RealGitProbe + StubGitProbe; ENG-2.5
└── security.py           # Path validation, symlink refusal, size cap; ENG-6.5
```

Module count: 11 Python files (excluding `__init__.py` files). `checks/` is a sub-package containing 3 modules.

### 1.2 Responsibility Boundaries

| Module | Responsibility | Depends on |
|--------|---------------|------------|
| `cli.py` | Parse CLI args; wire DI; call GateRunner; format exit | models, gate, output, audit, security |
| `gate.py` | Run S01–S11, B01–B03, G01 in order; collect CheckItems; compute GateResult | extractor, checks/*, models, git_probe |
| `extractor.py` | YAML frontmatter extraction; `strip_jury_gate()`; content_sha256 hashing | — (stdlib only) |
| `models.py` | Data types + ToolError exception hierarchy; no logic | — (pure dataclasses + enums) |
| `checks/schema.py` | S01–S11 check functions; return `CheckItem` | models, extractor |
| `checks/body.py` | B01–B03 regex checks on body text | models |
| `checks/git.py` | G01 check using injected GitProbe | models, git_probe |
| `output.py` | Render stdout table; write `jury_gate:` block atomically | models, extractor (C-P4-J2-004) |
| `audit.py` | Append JSON-Lines log entry; non-fatal on failure | models |
| `git_probe.py` | Protocol definition + real subprocess impl + test stub | models |
| `security.py` | Validate SYNTHESIS path; validate --log-dir path | — (stdlib only) |

**Import DAG (C-P4-J1-006) — strictly acyclic:**
```
models.py  ←  checks/*  ←  gate.py  ←  cli.py
models.py  ←  extractor.py  ←  gate.py, output.py, checks/schema.py
models.py  ←  git_probe.py  ←  checks/git.py
models.py  ←  security.py  ←  cli.py
```
`ToolError` lives in `models.py`. No module imports from `gate.py` or `cli.py`.

### 1.3 Data Flow

```
CLI args
  │
  ▼
security.py: (1) exists? (2) is_file? (3) symlink? (4) size ≤ 1MB?  ← C-P4-J5-003
  │             raises ToolError on any failure → exit 2
  ▼
extractor.py: parse frontmatter + body (yaml.safe_load)
  │             strip_jury_gate(raw_text) → compute content_sha256
  ▼
gate.py → checks/schema.py   → [S01–S11 CheckItems]
        → checks/body.py     → [B01–B03 CheckItems or SKIP]
        → checks/git.py      → [G01 CheckItem]
  │
  ▼
GateResult (content_sha256, verdict, checks[])
  │
  ├─→ output.py: render stdout table
  ├─→ audit.py: append gate.log entry
  └─→ output.py: write jury_gate: block (if --output append, exit 0 or 1)
```

**content_sha256 computation point:** After `extractor.parse()` succeeds, `gate.py` calls
`extractor.strip_jury_gate(raw_text)` then computes the hash (see §4 ADR-002 for exact formula).

---

## 2. Dependency Injection Design (ENG-2.5 — Protocol Abstraction)

### 2.1 extractor.py Public API (C-P4-J4-003, C-P4-J1-001)

```python
# extractor.py
from pathlib import Path

class UnclosedFrontmatterError(Exception): ...

def parse(path: Path) -> tuple[dict, str]:
    """Parse YAML frontmatter and return (frontmatter_dict, body_str).

    Raises:
        UnclosedFrontmatterError: opening --- found but no closing ---
        yaml.YAMLError: frontmatter is not valid YAML
    Returns empty dict for frontmatter if no opening --- found.
    """
    ...

def strip_jury_gate(content: str) -> str:
    """Remove the jury_gate: key and its entire value block from YAML
    frontmatter text. Returns content unchanged if no jury_gate: key present.
    The operation preserves all other frontmatter keys and the body unchanged.
    Uses YAML parse-and-remove for determinism (not regex).

    Input: Full file content including `---` delimiters and body (i.e., the
    decoded raw bytes of the synthesis file, as passed by the canonical hash
    formula). Output: Same structure with jury_gate: block excised from
    frontmatter. (C-P4-J5-001-R2, C-P4-J2-NF-003-R2)
    """
    ...
```

**content_sha256 formula (ADR-002 amendment — C-P4-J2-001, C-P4-J5-001):**
```python
import hashlib
raw_bytes: bytes = path.read_bytes()
stripped: str = extractor.strip_jury_gate(raw_bytes.decode('utf-8'))
content_sha256: str = hashlib.sha256(stripped.encode('utf-8')).hexdigest()
```
Encoding: UTF-8 decode then UTF-8 encode. This is the **only** canonical computation. Hashing re-serialized YAML is explicitly PROHIBITED (key-order and whitespace non-determinism).

### 2.2 security.py Public API (C-P4-J4-006, C-P4-J5-003)

```python
# security.py
from pathlib import Path

def validate_synthesis_path(path: Path) -> Path:
    """Validate SYNTHESIS argument path.
    Sequence (order matters — C-P4-J5-003):
      1. path.exists()           → ToolError "synthesis file not found"       exit 2
      2. path.is_file()          → ToolError "synthesis path is a directory"   exit 2
      3. path.is_symlink()       → ToolError "synthesis path is a symlink"     exit 2
      4. path.stat().st_size     → ToolError "synthesis file too large (max 1MB)" exit 2
    Returns resolved absolute Path on success.
    Raises ToolError (→ exit 2) on any violation.
    """
    ...

def validate_log_dir(log_dir: str | None) -> Path:
    """Resolve and validate --log-dir path.
    1. Expand ~ via os.path.expanduser()
    2. Resolve symlinks via os.path.realpath()
    3. Verify resolved path does not escape CWD
    Returns resolved Path. Raises ToolError on path-boundary violation.
    """
    ...
```

### 2.3 GitProbe Protocol

```python
# git_probe.py
from typing import Protocol
from pathlib import Path
from .models import GitStatus

class GitProbe(Protocol):
    """Injectable interface for git state inspection.
    Enables test isolation without filesystem/subprocess coupling."""
    def check(self, path: Path) -> GitStatus: ...


class RealGitProbe:
    """Production implementation using subprocess git commands."""
    def check(self, path: Path) -> GitStatus:
        # 1. git rev-parse --is-inside-work-tree
        # 2. git ls-files --error-unmatch <path>
        # 3. git diff --name-only HEAD -- <path>
        # All calls: subprocess.run([...], shell=False)
        ...


class StubGitProbe:
    """Test double for unit testing gate logic without git."""
    def __init__(self, status: GitStatus):
        self._status = status

    def check(self, path: Path) -> GitStatus:
        return self._status
```

### 2.2 Wiring in cli.py (renamed from 2.2 — now 2.4 after API sections)

```python
# cli.py (simplified)
@click.command()
@click.argument('synthesis', type=click.Path())   # exists check omitted; security.py validates (C-P4-J2-007)
@click.option('--allow-no-git', is_flag=True)
@click.option('--output', type=click.Choice(['append']))
@click.option('--log-dir', type=click.Path(), default=None)
def main(synthesis, allow_no_git, output, log_dir):
    probe: GitProbe = RealGitProbe()          # production wiring
    runner = GateRunner(git_probe=probe)
    result = runner.run(Path(synthesis), allow_no_git=allow_no_git)
    render_stdout(result)
    write_audit_log(result, log_dir)
    if output == 'append':
        write_jury_gate_block(result, Path(synthesis))
    sys.exit(result.verdict.exit_code)        # GateVerdict.exit_code — see §5.3
```

**Raw `sys.exit()` ban (C-P4-J5-005):** All exit paths inside command functions MUST use `ctx.exit()`, raise a `click.ClickException`, or raise `SystemExit`. Raw `sys.exit()` calls outside `main()` are prohibited — they prevent `CliRunner` from capturing results cleanly in integration tests.

**No DI framework.** Constructor injection is sufficient for this tool's scope. Consistent with `citation-auditor` pattern.

---

## 3. Security Threat Model (ENG-6.1, ENG-6.5)

### 3.1 Threat Register

| ID | Threat | STRIDE | Attack Vector | Mitigation | Residual Risk |
|----|--------|--------|--------------|-----------|---------------|
| T1 | YAML DoS via oversized file | DoS | Attacker supplies >1MB `.md` file | 1MB pre-parse cap in `security.py`; exit 2 | Low |
| T2 | Arbitrary code execution via `yaml.load()` | Execution | Malicious YAML with `!!python/object` tag | `yaml.safe_load()` only (AC-SEC-01) | None |
| T3 | Path traversal via SYNTHESIS arg | Elevation | `../../../../etc/passwd` as path | `os.path.realpath()` + cwd-boundary check in `security.py` | Low |
| T4 | Symlink escape | Elevation | Symlink to sensitive file outside cwd | Symlink detection before open; exit 2 | Low |
| T5 | Log dir escape via `--log-dir` or env var | Elevation | `../../../var/log` via AA_JURY_GATE_LOG_DIR | realpath + cwd-boundary in `security.py` | Low |
| T6 | Temp file race (TOCTOU) | Tampering | Replace temp file between write and rename | `tempfile.NamedTemporaryFile(dir=target_dir)` + `os.replace()` atomic rename | Low |
| T7 | Shell injection via git commands | Execution | Malicious path with shell metacharacters | `subprocess.run([...], shell=False)` always | None |
| T8 | Audit log poisoning | Tampering | Multi-process concurrent writes | JSON-Lines append; best-effort atomic on local POSIX FS for small records; **NOT guaranteed on NFS/SMB** (C-P4-J1-003, C-P4-J4-002) | Low (local FS); Medium (NFS) |
| T9 | Forged synthesis / tamper after gate approval | Tampering | Modify synthesis after gate approval | `content_sha256` in `jury_gate:` block; humans verify hash on APPROVE. v1 limitation: no mechanical re-check on re-run (C-P4-J3-002 deferred to v2) | Low |

### 3.2 Security Controls (ENG-6.5 NON-NEGOTIABLE)

| Control | Location | Enforcement level |
|---------|----------|------------------|
| `yaml.safe_load()` only | `extractor.py` | NON-NEGOTIABLE (AC-SEC-01) |
| `shell=False` on all subprocess | `git_probe.py` | NON-NEGOTIABLE |
| 1MB YAML size cap | `security.py` | Required |
| Symlink refusal | `security.py` | Required |
| realpath cwd-boundary for all paths | `security.py` | Required |
| Atomic write (`os.replace()`, same-dir temp) | `output.py` | Required |
| No PII in audit log | `audit.py` | Required (ENG-6.4) |

### 3.3 Out-of-Scope Threats (v1)

- Network-based threats: tool is local-only; no network I/O
- Multi-user file permission attacks: not in PRD-5.1 v1 scope
- Cryptographic signing of gate results: v2 hardening

---

## 4. Architecture Decision Records

### ADR-001: Click as CLI Framework

**Status:** ACCEPTED
**Law:** ENG-1.5 (API-First Design), ENG-2.1

**Decision:** Use `click >= 8.1` as the CLI framework.

**Rationale:**
- Consistent with `citation-auditor` (same constitution tool family)
- `CliRunner` enables `--invoke` testing without subprocesses (ENG-4.4 BDD)
- Declarative option/argument definition aligns with ENG-1.5 contract-first design
- No alternative evaluated that provides comparable testability at this scope

**Consequences:**
- `click.Path()` (no `exists` argument) used for SYNTHESIS — existence check is our responsibility (S01). Note: `exists=False` is Click's default and is misleading; use bare `click.Path()` with a comment. (C-P4-J2-007)
- `click.Choice(['append'])` for `--output` prevents free-form flag abuse

---

### ADR-002: content_sha256 Computed Post-Strip

**Status:** ACCEPTED
**Law:** ENG-6.5, ENG-6.7, BUS-7.1

**Decision:** `content_sha256` is computed on file bytes **after** stripping the `jury_gate:` frontmatter key, not on raw file bytes.

**Canonical formula (C-P4-J2-001, C-P4-J5-001):**
```python
raw_bytes: bytes = path.read_bytes()
stripped: str = extractor.strip_jury_gate(raw_bytes.decode('utf-8'))
content_sha256: str = hashlib.sha256(stripped.encode('utf-8')).hexdigest()
```
- Encoding: UTF-8 decode → UTF-8 encode. No other codec permitted.
- Hashing re-serialized YAML is **PROHIBITED** — key-order and whitespace are non-deterministic.
- `strip_jury_gate()` uses YAML parse-and-remove (not regex) for determinism.

**Rationale:**
- Produces a stable content-address: re-runs on unchanged synthesis yield identical hash
- Audit consumers can reliably detect synthesis content changes across gate runs
- Alternative (hash raw bytes) creates a hash chain — each run's hash encodes the previous run's `jury_gate:` block
- Judicial synthesis (Phase 3) ruled this REQUIRED

**Consequences:**
- `extractor.py` exposes `strip_jury_gate(content: str) -> str` (see §2.1)
- Hash is computed in `gate.py` before any write operations

---

### ADR-003: write-on-exit-1 for --output append

**Status:** ACCEPTED (J3 CHALLENGE DISMISSED)
**Law:** ENG-6.7, BUS-7.1

**Decision:** `--output append` writes the `jury_gate:` block on exit 0 AND exit 1. NOT written on exit 2.

**Rationale:**
- A gate FAIL is a meaningful governance event; it must be recorded in the artifact
- stdout and gate.log are ephemeral in many CI systems; artifact-embedded state is durable
- J3 (Product Lens) challenged this; J1/J2/J4/J5 accepted; judicial synthesis dismissed the challenge
- CI pipelines requiring clean worktree post-failure: `git checkout -- <synthesis_file>`

**Consequences:**
- `output.py` checks `result.verdict != GateVerdict.ERROR` before writing
- `jury_gate.verdict` is `"PASS"` (exit 0) or `"FAIL"` (exit 1)

**jury_gate: block on exit 1 (C-P4-J1-004):**
```yaml
jury_gate:
  tool: aa-jury-gate
  version: "1.0.0"
  timestamp_utc: "2026-05-25T20:00:00Z"
  verdict: "FAIL"
  content_sha256: "abc123..."
  checks_failed: 2
  checks_skipped: 3
```

---

### ADR-004: No DI Framework — Constructor Injection Only

**Status:** ACCEPTED
**Law:** ENG-2.5, PRD-5.1

**Decision:** Dependency injection via constructor parameters only. No DI container framework (no `inject`, `dependency_injector`, `lagom`).

**Rationale:**
- Tool has exactly one injectable boundary: `GitProbe`
- DI frameworks add installation weight and configuration complexity for one injection point
- `Protocol`-based typing (PEP 544) provides interface contracts without framework coupling
- `StubGitProbe` for tests is trivially constructible (one line)
- Consistent with `citation-auditor` architecture

**Consequences:**
- `GateRunner.__init__(self, git_probe: GitProbe)` is the only DI seam
- `cli.py` is the composition root — it instantiates `RealGitProbe` and passes it in
- Future injectable seams (e.g., `AuditLogger`) added via same pattern

---

## 5. Check Execution Strategy (ENG-3.7 — Error Handling)

### 5.1 Fast-fail vs. Collect-all

```
Phase          Behaviour on FAIL        Rationale
─────────────  ───────────────────────  ──────────────────────────────────────
S01 (exists)   exit 2 immediately       No point continuing; file absent
S02 (ext)      continue, collect FAIL   Policy violation; other checks may run
S03 (YAML)     exit 2 immediately       Cannot parse; all downstream checks invalid
S04 (dict)     exit 2 immediately       Cannot proceed; root is not a mapping
S05–S11        collect, report all      Surface all schema violations at once
B01–B03        collect (or SKIP)        B-checks SKIP if S11 failed
G01            collect, report          Git check independent; always informative
```

### 5.2 Exception Handling Boundaries

```python
# models.py — exception hierarchy (C-P4-J1-006: ToolError lives in models.py)
class ToolError(Exception):
    """Invocation/tool errors → exit 2. User-facing message included."""
    ...

class GitBinaryNotFoundError(ToolError):
    """git binary absent from PATH → exit 2 (C-P4-J4-005)."""
    ...

class GitProbeError(Exception):
    """Git repo-state failures (file not tracked, uncommitted) → G01 FAIL (exit 1).
    Distinguished from GitBinaryNotFoundError which is a tool-configuration error."""
    ...
```

```python
# gate.py pattern
try:
    frontmatter, body = extractor.parse(path)
except extractor.UnclosedFrontmatterError:
    raise ToolError("synthesis file has unclosed YAML frontmatter")
except yaml.YAMLError as e:
    raise ToolError(f"synthesis file is not valid YAML: {e}")
except PermissionError:
    raise ToolError(f"cannot read synthesis file: {path}")   # C-P4-J1-002
```

**Exception routing in cli.py:**
- `ToolError` (incl. `GitBinaryNotFoundError`) → stderr message → exit 2
- `GitProbeError` → G01 `CheckItem(result=FAIL, detail=...)` → exit 1
- `PermissionError` → wrapped as `ToolError` → stderr + exit 2
- Unexpected exceptions → `Error: unexpected error: <type>: <msg>` → exit 2

**Git error taxonomy (C-P4-J4-005 — resolves Phase 3 §1.5 vs Phase 4 §5 conflict):**

| Error type | Class | Exit |
|-----------|-------|------|
| `git` binary not in PATH | `GitBinaryNotFoundError(ToolError)` | 2 |
| `git rev-parse` fails (not a git repo, --allow-no-git not set) | `GitProbeError` | 1 (G01 FAIL) |
| `git ls-files` or `git diff` shows uncommitted state | `GitProbeError` | 1 (G01 FAIL) |

### 5.3 GateVerdict Exit Code Mapping (C-P4-J2-002, C-P4-J4-004)

```python
# models.py
from enum import Enum

class GateVerdict(Enum):
    PASS = "PASS"    # all checks PASS → exit 0
    FAIL = "FAIL"    # one or more checks FAIL → exit 1
    ERROR = "ERROR"  # invocation/parse error → exit 2

    @property
    def exit_code(self) -> int:
        return {GateVerdict.PASS: 0, GateVerdict.FAIL: 1, GateVerdict.ERROR: 2}[self]
```

---

## 6. Audit Log Design (ENG-6.7, ENG-10.1, BUS-7.1)

### 6.1 Log Entry Schema

```python
@dataclass
class AuditEntry:
    tool: str = "aa-jury-gate"
    version: str = ""            # tool version from importlib.metadata (C-P4-J1-007)
    timestamp_utc: str = ""      # ISO-8601
    synthesis_path: str = ""     # absolute path
    content_sha256: str = ""
    verdict: str = ""            # "PASS" | "FAIL"
    allow_no_git: bool = False
    checks_failed: int = 0
    checks_skipped: int = 0
    checks: list[dict[str, Any]] = field(default_factory=list)
    # checks is populated via: [asdict_enum_safe(c) for c in gate_result.checks]
    # where asdict_enum_safe uses: json.dumps(dataclasses.asdict(c),
    #   default=lambda o: o.value if isinstance(o, Enum) else str(o))
    # dataclasses.asdict() does NOT auto-convert Enum → .value; the default=
    # lambda is REQUIRED to avoid TypeError (C-P4-J2-NF-003-R2, C-P4-J5-004-R2)
```

**Serialization contract (C-P4-J2-005, C-P4-J5-004, C-P4-J2-NF-003-R2):**
- `audit.py` serializes each `CheckItem` via `json.dumps(dataclasses.asdict(entry), default=lambda o: o.value if isinstance(o, Enum) else str(o))`.
- `dataclasses.asdict()` does **not** automatically convert `Enum` members to their `.value`; the `default=` lambda is mandatory.
- `CheckResult` enum values serialize to `"PASS"`, `"FAIL"`, `"SKIP"` strings via this lambda.
- Any non-serializable field (e.g., `Path`, `datetime`) must be converted to `str` before population or handled by the `default=` lambda.

**version field:** sourced from `importlib.metadata.version("aa-jury-gate")` at runtime. Audit schema version is implicitly `1` for this release; a `schema_version` field may be added in v2.

### 6.2 Log Rotation

- v1: No rotation. Append-only `gate.log`. **Operator guidance:** log exceeding 100MB should be manually archived. No automated warning in v1.
- v2: Size-based rotation (configurable `--log-max-size`).

### 6.3 Audit Non-Fatality

Audit log write failure (permissions, disk full) → `Warning:` on stderr → execution continues. Exit code is not affected by log failures. Consistent with ENG-3.7 (non-critical errors must not abort primary operation).

### 6.4 Concurrent Write Limitation (C-P4-J5-006)

Two simultaneous `aa-jury-gate --output append` invocations on the **same synthesis file** are not supported. Both processes read the file, compute independently, and `os.replace()` the last writer wins. This is a **known limitation** for v1:
- Document: "Do not run concurrent gate invocations on the same synthesis file."
- v2: advisory lock via `fcntl.flock()` or per-invocation temp output path.

---

## 7. Testing Architecture (ENG-4.4)

### 7.1 Test Layer Strategy

| Layer | Tool | Covers | Isolation |
|-------|------|--------|-----------|
| Unit | `pytest` | Each check function independently | StubGitProbe, tmp files |
| Integration | `pytest` + `CliRunner` | Full CLI invocations (all 26 BDD scenarios) | StubGitProbe, tmp files |
| Security | `pytest` | Symlink refusal, size cap, path traversal | tmp dirs with symlinks |
| Smoke | `pytest` (`tests/test_smoke.py`) | Real subprocess git integration (C-P4-J2-006) | Real git repo via tmp_path fixture |

**Smoke test spec (C-P4-J1-005, C-P4-J2-006, C-P4-J3-005):**
- File: `tests/test_smoke.py` — part of the default `pytest` run
- Fixture: `tmp_path`-based real git repo via `subprocess.run(["git", "init", ...])` (same as `valid_synthesis` fixture)
- Minimum 3 smoke scenarios invoked via `subprocess.run(["aa-jury-gate", ...])` (not CliRunner):
  1. Valid committed synthesis → exit 0, stdout contains "GATE: PASS"
  2. Valid synthesis with uncommitted changes → exit 1, stdout contains "G01    FAIL"
  3. Nonexistent path → exit 2, stderr contains "Error: synthesis file not found"
- CI: `pytest tests/test_smoke.py` runs in a separate CI job step after unit/integration; **CI-blocking**

### 7.2 Fixture Strategy

```python
@pytest.fixture
def valid_synthesis(tmp_path) -> Path:
    """Well-formed synthesis fixture that passes all 14 checks."""
    content = VALID_SYNTHESIS_TEMPLATE
    p = tmp_path / "phase-N-synthesis.md"
    p.write_text(content)
    # initialise a git repo so G01 can PASS
    subprocess.run(["git", "init", str(tmp_path)], check=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=tmp_path, check=True)
    return p
```

---

## 8. Phase 4 Design Summary

| Decision | ADR | Status |
|---------|-----|--------|
| Click >= 8.1 as CLI framework | ADR-001 | ACCEPTED |
| content_sha256 post-strip (UTF-8 canonical formula) | ADR-002 | ACCEPTED |
| write-on-exit-1 for --output append | ADR-003 | ACCEPTED |
| Constructor DI only, no framework | ADR-004 | ACCEPTED |
| extractor.py public API (parse + strip_jury_gate) | §2.1 | Defined |
| security.py public API (validate_synthesis_path, validate_log_dir) | §2.2 | Defined |
| GitProbe Protocol (ENG-2.5) | §2.3 | Defined |
| 9-threat security model | §3 | Defined |
| Module decomposition (11 modules) | §1 | Defined |
| Fast-fail vs. collect-all strategy | §5.1 | Defined |
| Exception hierarchy (ToolError, GitBinaryNotFoundError, GitProbeError) | §5.2 | Defined |
| GateVerdict.exit_code property (0/1/2) | §5.3 | Defined |
| Audit log schema + serialization contract | §6 | Defined |
| Concurrent write limitation (v1 known gap) | §6.4 | Documented |
| Test layer strategy (unit/integration/security/smoke) | §7 | Defined |
| Packaging (pyproject.toml, pipx, Python 3.10+) | §9 | Defined |

---

## 9. Packaging and Distribution (C-P4-J1-009, C-P4-J3-006)

### 9.1 pyproject.toml Structure

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "aa-jury-gate"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "click>=8.1",
    "PyYAML>=6.0",
]

[project.scripts]
aa-jury-gate = "aa_jury_gate.cli:main"

[project.optional-dependencies]
dev = ["pytest>=7.0", "pytest-cov"]
```

### 9.2 Version Source of Truth

Single-source version in `pyproject.toml`. Runtime access via `importlib.metadata.version("aa-jury-gate")`. No `__version__` hardcoded in source files.

### 9.3 Installation Methods (v1)

| Method | Command | Use case |
|--------|---------|---------|
| Development | `pip install -e .` | Constitution repo contributors |
| Isolated install | `pipx install .` | Operator workstations (recommended) |
| CI | `pip install -e .` or `pip install aa-jury-gate` (if AA internal PyPI available) | Pipeline automation |

### 9.4 Distribution

- v1: `pip install -e .` from constitution repo clone (editable install). AA internal PyPI publication is aspirational, pending registry availability (v1.1+). (C-P4-J3-006-R2)
- Package name: `aa-jury-gate`; import name: `aa_jury_gate`
- Entry point: `aa-jury-gate` CLI command (registered via `[project.scripts]`)
- No container image in v1 scope
