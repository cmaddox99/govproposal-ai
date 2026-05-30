"""Shared fixtures for the Java/Spring Boot avatar test suite."""

import pytest
import yaml
from pathlib import Path


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


@pytest.fixture(scope="session")
def java_spring_dir(repo_root) -> Path:
    return repo_root / "avatars" / "technology" / "java-spring"


@pytest.fixture(scope="session")
def manifest_data(java_spring_dir) -> dict:
    return yaml.safe_load((java_spring_dir / "manifest.yaml").read_text(encoding="utf-8"))
