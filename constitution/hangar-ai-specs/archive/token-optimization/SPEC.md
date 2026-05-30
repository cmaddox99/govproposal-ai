# OpenSpec: AA-Engineering-Laws Token Optimization

## Metadata

| Field | Value |
|-------|-------|
| **Proposal ID** | aa-engineering-laws-token-optimization |
| **Status** | ✅ implemented |
| **Author** | AA Engineering Team |
| **Created** | 2026-02-04 |
| **Implemented** | 2026-02-04 |
| **Target Repository** | aa-engineering-laws |
| **Reference Repository** | hangar-ai-constitution |

---

## Problem Statement

The aa-engineering-laws repository uses a **monolithic structure** that is inefficient for AI agent consumption:

1. **Single 1004-line ENGINEERING-LAWS.md** - Too large for efficient token usage, agents load entire file when only specific laws are needed
2. **Old ADOPTION.md format** for technology adoptions - Single file per technology (~650 lines each), not decomposed for selective loading
3. **Naming inconsistency** - Folder is `technology-adoptions/` but should be `technology-avatars/` to align with hangar-ai-constitution
4. **Obsolete folders** - `amendments/` and `committee/` folders are not needed in the decomposed structure
5. **No automated compliance checking** - Engineers have no way to lint their repos against the engineering laws
6. **Obsolete CONTRIBUTING.md** - File is outdated and should be removed

### Current Structure (Inefficient)

```
aa-engineering-laws/
├── CONTRIBUTING.md                  # Obsolete - REMOVE
├── amendments/                      # Obsolete - REMOVE
│   └── ...
├── committee/                       # Obsolete - REMOVE
│   └── ...
├── laws/
│   └── ENGINEERING-LAWS.md          # 1004 lines (monolithic)
├── practice-guides/
│   └── ...
└── technology-adoptions/
    ├── java-spring/
    │   └── ADOPTION.md              # 651 lines (monolithic)
    └── ... (10 total)
```

### Target Structure (Optimized)

```
aa-engineering-laws/
├── README.md                        # Updated with new structure
├── laws/
│   ├── index.yaml                   # Law registry
│   └── engineering/
│       ├── _domain.yaml             # Domain metadata
│       ├── foundations.md           # Article I
│       ├── architecture.md          # Article II
│       ├── quality.md               # Article III
│       ├── testing.md               # Article IV
│       ├── devops.md                # Article V
│       ├── security.md              # Article VI
│       ├── resiliency.md            # Article VII
│       ├── platform.md              # Article VIII
│       ├── ai-collaboration.md      # Article IX
│       └── amendments.md            # Article X
├── practice-guides/
│   ├── constitution-lint/           # NEW: Linter usage guide
│   │   └── README.md
│   └── ... (existing guides)
├── avatars/                         # Renamed from adoptions
│   ├── index.yaml                   # Avatar registry
│   ├── java-spring/
│   │   ├── manifest.yaml            # Stack config, law mappings
│   │   ├── guidance.md              # Technology-specific guidance
│   │   └── examples/
│   └── ... (6 technology avatars)
└── tools/
    └── constitution-lint/           # NEW: Compliance linter
        ├── README.md
        ├── pyproject.toml
        └── src/
```

---

## Benefits

| Benefit | Description |
|---------|-------------|
| **Token Efficiency** | Agents load only needed laws/examples, not entire monolithic files |
| **Selective Loading** | AI can fetch specific article (e.g., testing.md) without loading all laws |
| **Structured Discovery** | index.yaml enables agents to understand available resources |
| **Consistent Naming** | Aligns with hangar-ai-constitution's avatar pattern (adoptions → avatars) |
| **Better Examples** | Examples isolated by law ID for targeted retrieval |
| **Automated Compliance** | Engineers can lint repos to verify adherence to engineering laws |
| **Cleaner Structure** | Removal of obsolete folders reduces confusion |

---

## Tasks

### Phase 1: Decompose Engineering Laws

- [ ] **Task 1.1**: Create `laws/index.yaml` registry file
- [ ] **Task 1.2**: Create `laws/engineering/_domain.yaml` metadata
- [ ] **Task 1.3**: Extract Article I → `laws/engineering/foundations.md`
- [ ] **Task 1.4**: Extract Article II → `laws/engineering/architecture.md`
- [ ] **Task 1.5**: Extract Article III → `laws/engineering/quality.md`
- [ ] **Task 1.6**: Extract Article IV → `laws/engineering/testing.md`
- [ ] **Task 1.7**: Extract Article V → `laws/engineering/devops.md`
- [ ] **Task 1.8**: Extract Article VI → `laws/engineering/security.md`
- [ ] **Task 1.9**: Extract Article VII → `laws/engineering/resiliency.md`
- [ ] **Task 1.10**: Extract Article VIII → `laws/engineering/platform.md`
- [ ] **Task 1.11**: Extract Article IX → `laws/engineering/ai-collaboration.md`
- [ ] **Task 1.12**: Extract Article X → `laws/engineering/amendments.md`
- [ ] **Task 1.13**: Add YAML frontmatter with law IDs to each file
- [ ] **Task 1.14**: Archive original `ENGINEERING-LAWS.md`

### Phase 2: Transform Adoptions to Avatars

- [ ] **Task 2.1**: Rename `adoptions/` → `avatars/`
- [ ] **Task 2.2**: Create `avatars/index.yaml` registry
- [ ] **Task 2.3**: Transform java-spring/ADOPTION.md → manifest.yaml + guidance.md + examples/
- [ ] **Task 2.4**: Transform python-fastapi/ADOPTION.md → manifest.yaml + guidance.md + examples/
- [ ] **Task 2.5**: Transform nodejs-typescript/ADOPTION.md → manifest.yaml + guidance.md + examples/
- [ ] **Task 2.6**: Transform dotnet-core/ADOPTION.md → manifest.yaml + guidance.md + examples/
- [ ] **Task 2.7**: Transform react-frontend/ADOPTION.md → manifest.yaml + guidance.md + examples/
- [ ] **Task 2.8**: Transform angular-frontend/ADOPTION.md → manifest.yaml + guidance.md + examples/
- [ ] **Task 2.9**: Remove security-and-compliance/ folder (non-technology adoption)
- [ ] **Task 2.10**: Remove technology-standards/ folder (non-technology adoption)

### Phase 3: Repository Cleanup

- [ ] **Task 3.1**: Remove `amendments/` folder
- [ ] **Task 3.2**: Remove `committee/` folder
- [ ] **Task 3.3**: Remove `CONTRIBUTING.md` file

### Phase 4: Create Constitution Linter Tool

- [ ] **Task 4.1**: Create `tools/constitution-lint/` directory structure
- [ ] **Task 4.2**: Create `tools/constitution-lint/pyproject.toml` with dependencies
- [ ] **Task 4.3**: Create `tools/constitution-lint/README.md` with usage instructions
- [ ] **Task 4.4**: Create linter source code (`src/`) adapted from AA-Hangar version
- [ ] **Task 4.5**: Implement law ID validation (ENG-* references)
- [ ] **Task 4.6**: Implement test pyramid structure check (ENG-4.2)
- [ ] **Task 4.7**: Implement complexity checks (ENG-3.1)
- [ ] **Task 4.8**: Add CI/CD integration examples (GitHub Actions)

### Phase 5: Create Practice Guide for Constitution Linter

- [ ] **Task 5.1**: Create `practice-guides/constitution-lint/README.md`
- [ ] **Task 5.2**: Document installation and setup
- [ ] **Task 5.3**: Document usage examples (CLI, pre-commit, CI/CD)
- [ ] **Task 5.4**: Document all checks and their corresponding laws
- [ ] **Task 5.5**: Add troubleshooting section for common violations

### Phase 6: Update Documentation

- [ ] **Task 6.1**: Update main `README.md` with new structure and usage
- [ ] **Task 6.2**: Update `practice-guides/README.md` index
- [ ] **Task 6.3**: Update `practice-guides/ai-pairing/` references
- [ ] **Task 6.4**: Update `practice-guides/atomic-tdd/` references
- [ ] **Task 6.5**: Update `practice-guides/code-quality/` references
- [ ] **Task 6.6**: Update `practice-guides/ddd/` references
- [ ] **Task 6.7**: Update `practice-guides/test-pyramid/` references
- [ ] **Task 6.8**: Update `practice-guides/vertical-slice/` references

### Phase 7: Create Token Optimization Analysis Report

- [ ] **Task 7.1**: Create `docs/` folder in aa-engineering-laws
- [ ] **Task 7.2**: Create `docs/token-optimization-analysis.md`
- [ ] **Task 7.3**: Document before/after file structure
- [ ] **Task 7.4**: Calculate and document token counts (before vs after)
- [ ] **Task 7.5**: Document selective loading examples
- [ ] **Task 7.6**: Add usage scenarios showing token savings

### Phase 8: Validation & Finalization

- [ ] **Task 8.1**: Verify all law IDs preserved and referenced correctly
- [ ] **Task 8.2**: Verify all practice guide cross-references work
- [ ] **Task 8.3**: Run constitution-lint on repo (self-validation)
- [ ] **Task 8.4**: Final review of all documentation
- [ ] **Task 8.5**: Commit with descriptive message

---

## Acceptance Criteria

1. **Decomposed laws**: 10 separate article files + index.yaml + _domain.yaml
2. **Avatar structure**: All 6 technology adoptions transformed to manifest.yaml + guidance.md + examples/
3. **Naming alignment**: Folder renamed from `adoptions/` to `avatars/`
4. **No data loss**: All content from original files preserved
5. **YAML frontmatter**: Each law file has structured metadata with law IDs
6. **Index files**: Both laws/ and technology-avatars/ have index.yaml
7. **Cleanup complete**: amendments/, committee/, CONTRIBUTING.md removed
8. **Constitution linter**: Functional tool in tools/constitution-lint/
9. **Practice guide for linter**: Documentation in practice-guides/constitution-lint/
10. **Documentation updated**: All practice guides and README.md reflect new structure
11. **Token optimization report**: Analysis document in docs/ with before/after metrics
12. **Self-validation**: constitution-lint passes on aa-engineering-laws repo

---

## File Format Reference

### Law File Format (example: testing.md)

```markdown
---
domain: engineering
article: IV
title: Testing Laws
laws:
  - id: ENG-4.1
    title: Atomic TDD Law
    non_negotiable: true
    summary: TDD SHALL be practiced in atomic cycles
  - id: ENG-4.2
    title: Test Pyramid Law
    summary: Test suites SHALL maintain proper distribution
---

# Article IV: Testing Laws

## Section 4.1: Atomic Test-Driven Development Law
...
```

### Avatar manifest.yaml Format

```yaml
avatar:
  id: java-spring
  type: technology
  name: Java/Spring Boot
  version: "2.0.0"

stack:
  language: Java 21+
  framework: Spring Boot 3.x
  testing: [JUnit 5, Mockito, AssertJ]

specializes_laws:
  - id: ENG-4.1
    example_file: examples/ENG-4.1-atomic-tdd.md
  - id: ENG-3.1
    example_file: examples/ENG-3.1-complexity.md
```

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Content loss during decomposition | Low | High | Verify line counts, diff against original |
| Broken cross-references | Medium | Medium | Search for all internal links before/after |
| Missing law IDs | Low | Medium | Extract all ENG-X.X patterns, verify coverage |

---

## Estimated Effort

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| Phase 1: Decompose Laws | 14 | 2-3 hours |
| Phase 2: Transform Avatars | 10 | 2-3 hours |
| Phase 3: Repository Cleanup | 3 | 15 minutes |
| Phase 4: Constitution Linter | 8 | 2-3 hours |
| Phase 5: Linter Practice Guide | 5 | 1-2 hours |
| Phase 6: Update Documentation | 8 | 1-2 hours |
| Phase 7: Token Analysis Report | 6 | 1-2 hours |
| Phase 8: Validation | 5 | 1 hour |
| **Total** | **59** | **10-15 hours** |

---

## Notes

- Original ENGINEERING-LAWS.md should be archived to `laws/archive/` or deleted after verification
- Practice-guides/ may contain references that need updating
- Constitution-lint tool should be adapted from hangar-ai-constitution version
- The linter enables engineers to validate their project repos against AA engineering laws
- amendments/ and committee/ content is historical and can be removed (governance now in the laws themselves)
