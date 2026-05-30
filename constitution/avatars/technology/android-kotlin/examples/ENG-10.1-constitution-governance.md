---
law_id: ENG-10.1
avatar: android-kotlin
---

# ENG-10.1: Constitution Governance — Android Projects

> **Law:** Every AI-governed project must include a `hangar-ai-specs/` directory. The avatar manifest is the authoritative reference for which laws, patterns, and skills apply to the codebase. Agents must read the manifest before proposing changes.

---

## Required Project Structure

```
androidapps/               ← Gradle project root
  hangar-ai-specs/
    manifest-ref.yaml      ← points to the governing avatar manifest
    changes/               ← per-sprint enrichment changelogs
    overrides/             ← justified deviations (require human sign-off)
  app/
    src/
      main/kotlin/
      test/kotlin/
  lintchecks/              ← custom Android Lint rules for constitution checks
  build.gradle
```

## `manifest-ref.yaml`

```yaml
# hangar-ai-specs/manifest-ref.yaml
avatar: android-kotlin
constitution: hangar-ai-constitution
governing_laws:
  - ENG-4.1   # Atomic TDD — non-negotiable
  - ENG-10.1  # Constitution Governance — non-negotiable
  - ENG-11.1  # Spec-Driven Development — non-negotiable
  - ENG-3.1   # Complexity Limits (≤10 cyclomatic per Kotlin function)
  - ENG-3.2   # Immutability (val over var, @Immutable/@Stable for Compose)
  - ENG-6.1   # Security by Design
  - ENG-6.4   # Data Protection
last_validated: 2026-05-05
validator: hangar-ai-constitution avatar-workflow Phase 3 (Validate)
```

## CI Compliance Gates (Gradle + Jenkins)

```groovy
// lintchecks/build.gradle — register custom Lint rules
dependencies {
    compileOnly "com.android.tools.lint:lint-api:$lintVersion"
}

// app/build.gradle — wire lint to CI gate
android {
    lintOptions {
        abortOnError true
        warningsAsErrors false
        xmlReport true                     // consumed by SonarQube
        htmlReport false
        // Constitution-required checks
        enable "ConstitutionComplexity"    // ENG-3.1 — cyclomatic ≤10
        enable "ConstitutionImmutability"  // ENG-3.2 — val over var
        enable "ConstitutionLayering"      // ENG-2.2 — no Android imports in domain
    }
}
```

```groovy
// Jenkinsfile — quality gate stage
stage('Constitution Gate') {
    steps {
        sh './gradlew lint'
        sh './gradlew sonarqube -Papp.isJenkins=true'
        // Gate: SonarQube Quality Gate must be GREEN before merge
        waitForQualityGate abortPipeline: true
    }
}
```

## What Agents Do with This

Before proposing any code change in an Android repo:
1. Check for `hangar-ai-specs/manifest-ref.yaml`
2. Read the governing avatar manifest (`android-kotlin`)
3. Confirm the proposed change complies with all listed laws
4. Run `./gradlew lint` locally — zero new ENG-3.1 violations before pushing
5. If a deviation is required, log it in `hangar-ai-specs/overrides/` with justification before proceeding

## What Agents Must NOT Do

- Do not bypass the manifest lookup by assuming defaults
- Do not introduce Detekt — it is NOT configured in the live `androidapps` codebase (use ktlint + Android Lint)
- Do not add a library or pattern that conflicts with the manifest's technology stack
- Do not mark a change as compliant without having read the applicable law file
