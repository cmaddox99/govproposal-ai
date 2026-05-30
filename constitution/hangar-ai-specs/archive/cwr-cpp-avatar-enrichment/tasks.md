# Tasks: CWR C++ Avatar Enrichment

> **Proposal:** [PROPOSAL.md](./PROPOSAL.md)
> **Spec scenario IDs:** CWR-01 through CWR-10
> **Branch:** `proposal/cwr-cpp-avatar-enrichment`
> **Workflow:** Avatar Workflow Mode 4 (Enrich) — constitutional TDD cycle per ENG-4.1

Each task follows RED → GREEN → REFACTOR. Test file: `tests/unit/test_cpp_avatar/test_cwr_enrichment.py`

---

## Progress Summary

**Completed:** 10 / 10
**In Progress:** 0 / 10
**Blocked:** 0 / 10

---

## Tasks

- [x] **CWR-01** — `manifest brownfield_makefile commands` ✓
  Scenario: `test_manifest_has_brownfield_makefile_commands`
  - Test: manifest `commands` block contains a `brownfield_makefile` key with `make -f nbproject/Makefile-CI-Release.mk`
  - File: `avatars/technology/cpp/manifest.yaml`

- [x] **CWR-02** — `manifest brownfield_jni_stack dependencies` ✓ `8e35d1d`
  Scenario: `test_manifest_has_brownfield_jni_stack_dependencies`
  - Test: manifest `dependencies` block contains `brownfield_jni_stack` key with `xpress` / `jsoncpp` / `TinyXML` / `JNI`
  - File: `avatars/technology/cpp/manifest.yaml`

- [x] **CWR-03** — `manifest brownfield_cpp98 naming conventions` ✓ `ebadfff`

- [x] **CWR-04** — `manifest brownfield_jni_solver project structure` ✓ `eec58f7`

- [x] **CWR-05** — `ENG-2.3 JNI ABI stability example` ✓ `bd22786`

- [x] **CWR-06** — `ENG-6.1 safety-critical JNI example` ✓ `fb45b46`

- [x] **CWR-07** — `ENG-4.1 brownfield characterization test section` ✓ `be7d567`

- [x] **CWR-08** — `full-reference.md JNI safety section` ✓ `e5a4ce2`

- [x] **CWR-09** — `full-reference.md FAR 117 aviation safety section` ✓ `d0abef9`

- [x] **CWR-10** — `full-reference.md CWR anti-pattern catalog` ✓ `3f45a73`
  Scenario: `test_full_reference_has_cwr_antipattern_catalog`
  - Test: `docs/guides/avatars/cpp/full-reference.md` contains `Anti-Pattern` section with at least 5 named anti-patterns
  - File: `docs/guides/avatars/cpp/full-reference.md` (update)
