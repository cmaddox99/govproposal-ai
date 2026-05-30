# Stage A Evidence: Problem Framing
## Changeset: `build-adoption-guide-2026-001`
**Stage:** A — Problem Framing  
**Status:** COMPLETE  
**Authority:** PRD-2.5 ⛔ — Evidence artifact required for stage transition  
**Next Stage Gate:** Stage B (Assumption Mapping) requires 3+ coach interviews or quantitative evidence to reclassify to Moderate per PRD-1.5 ⛔

---

## Evidence Classification (PRD-1.5 ⛔)

**Level: WEAK** — Repository structural inspection only; no customer interviews on file at time of this artifact.

Weak evidence is valid for Stage A (Problem Framing) per PRD-2.5. Stage C (JTBD) cannot begin until evidence is reclassified to Moderate or Strong through Stage B validation activities.

---

## Problem Statement (PRD-1.2 ⛔ Template)

| Field | Content |
|-------|---------|
| **Who** | Technical coaches and senior architects onboarding new engineering teams to the Hangar AI Constitution |
| **Problem** | No unified, navigable, persona-aware entry point connects the laws, skills, avatars, and RAG model into a coherent adoption path |
| **Evidence** | Repository inspection — see structural observations below (Weak) |
| **Frequency** | Every new team onboarding engagement; estimated 3–5 per quarter per technical coach |
| **Severity** | HIGH — friction compounds across every engagement; no incremental adoption path exists |

---

## Structural Observations (Source: Repository Inspection)

The following gaps were observed by direct inspection of `/Users/979925/Repos/governance/hangar-ai-constitution/` on 2026-05-01:

| # | Observation | Files Inspected |
|---|-------------|----------------|
| 1 | No landing page exists — `README.md` serves as the only structural index | `README.md` |
| 2 | No persona-based quick start for Engineer / AI Agent / New Project / Technical Coach paths | `docs/`, `agent-skills/` |
| 3 | The RAG model visualization artifact exists but has no parent navigation or guide context | Session artifact |
| 4 | 168 laws navigable only by reading raw markdown files — no search or filter interface | `laws/`, `laws/index.yaml` |
| 5 | Avatar selection requires manual exploration of `avatars/` — no selection wizard | `avatars/AVATAR-RAG-INDEX.yaml` |
| 6 | SDD workflow (PROPOSE→IMPLEMENT→ARCHIVE) has no interactive reference format for new adopters | `hangar-ai-specs/`, `agent-skills/skills-by-domain/discovery-research/spec-governance.md` |
| 7 | Skill catalog (29+ skills across 5 domains) not navigable outside raw YAML files | `agent-skills/skills-by-domain/*/index.yaml` |

---

## Stage B Validation Plan

**Required to advance to Stage C:** Evidence reclassified to Moderate (3–4 interviews OR quantitative proxy data).

| Action | Owner | Evidence Artifact |
|--------|-------|------------------|
| Conduct 3+ structured interviews with technical coaches who have attempted constitution onboarding | Product Owner (Priya Kapoor) | `stage-b-evidence.md` |
| Collect quantitative evidence from adoption logs, support tickets, or Slack thread data showing onboarding friction | Compliance Officer (Carlos Mendez) | `stage-b-evidence.md` |
| Jury deliberates evidence strength per PRD-1.5 classification table | All 6 jurors | Deliberation log entry |

---

*Stage A evidence artifact — filed per PRD-2.5 ⛔ Stage A exit criteria*  
*Jury log entry required for Stage A → Stage B transition per BUS-7.1 ⛔*
