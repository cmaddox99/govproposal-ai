# Customer Relations Operations Product Guidance

Welcome to the American Airlines Customer Relations Operations product avatar. This guide applies the Hangar AI Constitution to AI-assisted complaint response drafting workflows for Customer Relations Representatives (CR Reps).

---

## What We Do

American Airlines Customer Relations Operations provides AI-assisted drafting support for CR Reps handling passenger complaints. A structured complaint record enters the system: the service redacts PII, runs a silent 3-stage compliance agent pipeline (Analysis → Compliance → Drafting), applies template governance, and returns a policy-compliant draft — all without the CR Rep ever touching an LLM directly.

**Key differentiators:**
- **Compliance-first:** Company policy always outranks tone or style preferences (per `BUS-1.1` Priority Hierarchy)
- **PII-safe:** Customer PII is redacted before every LLM call and restored only in deterministic output (per `ENG-6.5` Input Validation)
- **Silent orchestration:** Only the final compliant draft surfaces to the CR Rep — internal reasoning is suppressed
- **Audit immutability:** Every LLM call and compensation decision is traced to an append-only PostgreSQL audit table (per `BUS-7.1` Audit Trail)

---

## Product Laws for Customer Relations Operations

> **Full PRD law definitions** are in [PRD Laws Reference](../../../docs/guides/avatars/prd-laws-reference.md). This section shows domain-specific applications.

### 1. PRD-1.1: Continuous Discovery

**For Customer Relations Operations specifically:**
- Interview CR Reps and supervisors about categories where draft quality is consistently rejected
- Analyze compensation validation failures: which category/subcategory combinations produce incorrect award amounts
- Monitor prohibited-word violations (trademark errors, liability language slippage) per weekly batch analysis
- Study template coverage gaps: complaint categories with no governing template produce the highest edit rates

**Example discovery insight:** CR Reps spend 35% of review time correcting liability language ("we will investigate" → must be removed) in INFLIGHT - FLIGHT ATTENDANTS complaints. Adding an explicit liability phrase scan to the Drafting Agent's final pass would reduce that correction cycle.

---

### 2. PRD-2.1: User Journey Mapping

**For Customer Relations Operations specifically:**
- Map the full CR Rep journey: receive complaint → open tool → review generated draft → approve or edit → submit → case close
- Identify where drafts are rejected most frequently (which categories, which compliance rules fire)
- Track rework loops: how often CR Reps return a draft to the system vs. manually editing in place
- Document handoff points where a CR Supervisor review is required (high-compensation cases, escalation categories)

**Core journey stages:**

```
COMPLAINT DRAFT GENERATION JOURNEY

Complaint Received ──────────────────────────────────────────────
│  Structured record arrives (category, subcategory, flight, customer)
│
PII Redaction ───────────────────────────────────────────────────
│  Customer names, PNR, contact info redacted before LLM boundary
│  Hash chain written to audit trace
│
Template Selection ──────────────────────────────────────────────
│  Category/subcategory → template map lookup
│  Compensation eligibility evaluated
│  Secondary PAX rules applied if applicable
│
Silent Agent Orchestration ──────────────────────────────────────
│  Analysis Agent   → tone, sentiment, topic emphasis (internal only)
│  Compliance Agent → compensation rules, prohibited phrases, liability language
│  Drafting Agent   → final customer-facing message only
│
Compliance Validation ───────────────────────────────────────────
│  Trademark check (add/remove ® per approved word list)
│  Prohibited-words scan
│  Response structure validation (apology count, paragraph order)
│
PII Restoration ─────────────────────────────────────────────────
│  Customer names and data restored from redaction map
│
CR Rep Review ───────────────────────────────────────────────────
│  Displays draft to CR Specialist
│  Rep accepts, edits, or rejects
│
Audit Close ─────────────────────────────────────────────────────
│  LLM call record, compensation decision, and PII hash chain
│  written to append-only traces table in PostgreSQL
```

---

### 3. PRD-3.1: Roadmap Planning

**For Customer Relations Operations specifically:**
- Rank capabilities by compliance risk reduction, not feature richness
- Sequence: Draft quality baseline → Compensation accuracy → PII safety hardening → Audit completeness → Category coverage expansion
- Engineering effort anchor: Compensation validation rules are the highest-risk, highest-value investment — errors here create financial and legal exposure
- Align to CR Ops quarterly review cycles: test coverage improvements before each policy update season

---

### 4. PRD-5.1: Metrics and Success Definition

| Metric | Definition | Target |
|--------|------------|--------|
| **Draft Acceptance Rate** | % of generated drafts accepted with no or minor edits | >80% |
| **Compliance Violation Rate** | % of generated drafts containing a policy violation before validation | 0% delivered |
| **PII in LLM Payload Rate** | % of LLM call payloads where real PII was detected (audit log check) | 0% |
| **Avg Review Time** | Seconds from draft displayed to CR Rep acceptance/submission | <120s |
| **Audit Trace Completeness** | % of LLM calls with a corresponding audit trace record | 100% |
| **Compensation Accuracy Rate** | % of compensation offers validated as within category policy bounds | >99% |

---

## Compliance Rules Governance

> **Per `BUS-1.1` (Priority Hierarchy):** The following ordering is non-negotiable in all agent output decisions.

### Priority Order (Highest to Lowest)

1. Company policies and compensation rules
2. Explicit instructions in the complaint record or user prompt
3. Tone and linguistic guidelines
4. Stylistic preferences

### Prohibited Language Categories

Four categories of language are forbidden in all generated drafts regardless of tone instruction:

| Category | Examples | Law Precedence |
|----------|----------|----------------|
| **Liability language** | "We are responsible for", "This was our fault", "We failed to" | `BUS-1.1` |
| **Promise language** | "We will improve", "Someone will look into this", "We will train our staff" | `BUS-1.1` |
| **Reference to internal systems** | "Our internal team has been notified", "I've opened a ticket" | `BUS-1.1` |
| **Regulatory references** | "Per DOT regulations", "Under federal law" | `BUS-1.1` (unless explicitly instructed) |

### Apology Rules

- Only one apology is permitted per response
- "Sorry" is the approved form (not "apologize")
- Apology must appear in the first paragraph only
- No emotional amplifiers: "disappointing", "discouraging", "regret" are prohibited

---

## PII Safety Pattern

> **Per `ENG-6.5` (Input Validation):** PII must be stripped at the LLM boundary, not after.

### PII Pipeline Stages

1. **Redact before LLM call** — Replace customer names, PNR, phone, email with tokens (e.g., `[CUSTOMER_NAME]`, `[PNR]`)
2. **Redact names for LLM call** — Even within the complaint body, customer names replaced with generic references
3. **Call LLM with clean payload** — No real PII ever crosses the OpenAI API call
4. **Restore PII in final response** — Token map applied to draft output deterministically
5. **Hash and store for audit** — PII fields hashed with `PII_ENCRYPTION_KEY` + `PII_ENCRYPTION_SALT` before PostgreSQL write

### Testing the PII Pipeline

```python
# Per ENG-4.1 (Atomic TDD): PII redaction must be tested independently of LLM calls

def test_pii_redaction_removes_customer_name_before_llm_payload():
    # GIVEN
    complaint = {"customer_name": "John Smith", "comment": "John Smith was unhappy"}
    
    # WHEN
    redacted, token_map = redact_pii_for_llm(complaint)
    
    # THEN
    assert "John Smith" not in redacted["comment"]
    assert "John Smith" not in redacted["customer_name"]
    assert token_map["[CUSTOMER_NAME_0]"] == "John Smith"

def test_pii_restoration_reinserts_names_in_final_response():
    # GIVEN
    draft = "We're sorry, [CUSTOMER_NAME_0], for the experience."
    token_map = {"[CUSTOMER_NAME_0]": "John Smith"}
    
    # WHEN
    restored = restore_pii_in_response(draft, token_map)
    
    # THEN
    assert restored == "We're sorry, John Smith, for the experience."
```

---

## Audit Immutability Pattern

> **Per `BUS-7.1` (Audit Trail):** Audit records must be append-only. No UPDATE or DELETE on trace rows.

### Required Audit Fields

Every LLM interaction must produce an audit record containing:

| Field | Value | Purpose |
|-------|-------|---------|
| `tid` | Transaction ID passed through all calls | End-to-end traceability |
| `complaint_category` | Complaint category code | Compliance scope context |
| `compensation_offered` | Amount and type offered | Financial audit |
| `pii_hash` | SHA-256 hash of redacted fields | PII audit without storing PII |
| `llm_model` | Azure OpenAI deployment name used | Model version traceability |
| `prompt_version` | Hash or tag of system prompt used | Prompt governance |
| `timestamp_utc` | UTC timestamp of call | Audit timeline |
| `outcome` | `accepted` / `edited` / `rejected` | Quality signal |

---

## Brownfield Adoption Notes

> **Per `ENG-10.1` (Brownfield Preservation):** Do not propose structural changes to the PII pipeline, compensation validation, or audit trace patterns without explicit approval and parity evidence.

When working with `cr-genai-draft-response`:
- **DO** add new complaint category templates following the existing `templates/` pattern
- **DO** add new prohibited word/phrase rules to the existing check layer
- **DO** add new audit fields to the trace record — but never remove existing ones
- **DO NOT** restructure the 3-stage silent agent into a visible multi-agent chat pattern
- **DO NOT** move PII redaction to a post-LLM step — that violates `ENG-6.5`
- **DO NOT** add a direct LLM call path that bypasses the compliance validation layer
