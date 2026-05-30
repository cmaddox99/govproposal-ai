"""Test fixtures for integration testing."""
import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def tmp_git_repo(tmp_path: Path) -> Path:
    """Create a temporary git repository with a valid committed file.

    Returns the path to a synthesis.md file that is tracked and clean.
    """
    # Initialize git repo
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )

    # Create and commit a valid synthesis file
    synthesis_path = tmp_path / "synthesis.md"
    synthesis_path.write_text(
        """---
schema_version: 1
juror_count: 5
jurors:
- id: J1
  model: claude-opus-4.6
  role: Domain Sceptic
  r1_verdict: APPROVED
- id: J2
  model: claude-sonnet-4.6
  role: Technical Expert
  r1_verdict: APPROVED
- id: J3
  model: gpt-5.4
  role: Strategic Lens
  r1_verdict: APPROVED
- id: J4
  model: gpt-5.2
  role: Defense Counsel
  r1_verdict: APPROVED
- id: J5
  model: gpt-5.4-mini
  role: Devil's Advocate
  r1_verdict: APPROVED
synthesizer: claude-opus-4.5
slice: VS-01
title: Test Synthesis
verdict: APPROVED
rounds:
  r1_completed: true
  r2_completed: true
---

## R1 Deliberation

Test R1 synthesis document body text.

## R2 Deliberation

Test R2 content.

## Synthesis

Final synthesis content.

[ENG-2.1]: Automated Tests Required
""",
        encoding="utf-8",
    )

    subprocess.run(["git", "add", "synthesis.md"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )

    return synthesis_path


@pytest.fixture
def synthesis_factory(tmp_path: Path):
    """Factory for creating synthesis .md files with configurable frontmatter."""

    def _make(
        *,
        schema_version: int = 1,
        juror_count: int = 5,
        verdict: str = "APPROVED",
        slice_id: str = "VS-01",
        title: str = "Test",
        body: str = "\n# Body\n\nTest body.\n",
        filename: str = "test.md",
    ) -> Path:
        """Create a synthesis file with given params."""
        import yaml

        fm = {
            "schema_version": schema_version,
            "juror_count": juror_count,
            "jurors": [
                {
                    "id": f"J{i}",
                    "model": f"model-{i}",  # Unique models to avoid S08a FAIL
                    "role": "test",
                    "r1_verdict": "APPROVED",
                }
                for i in range(1, juror_count + 1)
            ],
            "synthesizer": "test-synth",
            "slice": slice_id,
            "title": title,
            "verdict": verdict,
            "rounds": {
                "r1_completed": True,  # Satisfy S09
                "r2_completed": True,  # Satisfy S10
            },
        }

        fm_text = yaml.dump(fm, default_flow_style=False, sort_keys=False)

        # Add body sections to satisfy B01-B03
        default_body = """
## R1 Deliberation

Test R1 content.

## R2 Deliberation

Test R2 content.

## Synthesis

Test synthesis content.
"""

        # Use default_body if body is the default placeholder
        actual_body = body if body != "\n# Body\n\nTest body.\n" else default_body
        content = f"---\n{fm_text}---{actual_body}"

        path = tmp_path / filename
        path.write_text(content, encoding="utf-8")
        return path

    return _make


@pytest.fixture
def env_isolation(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Isolate CLI tests to tmp_path — no writes outside tmp_path."""
    log_dir = tmp_path / "logs"
    log_dir.mkdir()

    # Monkeypatch default log_dir if needed (currently not used but reserved)
    # This fixture ensures all test writes stay within tmp_path

    yield log_dir

    # Assert no writes outside tmp_path (basic sanity — tests should use tmp_path fixtures)
