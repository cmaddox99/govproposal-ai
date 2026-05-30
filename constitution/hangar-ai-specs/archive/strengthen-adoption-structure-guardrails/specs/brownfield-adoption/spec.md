# Spec: Brownfield Adoption Guide

> **Capability:** brownfield-adoption  
> **Type:** Modified  
> **Change:** strengthen-adoption-structure-guardrails

---

## MODIFIED Requirements

### Requirement: Structure requirements placement

The brownfield adoption guide SHALL place all folder structure requirements in a single consolidated section near the top of the guide, immediately after the Constitutional Authority section.

#### Scenario: Structure section appears before Phase 1
- **WHEN** an AI agent reads the brownfield adoption guide
- **THEN** the "Required Adoption Structure" section SHALL appear before "Phase 1: Establish Safety Net"
- **AND** SHALL appear after "Constitutional Authority"

#### Scenario: Structure section is marked as critical
- **WHEN** an AI agent reads the structure section
- **THEN** the section SHALL be prefixed with "⚠️ CRITICAL:"
- **AND** SHALL state "This structure is NON-NEGOTIABLE"

---

### Requirement: Validation checkpoint after Step 1.1

The brownfield adoption guide SHALL include a mandatory STRUCTURE VALIDATION checkpoint immediately after Step 1.1 (Initialize OpenSpec).

#### Scenario: Checkpoint requires explicit verification
- **WHEN** AI agent completes Step 1.1
- **THEN** the guide SHALL instruct AI to run validation commands
- **AND** SHALL instruct AI to "STOP and verify" before proceeding

#### Scenario: Checkpoint includes stop-on-failure instruction
- **WHEN** validation fails (any artifact missing)
- **THEN** the guide SHALL instruct AI to "STOP and fix before proceeding"
- **AND** SHALL NOT allow AI to continue to Step 1.2 until structure is correct

---

### Requirement: Explicit path constraints for AGENTS.md

The brownfield adoption guide SHALL explicitly state that AGENTS.md MUST be created at the project root directory, not nested in any subdirectory.

#### Scenario: Guide states root-only requirement
- **WHEN** AI agent reads AGENTS.md creation instructions
- **THEN** the guide SHALL state "AGENTS.md MUST be at project root (not nested)"
- **AND** SHALL provide the exact path: `touch AGENTS.md` (not `touch src/AGENTS.md`)

#### Scenario: Guide lists forbidden AGENTS.md locations
- **WHEN** AI agent reads the forbidden paths section
- **THEN** the guide SHALL list incorrect locations:
  - `src/AGENTS.md`
  - `app/AGENTS.md`
  - `openspec/AGENTS.md`

---

### Requirement: Fallback manual commands

The brownfield adoption guide SHALL provide fallback manual commands in case `openspec init` fails or is unavailable.

#### Scenario: Manual structure creation commands provided
- **WHEN** `openspec init` fails or is not installed
- **THEN** the guide SHALL provide manual mkdir/touch commands:
  - `mkdir -p openspec/specs openspec/changes`
  - `touch openspec/project.md`
  - `touch AGENTS.md`

#### Scenario: Fallback instructions are clearly marked
- **WHEN** AI agent encounters fallback section
- **THEN** the section SHALL be labeled "Fallback: Manual Structure Creation"
- **AND** SHALL state "Use these commands if openspec init fails"

---

### Requirement: Model-agnostic guardrail language

The brownfield adoption guide SHALL use explicit, unambiguous language that works consistently across different AI models (GPT-4, Claude, Gemini).

#### Scenario: Guardrails use imperative language
- **WHEN** AI agent reads critical instructions
- **THEN** instructions SHALL use "MUST", "SHALL", "REQUIRED"
- **AND** SHALL NOT use "should", "could", "may" for required steps

#### Scenario: Guardrails use stop markers
- **WHEN** AI agent reaches a checkpoint
- **THEN** the checkpoint SHALL use "⛔ STOP" or "⚠️ CRITICAL" markers
- **AND** SHALL be visually distinct from regular text

---

## ADDED Requirements

### Requirement: AI Agent guardrail for custom folder requests

The brownfield adoption guide SHALL instruct AI agents to refuse user requests to create adoption artifacts in custom folders.

#### Scenario: AI refuses custom folder requests
- **WHEN** user asks to create AGENTS.md in a custom location (e.g., "put AGENTS.md in src/")
- **THEN** AI agent SHALL refuse and explain "AGENTS.md must be at project root per constitutional requirements"
- **AND** SHALL proceed with correct location regardless of request

#### Scenario: AI redirects to correct structure
- **WHEN** user asks to skip openspec initialization
- **THEN** AI agent SHALL explain why openspec structure is required
- **AND** SHALL create the structure using fallback commands if needed
