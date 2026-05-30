"""Tests for pdf_exporter.py (Phase 6 — RED)."""
from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

# This import will fail until pdf_exporter.py is created — RED phase.
from aa_artifact_render.pdf_exporter import export_pdf

SAMPLE_HTML = textwrap.dedent("""\
    <!DOCTYPE html>
    <html lang="en">
    <head><meta charset="utf-8"><title>Test</title></head>
    <body><h1>Test PDF Export</h1><p>Content here.</p></body>
    </html>
""")


@pytest.fixture()
def html_file(tmp_path):
    f = tmp_path / "test.html"
    f.write_text(SAMPLE_HTML)
    return f


# ---------------------------------------------------------------------------
# 6.1a — PDF file is created
# ---------------------------------------------------------------------------
def test_pdf_file_created(html_file, tmp_path):
    pdf_path = tmp_path / "out.pdf"
    export_pdf(html_file, pdf_path)
    assert pdf_path.exists()


# ---------------------------------------------------------------------------
# 6.1b — PDF file size > 0
# ---------------------------------------------------------------------------
def test_pdf_file_nonempty(html_file, tmp_path):
    pdf_path = tmp_path / "out.pdf"
    export_pdf(html_file, pdf_path)
    assert pdf_path.stat().st_size > 0


# ---------------------------------------------------------------------------
# 6.1c — PDF starts with PDF magic bytes
# ---------------------------------------------------------------------------
def test_pdf_magic_bytes(html_file, tmp_path):
    pdf_path = tmp_path / "out.pdf"
    export_pdf(html_file, pdf_path)
    header = pdf_path.read_bytes()[:4]
    assert header == b"%PDF", f"Expected PDF header, got {header!r}"


# ---------------------------------------------------------------------------
# 6.1d — Missing HTML file raises clear error (not an obscure crash)
# ---------------------------------------------------------------------------
def test_missing_html_raises_file_not_found(tmp_path):
    missing = tmp_path / "ghost.html"
    pdf_path = tmp_path / "out.pdf"
    with pytest.raises((FileNotFoundError, RuntimeError, OSError)):
        export_pdf(missing, pdf_path)


# ---------------------------------------------------------------------------
# 6.1e — Accepts Path objects (not just strings)
# ---------------------------------------------------------------------------
def test_accepts_path_objects(html_file, tmp_path):
    pdf_path = tmp_path / "path_test.pdf"
    # Should not raise a TypeError
    export_pdf(Path(html_file), Path(pdf_path))
    assert pdf_path.exists()
