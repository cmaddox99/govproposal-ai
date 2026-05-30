# Tasks — Constitutional Companion Updates & Fixes

**Spec ID:** `constitutional-companion-updates`
**Status:** PROPOSE — implementation in progress

## Task List

## Progress: 74 / 78 complete (CCU-43A–N done; CCU-42F, 42G-GRASP, 42H, 42I BLOCKED — await Type 2/3 review)

- [x] CCU-01 (AMEND-1A) — Reorder tasks.md template: 3a→3b→3c→3e→3d(parallel)→3f; add phase order note
- [x] CCU-02 (AMEND-1B) — Relabel Step 2 SonarQube row as pre-flight check; distinguish from Phase 3d; fix pre-flight check list label
- [x] CCU-03 (AMEND-1C) — Replace hard STOP with checkpoint dialog offering "continue now" vs "next session"
- [x] CCU-04 (AMEND-1D) — Redraw Phase 3a–3f overview with checkpoint arrows and explicit SQL dependency chain note

- [x] CCU-05 (AMEND-2A) — Add stack-detection table to Step 0a; instruct AI to record and carry result forward; prohibit re-scan at Step 2.1
- [x] CCU-06 (AMEND-2B) — Add detected-stack confirmation line to gateway dialog header
- [x] CCU-07 (AMEND-2C) — Add "Session 1 preview" callout inside Path A description

- [x] CCU-08 (AMEND-3A) — Refine stack detection table: add "Refine to avatar" column; Java → check for spring-boot → java-spring; Node → check for react/express
- [x] CCU-09 (AMEND-3B) — Move adjacent/openspec checks to silent-only pre-flight; remove from user-facing status table

- [x] CCU-10 (AMEND-4A) — Add Step 2 hard-limits callout: prohibit source file reads, product avatar selection, extra artifacts; add self-check sentence
- [x] CCU-11 (AMEND-4B) — Hard limits callout covers artifact invention (adoption-check.md) — no separate change needed

- [x] CCU-12 (AMEND-5A) — Replace "Run workflows/adoption.md" with inline AGENTS.md and project-rules.md templates; both use literal `none — deferred` for product avatar
- [x] CCU-13 (AMEND-5B) — Add `## Progress: 0 / 6 complete` to tasks.md template
- [x] CCU-14 (AMEND-5C) — project-rules.md template uses `[TO BE FILLED IN DURING PHASE 3A]` for Architecture; Local Extensions comment deferred until after Phase 3a

- [x] CCU-15 (AMEND-6A) — Expand Priority 3/4 descriptions with concrete examples; eliminate ambiguity for empty/bare hangar-ai-specs/
- [x] CCU-16 (AMEND-6B) — Add explicit status table template to Step 0a with Stack detected as mandatory last row; prohibit placing it outside the table

- [x] CCU-17 (AMEND-7A) — Replace {detected_framework} with {build_tool} — version deferred to Phase 3a; add prohibition on reading pom.xml/build.gradle for version
- [x] CCU-18 (AMEND-7B) — Add note to AGENTS.md template: calculate constitution path from directory names only, no source file reads
- [x] CCU-19 (AMEND-7C) — Add placeholder callout to PROPOSAL.md template explaining brackets are intentional

- [x] CCU-20 (AMEND-8) — Add explicit commit block after every "Check off" instruction (3a, 3c, 3d) with template message and hard ordering rule: tasks.md updated BEFORE commit, not after
- [x] CCU-21 (AMEND-9) — Add "Checkpoint Dialog Standard" and explicit "type `continue`" instructions at all 7 phase-gate stop points (novice UX)
- [x] CCU-22 (AMEND-10) — Split Phase 3b into two explicit gates: verdict choice (Gate 1) then Target Architecture confirmation (Gate 2, REFACTOR only); add ⛔ prohibition on designing architecture before verdict chosen
- [x] CCU-23 (AMEND-11) — Fix "check off" ambiguity: add in-place editing rule to tasks.md template; change all 6 "check off" instructions to explicit "edit existing line in-place" wording
- [x] CCU-24 (AMEND-12) — Add missing commit block before Step 2 STOP checkpoint (governance scaffold was left uncommitted)
- [x] CCU-25 (AMEND-13) — Mandate sequential numbering of seam candidates; add fixed sub-field template; tighten closing prompt to "Type `use seam N` (e.g., `use seam 1`)"
- [x] CCU-26 (AMEND-14) — Fix hash-stamp chicken-and-egg: explicit two-step commit process at all 5 phase gates; explicit PROPOSAL.md title fill-in instruction with example

- [x] CCU-27 (AMEND-15) — Fix two Phase 3a unfilled placeholders: PROPOSAL.md title (split into two explicit numbered steps + ⛔ note); project-rules.md Architecture section (add explicit fill-in step with mini-template + ⛔ before commit block)

- [x] CCU-28 (AMEND-16A) — Phase 3a: fill in PROPOSAL.md Scope body (Bounded context + Seams lines) and Problem Statement [context name] — add to "Before starting" alongside title fill-in
- [x] CCU-29 (AMEND-16B) — Phase 3b: fill in PROPOSAL.md Scope Approach line after verdict confirmed — add explicit edit step after phase-2-decision.md is written
- [x] CCU-30 (AMEND-16C) — Product avatar deferral never resolved: at end of Phase 3a add optional ask_user prompt to confirm or keep deferred; update AGENTS.md + project-rules.md if user names one

- [x] CCU-31 (AMEND-17A) — Phase 3c: environment workarounds (JAVA_HOME, build flags) discovered during test/coverage runs never documented — add rule: record any workaround in project-rules.md ## Environment Notes before continuing
- [x] CCU-32 (AMEND-17B) — Phase 3d SonarQube Option A: one-token flow causes 3 extra ask_user interactions because analysis tokens rarely have metrics read access — ask for both analysis token AND read/browse token upfront
- [x] CCU-33 (AMEND-17C) — Phase 3c characterization test comment style: // --- dividers trigger SonarQube "commented-out code" rule as false positives — add guidance to use plain // or @Nested/@DisplayName for grouping

- [x] CCU-34 (AMEND-18) — Continuous refactoring loop: adoption ends at Phase 3c; refactoring-backlog.md seeded at Phase 3b; Phase 4 replaces 3e/3f with per-proposal TDD cycle (R1–R5), characterization gate, three-path checkpoint, seam-clean detection, and infinite loop until user stops

- [x] CCU-35 (AMEND-19) — Mutation hardening integration: Phase 3c async baseline offer; MUTATION entry type in backlog; Phase 4 R4b async delta; seam-clean gate requires >=70% or MUTATION entry; natural-break proactive offer at `stop`; MUTATION tasks.md template (M1-M5)

- [x] CCU-37 (AMEND-21) — Panel review moderate findings: Pitest timing claim, dead code exemption scope, Spring Boot entry point guidance, Phase 4 Step 2 invalid ID handling, Step 1 BLOCKED seam visibility, design-rationale.md path rule, Minimum Viable Session gateway reference, ENG-4.12 Legacy Rescue threshold ✓ 710ea20

- [x] CCU-38A (AMEND-22) — Step 0a: silent constitution freshness check via git fetch before adoption status check ✓ cb90d4a
- [x] CCU-38B (AMEND-22) — Phase 3c tool table: add iOS/Swift row (xccov + Muter); replace vague fallback with 4-step escalation ✓ cb90d4a
- [x] CCU-38C (AMEND-22) — Phase 4 R4: add ⛔ SHOW test output gate; update tasks template and Step 6 invariants ✓ cb90d4a
- [x] CCU-38D (AMEND-22) — Step 0b: add re-prompt instruction for ambiguous/non-standard path selection phrasing ✓ cb90d4a
- [x] CCU-38E (AMEND-22) — Phase 3c: add structurally-blocked coverage exception (DI coupling) distinct from dead code ✓ cb90d4a
- [x] CCU-38F (AMEND-22) — Phase 4 restart: add session-resume backlog/git consistency cross-check ✓ cb90d4a
- [x] CCU-38G (AMEND-22) — Phase 4 R4b: make mutation delta offer mandatory (must present before R5, user may skip) ✓ cb90d4a
- [x] CCU-38H (AMEND-22) — Step 7: add mutation baseline guard before seam-clean detection ✓ cb90d4a



- [x] CCU-39A (AMEND-23) — Add "When the AI Loses Track" preamble (14-row correction table) after purpose block in skill ✓ 6fdf174
- [x] CCU-39B (AMEND-23) — Create `docs/guides/adoption/ai-correction-prompts.md` with 14 failure patterns, full prompts, quick reference card ✓ 6fdf174

- [x] CCU-40A (AMEND-24) — Add mandatory full-read guard at top of main skill body ✓ a78ac5e
- [x] CCU-40B (AMEND-24) — Extract Step 2 (Governance Setup + templates) to 02-adoption-setup.md ✓ a78ac5e
- [x] CCU-40C (AMEND-24) — Extract Phase 3b (Decision) to 02-adoption-setup.md ✓ a78ac5e
- [x] CCU-40D (AMEND-24) — Extract Phase 3d (SonarQube Setup) to 02-adoption-setup.md ✓ a78ac5e
- [x] CCU-40E (AMEND-24) — Create 02-adoption-setup.md with header + all three extracted sections ✓ a78ac5e
- [x] CCU-40F (AMEND-24) — Update PROPOSAL.md status, tasks.md progress count, bump version to 2.24.0 ✓ a78ac5e

- [x] CCU-41A (AMEND-25) — Remove EXTEND verdict from Gate 1 in supplement; replace EXTEND Feathers callout with CHARACTERIZE-ONLY callout; update template strings ✓ c380303
- [x] CCU-41B (AMEND-25) — Add CHARACTERIZE-ONLY as 4th verdict: skip Gate 2, record as "REFACTOR — DEFERRED" in phase-2-decision.md, seed backlog with deferred entries; Phase 4 Gate 2 trigger on deferred pick ✓ c380303
- [x] CCU-41C (AMEND-25) — Add Companion Mode row for characterize-without-refactoring; update Phase 3a–3c diagram; add deferred-entry note to Phase 4 backlog display ✓ c380303

- [x] CCU-42A (AMEND-26) ✅ READY — F-1.1: Replace 13-row correction-prompts table with 3 critical rows + callout to ai-correction-prompts.md (~10 lines saved) ✓ 4af8520
- [x] CCU-42B (AMEND-26) ✅ READY — F-1.2: Replace embedded 8-step TDD cycle in AGENTS.md template with 4-line ENG-4.1 citation (~8 lines saved) ✓ 4af8520
- [x] CCU-42C (AMEND-26) ✅ READY — F-1.6: Replace violation-tier table with 2-line reference to brownfield-adoption.md §Violation Tiers (~6 lines saved) ✓ 4af8520
- [x] CCU-42D (AMEND-26) ✅ READY — F-1.8: Replace "Key Files" prose section with 6-row quick-reference table + guide links (~33 lines saved) ✓ 4af8520
- [x] CCU-42E (AMEND-26) ✅ READY — F-1.9: Condense "What's Next" to 4 lines + starter prompt; link to pragmatic-adoption.md (~37 lines saved) ✓ 4af8520
- [ ] CCU-42F (AMEND-26) ⛔ BLOCKED — F-1.3: Replace seam-theory definitions with callout to characterization-testing.md. BLOCKED: must add seam-size table + mock-necessity tree + Sensing/Separation guidance to docs/guides/testing/characterization-testing.md first
- [ ] CCU-42G (AMEND-26) ⛔ PARTIAL — F-1.4: Replace SOLID table (READY ~10L) + DDD table (READY ~17L) with law citations now; GRASP table replacement BLOCKED until GRASP added to laws/engineering/architecture.md §2.1 (F-3.8 gap-fill)
- [ ] CCU-42H (AMEND-26) ⛔ BLOCKED — F-1.5: Reduce Phase 3d SonarQube dialog to 6-line routing stub. BLOCKED: must add adoption-context setup dialog + dual-credential note + BLOCKED_THIS_ITERATION pattern to skill-sonarqube-compliance-gate.md first
- [ ] CCU-42I (AMEND-26) ⛔ BLOCKED — F-1.7: Replace inline refactoring PROPOSAL.md template with spec-governance reference. BLOCKED: must add "Refactoring Proposal Variant" section to spec-governance.md with adoption-specific fields annotated by law first

- [x] CCU-43A (AMEND-27) — companion ~473: add [ENG-1.2](../../../laws/engineering/foundations.md#section-12-ai-engineer-pairing-law) to checkpoint dialog gate rule ✓ e903a68
- [x] CCU-43B (AMEND-27) — companion ~519: add [ENG-1.2](../../../laws/engineering/foundations.md#section-12-ai-engineer-pairing-law) to "MUST NOT start refactoring until human explicitly chooses" ✓ e903a68
- [x] CCU-43C (AMEND-27) — companion ~787: add [ENG-4.8](../../../laws/engineering/testing.md#section-48-mock-boundaries-law) to seam-wide sociable testing invariant header ✓ e903a68
- [x] CCU-43D (AMEND-27) — companion ~830: add [ENG-4.6](../../../laws/engineering/testing.md#section-46-coverage-requirements) to "coverage gates apply to seam files only" callout ✓ e903a68
- [x] CCU-43E (AMEND-27) — companion ~959: add [ENG-4.1](../../../laws/engineering/testing.md#section-41-atomic-test-driven-development-law) to "Do NOT change any logic in Phase 3c" ✓ e903a68
- [x] CCU-43F (AMEND-27) — companion ~1191: add [ENG-4.1](../../../laws/engineering/testing.md#section-41-atomic-test-driven-development-law) to characterization-test RED invariant ✓ e903a68
- [x] CCU-43G (AMEND-27) — companion ~1206: add [ENG-4.1](../../../laws/engineering/testing.md#section-41-atomic-test-driven-development-law) to "SHOW test output before proceeding" ✓ e903a68
- [x] CCU-43H (AMEND-27) — companion ~1232: add [ENG-4.11](../../../laws/engineering/testing.md#section-411-mutation-testing-law) to "R4b offer is mandatory" rule ✓ e903a68
- [x] CCU-43I (AMEND-27) — companion ~1367: add [ENG-4.11](../../../laws/engineering/testing.md#section-411-mutation-testing-law) to mutation baseline guard callout header ✓ e903a68
- [x] CCU-43J (AMEND-27) — companion ~1501: add [ENG-3.1](../../../laws/engineering/quality.md#section-31-complexity-limits) to mechanical line-count splitting prohibition ✓ e903a68
- [x] CCU-43K (AMEND-27) — companion ~1693: add [ENG-2.3](../../../laws/engineering/architecture.md#section-23-vertical-slice-architecture-law) + [ENG-2.4](../../../laws/engineering/architecture.md#section-24-bounded-context-law) to "MUST NOT scan outside bounded context" ✓ e903a68
- [x] CCU-43L (AMEND-27) — companion ~1706: add [ENG-12.1](../../../laws/engineering/agentic-feedback.md#eng-121-agentic-feedback-loop-law) to "each iteration MUST NOT add new violations" ✓ e903a68
- [x] CCU-43M (AMEND-27) — companion ~997–999: add [ENG-6.7](../../../laws/engineering/security.md#eng-67--audit-trail-law) to refactoring-backlog-driven-work statement ✓ e903a68
- [x] CCU-43N (AMEND-27) — setup (multiple commit instructions): add [ENG-6.7](../../../laws/engineering/security.md#eng-67--audit-trail-law) to commit message format instructions in Phase 3b + 3c ✓ e903a68
