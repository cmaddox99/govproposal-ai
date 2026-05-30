# Proposal: Strengthen Adoption Structure Guardrails

## Why

During workshop sessions, instructors observed that some AI models fail to create the correct adoption structure — missing `AGENTS.md` at root, incorrect `openspec/` folder nesting, or incomplete directory structure. This inconsistency occurs because the brownfield adoption guide lacks explicit validation checkpoints and consolidated structure requirements, causing RAG chunking and model variance to produce different results across GPT-4, Claude, and Gemini.

## What Changes

- **Add consolidated structure requirements** — Single "Required Adoption Structure" section at top of brownfield-adoption.md with ASCII diagram and machine-readable YAML definition
- **Add validation checkpoints** — Mandatory STRUCTURE VALIDATION step after Step 1.1 with bash verification commands
- **Add explicit path requirements** — Clear statement that `AGENTS.md` MUST be at project root (not nested)
- **Add forbidden paths guidance** — Explicit list of incorrect locations (e.g., `src/AGENTS.md` is wrong)
- **Add "STOP if failed" instructions** — Force AI agents to halt and fix before proceeding with incomplete structure
- **Update AI Agent Quick Reference** — Expand checklist with explicit file paths and ⛔ markers
- **Update Adoption Compliance Checklist** — Add path verification (not just existence checks)
- **BREAKING**: None — these are additive guardrails

## Capabilities

### New Capabilities

- `adoption-structure-validation`: Machine-readable YAML definition of required adoption structure with validation commands

### Modified Capabilities

- `brownfield-adoption`: Add structure requirements section, validation checkpoints, and guardrail instructions
- `adoption-compliance-checklist`: Add path verification and common mistakes section

## Impact

- **Docs affected**: `docs/guides/adoption/brownfield-adoption.md`, `docs/guides/adoption/adoption-compliance-checklist.md`
- **Tools affected**: Potential future enhancement to `constitution-lint` for structure validation
- **Workshops affected**: All adoption workshops will benefit from consistent structure creation
- **AI models affected**: Changes designed to work consistently across GPT-4, Claude, and Gemini
