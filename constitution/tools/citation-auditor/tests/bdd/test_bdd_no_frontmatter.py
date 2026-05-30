"""BDD tests — Phase 3 §4.5 Scenarios 3–5: --output append on no-frontmatter artifact.

Verifies that --output append:
- Creates a frontmatter block on artifacts with no existing frontmatter
- Preserves original content after the new frontmatter
- Correctly handles overwrites on subsequent runs (idempotent structure)
- Stable verdict ordering across runs (FAIL→WARN→PASS)
"""
from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from citation_auditor.cli import main

RUNNER = CliRunner()
BDD_REGISTRY = Path(__file__).parent.parent / "fixtures" / "bdd" / "registry"
FIXTURE_NO_FM = (
    Path(__file__).parent.parent / "fixtures" / "bdd" / "artifact_no_frontmatter.md"
)


def _artifact(tmp_path: Path, content: str, fname: str = "artifact.md") -> Path:
    p = tmp_path / fname
    p.write_text(content)
    return p


def _run(artifact: Path, extra: list[str] | None = None):
    args = [str(artifact), "--laws-dir", str(BDD_REGISTRY)] + (extra or [])
    return RUNNER.invoke(main, args)


# ---------------------------------------------------------------------------
# §4.5 Sc-3: --output append on artifact with no frontmatter creates block
# ---------------------------------------------------------------------------
class TestNoFrontmatterCreatesBlock:
    def test_prepend_with_frontmatter(self, tmp_path):
        art = _artifact(tmp_path, "No frontmatter here.\n\nENG-3.5 cited.\n")
        result = _run(art, ["--output", "append"])
        assert result.exit_code != 2
        content = art.read_text()
        assert content.startswith("---")

    def test_citation_audit_block_created(self, tmp_path):
        art = _artifact(tmp_path, "No frontmatter here.\n\nENG-3.5 cited.\n")
        _run(art, ["--output", "append"])
        content = art.read_text()
        assert "citation_audit" in content

    def test_original_content_preserved(self, tmp_path):
        original = "No frontmatter here.\n\nENG-3.5 cited.\n"
        art = _artifact(tmp_path, original)
        _run(art, ["--output", "append"])
        content = art.read_text()
        assert "No frontmatter here" in content
        assert "ENG-3.5 cited" in content

    def test_exit_code_0(self, tmp_path):
        art = _artifact(tmp_path, "No frontmatter here.\n\nENG-3.5 cited.\n")
        result = _run(art, ["--output", "append"])
        assert result.exit_code == 0

    def test_fixture_file_no_frontmatter(self, tmp_path):
        """Copy the pre-built no-frontmatter fixture, run append, check."""
        import shutil
        art = tmp_path / "artifact_no_frontmatter.md"
        shutil.copy(FIXTURE_NO_FM, art)
        result = _run(art, ["--output", "append"])
        assert result.exit_code != 2
        content = art.read_text()
        assert content.startswith("---")
        assert "citation_audit" in content


# ---------------------------------------------------------------------------
# §4.5 Sc-4: --output append overwrites existing citation_audit block
# ---------------------------------------------------------------------------
class TestOverwriteExistingCitationAudit:
    def test_only_one_citation_audit_key(self, tmp_path):
        # Run twice — should have only one citation_audit block
        art = _artifact(tmp_path, "---\ntitle: t\n---\n\nENG-3.5 cited.\n")
        _run(art, ["--output", "append"])
        _run(art, ["--output", "append"])
        content = art.read_text()
        count = content.count("citation_audit:")
        assert count == 1

    def test_timestamp_updated_on_second_run(self, tmp_path):
        import time
        import yaml as _yaml

        art = _artifact(tmp_path, "---\ntitle: t\n---\n\nENG-3.5 cited.\n")

        def _get_timestamp(content: str) -> str:
            end = content.find("\n---", 3)
            if end == -1:
                return ""
            fm = _yaml.safe_load(content[3:end]) or {}
            return fm.get("citation_audit", {}).get("timestamp", "")

        _run(art, ["--output", "append"])
        ts1 = _get_timestamp(art.read_text())
        time.sleep(1)
        _run(art, ["--output", "append"])
        ts2 = _get_timestamp(art.read_text())
        # Both timestamps must be non-empty ISO-8601 strings
        assert ts1, "No timestamp after first run"
        assert ts2, "No timestamp after second run"
        # 1-second sleep guarantees the second differs
        assert ts1 != ts2, f"Timestamps unchanged: {ts1!r}"


# ---------------------------------------------------------------------------
# §4.5 Sc-5: --output append — verdict ordering stable across runs
# ---------------------------------------------------------------------------
class TestAppendVerdictOrderingStable:
    def test_fail_before_warn_before_pass(self, tmp_path):
        body = "ENG-3.5 PASS. ENG-10.1 (Amendment Process Law) WARN. ENG-99.9 FAIL.\n"
        art = _artifact(tmp_path, f"---\ntitle: t\n---\n\n{body}")
        _run(art, ["--output", "append"])
        content = art.read_text()
        # PyYAML dumps enum values without quotes: verdict: FAIL
        fail_pos = content.find("verdict: FAIL")
        warn_pos = content.find("verdict: WARN")
        pass_pos = content.find("verdict: PASS")
        assert fail_pos != -1, "No FAIL verdict in append output"
        assert warn_pos != -1, "No WARN verdict in append output"
        assert pass_pos != -1, "No PASS verdict in append output"
        assert fail_pos < warn_pos < pass_pos

    def test_second_run_identical_verdict_order(self, tmp_path):
        import yaml as _yaml
        body = "ENG-3.5 named. ENG-10.1 (Amendment Process Law). ENG-99.9 hallucinated.\n"
        art = _artifact(tmp_path, f"---\ntitle: t\n---\n\n{body}")

        def _get_verdicts(content: str) -> list[str]:
            """Extract verdict list from citation_audit YAML block."""
            if not content.startswith("---"):
                return []
            end = content.find("\n---", 3)
            if end == -1:
                return []
            fm = _yaml.safe_load(content[3:end]) or {}
            ca = fm.get("citation_audit", {})
            return [v["verdict"] for v in ca.get("verdicts", [])]

        _run(art, ["--output", "append"])
        order1 = _get_verdicts(art.read_text())
        _run(art, ["--output", "append"])
        order2 = _get_verdicts(art.read_text())
        assert order1 == order2
        assert order1[0] == "FAIL"   # FAIL first
