# AA Constitution Lint

Constitutional compliance linter for hangar-ai-constitution projects.

## Installation

```bash
pip install aa-constitution-lint
```

Or install from source:

```bash
cd tools/constitution-lint
pip install -e .
```

## Usage

```bash
# Lint current directory
aa-constitution-lint .

# Lint with JSON output (for CI/CD)
aa-constitution-lint --format json

# Install pre-commit hook
aa-constitution-lint hooks install
```

## What Gets Checked (v0.2.0)

> **Note:** The 4 adoption-focused rules (`AgentsFileRule`, `TestPyramidRule`, `HangarAiSpecsDirRule`, `AtomicTddRule`) were removed in v0.2.0. They have been moved to adoption workflows.

### Constitution Self-Governance Rules

| Rule ID | Law | Description |
|---------|-----|-------------|
| `constitution.product_avatar_completeness` | ENG-10.1 | Every product avatar dir must have `manifest.yaml`, `guidance.md`, and `examples/` |
| `constitution.tech_avatar_completeness` | ENG-10.1 | Every technology avatar dir must have `manifest.yaml`, `guidance.md`, and `examples/` |
| `constitution.product_avatar_nonneg_examples` | ENG-10.1 | Product avatar `examples/` must reference non-negotiable PRD laws (PRD-1.2, PRD-1.5, PRD-2.5, PRD-5.1, PRD-6.2) |
| `constitution.tech_avatar_nonneg_examples` | ENG-10.1 | Technology avatar `examples/` must reference non-negotiable ENG laws (ENG-4.1, ENG-6.1, ENG-6.4, ENG-6.7) |
| `constitution.no_deprecated_adoption` | ENG-10.1 | `ADOPTION.md` is deprecated; use `guidance.md` instead |
| `constitution.avatar_manifest_schema` | ENG-10.1 | `manifest.yaml` must have `avatar.id`, `avatar.type`, `avatar.name`, `activates`, `specializes_laws` |
| `constitution.avatar_manifest_nonneg_citation` | ENG-10.1 | `specializes_laws` in `manifest.yaml` must cite at least one non-negotiable law |
| `constitution.law_frontmatter_completeness` | ENG-10.1 | Law `.md` files must have valid YAML frontmatter with `domain`, `article`, `title`, and ≥1 `laws` entry |
| `constitution.skill_index_consistency` | ENG-10.1 | Skill `index.yaml` file refs must exist on disk and all `.md` files must be indexed |

### Index Integrity Rules

| Rule ID | Law | Description |
|---------|-----|-------------|
| `index.laws_registry_files_exist` | ENG-10.1 | All files listed in `laws/index.yaml` must exist on disk |
| `index.laws_registry_complete` | ENG-10.1 | All `.md` files in `laws/{domain}/` must be listed in `laws/index.yaml` |
| `index.avatar_rag_complete` | ENG-10.1 | Every avatar directory must have an entry in `AVATAR-RAG-INDEX.yaml` |
| `index.avatar_rag_files_exist` | ENG-10.1 | All file paths referenced in `AVATAR-RAG-INDEX.yaml` must exist on disk |
| `index.avatar_rag_laws_valid` | ENG-10.1 | All law IDs in `AVATAR-RAG-INDEX.yaml` must be registered |
| `index.avatar_index_complete` | ENG-10.1 | All avatar dirs must be listed in `avatars/index.yaml` and `avatars/product-type/index.yaml` |
| `index.nonneg_laws_consistent` | ENG-10.1 | Non-negotiable IDs in `laws/index.yaml` must match `non_negotiable: true` in law file frontmatter |

### Law Reference Rule

| Rule ID | Law | Description |
|---------|-----|-------------|
| `references.law_reference` | ENG-10.1 | All `ENG-*`, `PRD-*`, `BUS-*` law ID references in files must be registered |

## Integration with GitHub Copilot Workflow

This tool integrates with the Atomic TDD cycle (ENG-4.1) at the VERIFY step:

```
1. RED      → Write ONE failing test
2. GREEN    → Write MINIMUM code to pass
3. REFACTOR → Improve code quality
4. VERIFY   → Tests + coverage + aa-constitution-lint  ← HERE
5. COMMIT   → Save progress
6. REPEAT   → Start next test
```

## Aviation Compliance

For aviation-specific projects, the linter validates compliance with:
- **BUS-2.1** - FAA Regulatory Compliance
- **BUS-2.2** - TSA Security Requirements
- **BUS-2.3** - DOT Consumer Protection

## Output Format

JSON output complies with ENG-10.1 (Constitution Metrics Collection Law) schema:

```json
{
  "evaluations": [
    {
      "law_id": "ENG-4.2",
      "result": "pass",
      "evaluation_point": "aa-constitution-lint",
      "timestamp": "2026-02-01T10:30:00Z",
      "context": {"rule": "test-pyramid-structure"}
    }
  ],
  "summary": {
    "total": 5,
    "passed": 4,
    "failed": 1,
    "skipped": 0
  }
}
```

## Configuration

Create `.constitution-lint.yaml` in your project root to customize:

```yaml
version: 1
rules:
  structure.agents_file:
    enabled: true
  structure.test_pyramid:
    enabled: true
  structure.hangar_ai_specs_dir:
    enabled: true
settings:
  fail_on_warning: false
```

## Pre-commit Hook

After running `aa-constitution-lint hooks install`, add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: aa-constitution-lint
        name: AA Constitution Lint
        entry: aa-constitution-lint
        language: system
        pass_filenames: false
        always_run: true
```

## License

MIT - American Airlines Engineering
