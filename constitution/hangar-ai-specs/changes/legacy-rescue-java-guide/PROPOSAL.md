# Author: `legacy-rescue-java.md` — Java/Spring Boot Avatar Guide

**Status:** 🔨 IMPLEMENT
**Spec ID:** `legacy-rescue-java-guide`
**Laws:** ENG-10.1 (Constitution Metrics — file reference integrity), ENG-6.7 (Audit Trail)
**Branch:** `fix/legacy-rescue-java-guide`
**Type:** Bug fix (missing file that breaks ENG-10.1 lint gate)

---

## Problem

`avatars/technology/java-spring/manifest.yaml` declares:

```yaml
activates:
  workflow_guides:
    legacy-rescue-refactor: legacy-rescue-java.md
```

`avatars/AVATAR-RAG-INDEX.yaml` indexes this as:

```yaml
legacy_rescue: legacy-rescue-java.md
```

The file `avatars/technology/java-spring/legacy-rescue-java.md` was **never created**.
This causes an ENG-10.1 lint failure on every PR since the broken reference was introduced
in commit `23863053` (2026-04-27, BFF enrichment session).

The file was a forward declaration of intent — the java-spring avatar *should* carry a
Java-specific enrichment of the generic `workflows/legacy-rescue-refactor.md` workflow.
The `legacy-rescue-refactor.md` workflow itself explicitly references this file:

> "The Java/Spring Boot avatar contains additional Java-specific patterns and a
> `legacy-rescue-java.md` guide enriched from live runs."

## Fix

Author `avatars/technology/java-spring/legacy-rescue-java.md` containing:

- Java/Spring Boot tool command translations for each workflow phase (Maven/Gradle, JaCoCo,
  PIT/pitest-maven, SonarQube scanner)
- AA BFF fleet–specific patterns: god-class characterization, ServiceLocator migration,
  mutable singleton remediation, copy-paste versioning
- Phase-gated SonarQube commands for the Java stack
- Mutation testing setup (`pitest-maven`) per ENG-4.12
- Known gotchas from live BFF rescue runs (2026-004: scope declaration, test level
  migration, new-class coverage gap)

## Scope

| File | Change |
|------|--------|
| `avatars/technology/java-spring/legacy-rescue-java.md` | **CREATE** — authors the missing guide |
| `tests/unit/test_java_spring_avatar/test_legacy_rescue_guide.py` | **CREATE** — RED test before file is authored |

No other files change. `manifest.yaml` and `AVATAR-RAG-INDEX.yaml` already correctly
reference the file — they require no modification.

## Success Criteria

- `aa-constitution-lint .` passes with 0 violations (ENG-10.1 gate green)
- The new test passes after the file is created
- All existing tests remain green
- Content covers all `search_queries` in `AVATAR-RAG-INDEX.yaml` that route to
  `legacy-rescue-java.md`
