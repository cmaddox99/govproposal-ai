# Tasks — Iterative Adoption for Large Codebases

**Proposal:** iterative-adoption-large-codebases
**Total Tasks:** 8
**Completed:** 8/8

## Progress Summary

- [x] IA-01 — Create `skill-iterative-adoption.md` in development-practices ✓ bb0f6ee
- [x] IA-02 — Create `docs/guides/adoption/iterative-adoption-large-codebases.md` ✓ bb0f6ee
- [x] IA-03 — Register skill in `development-practices/index.yaml` (count 11 → 12) ✓ bb0f6ee
- [x] IA-04 — Add large-codebase routing callout to `workflows/adoption.md` ✓ bb0f6ee
- [x] IA-05 — Create change proposal artifacts (`PROPOSAL.md`, `tasks.md`, `PROGRESS.md`) ✓ 57073c8
- [x] IA-06 — Amendment 1: Add Trust Ramp (AI on-ramp) to skill and guide ✓
- [x] IA-07 — Amendment 1: Add Minimum Viable Session (low bandwidth) to skill and guide ✓
- [x] IA-09 — Amendment 2: Rename to Pragmatic Adoption — files, ids, labels, and callouts ✓
- [x] IA-10 — Amendment 3: Orientation triggers and Key Files reference section ✓
- [x] IA-11 — Amendment 4: Remove mandatory linter run from governance setup step ✓
- [x] IA-12 — Amendment 5: Feathers characterization phase (Phase 3c) with 4-step process, hard stop, human checkpoint ✓
- [x] IA-13 — Amendment 6: Optional SonarQube checkpoint (Phase 3d) with persistent reminder pattern ✓
- [x] IA-14 — Amendment 7: Proposal-first governance — PROPOSAL.md + tasks.md created before any code work; check-offs through each phase; archive prompt at close ✓
- [x] IA-15 — Amendment 8: GRASP/SOLID/DDD design principles; design-rationale.md artifact; pattern-named decisions mandatory ✓
- [x] IA-16 — Amendment 9: Seam definition + size spectrum; interactive two-step discovery; explore-before-confirm instruction; Phase 3b multi-file table ✓
- [x] IA-17 — Amendment 10: Technology-agnostic coverage tools; explicit STOP report checklist with mandatory fields ✓
- [x] IA-18 — Amendment 11: Missing tool pre-check; A/B/C dialog; defer path with INCOMPLETE flag and risk acknowledgement ✓
- [x] IA-19 — Amendment 12: Seam-scoped coverage gates; explicit prohibition on project-wide blocking; SonarQube per-seam-file metrics ✓
- [x] IA-20 — Amendment 13: "What's Next" post-adoption section; pattern continuity; 5-step table; starter feature prompt template ✓
- [x] IA-21 — Amendment 14: Idempotent governance setup; pre-flight check; never overwrite existing AGENTS.md or hangar-ai-specs/ ✓
- [x] IA-22 — Amendment 15 (P0): SonarQube 5-option informed dialog; mutation progressive ladder; ENG-4.10 scaffolding exemption ✓
- [x] IA-23 — Amendment 16 (P1): ENG-4.1 frontmatter; Key Definitions callout; dead code escape hatch; cross-BC seam dialog; ENG-4.10 char test retirement ✓
- [x] IA-24 — Amendment 17 (P2): Step numbering; Sensing/Separation note; Sprout/Wrap callout; Pitest targetClasses; "non-trivial" defined ✓

## Task Detail

### IA-01 — Skill: skill-iterative-adoption.md ✓
**File:** `agent-skills/skills-by-domain/development-practices/skill-iterative-adoption.md`

Created skill with:
- 17 trigger phrases covering all four adoption blockers
- AI-executable 6-step procedure (scope → governance setup → bounded-context iteration → sonar delta → ENG-3.1 design-first → report and stop)
- Copy-paste `project-rules.md` templates for product avatar deferral, chunking protocol, SonarQube delta policy, ENG-3.1 interpretation
- `followed_by` links to `skill-sonarqube-compliance-gate`, `06-atomic-tdd`, `09-refactoring`

### IA-02 — Guide: iterative-adoption-large-codebases.md ✓
**File:** `docs/guides/adoption/iterative-adoption-large-codebases.md`

Created full reference guide covering:
- Part 1: One-time governance setup (product avatar deferral, SonarQube baseline)
- Part 2: Bounded-context iteration sequence (archaeology → decision → implement → delta)
- Part 3: SonarQube delta model (HARD_BLOCK / PHASE_GATE / WARNING classification)
- Part 4: ENG-3.1 design-first interpretation (Strategy/Command/Guard Clause vs. line-splitting)
- Part 5: project-rules.md templates (ready to copy)

### IA-03 — Index registration ✓
**File:** `agent-skills/skills-by-domain/development-practices/index.yaml`

Added skill entry with all 17 trigger phrases. Updated count: 11 → 12.

### IA-04 — Adoption workflow callout ✓
**File:** `workflows/adoption.md`

Added callout after the workflow title block directing large-codebase teams to
`skill-iterative-adoption` and the guide.

### IA-05 — Change proposal artifacts ✓
**Files:** `hangar-ai-specs/changes/iterative-adoption-large-codebases/`

Created `PROPOSAL.md`, `tasks.md`, `PROGRESS.md` per ENG-11.1 SDD Law.
