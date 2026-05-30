# Spec: Adoption Compliance Checklist

> **Capability:** adoption-compliance-checklist  
> **Type:** Modified  
> **Change:** strengthen-adoption-structure-guardrails

---

## MODIFIED Requirements

### Requirement: Path verification for governance files

The adoption compliance checklist SHALL verify that governance files exist at the correct paths, not just that they exist somewhere in the project.

#### Scenario: AGENTS.md path verification
- **WHEN** verifying AGENTS.md compliance
- **THEN** checklist SHALL verify file exists at `./AGENTS.md` (project root)
- **AND** SHALL fail if AGENTS.md exists only in subdirectories

#### Scenario: openspec directory path verification
- **WHEN** verifying openspec compliance
- **THEN** checklist SHALL verify `./openspec/` exists at project root
- **AND** SHALL verify `./openspec/specs/` exists
- **AND** SHALL verify `./openspec/changes/` exists

---

## ADDED Requirements

### Requirement: Verification commands for each item

The adoption compliance checklist SHALL provide bash commands that can verify each checklist item programmatically.

#### Scenario: AGENTS.md verification command
- **WHEN** user needs to verify AGENTS.md
- **THEN** checklist SHALL provide command: `[ -f "./AGENTS.md" ] && echo "✓ AGENTS.md at root" || echo "✗ AGENTS.md missing or misplaced"`

#### Scenario: openspec structure verification command
- **WHEN** user needs to verify openspec structure
- **THEN** checklist SHALL provide command that checks all required directories exist

#### Scenario: Constitution reference verification command
- **WHEN** user needs to verify AGENTS.md content
- **THEN** checklist SHALL provide command: `grep -q "hangar-ai-constitution" AGENTS.md && echo "✓ Constitution referenced" || echo "✗ Constitution not referenced"`

---

### Requirement: Common mistakes section

The adoption compliance checklist SHALL include a "Common Mistakes" section that lists frequent adoption errors and how to fix them.

#### Scenario: Lists AGENTS.md placement mistakes
- **WHEN** user reviews common mistakes
- **THEN** checklist SHALL list:
  - "AGENTS.md in src/ instead of root" with fix "Move to project root"
  - "AGENTS.md in openspec/ instead of root" with fix "Move to project root"

#### Scenario: Lists openspec structure mistakes
- **WHEN** user reviews common mistakes
- **THEN** checklist SHALL list:
  - "Missing openspec/specs/ directory" with fix "Run mkdir -p openspec/specs"
  - "Missing openspec/changes/ directory" with fix "Run mkdir -p openspec/changes"
  - "Using PROJECT-CONSTITUTION.md instead of project.md" with fix "Rename to openspec/project.md"

#### Scenario: Lists content mistakes
- **WHEN** user reviews common mistakes
- **THEN** checklist SHALL list:
  - "AGENTS.md missing Constitution reference" with fix "Add hangar-ai-constitution path to Authority section"
  - "AGENTS.md missing Authority Hierarchy" with fix "Add authority hierarchy section per template"
