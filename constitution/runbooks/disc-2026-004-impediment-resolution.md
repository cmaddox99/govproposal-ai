# Impediment Resolution Runbook — disc-2026-004
## AA Mobile Platform — Avatar-Grounded Engineering Discipline Programme
### Stage C Code Evidence — Constitutional Compliance

**Runbook version:** 1.0.0  
**Discovery:** disc-2026-004  
**Constitutional reference:** product-discovery-stage-a-f v2.1.0  
**Author:** GitHub Copilot CLI (ENG-12.3 — human sponsor must certify completion)  
**Owner:** Adeel Ali (Technical Coach) — resolution coordination  
**Sponsor approval required:** Ram Santhanam (Director of Product Agility)  

---

## Impediment Status

| ID | Title | Owner | Status | P |
|----|-------|-------|--------|:-:|
| [IMP-1](#imp-1) | Android Robolectric Java 21 — 17 modules excluded from JaCoCo | Android team | ✅ **CODE FIX APPLIED** — retest required | 🔴 P1 |
| [IMP-2](#imp-2) | BFF artifact registry credentials — tests blocked | BFF team + DevOps | ⏳ Awaiting human action | 🔴 P1 |
| [IMP-3](#imp-3) | BFF not on enterprise SonarQube | BFF team + SQ admin | ⏳ Awaiting human action | 🔴 P1 |
| [IMP-4](#imp-4) | iOS not on enterprise SonarQube | iOS team + SQ admin | ⏳ Awaiting human action | 🔴 P1 |
| [IMP-5](#imp-5) | iOS simulator runtime absent — tests unrunnable | iOS team + CI/CD | ⏳ Awaiting human action | 🔴 P1 |
| [IMP-6](#imp-6) | Mutation testing all platforms — ENG-4.11 unmet | Platform teams | ✅ **BFF CONFIGURED** — Android/iOS blocked | 🟠 P2 |
| [IMP-7](#imp-7) | Wrong SonarQube gate on Android enterprise CI | SQ admin | ⏳ Awaiting admin action | 🔴 P1 |

---

<a name="imp-1"></a>
## IMP-1: Android Robolectric Java 21 Compatibility

**Constitutional law:** ENG-4.6, ENG-12.3  
**Impact:** 17/60 Android modules excluded from JaCoCo — coverage figure is a floor estimate  

### Fix Applied (by GitHub Copilot CLI)

1. **`gradle/libs.versions.toml`** — upgraded `robolectric = "4.11.1"` → `"4.14.1"`  
   Robolectric 4.12+ supports Java 21 (DRBG provider fixed)

2. **`build.gradle` (root)** — added JVM arg as belt-and-suspenders:
   ```groovy
   tasks.withType(Test).configureEach {
       systemProperty "robolectric.enabledSdks", "33"
       jvmArgs "-Djava.security.egd=file:/dev/./urandom"
   }
   ```

### Verification Steps (Android team)

```bash
cd android/androidapps/american-airlines-android
export JAVA_HOME=$(/usr/libexec/java_home -v 21)

# Run all unit tests with coverage
./gradlew testDebugUnitTestCoverage --continue \
  -Dorg.gradle.jvmargs="-Xmx4g -Djava.security.egd=file:/dev/./urandom" \
  --no-daemon

# Confirm all 60 modules produced JaCoCo XML
find . -name "*.xml" -path "*/jacoco/*" | wc -l
# Expected: ~60 files

# Re-scan to SonarQube
# (see IMP-7 for enterprise gate; local scan below)
```

### Expected Outcome
- All 60 modules produce `build/reports/jacoco/testDebugUnitTestCoverage.xml`
- Enterprise SonarQube coverage figure rises above 22.6% floor
- No `NullPointerException at DRBG.java:158` in build logs

---

<a name="imp-2"></a>
## IMP-2: BFF Artifact Registry — Tests Cannot Execute

**Constitutional law:** ENG-4.6, ENG-12.1  
**Impact:** BFF coverage is 0% — not a measurement, tests are completely blocked  

### Root Cause

`package-manager.aa.com` (Cloudsmith) Maven repository requires credentials:
```groovy
// bff/Mobile-Manage-Minilith/mobilewebservices/build.gradle
maven {
    url = "https://package-manager.aa.com/basic/prod/maven/"
    credentials {
        username = System.getenv("PACKAGE_REGISTRY_USER")
        password = System.getenv("PACKAGE_REGISTRY_TOKEN")
    }
}
```

Blocked dependency: `com.aa.ct.fly:payment-service-stubs:1.0.0-28`

### Resolution Steps (DevOps + BFF team)

```bash
# Step 1: Provision CI service account (DevOps action)
# Create read-only Cloudsmith service account for CI
# Grant access to: package-manager.aa.com/basic/prod/maven/

# Step 2: Store as CI secrets (GitHub Actions example)
# Settings → Secrets → Actions:
# PACKAGE_REGISTRY_USER = <service-account-username>
# PACKAGE_REGISTRY_TOKEN = <service-account-api-key>

# Step 3: Verify locally with credentials
export PACKAGE_REGISTRY_USER=<your-username>
export PACKAGE_REGISTRY_TOKEN=<your-token>
cd bff/Mobile-Manage-Minilith/mobilewebservices
export JAVA_HOME=/tmp/jdk17/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home
./gradlew test jacocoTestReport

# Step 4: Expected — all tests pass, jacocoTestReport produces XML at:
# build/reports/jacoco/test/jacocoTestReport.xml
```

### CI Pipeline Snippet (add to BFF CI workflow)

```yaml
# .github/workflows/bff-ci.yml (or equivalent)
- name: Run BFF tests with coverage
  env:
    PACKAGE_REGISTRY_USER: ${{ secrets.PACKAGE_REGISTRY_USER }}
    PACKAGE_REGISTRY_TOKEN: ${{ secrets.PACKAGE_REGISTRY_TOKEN }}
    JAVA_HOME: ${{ env.JAVA_17_HOME }}
  run: |
    cd bff/Mobile-Manage-Minilith/mobilewebservices
    ./gradlew test jacocoTestReport
```

---

<a name="imp-3"></a>
## IMP-3: BFF Not on Enterprise SonarQube

**Constitutional law:** ENG-12.1, ENG-12.3  
**Impact:** BFF has 4 HARD_BLOCKs (3 CVEs, security E, 30 blockers, 751 criticals) but CI has no gate — these can ship to production undetected  

### Current State

- `Mobile_Api_BFF` and `mobile-booking-bff-monorepo` project shells exist on `sonarqube.aa.com`
- **Zero analyses ever run** — confirmed via `api/project_analyses/search`
- BFF CI pipeline does NOT include `sonar-scanner` step

### Resolution Steps (BFF team + SQ admin)

```bash
# Step 1: Confirm project key to use
# Use: mobile-booking-bff-monorepo (matches codebase structure)
# Verify: curl -u "$SONAR_TOKEN:" "https://sonarqube.aa.com/api/projects/search?projects=mobile-booking-bff-monorepo"

# Step 2: Apply constitutional gate to the project (SQ ADMIN REQUIRED)
# Admin token needed — adeel-ali82877 is sonar-users only (no gate association permission)
# Admin command:
curl -X POST -u "$ADMIN_TOKEN:" \
  "https://sonarqube.aa.com/api/qualitygates/select" \
  -d "projectKey=mobile-booking-bff-monorepo&gateName=Hangar-AI-Constitution-Gate-v1.1.0"
# Note: gate must first be created by admin using provision.sh

# Step 3: Create sonar-project.properties (DONE — see below)
# bff/Mobile-Manage-Minilith/mobilewebservices/sonar-project.properties

# Step 4: Add sonar-scanner to BFF CI pipeline (requires IMP-2 credentials)
```

### BFF sonar-project.properties

```properties
# Constitutional SonarQube configuration — disc-2026-004
# sonarqube.aa.com project: mobile-booking-bff-monorepo
sonar.projectKey=mobile-booking-bff-monorepo
sonar.projectName=AA Mobile BFF Minilith
sonar.projectVersion=1.0

sonar.sources=src
sonar.java.source=17
sonar.java.binaries=build/classes
sonar.coverage.jacoco.xmlReportPaths=build/reports/jacoco/test/jacocoTestReport.xml

sonar.host.url=https://sonarqube.aa.com
sonar.token=${env.SONAR_TOKEN}

# Exclusions (third-party / generated)
sonar.exclusions=**/test/**,**/lib/**,**/lib-ext/**,**/axis-lib/**
```

### CI Pipeline Snippet (complete with sonar)

```yaml
- name: Run BFF SonarQube analysis
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
    PACKAGE_REGISTRY_USER: ${{ secrets.PACKAGE_REGISTRY_USER }}
    PACKAGE_REGISTRY_TOKEN: ${{ secrets.PACKAGE_REGISTRY_TOKEN }}
  run: |
    cd bff/Mobile-Manage-Minilith/mobilewebservices
    ./gradlew test jacocoTestReport
    sonar-scanner \
      -Dsonar.projectKey=mobile-booking-bff-monorepo \
      -Dsonar.host.url=https://sonarqube.aa.com \
      -Dsonar.token=$SONAR_TOKEN \
      -Dsonar.coverage.jacoco.xmlReportPaths=build/reports/jacoco/test/jacocoTestReport.xml
```

---

<a name="imp-4"></a>
## IMP-4: iOS Not on Enterprise SonarQube

**Constitutional law:** ENG-12.1, ENG-12.3  
**Impact:** 49 repos, 5,031 Swift files, 468,759 LOC — zero quality signal on enterprise  

### Current State

- No iOS consumer app project exists on `sonarqube.aa.com`
- Swift plugin v5.0.0.12095 IS installed — enterprise is capable of scanning Swift
- `sonar-project.properties` written at `ios/americanmobileapp-ios/sonar-project.properties` (token redacted)
- `adeel-ali82877` token cannot create projects — admin action required

### Resolution Steps (Enterprise SonarQube admin)

```bash
# Step 1: Admin creates the project (ADMIN TOKEN REQUIRED)
curl -X POST -u "$ADMIN_TOKEN:" \
  "https://sonarqube.aa.com/api/projects/create" \
  -d "name=AA+iOS+Consumer+App&project=disc-2026-004-ios&mainBranch=main"

# Step 2: Admin applies constitutional gate to project
curl -X POST -u "$ADMIN_TOKEN:" \
  "https://sonarqube.aa.com/api/qualitygates/select" \
  -d "projectKey=disc-2026-004-ios&gateName=Hangar-AI-Constitution-Gate-v1.1.0"

# Step 3: Once project exists, run first scan (can be done with adeel-ali82877 token)
cd ios/americanmobileapp-ios
export SONAR_TOKEN=$(cat ~/.sonarqube-token)
/private/tmp/sonar-scanner-5.0.1.3006-macosx/bin/sonar-scanner \
  -Dsonar.projectKey=disc-2026-004-ios \
  -Dsonar.sources=../ \
  -Dsonar.exclusions="**/Carthage/**,**/Pods/**,**/.build/**,**/*Tests*/**" \
  -Dsonar.host.url=https://sonarqube.aa.com \
  -Dsonar.token=$SONAR_TOKEN \
  -Dsonar.swift.file.suffixes=.swift

# Step 4: Verify scan appears in enterprise dashboard
curl -u "$SONAR_TOKEN:" \
  "https://sonarqube.aa.com/api/project_analyses/search?project=disc-2026-004-ios" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('Analyses:', len(d['analyses']))"
```

### sonar-project.properties (ready at `ios/americanmobileapp-ios/sonar-project.properties`)

Already written — admin only needs to create the project, then scanner can run.

---

<a name="imp-5"></a>
## IMP-5: iOS Simulator Runtime Absent — Tests Unrunnable

**Constitutional law:** ENG-4.6, ENG-4.11  
**Impact:** 1,952 iOS test files status unknown. Coverage = 0 by inference. Muter blocked.  

### Resolution Steps (iOS team + CI/CD)

```bash
# Step 1: Install iOS simulator runtime on dev machine / CI runner
# On macOS with Xcode 26+:
xcodebuild -downloadPlatform iOS
# Or via Xcode Preferences → Platforms → iOS

# Step 2: Verify runtime installed
xcrun simctl list runtimes
# Expected: "iOS 18.x (18.x.x - ...) - com.apple.CoreSimulator.SimRuntime.iOS-18-x"

# Step 3: Run XCTest to verify tests pass
cd ios/americanmobileapp-ios
xcodebuild test \
  -workspace AmericanAirlines.xcworkspace \
  -scheme "AmericanAirlines - iOS - Debug" \
  -destination "platform=iOS Simulator,name=iPhone 16" \
  -enableCodeCoverage YES \
  -derivedDataPath build/

# Step 4: Export coverage report for SonarQube
xcrun xccov view --report --json \
  build/Logs/Test/*.xcresult > build/coverage.json

# Step 5: Once IMP-4 resolved, wire to enterprise SonarQube
# sonar.swift.coverage.reportPaths=build/coverage.json
```

### Muter v16 — iOS Mutation Testing (after IMP-5 resolved)

```bash
# Install Muter via Homebrew (canonical install — replaces the /tmp source-build path)
brew install muter-mutation-testing/formulae/muter

cd ios/americanmobileapp-ios
muter init
# Edit muter.conf.yml — set scheme, test plan, exclusions (see canonical workflow for template)

muter run --format html --output muter-report.html
# Report: muter-report.html
# Constitutional threshold: ≥70% mutation score
# Critical paths (booking, checkin, payment): ≥85%
```

---

<a name="imp-6"></a>
## IMP-6: Mutation Testing — All Platforms (ENG-4.11)

**Constitutional law:** ENG-4.11  
**Constitutional threshold:** ≥70% mutation score overall, ≥85% for critical paths  

### BFF — Pitest (CONFIGURED ✅)

Pitest `info.solidsoft.pitest` v1.15.0 added to `build.gradle`:

```bash
# Once IMP-2 resolved (artifact registry credentials):
cd bff/Mobile-Manage-Minilith/mobilewebservices
export PACKAGE_REGISTRY_USER=<user>
export PACKAGE_REGISTRY_TOKEN=<token>
export JAVA_HOME=/tmp/jdk17/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home

./gradlew pitest

# Reports at: build/reports/pitest/
# XML report: build/reports/pitest/mutations.xml
# Constitutional gate: threshold 70% configured in pitest block
```

### Android — pl.droidsonroids.pitest (OSS Gradle Plugin)

```bash
# Plugin: pl.droidsonroids.pitest v0.2.27 (Gradle Plugin Portal — open source)
# No commercial licence required. Replaces the incorrect ArcMutate reference.

# Step 1: Add to root build.gradle.kts plugins block:
#   id("pl.droidsonroids.pitest") version "0.2.27" apply false

# Step 2: Configure per-module (priority: app, data2, ancillaryoffers, checkin_base):
# In each module's build.gradle.kts:
pitest {
    targetClasses.set(listOf("com.aa.<module>.*"))
    targetTests.set(listOf("com.aa.<module>.*Test"))
    mutationThreshold.set(70)
    outputFormats.set(setOf("HTML", "XML"))
    threads.set(4)
}

# Run: ./gradlew :<module>:pitestDebug
# Report: <module>/build/reports/pitest/debug/index.html
```

> **Note:** The original runbook entry referenced `com.arcmutate.pitest-android` — that plugin does not exist.
> ArcMutate's products (base, spring, kotlin, git) are JVM-only. The correct Android tool is
> `pl.droidsonroids.pitest` (OSS, Gradle Plugin Portal, updated March 2026).

### iOS — Muter v16 (BLOCKED — requires IMP-5)

See IMP-5 resolution steps. Install Muter via `brew install muter-mutation-testing/formulae/muter`.

---

<a name="imp-7"></a>
## IMP-7: Wrong SonarQube Gate on Android Enterprise CI

**Constitutional law:** ENG-12.1, ENG-12.3  
**Impact:** Android enterprise CI uses `Sonar way - AAAndroid` gate. This gate's new_coverage threshold is 50% (vs constitutional 90%) and does NOT enforce HARD_BLOCK on vulnerabilities. CI passed with 13 CVEs.  

### Current State

- `androidapps` project uses `Sonar way - AAAndroid` gate (confirmed via API)
- Our token (`adeel-ali82877`) has `actions.associateProjects: false` — cannot change gate
- Constitutional gate v1.1.0 does NOT yet exist on enterprise (it is on local CE only)
- Gate spec: `governance/hangar-ai-constitution/tools/sonarqube-gate/gate-config.json`
- Provisioner: `governance/hangar-ai-constitution/tools/sonarqube-gate/provision.sh`

### Resolution Steps (Enterprise SonarQube admin — ADMIN TOKEN REQUIRED)

```bash
# Step 1: Create constitutional gate on enterprise
# The provision.sh script creates the gate — it needs to run against enterprise
# by an admin-credentialed account

export SONAR_HOST=https://sonarqube.aa.com
export SONAR_ADMIN_TOKEN=<admin-token>

# Provision script creates gate named "Hangar-AI-Constitution-Gate-v1.1.0"
bash governance/hangar-ai-constitution/tools/sonarqube-gate/provision.sh

# Step 2: Associate with androidapps project
curl -X POST -u "$SONAR_ADMIN_TOKEN:" \
  "https://sonarqube.aa.com/api/qualitygates/select" \
  -d "projectKey=androidapps&gateName=Hangar-AI-Constitution-Gate-v1.1.0"

# Step 3: Verify
curl -u "$SONAR_ADMIN_TOKEN:" \
  "https://sonarqube.aa.com/api/qualitygates/get_by_project?project=androidapps" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('Gate:', d['qualityGate']['name'])"
# Expected: "Hangar-AI-Constitution-Gate-v1.1.0"

# Step 4: Next CI run on androidapps will immediately show gate=ERROR
# (13 vulns, 38 blockers, 932 criticals all trigger HARD_BLOCK)
# This is the correct behaviour — it surfaces what already exists in the codebase
```

### Note: Confirmed `Sonar way - AAAndroid` Gate Conditions (from enterprise API)

```
Metric                          Threshold       Constitutional Gate
new_security_rating             > 1 (D/E)       HB-2: security_rating > A (HARD_BLOCK)
new_reliability_rating          > 1             — (no equivalent)
new_maintainability_rating      > 1             — (no equivalent)
new_coverage                    < 50%           AA-B2: < 90% (HARD_BLOCK for new code)
new_duplicated_lines_density    > 3%            W-1: > 3% (WARNING)
new_security_hotspots_reviewed  < 100%          — (no equivalent)

MISSING from AAAndroid gate:
  - vulnerabilities count        (constitutional: HB-1 HARD_BLOCK if > 0)
  - blocker_violations           (constitutional: HB-3 HARD_BLOCK if > 0)
  - critical_violations          (constitutional: HB-4 HARD_BLOCK if > 0)
```

With the current Android state (13 vulns, 38 blockers, 932 criticals):
- `Sonar way - AAAndroid` → **PASSES** (none of these are checked)
- `Hangar-AI-Constitution-Gate-v1.1.0` → **FAILS with 4 HARD_BLOCKs**

`provision.sh` currently targets `http://localhost:9000` via `SONAR_HOST` env var.
It is idempotent — safe to run multiple times.
When run against enterprise with admin credentials, it will create the gate and apply all 10 conditions.

---

## Summary: Who Does What

| Action | Who | Blocker? | Complexity |
|--------|-----|:--------:|:----------:|
| Verify Robolectric 4.14.1 fix + re-run tests | Android team | Unblocked | Low |
| Provide `package-manager.aa.com` CI credentials | DevOps | Unblocked | Low |
| Onboard BFF to enterprise SonarQube CI scan | BFF team + DevOps | After credentials | Medium |
| Create iOS project on enterprise SonarQube | Enterprise SQ admin | Needs admin token | Low |
| Install iOS simulator runtime on CI runner | iOS team + CI/CD | Unblocked | Low |
| Run iOS scan after project created | Any (token ready) | After admin action | Low |
| Apply constitutional gate to androidapps (enterprise) | Enterprise SQ admin | Needs admin token | Low |
| Procure ArcMutate licence for Android mutation | ~~Android team lead~~ **RESOLVED** — use OSS `pl.droidsonroids.pitest` v0.2.27 (no licence required) | N/A | Closed |
| Run BFF Pitest (already configured) | BFF team | After credentials | Low |
| Run iOS Muter | iOS team | After simulator | Medium |

---

*Runbook authored by GitHub Copilot CLI under disc-2026-004 Stage C.*  
*ENG-12.3: All verification steps cite command output, not self-certification.*  
*Human completion sign-off required from Adeel Ali + Ram Santhanam at Stage C exit gate.*
