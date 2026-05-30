# Tasks: IOC_ALP C++ Avatar Enrichment

> **Proposal:** [PROPOSAL.md](./PROPOSAL.md)
> **Spec scenario IDs:** ALP-01 through ALP-10
> **Branch:** `proposal/alp-cpp-avatar-enrichment`
> **Workflow:** Avatar Workflow Mode 4 (Enrich) — constitutional TDD cycle per ENG-4.1
> **Source:** `AAInternal/IOC_ALP` (PCLoadPlan, C++98, MSVC, MFC Windows)

Each task follows RED → GREEN → REFACTOR → VERIFY → COMMIT. Test file: `tests/unit/test_cpp_avatar/test_alp_enrichment.py`

---

## Progress Summary

**Completed:** 10 / 10
**In Progress:** 0 / 10
**Blocked:** 0 / 10

---

## Tasks

- [x] **ALP-01** — `manifest brownfield_msvc_build commands` ✓ `b4139f2`
  Scenario: `test_manifest_has_brownfield_msvc_build_commands`
  - Test: manifest `commands` block contains `brownfield_msvc_build` key with `msbuild ALPGUI.sln`
  - File: `avatars/technology/cpp/manifest.yaml`

- [x] **ALP-02** — `manifest brownfield_mfc_stack dependencies` ✓ `4d75b49`
  Scenario: `test_manifest_has_brownfield_mfc_stack_dependencies`
  - Test: manifest `dependencies` block contains `brownfield_mfc_stack` key with AACCSAPI / MFC / TinyXML2 / culib
  - File: `avatars/technology/cpp/manifest.yaml`

- [x] **ALP-03** — `manifest brownfield_mfc_cpp98 naming conventions` ✓ `d00e1d6`
  Scenario: `test_manifest_has_brownfield_mfc_cpp98_naming_conventions`
  - Test: manifest `conventions` block contains `brownfield_mfc_cpp98` key with C prefix, Manager/Controller/Task suffixes, RCPtr
  - File: `avatars/technology/cpp/manifest.yaml`

- [x] **ALP-04** — `manifest brownfield_winforms_desktop project archetype` ✓ `743c4db`
  Scenario: `test_manifest_project_archetypes_has_brownfield_winforms_desktop`
  - Test: manifest `activates.project_archetypes` contains `brownfield_winforms_desktop` with alpsource/, Thread Classes/, ALPGUI.sln
  - File: `avatars/technology/cpp/manifest.yaml`

- [x] **ALP-05** — `ENG-2.3 RCPtr ABI stability example` ✓ `a3cadfe`
  Scenario: `test_rcptr_abi_stability_example_exists`
  - Test: `examples/ENG-2.3-rcptr-abi-stability.md` exists, contains RCPtr/RCObject/addReference, ≤850 tokens
  - File: `avatars/technology/cpp/examples/ENG-2.3-rcptr-abi-stability.md` (new)

- [x] **ALP-06** — `ENG-6.1 host exception safety example` ✓ `01a665b`
  Scenario: `test_host_exception_safety_example_exists`
  - Test: `examples/ENG-6.1-host-exception-safety.md` exists, contains CALPException/CHostException/catch, ≤850 tokens
  - File: `avatars/technology/cpp/examples/ENG-6.1-host-exception-safety.md` (new)

- [x] **ALP-07** — `ENG-4.1 atomic-tdd example has Windows/MFC section` ✓ `a23ff3d`
  Scenario: `test_atomic_tdd_example_has_windows_mfc_section`
  - Test: `examples/ENG-4.1-atomic-tdd.md` contains `Windows` or `MFC` or `ActiveTest` section
  - File: `avatars/technology/cpp/examples/ENG-4.1-atomic-tdd.md` (update)

- [x] **ALP-08** — `full-reference.md Load Planning domain section` ✓ `fca1303`
  Scenario: `test_full_reference_has_load_planning_section`
  - Test: `full-reference.md` contains `## Load Planning` heading with ZFW/CG/MEL/CSAPI markers
  - File: `docs/guides/avatars/cpp/full-reference.md` (update)

- [x] **ALP-09** — `full-reference.md MFC/Windows brownfield governance section` ✓ `77d4c0c`
  Scenario: `test_full_reference_has_mfc_windows_section`
  - Test: `full-reference.md` contains `## MFC` heading with RCPtr/Observer/Command markers
  - File: `docs/guides/avatars/cpp/full-reference.md` (update)

- [x] **ALP-10** — `full-reference.md IOC_ALP anti-pattern catalog` ✓ `adb4a42`
  Scenario: `test_full_reference_has_alp_anti_pattern_catalog`
  - Test: `full-reference.md` contains `## IOC_ALP Anti-Pattern` heading with god class/macro/mixed ownership markers
  - File: `docs/guides/avatars/cpp/full-reference.md` (update)
