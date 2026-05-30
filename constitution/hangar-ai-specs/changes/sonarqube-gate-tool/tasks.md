# Tasks: sonarqube-gate-tool

> Atomic tasks following the Hangar AI Constitution strictly.
> Update status after each task completes.

---

## Workstream 1 — `tools/sonarqube-gate/` in Constitution Repo

- [ ] **1-01** Create `tools/sonarqube-gate/gate-config.json` — machine-readable definition of all 9 Hangar AI Constitution Gate conditions (AA baseline 4 + HARD_BLOCK 3 + PHASE_GATE 1 + WARNING 1)
- [ ] **1-02** Create `tools/sonarqube-gate/docker-compose.yml` — project-agnostic SonarQube 10.7 Community + PostgreSQL 15; no hardcoded project keys; healthchecks; named volumes
- [ ] **1-03** Create `tools/sonarqube-gate/provision.sh` — idempotent; accepts `--project-key` and `--token-path`; start Docker → wait healthy → create gate from `gate-config.json` → create project → write token
- [ ] **1-04** Create `tools/sonarqube-gate/README.md` — quick start guide: zero to FAIL state in < 5 minutes; corporate SonarQube alternative path; `.gitignore` reminder for `.sonar-token`
- [ ] **1-05** Verify `tools/sonarqube-gate/` works end-to-end against live SonarQube at localhost:9000

---

## Workstream 2 — New Law: ENG-12 Agentic Compliance Feedback Loop

- [ ] **2-01** Create `laws/engineering/agentic-feedback.md` with ENG-12.1 (Agentic Feedback Loop — NON-NEGOTIABLE), ENG-12.2 (Dashboard-First Development), ENG-12.3 (External Referee Law)
- [ ] **2-02** Register ENG-12.x in `laws/engineering/_domain.yaml` (law registry)
- [ ] **2-03** Verify no existing law ID conflicts with ENG-12.x

---

## Workstream 3 — Update `adoption.md`

- [ ] **3-01** Add Phase 2b "Provision the Constitutional Gate" after Phase 2 (Adopt) and before Phase 3 (Verify) — includes `provision.sh` command, dashboard URL, "keep open throughout session" instruction
- [ ] **3-02** Add ENG-12.1 citation to Phase 2b gate in the phase table
- [ ] **3-03** Update conditional skip logic — if `.sonar-token` exists AND gate is already provisioned, Phase 2b may be skipped

---

## Workstream 4 — Update `skill-sonarqube-compliance-gate.md`

- [ ] **4-01** Add "Prerequisites — Local Development" section: run `tools/sonarqube-gate/provision.sh`, token auto-written, URL is `http://localhost:9000`
- [ ] **4-02** Add "Prerequisites — Corporate SonarQube" section: existing env var approach (no change to existing content)
- [ ] **4-03** Add ENG-12.2 citation: "The dashboard MUST be open throughout the session — it is the human review checkpoint, not the API call alone"
- [ ] **4-04** Update Integration Checklist: add `[ ] SonarQube dashboard open at project URL`

---

## Workstream 5 — Update `AGENTS.md`

- [ ] **5-01** Add `tools/sonarqube-gate/` to project structure tree alongside `tools/constitution-lint/`
- [ ] **5-02** Add ENG-12.1 to the Non-Negotiable Laws section
- [ ] **5-03** Add `tools/sonarqube-gate/` to governance tools table with description: "Provision the Constitutional Gate — one command from zero to FAIL state"

---

## Workstream 6 — Update Application Guide

- [ ] **6-01** Add Step 0b "Provision the Constitutional Gate" to `exercises/application-guide.html` — reference `tools/sonarqube-gate/provision.sh` from constitution repo; frame as human engagement interface; dashboard-open instruction
- [ ] **6-02** Move SonarQube setup from "Optional" callout to core Step 0b with framing: "This is what turns agentic development from best-effort into objectively governed"
- [ ] **6-03** Keep optional callout for teams using corporate SonarQube — they skip provision.sh but must still open the dashboard

---

## Final

- [ ] **F-01** Commit and push all Workstream 1-5 changes to `hangar-ai-constitution` repo
- [ ] **F-02** Commit and push Workstream 6 changes to `hangar-ai-constitution-workflows` repo
- [ ] **F-03** Mark PROPOSAL.md status: IMPLEMENTED
