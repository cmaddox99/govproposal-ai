# R7 — Plaintiff's Litigation Attorney: Version-Sensitivity Review of ESE Proposal

**Reviewer:** Plaintiff's litigation attorney — wrongful death / negligent coding / product
liability / copyright-IP. 33% contingency. Billing starts the moment this document enters
discovery.

**Occasion:** Post-implementation review of the 5-tier C++ version-sensitive routing system
(PR #47/#48) and its effect on the ESE proposal's litigation profile.

**Review Date:** 2026-07-14
**Prior R7 Verdicts:** Original: 🚨 CATASTROPHIC. Post-OSS: 🔴 SERIOUS, demand UP.
**This Review:** 🔴 SERIOUS — routing system is a partial shield and a new documentary sword.

---

## Updated Demand Assessment

**Net movement: DEMAND NEUTRAL TO SLIGHTLY DOWN — but the composition of risk has shifted
in ways that make certain theories stronger and harder to defend.**

The version routing system provides a genuine, defensible liability reduction on one specific
theory (the C++20 advice served to C++14 CWR developers). That is real credit, and I do not
oversell weak theories. However:

- The routing system *simultaneously* crystallizes the JNI gap as a documented, affirmative
  knowledge problem rather than a mere oversight
- The FAR 117 timezone gap becomes *worse* under routing, not better
- The `idiom_level` concept introduces a new, narrow but winnable theory
- The 100% test score creates a "certified safe" representation that can be weaponized
  post-ESE if routing failures occur
- The breadcrumb trail of documentation has now grown: restructuring-results.md → tasks-
  amendment1.md → cpp-version-sensitive-routing.md → this proposal → REVIEW-PANEL.md →
  this review. Each document AA produces to demonstrate diligence extends the documented
  knowledge window.

The wrongful death ($630M–$7.2B) and negligence per se theories remain fully viable.
The FAR 117 timezone angle has materially worsened. One new theory (idiom_level UB) is
narrow but technically winnable. The 100% score creates pre-trial impeachment value.

**Revised settlement demand posture:** Slightly below OSS-response level on IP theories,
unchanged on wrongful death and negligence per se, UP on FAR 117 timezone,
UP on documented-gap-without-closure theory.

---

## Section 1: Version Routing as Liability Shield — Does It Actually Reduce Wrongful Death Exposure?

### The Shield That Was Built

The routing system works as described. A CWR developer with `.copilot/project.yaml` declaring
`standard: 14, idiom_level: 03` is correctly routed to the `transitional` tier. The
`transitional` tier's `prefer` list routes to `ref-core-type-safety.md`,
`ref-safety-memory-lifetime.md`, and `ref-concurrency-threading.md`. The `greenfield` tier's
coroutines and C++20 content is not served. The `★ C++20` markers on `std::scoped_lock`
sections within `ref-concurrency-threading.md` are filtered. This genuinely reduces the
probability that a CWR developer receives C++20 advice that cannot compile in their toolchain.

**I will concede this point at trial.** The routing system is a real engineering improvement
and a real liability reduction for the specific failure mode it addresses: C++20 code patterns
served to C++14 developers. AA's engineers did real work and I will not pretend otherwise.

### The Gap That Was Not Filled: GAP-AA2 and "Routing to Nothing"

Here is where the shield becomes a sword.

The routing system correctly routes a CWR developer asking about JNI thread safety to the
`transitional` tier. The `transitional` tier's `prefer` list contains exactly three files:
`ref-core-type-safety.md`, `ref-safety-memory-lifetime.md`, and `ref-concurrency-threading.md`.
**None of these files contain JNI thread safety guidance.** GAP-AA2 — the JNI safety content
that should cover `AttachCurrentThread`/`DetachCurrentThread` lifecycle and `JNIEnv*`
thread-local contracts — is documented in the ESE proposal as `ref-brownfield-survival.md`,
which does not yet exist.

Before the routing system existed, a CWR developer asking about JNI threading might have
received C++20 lock-free guidance that was at least *topically adjacent* to threading — wrong
version, but in the ballpark of concurrency. Wrong-but-related guidance could trigger review.

After the routing system, that same CWR developer receives version-appropriate transitional
tier content that has zero JNI coverage. **The routing system has improved the quality of
what is served while simultaneously removing whatever accidental coverage existed in the
wrong-version content.** The developer now receives authoritative-looking, version-correct
guidance on thread safety that does not apply to their actual problem — and has no JNI
caveat warning them that the guidance is incomplete for JNI contexts.

**For litigation purposes:** "Routing to nothing" is worse than "routing to wrong content" in
a wrongful death theory. The wrongful-content theory requires me to establish causation through
a detour: developer received content → developer misapplied it → priority inversion → incident.
The routing-to-nothing theory has a shorter chain: developer needed JNI guidance → avatar
produced no JNI guidance → developer improvised using available concurrency patterns →
`static JNIEnv* g_env` or `std::atomic<JNIEnv*> g_env` → undefined behavior → incident.
R6 has already scripted exactly this scenario with both wrong patterns. The routing system
did not address it. The routing system confirmed it by routing to non-JNI content.

**The deposition question writes itself:** *"Your routing system, which you described in writing
as achieving 100% accuracy, correctly identified this developer's project as a C++14 codebase,
correctly routed them to the transitional tier, and the transitional tier had no JNI guidance
at all — is that correct?"*

**Practical exposure change:** Wrongful death theory — structurally unchanged. The causal chain
may actually be *cleaner* post-routing because the routing system's precision eliminates the
"developer should have known the C++20 content was wrong" counter-argument. Now the developer
received version-appropriate guidance, had no reason to question it, and was simply not warned.

### The `legacy-safe` Fallback: A Limited Shield

The conservative fallback (unknown version → `legacy-safe` → agent warns before serving
modern content) is a meaningful improvement. For repositories that have not set a
`.copilot/project.yaml`, the agent now asks before serving version-annotated content. This
reduces the probability of wrong-version guidance reaching unknown-version projects.

However, CWR has been explicitly documented as `standard: 14, idiom_level: 03`. CWR does not
benefit from the `legacy-safe` fallback because CWR's version is known and declared. The
fallback is a shield for undeclared projects. The most dangerous file in AA's C++ portfolio
(`CrewWatchSolverJNI.cpp`) lives in a project with a declared standard. The fallback does not
protect it.

---

## Section 2: The Documentation Paradox — Routing Edition

### What AA Has Now Written Down

Before the routing system, AA had a review panel documenting technical defects in an ESE
proposal. That was concerning from a discovery perspective. After the routing system, AA has
the following additional documents in the corpus:

| Document | What It Proves in Discovery |
|----------|----------------------------|
| `restructuring-results.md` | Proves AA formally surveyed its C++ portfolio in April 2026 and found ~95% of LOC was receiving systematically wrong guidance. Establishes the *date* of knowledge. |
| `tasks-amendment1.md` | 40 completed tasks with commit references. Proves AA took the problem seriously enough to devote substantial engineering effort to it. Proves the fix was deliberate and measured, not accidental. |
| `test_phase2_e4_rag_eval.py` | Proves the system was tested to a specific designed-and-executed test harness. The harness's own docstring documents its scope limitations, which I discuss in Section 5. |
| `cpp-version-sensitive-routing.md` | AA's canonical explanation of the failure mode, the fix, and the maintenance obligations. A 300-line guide to why the system was broken and how it was fixed. |

**The double-edged sword principle:** This documentation simultaneously demonstrates AA's
diligence (they found a problem and fixed it) and establishes the precise date of AA's
knowledge of the problem (the April 2026 survey). In a post-incident case, I will argue that
this documentation proves AA knew about the systematic misdirection problem before any
incident occurred and had documented exactly which codebases (CWR, IOC_ALP) were affected.

**The restructuring-results.md is the most important document in this corpus.** It contains the
table:

> IOC_ALP, hte_pm_hostconn, CWR, IOC_FosQuery2 | C++14 (toolset default) | ~60% | HIGH —
> modern advice silently unusable

This sentence, published in AA's own governance infrastructure, establishes that AA possessed
actual knowledge — with attribution to a specific survey — that CWR was receiving guidance
classified as HIGH risk before the routing fix was fully deployed. In Texas, actual knowledge
of a dangerous condition before harm is a prerequisite for gross negligence and the opening
of the punitive damages gate under Tex. Civ. Prac. § 41.003(a).

**Does the documentation help or hurt overall?** It helps on standard of care (shows AA took
reasonable steps) and hurts on willful-knowledge (shows AA knew, precisely, what was wrong
before fixing it completely). For the theories I actually bring — wrongful death and negligence
per se — the hurt is larger than the help. For standard-of-care defenses in ordinary negligence,
the documentation helps. But I am not bringing ordinary negligence. I am bringing gross negligence.

---

## Section 3: The ESE-A Gap — Documented but Unimplemented

### The Specific Problem

The state of play is now:

1. Version routing system **EXISTS** — CWR developers are correctly routed to `transitional` tier
2. ESE Brownfield Survival Pack (ESE-A: GAP-AA1–AA4) **APPROVED but UNIMPLEMENTED**
3. `ref-brownfield-survival.md` **DOES NOT EXIST**
4. A CWR developer receives `transitional` tier routing to content with zero JNI coverage
5. The avatar's REVIEW-PANEL.md formally declares `CrewWatchSolverJNI.cpp` "the most dangerous
   file in AA's C++ portfolio"

This is not a theoretical risk. AA has created a formal chain of documented knowledge that is
essentially a roadmap for a plaintiff's lawyer:

**Step 1 — Identify the dangerous file:**
> "R6 flagged `CrewWatchSolverJNI.cpp` as 'the most dangerous file in AA's C++ portfolio.'"
> — REVIEW-PANEL.md, confirmed by R5, R6, and R7 in three separate review rounds

**Step 2 — Establish that AA's AI governance knows it is dangerous:**
> "The avatar's concurrency examples could mislead Copilot into fatal JNI errors."
> — PROPOSAL.md, GAP-AA2 description

**Step 3 — Show what the AI actually serves when a developer touches that file:**
> `transitional` tier → `ref-core-type-safety.md`, `ref-safety-memory-lifetime.md`,
> `ref-concurrency-threading.md` — none of which contain `JNIEnv`, `AttachCurrentThread`,
> `DetachCurrentThread`, or `GlobalRef`

**Step 4 — Show AA knew the correct content was missing:**
> "ESE-A: Brownfield Survival Pack — execute BEFORE Phase 1" — PROPOSAL.md, sequencing note
> "GAP-AA2 (JNI thread safety): ref-brownfield-survival.md... does not yet exist"

**Step 5 — Show AA had a plan but did not execute it:**
> "Status: REVIEW-AMENDED" — PROPOSAL.md header. Approved, not implemented.

This five-step chain is entirely documentary. I do not need an expert witness to establish
it. I read five of AA's own governance documents in sequence. Each step is a quote.

### "We Identified the Gap and Have a Proposal" — A Defensible Position?

No. It is demonstrably worse than not having documented the gap at all.

If the gap were undocumented, AA's counsel could argue that the deficiency was an unknown
unknown — a governance limitation that the engineering team could not have been expected to
anticipate. That argument is destroyed the moment the gap is formally documented in a proposal
that was reviewed by seven reviewers, including an adversarial attorney reviewer who explicitly
named the JNI risk as a wrongful death vector.

**Under** *Owens v. Payless Cashways* **(Tex. App. 1992)** and its descendants in Texas product
liability doctrine: awareness of a defect combined with a business decision to proceed without
correcting it is evidence of conscious indifference to the rights, safety, or welfare of others.
That is the gross negligence standard under Tex. Civ. Prac. § 41.003(a)(2).

**The "proposal approved" status makes this worse, not better.** Approved means the organization
concluded this was necessary. Unimplemented means the organization made the business decision
not to do it yet — or to do other things first. In a post-incident deposition:

*"Your organization formally approved a proposal to add JNI thread safety guidance to the
C++ avatar. The proposal was approved in July 2026. When was it implemented?"*
[Answer involves a date after any incident]
*"And during the period between the approval and the implementation, CWR developers were using
the avatar to assist with `CrewWatchSolverJNI.cpp` without JNI thread safety guidance?"*
[Discovery confirms usage]
*"And you knew, at the time of the approval, that your own senior engineer had called that file
'the most dangerous file in AA's C++ portfolio'?"*

That exchange closes the gross negligence analysis.

**Required immediate action to reduce exposure:** Implement GAP-AA2 (JNI thread safety) before
any additional Copilot-assisted development touches `CrewWatchSolverJNI.cpp`. The routing
system is now a witness to the gap rather than a solution to it.

---

## Section 4: `idiom_level` — New Liability Angle

### What AA Has Documented

The `.copilot/project.yaml` template documents this configuration:

```yaml
standard: "14"       # Actual C++ standard compiled with
idiom_level: "03"    # Actual coding idioms in use
notes: "CWR migration — standard is C++14 but idiom level is C++03 due to legacy patterns"
```

The routing guide confirms: *"The avatar uses `idiom_level` — not `standard` — to select
example files when they diverge. This is the 'CWR scenario.'"*

AA has formally published that CWR developers code in C++03 idioms inside a C++14 compiler.
This is technically accurate and the routing system's author deserves credit for recognizing
the distinction. However, the formal documentation of this divergence creates a new exposure.

### The Subtle UB Problem

C++03 and C++14 are not binary-compatible in all idiom-level behaviors. Certain C++03 idiomatic
patterns exhibit undefined behavior under C++14 that they did not exhibit under C++03 (or vice
versa). Examples:

- **Value-initialization semantics**: C++11 changed value-initialization for POD types in
  certain contexts. A C++03 idiom relying on pre-C++11 POD zero-initialization behavior may
  compile silently under C++14 while producing UB that did not exist under C++03.
- **`>>` in templates**: C++11 removed the C++03 requirement to write `> >` instead of `>>`
  in template declarations. Code written with `>>` in C++03 style but compiled as C++14 changes
  parse semantics. Automated idiom examples could reinforce the C++03 pattern without noting
  the C++14 parsing difference.
- **Deleted functions vs. pre-C++11 private-undefined trick**: C++03 idiom for preventing
  copy is to declare copy constructor `private` without a definition. Under C++14, this still
  compiles but generates a different class layout and ODR exposure than `= delete`. An avatar
  serving C++03 idiom examples could reinforce the private-undefined pattern in C++14 code
  where `= delete` is the correct modern idiom — creating fragile code that compiles, passes
  CI, and fails at runtime under specific instantiation conditions.

### The Legal Argument

AA has done something legally interesting: they have formally documented a systematic category
mismatch (`idiom_level` ≠ `standard`) for their highest-risk codebase, and then configured
their AI guidance system to operate in that mismatch zone intentionally.

**The theory:** AA acknowledged that CWR developers use C++03 idioms in a C++14 codebase,
explicitly configured the AI avatar to serve C++03 idiom examples accordingly, and that
configuration produced guidance for patterns with documented subtle behavioral differences
under C++14 compilation. When a UB instance in CWR traces back to an `idiom_level: 03` example
served by the avatar, AA has documented both the decision to serve C++03 idioms and the
knowledge that CWR's `standard` was not C++03.

**Strength assessment:** This is a narrower and harder theory than wrongful death. I would not
lead with it. However, in a post-incident context where I have established the JNI wrongful
death theory, the idiom_level angle provides a second causal chain from the same event. Expert
witnesses — C++ standards committee members with DO-178C experience — can construct a cogent
argument that AA's configuration was a foreseeable source of UB for the specific idiom deltas
between C++03 and C++14.

**What AA should do:** Either (a) document the specific C++03 idioms that are safe under C++14
and gate the avatar examples to only those idioms, or (b) add a mandatory caveat in every
C++03-idiom example served to CWR: *"This pattern is safe under C++14 because [specific
reason]. The following C++03 idioms in this codebase require C++14 validation: [list]."*
Without that documentation, the `idiom_level` configuration is a liability without a corresponding
safety annotation.

---

## Section 5: The 100% Test Score — Attack Vectors

### What "100%" Actually Means

`test_phase2_e4_rag_eval.py` documents its own methodology in its docstring, and that
methodology has exploitable limitations that AA has published in writing:

**The harness uses keyword-frequency routing simulation, not semantic reasoning:**

```python
def _route_by_query(query: str, index: dict) -> list[str]:
    query_words = [w for w in query_lower.split() if len(w) > 3]
    hits = sum(1 for w in query_words if w in entry_lower)
    if hits >= 2:
        matches.append(ref_path)
```

This is a word-intersection count with a threshold of 2. A real Copilot query is a large
language model generating a natural-language completion. The harness simulates routing by
asking whether two query words appear in the search_queries YAML entry. These are not the
same thing. A real Copilot query for "how do I safely pass the JNI environment to a worker
thread spawned by the FICO Xpress callback" would not match the harness's criteria because
"JNI environment" and "FICO Xpress" and "worker thread" do not appear in any search_query
entries — because the ref files for GAP-AA2 and GAP-AA3 do not exist yet.

**The 100% score was measured against pre-ESE content.** The harness's 30 scenarios were
written to match the 34 existing reference files. Every scenario has an `expected_primary`
file that exists in the avatar today. When ESE adds ~45 new reference files and new
search_query entries to `AVATAR-RAG-INDEX.yaml`, each new entry is a new routing path that
could interfere with existing routes or create new tier mismatches. The 30 scenarios do not
test any of the ~45 new ESE documents.

This is not a criticism of the test harness — the harness is well-engineered for what it does.
The problem is AA's public characterization of the result.

### The Published "100% Accuracy" Claim

`restructuring-results.md` states:

> | Routing accuracy | 30/30 (100%) | ≥70% | ✅ PASS |
> | Tier version safety | 30/30 (100%) | 100% | ✅ PASS |
> | Answer coverage | 30/30 (100%) | ≥70% | ✅ PASS |
> | No ungated leakage | 30/30 (100%) | 100% | ✅ PASS |

This document does not say "30/30 on 30 pre-ESE scenarios using keyword matching simulation."
It says "100%" — full stop. And it is published in AA's governance infrastructure.

**Attack vector 1 — Scope misrepresentation:** If a routing failure occurs post-ESE on a
scenario type not covered by the 30 test cases (e.g., a JNI query that routes to wrong content
after ESE content is added), AA's published "100% routing accuracy" claim is impeachable as
a material overstatement of the system's verified scope. The test result was accurate for
its scope; the publication of "100%" without scope qualification creates the misrepresentation.

**Attack vector 2 — Keyword simulation vs. production behavior:** The harness simulates routing
using word-count matching. Production Copilot uses transformer-based semantic similarity over
much longer context windows. These can diverge. If production routing differs from harness
simulation in a safety-relevant way, and AA cited "100% accuracy" as evidence of the system's
reliability, that citation is inaccurate as applied to production behavior.

**Attack vector 3 — The ESE invalidation problem:** When ESE adds ~45 new reference files to
`AVATAR-RAG-INDEX.yaml`, the tier routing `prefer` lists will be modified. New entries in
`prefer` lists for `transitional` and other tiers will interact with existing routing. If any
new ESE file is mis-tiered (added to a tier whose `cpp_version_min` exceeds the tier's declared
standard), it will trigger a tier version safety violation of exactly the type the harness tests.
The 100% score becomes meaningless — not because the test was wrong, but because the system it
tested no longer exists. AA will need to re-run the harness after every ESE batch and re-publish
the score. Until that re-run occurs and is published, the 100% claim is stale.

**What this means for liability:** If an incident occurs between the first ESE commit (which
changes the routing table) and the next harness run (which re-validates it), AA will have been
operating with a routing system it claimed was "100% accurate" but had not validated in its
current configuration. That gap is discoverable. The git history of `AVATAR-RAG-INDEX.yaml`
will show the exact commit that changed the routing table, and the test run timestamps will
show when the next validation occurred. The window between them is the exposure window.

**Required immediate action:** AA must amend `restructuring-results.md` to add scope language:
*"100% accuracy on 30 pre-ESE scenarios using keyword-simulation routing. Score must be
re-validated after each AVATAR-RAG-INDEX.yaml modification that adds or modifies tier routing."*
It must also add a CI gate requiring E4 to pass before any AVATAR-RAG-INDEX.yaml change merges.
(Note: This CI gate is a defense measure. It also means the harness's 42 tests become a
blocking gate, and any ESE file that causes a harness regression will delay deployment. That
delay should be welcomed. It is the correct behavior.)

---

## Section 6: FAR 117 Timezone Routing Gap

### This Is the Strongest Section

The routing system has inadvertently created a safety regression for FAR 117 timezone compliance
that did not exist before the routing system was implemented. This is the section where my
demand goes up.

### The Specific Routing Gap

CWR is `standard: 14` → `transitional` tier.
GAP-20-11 (C++20 Calendar/timezone: `std::chrono::zoned_time`, `std::chrono::get_tzdb()`) is
C++20 content → `greenfield` tier.

The transitional tier's `prefer` list: `ref-core-type-safety.md`,
`ref-safety-memory-lifetime.md`, `ref-concurrency-threading.md`. None contain C++20
Calendar/timezone guidance.

C++20 Calendar/timezone APIs are *gated* behind the `greenfield` tier. A CWR developer asking
"how do I calculate crew rest period in a DST-boundary timezone" is routed to `transitional`
content with zero relevant timezone arithmetic guidance.

**There is no C++14-compatible equivalent to `std::chrono::zoned_time`.** The C++14 chrono
library has no IANA timezone database access, no `zoned_time`, no `get_tzdb()`. The legally
correct approach for FAR 117 timezone arithmetic in a C++14 codebase involves POSIX `mktime`
with explicit DST handling, `localtime_r` with timezone environment variable manipulation,
or a third-party library (Howard Hinnant's `date` library, or ICU). None of these are in the
avatar for any tier.

**Before the routing system:** A CWR developer asking about timezone arithmetic *might* have
received C++20 `zoned_time` guidance — wrong version, yes, but at least pointing in the right
direction toward timezone-aware arithmetic as the correct paradigm. The developer could then
research whether `Howard Hinnant's date` library (the C++20 chrono predecessor) was applicable.

**After the routing system:** A CWR developer asking about timezone arithmetic receives
transitional tier threading guidance. The routing system has correctly identified that C++20
content is version-inappropriate and has blocked it. But it has provided nothing in its place.
The developer is now more likely to fall back to naive `time_t` arithmetic, which does not
handle DST boundaries correctly, which is exactly the class of error that produces incorrect
FAR 117 rest period calculations.

**The routing system is actively making FAR 117 compliance harder for CWR developers.**

### The Legal Theory

Under 14 CFR § 117.5, airline operators must comply with fatigue risk management. Software
producing crew scheduling calculations that do not correctly handle DST boundaries can generate
rest assignments that appear compliant but are not. If a DST boundary error results in a
rest period calculation that is 60 minutes shorter than required under FAR 117 § 117.25, AA
has violated federal aviation safety law.

AA's review panel (R5 and R6 independently) flagged GAP-20-11 as requiring P1 classification
with an explicit FAR 117 safety rationale. The PROPOSAL.md was amended to reflect P1 status
for GAP-20-11. The routing system was then implemented, which gates C++20 timezone content
away from C++14 developers, with no C++14-compatible timezone guidance provided as an
alternative.

**The jury argument:** *"American Airlines' aviation safety regulations require pilots to
receive legally-mandated rest. Their crew scheduling software runs on C++14. Their AI
governance tool, which their own engineers used to write crew scheduling code, correctly
identified that C++14 developers should not receive C++20 content — and then provided nothing
for timezone arithmetic. Nothing. Their own review panel told them this was a safety-critical
gap at the highest priority level. The timezone guidance they blocked was the guidance their
developers needed to comply with federal pilot fatigue law."*

**This is the cleanest wrongful death causal chain in the portfolio.** It does not require
proving that a developer followed wrong advice. It requires proving that a developer lacked
correct advice, used default `time_t` arithmetic as a result, and a DST-boundary error produced
a non-compliant rest assignment. The routing system's correctness (properly blocking C++20
content from C++14 developers) is used as evidence against AA by showing the blockade had no
compensating C++14-compatible alternative.

**Required immediate action:** Add C++14-compatible timezone guidance to the avatar's
`transitional` tier before any Copilot-assisted development touches CWR timezone arithmetic.
The guidance must cover: (a) POSIX `localtime_r` DST handling, (b) Howard Hinnant's `date`
library as the C++14-compatible `zoned_time` equivalent, (c) explicit test cases for DST
boundary arithmetic, (d) a mandatory note that C++14 has no stdlib timezone database and
any solution requires an explicit external timezone source.

The cost of adding this guidance is one afternoon. The cost of not adding it is the exposure
described above.

---

## Required Immediate Actions

### 🔴 BEFORE ANY FURTHER COPILOT-ASSISTED DEVELOPMENT ON CWR

| # | Action | Theory it closes | Cost |
|---|--------|-----------------|------|
| 1 | Add C++14-compatible timezone guidance to `transitional` tier | FAR 117 timezone gap | One day |
| 2 | Implement GAP-AA2 (JNI thread safety for `CrewWatchSolverJNI.cpp`) | Wrongful death / routing-to-nothing | Two days |
| 3 | Add CI gate requiring E4 harness pass before AVATAR-RAG-INDEX.yaml merges | 100% score invalidation | Half day |
| 4 | Add scope qualification to `restructuring-results.md` "100%" claim | Published misrepresentation | One hour |
| 5 | Document C++03/C++14 idiom delta — annotate which C++03 idioms in CWR avatar examples are safe under C++14 and which require validation | idiom_level UB theory | Two days |

### 🔴 BEFORE ESE CONTENT IS ADDED TO THE ROUTING TABLE

| # | Action | Theory it closes | Cost |
|---|--------|-----------------|------|
| 6 | Re-run E4 harness and publish updated score after every batch of ESE files added to AVATAR-RAG-INDEX.yaml | 100% score staleness | Automated |
| 7 | Add ESE scenarios to E4 covering new ESE file tier routing — especially ESE-A (brownfield/transitional) | 100% score scope gap | One day |
| 8 | Verify all ESE files have `cpp_version_min` frontmatter compatible with their assigned tiers | Tier version safety regression | Automated (C4 test already exists) |

### 🟠 STRUCTURAL (BEFORE AI-ASSISTED CODE SHIPS TO SAFETY-CRITICAL SYSTEMS)

| # | Action | Theory it closes | Cost |
|---|--------|-----------------|------|
| 9 | FAA pre-consultation before AI-assisted code ships to CWR/IOC_ALP | All theories | High; highest ROI |
| 10 | Establish two-tier AI governance: safety-critical tier (FAR 117) vs. general development | Negligence per se, enterprise governance | Structural |
| 11 | Technical Copilot access controls on CWR/IOC_ALP (not policy only) | Negligence per se | Infrastructure |
| 12 | External JNI thread safety expert review for `CrewWatchSolverJNI.cpp` — formal report, external C++ JNI expert, in writing | Wrongful death, industry standard defense | $15K–$50K |

---

## Summary

The version routing system is a real engineering achievement. It reduces one specific category
of liability — C++20 advice served to C++14 developers — and I will not argue otherwise at
trial.

It simultaneously:
- Crystallizes the JNI gap into a documented, actionable theory by routing to nothing where
  the avatar's concurrency content previously provided accidental proximity to the problem
- Creates a FAR 117 safety regression by correctly blocking C++20 timezone guidance without
  providing a C++14 alternative
- Generates a discovery corpus (restructuring-results.md, tasks-amendment1.md, the routing
  guide) that proves pre-deployment knowledge of the systematic guidance failure
- Publishes a "100% accuracy" claim that is scope-limited in ways that make it impeachable
  after any post-ESE routing modification
- Formally documents the `idiom_level` duality for CWR — a narrow but technically grounded
  new theory

The routing system reduced liability in one direction and increased it in two others. The net
movement is approximately neutral on wrongful death, up on FAR 117 timezone, and structurally
unchanged on negligence per se.

**Actions 1 and 2 above are the only actions that meaningfully reduce my strongest theories.**
Everything else is marginal compared to those two. Implement GAP-AA2 and add C++14 timezone
guidance. Do it before the next Copilot-assisted commit touches `CrewWatchSolverJNI.cpp` or
CWR's scheduling arithmetic.

---

*R7 version-sensitivity filing statement: "The routing system's authors did careful work and
documented it thoroughly. The documentation is now my evidence of what AA knew and when they
knew it. The two gaps that remain — JNI and timezone — are not subtle implementation details.
They are the exact failure modes that your own review panel identified as safety-critical.
The routing system found the problem and routed around it perfectly. Now fill the gaps. If
there is an incident before you do, the routing system's precision becomes evidence of your
precision in knowing what was missing."*
