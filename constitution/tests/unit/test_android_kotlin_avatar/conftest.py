"""Shared fixtures for the Android Kotlin avatar test suite."""

import pytest
import yaml
from pathlib import Path


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


@pytest.fixture(scope="session")
def android_dir(repo_root) -> Path:
    return repo_root / "avatars" / "technology" / "android-kotlin"


@pytest.fixture(scope="session")
def guidance_content(android_dir) -> str:
    return (android_dir / "guidance.md").read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def manifest_data(android_dir) -> dict:
    return yaml.safe_load((android_dir / "manifest.yaml").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def examples_dir(android_dir) -> Path:
    return android_dir / "examples"
