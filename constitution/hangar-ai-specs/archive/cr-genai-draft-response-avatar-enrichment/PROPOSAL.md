# Proposal: cr-genai-draft-response Avatar Enrichment — Customer Relations Ops, Azure OpenAI, PostgreSQL/SQLAlchemy, OpenTelemetry Python

**Proposal ID:** cr-genai-draft-response-avatar-enrichment  
**Submitted:** March 18, 2026  
**Status:** PROPOSED  
**Triggered by:** Brownfield adoption analysis of `codebases/oraa/cr-genai-draft-response`

---

## Constitutional Authority

This proposal operates under the following laws and skills.

### Laws Applied

| Law ID | Title | Application |
|--------|-------|-------------|
| **ENG-1.2** | AI-Engineer Pairing Law | All avatar content must cite the law that drives each guidance rule |
| **ENG-4.1** | Atomic TDD Law | Any implementation work following this proposal must follow RED → GREEN → REFACTOR |
| **ENG-4.4** | Test-First Brownfield Law | Characterization tests before any behavior change in the target repo |
| **ENG-10.1** | Constitution Compliance / Brownfield Preservation | No stack rewrite by default; preserve working patterns unless explicitly approved |
| **BUS-1.1** | Priority Hierarchy | Legal, compliance, and PII-safety constraints ranked first in all avatar guidance |
| **BUS-7.1** | Audit Trail Law | Avatar creation decisions, taxonomy gates, and approval must be recorded and traceable |
| **PRD-1.1** | Discovery Law | Product avatar must capture real domain discovery patterns for the Customer Relations Ops domain |
| **PRD-2.1** | User Journey Law | CR Rep journeys (complaint intake → template selection → compliance check → draft generation) must be modeled |
| **PRD-5.1** | MVP Law | Scope each avatar to minimum viable guidance before adding use-case examples |

### Skills Invoked

| Skill | Purpose |
|-------|---------|
| **skill-spec-governance** | Orchestrate this proposal through the Hangar SDD lifecycle |
| **skill-30-taxonomy-governed-avatar-enrichment** | Run taxonomy gates before any avatar is created or extended |
| **skill-21-prompt-engineering** | Inform `azure-openai` and `customer-relations-ops` avatar guidance on prompt governance |
| **skill-13-observability** | Inform `opentelemetry-python` avatar guidance |
| **skill-12-api-design** | Inform `postgresql-sqlalchemy` avatar guidance on async patterns |
| **skill-06-atomic-tdd** | All new avatar artifact code examples must follow Atomic TDD |

---

## Problem

During brownfield adoption planning for `cr-genai-draft-response` (an ORAA AI drafting service for Customer Relations Representatives), a pre-adoption avatar coverage analysis revealed **four gaps** where no existing avatar adequately governs the codebase's domain or technology stack.

Without avatar coverage, the AI agent's retrieval defaults to the nearest general-purpose prior — in this case, generic FastAPI or LangChain patterns — which **cannot encode compliance-critical domain rules** specific to:

- How PII must be redacted before and restored after every LLM call
- How Azure OpenAI deployment names, API versions, and endpoint construction differ from the OpenAI SDK defaults
- How async PostgreSQL sessions must be scoped around PII-encrypted audit columns
- How OpenTelemetry instrumentation must wrap every inbound request and outbound LLM call for observability compliance

The absence of these avatars is a **brownfield governance risk** per `ENG-10.1`: the agent cannot distinguish between safe preservation of compliance logic and rewrite behavior.

### What `cr-genai-draft-response` Does

This service is an **AI-assisted complaint response drafting engine** for internal AA Customer Relations staff. When a representative receives a passenger complaint, the service:

1. Accepts a structured complaint record (category, subcategory, flight details, compensation eligibility, customer history)
2. Routes through a **PII redaction pipeline** before any LLM invocation
3. Executes a **silent 3-stage agent orchestration**: Analysis Agent → Compliance Agent → Drafting Agent (only the final draft is returned; internal reasoning is suppressed)
4. Applies **template governance**: compensation rules, secondary PAX policies, prohibited words/phrases, trademark enforcement, liability language restrictions
5. Validates the draft against trademark and compliance checks
6. Restores PII in the final response
7. Writes an **immutable audit trace** to PostgreSQL with PII-hashed columns
8. Returns the policy-compliant draft to the CR representative

### Current Avatar Coverage Gaps

| # | Layer | What Is Missing | Nearest Current Avatar | Why It Falls Short |
|---|-------|-----------------|----------------------|-------------------|
| 1 | Product-type | AI-assisted complaint response drafting domain | `customer-service` or `internal-productivity` | `customer-service` is written from the customer journey POV (Stranded Passenger, Voluntary Changer personas); it has no guidance for internal CR Rep workflows, silent agent orchestration, or compliance agent chaining. `internal-productivity` covers generic workflow automation but has no guidance on complaint categorization governance, compensation policy compliance, PII redaction pipelines, or prohibited-language enforcement. |
| 2 | Technology | Azure OpenAI Service patterns | `azure-ml` | `azure-ml` governs Azure Machine Learning Studio (pipelines, experiments, model registry). Azure OpenAI Service uses a completely different API surface: deployment names, API versions, endpoint construction (`https://{service}.openai.azure.com`), key-rotation patterns, and custom LLM wrapper conventions. No avatar addresses this. |
| 3 | Technology | Async PostgreSQL with SQLAlchemy + asyncpg | `python-fastapi` (partial) | `python-fastapi` mentions SQLAlchemy in its ORM section but provides no guidance on: async session lifecycle, asyncpg connection pool management, raw SQL migration governance, or PII-encrypted column audit patterns. This service uses all of these patterns. |
| 4 | Technology | OpenTelemetry Python instrumentation | _(none)_ | The service uses the full OTEL stack (`opentelemetry-api`, `opentelemetry-distro`, `opentelemetry-exporter-otlp`, `opentelemetry-instrumentation-fastapi`, `opentelemetry-instrumentation-logging`). No avatar governs Python OTEL instrumentation patterns, span naming, context propagation, or OTLP exporter configuration. |

---

## Taxonomy Governance Position

Per `skill-30-taxonomy-governed-avatar-enrichment`, all proposed avatars must pass five taxonomy gates before creation is approved.

### Taxonomy Gates

**Gate 1: Domain gate** — Does the proposed product avatar represent an independent business capability?  
**Gate 2: Journey gate** — Are there distinct user/operator journeys not covered by existing avatars?  
**Gate 3: Boundary gate** — Is there no material overlap with existing product avatars?  
**Gate 4: Stability gate** — Would this avatar remain valid if the org chart changes?  
**Gate 5: Retrieval gate** — Does this avatar improve RAG routing precision for the target repos?

### Gate Results

#### Product Avatar: `customer-relations-ops`

| Gate | Result | Evidence |
|------|--------|---------|
| Domain gate | ✅ Pass | AI-assisted complaint response drafting is a distinct business capability: complaint intake → triage → compliance-governed draft generation → PII-safe audit. This is not rebooking, not baggage, not general inquiry. |
| Journey gate | ✅ Pass | CR Rep journeys (complaint categorization, template selection, compensation validation, draft review) are not modeled anywhere in `customer-service` (which models passenger journeys, not staff workflows). |
| Boundary gate | ✅ Pass | `customer-service` = passenger-facing journeys. `internal-productivity` = generic automation. Neither covers the compliance-agent orchestration + PII pipeline + CR-staff workflow combination. |
| Stability gate | ✅ Pass | Customer Relations is a permanent operational function at any airline. The domain is independent of ORAA team structure or org changes. |
| Retrieval gate | ✅ Pass | Without this avatar, agents retrieving context for `cr-genai-draft-response` will default to passenger-facing guidance and risk recommending patterns that expose PII or bypass compensation policy compliance. |

#### Technology Avatar: `azure-openai`

| Gate | Result | Evidence |
|------|--------|---------|
| Domain gate | ✅ Pass | Azure OpenAI Service is a distinct runtime with deployment-name routing, API versioning (`api-version=2024-xx-xx`), endpoint construction, and Managed Identity / key patterns that differ materially from generic OpenAI SDK usage. |
| Retrieval gate | ✅ Pass | `azure-ml` will be incorrectly retrieved for any service using `AZURE_OPENAI_KEY`, `AZURE_OPENAI_MODEL`, `AZURE_OPENAI_VERSION`, or `AZURE_OPENAI_SERVICE` env vars, introducing guidance about AzureML pipelines that does not apply. |

#### Technology Avatar: `postgresql-sqlalchemy`

| Gate | Result | Evidence |
|------|--------|---------|
| Domain gate | ✅ Pass | Async PostgreSQL with SQLAlchemy + asyncpg introduces session lifecycle, connection pool, and migration governance patterns that are not present in the generic `python-fastapi` avatar. |
| Retrieval gate | ✅ Pass | The combination of asyncpg, PII-encrypted columns, and raw SQL migration scripts (non-Alembic) is a documented pattern for AA's ORAA codebase family. Dedicated guidance prevents incorrect ORM migration recommendations. |

#### Technology Avatar: `opentelemetry-python`

| Gate | Result | Evidence |
|------|--------|---------|
| Domain gate | ✅ Pass | OTEL instrumentation in Python requires specific patterns for: auto-instrumentation vs. manual spans, `opentelemetry-distro` bootstrapping, OTLP exporter configuration, Dynatrace correlation (as seen in `assets/otel_correlate_logs.png`), and `structlog` integration. None of this is codified in any existing avatar. |
| Retrieval gate | ✅ Pass | Without this avatar, agents assisting with observability work will have no constitutional guidance and may recommend patterns incompatible with AA's Dynatrace/OTLP pipeline. |

---

## Solution

Four phases of avatar creation, each gated by taxonomy review and registry wiring. All phases are **additive only** — no existing avatar content is modified without explicit approval.

### Phase 1: Product Avatar — `customer-relations-ops`

Create a full product avatar for AI-assisted Customer Relations complaint response workflows.

**Scope:**
- Complaint intake and category/subcategory classification workflows (OPERATIONS, ADMIRALS CLUB, INFLIGHT, AIRPORT EXPERIENCE, etc.)
- Silent multi-stage agent orchestration: Analysis → Compliance → Drafting (per `BUS-1.1` priority hierarchy: company policy > explicit instructions > tone > style)
- PII redaction/restoration pipeline wrapping every LLM call (per `ENG-6.5` Input Validation, `BUS-7.1` Audit Trail)
- Template governance: compensation rules by category, secondary PAX rules, prohibited words/phrases, trademark enforcement, liability language constraints
- Compensation validation against category-specific eligibility rules
- Audit trace immutability: all LLM interactions and compensation decisions logged with PII hash chain
- CR Rep-facing journeys: complaint receipt → template selection → compliance review → draft acceptance/rejection → case close

**Artifacts to deliver:**
- `avatars/product-type/customer-relations-ops/manifest.yaml` — domain, personas (CR Specialist, CR Supervisor, Compliance Reviewer), journeys, law specializations
- `avatars/product-type/customer-relations-ops/guidance.md` — PRD law applications, silent agent pattern, PII safety, compensation validation, metrics (draft acceptance rate, compliance pass rate, avg handle time)
- `avatars/product-type/customer-relations-ops/ADOPTION.md` — brownfield adoption process for CR-domain repos, validation gates, workflow steps
- `avatars/product-type/customer-relations-ops/examples/personas.md` — CR Specialist, Supervisor, Compliance Reviewer personas
- `avatars/product-type/customer-relations-ops/use-cases/complaint-draft-generation/README.md` — end-to-end use case: complaint record in → compliant draft out

**Law specializations:**
- `PRD-1.1` — Discovery: complaint category taxonomy, prohibited language catalog, compensation matrix
- `PRD-2.1` — Journey: CR Rep workflow stages and decision points
- `PRD-3.1` — Roadmap: incremental capability delivery (draft quality → compensation accuracy → PII safety)
- `PRD-5.1` — Metrics: draft acceptance rate, compliance violation rate, avg review time
- `BUS-1.1` — Priority Hierarchy: policy compliance must outrank stylistic preferences at every level
- `BUS-7.1` — Audit Trail: every LLM call and compensation decision auditable and immutable
- `ENG-6.5` — Input Validation: all complaint fields validated at boundary; PII stripped before LLM boundary

---

### Phase 2: Technology Avatar — `azure-openai`

Create a technology avatar for Azure OpenAI Service integration patterns.

**Scope:**
- Azure OpenAI endpoint construction: `https://{AZURE_OPENAI_SERVICE}.openai.azure.com`
- Deployment name routing vs. model name routing (key distinction from OpenAI SDK)
- API version governance: pinning `AZURE_OPENAI_VERSION` (`api-version` header), changelog awareness
- Authentication: API key pattern (`AZURE_OPENAI_KEY`) vs. Managed Identity token flow — when to use each
- Custom LLM wrapper conventions: `_call_llm(tid, payload)` pattern, TID (transaction ID) propagation through all LLM calls for traceability
- Rate limit and retry patterns using `tenacity`
- Azure OpenAI + LangChain integration (`langchain-openai` `AzureChatOpenAI`)
- Response validation: `finish_reason`, `content_filter_results`, token usage logging

**Artifacts to deliver:**
- `avatars/technology/azure-openai/manifest.yaml` — stack, dependencies, law specializations
- `avatars/technology/azure-openai/guidance.md` — endpoint patterns, deployment routing, auth, wrapper conventions, error handling
- `avatars/technology/azure-openai/examples/ENG-4.1-wrapper-tdd.md` — Atomic TDD example for custom LLM wrapper with TID propagation

**Law specializations:**
- `ENG-4.1` — Atomic TDD: LLM wrapper must be unit-testable with mocked HTTP responses
- `ENG-6.5` — Input Validation: validate payload structure before Azure OpenAI API call
- `ENG-6.1` — Security: API key must never be logged; Managed Identity preferred for production
- `BUS-7.1` — Audit Trail: TID must propagate through every LLM call for full traceability

---

### Phase 3: Technology Avatar — `postgresql-sqlalchemy`

Create a technology avatar for async PostgreSQL with SQLAlchemy + asyncpg patterns.

**Scope:**
- `asyncpg` connection pool configuration: `min_size`, `max_size`, pool timeout, server-side cursor patterns
- `SQLAlchemy` async session lifecycle: `async_session_maker`, `AsyncSession`, `commit`/`rollback` scope management
- PII-column encryption patterns: encrypted-at-rest column values, hash-based lookup for non-reversible PII fields, key management via environment variables (`PII_ENCRYPTION_KEY`, `PII_ENCRYPTION_SALT`)
- Raw SQL migration governance: `scripts/*.sql` files, versioning strategy, rollback safety, idempotency requirements (when not using Alembic)
- `DBConnector` pattern: single-class connection manager, environment-driven config, health check query patterns
- Integration test patterns: real PostgreSQL via Docker Compose for integration tests, mocked `DBConnector` for unit tests
- Trace table schema governance: immutable audit rows (no UPDATE/DELETE on trace records), `created_at` UTC, structured JSON payloads

**Artifacts to deliver:**
- `avatars/technology/postgresql-sqlalchemy/manifest.yaml` — stack, dependencies, law specializations
- `avatars/technology/postgresql-sqlalchemy/guidance.md` — async session patterns, PII column encryption, migration governance, DBConnector conventions
- `avatars/technology/postgresql-sqlalchemy/examples/ENG-4.1-db-tdd.md` — Atomic TDD for DB connector with mocked SQLAlchemy session

**Law specializations:**
- `ENG-4.1` — Atomic TDD: DB connectors testable with mocked sessions; integration tests use real containers
- `ENG-4.2` — Test Pyramid: unit tests mock sessions; Docker Compose PostgreSQL for integration
- `BUS-7.1` — Audit Trail: trace tables must be append-only; no UPDATE/DELETE on audit records
- `ENG-6.5` — Input Validation: PII field values validated and typed before DB write
- `ENG-6.1` — Security: credentials from env vars only; PII encryption key never logged

---

### Phase 4: Technology Avatar — `opentelemetry-python` *(Medium Priority)*

Create a technology avatar for Python OpenTelemetry instrumentation patterns.

**Scope:**
- `opentelemetry-distro` bootstrapping: `opentelemetry-bootstrap -a install`, auto-instrumentation entry point
- `opentelemetry-instrument` wrapper for uvicorn: span creation, propagation, FastAPI middleware integration
- OTLP exporter configuration: endpoint, protocol (`grpc` vs `http/protobuf`), TLS, header injection
- Manual span creation alongside auto-instrumentation: `tracer.start_as_current_span()` for critical business operations (PII redaction, LLM call, compensation validation)
- `structlog` + OTEL logging correlation: trace ID injection into structured log records
- Dynatrace correlation: OneAgent OTLP-native ingestion, span attribute mapping for Dynatrace dashboards (as used in AA's observability stack)
- Context propagation across async boundaries: `asyncio` task spans, `httpx` async client instrumentation

**Artifacts to deliver:**
- `avatars/technology/opentelemetry-python/manifest.yaml` — stack, dependencies, law specializations
- `avatars/technology/opentelemetry-python/guidance.md` — bootstrapping, OTLP config, manual spans, Dynatrace patterns, structlog correlation

**Law specializations:**
- `ENG-4.1` — Atomic TDD: span emission testable with `opentelemetry-sdk` in-memory exporters
- `BUS-7.1` — Audit Trail: every LLM call and compliance decision must emit a span for observability
- `ENG-1.2` — AI-Engineer Pairing: OTEL configuration decisions must be explainable with law citations

---

### Phase 5: Registry and RAG Wiring

After all avatars are approved and created, update routing artifacts:

1. `avatars/index.yaml` — add `azure-openai`, `postgresql-sqlalchemy`, `opentelemetry-python` entries under `technology`
2. `avatars/product-type/index.yaml` — add `customer-relations-ops` entry with personas, law references, and established date
3. `avatars/AVATAR-RAG-INDEX.yaml` — add RAG routing entries so queries about Azure OpenAI, PostgreSQL, OTEL, and CR complaint drafting route to the correct avatars

---

## Brownfield Safety Constraints

Per `ENG-10.1` and the `brownfield-code-preservation.md` guide, the following constraints apply to all work following this proposal:

1. **No language rewrite by default.** The target repo is Python 3.12. No technology avatar created under this proposal may recommend migration to another language.
2. **No framework swap by default.** `FastAPI`, `SQLAlchemy`, `LangChain`, and `asyncpg` are the operating stack. Avatar guidance must work within these choices.
3. **Preserve PII pipeline.** The PII redaction/restoration pattern in `agents/pii_redact.py` is a compliance boundary. No adoption recommendation may propose removing or restructuring this without explicit team and legal approval.
4. **Preserve audit immutability.** Trace records in PostgreSQL are append-only by design (`BUS-7.1`). No avatar guidance may recommend adding UPDATE/DELETE on these tables.
5. **Migration gate required.** If any future work proposes a stack migration (e.g., moving from `asyncpg` to another async driver), a parity plan with test equivalence evidence is required before approval.

---

## Deliverables

### New Avatars (4 artifacts)

| # | Path | Priority | Phases |
|---|------|----------|--------|
| 1 | `avatars/product-type/customer-relations-ops/` | 🔴 Critical | Phase 1 |
| 2 | `avatars/technology/azure-openai/` | 🟠 High | Phase 2 |
| 3 | `avatars/technology/postgresql-sqlalchemy/` | 🟠 High | Phase 3 |
| 4 | `avatars/technology/opentelemetry-python/` | 🟡 Medium | Phase 4 |

Each avatar must contain at minimum:
- `manifest.yaml` — machine-readable stack config, law specializations, activation rules
- `guidance.md` — domain or stack guidance with law citations
- `ADOPTION.md` (product-type avatars only) — brownfield adoption process
- At least one `examples/` file demonstrating Atomic TDD application

### Registry Updates (3 files)

| File | Change |
|------|--------|
| `avatars/index.yaml` | Add 3 new technology avatar entries |
| `avatars/product-type/index.yaml` | Add `customer-relations-ops` product avatar entry |
| `avatars/AVATAR-RAG-INDEX.yaml` | Add RAG routing for all 4 new avatars |

---

## Exit Criteria

| Criterion | Phase | Verification |
|-----------|-------|-------------|
| ✅ Taxonomy gates passed and documented for all 4 proposed avatars | Gates | This proposal section `Taxonomy Governance Position` |
| ⬜ `customer-relations-ops` avatar created with all required artifacts | Phase 1 | `manifest.yaml` + `guidance.md` + `ADOPTION.md` + 1 persona file + 1 use case |
| ⬜ `azure-openai` avatar created with all required artifacts | Phase 2 | `manifest.yaml` + `guidance.md` + 1 TDD example |
| ⬜ `postgresql-sqlalchemy` avatar created with all required artifacts | Phase 3 | `manifest.yaml` + `guidance.md` + 1 TDD example |
| ⬜ `opentelemetry-python` avatar created with all required artifacts | Phase 4 | `manifest.yaml` + `guidance.md` |
| ⬜ All 3 registry files updated | Phase 5 | `avatars/index.yaml`, `avatars/product-type/index.yaml`, `avatars/AVATAR-RAG-INDEX.yaml` |
| ⬜ Dry-run retrieval against `cr-genai-draft-response` returns correct avatars for Azure OpenAI, PostgreSQL, OTEL, and CR complaint drafting queries | Phase 5 | Manual RAG dry-run prompt |
| ⬜ Brownfield adoption of `cr-genai-draft-response` proceeds with full avatar coverage | Post-approval | Adoption plan references all 4 new avatars |

---

## Approval Required

This proposal requires review and approval before any implementation begins. Per `BUS-7.1`, approval must be recorded in `PROGRESS.md` before Phase 1 starts.

**Minimum sign-offs per `taxonomy-aligned-avatar-enrichment-workflow.md`:**
1. Constitution steward (taxonomy compliance)
2. ORAA domain/product representative (journey validity for `customer-relations-ops`)
3. Engineering representative (brownfield safety for PostgreSQL + OTEL patterns)
