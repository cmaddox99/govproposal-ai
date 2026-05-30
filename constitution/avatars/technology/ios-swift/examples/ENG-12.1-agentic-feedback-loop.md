---
law_id: ENG-12.1
avatar: ios-swift
non_negotiable: true
---

# ENG-12.1: Agentic Feedback Loop Law — iOS (Swift)

> **Law:** The Constitutional Gate (SonarQube) MUST be provisioned before any workflow phase begins. The agent cannot advance phases without a human reviewing gate results on the dashboard.

---

## iOS Context

iOS module repos are individual Swift packages with their own CI pipeline. ENG-12.1 applies at the module level — each repo runs a SonarQube scan as a gate before a framework release is created.

---

## COMPLIANT: Gate Flow for iOS Feature Development

```
┌─────────────────────────────────────────────────────────────────┐
│  Constitutional Gate Flow — iOS Swift Module                     │
│                                                                  │
│  1. Agent opens hangar-ai-specs/ for the feature                 │
│  2. SonarQube scan provisioned and dashboard confirmed OPEN      │
│     → bundle exec fastlane run_unit_tests                        │
│     → ./gradlew sonarqube (or sonar-scanner for Swift)           │
│  3. Agent completes phase work                                   │
│  4. Agent reports API gate result                                │
│  5. HUMAN reviews SonarQube dashboard ← NON-NEGOTIABLE STEP     │
│  6. Human approves phase advance                                 │
│  7. Agent proceeds to next phase                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## COMPLIANT: Pre-Phase SonarQube Check in CI (Fastfile)

```ruby
# Tooling/fastlane/Fastfile
lane :constitutional_gate do
  # ENG-12.1: scan must run before framework release
  sh "sonar-scanner \
    -Dsonar.projectKey=#{ENV['SONAR_PROJECT_KEY']} \
    -Dsonar.sources=Sources/ \
    -Dsonar.swift.coverage.reportPaths=fastlane/test_output/coverage.xml \
    -Dsonar.login=#{ENV['SONAR_TOKEN']}"

  UI.message("🔍 ENG-12.1: Review gate status at #{ENV['SONAR_DASHBOARD_URL']}")
  UI.user_error!("Human must confirm dashboard gate PASS before release") unless ENV['GATE_CONFIRMED'] == 'true'
end

lane :create_framework_release do
  # Gate check must precede release — ENG-12.1
  constitutional_gate
  # ... release steps
end
```

---

## COMPLIANT: `.sonar-token` gitignored

```
# .gitignore
.sonar-token
sonar-project.properties  # contains auth details
fastlane/report.xml        # local only
```

---

## VIOLATION: Phase Advance Without Dashboard Review

```swift
// ❌ Workflow violation — agent declared phase complete based on API result only
// Agent: "SonarQube API returned { qualityGateStatus: 'OK' }"
// Agent proceeds to Phase 6 commit ← VIOLATION of ENG-12.1

// Correct: API result is not the checkpoint.
// Human MUST open dashboard and confirm gate PASS before agent advances.
// One failing condition: "NEW_COVERAGE < 80%" may show WARN in API but FAIL on dashboard
```

**Why ENG-12.1 non-negotiable:** API results can be cached, stale, or scoped differently from the dashboard view. The human reviewing the live dashboard is the constitutional contract — not the API call.

---

## Phase Gate Triggers for iOS

| Phase | Human Action Required |
|---|---|
| Before new feature spec | Confirm SonarQube project visible for this module |
| Before Phase 4 (Build) | Review baseline scan on dashboard |
| Before Phase 6 (Commit) | Confirm gate PASS on dashboard |
| Framework release | `GATE_CONFIRMED=true` env var set by human after dashboard review |
