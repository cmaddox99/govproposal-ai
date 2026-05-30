"""
pdf_exporter.py — Headless Chromium PDF generator for aa-artifact-render.

Uses Playwright's sync API to render a self-contained HTML file through
headless Chromium and produce a print-quality PDF with the AA design system
page dimensions (1088 × 1408 px, matching the @page CSS rules in _base.html).

Usage:
    from aa_artifact_render.pdf_exporter import export_pdf
    export_pdf(Path("PROPOSAL.html"), Path("PROPOSAL.pdf"))

Prerequisites:
    playwright install chromium
"""
from __future__ import annotations

from pathlib import Path


def export_pdf(html_path: Path | str, pdf_path: Path | str) -> None:
    """
    Render *html_path* through headless Chromium and write the result to *pdf_path*.

    Args:
        html_path: Path to the self-contained HTML file to convert.
        pdf_path:  Destination path for the generated PDF.

    Raises:
        FileNotFoundError: If *html_path* does not exist.
        RuntimeError:      If Playwright / Chromium is not installed.
        OSError:           If *pdf_path* cannot be written.
    """
    html_path = Path(html_path)
    pdf_path = Path(pdf_path)

    if not html_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_path}")

    try:
        from playwright.sync_api import sync_playwright  # noqa: PLC0415
    except ImportError as exc:
        raise RuntimeError(
            "PDF export requires Playwright. Install it with:\n"
            "  pip install playwright\n"
            "  playwright install chromium"
        ) from exc

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(
                "Chromium is not installed. Run:\n"
                "  playwright install chromium"
            ) from exc

        page = browser.new_page()
        page.goto(f"file://{html_path.resolve()}", wait_until="networkidle")

        page.pdf(
            path=str(pdf_path),
            print_background=True,
            # Match the @page dimensions from _base.html (1088px × 1408px at 96dpi = 8.5" × 11")
            width="8.5in",
            height="11in",
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )

        browser.close()
