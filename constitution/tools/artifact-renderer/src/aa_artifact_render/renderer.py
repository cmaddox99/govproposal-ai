"""
renderer.py — HTML rendering engine for Hangar AI Constitution governance artifacts.

Converts a ParsedArtifact into a self-contained HTML document using:
- AA constitutional design system (docs-common.css tokens embedded)
- Per-artifact-type Jinja2 templates (proposal, tasks, adr, evidence, spec, skill, generic)
- Interactive law citation tooltips (resolved via CitationResolver)
- Print-ready page layout (@page rules, gradient bar, ✈ watermark)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown_it import MarkdownIt

from aa_artifact_render.citation_resolver import CitationResolver
from aa_artifact_render.parser import ParsedArtifact

_TEMPLATES_DIR = Path(__file__).parent / "templates"

_md = MarkdownIt("commonmark", {"html": True}).enable("table")

_CITATION_IN_HTML_RE = re.compile(
    r"(?<![='\"-])(?<!\w)\b([A-Z]{2,3}-\d+\.\d+)\b(?![^<]*?>)"
)

_CHECKBOX_DONE_RE    = re.compile(r'<li>\s*\[x\]\s*', re.IGNORECASE)
_CHECKBOX_PENDING_RE = re.compile(r'<li>\s*\[ \]\s*')
_KNOWN_TYPES = {"proposal", "tasks", "adr", "evidence", "spec", "skill", "generic", "discovery", "avatar"}


def render(
    artifact: ParsedArtifact,
    resolver: CitationResolver,
    artifact_type: str = "generic",
    theme: str = "print",
    tooltip_depth: str = "brief",
) -> str:
    """
    Render a ParsedArtifact to a self-contained HTML string.

    Args:
        artifact:      Parsed governance artifact (frontmatter + body + citations).
        resolver:      CitationResolver instance for tooltip metadata.
        artifact_type: One of proposal|tasks|adr|evidence|spec|skill|generic.
        theme:         'print' (page layout) or 'light' (screen-optimised).
        tooltip_depth: 'brief' (title only) or 'full' (title + summary).

    Returns:
        Complete self-contained HTML5 document as a string.
    """
    if artifact_type not in _KNOWN_TYPES:
        artifact_type = "generic"

    html_body = _render_markdown(artifact.body)
    html_body = _style_checkboxes(html_body)
    html_body = _inject_citation_tooltips(html_body, resolver, tooltip_depth)

    env = Environment(
        loader=FileSystemLoader(str(_TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
    )
    template_name = f"{artifact_type}.html"
    if not (_TEMPLATES_DIR / template_name).exists():
        template_name = "generic.html"

    tmpl = env.get_template(template_name)
    return tmpl.render(
        frontmatter=artifact.frontmatter,
        body=html_body,
        artifact_type=artifact_type,
        theme=theme,
        tooltip_depth=tooltip_depth,
    )


def _style_checkboxes(html: str) -> str:
    """Convert markdown-rendered checkboxes into styled task-done/task-pending divs."""
    def _wrap(cls: str, m: re.Match) -> str:
        return f'<li><div class="{cls}"><div class="cb"></div><div class="task-text">'

    html = _CHECKBOX_DONE_RE.sub(lambda m: _wrap("task-done", m), html)
    html = _CHECKBOX_PENDING_RE.sub(lambda m: _wrap("task-pending", m), html)
    # Close the two inner divs before each </li> that follows an opened task div
    html = re.sub(
        r'(<div class="task-(?:done|pending)">.*?)(</li>)',
        r'\1</div></div>\2',
        html,
        flags=re.DOTALL,
    )
    return html


def _render_markdown(body: str) -> str:
    """Convert markdown body to HTML."""
    return _md.render(body)


def _inject_citation_tooltips(
    html: str,
    resolver: CitationResolver,
    tooltip_depth: str,
) -> str:
    """
    Replace bare law citation text in HTML prose with tooltip-enabled spans.
    Skips content inside <code>, <pre> elements and HTML tag attributes.
    """
    # Split on <code>/<pre> blocks to protect them from replacement
    segments = _split_on_code_blocks(html)
    result = []
    for text, is_code in segments:
        if is_code:
            result.append(text)
        else:
            result.append(_replace_citations_in_segment(text, resolver, tooltip_depth))
    return "".join(result)


def _split_on_code_blocks(html: str) -> list[tuple[str, bool]]:
    """Split HTML into (segment, is_code) pairs around <code> and <pre> blocks."""
    pattern = re.compile(r"(<(?:pre|code)[^>]*>.*?</(?:pre|code)>)", re.DOTALL | re.IGNORECASE)
    parts = pattern.split(html)
    segments = []
    for i, part in enumerate(parts):
        is_code = i % 2 == 1
        segments.append((part, is_code))
    return segments


def _replace_citations_in_segment(text: str, resolver: CitationResolver, tooltip_depth: str) -> str:
    """Replace citation patterns in a non-code HTML segment with tooltip spans."""
    def replacer(m: re.Match) -> str:
        law_id = m.group(1)
        resolved = resolver.resolve(law_id)
        if not resolved.found:
            return m.group(0)

        nn_attr = 'data-non-negotiable="true"' if resolved.non_negotiable else 'data-non-negotiable="false"'
        nn_label = " · <em>NON-NEGOTIABLE</em>" if resolved.non_negotiable else ""

        if tooltip_depth == "full":
            tooltip_body = (
                f"<strong>{resolved.title}</strong>{nn_label}"
                f"<br><span class=\"law-summary\">{resolved.summary}</span>"
            )
        else:
            tooltip_body = f"<strong>{resolved.title}</strong>{nn_label}"

        return (
            f'<span class="law-cite" data-law-id="{law_id}" {nn_attr}>'
            f"{law_id}"
            f'<span class="law-tooltip">{tooltip_body}</span>'
            f"</span>"
        )

    return _CITATION_IN_HTML_RE.sub(replacer, text)
