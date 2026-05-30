# Progress: Check-In Avatar Enrichment

**Last Updated:** February 23, 2026

---

## Status Summary

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1: Reusable Enrichment Templates | ✅ Complete | 5 worksheets created in `docs/templates/enrichment/` |
| Phase 2a: Team Sessions (People-Knowledge) | 🟡 Prep Done | Pre-filled worksheets ready; 2 sessions with Check-In team (~2 hrs) for metrics + personas |
| Phase 2b: Autonomous Code Assessment | ⬜ Not Started | Hangar Labs scans repos for W3, W4, partial W5 (no team time needed) |
| Phase 2c: Workflow Discovery Review | ⬜ Not Started | 1 session to validate code findings + select agentic pilots (~1.5 hrs) |
| Phase 3: Avatar Enrichment | ⬜ Not Started | Blocked by Phase 2a + 2b (need real data from both tracks) |
| Phase 4: Agentic Workflow Discovery | ⬜ Not Started | Blocked by Phase 3 (need enriched avatar) |

**Overall:** 25% complete (Phase 1 of 4).

---

## Phase 1 Details: Enrichment Templates

Created 5 reusable enrichment worksheets:

| Template | Purpose | Lines |
|----------|---------|-------|
| `docs/templates/enrichment/01-metrics-collection.md` | KPIs, tiers, dashboards, measurement gaps | ~90 |
| `docs/templates/enrichment/02-persona-validation.md` | Validate/replace personas, internal users, prioritization | ~100 |
| `docs/templates/enrichment/03-codebase-assessment.md` | Service inventory, APIs, integrations, test coverage, tech stack | ~110 |
| `docs/templates/enrichment/04-domain-model-inventory.md` | Entities, business rules, event flows, exceptions, glossary | ~120 |
| `docs/templates/enrichment/05-agentic-workflow-discovery.md` | Time audit, change patterns, error hotspots, pilot selection | ~110 |

These are reusable across any product avatar (Cargo, Loyalty, etc.), not Check-In-specific.

---

## Phase 2 Readiness: Discovery Sprint

### Track A: Team Sessions (People-Knowledge)

Pre-filled worksheets created — present templated data for team to react to (confirm / correct / replace).

| # | Session | Prep Sheet | Duration | Participants Needed |
|---|---------|-----------|----------|-------------------|
| 1 | Metrics Collection | `worksheets/01-metrics-collection-checkin.md` ✅ Pre-filled | 1 hr | Product Owner + Analytics Lead |
| 2 | Persona Validation | `worksheets/02-persona-validation-checkin.md` ✅ Pre-filled | 1 hr | Product Owner + UX Researcher |

### Track B: Autonomous Code Assessment (Hangar Labs only)

Once the team provides a **codebase inventory** (repo URLs + service names), Hangar Labs fills worksheets by scanning code. No meetings required.

| Worksheet | Extraction Method | Estimated Effort |
|-----------|------------------|------------------|
| W3 Codebase Assessment | Scan `pom.xml`/`package.json`, test dirs, OpenAPI specs, CI YAML | ~4 hrs |
| W4 Domain Model Inventory | Scan model classes, events, validation, DB schemas | ~4 hrs |
| W5 Agentic Discovery (partial) | `git log --stat`, CI failures, test gaps, PR patterns | ~2 hrs |

### Track C: Collaborative Review

| # | Session | Duration | Participants |
|---|---------|----------|--------------|
| 3 | Agentic Workflow Discovery — review code findings + select pilots | 1.5 hr | Hangar Labs + Full Team |

**Total team time: ~3.5 hours** (2 sessions + 1 review) instead of ~8 hours.

### Prep Checklist

- [x] Pre-fill W1 metrics worksheet with templated data from avatar
- [x] Pre-fill W2 persona worksheet with templated data from avatar
- [ ] Identify Check-In Product Owner
- [ ] Get codebase inventory from Tech Lead (repo URLs + service names — ~15 min ask)
- [ ] Send pre-filled worksheets to participants 24 hours before sessions
- [ ] Schedule 2 team sessions (Track A)
- [ ] Hangar Labs runs autonomous code assessment (Track B)
- [ ] Schedule review session after Track A + B complete (Track C)
- [ ] Confirm data sensitivity constraints (can we use exact metrics or directional only?)

---

## Files Changed

| Commit | Files | Description |
|--------|-------|-------------|
| Pending | 5 template files | Phase 1: Enrichment worksheets |
| TBD | 5 completed worksheets | Phase 2: Filled worksheets (after sessions) |
| TBD | 12 avatar files | Phase 3: Fabricated → real data |
| TBD | guidance.md + pilot AGENTS.md | Phase 4: Agentic workflow artifacts |

---

## Archive Note

**Archived:** 2026-04-09
**Reason:** Paused — moving focus to other product teams. Phase 1 (enrichment worksheets) complete. Phases 2-4 require Check-In team scheduling and codebase access; resumable when team availability opens up.
