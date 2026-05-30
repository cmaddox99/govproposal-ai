"""Tests for CI workflow and project configuration correctness.

Amendment V (P2+P5 panel review):
- V-01: pyproject.toml must declare pythonpath=["."] for reliable absolute imports
- V-02: governance-tests.yml must run tests/unit/ (not just tests/governance/)

Amendment Y (CI build fix):
- Y-01: unit-tests job must install tools/constitution-lint before running tests/unit/
"""
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.parent


# ---------------------------------------------------------------------------
# Amendment V-01: pyproject.toml declares pythonpath=["."]
# ---------------------------------------------------------------------------

def test_pyproject_toml_declares_pythonpath():
    """Amendment V-01: pyproject.toml [tool.pytest.ini_options] must declare
    pythonpath=['.'] so that 'from tests.unit.test_cpp_avatar.avatar_test_helpers import ...'
    absolute imports work reliably regardless of pytest's conftest path injection."""
    content = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'pythonpath' in content, (
        "pyproject.toml [tool.pytest.ini_options] missing 'pythonpath' — "
        "absolute package imports (from tests.unit...) are fragile without it"
    )
    assert '= ["."]' in content or "= [ '.' ]" in content or '= [\'.\']' in content, (
        "pyproject.toml must set pythonpath = [\".\"] so the repo root is on sys.path"
    )


# ---------------------------------------------------------------------------
# Amendment V-02: governance-tests.yml runs the unit test suite
# ---------------------------------------------------------------------------

def test_governance_ci_runs_unit_tests():
    """Amendment V-02: .github/workflows/governance-tests.yml must contain a job
    that runs tests/unit/ so that the 768-test unit suite is visible to CI.
    Currently only tests/governance/ (10 tests) runs on push/PR, making all
    unit test failures invisible to reviewers."""
    ci_path = REPO_ROOT / ".github" / "workflows" / "governance-tests.yml"
    assert ci_path.exists(), ".github/workflows/governance-tests.yml does not exist"
    content = ci_path.read_text(encoding="utf-8")
    assert "tests/unit" in content, (
        "governance-tests.yml does not run tests/unit/ — "
        "the 768-test unit suite is invisible to CI (Amendment V-02 blocker)"
    )


# ---------------------------------------------------------------------------
# Amendment Y-01: unit-tests job installs tools/constitution-lint
# ---------------------------------------------------------------------------

def test_unit_tests_ci_job_installs_constitution_lint():
    """Amendment Y-01: the unit-tests job in governance-tests.yml must install
    tools/constitution-lint before running pytest tests/unit/.
    tests/unit/test_constitution_lint/ imports aa_constitution_lint directly;
    without this step the job fails with ModuleNotFoundError at collection time."""
    ci_path = REPO_ROOT / ".github" / "workflows" / "governance-tests.yml"
    content = ci_path.read_text(encoding="utf-8")
    assert "tools/constitution-lint" in content, (
        "governance-tests.yml unit-tests job does not install tools/constitution-lint — "
        "tests/unit/test_constitution_lint/ will fail with ModuleNotFoundError (Amendment Y-01)"
    )
