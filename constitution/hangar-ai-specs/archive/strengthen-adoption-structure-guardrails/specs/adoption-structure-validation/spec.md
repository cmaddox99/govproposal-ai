# Spec: Adoption Structure Validation

> **Capability:** adoption-structure-validation  
> **Type:** New  
> **Change:** strengthen-adoption-structure-guardrails

---

## ADDED Requirements

### Requirement: Machine-readable structure definition

The brownfield adoption guide SHALL include a machine-readable YAML definition of the required adoption structure that specifies all required files, directories, and forbidden paths.

#### Scenario: YAML definition includes all required paths
- **WHEN** an AI agent reads the adoption structure definition
- **THEN** the definition SHALL include:
  - `AGENTS.md` at project root with location constraint "root"
  - `openspec/` directory at project root
  - `openspec/project.md` file
  - `openspec/specs/` directory
  - `openspec/changes/` directory

#### Scenario: YAML definition includes forbidden paths
- **WHEN** an AI agent reads the adoption structure definition
- **THEN** the definition SHALL include forbidden paths:
  - `src/AGENTS.md` with reason "AGENTS.md must be at project root"
  - `**/PROJECT-CONSTITUTION.md` with reason "Deprecated - use openspec/project.md"

#### Scenario: YAML definition includes content validation
- **WHEN** an AI agent reads the AGENTS.md requirements
- **THEN** the definition SHALL specify must-contain rules:
  - "hangar-ai-constitution"
  - "Authority Hierarchy"

---

### Requirement: Validation checkpoint commands

The brownfield adoption guide SHALL provide bash commands that AI agents can execute to verify the adoption structure was created correctly.

#### Scenario: Validation command checks AGENTS.md location
- **WHEN** AI agent runs the validation command
- **THEN** it SHALL check that `AGENTS.md` exists at project root
- **AND** output "✓ AGENTS.md at root" if present
- **AND** output "✗ MISSING: AGENTS.md" if absent

#### Scenario: Validation command checks openspec structure
- **WHEN** AI agent runs the validation command
- **THEN** it SHALL check that `openspec/` directory exists
- **AND** check that `openspec/specs/` directory exists
- **AND** check that `openspec/changes/` directory exists
- **AND** output status for each check

#### Scenario: Validation command is copy-paste ready
- **WHEN** AI agent encounters the validation command
- **THEN** the command SHALL be a single bash block that can be executed without modification
- **AND** SHALL work on macOS, Linux, and WSL

---

### Requirement: ASCII structure diagram

The brownfield adoption guide SHALL include a clear ASCII diagram showing the exact folder structure required after adoption.

#### Scenario: Diagram shows all required artifacts
- **WHEN** an AI agent reads the structure diagram
- **THEN** the diagram SHALL show:
  - `AGENTS.md` at root with annotation "← REQUIRED: At root, not nested"
  - `openspec/` at root with annotation "← REQUIRED: OpenSpec root"
  - `openspec/project.md` with annotation "← REQUIRED: Project context"
  - `openspec/specs/` with annotation "← REQUIRED: Baseline specs"
  - `openspec/changes/` with annotation "← REQUIRED: Change proposals"
  - `tests/unit/` and `tests/integration/` directories

#### Scenario: Diagram uses clear visual hierarchy
- **WHEN** an AI agent reads the structure diagram
- **THEN** the diagram SHALL use tree-style formatting with `├──`, `└──`, and `│` characters
- **AND** SHALL clearly distinguish between existing and new directories
