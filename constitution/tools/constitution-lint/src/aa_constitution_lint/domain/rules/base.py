"""Base rule interface."""

from abc import ABC, abstractmethod
from pathlib import Path

from aa_constitution_lint.domain.models import LawEvaluation


class Rule(ABC):
    """Abstract base class for all constitution lint rules."""

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier for this rule."""
        ...

    @property
    @abstractmethod
    def law_id(self) -> str:
        """The constitutional law this rule enforces."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of what this rule checks."""
        ...

    @abstractmethod
    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        """
        Evaluate the rule against a project.

        Args:
            project_path: Path to the project root directory.

        Returns:
            List of LawEvaluation results (usually one per rule).
        """
        ...
