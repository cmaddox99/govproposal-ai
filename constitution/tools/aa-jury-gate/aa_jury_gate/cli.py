"""CLI entrypoint for aa-jury-gate."""
from __future__ import annotations

import sys
from pathlib import Path

import click

from aa_jury_gate import __version__
from aa_jury_gate.gate import GateRunner
from aa_jury_gate.git_probe import RealGitProbe
from aa_jury_gate.models import GateResult, GateVerdict, ToolError
from aa_jury_gate.output import append_gate_result
from aa_jury_gate.security import validate_synthesis_path


@click.command()
@click.argument("synthesis", type=click.Path(exists=False, path_type=Path))
@click.option(
    "--output",
    type=click.Choice(["append"]),
    help="Write jury_gate: block to synthesis file (only on PASS/FAIL)",
)
@click.option(
    "--log-dir",
    type=click.Path(file_okay=False, path_type=Path),
    help="Directory for audit logs (BUS-7.1 compliance)",
)
@click.option(
    "--allow-no-git/--no-allow-no-git",
    default=False,
    help="SKIP G01 if git unavailable (CI/CD support)",
)
@click.version_option()
def main(
    synthesis: Path,
    output: str | None,
    log_dir: Path | None,
    allow_no_git: bool,
) -> None:
    """Validate jury synthesis artifact per Hangar AI Constitution.

    SYNTHESIS: path to synthesis .md file (must be git-tracked + clean)

    Exit codes:
      0 = PASS (all checks pass or skip)
      1 = FAIL (one or more checks fail)
      2 = ERROR (invalid input, tool error, security violation)
    """
    try:
        # Security validation (single call site per C-P5-J4-R2-001)
        validate_synthesis_path(synthesis)

        # Validate log_dir if provided
        if log_dir is not None:
            from aa_jury_gate.security import validate_log_dir

            validate_log_dir(log_dir)

        # Run gate
        runner = GateRunner(git_probe=RealGitProbe())
        result = runner.run(synthesis, allow_no_git)

        # Print results (Phase 3 §1.4 format)
        _print_result(result, synthesis)

        # Compute SHA256 before any file modification (for audit integrity)
        content_sha256 = None
        if log_dir is not None and result.verdict in (GateVerdict.PASS, GateVerdict.FAIL):
            from aa_jury_gate.gate import _compute_sha256

            content = synthesis.read_text(encoding="utf-8")
            content_sha256 = _compute_sha256(content)

        # Write output if requested (only on PASS/FAIL, not ERROR)
        if output == "append" and result.verdict in (GateVerdict.PASS, GateVerdict.FAIL):
            append_gate_result(synthesis, result)

        # Write audit log if requested (BUS-7.1)
        if log_dir is not None and result.verdict in (GateVerdict.PASS, GateVerdict.FAIL):
            from aa_jury_gate.audit import write_audit_log

            # Count failed and skipped checks
            failed = sum(1 for c in result.checks if c.result.value == "FAIL")
            skipped = sum(1 for c in result.checks if c.result.value == "SKIP")

            try:
                write_audit_log(
                    log_dir=log_dir,
                    synthesis_path=synthesis,
                    verdict=result.verdict,
                    checks_failed=failed,
                    checks_skipped=skipped,
                    content_sha256=content_sha256,
                    tool_version=__version__,
                    exit_code=result.verdict.exit_code,
                )
            except Exception as e:
                # Audit logging failure should not crash gate execution
                click.echo(f"WARNING: Failed to write audit log: {e}", err=True)

        sys.exit(result.verdict.exit_code)

    except ToolError as exc:
        # Write audit log for ERROR verdict (J5-P8-003)
        if log_dir is not None:
            from aa_jury_gate.audit import write_audit_log

            try:
                write_audit_log(
                    log_dir=log_dir,
                    synthesis_path=synthesis,
                    verdict=GateVerdict.ERROR,
                    checks_failed=0,
                    checks_skipped=0,
                    content_sha256="",
                    tool_version=__version__,
                    exit_code=2,
                )
            except Exception as e:
                # Log ERROR audit failures to stderr (J5-P8R2-003)
                click.echo(f"WARNING: Failed to write ERROR audit log: {e}", err=True)

        # Exit 2 on tool errors (Phase 3 §1.3: empty or error-only stdout)
        click.echo(f"ERROR: {exc}", err=True)
        sys.exit(2)


def _print_result(result: GateResult, synthesis_path: Path) -> None:
    """Print check results in tabular format per Phase 3 §1.4."""
    if result.verdict == GateVerdict.ERROR:
        # Empty stdout on ERROR (Phase 3 §1.3 contract)
        return

    # Path banner
    click.echo(f"aa-jury-gate check results for: {synthesis_path}")
    click.echo("─" * 58)

    # Check table header
    click.echo(" CHECK  RESULT  DETAIL")

    # Checks
    for check in result.checks:
        detail = check.detail or ""
        click.echo(f" {check.check_id:5}  {check.result.value:6}  {detail}")

    # Final separator and summary
    click.echo("─" * 58)

    # Count failures
    failed_count = sum(1 for c in result.checks if c.result.value == "FAIL")

    # Gate summary
    if result.verdict == GateVerdict.PASS:
        click.echo("GATE: PASS")
    else:
        plural = "check" if failed_count == 1 else "checks"
        click.echo(f"GATE: FAIL  ({failed_count} {plural} failed)")
