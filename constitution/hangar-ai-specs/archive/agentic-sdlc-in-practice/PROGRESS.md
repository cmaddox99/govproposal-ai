# PROGRESS: Agentic SDLC in Practice Workshop Slideware

## Status: � Implementation Complete

## Current Phase: Ready for Review

---

## Completed

- [x] **SPEC.md created** — Full workshop structure defined
  - 65 slides across 4 modules + opening
  - Workshop Facilitator persona defined
  - Slide-agent cue protocol documented
  - Exercise integration points identified

- [x] **Slideware created** — `docs/slides/agentic-sdlc-workshop-3hr/`
  - `README.md` — Facilitator guide with setup checklists
  - `slides.md` — Full 65-slide deck in Marp format with agent cues

- [x] **Workshop Facilitator workflow** — `agent-skills/workflows/workshop-facilitation.md`
  - Trigger phrases defined
  - Operating modes (Lecture, Demo, Exercise, Q&A)
  - Teaching principles documented
  - Module-specific guidance
  - Error handling protocols

---

## Files Created

| File | Purpose | Status |
|------|---------|--------|
| `docs/slides/agentic-sdlc-workshop-3hr/README.md` | Facilitator guide | ✅ Complete |
| `docs/slides/agentic-sdlc-workshop-3hr/slides.md` | 65-slide deck with agent cues | ✅ Complete |
| `agent-skills/workflows/workshop-facilitation.md` | Workshop Facilitator workflow | ✅ Complete |

---

## Module Checklist

| Module | Slides | Duration | Status |
|--------|--------|----------|--------|
| Opening: Welcome & Agenda | 1-4 | 10 min | ✅ Complete |
| 1: Constitution Deep-Dive | 5-18 | 35 min | ✅ Complete |
| 2: Brownfield Adoption Exercise | 19-30 | 45 min | ✅ Complete |
| 3: OpenSpec vs SpecKit & Tokens | 31-42 | 30 min | ✅ Complete |
| 4: Agentic SDLC Step-by-Step | 43-65 | 60 min | ✅ Complete |

---

## Next Steps (Validation Phase)

- [ ] Dry run full 3-hour workshop
- [ ] Validate agent co-facilitation at each module
- [ ] Test trigger phrases activate Workshop Facilitator persona
- [ ] Verify Exercise 1 integration with `hangar-ai-constitution-brownfield`
- [ ] Verify Exercise 2 integration with `hangar-ai-constitution-greenfield`
- [ ] Gather feedback, iterate

---

## Key Decisions

| Decision | Rationale | Date |
|----------|-----------|------|
| Use Marp/Slidev format | Markdown-native, version control friendly | 2026-02-09 |
| 4-module structure | Clear narrative arc, natural break points | 2026-02-09 |
| Agent cue protocol | Enables co-facilitation without custom tooling | 2026-02-09 |
| 64% token savings as key metric | Compelling, data-backed argument | 2026-02-09 |

---

## Open Questions

1. **Slide format**: Generate PPTX via Slide-Modeler or use Marp/Slidev?
2. **Prerequisites**: Devcontainer or pre-install checklist?
3. **Recording**: Should we provide video walkthroughs of exercises?

---

## Constitutional Compliance

| Law | Requirement | Status |
|-----|-------------|--------|
| ENG-1.2 | AI pairing patterns documented | ✅ Workshop Facilitator persona |
| ENG-4.1 | Atomic TDD taught | ✅ Module 1 + Exercise 2 |
| ENG-6.7 | Audit trail emphasized | ✅ Task tracking in every cycle |
| PRD-5.1 | OpenSpec explained | ✅ Module 2 comparison |
