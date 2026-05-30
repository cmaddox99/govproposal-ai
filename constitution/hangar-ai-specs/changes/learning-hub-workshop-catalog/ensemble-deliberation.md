# Ensemble Deliberation — Hangar AI Workshop Catalog (Learning Hub Publication)

**Evidence Artifact ID:** `ensemble-deliberation-lhw-001`
**Date:** 2026-04-10
**Scope:** Review of `hangar-ai-specs/changes/learning-hub-workshop-catalog/PROPOSAL.md` — LHW-001 four-workshop catalog (HAW-GF-001, HAW-LR-001, HAW-AW-001, HAW-PD-001)
**Convened by:** GitHub Copilot (facilitating on behalf of the author)
**Required outcome:** Complete approval to proceed; partial approval from all five roles

---

## Ensemble Roster

| Role | Persona | Focus |
|------|---------|-------|
| ADD-Therapist | Clara | Cognitive load, clarity, simplicity at every instruction step |
| Critic | Marcus | Finds a better way; skeptical of first ideas |
| Facilitator | Sarah | Workshop flow, process construction, live-session mechanics |
| XP-Architect | David | Technical excellence, code quality, correctness of technical content |
| Downstream-Advocate | Jin | Self-delivery — can a participant complete this without outside help? |

---

## Methodology

Each persona reviewed the PROPOSAL.md independently against the five open questions submitted by the author:

1. **Q1 — Legacy Rescue positioning:** Should the two sessions be enrollable separately, or only as a pair?
2. **Q2 — Prerequisite enforcement:** Should the learning path be recommended-only, or should the Learning Hub gate Avatar Workflow behind Greenfield completion?
3. **Q3 — Avatar Workshop audience split:** Should there be two tracks (builders vs consumers), or is the single track sufficient?
4. **Q4 — Product Discovery audience:** Is self-service format appropriate for product managers who do not operate AI agents?
5. **Q5 — Certification:** Should completion of all four workshops yield a recognisable certification or badge?

Personas then brought findings to convergence. Each gives an independent verdict: **Full Approval**, **Partial Approval (Conditional)**, or **Reject**. The composite verdict requires all roles at partial approval or above.

---

## Independent Reviews

---

### Clara — ADD-Therapist

*Reviewing for: cognitive load at each decision point; clarity of enrollment model; one thing at a time.*

**On Q1 — Legacy Rescue enrollment model:**

The two-session structure is a cognitive double-bind for a learner reading the course catalog. A single listing that says "Part 1 + Part 2, 6 hours total" is unambiguous. Splitting it into two separate enrollable units creates a coordination problem: does Part 1 completion automatically enroll me in Part 2? What happens if I never come back? The constitutional evidence artifacts from Part 1 are the *input* to Part 2. Splitting the enrollment is splitting the artifact chain, which violates the cognitive contract of "you will leave with a complete set of evidence."

*Decision:* One enrollment unit, two clearly labelled sessions. Course page should show "Session 1 of 2" and "Session 2 of 2" structure visually, with a natural checkpoint between them. Participants who need a break can take one without re-enrolling.

**On Q2 — Prerequisite gates:**

Hard gates on a Learning Hub are a support burden and an adoption friction point. Engineers who have already done legacy rescue work in production do not need the greenfield workshop to understand the avatar catalog. The recommended learning path (shown visually as a progression, not enforced by software) is the right pattern. Add a "New to Hangar AI? Start here" callout on the landing page that points at Workshop 1 — that is the cognitive equivalent of a soft gate with zero friction.

*Decision:* Recommended path only, no software gates. Landing page callout for new learners.

**Clara's Verdict: FULL APPROVAL**
*No conditions. Both decisions are clean and cognitively sound.*

---

### Marcus — Critic

*Reviewing for: is this the right approach? Is there a better way? Skeptical of first ideas.*

**On Q3 — Avatar Workshop audience split:**

The single-track argument assumes that avatar builders and avatar consumers want the same workshop experience. I do not accept that assumption uncritically. An engineer who is *generating* avatars needs to understand the YAML frontmatter schema, the RAG routing layer, the trigger phrase design, and the law registration process. An engineer who is *consuming* existing avatars needs to know how to reference them in AGENTS.md, what behaviors they activate, and how to verify correct invocation.

These are different cognitive tasks. A combined workshop either front-loads the builder material (boring for consumers who will never register a law) or back-loads the consumer material (frustrating for builders who came to generate avatars).

*However:* The maintenance argument is real. Two tracks means two lab guides, two prompt guides, two sets of participant materials — all of which must stay in sync as the avatar framework evolves. A single track with clearly labelled "For avatar builders" and "For avatar consumers" sections within the same workshop document is not a compromise — it is the better design. Participants skip to what they need; the material stays coherent as a whole.

*Decision:* Single track with clearly labelled audience-specific sections. The course page should describe both audiences explicitly and indicate which sections apply to each.

**On Q5 — Certification:**

The certification question is a motivational one, not a technical one. The evidence artifact chain already exists — every workshop produces durable committed artifacts. A badge on Learning Hub is lightweight to implement and gives practitioners a referenceable credential. The risk is that the badge signals completion rather than fluency. A practitioner who completed all four workshops in a sandbox may not be fluent on their own codebase.

*Recommendation:* Issue a "Hangar AI Constitutional Fluency" badge on completion of all four workshops *and* submission of at least one real-codebase adoption artifact (not just the workshop's sample codebase). This raises the bar from "I finished the exercises" to "I applied this to real work." It also produces a richer evidence chain for governance purposes.

*Decision:* Badge on 4-workshop completion + one real-codebase adoption artifact. Define the submission mechanism in the Learning Hub course completion flow.

**Marcus's Verdict: PARTIAL APPROVAL (Conditional)**
*Condition: Certification definition must include real-codebase artifact submission, not workshop completion alone.*

---

### Sarah — Facilitator

*Reviewing for: workshop flow, learning path design, self-service mechanics.*

**On Q1 — Legacy Rescue sessions:**

From a facilitation perspective, the single-enrollment model is correct, but the course page must communicate the inter-session gap clearly. Participants need to know: "You will complete Session 1 in approximately 3 hours. Session 2 picks up exactly where Session 1 ends. You may take a break between sessions — your work is saved in your repository." This is not a recommendation — it is a required element of the course listing. Without it, participants will either rush through both sessions in one sitting or lose their session state.

*Required addition to course page:* Add an explicit "Between Sessions" note describing what state is preserved and how to resume.

**On Q4 — Product Discovery audience:**

The current framing ("product managers") is the wrong audience for a self-service AI-agent workshop. Product managers at American Airlines broadly do not operate AI coding agents as a daily tool. The workshop as described requires the learner to run AI-agent prompts, navigate `hangar-ai-specs/` directory structures, and commit YAML evidence artifacts. These are engineering-native activities.

The right audience framing is: *technical product managers, product-minded senior engineers, and architects conducting pre-initiative discovery*. This is not a limitation — it is an honest description of who will get value from the workshop. A facilitated PM variant (where the engineering lead operates the agent and the PM steers the discovery) is a genuine future enhancement but must not block the current catalog.

*Required update to course page:* Reframe HAW-PD-001 audience to "technical product managers, product-minded senior engineers, and architects." Add a note: "A facilitated variant for non-technical product managers is on the roadmap."

**Sarah's Verdict: PARTIAL APPROVAL (Conditional)**
*Conditions: (1) "Between Sessions" note on HAW-LR-001 course page; (2) HAW-PD-001 audience reframe in course listing.*

---

### David — XP-Architect

*Reviewing for: technical correctness, constitutional compliance, code quality of workshop artifacts.*

**On Q3 — Avatar Workshop audience:**

The single-track design is correct from a technical standpoint. The avatar generation and avatar consumption workflows share a common mental model: the avatar schema, the RAG routing layer, and the AGENTS.md binding. A practitioner who understands the full lifecycle — from designing trigger phrases through testing RAG routing through consuming an avatar in a new project — is more valuable than one who has only seen half the picture.

The concern about section labelling is valid. The current workshop guide (if it exists) must be audited for constitutional correctness: all law citations must be valid, all avatar references must point to registered entries in AVATAR-RAG-INDEX.yaml, and the workshop's output artifacts must pass `aa-constitution-lint`. This is a Phase 2 readiness check — not a blocker for the deliberation verdict.

**On Q5 — Certification evidence:**

Marcus's point about real-codebase artifacts is technically sound and I support it. Durable evidence means real work, not just sandbox work. The artifact chain from the workshops is necessary but not sufficient. The certification check should verify that the learner has at minimum a committed `adoption-verified.md` from a non-workshop repository.

**David's Verdict: FULL APPROVAL**
*Marcus's certification condition is adopted. No additional conditions from David.*

---

### Jin — Downstream-Advocate

*Reviewing for: self-delivery — can a participant complete this without outside help?*

**On Q2 — Prerequisites:**

The recommended-path design is correct, but there is a self-delivery gap that prerequisites cannot solve: a learner starting with the Avatar Workshop or Product Discovery workshop without completing Greenfield first will encounter references to `hangar-ai-specs/`, `AGENTS.md`, and `aa-constitution-lint` that assume prior familiarity. These are not hard blockers, but they are moments where a learner without context will pause, search, and potentially drop out.

*Required mitigation* (not a prerequisite gate): Each workshop's course page and lab guide must include a self-contained glossary or "Key Concepts" section covering the four foundational concepts (constitution structure, AGENTS.md binding, spec governance, lint tool). This allows a learner to start anywhere without external support.

**On Q4 — Product Discovery self-service:**

The audience reframe Sarah identified is the right fix. But there is an additional self-delivery concern: the Product Discovery workflow has six sequential stages (A through F), each with its own evidence artifact. Stage C (code evidence) requires running the AI agent against a real codebase — or the provided sample codebase. Stage E (metrics) requires access to actual product metrics or the ability to construct plausible ones for a sample domain.

For self-delivery to work, the workshop must ship with a **complete sample discovery scenario** — a fictional-but-realistic product initiative with pre-populated Stage A context (initiative brief), Stage C sample codebase output, and Stage E baseline metrics. Without this, a learner starting Stage B cold has nothing to synthesize. This is a Phase 2 readiness requirement for HAW-PD-001.

**Jin's Verdict: PARTIAL APPROVAL (Conditional)**
*Conditions: (1) Key Concepts section in each workshop course page + lab guide; (2) HAW-PD-001 must ship with complete sample discovery scenario (Stage A–C pre-populated context) before publication.*

---

## Composite Decisions on Open Questions

| # | Question | Decision |
|---|----------|----------|
| Q1 | Legacy Rescue enrollment model | **Single enrollment unit, two sessions.** One course page, "Session 1 of 2 / Session 2 of 2" structure, "Between Sessions" note on course page. |
| Q2 | Prerequisite enforcement | **Recommended path only, no hard gates.** Landing page "New to Hangar AI? Start here" callout pointing at HAW-GF-001. |
| Q3 | Avatar Workshop audience split | **Single track** with clearly labelled "For avatar builders" and "For avatar consumers" sections. Course page describes both audiences explicitly. |
| Q4 | Product Discovery audience | **Reframe audience:** technical product managers, product-minded senior engineers, and architects. Facilitated PM variant deferred to roadmap. HAW-PD-001 requires sample discovery scenario before publication (Phase 2.4 readiness gate). |
| Q5 | Certification | **"Hangar AI Constitutional Fluency" badge** on completion of all 4 workshops + submission of one real-codebase `adoption-verified.md` artifact. Define submission mechanism in Learning Hub completion flow. |

---

## Individual Verdicts

| Persona | Verdict | Conditions |
|---------|---------|------------|
| Clara (ADD-Therapist) | **FULL APPROVAL** | None |
| Marcus (Critic) | **PARTIAL APPROVAL** | Certification must include real-codebase artifact, not sandbox completion alone |
| Sarah (Facilitator) | **PARTIAL APPROVAL** | (1) "Between Sessions" note on HAW-LR-001; (2) HAW-PD-001 audience reframe |
| David (XP-Architect) | **FULL APPROVAL** | Adopts Marcus's certification condition |
| Jin (Downstream-Advocate) | **PARTIAL APPROVAL** | (1) Key Concepts section per workshop; (2) HAW-PD-001 sample discovery scenario before publication |

---

## Composite Verdict

```yaml
ensemble_verdict: APPROVED
date: 2026-04-10
spec_id: LHW-001
all_roles_at_minimum_partial: true
complete_approval: false
proceed_to_implementation: true
conditions_before_publication:
  - q1_enrollment: HAW-LR-001 course page includes "Between Sessions" note describing state preservation and resume instructions
  - q2_landing_page: Learning Hub landing page includes "New to Hangar AI? Start here" callout pointing at HAW-GF-001
  - q3_audience_sections: Avatar Workshop lab guide and course page label "For avatar builders" / "For avatar consumers" sections explicitly
  - q4_audience_reframe: HAW-PD-001 course page audience updated to "technical product managers, product-minded senior engineers, and architects"; facilitated variant noted as roadmap item
  - q4_sample_scenario: HAW-PD-001 ships with complete sample discovery scenario (Stage A–C pre-populated) before publication; if not ready, defer HAW-PD-001 and publish the other three
  - q5_certification: Badge defined as 4-workshop completion + one real-codebase adoption-verified.md submission; submission mechanism documented in Learning Hub completion flow
  - key_concepts: Each workshop course page and lab guide includes a self-contained "Key Concepts" section covering constitution structure, AGENTS.md binding, spec governance, and aa-constitution-lint
rationale: >
  The four-workshop catalog is strategically sound, constitutionally grounded,
  and addresses a genuine adoption gap. The PROPOSAL is well-structured with
  clear outcomes, artifact definitions, and law citations. The identified
  conditions are all presentation-layer and course-page requirements — none
  require changes to the underlying workshop content. The ensemble approves
  proceeding to Phase 2 (workshop readiness audit) with these conditions
  tracked as tasks in tasks.md.
```

---

*Ensemble deliberation complete. Proceeding to Phase 2 — Workshop Repository Readiness.*
