"""Data models for aa-agents-sync."""
from dataclasses import dataclass, field


@dataclass
class MarkerSection:
    """A hangar-ai-constitution BEGIN/END bounded section found in an AGENTS.md."""

    name: str
    version: str
    content: str


@dataclass
class CheckResult:
    """Result of a check_drift call."""

    sections: list[MarkerSection] = field(default_factory=list)
    constitution_version: str = ""
    has_drift: bool = False
    has_markers: bool = False
    errors: list[str] = field(default_factory=list)
