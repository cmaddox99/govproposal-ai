"""cli.py — Presentation layer / DI host for aa-citation-audit.

ADR-001: cli.py is the dependency injection host. It calls registry → scanner → auditor
in sequence. Lower modules do NOT call each other.

Validation order (ENG-6.5): Surface 1 → 2 → 3 → 4 → scan → output.
Exit 2 on any validation or tool failure; stdout clean on exit 2 (ENG-6.1).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import click
import yaml

from citation_auditor import __version__
from citation_auditor.auditor import audit
from citation_auditor.exceptions import AuditError, RegistryLoadError
from citation_auditor.models import Verdict
from citation_auditor.registry import load_registry
from citation_auditor.scanner import scan_artifact

# Law ID pattern for --allow-draft validation
_DRAFT_ID_RE = re.compile(r"^[A-Z]+-\d+\.\d+$")

# Allowed artifact file extensions (Surface 1 guard)
_ALLOWED_SUFFIXES = {".md", ".html", ".htm"}

# Audit log directory (can be overridden by env var for testing)
_DEFAULT_LOG_DIR = Path.home() / ".aa-citation-audit"

_TOOL_VERSION = __version__

# Column widths for stdout table
_COL_ID = 12
_COL_VERDICT = 8


def _log_dir() -> Path:
    """Return audit log directory (AA_AUDIT_LOG_DIR env var overrides for testing)."""
    override = os.environ.get("AA_AUDIT_LOG_DIR")
    return Path(override) if override else _DEFAULT_LOG_DIR


def _err(msg: str) -> None:
    """Print error to stderr only (stdout stays clean per ENG-6.1)."""
    click.echo(f"Error: {msg}", err=True)


def _exit2(msg: str) -> None:
    """Print error to stderr and exit 2."""
    _err(msg)
    sys.exit(2)


def _parse_allow_draft(raw: str) -> list[str]:
    """Parse comma-separated allow-draft IDs; raises ValueError on invalid format."""
    if not raw.strip():
        return []
    ids = [x.strip() for x in raw.split(",")]
    for law_id in ids:
        if not _DRAFT_ID_RE.match(law_id):
            raise ValueError(f"Invalid --allow-draft ID format: '{law_id}' "
                             f"(expected [A-Z]+-N.N)")
    return ids


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _write_audit_log(artifact_path: Path, result) -> None:
    """Append one JSON line to audit.log (BUS-7.1)."""
    log_dir = _log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "artifact": str(artifact_path.resolve()),
        "fail_count": result.fail_count,
        "warn_count": result.warn_count,
        "pass_count": result.pass_count,
        "tool_version": _TOOL_VERSION,
        "timestamp": result.timestamp,
        "sha256_artifact": _sha256(artifact_path),
    }
    with open(log_dir / "audit.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def _write_audit_log_error(artifact_path: str, error_type: str, message: str) -> None:
    """Append tool_error event to audit.log (Phase 4 §5)."""
    try:
        log_dir = _log_dir()
        log_dir.mkdir(parents=True, exist_ok=True)
        record = {
            "event": "citation_audit.tool_error",
            "artifact": artifact_path,
            "error_type": error_type,
            "message": message,
            "timestamp": _timestamp(),
        }
        with open(log_dir / "audit.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except OSError:
        pass  # log failure is non-fatal


def _print_table(result, use_ansi: bool = False) -> None:
    """Print audit results table to stdout."""
    click.echo(f"aa-citation-audit v{_TOOL_VERSION}")
    click.echo(f"Artifact: {result.artifact_path}")
    click.echo(f"Registry: {result.registry_path} ({result.law_count} laws loaded)")
    click.echo("")

    header = f"{'ID':<{_COL_ID}}  {'Verdict':<{_COL_VERDICT}}  Note"
    sep = f"{'-' * _COL_ID}  {'-' * _COL_VERDICT}  {'-' * 47}"
    click.echo(header)
    click.echo(sep)

    for r in result.results:
        note = r.note or ""
        if use_ansi:
            if r.verdict == Verdict.FAIL:
                verdict_str = click.style("FAIL", fg="red", bold=True)
            elif r.verdict == Verdict.WARN:
                verdict_str = click.style("WARN", fg="yellow")
            else:
                verdict_str = click.style("PASS", fg="green")
        else:
            verdict_str = r.verdict.value
        click.echo(f"{r.law_id:<{_COL_ID}}  {verdict_str:<{_COL_VERDICT}}  {note}")

    for draft_id in result.draft_skipped:
        if use_ansi:
            verdict_str = click.style("SKIP", fg="cyan")
        else:
            verdict_str = "SKIP"
        click.echo(f"{draft_id:<{_COL_ID}}  {verdict_str:<{_COL_VERDICT}}  draft — not evaluated")

    click.echo("")
    click.echo(
        f"Summary: {result.scanned} citations scanned | "
        f"{result.fail_count} FAIL | {result.warn_count} WARN | {result.pass_count} PASS"
    )
    click.echo(f"Exit: {result.audit_exit_code}")


def _build_citation_audit_block(result, laws_dir: Path) -> dict:
    """Build citation_audit YAML dict for --output append."""
    index_path = str((laws_dir / "index.yaml").resolve())
    return {
        "citation_audit": {
            "tool": "aa-citation-audit",
            "version": _TOOL_VERSION,
            "timestamp": result.timestamp,
            "registry": index_path,
            "law_count": result.law_count,
            "scanned": result.scanned,
            "draft_skipped": result.draft_skipped,
            "fail_count": result.fail_count,
            "warn_count": result.warn_count,
            "pass_count": result.pass_count,
            "exit_code": result.audit_exit_code,
            "allow_draft": result.allow_draft,
            "strict": result.strict,
            "verdicts": [
                {
                    "id": r.law_id,
                    "verdict": r.verdict.value,
                    **({"note": r.note} if r.note else {}),
                    "context_snippet": r.context_snippet,
                }
                for r in result.results
            ],
        }
    }


def _write_append(artifact_path: Path, result, laws_dir: Path) -> None:
    """Atomically write citation_audit block to artifact frontmatter (T-06)."""
    text = artifact_path.read_text(encoding="utf-8", errors="replace")
    block = _build_citation_audit_block(result, laws_dir)
    block_yaml = yaml.dump(block, default_flow_style=False, allow_unicode=True)

    has_frontmatter = text.startswith("---")

    if has_frontmatter:
        # Find the closing ---
        end = text.find("\n---", 3)
        if end == -1:
            # Malformed: treat as no frontmatter
            new_text = f"---\n{block_yaml}---\n\n{text}"
        else:
            fm_text = text[3:end]  # existing frontmatter content
            # Parse existing frontmatter and remove stale citation_audit key
            try:
                fm_data = yaml.safe_load(fm_text) or {}
            except yaml.YAMLError:
                fm_data = {}
            fm_data.pop("citation_audit", None)
            fm_data.update(block)
            new_fm = yaml.dump(fm_data, default_flow_style=False, allow_unicode=True)
            rest = text[end + 4:]  # skip \n---
            new_text = f"---\n{new_fm}---\n{rest}"
    else:
        new_text = f"---\n{block_yaml}---\n\n{text}"

    # Atomic write (T-06): temp file in same directory → os.replace
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=artifact_path.parent,
        delete=False, suffix=".tmp"
    ) as tmp:
        tmp.write(new_text)
        tmp_path = tmp.name

    os.replace(tmp_path, artifact_path)


@click.command()
@click.argument("artifact", type=click.Path(exists=False))
@click.option("--laws-dir", default="laws", type=click.Path(), show_default=True)
@click.option("--allow-draft", "allow_draft_raw", default="", type=str,
              help="Comma-separated draft law IDs to skip.")
@click.option("--strict", is_flag=True, default=False,
              help="Exit 1 if any WARN exists.")
@click.option("--output", type=click.Choice(["stdout", "append", "console"]),
              default="stdout", show_default=True)
@click.version_option(version=_TOOL_VERSION, prog_name="aa-citation-audit")
def main(artifact: str, laws_dir: str, allow_draft_raw: str,
         strict: bool, output: str) -> None:
    """Audit law citation IDs in a Hangar AI Constitution artifact."""

    # ── Surface 1: artifact validation ──────────────────────────────────────
    artifact_path = Path(artifact)
    if not artifact_path.exists():
        _exit2(f"Artifact not found: {artifact}")
    if not artifact_path.is_file():
        _exit2(f"Artifact is not a regular file: {artifact}")
    if artifact_path.suffix.lower() not in _ALLOWED_SUFFIXES:
        _exit2(f"Artifact must have .md, .html, or .htm extension: {artifact}")

    # ── Surface 2: laws-dir validation ──────────────────────────────────────
    laws_path = Path(laws_dir)
    index_yaml = laws_path / "index.yaml"
    if not laws_path.is_dir():
        _exit2(f"Laws directory not found: {laws_dir}")
    if not index_yaml.exists():
        _exit2(f"index.yaml not found in laws directory: {laws_dir}")

    # ── Surface 3: --allow-draft validation ─────────────────────────────────
    try:
        allow_draft = _parse_allow_draft(allow_draft_raw)
    except ValueError as exc:
        _exit2(str(exc))
        return  # unreachable, satisfies type checker

    # ── Surface 4 (write-time): checked before scan for append mode ─────────
    if output == "append":
        try:
            with open(artifact_path, "a"):
                pass
        except OSError as exc:
            _exit2(f"Cannot write to artifact: {exc}")
            return

    # ── Load registry ────────────────────────────────────────────────────────
    try:
        registry = load_registry(laws_path)
    except RegistryLoadError as exc:
        _write_audit_log_error(str(artifact_path), "RegistryLoadError", str(exc))
        _exit2(f"Registry load failed: {exc}")
        return

    # ── Scan artifact ────────────────────────────────────────────────────────
    try:
        citations, draft_skipped = scan_artifact(artifact_path, registry, allow_draft)
    except AuditError as exc:
        _write_audit_log_error(str(artifact_path), "AuditError", str(exc))
        _exit2(f"Scan failed: {exc}")
        return

    # ── Audit (verdict logic) ────────────────────────────────────────────────
    try:
        result = audit(
            citations=citations,
            registry=registry,
            artifact_path=str(artifact_path),
            registry_path=str(index_yaml),
            law_count=len(registry),
            draft_skipped=draft_skipped,
            allow_draft=allow_draft,
            strict=strict,
            timestamp=_timestamp(),
            tool_version=_TOOL_VERSION,
        )
    except AuditError as exc:
        _write_audit_log_error(str(artifact_path), "AuditError", str(exc))
        _exit2(f"Audit failed: {exc}")
        return

    # ── Output ───────────────────────────────────────────────────────────────
    _print_table(result, use_ansi=(output == "console"))

    if output == "append":
        try:
            _write_append(artifact_path, result, laws_path)
        except OSError as exc:
            _write_audit_log_error(str(artifact_path), "WriteError", str(exc))
            _exit2(f"Failed to write citation_audit block: {exc}")
            return
        click.echo("[written: citation_audit block]")

    # ── BUS-7.1 audit log ───────────────────────────────────────────────────
    try:
        _write_audit_log(artifact_path, result)
    except OSError:
        pass  # audit log write failure is non-fatal

    sys.exit(result.audit_exit_code)
