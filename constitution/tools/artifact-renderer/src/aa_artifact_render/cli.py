"""CLI entry point for aa-artifact-render."""
from __future__ import annotations

import sys
from importlib.metadata import PackageNotFoundError, version as _pkg_version
from pathlib import Path

import click

from .citation_resolver import CitationResolver
from .diagnose import collect as _diagnose_collect, format_text as _diagnose_format, has_drift as _diagnose_has_drift
from .parser import parse_artifact
from .renderer import render

_VALID_TYPES = {"proposal", "tasks", "adr", "evidence", "spec", "skill", "generic", "discovery", "avatar"}
_DISCOVERY_STAGES = {"A", "B", "C", "D", "E", "F"}


def _resolve_artifact_type(frontmatter: dict, cli_override: str | None) -> str:
    """Resolve the artifact type. Precedence (highest first):

    1. --artifact-type CLI flag
    2. Explicit `type:` in frontmatter
    3. Legacy `artifact:` in frontmatter
    4. Auto-detect: workflow contains 'product-discovery' AND stage in {A..F}
    5. Fallback to 'generic'
    """
    if cli_override:
        return cli_override
    explicit = frontmatter.get("type") or frontmatter.get("artifact")
    if explicit:
        return str(explicit)
    workflow = str(frontmatter.get("workflow", "")).lower()
    stage = str(frontmatter.get("stage", "")).strip().upper()
    if "product-discovery" in workflow and stage in _DISCOVERY_STAGES:
        return "discovery"
    return "generic"


def _installed_version() -> str:
    try:
        return _pkg_version("aa-artifact-render")
    except PackageNotFoundError:
        return "unknown"


@click.command()
@click.argument("artifact", type=click.Path(exists=False), required=False)
@click.option(
    "--diagnose",
    is_flag=True,
    default=False,
    help="Print install + source diagnostic and exit. Exits 3 if drift detected.",
)
@click.option("--output", "-o", default=None, help="Output HTML path (default: <artifact>.html)")
@click.option("--pdf", is_flag=True, default=False, help="Also generate a PDF alongside the HTML")
@click.option("--pdf-only", is_flag=True, default=False, help="Generate PDF only (no HTML output file kept)")
@click.option("--pdf-output", default=None, help="Output PDF path (default: <artifact>.pdf)")
@click.option(
    "--artifact-type",
    default=None,
    help="Override artifact type (proposal|tasks|adr|evidence|spec|skill|generic)",
)
@click.option(
    "--laws-dir",
    default=None,
    help="Path to the constitution laws/ directory (auto-detected if omitted)",
)
@click.option("--quiet", "-q", is_flag=True, default=False, help="Suppress output on success")
@click.option("--tooltip-depth", default="full", hidden=True, help="Tooltip detail level")
@click.option("--theme", default="default", hidden=True, help="Visual theme (reserved)")
def main(
    artifact: str | None,
    diagnose: bool,
    output: str | None,
    pdf: bool,
    pdf_only: bool,
    pdf_output: str | None,
    artifact_type: str | None,
    laws_dir: str | None,
    quiet: bool,
    tooltip_depth: str,
    theme: str,
) -> None:
    """Render a Hangar AI Constitution governance artifact as self-contained HTML.

    ARTIFACT is the path to a markdown governance artifact (.md file).
    """
    # ── --diagnose short-circuit ────────────────────────────────────────────
    if diagnose:
        snapshot = _diagnose_collect()
        if not quiet:
            click.echo(_diagnose_format(snapshot))
        sys.exit(3 if _diagnose_has_drift(snapshot) else 0)

    # ── input validation ────────────────────────────────────────────────────
    if not artifact:
        click.echo("Error: ARTIFACT path is required (or pass --diagnose).", err=True)
        sys.exit(1)
    artifact_path = Path(artifact)
    if not artifact_path.exists():
        click.echo(f"Error: File not found: {artifact}", err=True)
        sys.exit(1)

    if laws_dir is not None:
        laws_path = Path(laws_dir)
        if not laws_path.exists():
            click.echo(f"Error: --laws-dir path not found: {laws_dir}", err=True)
            sys.exit(1)
    else:
        laws_path = None  # CitationResolver auto-detects

    # ── validate artifact-type if given ─────────────────────────────────────
    if artifact_type is not None and artifact_type not in _VALID_TYPES:
        click.echo(
            f"Error: Unknown --artifact-type '{artifact_type}'. "
            f"Valid types: {', '.join(sorted(_VALID_TYPES))}",
            err=True,
        )
        sys.exit(2)

    # ── determine output paths ───────────────────────────────────────────────
    html_out = Path(output) if output else artifact_path.with_suffix(".html")
    if html_out.parent and not html_out.parent.exists():
        click.echo(f"Error: Output directory does not exist: {html_out.parent}", err=True)
        sys.exit(1)

    # When --pdf-only, use a temp file for the intermediate HTML
    import tempfile  # noqa: PLC0415
    _tmp_html = None
    if pdf_only and not output:
        fd, tmp = tempfile.mkstemp(suffix=".html")
        import os  # noqa: PLC0415
        os.close(fd)
        html_out = Path(tmp)
        _tmp_html = html_out

    # ── parse ────────────────────────────────────────────────────────────────
    source = artifact_path.read_text(encoding="utf-8")
    parsed = parse_artifact(source)

    # Resolve artifact type — flag > explicit frontmatter > auto-detect > generic
    resolved_type = _resolve_artifact_type(parsed.frontmatter, artifact_type)
    parsed.frontmatter["type"] = resolved_type

    # ── resolve citations ────────────────────────────────────────────────────
    resolver = CitationResolver(laws_dir=laws_path)
    resolved_map = {}
    for citation in parsed.citations:
        if citation.law_id not in resolved_map:
            resolved_map[citation.law_id] = resolver.resolve(citation.law_id)

    resolved_count = sum(1 for r in resolved_map.values() if r.found)
    unresolved_count = sum(1 for r in resolved_map.values() if not r.found)

    # ── render HTML ──────────────────────────────────────────────────────────
    html = render(parsed, resolver, artifact_type=resolved_type)
    html_out.write_text(html, encoding="utf-8")

    # ── optional PDF (--pdf or --pdf-only) ───────────────────────────────────
    if pdf or pdf_only:
        pdf_path = Path(pdf_output) if pdf_output else artifact_path.with_suffix(".pdf")
        try:
            from .pdf_exporter import export_pdf  # noqa: PLC0415

            export_pdf(html_out, pdf_path)
            if not quiet:
                click.echo(f"✓ PDF:      {pdf_path}")
        except ImportError as exc:
            click.echo(f"Error: PDF export requires playwright. {exc}", err=True)
            sys.exit(1)
        finally:
            # Clean up temp HTML when using --pdf-only
            if _tmp_html and _tmp_html.exists():
                _tmp_html.unlink()

    # ── success message ───────────────────────────────────────────────────────
    if not quiet and not pdf_only:
        click.echo(
            f"✓ Rendered: {html_out} "
            f"[{resolved_count} citation{'s' if resolved_count != 1 else ''} resolved"
            f", {unresolved_count} unresolved]"
        )
        click.echo(
            f"  aa-artifact-render v{_installed_version()} "
            f"· type={resolved_type}"
        )
