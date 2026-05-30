---
skill:
  id: skill-12-legacy-refactor-rhythm
  name: Legacy Rescue Commit Rhythm
  category: development
  version: "1.0.0"

laws:
  implements:
    - id: ENG-4.14
      title: Legacy Rescue Commit Rhythm Law
    - id: ENG-3.4
      title: Single Responsibility Principle
  references:
    - id: ENG-4.1
      title: Atomic TDD Law
    - id: ENG-4.10
      title: Test Evolution Law
    - id: ENG-3.9
      title: Open/Closed Principle
    - id: ENG-12.1
      title: Agentic Phase Gate Law

triggers:
  phrases:
    - "Legacy rescue commit"
    - "How to commit during refactoring"
    - "Atomic commits for legacy code"
    - "Characterization test commit"
    - "Refactor commit rhythm"

followed_by:
  - skill-09-refactoring
  - skill-11-mutation-testing
  - skill-08-code-review
---

# Skill: Legacy Rescue Commit Rhythm

> **Purpose:** Guide agents through atomic commit cycles during legacy rescue refactoring, ensuring one test/violation per commit with verification checkpoints.
> **Workflow:** See `workflows/legacy-rescue-refactor.md` for the full governed refactor sequence.

---

## Purpose

Legacy Rescue Commit Rhythm implements **substrate engineering** for commit hygiene: encoding WHEN to commit (not just HOW MUCH) through explicit workflow cycles. This skill ensures:

1. **Atomic commits** - One concern per commit (one test OR one violation)
2. **Verification before damage** - Catch contamination before it enters history
3. **Reviewable diffs** - Each commit fits on one screen (< 5 min review)
4. **Natural rhythm** - Cycles teach when to commit, making good hygiene automatic
5. **Evidence for gates** - Phase gates verify commit hygiene via git log analysis

**The Problem This Solves:**

Legacy rescue workshops (iOS, Android, Constitution) showed that **good intentions fail without enforcing structure**:
- iOS Workshop: 14,373-line commits (bundled 3 refactors + 40 tests)
- Constitution Slice 1: 348-line commit (contaminated with files from other session)

**Root Cause:** Advisory rules ("one violation per commit") are bypassed. Developers use `git add -A`, stage unintended changes, discover problems 3 commits later (expensive to fix).

**Solution:** Explicit cycles with verification checkpoints (Steps 5/6, 7/8) catch contamination immediately.

---

## When to Invoke

Invoke this skill during:

- **Phase 3 (Characterize):** Adding characterization tests for legacy code
- **Phase 4 (Remediate):** Fixing violations before refactoring
- **Phase 5 (Refactor):** Extracting classes, moving methods, simplifying logic

**Trigger phrases:**
- "How do I commit this characterization test?"
- "I fixed the violation, what's next?"
- "Ready to commit the refactor"
- "Should I commit now or keep going?"

**First action:** Identify which cycle applies (Characterization or Refactor), then execute all steps in order.

---

## Constitutional Foundation

### Engineering Constitution
- **ENG-4.14** - Legacy Rescue Commit Rhythm Law: Explicit cycles with verification checkpoints
- **ENG-4.1** - Atomic TDD Law: Greenfield precedent (8-step cycle ending with commit)
- **ENG-3.4** - Single Responsibility Principle: One violation per commit enforces SRP at commit level
- **ENG-12.1** - Agentic Phase Gate Law: Jury reviews commit atomicity at gates

### Evidence from Substrate Hardening
- **Jason's iOS Workshop feedback:** Phase 5 bundled 3 refactors + 40 tests → 2,000-line commit
- **Constitution Slice 1:** `e9d7cdf` contaminated with 207 lines of phase-8 corrections due to `git add -A`
- **Lesson:** Verification checkpoints (Steps 5, 7/8) are non-negotiable

---

## Method: Two Commit Cycles

### Cycle 1: Characterization (7 Steps)

Use when adding characterization tests for untested legacy code (Phase 3).

**Goal:** One characterization test per commit.

```
1. IDENTIFY BEHAVIOR
   │ Select one specific behavior to characterize
   │ Example: "MileageCalculator.calculate() returns 0 for null input"
   │
2. WRITE TEST
   │ Create characterization test capturing CURRENT behavior
   │ NOT ideal behavior — capture what code ACTUALLY does
   │
3. VERIFY CURRENT BEHAVIOR
   │ Run test against existing code → should PASS
   │ If fails: behavior understanding is wrong, revise test
   │
4. STAGE TEST ONLY
   │ git add <test-file>
   │ ⚠️ NO `git add -A` or `git add .`
   │
5. VERIFY STAGING ✓ CHECKPOINT
   │ git diff --cached --stat
   │ Confirm: ONLY test file staged
   │ If extra files: git reset, restart from Step 4
   │
6. COMMIT TEST
   │ Format: test(char): capture <behavior> in <component>
   │ Body: "Characterization test for legacy code..."
   │
7. VERIFY COMMIT ✓ CHECKPOINT
   │ git show --stat HEAD
   │ Confirm: No unexpected files
   │ If contaminated: git reset HEAD~1, restart from Step 4
   │
8. ADVANCE
   └─ Mark test as done, proceed to next behavior
```

**Typical Output:** 20-80 lines, 1 file, ~2 min review time.

---

### Cycle 2: Refactor (8 Steps)

Use when refactoring code with test coverage (Phases 4, 5).

**Goal:** One violation remediation per commit.

```
1. SELECT VIOLATION
   │ Identify one SOLID/code-quality violation to fix
   │ Example: "MileageCalculator has 5 responsibilities (ENG-3.4 SRP)"
   │
2. PLAN REFACTOR
   │ Document approach before coding
   │ Example: "Extract tier-lookup logic into TierLookup class"
   │
3. APPLY REFACTOR
   │ Make the change (preserve behavior)
   │ Refactor = rearrange, NOT rewrite
   │
4. VERIFY TESTS GREEN
   │ Run full test suite → all tests MUST pass
   │ If red: fix tests or refactor, do NOT proceed
   │
5. STAGE CHANGES
   │ git add <files-modified-by-refactor>
   │ Stage specific files matching plan
   │ ⚠️ NO `git add -A` or `git add .`
   │
6. VERIFY STAGING ✓ CHECKPOINT
   │ git diff --cached --stat
   │ Confirm: File count matches plan (typically 1-3 files)
   │ If mismatch: git reset, restart from Step 5
   │
7. COMMIT REFACTOR
   │ Format: refactor(<violation-id>): <what-changed>
   │ Body: Before/After description, tests green
   │
8. VERIFY COMMIT ✓ CHECKPOINT
   │ git show --stat HEAD | head -20
   │ Confirm: No unexpected files, atomic change
   │ If contaminated: git reset HEAD~1, restart from Step 5
   │
9. ADVANCE
   └─ Mark violation as done, proceed to next violation
```

**Typical Output:** 50-300 lines, 1-3 files, ~3-5 min review time.

---

## Verification Checkpoints Explained

### Why Checkpoints Matter

**Without Checkpoints (Failure Mode):**
1. Developer stages everything: `git add -A`
2. Working tree has unrelated changes from other work
3. Commit bundles 3 concerns (348 lines, 5 files)
4. Discovers problem 3 commits later
5. Expensive to fix (rebase, force push, conflicts)

**With Checkpoints (Success Mode):**
1. Developer stages everything: `git add -A`
2. **Step 5/6 catches extra files before commit**
3. Developer restages correctly: `git add <intended-files>`
4. **Step 7/8 confirms clean commit after**
5. Advances confidently, no rework needed

### Checkpoint 1: Verify Staging (Steps 5, 6)

**Command:** `git diff --cached --stat`

**What it shows:**
```
src/test/MileageCalculatorTest.java | 42 ++++++++++++++++++
1 file changed, 42 insertions(+)
```

**Green signals:**
- ✅ File count matches intent (Characterization: 1 file, Refactor: 1-3 files)
- ✅ Line count is reasonable (Characterization: 20-80, Refactor: 50-300)
- ✅ No unrelated files (config changes, docs, other features)

**Red signals:**
- ❌ More files than expected (contamination)
- ❌ Line count > 500 (too large, split the work)
- ❌ Files from unrelated work (e.g., `RUNBOOK.md`, `phase-8-plan.md`)

**Action on red:** `git reset`, then `git add <specific-files>`

#### Agent Heuristics for Staging Verification

Use these explicit algorithms to detect red signals:

**1. Intent Matching Algorithm**
- Compare staged files against your working context
- Example: "I'm adding ENG-3.10 to quality.md" → Expected: 1 file (quality.md)
- If actual staging shows additional files → ❌ RED (contamination)

**2. File Count Rules**
- Characterization cycle: 1 test file (exception: +1 for shared fixtures)
- Refactor cycle: 1-3 production files (1 typical, 2-3 for extract class + update callers)
- **>3 files staged → ❌ RED** (unless justified extraction pattern)

**3. File Type Rules**
- Characterization: Test file ONLY → ✅ GREEN
- Refactor: Production file(s) ONLY → ✅ GREEN
- **Test + Production together → ❌ RED** (exception: TDD red-green cycle)

**4. Line Count Thresholds**
- Characterization: 20-80 lines ✅ GREEN, >200 lines ❌ RED (multiple tests bundled?)
- Refactor: 50-300 lines ✅ GREEN, >500 lines ❌ RED (multiple violations bundled?)
- New artifact (skill/law file): 300-700 lines ✅ GREEN (single-concern creation)

**5. Path Consistency Check**
- All files in same module/domain → ✅ GREEN
- Files span multiple domains → ❌ RED

**Example Scenarios:**

**Scenario 1: Contamination Detection**
```bash
$ git diff --cached --stat
laws/engineering/quality.md       | 139 +++  # ✅ Intended
phase-8-r1-corrections-plan.md    | 207 +++  # ❌ Unexpected!
RUNBOOK.md                         | 11 +++   # ❌ Unexpected!
```
**Algorithm:** Intent was 1 file, got 3 files (2 unexpected) → ❌ RED
**Action:** `git reset`, `git add laws/engineering/quality.md`

**Scenario 2: Multiple Tests Bundled**
```bash
$ git diff --cached --stat
tests/mileage_service_test.py | 247 +++
```
**Algorithm:** 247 lines > 200 threshold → ❌ RED (likely multiple tests)
**Action:** Inspect diff, split into separate cycles if multiple test methods

**Scenario 3: Test + Production Mixed**
```bash
$ git diff --cached --stat
src/mileage_service.py       | 85 +++---
tests/mileage_service_test.py | 42 +++
```
**Algorithm:** Test + Production types → ❌ RED (two concerns)
**Action:** Are you in TDD cycle? If NO, split into two commits

**Scenario 4: Extract Class (Atomic Multi-File)**
```bash
$ git diff --cached --stat
src/MileageCalculator.java | 45 ++---
src/TierLookup.java         | 38 +++++
```
**Algorithm:** 2 production files, 52 lines, same module → ✅ GREEN (cohesive extraction)
**Action:** Proceed to commit (ONE refactor spanning 2 files)

---

### Checkpoint 2: Verify Commit (Steps 7, 8)

**Command:** `git show --stat HEAD | head -20`

**What it shows:**
```
commit a1b2c3d
refactor(V-01): extract tier-lookup from MileageCalculator

 src/MileageCalculator.java | 45 ++---
 src/TierLookup.java         | 38 +++++
 2 files changed, 52 insertions(+), 31 deletions(-)
```

**Green signals:**
- ✅ Commit message matches cycle format
- ✅ File list matches what was intended
- ✅ Atomic change (one concern)

**Red signals:**
- ❌ Unexpected files in commit
- ❌ Multiple unrelated concerns
- ❌ Message doesn't describe what changed

**Action on red:** `git reset HEAD~1` (rollback), fix staging, recommit

---

## Commit Message Formats

### Characterization Test

```
test(char): capture <behavior> in <component>

Characterization test for legacy code before refactoring.
Captures CURRENT behavior (not ideal).

Component: src/MileageCalculator.java
Behavior: Returns 0 for null frequent-flyer-number input
```

**Template:**
```bash
git commit -m "test(char): capture <BEHAVIOR> in <COMPONENT>

Characterization test for legacy code before refactoring.
Captures CURRENT behavior (not ideal).

Component: <file/class>
Behavior: <specific case>
"
```

---

### Refactor Commit

```
refactor(V-01): extract tier-lookup from MileageCalculator

Fix SRP violation: calculator was responsible for tier lookup.

Before: MileageCalculator had 5 responsibilities
After: TierLookup handles tier queries
Tests: 47/47 green
```

**Template:**
```bash
git commit -m "refactor(<VIOLATION-ID>): <what-changed>

Fix <SOLID principle / code smell> violation.

Before: <problem description>
After: <solution description>
Tests: <N>/<N> green
"
```

**Violation ID Examples:**
- `V-01`: First violation in this phase
- `ENG-3.4-01`: SRP violation #1
- `GOD-CLASS-01`: God class extraction #1

---

## IDE Integration Guides

### VS Code

**Stage by Intent (not by convenience):**
1. Open Source Control panel (`Ctrl+Shift+G`)
2. Review each changed file
3. Click `+` next to ONLY files for this commit
4. **Skip** files that are unrelated work

**Verify Before Commit:**
- Review "Staged Changes" section
- Count files (should match intent)
- Scan diffs (should be one concern)

**Command Palette:**
- `Git: Stage Selected Ranges` - for surgical staging

**Settings:**
```json
{
  "git.confirmSync": false,
  "git.confirmEmptyCommits": false,
  "git.alwaysSignOff": true,
  "git.postCommitCommand": "none"
}
```

---

### IntelliJ IDEA / Android Studio

**Commit Panel Workflow:**
1. Open Commit tool window (`Cmd+K` / `Ctrl+K`)
2. Review "Changes" list
3. **Uncheck** files not for this commit
4. Review diff for each checked file
5. Write commit message
6. Click "Commit" (NOT "Commit and Push")

**After Commit:**
- View commit in Git log (`Cmd+9` / `Alt+9`)
- Verify file list matches intent
- If wrong: Right-click commit → "Undo Commit"

**Settings:**
- Preferences → Version Control → Commit
  - ✅ "Analyze code"
  - ✅ "Check TODO"
  - ❌ "Reformat code" (can mix concerns)

---

### CLI (Git Command Line)

**Stage Specific Files:**
```bash
# Characterization: stage test only
git add src/test/MileageCalculatorTest.java

# Refactor: stage files modified by refactor
git add src/MileageCalculator.java src/TierLookup.java
```

**Interactive Staging (for fine control):**
```bash
git add -p src/MileageCalculator.java
# Then: y (yes), n (no), s (split), q (quit)
```

**Verify Staging:**
```bash
git diff --cached --stat      # File summary
git diff --cached --name-only # File list only
git diff --cached             # Full diff
```

**Commit:**
```bash
git commit -m "test(char): capture null-input behavior

Characterization test for legacy code.
Captures CURRENT behavior (not ideal).

Component: MileageCalculator
Behavior: Returns 0 for null FFN
"
```

**Verify Commit:**
```bash
git show --stat HEAD          # Summary
git show HEAD                 # Full diff
```

**Rollback if Contaminated:**
```bash
git reset HEAD~1              # Undo commit, keep changes
git status                    # See what's staged/unstaged
# Then restage correctly and recommit
```

---

## Example: Refactoring God Class (5 Cycles)

**Scenario:** `MileageCalculator` has 5 responsibilities (SRP violation). Extract into 5 classes.

### Cycle 1: Extract Tier Lookup

**Step 1: Select Violation**
```
Violation: MileageCalculator.lookupTier() (responsibility 1/5)
Law: ENG-3.4 (SRP)
Plan: Extract TierLookup class
```

**Step 2: Plan Refactor**
```
Files to modify:
- src/MileageCalculator.java (remove lookupTier, delegate to TierLookup)
- src/TierLookup.java (NEW - tier lookup logic)

Expected size: ~80 lines
```

**Step 3-4: Apply Refactor + Tests Green**
```bash
# Edit files
vim src/MileageCalculator.java   # Remove lookupTier method
vim src/TierLookup.java           # Add new class

# Run tests
./gradlew test
# All 47 tests pass ✅
```

**Step 5-6: Stage + Verify**
```bash
git add src/MileageCalculator.java src/TierLookup.java

git diff --cached --stat
# Output:
#  src/MileageCalculator.java | 23 +----
#  src/TierLookup.java         | 38 +++++
#  2 files changed, 40 insertions(+), 21 deletions(-)
# ✅ 2 files as planned, ~60 lines total
```

**Step 7-8: Commit + Verify**
```bash
git commit -m "refactor(V-01): extract tier-lookup from MileageCalculator

Fix SRP violation: calculator was doing tier lookups.

Before: MileageCalculator had 5 responsibilities
After: TierLookup handles tier queries
Tests: 47/47 green
"

git show --stat HEAD
# ✅ Only the 2 intended files, atomic change
```

**Repeat for 4 more responsibilities** (bonus calculation, discount rules, accrual timing, expiration logic).

**Result:** 5 commits, each 50-100 lines, each reviewable in ~3 minutes. Total: 350 lines across 5 commits (vs. 1 monster commit of 350 lines).

---

## Pre-Commit Hook (Optional Reinforcement)

Add this to `.git/hooks/pre-commit` for automated verification:

```bash
#!/bin/bash
# Hangar AI Constitution - ENG-4.14 Commit Rhythm Enforcement
# Warns if commit is too large for atomic legacy rescue rhythm

file_count=$(git diff --cached --name-only | wc -l | tr -d ' ')
line_count=$(git diff --cached --numstat | awk '{add+=$1; del+=$2} END {print add+del}')

echo "📊 Commit size: $file_count files, $line_count lines"

# Warnings (soft)
if [ $file_count -gt 5 ]; then
  echo "⚠️  WARNING: $file_count files staged."
  echo "   Legacy rescue commits should be atomic (1-3 files)."
  echo "   Review: git diff --cached --stat"
  echo ""
fi

if [ $line_count -gt 300 ]; then
  echo "⚠️  WARNING: $line_count lines changed."
  echo "   Legacy rescue commits should be focused:"
  echo "   - Characterization: 20-80 lines"
  echo "   - Refactor: 50-300 lines"
  echo "   Consider splitting this commit."
  echo ""
fi

# Hard block (optional, enable if strict enforcement needed)
# if [ $file_count -gt 10 ]; then
#   echo "🔴 BLOCKED: Too many files ($file_count > 10)."
#   echo "   Split this work into multiple atomic commits."
#   exit 1
# fi

# If warnings shown, ask for confirmation
if [ $file_count -gt 5 ] || [ $line_count -gt 300 ]; then
  read -p "Proceed with commit? (y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Commit aborted. Review and restage files."
    exit 1
  fi
fi

echo "✅ Commit size acceptable. Proceeding..."
exit 0
```

**Installation:**
```bash
cd /path/to/codebase
cp /path/to/hangar-ai-constitution/tools/hooks/pre-commit-rhythm.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

**Effect:**
- Warns if > 5 files or > 300 lines
- Hard blocks if > 10 files (optional)
- Asks for confirmation before allowing commit

---

## Troubleshooting

### Problem: "I accidentally staged extra files"

**Symptoms:**
- `git diff --cached --stat` shows unexpected files
- File count doesn't match plan

**Solution:**
```bash
# Option 1: Unstage everything, start over
git reset

# Option 2: Unstage specific files
git reset HEAD <unwanted-file>

# Then restage correctly
git add <intended-files>
```

---

### Problem: "I committed contaminated changes"

**Symptoms:**
- `git show --stat HEAD` shows unrelated files
- Commit has multiple concerns

**Solution (if haven't pushed):**
```bash
# Undo commit, keep changes
git reset HEAD~1

# Review what's changed
git status

# Restage correctly
git add <intended-files>

# Recommit
git commit -m "..."
```

**Solution (if already pushed):**
- Do NOT force push if others have pulled
- Create fixup commits to separate concerns
- Document in phase artifact that commit was non-atomic

---

### Problem: "The commit is too large"

**Symptoms:**
- > 300 lines for refactor
- > 80 lines for characterization test
- Diff doesn't fit on one screen

**Solution:**
- The work is too large for one cycle
- Split into smaller steps:
  - Characterization: Test one method at a time, not whole class
  - Refactor: Extract one responsibility at a time, not all 5

---

### Problem: "Tests broke after refactor"

**Symptoms:**
- Step 4 fails (tests red after applying refactor)

**Solution:**
1. **DO NOT COMMIT** (never commit broken tests)
2. Review diff: `git diff`
3. Options:
   - Fix the refactor (behavior preservation failed)
   - Fix the tests (characterization was wrong)
4. Re-run tests until green
5. Then proceed to Step 5 (stage changes)

---

### Problem: "Not sure which cycle to use"

**Decision tree:**

**Am I adding a characterization test?**
- YES → Use Characterization Cycle (7 steps)
- NO → Continue...

**Am I refactoring existing code?**
- YES → Use Refactor Cycle (8 steps)
- NO → Not a legacy rescue commit (use standard git workflow)

---

## Success Metrics

Track these metrics at phase gates (ENG-12.1):

### Commit Hygiene Metrics

**Per Phase:**
- Total commits
- Avg lines/commit
- Avg files/commit
- % atomic commits (≤ 3 files, ≤ 300 lines)
- Contaminated commits (violations)

**Example Report:**
```
Phase 3 (Characterize): 47 commits
- Avg lines/commit: 52
- Avg files/commit: 1.1
- Atomic commits: 46/47 (98%)
- Violations: 1 (commit c3d4e5f had 4 files)
```

### Rhythm Compliance

**Phase 3 (Characterize):**
- Each commit should have 1 test file
- Message format: `test(char): ...`
- No production code changes

**Phase 5 (Refactor):**
- Each commit should fix 1 violation
- Message format: `refactor(<V-ID>): ...`
- Tests green before and after

---

## Relationship to Other Skills

**Prerequisites:**
- `skill-06-atomic-tdd` - Establishes TDD cycle rhythm (commit checkpoint)
- `skill-09-refactoring` - Refactoring patterns and techniques

**Followed by:**
- `skill-11-mutation-testing` - Verify test quality after refactoring
- `skill-08-code-review` - Review atomic commits (easier than monster diffs)

**Complements:**
- `skill-spec-governance` - Tracks violations in PROPOSAL.md
- `skill-artifact-html-rendering` - Phase artifacts show commit hygiene metrics

---

## Related Workflows

- **workflows/legacy-rescue-refactor.md** - Full Legacy Rescue Refactor Track
  - Phase 3: Use Characterization Cycle
  - Phase 4: Use Refactor Cycle (remediation)
  - Phase 5: Use Refactor Cycle (extraction)
  - Phase 6: Jury gate verifies commit hygiene

---

## Summary

Legacy Rescue Commit Rhythm provides:

1. ✅ **Explicit cycles** - Know exactly when to commit (no guessing)
2. ✅ **Verification checkpoints** - Catch contamination before damage
3. ✅ **Atomic commits** - One test OR one violation per commit
4. ✅ **Reviewable diffs** - Each commit < 5 min review time
5. ✅ **Phase gate evidence** - Git log proves rhythm compliance

**Key Principle:** Teaching beats policing. The cycles teach WHEN to commit through structure, making good hygiene automatic.

**Evidence:** Slice 1 contamination (348 lines, 3 concerns) validates that verification checkpoints are non-negotiable.

For constitutional foundation and success criteria, see **ENG-4.14** (Legacy Rescue Commit Rhythm Law).
