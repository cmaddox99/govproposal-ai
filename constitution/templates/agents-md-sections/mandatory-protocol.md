<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->
## ⛔ MANDATORY AGENT PROTOCOL

**Every coding task in this repository MUST follow this exact 8-step cycle. No exceptions.**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              MANDATORY AGENT PROTOCOL (Per ENG-4.1 — NON-NEGOTIABLE)        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Step 1 — IDENTIFY   Find the FIRST unchecked task in                      │
│                       hangar-ai-specs/changes/<change-id>/tasks.md          │
│                       Read the linked spec scenario ID                      │
│                       ↓                                                     │
│  Step 2 — RED        Write EXACTLY ONE failing test                         │
│                       Run tests → Required output: FAILED                   │
│                       ⛔ SHOW the failure output before continuing           │
│                       ↓                                                     │
│  Step 3 — GREEN      Write MINIMUM code to make that ONE test pass          │
│                       Run tests → Required output: PASSED                   │
│                       ⛔ SHOW the pass output before continuing              │
│                       ↓                                                     │
│  Step 4 — REFACTOR   Improve code quality (no behavior changes)             │
│                       Run tests → Required output: still PASSED             │
│                       ↓                                                     │
│  Step 5 — VERIFY     Run full test suite + constitution-lint                │
│                       ALL gates must be green before proceeding             │
│                       ⛔ AT PHASE GATES: run Phase Gate Sub-Protocol below  │
│                       ↓                                                     │
│  Step 6 — UPDATE     Open hangar-ai-specs/changes/<change-id>/tasks.md     │
│           TASKS.MD   and mark task [x] with ✓ + commit hash                │
│                       Update progress summary counts                         │
│                       ↓                                                     │
│  Step 7 — COMMIT     git add -A && git commit -m "<conventional-msg>"      │
│                       Commit message MUST reference spec scenario ID        │
│                       ↓                                                     │
│  Step 8 — STOP AND   Report the completed test, commit hash, and next task  │
│           REPORT     Wait for human confirmation before starting next cycle │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```
<!-- END hangar-ai-constitution:mandatory-protocol -->
