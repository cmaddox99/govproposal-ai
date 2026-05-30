# Pre-Implementation Codebase Audit — Mutation Testing Governance (ENG-4.11)

**Purpose:** Verify that American Airlines' AA-Hangar-AI codebase and infrastructure can support the mutation testing law (ENG-4.11) before governance approval.

**Timeline:** Complete before REVISION 3 submission; audit results inform pilot project selection.

**Conducted By:** DevOps + Engineering Leads (SonarQube admin, CI/CD owner, crew-scheduling + dispatch teams)

---

## Part A: SonarQube Infrastructure Readiness

### A1: SonarQube Version & Custom Metrics Support
**What to Check:** Does SonarQube support custom metrics and gates for mutation score?

- [ ] **Check SonarQube version:**
  ```bash
  # SSH to SonarQube server, or check admin panel
  curl https://sonarqube.aa-hangar.internal/api/system/about
  # Look for: "version": "X.Y.Z"
  ```
  - **Expected:** SonarQube v9.2+ (supports custom metrics API)
  - **If <9.2:** Upgrade required; contact DevOps

- [ ] **Check custom metrics plugin:**
  ```bash
  # In SonarQube admin panel: Administration > Plugins > Available
  # Search for: "Custom Metrics Plugin" or "Community Branch Plugin"
  ```
  - **Expected:** Plugin installed and enabled
  - **If not available:** Install via plugin marketplace or contact SonarQube admin

- [ ] **Verify quality gate configuration:**
  - In SonarQube: Administration > Quality Gates
  - [ ] Can create custom gate with condition: `Mutation Score > 70` (yes/no)
  - [ ] Can set gate condition to WARN vs. ERROR (yes/no)
  - [ ] Can assign gate to project and make it mandatory (yes/no)
  - **If any NO:** Document as limitation; will use SonarQube plugin API instead

### A2: SonarQube Mutation Score Metric Registration
**What to Check:** Can SonarQube receive and display mutation score data?

- [ ] **Check if mutation score metric exists:**
  ```bash
  # SonarQube API
  curl https://sonarqube.aa-hangar.internal/api/metrics/search
  # Look for metric with key "mutation_score" or "mutations_killed"
  ```
  - **Expected:** Metric exists (registered by mutation testing tools)
  - **If not found:** Will create custom metric via API

- [ ] **Test mutation score import:**
  - [ ] Run Stryker on sample TypeScript project (crew-scheduling-api)
  - [ ] Export JSON report: `reports/mutation/report.json`
  - [ ] Upload to SonarQube via generic metrics API:
    ```bash
    curl -X POST https://sonarqube.aa-hangar.internal/api/ce/activity \
      -H "Content-Type: application/json" \
      -d '{"mutation_score": 75.5}' \
      -u sonarqube-api-token
    ```
  - [ ] Verify mutation score appears in SonarQube dashboard
  - **Result:** PASS / FAIL (if FAIL, document workaround)

### A3: SonarQube Webhook & PR Integration
**What to Check:** Can SonarQube report mutation scores on GitHub PR comments?

- [ ] **Check webhook configuration:**
  - In SonarQube: Administration > Webhooks
  - [ ] GitHub webhook configured (points to AA-Hangar-AI repo)
  - [ ] Webhook triggers on project analysis (yes/no)
  - **If no:** Create webhook manually; see SonarQube docs

- [ ] **Test PR reporting:**
  - [ ] Create test PR with mutation testing results
  - [ ] Verify SonarQube posts comment with mutation score breakdown
  - [ ] Verify mutation score gate status (PASS/FAIL) is visible
  - **Result:** PASS / FAIL

---

## Part B: Mutation Testing Tool Availability

### B1: Stryker.js Installation (TypeScript/JavaScript)
**What to Check:** Is Stryker available for TypeScript projects (crew-scheduling, dispatch APIs)?

- [ ] **Check npm registry access:**
  ```bash
  npm config get registry
  # Expected: https://registry.npmjs.com or AA's private npm registry
  npm search @stryker-mutator/core --long
  ```
  - **Result:** Available / Not available

- [ ] **Test Stryker installation in crew-scheduling-api:**
  ```bash
  cd codebases/crew-scheduling-api
  npm install --save-dev @stryker-mutator/core @stryker-mutator/typescript-checker
  # Check node_modules/@stryker-mutator exists (yes/no)
  npx stryker --version
  ```
  - **Expected:** Stryker v6.x+ installed, no permission errors
  - **If error:** Document issue (private registry, corporate proxy, etc.)

- [ ] **Test Stryker on sample code:**
  ```bash
  # In crew-scheduling-api
  npx stryker run --testRunner jest --mutate "src/core/*.ts"
  ```
  - [ ] Execution completes without errors (yes/no)
  - [ ] HTML report generated: `reports/mutation/index.html` (yes/no)
  - [ ] Mutation score calculated (yes/no)
  - **Expected:** <5 minutes for 1000 LOC
  - **If >10 minutes:** Performance optimization needed

### B2: Pitest Installation (Java)
**What to Check:** Is Pitest available for Java projects (if any)?

- [ ] **Check Maven central access:**
  ```bash
  # In pom.xml, verify Maven Central repository is accessible
  mvn help:active-profiles
  ```
  - **Result:** Central accessible / Blocked by corporate proxy

- [ ] **Check Pitest Maven plugin:**
  ```bash
  # Add to pom.xml:
  <plugin>
    <groupId>org.pitest</groupId>
    <artifactId>pitest-maven</artifactId>
    <version>1.14.5</version>
  </plugin>
  
  # Try to install
  mvn pitest:mutationCoverage
  ```
  - **Expected:** Plugin installs without errors, mutation testing runs
  - **If error:** Document Maven central/proxy issue

### B3: mutmut Installation (Python)
**What to Check:** Is mutmut available for Python projects?

- [ ] **Check pip access:**
  ```bash
  pip install mutmut
  mutmut --version
  ```
  - **Result:** Installed / Not available

- [ ] **Test mutmut on sample Python code:**
  ```bash
  # In a Python project directory
  mutmut run --tests-dir tests
  mutmut results
  ```
  - [ ] Execution completes (yes/no)
  - [ ] Mutation report generated (yes/no)
  - **Expected:** <5 minutes for typical test suite
  - **If unavailable:** Note as limitation; can defer Python projects

### B4: cosmic-ray Installation (Go)
**What to Check:** Is cosmic-ray available for Go projects?

- [ ] **Check Go module proxy access:**
  ```bash
  go get github.com/jmrodriquez/cosmic-ray
  cosmic-ray --version
  ```
  - **Result:** Installed / Not available

- [ ] **Test cosmic-ray on sample Go code:**
  - [ ] Execution completes (yes/no)
  - [ ] Mutation report generated (yes/no)
  - **If unavailable:** Note as limitation; coordinate with Go maintainers

---

## Part C: CI/CD Pipeline Integration

### C1: GitHub Actions Async Execution
**What to Check:** Can GitHub Actions run mutation testing asynchronously without blocking developer feedback?

- [ ] **Check GitHub Actions configuration:**
  - [ ] Repository has `.github/workflows/` directory (yes/no)
  - [ ] Existing CI workflow (lint, test, build) is defined (yes/no)
  - [ ] Workflow has multiple jobs or matrix build (yes/no)
  - **Note:** Mutation testing should run in parallel job, not block main test workflow

- [ ] **Test async execution:**
  ```bash
  # Create test workflow: .github/workflows/mutation-testing.yml
  name: Mutation Testing (Async)
  on: [pull_request]
  jobs:
    mutation-test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Run Stryker
          run: npm install @stryker-mutator/core && npx stryker run
        - name: Upload to SonarQube
          run: |
            curl -X POST https://sonarqube.aa-hangar.internal/api/ce/activity \
              -d @reports/mutation/report.json
  ```
  - [ ] Workflow syntax valid (yes/no)
  - [ ] Push test PR and verify workflow triggers (yes/no)
  - [ ] Mutation testing completes in parallel without blocking PR checks (yes/no)
  - **Result:** PASS / FAIL

### C2: CI/CD Artifact Storage
**What to Check:** Can GitHub Actions upload mutation reports to SonarQube?

- [ ] **Check artifact upload capability:**
  - [ ] SonarQube API token available in GitHub Secrets (yes/no)
  - [ ] GitHub Actions can authenticate to SonarQube (yes/no)
  - [ ] Mutation report JSON can be uploaded and parsed (yes/no)

- [ ] **Test upload:**
  ```bash
  # In GitHub Actions workflow
  - name: Upload Mutation Report to SonarQube
    run: |
      curl -v -X POST "https://sonarqube.aa-hangar.internal/api/ce/activity" \
        -H "Authorization: Bearer ${{ secrets.SONARQUBE_TOKEN }}" \
        -F "report=@reports/mutation/report.json"
  ```
  - [ ] Upload succeeds (200 status) (yes/no)
  - [ ] SonarQube dashboard updates with mutation score (yes/no)
  - **Result:** PASS / FAIL

### C3: Pipeline Performance Impact
**What to Check:** Does adding mutation testing create unacceptable pipeline delays?

- [ ] **Baseline: Measure current CI/CD execution time**
  - [ ] Record typical PR workflow duration (lint + test + build)
  - **Expected:** ~10–15 minutes

- [ ] **Mutation testing overhead:**
  - [ ] Run mutation testing on crew-scheduling-api (parallel job)
  - [ ] Record execution time
  - [ ] Calculate overhead: (mutation_time / baseline_time) × 100%
  - **Acceptable:** <20% overhead (mutation adds ~2–3 min to 10–15 min baseline)
  - **If >20%:** Discuss performance optimization or async-only approach

---

## Part D: Team Readiness & Documentation

### D1: Tool Documentation & Training Resources
**What to Check:** Are engineers prepared to use mutation testing tools?

- [ ] **Stryker documentation:** Available at https://stryker-mutator.io/docs/stryker-js/api
  - [ ] TypeScript/Jest configuration examples (yes/no)
  - [ ] Mutation operator documentation (yes/no)
  - [ ] Equivalent mutant handling guidance (yes/no)

- [ ] **Pitest documentation:** Available at https://pitest.org
  - [ ] Maven integration examples (yes/no)
  - [ ] Configuration options (yes/no)

- [ ] **mutmut documentation:** Available at https://mutmut.readthedocs.io
  - [ ] Python setup examples (yes/no)
  - [ ] Configuration options (yes/no)

- [ ] **Internal guidance:**
  - [ ] Mutation testing skill created in constitution (yes/no)
  - [ ] Workshop materials prepared for pilot teams (yes/no)

### D2: Pilot Project Selection
**What to Check:** Are crew-scheduling, dispatch, maintenance codebases ready for pilot?

- [ ] **Crew-Scheduling API:**
  - [ ] Language: TypeScript (Stryker compatible) (yes/no)
  - [ ] Test framework: Jest (Stryker compatible) (yes/no)
  - [ ] Test coverage ≥90%: (yes/no) — baseline for mutation testing
  - [ ] Codebase size: ~2000–5000 LOC in `core/` (yes/no)
  - [ ] Critical path identified: `core/assignment.ts`, `core/time-calculations.ts` (yes/no)

- [ ] **Dispatch API:**
  - [ ] Language: TypeScript or Python (yes/no)
  - [ ] Test framework compatible with selected tool (yes/no)
  - [ ] Critical path: `core/safety-constraints.ts` (yes/no)

- [ ] **Maintenance Records API:**
  - [ ] Language: TypeScript, Python, or Java (yes/no)
  - [ ] Critical path: `core/compliance-tracking.ts` (yes/no)

---

## Part E: Risk Mitigation

### E1: Tool Performance Degradation
**Risk:** Mutation testing adds 2–5x runtime; slows developer feedback loop.

- [ ] **Mitigation:** Run mutation testing async (separate GitHub Actions job); gate PR merge on result but don't block initial feedback
  - [ ] Async workflow configured (yes/no)
  - [ ] SonarQube gate waiver process documented (yes/no)

### E2: Equivalent Mutant False Positives
**Risk:** High equivalent mutant rate (>10%) inflates complexity without benefit.

- [ ] **Mitigation:** Use tool auto-detection; limit mutation operators (exclude string literals, logging constants)
  - [ ] Tool configuration specifies excluded operators (yes/no)
  - [ ] Equivalent mutant policy documented (yes/no)

### E3: SonarQube Integration Failure
**Risk:** Mutation scores don't import to SonarQube; gates can't be enforced.

- [ ] **Mitigation:** Fallback to manual PR comment reporting (GitHub Actions output); gates enforced via workflow status
  - [ ] Fallback workflow documented (yes/no)
  - [ ] Manual gate enforcement procedure (yes/no)

---

## Summary Checklist

**SonarQube Infrastructure:**
- [ ] SonarQube v9.2+ running
- [ ] Custom metrics support verified
- [ ] Webhook integration tested
- [ ] Mutation score metric receives data

**Mutation Testing Tools:**
- [ ] Stryker.js installed for TypeScript projects
- [ ] Pitest available for Java projects
- [ ] mutmut available for Python projects
- [ ] cosmic-ray available for Go projects (if needed)

**CI/CD Integration:**
- [ ] Async mutation testing job configured
- [ ] Report upload to SonarQube working
- [ ] Pipeline overhead <20%
- [ ] Performance SLA <5 min for unit tests

**Team Readiness:**
- [ ] Tool documentation available
- [ ] Pilot project teams identified
- [ ] Training/workshop scheduled
- [ ] Risk mitigation plan in place

---

## Audit Results

**Audit Date:** [TO BE FILLED BY OPERATIONS TEAM]  
**Conducted By:** [NAME/TEAM]  
**Overall Status:** ⚠️ IN PROGRESS / ✅ COMPLETE / ❌ BLOCKED

### Critical Blockers
- [ ] None identified
- [ ] SonarQube version too old (upgrade required)
- [ ] Tool unavailable (specify: Stryker / Pitest / mutmut / cosmic-ray)
- [ ] CI/CD integration not feasible
- [ ] Performance unacceptable (>20% overhead)

### Conditional Approvals
- [ ] Performance acceptable but optimization recommended
- [ ] Some tools unavailable; pilot scope reduced
- [ ] SonarQube upgrade required but scheduled

### Sign-Off
- **DevOps Lead:** _________________ Date: _______
- **SonarQube Admin:** _________________ Date: _______
- **Crew-Scheduling Tech Lead:** _________________ Date: _______
- **Dispatch Tech Lead:** _________________ Date: _______

---

## Next Steps

Once audit is COMPLETE:
1. Document all findings in this file (replace [TO BE FILLED] placeholders)
2. Provide audit results to governance review (attach as CODEBASE-AUDIT-RESULTS.md)
3. Proceed with REVISION 3 proposal if all critical items PASS
4. If blockers exist: Document as conditions for future remediation
5. If conditional: Proceed with reduced pilot scope (e.g., crew-scheduling only)
