---
law_id: ENG-12.1
avatar: android-kotlin
non_negotiable: true
---

# ENG-12.1: Agentic Feedback Loop Law — Android (Kotlin)

> **Law:** The Constitutional Gate (SonarQube) MUST be provisioned before any workflow phase begins. The agent cannot advance phases without a human reviewing gate results on the dashboard.

---

## Android Context

`sonarqube.gradle` exists in `android/androidapps/american-airlines-android/`. SonarQube is integrated into the AA Android CI pipeline. ENG-12.1 mandates that the human engineer opens the dashboard and reviews gate status before any phase advance — not just relies on the API call result.

---

## COMPLIANT: Gate Flow for Android Feature Development

```
┌─────────────────────────────────────────────────────────────────┐
│  Constitutional Gate Flow — Android Kotlin Module                │
│                                                                  │
│  1. Agent opens hangar-ai-specs/ for the feature                 │
│  2. SonarQube dashboard confirmed OPEN by human                  │
│  3. Agent completes phase work                                   │
│  4. Agent runs: ./gradlew sonarqube (uses sonarqube.gradle)      │
│  5. Agent reports API gate result                                │
│  6. HUMAN reviews SonarQube dashboard ← NON-NEGOTIABLE STEP     │
│  7. Human approves phase advance                                 │
│  8. Agent proceeds to next phase                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## COMPLIANT: SonarQube Scan in CI

```bash
# Run SonarQube gate scan (AA Android — sonarqube.gradle applies)
./gradlew sonarqube \
  -Dsonar.host.url=$SONAR_HOST_URL \
  -Dsonar.login=$SONAR_TOKEN \
  -Papp.isJenkins=true

# ENG-12.1: after scan completes, human MUST review dashboard at:
# $SONAR_HOST_URL/dashboard?id=com.aa.android
```

```groovy
// sonarqube.gradle — AA Android SonarQube configuration (already present in repo)
sonarqube {
    properties {
        property "sonar.projectKey", "com.aa.android"
        property "sonar.sources", "american-airlines-android"
        property "sonar.java.coveragePlugin", "jacoco"
        property "sonar.coverage.jacoco.xmlReportPaths",
            "american-airlines-android/app/build/reports/jacoco/**/*.xml"
    }
}
```

---

## COMPLIANT: `.sonar-token` gitignored

```
# .gitignore
.sonar-token
local.properties   # contains local SDK paths and any injected tokens
```

---

## VIOLATION: Phase Advance Without Dashboard Review

```kotlin
// ❌ Workflow violation
// Agent: "./gradlew sonarqube completed with qualityGateStatus: OK"
// Agent proceeds to commit ← VIOLATION of ENG-12.1

// Correct: SonarQube API status is not the compliance checkpoint.
// Human MUST open the dashboard, verify the gate, then authorise.
// dashboard shows flaky test coverage exclusions that API doesn't flag
```

**Why ENG-12.1 non-negotiable:** API-level gate results can miss module-level exclusions or cached project states visible only on the dashboard. The human reviewing the dashboard is the constitutional contract.

---

## Phase Gate Triggers for Android

| Phase | Human Action Required |
|---|---|
| Before new feature spec | Confirm `sonarqube.gradle` project visible on dashboard |
| Before Phase 4 (Build) | Review baseline scan; note any existing gate violations |
| Before Phase 6 (Commit) | Confirm gate PASS on dashboard before merge |
| Release build | Coverage delta reviewed on dashboard; `GATE_CONFIRMED=true` before deploy |
