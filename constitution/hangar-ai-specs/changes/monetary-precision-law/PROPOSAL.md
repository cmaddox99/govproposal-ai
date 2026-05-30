# Proposal: Monetary Precision Law (BUS-3.6)

**Status:** PROPOSED
**Spec ID:** `monetary-precision-law`
**Triggered by:** Constitutional gap surfaced during mobile-workshop authoring — 2026-04-14
**Scope:** `laws/business/data-governance.md` (new law), `laws/business/_domain.yaml` (registry), `avatars/**` (universal example coverage), `avatars/product-type/index.yaml:597` (reference bug fix)
**Laws:** ENG-10.1 (Amendment Process), ENG-11.1 (Hangar SDD, NON-NEGOTIABLE), BUS-3.4 (Data Quality — sibling), ENG-6.7 (Audit Trail), BUS-7.1 (Audit & Evidence)

---

## Problem

### 1. The constitution has no law governing monetary precision

A grep of `laws/**/*.md` for the concepts that define financial representation — `precision`, `monetary`, `decimal`, `BigDecimal`, `HALF_EVEN`, `rounding`, `floating-point`, `currency` — returns zero matches in any law file. The constitution is silent on whether `double` / `float` / IEEE 754 types are acceptable for money or loyalty currency.

The closest law today is `BUS-3.4 Data Quality Law`, which names "Accuracy (Data reflects reality; measure: Error rate)" as one of five quality dimensions. This is a correct but abstract framing: `BUS-3.4` does not prescribe types, rounding modes, or cross-system representation rules. An engineer reading `BUS-3.4` in isolation cannot tell whether `double miles` is compliant.

### 2. The gap produces downstream hallucinations

Workshop materials (`hangar-ai-constitution-workflows` — the sibling repository that teaches the constitution) currently cite `ENG-1.2` as "Monetary Precision Law" across ~35 files, including AGENTS.md files, sample-codebase source annotations, instructor runbook, and exercise guides. The real `ENG-1.2` is the AI-Engineer Pairing Law.

This is not an authoring defect in the workshop — it is a predictable outcome of citing a concept that is not defined anywhere in the upstream constitution. Downstream authors reach for the most plausible-sounding ID and a hallucination fills the gap. This will recur in every future project that needs to talk about monetary precision until the constitution defines a real law.

### 3. The avatar system perpetuates the gap

The `avatar-product-loyalty` avatar at `avatars/product-type/loyalty-aadvantage/` has a `specializes_laws` section (Phase 8 Compliance Enrichment) with entries for `BUS-2.2`, `BUS-4.1`, `BUS-4.3`, `ENG-6.4`. It has no entry for any monetary-precision concern, despite the avatar domain being AAdvantage — a loyalty program with 180M+ members where miles-balance accuracy is a material business concern.

Similarly, the technology avatars (`dotnet-core`, `python-fastapi`, etc.) include `Money(decimal)` in their examples for *other* laws (ENG-2.1 Aggregates, ENG-3.2 Immutability, ENG-3.3 Demeter) but treat the decimal choice as an incidental detail, never as the primary teaching point. There is no avatar example anywhere that says "this is the monetary-precision law; here is the violation; here is the remediation."

### 4. Related reference bug

`avatars/product-type/index.yaml:597` currently reads:

```
- Loyalty addresses financial accuracy (BUS-4.x)
```

`BUS-4.x` is the Privacy Laws family (GDPR, CCPA, Consent, Data Subject Rights, Cross-Border Transfer). It does not address financial accuracy. This reference is factually wrong and will remain wrong until a real monetary-precision law exists to point at.

---

## Solution

Add `BUS-3.6 Monetary Precision Law` as a new **non-negotiable** law in the Business domain, sibling to `BUS-3.4 Data Quality`. Mandate that every product-type and technology avatar carry an example file demonstrating the law in its domain. Fix the `index.yaml:597` reference as part of the same amendment.

### Draft law text (to be added as Section 3.6 of `laws/business/data-governance.md`)

---

**Section 3.6: Monetary Precision Law**
**Law ID:** `BUS-3.6` (NON-NEGOTIABLE)

Monetary and loyalty-currency quantities SHALL be represented and computed with platform-native arbitrary-precision decimal types. Binary floating-point types SHALL NOT be used for these quantities.

#### Scope

Applies to any quantity that:
- Represents money (fares, refunds, taxes, fees, commissions, partner settlements, revenue shares)
- Represents loyalty currency (miles, points, status credits, EQDs/EQMs, elite progress)
- Enters any aggregation, projection, comparison, or financial disclosure — internal or external

#### Mandatory Representation

| Platform | Type | Rounding Mode |
|---|---|---|
| Java / Kotlin (JVM) | `BigDecimal` | `HALF_EVEN` (banker's rounding) |
| Swift | `Decimal` | `.plain` with explicit scale |
| C# / .NET | `decimal` | `MidpointRounding.ToEven` |
| Python | `decimal.Decimal` | `ROUND_HALF_EVEN` |
| Go | `shopspring/decimal` or equivalent | half-even |
| TypeScript / JavaScript | `decimal.js` or equivalent | half-even |
| SQL columns | `NUMERIC(p, s)` / `DECIMAL(p, s)` | DBMS-configured |

#### Prohibited Patterns

- `double`, `float`, `Double`, `Float`, JavaScript `Number`, and IEEE 754 types of any width — for any monetary or loyalty-currency quantity.
- Cents-as-integer scaling (`amount * 100`) as a substitute for native decimal types. This pattern violates the Validity dimension of BUS-3.4 (silent overflow at large values; ambiguous scale at boundaries).
- Parsing monetary values directly from JSON numbers into native floating-point types. Cross-system monetary values SHALL be exchanged as JSON strings (`"125000.01"` not `125000.01`) and converted to the stack's decimal type at the system boundary.

#### Cross-System Consistency (companion to BUS-3.4 Data Quality)

Monetary values SHALL round-trip across system boundaries without precision loss. All serialization formats that permit strings SHALL use string representation for monetary values.

#### Audit Requirement (companion to ENG-6.7 Audit Trail, BUS-7.1 Audit & Evidence)

Any operation that modifies a monetary or loyalty-currency balance SHALL record, at minimum: pre-value, post-value, operator identity, operator authority, and timestamp — at the precision the stored type supports.

#### Migration Clause

Existing systems that represent monetary quantities as floating-point SHALL produce a migration plan within one release cycle. The plan SHALL identify every boundary where floating-point drift can occur, name the replacement decimal type, and define the backfill / correction procedure for already-propagated drift. Phased migration is acceptable; indefinite deferral is not.

#### Rationale

- Binary floating-point cannot exactly represent most decimal fractions (0.1 is an infinite repeating fraction in binary). Compound arithmetic accumulates drift.
- At scale (e.g., AAdvantage: 180M+ members, billions of annual accrual events), drift produces visibly wrong member-facing balances → trust erosion, customer-support cost, legal exposure for mis-stated loyalty obligations.
- Financial statements subject to SOX depend on exact ledger arithmetic. Double-precision violations introduce audit risk.
- Retroactive correction of propagated drift requires full ledger replay, which is prohibitively expensive. "Fix it later" is not an option.

#### Non-Negotiable Rationale

The error mode is invisible at small scale (unit tests pass) and catastrophic at production scale. A constitution that does not forbid this pattern at first-line level is one that will be retro-fitted at high cost. This law SHALL be enforced from first commit.

---

### Avatar coverage mandate

Every avatar in `avatars/product-type/` and `avatars/technology/` SHALL include an example file demonstrating `BUS-3.6` in that avatar's domain or technology stack:

- **Product avatars** demonstrate the business consequence (e.g., loyalty: miles drift → trust erosion; cargo: tariff drift → revenue misstatement; check-in: fee calculation drift → passenger disputes).
- **Technology avatars** demonstrate the correct type selection and rounding mode in the avatar's stack, plus one "bad" counter-example showing the prohibited pattern.

Example file naming: `BUS-3.6-monetary-precision.md` under each avatar's `examples/` directory.

For avatars where monetary quantities have no plausible domain presence (e.g., `vector-databases`, `streaming-ml` when used for non-financial telemetry), the example file SHALL explicitly state this and describe what a monetary concern WOULD look like if introduced (e.g., "if this ML pipeline were re-scoped to price-prediction, it would process monetary values; the type choice below would apply").

### Avatar enrichment mechanism

The `avatar-workflow` (at `workflows/avatar-workflow.md`) already defines an `enrich` mode for codebase-grounded avatar updates. That mode SHALL be used to add BUS-3.6 examples to avatars where a real reference codebase exists (notably `loyalty-aadvantage`, where the workshop's `loyalty-accrual` Java code and `loyalty-mobile` Swift/Kotlin code are the ground-truth patterns). For avatars without a reference codebase, `assess-correct` mode applies.

### Related index.yaml fix

`avatars/product-type/index.yaml:597` SHALL change from:
```
- Loyalty addresses financial accuracy (BUS-4.x)
```
to:
```
- Loyalty addresses financial accuracy (BUS-3.6)
```

---

## Decisions Requiring Review

Four design choices in this proposal are decisions, not facts. Each is stated below with the recommended answer and the reasoning; any of them can be changed without invalidating the rest of the amendment.

### D1 — Law ID placement

**Recommended:** `BUS-3.6`, sibling to `BUS-3.4 Data Quality`.

Alternatives considered:
- `BUS-2.7` under Compliance Framework (alongside FAA / TSA / DOT / PCI-DSS / SOX). SOX and PCI-DSS both depend on accurate ledgers, so this is defensible. Rejected because the `BUS-2.x` family is about *external regulatory frameworks*, and monetary precision is an *internal representation rule* that supports those frameworks.
- A new `BUS-8 Financial Controls` article. Clean namespace for future financial-domain laws (currency handling, FX, interest) but premature if this is the only law in the family today.

### D2 — Loyalty-currency scope

**Recommended:** Include loyalty currency (miles, points, EQDs) in the same prohibition as money.

Miles are not "money" in a strict accounting sense (different liability model, non-transferable, redemption-constrained), but their arithmetic properties are identical: compound precision errors at scale produce member-facing incorrect balances. Scoping the law to "money only" would leave the workshop's signature teaching moment (miles as `Double` → drift) outside the law's reach, which would perpetuate the same representation gap this amendment is meant to close.

Alternative: separate clause that explicitly inherits the rules from monetary scope. Equivalent substance, more prose.

### D3 — Avatar coverage: strict or pragmatic?

**Recommended:** Strict — every avatar, including those where monetary quantities are not currently in scope.

Alternatives considered:
- Pragmatic (only avatars with a financial surface). Rejected because non-negotiable laws in the Hangar model carry universal avatar coverage; skipping non-financial avatars creates an expectation that the law is "optional for some domains," which contradicts the non-negotiable status.
- Pragmatic with a "placeholder" requirement (every avatar acknowledges the law, but only financial-surface avatars must have a concrete example). Equivalent to strict, with slightly weaker non-financial examples. Included as a fallback if strict compliance cost is too high.

### D4 — Enforcement posture for existing code

**Recommended:** Firm on new code; migration-plan-required on legacy.

Alternatives considered:
- Firm on both (immediate forced migration). Rejected: unrealistic for existing ledger systems with large amounts of historical floating-point data.
- Permissive on both (recommendation, not requirement). Rejected: violates the non-negotiable stance.

The recommended posture is consistent with how other non-negotiable laws treat legacy (ENG-6.4 Data Protection, ENG-6.1 Security by Design — both require remediation plans, not instant migration).

---

## Deliverables

| # | Deliverable | Action | Governing Rule |
|---|---|---|---|
| 1 | `laws/business/data-governance.md` — Section 3.6 added | Append law text as drafted above | ENG-10.1 Amendment Process |
| 2 | `laws/business/_domain.yaml` — register BUS-3.6 in Article III; mark `non_negotiable: [BUS-3.6]` | Edit registry | ENG-10.1 |
| 3 | `avatars/product-type/index.yaml` — line 597 `BUS-4.x` → `BUS-3.6` | Edit reference | ENG-10.1 |
| 4 | `avatars/templates/BUS-3.6-monetary-precision.md` (new) | Canonical example template avatar authors adapt | ENG-11.2 Proposal Completeness |
| 5 | `avatars/product-type/loyalty-aadvantage/examples/BUS-3.6-monetary-precision.md` (new) | Domain example using `loyalty-accrual` (Java, BigDecimal) and `loyalty-mobile` (Swift Decimal / Kotlin BigDecimal) as ground truth | Avatar Workflow `enrich` mode |
| 6 | `avatars/product-type/loyalty-aadvantage/manifest.yaml` — add BUS-3.6 to `specializes_laws` Phase 8 Compliance Enrichment | Edit manifest | Avatar Workflow `assess-correct` |
| 7 | For each other `avatars/product-type/*` avatar: add `examples/BUS-3.6-monetary-precision.md` and update manifest | Coverage rollout | Avatar Workflow |
| 8 | For each `avatars/technology/*` avatar: add `examples/BUS-3.6-monetary-precision.md` and update manifest | Coverage rollout | Avatar Workflow |
| 9 | `docs/articles/what-is-the-hangar-ai-constitution.md` — list BUS-3.6 in the non-negotiables table | Edit if the table exists | ENG-11.3 Spec Freshness |
| 10 | RAG index refresh — ensure BUS-3.6 example files are retrievable | Run RAG eval | Avatar Workflow |

---

## Success Criteria

- BUS-3.6 text exists in `laws/business/data-governance.md` as Section 3.6.
- BUS-3.6 is registered in `_domain.yaml` with non-negotiable flag.
- `avatars/product-type/index.yaml:597` correctly references BUS-3.6.
- Every avatar under `avatars/product-type/` and `avatars/technology/` has a `BUS-3.6-monetary-precision.md` example file (strict coverage).
- The canonical template at `avatars/templates/BUS-3.6-monetary-precision.md` is available for reference.
- RAG evaluation for monetary-precision queries meets the `AVATAR-RAG-INDEX.yaml` thresholds (≥95% recall, ≥90% precision).
- Grep for `ENG-1.2.*Monetary|Monetary.*ENG-1.2` across the constitution returns 0 matches.

---

## Out of Scope

- Remediation of downstream consumers (notably the `hangar-ai-constitution-workflows` workshop repo). That is a separate downstream proposal that consumes this one.
- Constitution-lint tooling changes to enforce BUS-3.6 at scan time. A useful future proposal; not required for the law to stand.
- Changes to any other `BUS-3.x` law. BUS-3.4 Data Quality remains unchanged; BUS-3.6 is additive.
- Retroactive rewrite of existing avatar examples that happen to use decimal types for *other* laws (e.g., the dotnet-core `Money(decimal)` example for ENG-3.2 Immutability). Those remain valid examples of their respective laws.

---

## Migration Impact

**Upstream (this repo, the constitution):** the amendment adds one law, fixes one reference, and mandates new example files across ~20 avatars. No existing law text changes.

**Downstream (consumers of the constitution):** projects that currently cite `ENG-1.2` for monetary precision (workshop materials, sample codebases referencing the workshop) can migrate to `BUS-3.6` once this amendment ratifies. Until ratification, those projects should cite `BUS-3.4 Data Quality (Accuracy dimension)` as the closest existing law.

**Ratification risk:** none of the existing avatars break. New example files are additive. The `index.yaml:597` change is a bug fix with no dependency.

---

## References

- `laws/business/data-governance.md` — current BUS-3.x laws
- `laws/business/_domain.yaml` — BUS domain registry
- `avatars/product-type/index.yaml` — avatar index (line 597 reference bug)
- `avatars/product-type/loyalty-aadvantage/` — example reference avatar
- `workflows/avatar-workflow.md` — avatar lifecycle workflow (`enrich`, `assess-correct` modes)
- `AVATAR-RAG-INDEX.yaml` — RAG retrieval thresholds
- `ENG-10.1 Amendment Process Law` — the process this proposal follows
- `ENG-11.1 Hangar SDD Law (NON-NEGOTIABLE)` — the spec-driven development requirement this proposal satisfies

---

## Implementation Order (recommended)

1. Fix `avatars/product-type/index.yaml:597` — one-line bug fix, independent.
2. Add BUS-3.6 to `laws/business/data-governance.md` and `_domain.yaml`.
3. Create `avatars/templates/BUS-3.6-monetary-precision.md` as the canonical reference.
4. Enrich `avatars/product-type/loyalty-aadvantage/` (has real codebase ground truth).
5. Roll out remaining product-type avatars (synthetic examples where needed).
6. Roll out technology avatars (one example per stack).
7. RAG index refresh + eval.
8. Update any `docs/` artifacts that list non-negotiables.

Items 1–2 are the minimum viable amendment. Items 3–8 complete the coverage mandate.
