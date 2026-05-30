# Tasks: Strengthen Adoption Structure Guardrails

> **Change:** strengthen-adoption-structure-guardrails  
> **Specs:** 3 capabilities (adoption-structure-validation, brownfield-adoption, adoption-compliance-checklist)  
> **Status:** In Progress

---

## 1. Add Required Adoption Structure Section to Brownfield Guide

- [x] 1.1 Add "⚠️ CRITICAL: Required Adoption Structure" section after Constitutional Authority section ✓
- [x] 1.2 Create ASCII diagram showing exact folder structure with annotations ✓
- [x] 1.3 Add machine-readable YAML structure definition with required paths ✓
- [x] 1.4 Add forbidden paths list (src/AGENTS.md, PROJECT-CONSTITUTION.md, etc.) ✓
- [x] 1.5 Add "For AI Agent" instruction block stating structure is NON-NEGOTIABLE ✓

## 2. Add Validation Checkpoint After Step 1.1

- [x] 2.1 Add "STRUCTURE VALIDATION CHECKPOINT" subsection after Step 1.1 (Initialize OpenSpec) ✓
- [x] 2.2 Add bash validation command block that checks all required paths ✓
- [x] 2.3 Add "⛔ STOP if ANY validation fails" instruction with fix guidance ✓
- [x] 2.4 Add fallback manual commands section for when openspec init fails ✓

## 3. Update Step 1.2 (AGENTS.md Creation)

- [x] 3.1 Add explicit statement: "AGENTS.md MUST be at project root (not nested)" ✓
- [x] 3.2 Add list of forbidden AGENTS.md locations (src/, app/, openspec/) ✓
- [x] 3.3 Add verification command after AGENTS.md creation ✓

## 4. Update AI Agent Quick Reference

- [x] 4.1 Expand Phase 1 checklist to include explicit file paths for each artifact ✓
- [x] 4.2 Add verification command for each checklist item ✓
- [x] 4.3 Add ⛔ markers for critical checkpoint steps ✓
- [x] 4.4 Add "Common Mistakes" warning box ✓

## 5. Add AI Agent Guardrail Instructions

- [x] 5.1 Add instruction for AI to refuse custom folder requests for AGENTS.md ✓
- [x] 5.2 Add instruction for AI to refuse skipping openspec initialization ✓
- [x] 5.3 Add redirect language: "Explain why structure is required and proceed with correct location" ✓

## 6. Update Adoption Compliance Checklist

- [x] 6.1 Update Governance Files section to include path verification (not just existence) ✓
- [x] 6.2 Add bash verification command for each checklist item ✓
- [x] 6.3 Add "Common Mistakes" section with frequent errors and fixes ✓
- [x] 6.4 Add verification command for AGENTS.md content (Constitution reference check) ✓

## 7. Testing and Validation

- [x] 7.1 Run adoption guide validation on loyalty-service-legacy project ✓
- [x] 7.2 Test adoption guide with Claude Opus 4.5 to verify structure created correctly ✓
- [ ] 7.3 Test adoption guide with GPT-4 to verify structure created correctly (deferred)
- [x] 7.4 Document validation results: All 6 checkpoints passed ✓

### Test Results (2026-02-12)

| Checkpoint | Validation | Result |
|------------|-----------|--------|
| Step 1.1 | OpenSpec init creates structure | ✓ PASS |
| Step 1.2 | AGENTS.md at root with Constitution | ✓ PASS |
| Step 1.3 | Baseline specs created | ✓ PASS |
| Structure | openspec/specs/ exists | ✓ PASS |
| Structure | openspec/changes/ exists | ✓ PASS |
| Content | Constitution referenced in AGENTS.md | ✓ PASS |

---

## Progress Summary

| Group | Tasks | Completed |
|-------|-------|-----------|
| 1. Structure Section | 5 | 5 |
| 2. Validation Checkpoint | 4 | 4 |
| 3. AGENTS.md Creation | 3 | 3 |
| 4. AI Agent Quick Reference | 4 | 4 |
| 5. Guardrail Instructions | 3 | 3 |
| 6. Compliance Checklist | 4 | 4 |
| 7. Testing | 4 | 3 |
| **Total** | **27** | **26** |
