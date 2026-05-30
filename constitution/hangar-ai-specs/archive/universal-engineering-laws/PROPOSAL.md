# Universal Engineering Laws & Skill Discovery

## Problem

Several engineering laws express universal design principles using technology-specific tactical language (OOP setters, Java getter syntax, specific tool names). This conflates the *what* (the principle) with the *how* (the implementation in a specific stack). Meanwhile, the avatar system — designed for stack-specific guidance — has coverage gaps, and the skill system lacks a discovery protocol for intent-based prompts.

## Changes Made

### Phase 1: Law Rewrites (11 laws)

| Law | Before | After |
|-----|--------|-------|
| ENG-3.2 Immutability | "No setters on value objects" | "State representations SHALL be constructed once and never modified" |
| ENG-3.3 Law of Demeter | Java getter chain example | Universal pseudocode with arrow notation |
| ENG-3.5 Naming | Hard-coded casing table | Universal intent principles + Avatar Guidance |
| ENG-3.7 Error Handling | "typed exceptions/errors" | "specific descriptive types" |
| ENG-3.8 Refactoring | OOP pattern names (Extract Method, etc.) | Universal actions (Decompose, Simplify, etc.) |
| ENG-2.1 Value Objects | "no setters, final/readonly fields" | Cross-reference to ENG-3.2 |
| ENG-1.5 API-First | "OpenAPI, GraphQL SDL" | "standard specification format" |
| ENG-5.1 IaC | "Approved Tools: Terraform, Pulumi..." | "Tool selection per technology avatar" |
| ENG-6.2 Authentication | "JWT, OAuth2" | "industry-standard protocols" |
| ENG-6.4 Data Protection | "AES-256", "TLS 1.2+" | "industry-standard ciphers/protocols" |

### Phase 2: Skill Discovery Protocol

- Added Section 6.3 to `agent-skills/base/AGENT.md`
- 4-step protocol: Extract Intent → Search Skills Registry → Resolve to Skill → No Match Found
- Intent matching priority: Exact phrase > Semantic similarity > Law-concept > Category
- Enriched all 29 skills in `index.yaml` with 8 trigger phrases each (imperative, question, need, help forms)

### Phase 3: Avatar Examples (~23 new files)

- ENG-3.2 Immutability: java-spring, dotnet-core, nodejs-typescript, react-typescript, angular, mobile-react-native
- ENG-3.3 Law of Demeter: python-fastapi, java-spring, nodejs-typescript, dotnet-core
- ENG-3.5 Naming: python-fastapi, java-spring, nodejs-typescript, dotnet-core
- Coverage gaps: java-spring/ENG-2.2, angular/ENG-2.2, dotnet-core/ENG-2.2, mobile-react-native/ENG-2.2, mobile-react-native/ENG-3.1, nodejs-typescript/ENG-2.1, nodejs-typescript/ENG-2.2, data-engineering/ENG-3.1, data-engineering/ENG-6.5

### Phase 4: Cross-cutting Updates

- Updated AGENTS.md with Skill Discovery Protocol reference
- Updated 7 avatar manifests with new specializes_laws entries
- Updated AGENT.md Socratic guidance examples to use universal language
- Applied same changes to aa-engineering-laws companion repository

## Success Criteria

1. No engineering law contains language-specific syntax
2. No engineering law names specific tools (tool categories like SAST are fine)
3. Every rewritten law has avatar examples in the 4 core backend avatars
4. Skill discovery protocol documented in AGENT.md
5. All 29 skills have trigger phrases covering imperative, question, need, and help forms
