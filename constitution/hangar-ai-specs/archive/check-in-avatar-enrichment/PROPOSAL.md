# Proposal: Check-In Avatar Enrichment — Replace Templated Data with Real Domain Knowledge

**Proposal ID:** check-in-avatar-enrichment  
**Submitted:** February 23, 2026  
**Status:** IN PROGRESS — Phase 1 complete, Phase 2a requires team sessions, Phase 2b is autonomous code assessment

---

## Problem

The Check-In Travel avatar (`avatars/product-type/check-in-travel/`) was created during the Product Avatar Enrichment proposal (enrich-product-avatars-rag-pipeline). Its **structural framework is real** — it follows the correct constitution schema, cites the right PRD laws, and mirrors technology avatar patterns. But **every data point inside is fabricated.**

AI agents that retrieve Check-In avatar context will cite plausible-sounding but fake numbers, personas, journeys, and metrics. This is worse than having no data — it's confidently wrong data.

### What's Fabricated

| File | Fabricated Content | Example |
|------|-------------------|---------|
| `manifest.yaml` | Domain description, personas, journeys, dependencies | "1.7M daily passengers across 6,800+ flights" |
| `guidance.md` | KPIs, success stories, persona guidance, Q&A | "52% → 72% mobile adoption", "$13M annual savings" |
| `ADOPTION.md` | Journeys, KPIs, Gherkin scenarios | "78% on-time performance", "120+ concurrent gates" |
| `examples/personas.md` | 4 personas with ages, roles, behaviors | "Alex Chen, 38, Corporate Executive, 15+ flights/yr" |
| `examples/PRD-1.1-discovery.md` | Research data, competitive benchmarks | "N=200 digital travelers, 450 observed, 140 deep interviews" |
| `examples/PRD-2.1-journey.md` | Journey maps with touchpoints | Fabricated 5-phase journey with specific timings |
| `examples/PRD-3.1-roadmap.md` | Prioritization scores, roadmap items | "40% passenger + 40% operational + 20% effort" |
| `examples/PRD-4.1-mvp.md` | MVP definitions, daily volumes | "offline barcode fallback, 900K daily passengers" |
| `examples/PRD-5.1-metrics.md` | KPI tiers, targets, OKR definitions | "92% system reliability", "3.2x revenue per traveler" |
| `use-cases/digital-check-in/README.md` | 12-month use case with metrics | Fabricated adoption curve |
| `use-cases/gate-operations/README.md` | Gate operations use case | Fabricated operational flows |
| `use-cases/mobile-check-in/README.md` | Mobile/kiosk use case | Fabricated counter scenarios |

### What's Real

- ✅ File structure and naming conventions
- ✅ Law citations (PRD-1.1 through PRD-5.1, ENG-*)
- ✅ Constitution compliance patterns
- ✅ ADOPTION.md framework (Gherkin structure, law mapping)
- ✅ Links to skills and related avatars

### Impact

Without real data, the constitution **cannot be used for agentic workflows** with the Check-In team. Hangar Labs wants to leverage the constitution to discover where AI agents can accelerate check-in development — but agents grounded in fake data will produce fake recommendations.

---

## Solution

A four-phase approach that first creates **reusable enrichment templates** (applicable to any product avatar), then fills them with **real Check-In domain data** through collaborative workshops, then **replaces all fabricated content**, and finally **discovers agentic workflow opportunities** grounded in reality.

### Phase 1: Reusable Enrichment Templates ✅

Create 5 structured worksheets in `docs/templates/enrichment/` that any product team can fill out to enrich their avatar. These are distinct from the existing creation templates in `docs/templates/avatars/` — those scaffold new avatars from scratch; these replace templated data with real data.

| Template | Purpose | Session With |
|----------|---------|--------------|
| `01-metrics-collection.md` | Capture real KPIs, actuals, dashboards | Product Owner, Ops Manager |
| `02-persona-validation.md` | Validate/replace fabricated personas | Product Owner, UX Researcher |
| `03-codebase-assessment.md` | Map real services, APIs, tech stack | Tech Lead, Architect |
| `04-domain-model-inventory.md` | Document entities, rules, event flows | Domain Expert, Senior Engineer |
| `05-agentic-workflow-discovery.md` | Identify AI agent opportunities | Hangar Labs + Product Team |

### Phase 2a: Team Sessions — People-Knowledge (requires Check-In team)

These worksheets capture knowledge that lives in people's heads — metrics, priorities, personas, pain points. Cannot be extracted from code.

To minimize session time, we **pre-fill worksheets with the avatar's templated data** so the team reacts ("that's wrong, it's actually X") rather than starting from blank. Pre-filled prep sheets are in `hangar-ai-specs/changes/check-in-avatar-enrichment/worksheets/`.

| Session | Worksheet | Prep Sheet | Duration | Participants | Output |
|---------|-----------|-----------|----------|-------------|--------|
| 1 | Metrics Collection | `01-metrics-collection-checkin.md` (pre-filled with templated KPIs, tiers, dashboards) | 1 hr | Product Owner + Analytics Lead | Real KPIs, tiers, dashboard locations |
| 2 | Persona Validation | `02-persona-validation-checkin.md` (pre-filled with 4 templated personas + segment data) | 1 hr | Product Owner + UX Researcher | Validated personas with real goals/pains |

**Team commitment:** 2 sessions, ~2 hours total. Pre-filled worksheets sent 24 hours before each session.

### Phase 2b: Autonomous Code Assessment — Code-Knowledge (Hangar Labs only)

Once the Check-In team provides their **codebase inventory** (repo URLs, service names), Hangar Labs can fill the remaining worksheets autonomously by scanning repos, git history, CI configs, and code structure. No team time required.

| Worksheet | What Gets Extracted | How |
|-----------|-------------------|-----|
| Codebase Assessment (W3) | Service inventory, language/framework, test coverage %, API endpoints, dependencies, CI/CD config | Scan repos: `pom.xml`/`package.json`, test dirs, OpenAPI specs, CI YAML |
| Domain Model Inventory (W4) | Entities/aggregates, event flows, business rules in code, domain glossary | Scan model classes, event handlers, validation logic, DB schemas |
| Agentic Workflow Discovery (W5 — partial) | Common code change patterns, error hotspots, PR frequency by type | `git log --stat`, CI failure rates, test coverage gaps |

**What still needs the team for W5:** Pilot selection, success criteria, and prerequisite/blocker assessment require a collaborative session after the code analysis is done.

| Session | Worksheet | Duration | Participants | Output |
|---------|-----------|----------|-------------|--------|
| 3 | Agentic Workflow Discovery (review) | 1.5 hr | Hangar Labs + Full Team | Validate code findings, select pilots |

**Total team commitment across Phase 2a + 2b:** 3 sessions, ~3.5 hours (down from 5 sessions, ~8 hours).

**Output:** 5 completed worksheets stored in `hangar-ai-specs/changes/check-in-avatar-enrichment/worksheets/`

### Phase 3: Avatar Enrichment — Replace All Fabricated Data

Using the completed worksheets from Phase 2, rewrite every fabricated data point in the avatar:

| File | What Gets Replaced | Data Source (Worksheet) |
|------|-------------------|----------------------|
| `manifest.yaml` | Domain description, personas list, journeys, dependencies, tech stack | W2 (Personas) + W3 (Codebase) |
| `guidance.md` | All metrics, persona guidance sections, success stories, Q&A | W1 (Metrics) + W2 (Personas) |
| `ADOPTION.md` | Journey descriptions, KPIs, Gherkin scenario data | W1 (Metrics) + W4 (Domain) |
| `examples/personas.md` | All 4 personas (names, ages, roles, goals, pains) | W2 (Personas) |
| `examples/PRD-1.1-discovery.md` | Research data, competitive benchmarks, sample sizes | W1 (Metrics) + W2 (Personas) |
| `examples/PRD-2.1-journey.md` | Journey maps, touchpoints, timings | W4 (Domain) |
| `examples/PRD-3.1-roadmap.md` | Prioritization scores, roadmap items | W1 (Metrics) + W4 (Domain) |
| `examples/PRD-4.1-mvp.md` | MVP definitions, daily volumes, scope | W3 (Codebase) + W4 (Domain) |
| `examples/PRD-5.1-metrics.md` | KPI tiers, targets, OKR definitions | W1 (Metrics) |
| `use-cases/digital-check-in/README.md` | Full use case with real metrics | W1 + W4 |
| `use-cases/gate-operations/README.md` | Full use case with real ops data | W1 + W3 + W4 |
| `use-cases/mobile-check-in/README.md` | Full use case with real channel data | W1 + W3 + W4 |

**Constraint:** The constitutional structure (law citations, skill references, PRD section layout) stays intact. Only data values change.

### Phase 4: Agentic Workflow Discovery — Ground Recommendations in Reality

With the enriched avatar reflecting real domain data:

1. **Run the enriched avatar against real check-in codebases** — AI agents now have accurate context
2. **Validate worksheet 5 findings** — Compare Hangar Labs' agentic workflow candidates against what the enriched avatar actually surfaces
3. **Select 1-2 pilot workflows** — Define success criteria, duration, ownership
4. **Document findings** — Add agentic workflow recommendations to `guidance.md` and create AGENTS.md guidance for check-in repos

---

## Reference Ideas (Non-Validated) — Express Bags Comprehensive Spec

The PDF **EXPRESS_BAGS_COMPREHENSIVE_SPEC.pdf** contains a prior (templated) proposal for the Express Bags Prep Eligibility service. It is **not real data**, but it is a rich idea mine for Check-In improvements and agentic workflows. Use these as **hypotheses to validate** during Phases 2-4, not as facts.

**High-signal ideas to consider (tagged to laws):**

- **Audit trail & decision logging** (BUS-2.6, ENG-1.1): full eligibility decision context, compliance queries, analytics dashboard
- **Human-readable, accessible error messaging** (PRD-3.5, ENG-1.5): no error codes, screen-reader text, multilingual, actionable next steps
- **Tier-based VIP windows** (BUS-3.2): loyalty tier extensions, tier caching, fraud prevention
- **Proactive bag weight advisory** (BUS-1.2): predictive weight models, repack/ship/fee options, multi-channel messaging, quiet hours
- **Gate agent dashboard** (BUS-2.1/2.3): real-time queue status, staffing recommendations, accessibility highlights, anomaly detection
- **Resilience & observability** (ENG-3.2): timeouts, retries, circuit breakers, p50/p95/p99 upstream metrics
- **Testing pyramid & acceptance specs** (ENG-4.2): unit/integration/E2E ratios and Gherkin spec coverage
- **API contract standardization** (ENG-5): consistent error schema with actionRequired + accessibility flags
- **Agentic integration patterns** (AA-CHK-006): structured data contract for predictive advisories
- **Roadmap structure**: 3-phase delivery (foundation → personalization → operational intelligence)

**Where to apply these ideas in this proposal:**

- Phase 2b (code assessment): look for existing hooks in code that align to audit trails, error schemas, observability, and dashboards
- Phase 3 (avatar rewrite): convert validated ideas into real examples, metrics, and roadmaps
- Phase 4 (agentic workflows): use ideas to shape pilot candidates (e.g., audit-trail analysis agent, proactive advisory agent)

---

## Files Changed

### Phase 1 (New — Reusable Templates)

| File | Action |
|------|--------|
| `docs/templates/enrichment/01-metrics-collection.md` | Created |
| `docs/templates/enrichment/02-persona-validation.md` | Created |
| `docs/templates/enrichment/03-codebase-assessment.md` | Created |
| `docs/templates/enrichment/04-domain-model-inventory.md` | Created |
| `docs/templates/enrichment/05-agentic-workflow-discovery.md` | Created |

### Phase 2 (Worksheets — Pre-filled for Team Sessions)

| File | Action |
|------|--------|
| `hangar-ai-specs/changes/check-in-avatar-enrichment/worksheets/01-metrics-collection-checkin.md` | Created (pre-filled with templated metrics for team to correct) |
| `hangar-ai-specs/changes/check-in-avatar-enrichment/worksheets/02-persona-validation-checkin.md` | Created (pre-filled with templated personas for team to validate) |
| `hangar-ai-specs/changes/check-in-avatar-enrichment/worksheets/03-codebase-assessment-checkin.md` | To create |
| `hangar-ai-specs/changes/check-in-avatar-enrichment/worksheets/04-domain-model-inventory-checkin.md` | To create |
| `hangar-ai-specs/changes/check-in-avatar-enrichment/worksheets/05-agentic-workflow-discovery-checkin.md` | To create |

### Phase 3 (Modified — Avatar Files)

| File | Action |
|------|--------|
| `avatars/product-type/check-in-travel/manifest.yaml` | Rewrite fabricated fields |
| `avatars/product-type/check-in-travel/guidance.md` | Rewrite fabricated metrics/stories |
| `avatars/product-type/check-in-travel/ADOPTION.md` | Rewrite fabricated KPIs/journeys |
| `avatars/product-type/check-in-travel/examples/personas.md` | Rewrite all personas |
| `avatars/product-type/check-in-travel/examples/PRD-1.1-discovery.md` | Rewrite research data |
| `avatars/product-type/check-in-travel/examples/PRD-2.1-journey.md` | Rewrite journey maps |
| `avatars/product-type/check-in-travel/examples/PRD-3.1-roadmap.md` | Rewrite roadmap/scores |
| `avatars/product-type/check-in-travel/examples/PRD-4.1-mvp.md` | Rewrite MVP definitions |
| `avatars/product-type/check-in-travel/examples/PRD-5.1-metrics.md` | Rewrite KPI tiers/targets |
| `avatars/product-type/check-in-travel/use-cases/digital-check-in/README.md` | Rewrite with real data |
| `avatars/product-type/check-in-travel/use-cases/gate-operations/README.md` | Rewrite with real data |
| `avatars/product-type/check-in-travel/use-cases/mobile-check-in/README.md` | Rewrite with real data |

### Phase 4 (New — Agentic Workflow Artifacts)

| File | Action |
|------|--------|
| `avatars/product-type/check-in-travel/guidance.md` | Add agentic workflow section |
| Pilot repo AGENTS.md files | To create (repos TBD in Phase 2) |

---

## Success Criteria

| Criteria | Target | Current |
|----------|--------|---------|
| Reusable enrichment templates | 5 worksheets | ✅ 5 |
| Completed worksheets (Check-In) | 5 filled | ⬜ 0 |
| Avatar files with zero fabricated data | 12 files | ⬜ 0 |
| Agentic workflow pilots selected | 1-2 | ⬜ 0 |
| Validated with real codebase query | Pass | ⬜ Not started |

---

## Dependencies

- **Check-In team availability** — 3 sessions, ~3.5 hours total commitment (down from 5 sessions / 8 hours)
- **Access to real metrics** — Product Owner must be able to share KPIs (even directional)
- **Codebase inventory** — Team provides repo URLs and service names (one-time, ~15 min). Hangar Labs does the rest.
- **Hangar Labs capacity** — Autonomous code assessment for W3, W4, and partial W5 (~1-2 days of scanning/analysis)

## Open Questions

1. Which check-in repos should be used for the Phase 4 agentic pilot? (Resolved in Phase 2b codebase inventory)
2. Are there data sensitivity constraints on real metrics? (Some may need to be directional rather than exact)
3. Should Cargo and Loyalty avatars follow the same enrichment process? (Likely yes — use same templates)

## References

- [Enrichment Templates](../../../docs/templates/enrichment/)
- [Check-In Avatar](../../../avatars/product-type/check-in-travel/)
- [Creation Templates](../../../docs/templates/avatars/) — existing scaffold templates (distinct from enrichment)
- [Prior Proposal: Product Avatar Enrichment](../enrich-product-avatars-rag-pipeline/PROPOSAL.md) — created the avatar framework
- [Prior Proposal: RAG Routing Layer](../rag-routing-layer/PROPOSAL.md) — fixed agent pipeline traversal
