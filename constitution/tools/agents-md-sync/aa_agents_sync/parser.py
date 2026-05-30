"""Marker parser for hangar-ai-constitution BEGIN/END sections."""
import re
from .models import MarkerSection

BEGIN_RE = re.compile(
    r"^<!-- BEGIN hangar-ai-constitution:([a-z][a-z0-9-]+) v(\d+\.\d+\.\d+) -->\r?$",
    re.MULTILINE,
)
END_RE = re.compile(
    r"^<!-- END hangar-ai-constitution:([a-z][a-z0-9-]+) -->\r?$",
    re.MULTILINE,
)

# MVP section name enum — only these names are valid (C5/C7)
VALID_SECTION_NAMES: frozenset[str] = frozenset({"mandatory-protocol"})


def parse_markers(content: str) -> tuple[list[MarkerSection], list[str]]:
    """Parse all BEGIN/END marker pairs from content.

    Returns (sections, errors) where errors lists any structural violations:
    - END name mismatch
    - Unclosed BEGIN
    """
    content = content.lstrip("\ufeff")  # strip UTF-8 BOM if present
    sections: list[MarkerSection] = []
    errors: list[str] = []
    lines = content.splitlines(keepends=True)

    open_name: str | None = None
    open_version: str | None = None
    open_lines: list[str] = []

    for line in lines:
        begin_match = BEGIN_RE.search(line)
        end_match = END_RE.search(line)

        if begin_match:
            if open_name is not None:
                errors.append(
                    f"Nested BEGIN for '{begin_match.group(1)}' "
                    f"inside unclosed '{open_name}'"
                )
            section_name = begin_match.group(1)
            if section_name not in VALID_SECTION_NAMES:
                errors.append(
                    f"Unknown section name '{section_name}'; "
                    f"valid names: {sorted(VALID_SECTION_NAMES)}"
                )
            open_name = section_name
            open_version = begin_match.group(2)
            open_lines = [line]
        elif end_match:
            end_name = end_match.group(1)
            if open_name is None:
                errors.append(f"END '{end_name}' without matching BEGIN")
            elif end_name != open_name:
                errors.append(
                    f"END name '{end_name}' does not match BEGIN name '{open_name}'"
                )
                open_name = None
                open_version = None
                open_lines = []
            else:
                open_lines.append(line)
                assert open_version is not None  # always set alongside open_name
                sections.append(
                    MarkerSection(
                        name=open_name,
                        version=open_version,
                        content="".join(open_lines),
                    )
                )
                open_name = None
                open_version = None
                open_lines = []
        elif open_name is not None:
            open_lines.append(line)

    if open_name is not None:
        errors.append(f"Unclosed BEGIN for '{open_name}'")

    return sections, errors
