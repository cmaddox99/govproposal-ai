# Journey Summary: AI Persona Review Panels for Governance Proposals

**Proposal:** `cpp-external-sources-enrichment` (ESE-*)  
**Date:** 2026-04-24  
**Repository:** AAInternal/hangar-ai-constitution

---

## What We Did

Starting from a C++ avatar enrichment proposal for the American Airlines Hangar AI Constitution, we ran a multi-phase AI-assisted governance review process that evolved organically into something more powerful than originally planned.

---

## Phase 1 — The Proposal

We identified gaps in the C++ avatar by comparing it against four external sources:
- **C++ Core Guidelines** (isocpp.github.io)
- **C++ Concurrency in Action, 2nd Ed.** (Williams/Manning)
- **C++ Templates: The Complete Guide, 2nd Ed.** (Vandevoorde)
- **C++20: The Complete Guide** (Josuttis)

The proposal (`PROPOSAL.md` + `tasks.md`) outlined 55 tasks across 8 phases, organized as an ESE-* enrichment program. Copyright analysis was embedded from the start — the books are commercially licensed, so we flagged derivation risks immediately.

---

## Phase 2 — The 6-Persona Review Panel

We launched **6 independent AI reviewer agents** in parallel, each given a distinct professional identity, their own domain lens, and the full proposal:

| Persona | Domain |
|---------|--------|
| R1 — Senior Copyright Counsel | IP / Copyright Law |
| R2 — Software Application Lawyer | Enterprise Licensing / AI IP |
| R3 — AI & Software Ethicist | Ethics / Attribution |
| R4 — Constitutional AI RAG Expert | Retrieval Architecture |
| R5 — C++ Master | Technical Accuracy |
| R6 — Senior AA Engineer | Brownfield Relevance |

**What happened:** Each reviewer found completely different problems. R1 caught a license misidentification (Core Guidelines is NOT MIT-licensed — it uses a bespoke Standard C++ Foundation license with an internal-use-only restriction). R4 found that two RAG files were already over token budget before any new content was added. R5 found a false technical claim (`std::atomic<shared_ptr<T>>` presented as "lock-free" when it isn't on any major implementation) and a hallucinated CVE. R6 found that the entire proposal was focused on greenfield C++20 features while AA's actual production systems (JNI, MFC, legacy crew solvers) weren't addressed at all.

**Lesson:** No single reviewer — human or AI — finds everything. Domain-specific personas find domain-specific problems. The parallelism revealed blind spots that a single comprehensive review would have missed.

---

## Phase 3 — Adding the Adversarial Reviewer (R7)

On user request, we added a 7th persona: **a plaintiff's litigation attorney who makes a living suing companies for negligent coding practices causing accidents and deaths** — someone explicitly motivated to find the worst possible interpretation of everything.

R7's findings were qualitatively different from R1–R6:
- Connected the false lock-free claim → potential priority inversion → crew scheduling → FAR 117 violation → wrongful death damages ($630M–$7.2B range)
- Used AA's own constitutional language ("NON-NEGOTIABLE," "MANDATORY," "PROHIBITED ACTIONS") as evidence of negligence per se
- Identified the `oss-reference-registry.yaml` governance document as a litigation liability map
- Opened the punitive damages gate (Texas Civ. Prac. § 41.003) via documented pre-deployment knowledge

**Lesson:** An adversarial persona finds risks that no cooperative reviewer will surface. The adversarial attorney persona is uniquely valuable because it stress-tests your documentation, your governance language, and your compliance gaps the way an actual opponent would — before anyone else does.

---

## Phase 4 — The OSS Source Analysis

To address copyright concerns raised by R1–R3, we examined **22 open-source repositories** (Apache 2.0, MIT, Boost licenses) to find permissively-licensed alternatives to the commercially-licensed book examples:

- `boostorg/lockfree` — lock-free queues, ABA prevention
- `abseil/abseil-cpp` — memory ordering patterns
- `ericniebler/range-v3` — the reference implementation that *became* `std::ranges`
- `fmtlib/fmt` — the reference implementation that *became* `std::format`
- `bshoshany/thread-pool` — C++20-native thread pool with `std::jthread`/`std::stop_token`
- `facebook/folly` — hazard pointers

**Key finding:** 13 of 14 flagged copyright patterns were fully alleviated. The derivation chain could run through permissively-licensed OSS rather than commercial books. Books become "Further Reading" recommendations, not hidden sources.

**Lesson:** When faced with copyright concerns about training/reference material, systematic OSS archaeology can often find independent, permissively-licensed implementations that predate or are independent of the commercial work. Document the derivation chain *before* implementation begins — not after.

---

## Phase 5 — The Full OSS Response Panel

We ran all 7 reviewers again, each formally responding to the OSS analysis. This is where the process became most instructive:

**R1 (Copyright):** Copyright risk dropped significantly. But flagged 4 NEW compliance concerns — OSS itself has license obligations (NOTICE files, attribution requirements).

**R2 (Software Lawyer):** Manning/Pearson EULA risk eliminated. But Copilot Copyright Shield scope still uncertain — does a "custom Constitution" configuration fall outside Microsoft's indemnification coverage?

**R3 (Ethicist):** "Original composition" claim must be retired permanently. Correct description: "AI-assisted, OSS-derived, domain-adapted." The OSS analysis transformed the AI laundering concern, not resolved it.

**R4 (RAG Expert):** The OSS approach *introduced 4 new blocking issues* that didn't exist before — the `oss-reference-registry.yaml` itself would contaminate algorithm queries; Further Reading blocks would embed book references into the RAG index; two reference files were already over token budget as live defects.

**R5 (C++ Master):** OSS analysis is orthogonal to technical correctness. All original C++ accuracy blockers unchanged. Also caught a factual error in our own OSS analysis ("Boost predates Williams by 4 years" — the official Boost 1.53.0 release was February 2013, contemporaneous with Williams 2012).

**R6 (AA Engineer):** Not one of the 22 OSS repos addresses AA's actual production gaps (JNI, MFC, FICO Xpress). Documented a concrete failure scenario: Copilot, following the enriched avatar, would suggest `static JNIEnv*` or `std::atomic<JNIEnv*>` for `CrewWatchSolverJNI.cpp` — both fatally wrong, both sounding authoritative.

**R7 (Plaintiff Attorney):** Settlement demand went **UP**. The OSS registry became "the single most useful discovery document AA could have created for my purposes." The diligence paradox: the more documentation of known risks you create without closing them, the longer the willful-knowledge period runs.

---

## Lessons Learned

### 1. Personas Find What They're Shaped to Find
Each reviewer's domain identity is a forcing function. A copyright lawyer sees license misidentification. A RAG architect sees token budgets. A litigator sees punitive damages gates. **Design your personas around the failure modes you're most afraid of.**

### 2. The Adversarial Persona is Non-Optional for Governance Work
R7 found more actionable risk in one pass than R1–R6 combined. If your governance framework will be tested by adversaries (regulators, plaintiffs, auditors), you need an adversarial reviewer *before* deployment, not after. The persona doesn't need to be "nice." Its job is to find what will hurt you.

### 3. Parallel Review is Genuinely Parallel Thinking
Running reviewers sequentially would cause anchoring — later reviewers read earlier findings and converge. Running them in parallel preserves independent viewpoints. R4 found RAG token problems without knowing R5 found C++ accuracy problems. The independence is the value.

### 4. A Solution Can Create New Problems
The OSS analysis solved the copyright problem and introduced 4 new RAG architecture problems. R4's "8 blocking issues (4 original + 4 new)" finding is the clearest illustration of second-order effects. **Always re-run the full panel after a major remediation — not just the affected reviewers.**

### 5. Documented Knowledge is a Double-Edged Sword
R7's "diligence paradox" is real and generalizable: creating formal documentation of known risks without closing them extends the period of documented, willful exposure. The `oss-reference-registry.yaml` is both a governance asset and a litigation liability. **Documentation and remediation must be coupled, not decoupled.**

### 6. Personas Can Catch Each Other's Errors
R5 caught a factual error in the OSS analysis itself ("4 years" precedence claim). This is peer review at the analysis layer, not just the proposal layer. **Run reviewers on your analysis documents, not just your proposal documents.**

### 7. The Proposal Improves at Every Round
The proposal started as a 55-task C++20 enrichment plan. After the panel rounds it became a legally-defensible, technically-accurate, RAG-architecture-sound, brownfield-first, aviation-safety-conscious governance document with a clean OSS derivation chain. Each reviewer pass compounded the quality. **The value isn't in any single reviewer — it's in the iteration.**

### 8. Personas Need Domain-Specific Vocabulary to Be Effective
R7 citing "Texas Civ. Prac. § 41.003" and "scènes à faire doctrine" and R4 citing "token budget ceiling" and "`<!-- no-embed -->` annotation" — these aren't generic observations. The richer the domain knowledge you give the persona, the more specific and actionable the findings. **Invest in the persona prompt. Vague personas produce vague findings.**

---

## The Meta-Lesson

The most important thing this journey demonstrated is that **AI personas are a form of structured adversarial thinking made cheap**. Before AI, convening 7 independent expert reviewers — including one adversarial litigator — for a governance proposal would cost tens of thousands of dollars and weeks of calendar time. With AI personas, it takes hours.

The quality ceiling is real — an AI persona cannot replace an actual JNI threading expert reviewing actual production code. But for governance documents, architecture proposals, and risk surface analysis, the technique produces findings that are genuinely surprising, genuinely independent, and genuinely useful. The reviewers found things the authors didn't know to look for.

That's the point.

---

## Artifact Index

| File | Description |
|------|-------------|
| `PROPOSAL.md` | Core enrichment proposal — 55 tasks, 8 phases |
| `tasks.md` | Task list with ESE-* IDs and phase assignments |
| `REVIEW-PANEL.md` | Full 7-reviewer panel — original reviews + all OSS responses (1,729 lines) |
| `OSS-SOURCE-ANALYSIS.md` | 22-repository analysis; 13/14 patterns alleviated |
| `R4-OSS-RESPONSE.md` | RAG Expert full OSS response (400 lines) |
| `R5-OSS-RESPONSE.md` | C++ Master full OSS response (298 lines) |
| `R6-OSS-RESPONSE.md` | AA Engineer full OSS response (240 lines) |
| `JOURNEY-SUMMARY.md` | This document |
