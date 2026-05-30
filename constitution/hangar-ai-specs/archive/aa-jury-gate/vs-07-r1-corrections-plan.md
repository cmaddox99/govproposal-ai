# VS-07 R1 Corrections Plan

**R1 Verdict:** 3 APPROVED, 2 NEEDS_REVISION (J3, J5)

## MUST_FIX Items

### J3-001: CLI output doesn't match Phase 3 §1.4 spec
**Current:** Prints simple "Verdict: PASS" format
**Required:** 
- Path banner: `aa-jury-gate check results for: <path>`
- Separator line
- Check table with proper spacing
- Final summary: `GATE: PASS/FAIL (N checks failed)`

**Fix:** Update `cli.py:_print_result()` lines 78-92

### J3-002: Invalid YAML should be exit 2 (ERROR), not exit 1 (FAIL)
**Current:** S03 returns FAIL → exit 1
**Required:** Phase 3 §1.3 line 146 - YAML parse failure is exit 2

**Fix:** 
- Check S03 must raise ToolError on YAML parse failure
- Or gate.py must catch S03 FAIL and convert to ERROR verdict

### J3-003: jury_gate block missing required fields
**Current:** Only writes `verdict`, `content_sha256`, `checks` list
**Required:** Phase 3 §5.1 - must include:
- `tool: aa-jury-gate`
- `version: <semver>`
- `timestamp_utc: <ISO-8601>`
- `checks_failed: N`
- `checks_skipped: N`

**Fix:** Update `output.py:append_gate_result()` lines 43-54

### J3-003b: content_sha256 must strip prior jury_gate block first
**Current:** Computes SHA256 on full file content
**Required:** Phase 3 §5.3 - compute AFTER stripping prior `jury_gate:` key

**Fix:** 
- Update `gate.py:_compute_sha256()` to accept content string
- Call `extractor.strip_jury_gate()` before hashing
- Update all callers

### J5-001: S04 check unreachable; YAML parse failures misclassified
**Current:** `parse()` raises on non-dict FM before S04 runs
**Required:** S04 should catch and return FAIL CheckItem

**Fix:**
- gate.py should call parse() in try/except
- Catch yaml.YAMLError and return S04 FAIL (not ERROR)
- Or refactor parse() to return tuple with error

### J5-002: Click bypasses validate_synthesis_path() for missing files
**Current:** `click.Path(exists=True)` catches missing files first
**Required:** Single call site per C-P5-J4-R2-001

**Fix:** Remove `exists=True` from Click, handle in main()

## SHOULD_FIX Items (Consensus)

### Mutation 407: Test gap for s11_failed logic
**Issue:** `and→or` mutant survives; no test for "S06 FAIL + S11 PASS + B01-B03 run"

**Fix:** Add test case in `test_gate.py`:
```python
def test_body_checks_run_when_s11_pass_despite_other_fail(self, synthesis_factory):
    # S06 will FAIL (wrong juror_count), but S11 PASS (verdict=APPROVED)
    # Body checks should RUN, not SKIP
    path = synthesis_factory(juror_count=3)  # Creates 5 jurors → S06 FAIL
    # verdict remains APPROVED → S11 PASS
    
    stub_probe = StubGitProbe(GitStatus.CLEAN)
    runner = GateRunner(git_probe=stub_probe)
    result = runner.run(path, allow_no_git=False)
    
    assert result.verdict == GateVerdict.FAIL  # S06 failed
    s06 = next(c for c in result.checks if c.check_id == "S06")
    assert s06.result == CheckResult.FAIL
    s11 = next(c for c in result.checks if c.check_id == "S11")
    assert s11.result == CheckResult.PASS
    
    # Body checks should PASS (not SKIP) because S11 passed
    for check_id in ["B01", "B02", "B03"]:
        c = next(check for check in result.checks if check.check_id == check_id)
        assert c.result == CheckResult.PASS  # NOT SKIP
```

## Estimated Effort

- J3-001: 30 min (reformat CLI output)
- J3-002: 45 min (error classification refactor)
- J3-003: 30 min (add fields to jury_gate block)
- J3-003b: 45 min (strip_jury_gate before SHA256)
- J5-001: 30 min (handle parse() errors correctly)
- J5-002: 15 min (remove exists=True)
- Mutation 407 test: 15 min

**Total: ~3.5 hours**

## Implementation Priority

1. J5-002 (quick fix)
2. J3-001 (CLI output format)
3. J3-003 (jury_gate block fields)
4. J3-003b (content_sha256 strip)
5. J3-002 + J5-001 (error classification - linked)
6. Mutation 407 test

## Next Steps

After R1 corrections:
1. Run full test suite (all 264+ tests must pass)
2. Update vs-07-evidence.md with R1 corrections
3. Launch R2 jury (5 jurors)
4. Address R2 feedback if any
5. Judicial synthesis
6. Human APPROVE gate
7. Proceed to Phase 7
