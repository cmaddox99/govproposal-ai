"""Session-scoped fixtures shared across the C++ avatar test suite."""

import pytest
import yaml
from pathlib import Path


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


@pytest.fixture(scope="session")
def cpp_dir(repo_root) -> Path:
    return repo_root / "avatars" / "technology" / "cpp"


@pytest.fixture(scope="session")
def guidance_content(cpp_dir) -> str:
    return (cpp_dir / "guidance.md").read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def manifest_data(cpp_dir) -> dict:
    return yaml.safe_load((cpp_dir / "manifest.yaml").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def examples_dir(cpp_dir) -> Path:
    return cpp_dir / "examples"


@pytest.fixture(scope="session")
def laws_dir(repo_root) -> Path:
    return repo_root / "laws"


@pytest.fixture(scope="session")
def cpp_full_reference(cpp_dir) -> str:
    """Content of all avatars/technology/cpp/ref-*.md files (formerly full-reference.md, now split)."""
    return "\n".join(p.read_text(encoding="utf-8") for p in sorted(cpp_dir.rglob("ref-*.md")))
