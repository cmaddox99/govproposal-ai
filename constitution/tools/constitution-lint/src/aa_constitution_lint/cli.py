"""CLI entry point for aa-constitution-lint."""

import os
import subprocess
import sys
from pathlib import Path

import click
import yaml

from aa_constitution_lint import __version__
from aa_constitution_lint.application.linter import Linter
from aa_constitution_lint.config import Config
from aa_constitution_lint.domain.rules.agents_md_sync import AgentsMdDriftRule
from aa_constitution_lint.domain.rules.base import Rule
from aa_constitution_lint.domain.rules.constitution import (
    AvatarManifestNonnegCitationRule,
    AvatarManifestSchemaRule,
    DomainRegistrationCompletenessRule,
    LawBodyExistenceRule,
    LawFrontmatterCompletenessRule,
    LawTitleCoherenceRule,
    NoDeprecatedAdoptionRule,
    ProductAvatarCompletenessRule,
    ProductAvatarNonnegExamplesRule,
    SkillIndexConsistencyRule,
    TechAvatarCompletenessRule,
    TechAvatarNonnegExamplesRule,
)
from aa_constitution_lint.domain.rules.index_integrity import (
    AvatarIndexCompleteRule,
    AvatarRagCompleteRule,
    AvatarRagFilesExistRule,
    AvatarRagLawsValidRule,
    LawsRegistryCompleteRule,
    LawsRegistryFilesExistRule,
    NonnegLawsConsistentRule,
)
from aa_constitution_lint.domain.rules.references import LawReferenceRule
from aa_constitution_lint.infrastructure.law_registry import LawRegistry
from aa_constitution_lint.output.console import ConsoleFormatter
from aa_constitution_lint.output.json_output import JsonFormatter

# Pre-commit hook configuration template
PRECOMMIT_HOOK_CONFIG = {
    "repo": "local",
    "hooks": [
        {
            "id": "aa-constitution-lint",
            "name": "AA Constitution Lint",
            "entry": "aa-constitution-lint",
            "language": "system",
            "pass_filenames": False,
            "always_run": True,
        }
    ],
}


def get_formatter(format_type: str) -> ConsoleFormatter | JsonFormatter:
    """Get the appropriate formatter based on format type."""
    if format_type == "json":
        return JsonFormatter()
    return ConsoleFormatter()


def get_default_rules(project_path: Path, constitution_path: Path | None = None) -> list[Rule]:
    """
    Get the default set of rules to run.

    Args:
        project_path: Path to the project being linted.
        constitution_path: Optional path to hangar-ai-constitution for law validation.
    """
    # Determine where to load laws from
    laws_dir = None

    # Priority 1: Explicit constitution path
    if constitution_path:
        candidate = constitution_path / "laws"
        if candidate.exists():
            laws_dir = candidate

    # Priority 2: Project's own laws/ directory
    if laws_dir is None:
        candidate = project_path / "laws"
        if candidate.exists():
            laws_dir = candidate

    registry = None
    if laws_dir is not None:
        registry = LawRegistry.load(laws_dir)

    rules: list[Rule] = [
        ProductAvatarCompletenessRule(),
        TechAvatarCompletenessRule(),
        ProductAvatarNonnegExamplesRule(),
        TechAvatarNonnegExamplesRule(),
        NoDeprecatedAdoptionRule(),
        AvatarManifestSchemaRule(),
        AvatarManifestNonnegCitationRule(),
        LawFrontmatterCompletenessRule(),
        SkillIndexConsistencyRule(),
        LawsRegistryFilesExistRule(),
        LawsRegistryCompleteRule(),
        AvatarRagCompleteRule(),
        AvatarRagFilesExistRule(),
        AvatarRagLawsValidRule(registry),
        AvatarIndexCompleteRule(),
        NonnegLawsConsistentRule(),
        LawTitleCoherenceRule(),
        LawBodyExistenceRule(),
        DomainRegistrationCompletenessRule(),
    ]

    if registry is not None:
        rules.append(LawReferenceRule(registry))

    rules.append(AgentsMdDriftRule(constitution_path=constitution_path))

    return rules


def get_constitution_path_from_env() -> Path | None:
    """Get Constitution path from AA_CONSTITUTION_PATH environment variable."""
    env_path = os.environ.get("AA_CONSTITUTION_PATH")
    if env_path:
        path = Path(env_path)
        if path.exists():
            return path
    return None


class DefaultGroup(click.Group):
    """Click group that invokes a default command if none specified."""

    def __init__(self, *args, default_cmd: str | None = None, **kwargs) -> None:  # type: ignore[no-untyped-def]
        super().__init__(*args, **kwargs)
        self.default_cmd = default_cmd

    def parse_args(self, ctx: click.Context, args: list[str]) -> list[str]:
        """Parse arguments, invoking default command if needed."""
        # If no args or first arg is an option (starts with -) or a path, use default
        if self.default_cmd and (
            not args
            or args[0].startswith("-")
            or (args[0] not in self.commands and not args[0].startswith("-"))
        ):
            args = [self.default_cmd] + list(args)
        return super().parse_args(ctx, args)


@click.group(cls=DefaultGroup, default_cmd="lint", invoke_without_command=True)
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """AA Constitution Lint - Check project compliance with Constitutional laws."""
    pass


@cli.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path), default=".")
@click.option(
    "--format",
    "format_type",
    type=click.Choice(["console", "json"]),
    default="console",
    help="Output format (default: console)",
)
@click.option(
    "--constitution",
    "constitution_path",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Path to hangar-ai-constitution repo for law reference validation",
)
@click.option(
    "--with-rag-eval",
    "with_rag_eval",
    is_flag=True,
    default=False,
    help="After linting, run the RAG evaluation harness and fail if any score threshold is breached",
)
def lint(path: Path, format_type: str, constitution_path: Path | None, with_rag_eval: bool) -> None:
    """
    Lint a project for Constitutional compliance.

    PATH is the project directory to lint (defaults to current directory).
    """
    # Load configuration from project path
    config = Config.load(path)

    # Check for Constitution path from env var if not provided via flag
    if constitution_path is None:
        constitution_path = get_constitution_path_from_env()

    # Create linter with default rules and config
    linter = Linter(rules=get_default_rules(path, constitution_path), config=config)

    # Run lint
    result = linter.lint(path)

    # Format and output
    formatter = get_formatter(format_type)
    output = formatter.format(result)
    click.echo(output)

    lint_failed = result.has_failures()

    # ── Optional RAG eval integration (Phase 6) ────────────────────────────
    if with_rag_eval:
        rag_eval_script = path / "tools" / "rag-eval" / "evaluate.py"
        if not rag_eval_script.exists() and constitution_path:
            rag_eval_script = constitution_path / "tools" / "rag-eval" / "evaluate.py"

        if rag_eval_script.exists():
            click.echo("\n" + "─" * 60)
            click.echo("Running RAG evaluation harness…")
            click.echo("─" * 60)
            rag_result = subprocess.run(
                [sys.executable, str(rag_eval_script), "--threshold-check",
                 "--constitution", str(path)],
                capture_output=False,
            )
            if rag_result.returncode != 0:
                click.echo(
                    "\n[CRITICAL] RAG evaluation failed — one or more score thresholds breached.",
                    err=True,
                )
                lint_failed = True
        else:
            click.echo(
                "\n[WARNING] --with-rag-eval specified but tools/rag-eval/evaluate.py not found — skipping.",
                err=True,
            )

    # Exit with appropriate code
    if lint_failed:
        raise SystemExit(1)


@cli.group()
def hooks() -> None:
    """Manage pre-commit hooks for aa-constitution-lint."""
    pass


@hooks.command()
def install() -> None:
    """Install aa-constitution-lint as a pre-commit hook."""
    config_path = Path.cwd() / ".pre-commit-config.yaml"

    if config_path.exists():
        # Load existing config
        with open(config_path) as f:
            config = yaml.safe_load(f) or {}

        repos = config.get("repos", [])

        # Check if aa-constitution-lint is already installed
        for repo in repos:
            if repo.get("repo") == "local":
                for hook in repo.get("hooks", []):
                    if hook.get("id") == "aa-constitution-lint":
                        click.echo("aa-constitution-lint hook is already installed.")
                        return

        # Add our hook
        repos.append(PRECOMMIT_HOOK_CONFIG)
        config["repos"] = repos
    else:
        # Create new config
        config = {"repos": [PRECOMMIT_HOOK_CONFIG]}

    # Write config
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    click.echo("aa-constitution-lint hook installed successfully.")
    click.echo("Run 'pre-commit install' to activate the hook.")


@hooks.command()
def uninstall() -> None:
    """Remove aa-constitution-lint pre-commit hook."""
    config_path = Path.cwd() / ".pre-commit-config.yaml"

    if not config_path.exists():
        click.echo("No .pre-commit-config.yaml found.")
        return

    # Load existing config
    with open(config_path) as f:
        config = yaml.safe_load(f) or {}

    repos = config.get("repos", [])
    modified = False

    # Remove aa-constitution-lint from any local repo
    new_repos = []
    for repo in repos:
        if repo.get("repo") == "local":
            hooks_list = repo.get("hooks", [])
            new_hooks = [h for h in hooks_list if h.get("id") != "aa-constitution-lint"]
            if len(new_hooks) != len(hooks_list):
                modified = True
            if new_hooks:
                repo["hooks"] = new_hooks
                new_repos.append(repo)
            # If no hooks left, skip this repo entirely
        else:
            new_repos.append(repo)

    if not modified:
        click.echo("aa-constitution-lint hook not found in config.")
        return

    config["repos"] = new_repos

    # Write config
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    click.echo("aa-constitution-lint hook removed successfully.")


# Keep 'main' as the entry point for backwards compatibility
def main() -> None:
    """Entry point for aa-constitution-lint CLI."""
    cli()


if __name__ == "__main__":
    main()
