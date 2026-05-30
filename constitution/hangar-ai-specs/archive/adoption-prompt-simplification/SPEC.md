# OpenSpec Proposal: Adoption Prompt Simplification

**ID:** adoption-prompt-simplification  
**Status:** Draft  
**Author:** Aali  
**Created:** 2026-02-04  

---

## Problem Statement

The current adoption prompt in the loyalty-service-legacy workshop requires manual steps:
1. Manually clone the hangar-ai-constitution repository
2. Manually open VS Code
3. Copy/paste a complex prompt with many placeholders
4. Navigate between repos to understand the adoption process

This friction reduces workshop effectiveness and doesn't demonstrate the agentic workflow we're teaching.

Additionally, the terminology `PROJECT-CONSTITUTION.md` in adopted projects can cause confusion with the actual hangar-ai-constitution. Students may think they're creating a full constitution when they're just creating project-specific rules.

---

## Proposed Solution

### 1. Rename PROJECT-CONSTITUTION.md to project-rules.md

Update all adoption guides to use `project-rules.md` instead of `PROJECT-CONSTITUTION.md`:
- Clearly distinguishes project-specific rules from the central Constitution
- Communicates that projects EXTEND the constitution with rules, not create their own
- Reduces cognitive load for new adopters

### 2. Create Simple Bootstrap Adoption Prompt

Create a simple, self-contained adoption prompt that:
- **Agentically clones** the hangar-ai-constitution to the parent directory of the target repo
- **Reads the adoption guide** from the freshly cloned constitution
- **Performs full adoption** following the brownfield-adoption guide
- Uses a single placeholder `{{TARGET_REPO_PATH}}` for flexibility

The prompt should be:
- **Simple:** One paragraph with one placeholder
- **Autonomous:** Agentic workflow that requires minimal user intervention
- **Complete:** Results in a properly adopted project

---

## Changes Required

### Phase 1: Update Adoption Guides (hangar-ai-constitution)

| File | Change |
|------|--------|
| `docs/guides/adoption/how-to-adopt-constitution.md` | Rename `PROJECT-CONSTITUTION.md` → `project-rules.md` |
| `docs/guides/adoption/brownfield-adoption.md` | Rename `PROJECT-CONSTITUTION.md` → `project-rules.md` |
| `docs/guides/adoption/greenfield-mvp.md` | Rename `PROJECT-CONSTITUTION.md` → `project-rules.md` |

### Phase 2: Create Bootstrap Adoption Prompt

Create a new file `docs/guides/prompts/adoption-bootstrap.md` containing:
- The simple bootstrap prompt (copy-paste ready)
- Instructions for use
- Expected outcomes

### Phase 3: Update Workshop Files (loyalty-service-legacy)

| File | Change |
|------|--------|
| `docs/adoption-prompt.md` | Replace with simplified bootstrap prompt |

---

## Acceptance Criteria

1. [ ] All adoption guides use `project-rules.md` instead of `PROJECT-CONSTITUTION.md`
2. [ ] Bootstrap prompt exists at `docs/guides/prompts/adoption-bootstrap.md`
3. [ ] Bootstrap prompt agentically clones the constitution repository
4. [ ] Bootstrap prompt reads and follows the brownfield-adoption guide
5. [ ] Bootstrap prompt creates proper adoption structure:
   - `AGENTS.md` at project root
   - `openspec/` directory structure
   - `openspec/project-rules.md` for project extensions
   - Characterization tests for existing code
6. [ ] Single placeholder `{{TARGET_REPO_PATH}}` for target repo path
7. [ ] Prompt fits in a single, readable paragraph
8. [ ] Token optimization case study document created at `docs/articles/token-optimization-case-study.md`
9. [ ] Case study demonstrates efficient constitution reading (target: read <30% of total constitution)

---

## Token Optimization Tracking

Throughout implementation, gather metrics to demonstrate token optimization in how the **constitution is read and consumed** by AI agents during adoption.

### Metrics to Capture

| Metric | Description |
|--------|-------------|
| **Constitution Total Size** | Total tokens if entire constitution were read |
| **Tokens Actually Read** | Tokens read during efficient adoption |
| **Read Efficiency %** | Percentage of constitution actually needed |
| **Index-First Navigation** | Whether agent uses index files to navigate |
| **Selective Reading** | Files skipped due to smart filtering |

### Token Optimization Techniques for Constitution Reading

Document which techniques were applied:
- [ ] **Index-First Navigation** - Read index.yaml files first to discover relevant sections
- [ ] **Avatar Selection** - Only read avatars matching the detected technology/domain
- [ ] **Law Relevance Filtering** - Read only laws applicable to the adoption scenario
- [ ] **Lazy Loading** - Read detailed content only when needed, not upfront
- [ ] **Reference Pointers** - Use file paths and section references instead of full content
- [ ] **Hierarchical Discovery** - Start broad (index), narrow to specific (individual laws)

### Constitution Reading Flow (Optimized)

```
1. Read laws/index.yaml → Discover law categories
2. Read avatars/index.yaml → Discover available avatars  
3. Analyze target codebase → Determine technology & domain
4. Read ONLY matching technology avatar (e.g., java-spring/)
5. Read ONLY matching product-type avatar (e.g., loyalty-aadvantage/)
6. Read ONLY applicable laws based on adoption scenario
7. Skip irrelevant avatars, skills, and workflows entirely
```

### Deliverable

Create `docs/articles/token-optimization-case-study.md` documenting:
1. Total constitution size vs tokens actually read
2. Navigation techniques that reduced token consumption
3. Which files were read vs skipped and why
4. Recommendations for constitution structure optimization
5. Lessons learned for future prompt design

---

## Out of Scope

- Changes to the core constitution laws
- Changes to avatar structure
- OpenSpec CLI modifications
- Changes to other workshop materials

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Existing projects use `PROJECT-CONSTITUTION.md` | Guide supports both names during transition |
| Git clone may fail (auth, network) | Prompt includes fallback instructions |
| Adoption guide may be incomplete | Prompt references specific sections |

---

## Implementation Plan

```
┌────────────────────────────────────────────────────────────────┐
│  Phase 0: Baseline Metrics (~5 min)                            │
│  - Count tokens in existing adoption-prompt.md                 │
│  - Document current placeholder count                          │
│  - List manual steps required                                  │
├────────────────────────────────────────────────────────────────┤
│  Phase 1: Update Adoption Guides (~15 min)                     │
│  - Search/replace PROJECT-CONSTITUTION.md → project-rules.md   │
│  - Update all 3 adoption guide files                           │
│  - Update any related templates                                │
├────────────────────────────────────────────────────────────────┤
│  Phase 2: Create Bootstrap Prompt (~10 min)                    │
│  - Create docs/guides/prompts/adoption-bootstrap.md            │
│  - Write simple, agentic prompt                                │
│  - Add usage instructions                                      │
│  - Measure new token count                                     │
├────────────────────────────────────────────────────────────────┤
│  Phase 3: Update Workshop (~5 min)                             │
│  - Update loyalty-service-legacy adoption prompt               │
│  - Test the full adoption flow                                 │
├────────────────────────────────────────────────────────────────┤
│  Phase 4: Document Token Optimization (~10 min)                │
│  - Create docs/articles/token-optimization-case-study.md       │
│  - Calculate all metrics                                       │
│  - Document techniques applied                                 │
│  - Analyze effectiveness                                       │
└────────────────────────────────────────────────────────────────┘
```

---

## Notes

The goal is to make adoption as simple as:

> "Clone this constitution, read the adoption guide, fully adopt it to this project."

The agent should handle all the complexity while the student observes and learns.
