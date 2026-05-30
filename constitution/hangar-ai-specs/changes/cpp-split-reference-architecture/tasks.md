# Tasks: cpp-split-reference-architecture

**Proposal:** [PROPOSAL.md](PROPOSAL.md)
**PR:** #14

---

## Progress Summary

- Total tasks: 19
- Completed: 0
- Remaining: 19

---

## Phase 1: Section-to-File Mapping

- [ ] 1.1: Create definitive section-to-file mapping table (assign every `full-reference.md` section to exactly one `ref-*.md` file)
- [ ] 1.2: Measure actual token count of each planned file; split any file exceeding 3,500t

## Phase 2: Extract Reference Files

- [ ] 2.1: Extract `ref-core-patterns.md` — Domain Modeling, DI, Safety, Naming, Const, Casts, Nulls, Designated Initializers, SRP, Object Design, Implicit Conversions, Type-Safe Unions
- [ ] 2.2: Extract `ref-testing-quality.md` — Testing Framework, Test Isolation, CI Quality Toolchain, Toolchain Gap
- [ ] 2.3: Extract `ref-security-safety.md` — Safety-Critical C++ (MISRA/DO-178C/JSF AV)
- [ ] 2.4: Extract `ref-concurrency.md` — Concurrency, Coroutines, Resiliency Patterns, Exception Safety, Termination
- [ ] 2.5: Extract `ref-build-toolchain.md` — Package Management, Reproducible Builds, C++20 Modules, ABI Stability, Allocator Governance, Templates, Lambda Governance, Forwarding/ADL, Structured Logging, Configuration Management, Health Checks, Preprocessor/Macro, License Compliance
- [ ] 2.6: Extract `ref-memory-lifetime.md` — Advanced Memory and Object Lifetime, C/C++ Interop and FFI
- [ ] 2.7: Extract `ref-brownfield-migration.md` — Brownfield Migration, Per-Tier configs, Cross-Standard ABI, Feature-Detection, Compiler Flags, Sanitizers
- [ ] 2.8: Extract `ref-brownfield-playbooks.md` — Migration Playbooks (C++98→11→14→17→20), Dual-Toolchain, Dep Mismatch, Writing New Code for Legacy
- [ ] 2.9: Extract `ref-legacy-navigation.md` — Legacy Navigation, Mental Models, Code Smells, Triage, Survival Patterns, Priority Matrix
- [ ] 2.10: Extract `ref-operational.md` — Tools & Commands, Anti-Patterns, Skill Parity, Project Archetypes, Authorities

## Phase 3: Create Index and Update Guidance

- [ ] 3.1: Create `reference-index.md` with categorized topic router and preamble content
- [ ] 3.2: Update `guidance.md` — replace quick-links table with single `reference-index.md` link
- [ ] 3.3: Verify `guidance.md` ≤ 450t and `reference-index.md` ≤ 500t

## Phase 4: Test Updates and Verification

- [ ] 4.1: Update all tests referencing `full-reference.md` to target split `ref-*.md` files
- [ ] 4.2: Add token budget tests for each `ref-*.md` (≤ 3,500t each)
- [ ] 4.3: Run full test suite — all tests green
- [ ] 4.4: Verify zero content loss (every original section accounted for)

## Phase 5: Cleanup

- [ ] 5.1: Remove `full-reference.md` after all content verified in split files
