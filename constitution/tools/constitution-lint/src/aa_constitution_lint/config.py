"""Configuration loading for aa-constitution-lint."""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

CONFIG_FILENAME = ".constitution-lint.yaml"


class Config(BaseModel):
    """
    Configuration for aa-constitution-lint.

    Attributes:
        version: Config file version (currently 1)
        rules: Per-rule configuration (enabled, severity)
        settings: Global settings (fail_on_warning, ignore_paths)
    """

    version: int = 1
    rules: dict[str, dict[str, Any]] = Field(default_factory=dict)
    settings: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def load(cls, project_path: Path) -> "Config":
        """
        Load configuration from project path.

        Looks for .constitution-lint.yaml in the project root.
        Returns default config if file is missing.

        Args:
            project_path: Path to project root directory.

        Returns:
            Config instance with loaded or default values.
        """
        config_file = project_path / CONFIG_FILENAME

        if not config_file.exists():
            return cls()

        with open(config_file) as f:
            data = yaml.safe_load(f) or {}

        return cls(
            version=data.get("version", 1),
            rules=data.get("rules") or {},
            settings=data.get("settings") or {},
        )

    def is_rule_enabled(self, rule_id: str) -> bool:
        """
        Check if a rule is enabled.

        Rules are enabled by default. A rule is disabled only if
        it is explicitly set to enabled: false in the config.

        Args:
            rule_id: The rule identifier (e.g., "structure.agents_file")

        Returns:
            True if the rule should run, False if disabled.
        """
        if rule_id not in self.rules:
            return True  # Default: enabled

        rule_config = self.rules[rule_id]
        enabled = rule_config.get("enabled", True)
        return bool(enabled)
