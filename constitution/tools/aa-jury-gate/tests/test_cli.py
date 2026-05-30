"""CLI integration tests via CliRunner."""
import subprocess

from click.testing import CliRunner

from aa_jury_gate.cli import main


class TestCLI:
    """Integration tests for CLI via Click CliRunner."""

    def test_missing_argument_usage_error(self):
        """Test aa-jury-gate with no args → usage error (BDD scenario 7)."""
        runner = CliRunner()
        result = runner.invoke(main, [])

        assert result.exit_code == 2
        assert "SYNTHESIS" in result.output or "Usage:" in result.output

    def test_valid_synthesis_pass_exit_0(self, tmp_git_repo):
        """Test valid synthesis → exit 0, stdout contains PASS (BDD scenario 1)."""
        runner = CliRunner()
        result = runner.invoke(main, [str(tmp_git_repo)])

        assert result.exit_code == 0
        assert "GATE: PASS" in result.output
        assert "aa-jury-gate check results for:" in result.output

    def test_valid_synthesis_output_append_writes_block(self, tmp_git_repo):
        """Test --output append writes jury_gate: block (BDD scenario 2)."""
        runner = CliRunner()
        result = runner.invoke(main, [str(tmp_git_repo), "--output", "append"])

        assert result.exit_code == 0
        content = tmp_git_repo.read_text()
        assert "jury_gate:" in content
        assert "verdict: PASS" in content

    def test_output_append_idempotent(self, tmp_git_repo):
        """Test --output append twice → not duplicated (BDD scenario 3)."""
        runner = CliRunner()

        # Run first time
        result1 = runner.invoke(main, [str(tmp_git_repo), "--output", "append"])
        assert result1.exit_code == 0

        # Commit the changes to keep it CLEAN for second run
        import subprocess

        repo_dir = tmp_git_repo.parent
        subprocess.run(
            ["git", "add", tmp_git_repo.name], cwd=repo_dir, check=True, capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", "Add jury_gate"],
            cwd=repo_dir,
            check=True,
            capture_output=True,
        )

        # Run second time
        result2 = runner.invoke(main, [str(tmp_git_repo), "--output", "append"])
        assert result2.exit_code == 0

        content = tmp_git_repo.read_text()
        assert content.count("jury_gate:") == 1  # Not duplicated

    def test_invalid_synthesis_fail_exit_1(self, synthesis_factory, tmp_path):
        """Test invalid synthesis → exit 1, stdout contains FAIL lines (BDD scenario 4)."""
        # Create synthesis with bad juror_count
        path = synthesis_factory(juror_count=3)  # But creates 5 jurors → S05 FAIL
        content = path.read_text()
        # Manually corrupt it
        content = content.replace("juror_count: 3", "juror_count: 1")
        path.write_text(content)

        runner = CliRunner()
        result = runner.invoke(main, [str(path), "--allow-no-git"])

        assert result.exit_code == 1
        assert "FAIL" in result.output
        assert "S05" in result.output

    def test_nonexistent_file_exit_2(self, tmp_path):
        """Test nonexistent file → exit 2, no --output write (BDD scenario 15)."""
        nonexistent = tmp_path / "nonexistent.md"

        runner = CliRunner()
        result = runner.invoke(main, [str(nonexistent)])

        assert result.exit_code == 2
        assert "ERROR" in result.output or "does not exist" in result.output.lower()

    def test_directory_path_exit_2(self, tmp_path):
        """Test directory path → exit 2 (BDD scenario 16)."""
        runner = CliRunner()
        result = runner.invoke(main, [str(tmp_path)])

        assert result.exit_code == 2
        # Either usage error or unexpected error from extractor
        assert result.exit_code == 2

    def test_invalid_yaml_exit_2(self, tmp_path):
        """Test invalid YAML → exit 2 ERROR (Phase 3 §1.3 line 146)."""
        path = tmp_path / "bad.yaml.md"
        path.write_text("---\ninvalid: yaml: structure: [\n---\n\n# Body\n")

        runner = CliRunner()
        result = runner.invoke(main, [str(path), "--allow-no-git"])

        assert result.exit_code == 2  # ERROR (invocation error)
        # Output should mention "ERROR" or "not valid YAML" (Phase 3 §1.3)
        assert "ERROR" in result.output or "not valid YAML" in result.output

    def test_allow_no_git_outside_repo_pass(self, synthesis_factory, tmp_path):
        """Test --allow-no-git outside repo → exit 0, G01 SKIP (BDD scenario 19)."""
        path = synthesis_factory()  # Not in a git repo

        runner = CliRunner()
        result = runner.invoke(main, [str(path), "--allow-no-git"])

        assert result.exit_code == 0
        assert "G01" in result.output
        assert "SKIP" in result.output

    def test_allow_no_git_inside_repo_pass(self, tmp_git_repo):
        """Test --allow-no-git inside repo → exit 0, G01 PASS (BDD-F06)."""
        runner = CliRunner()
        result = runner.invoke(main, [str(tmp_git_repo), "--allow-no-git"])

        assert result.exit_code == 0
        assert "G01" in result.output
        assert "PASS" in result.output

    def test_no_allow_no_git_outside_repo_fail(self, synthesis_factory, tmp_path):
        """Test outside repo WITHOUT --allow-no-git → exit 1, G01 FAIL (BDD scenario 18)."""
        path = synthesis_factory()  # Not in a git repo

        runner = CliRunner()
        result = runner.invoke(main, [str(path)])

        assert result.exit_code == 1
        assert "G01" in result.output
        assert "FAIL" in result.output

    def test_s11_fail_body_checks_skip(self, synthesis_factory, tmp_path):
        """Test S11 FAIL → B01-B03 all SKIP in stdout (BDD scenario 11)."""
        path = synthesis_factory(verdict="INVALID")  # Bad verdict → S11 FAIL

        runner = CliRunner()
        result = runner.invoke(main, [str(path), "--allow-no-git"])

        assert result.exit_code == 1
        assert "S11" in result.output
        assert "FAIL" in result.output
        # B01-B03 should all show SKIP
        for check_id in ["B01", "B02", "B03"]:
            assert check_id in result.output
            # Find the line with this check_id and verify it says SKIP
            lines = result.output.split("\n")
            check_line = next(line for line in lines if check_id in line)
            assert "SKIP" in check_line

    def test_version_flag(self):
        """Test --version flag → version string (BDD scenario 19)."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])

        assert result.exit_code == 0
        assert "version" in result.output.lower() or "." in result.output  # e.g., "0.1.0"

    def test_error_verdict_empty_stdout(self, tmp_path):
        """Test exit-2 stdout is empty or error-only (Phase 3 §1.3 contract)."""
        path = tmp_path / "nonexistent.md"

        runner = CliRunner()
        result = runner.invoke(main, [str(path)])

        assert result.exit_code == 2
        # Stdout should NOT contain check tables
        assert "Check  Result  Detail" not in result.output
        assert "Verdict:" not in result.output

    def test_untracked_file_in_repo_fail(self, tmp_path):
        """Test untracked file in git repo → exit 1, G01 FAIL."""
        # Create a git repo
        subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.name", "Test"],
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

        # Create synthesis but don't git add it
        path = tmp_path / "synthesis.md"
        path.write_text("""---
schema_version: 1
juror_count: 5
jurors:
- {id: J1, model: test, role: test, r1_verdict: APPROVED}
- {id: J2, model: test, role: test, r1_verdict: APPROVED}
- {id: J3, model: test, role: test, r1_verdict: APPROVED}
- {id: J4, model: test, role: test, r1_verdict: APPROVED}
- {id: J5, model: test, role: test, r1_verdict: APPROVED}
synthesizer: test
slice: TEST
title: Test
verdict: APPROVED
---

# Body
""")

        runner = CliRunner()
        result = runner.invoke(main, [str(path)])

        assert result.exit_code == 1
        assert "G01" in result.output
        assert "FAIL" in result.output
        assert "not tracked" in result.output or "untracked" in result.output.lower()

    def test_uncommitted_file_in_repo_fail(self, tmp_path):
        """Test uncommitted changes → exit 1, G01 FAIL."""
        # Create git repo and commit initial version
        subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.name", "Test"],
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

        path = tmp_path / "synthesis.md"
        path.write_text("""---
schema_version: 1
juror_count: 5
jurors:
- {id: J1, model: test, role: test, r1_verdict: APPROVED}
- {id: J2, model: test, role: test, r1_verdict: APPROVED}
- {id: J3, model: test, role: test, r1_verdict: APPROVED}
- {id: J4, model: test, role: test, r1_verdict: APPROVED}
- {id: J5, model: test, role: test, r1_verdict: APPROVED}
synthesizer: test
slice: TEST
title: Test
verdict: APPROVED
---

# Body
""")
        subprocess.run(
            ["git", "add", "synthesis.md"], cwd=tmp_path, check=True, capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", "init"], cwd=tmp_path, check=True, capture_output=True
        )

        # Modify file without committing
        path.write_text(path.read_text() + "\n\n# Modified\n")

        runner = CliRunner()
        result = runner.invoke(main, [str(path)])

        assert result.exit_code == 1
        assert "G01" in result.output
        assert "FAIL" in result.output
        assert "uncommitted" in result.output.lower()
