"""Gate runner orchestrating all checks."""
from pathlib import Path

from aa_jury_gate.checks import body, git, schema
from aa_jury_gate.extractor import _extract_fm_text, parse, strip_jury_gate
from aa_jury_gate.git_probe import GitProbe
from aa_jury_gate.models import CheckItem, CheckResult, GateResult, GateVerdict, ToolError


class GateRunner:
    """Orchestrates all checks in order per Phase 3 §1 specification."""

    def __init__(self, git_probe: GitProbe) -> None:
        """Initialize with injected git probe (only DI seam per ADR-004)."""
        self.git_probe = git_probe

    def run(self, path: Path, allow_no_git: bool) -> GateResult:  # noqa: C901, PLR0912, PLR0915
        """Run all checks and return aggregated result.

        Execution order (Phase 3 §1.2):
        1. S01-S02: file existence, extension
        2. S03-S04: YAML parsing, frontmatter dict (fast-fail)
        3. S05-S11: schema checks (collect all FAILs)
        4. B01-B03: body checks (skip if S11 FAIL)
        5. G01: git probe (always run)

        Returns GateResult with verdict:
        - ERROR: ToolError or unreadable file (exit 2)
        - FAIL: any check FAIL (exit 1)
        - PASS: all checks PASS or SKIP (exit 0)
        """
        checks: list[CheckItem] = []

        # S01: file existence + is_file
        checks.append(schema.check_s01(path))
        if checks[-1].result == CheckResult.FAIL:
            # Can't proceed if file doesn't exist
            return GateResult(
                verdict=GateVerdict.FAIL,
                checks=checks,
                content_sha256="",
            )

        # S02: extension check
        checks.append(schema.check_s02(path))
        if checks[-1].result == CheckResult.FAIL:
            return GateResult(
                verdict=GateVerdict.FAIL,
                checks=checks,
                content_sha256="",
            )

        # Read content for SHA256
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as exc:
            raise ToolError(f"unexpected error reading {path}: {exc}") from exc

        # Extract frontmatter text (not yet parsed)
        try:
            fm_text, body_text = _extract_fm_text(path)
        except Exception as exc:
            raise ToolError(f"unexpected error extracting frontmatter: {exc}") from exc

        if fm_text is None:
            # No frontmatter present - S03 should FAIL
            checks.append(
                CheckItem("S03", CheckResult.FAIL, "no frontmatter found (missing opening ---)")
            )
            return GateResult(
                verdict=GateVerdict.FAIL,
                checks=checks,
                content_sha256=_compute_sha256(content),
            )

        # S03: valid YAML (raises ToolError on parse failure → exit 2)
        checks.append(schema.check_s03(fm_text))

        # Parse frontmatter to dict
        try:
            fm, body_text = parse(path)
        except ToolError:
            raise
        except Exception as exc:
            raise ToolError(f"unexpected error parsing {path}: {exc}") from exc

        # S04: frontmatter is dict
        checks.append(schema.check_s04(fm))
        if checks[-1].result == CheckResult.FAIL:
            return GateResult(
                verdict=GateVerdict.FAIL,
                checks=checks,
                content_sha256=_compute_sha256(content),
            )

        # S05-S11: collect all results (no fast-fail)
        checks.append(schema.check_s05(fm))
        checks.append(schema.check_s06(fm))
        checks.append(schema.check_s07(fm))
        checks.append(schema.check_s08a(fm))
        checks.append(schema.check_s08b(fm))
        checks.append(schema.check_s09(fm))
        checks.append(schema.check_s10(fm))
        checks.append(schema.check_s11(fm))

        # B01-B03: skip if S11 FAIL (Phase 3 §3.3)
        s11_failed = any(c.check_id == "S11" and c.result == CheckResult.FAIL for c in checks)
        if s11_failed:
            for check_id in ["B01", "B02", "B03"]:
                checks.append(
                    CheckItem(check_id=check_id, result=CheckResult.SKIP, detail="S11 FAIL")
                )
        else:
            checks.append(body.check_b01(body_text))
            checks.append(body.check_b02(body_text))
            checks.append(body.check_b03(body_text))

        # G01: git probe (always run)
        try:
            checks.append(git.check_g01(self.git_probe, path, allow_no_git=allow_no_git))
        except ToolError:
            raise  # GitBinaryNotFoundError with allow_no_git=False → exit 2

        # Compute verdict
        any_fail = any(c.result == CheckResult.FAIL for c in checks)
        verdict = GateVerdict.FAIL if any_fail else GateVerdict.PASS

        return GateResult(
            verdict=verdict,
            checks=checks,
            content_sha256=_compute_sha256(content),
        )


def _compute_sha256(content: str) -> str:
    """Compute SHA256 hex digest after stripping jury_gate block (Phase 3 §5.3)."""
    import hashlib

    # Strip prior jury_gate block for idempotent hashing
    stripped = strip_jury_gate(content)
    return hashlib.sha256(stripped.encode("utf-8")).hexdigest()
