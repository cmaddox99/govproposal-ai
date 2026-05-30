---
domain: business
article: III
title: Data Governance Laws
laws:
  - id: BUS-3.1
    title: Data Classification Law
    non_negotiable: true
    summary: All data MUST be classified (Public, Internal, Confidential, Restricted)
  - id: BUS-3.2
    title: Data Inventory Law
    summary: All data assets MUST be inventoried with owner, location, and retention
  - id: BUS-3.3
    title: Data Retention Law
    summary: Data SHALL be retained only as long as necessary with automated deletion
  - id: BUS-3.4
    title: Data Quality Law
    summary: Data SHALL meet quality standards (accuracy, completeness, timeliness, consistency, validity)
  - id: BUS-3.5
    title: Cross-Border Data Transfer Law
    summary: International data transfers MUST be legally authorized
  - id: BUS-3.6
    title: Monetary Precision Law
    non_negotiable: true
    summary: Monetary and loyalty-currency quantities SHALL use platform-native arbitrary-precision decimal types; binary floating-point types are prohibited
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article III: Data Governance Laws

## Section 3.1: Data Classification Law

**Law ID:** `BUS-3.1`

All data MUST be classified.

| Classification | Definition | Examples | Handling |
|----------------|------------|----------|----------|
| **Public** | No harm if disclosed | Marketing materials | Standard |
| **Internal** | Internal use only | Internal docs, roadmaps | Access control |
| **Confidential** | Business sensitive | Customer lists, financials | Encrypted + ACL |
| **Restricted** | Highest sensitivity | PII, PHI, credentials | Encrypted + audit + MFA |

### Classification Process

1. Data owner identifies classification at creation
2. Classification marked in metadata
3. Appropriate controls applied automatically
4. Reclassification requires owner approval

---

## Section 3.2: Data Inventory Law

**Law ID:** `BUS-3.2`

All data assets MUST be inventoried.

### Data Inventory Template

```markdown
## Data Asset: [Name]

**Classification:** [Public/Internal/Confidential/Restricted]
**Owner:** [Department/Person]
**Location:** [Systems where stored]
**Retention:** [How long kept]
**Legal Basis:** [Why we can keep it]

**Contains:**
- [ ] Personal Data (PII)
- [ ] Sensitive Personal Data
- [ ] Health Information (PHI)
- [ ] Financial Data
- [ ] Children's Data

**Processing Activities:**
- [What we do with this data]

**Sharing:**
- [Who has access, including third parties]
```

---

## Section 3.3: Data Retention Law

**Law ID:** `BUS-3.3`

Data SHALL be retained only as long as necessary.

### Retention Principles

- Define retention period for each data type
- Automate deletion where possible
- Document legal holds that extend retention
- Verify deletion actually occurred

### Retention Schedule Template

| Data Type | Retention Period | Basis | Deletion Method |
|-----------|------------------|-------|-----------------|
| User accounts | Account life + 30 days | Legitimate interest | Automated |
| Transaction logs | 7 years | Legal requirement | Manual review |
| Support tickets | 3 years | Customer service | Automated |
| Marketing consent | Until withdrawn | Consent | On request |

---

## Section 3.4: Data Quality Law

**Law ID:** `BUS-3.4`

Data SHALL meet quality standards.

### Quality Dimensions

| Dimension | Definition | Measure |
|-----------|------------|---------|
| **Accuracy** | Data reflects reality | Error rate |
| **Completeness** | All required data present | Fill rate |
| **Timeliness** | Data is current | Age of data |
| **Consistency** | Same data across systems | Reconciliation |
| **Validity** | Data conforms to rules | Validation pass rate |

---

## Section 3.5: Cross-Border Data Transfer Law

**Law ID:** `BUS-3.5`

International data transfers MUST be legally authorized.

### Transfer Mechanisms

| Mechanism | Use Case | Requirements |
|-----------|----------|--------------|
| Adequacy Decision | EU to adequate countries | None additional |
| Standard Contractual Clauses | EU to non-adequate | Sign SCCs |
| Binding Corporate Rules | Intra-group transfers | Approval required |
| Explicit Consent | Specific transfers | Documented consent |

---

## Section 3.6: Monetary Precision Law

**Law ID:** `BUS-3.6` | **Status:** NON-NEGOTIABLE

Monetary and loyalty-currency quantities SHALL be represented and computed with platform-native arbitrary-precision decimal types. Binary floating-point types SHALL NOT be used for these quantities.

### Scope

Applies to any quantity that:
- Represents money (fares, refunds, taxes, fees, commissions, partner settlements, revenue shares)
- Represents loyalty currency (miles, points, status credits, EQDs/EQMs, elite progress)
- Enters any aggregation, projection, comparison, or financial disclosure — internal or external

### Mandatory Representation

| Platform | Type | Rounding Mode |
|---|---|---|
| Java / Kotlin (JVM) | `BigDecimal` | `HALF_EVEN` (banker's rounding) |
| Swift | `Decimal` | `.plain` with explicit scale |
| C# / .NET | `decimal` | `MidpointRounding.ToEven` |
| Python | `decimal.Decimal` | `ROUND_HALF_EVEN` |
| Go | `shopspring/decimal` or equivalent | half-even |
| TypeScript / JavaScript | `decimal.js` or equivalent | half-even |
| SQL columns | `NUMERIC(p, s)` / `DECIMAL(p, s)` | DBMS-configured |

### Prohibited Patterns

- `double`, `float`, `Double`, `Float`, JavaScript `Number`, and IEEE 754 types of any width — for any monetary or loyalty-currency quantity.
- Cents-as-integer scaling (`amount * 100`) as a substitute for native decimal types. This pattern violates the Validity dimension of BUS-3.4 (silent overflow at large values; ambiguous scale at boundaries).
- Parsing monetary values directly from JSON numbers into native floating-point types. Cross-system monetary values SHALL be exchanged as JSON strings (`"125000.01"` not `125000.01`) and converted to the stack's decimal type at the system boundary.

### Cross-System Consistency (companion to BUS-3.4 Data Quality)

Monetary values SHALL round-trip across system boundaries without precision loss. All serialization formats that permit strings SHALL use string representation for monetary values.

### Audit Requirement (companion to ENG-6.7 Audit Trail, BUS-7.1 Audit & Evidence)

Any operation that modifies a monetary or loyalty-currency balance SHALL record, at minimum: pre-value, post-value, operator identity, operator authority, and timestamp — at the precision the stored type supports.

### Migration Clause

Existing systems that represent monetary quantities as floating-point SHALL produce a migration plan within one release cycle. The plan SHALL identify every boundary where floating-point drift can occur, name the replacement decimal type, and define the backfill / correction procedure for already-propagated drift. Phased migration is acceptable; indefinite deferral is not.

### Rationale

- Binary floating-point cannot exactly represent most decimal fractions (0.1 is an infinite repeating fraction in binary). Compound arithmetic accumulates drift.
- At scale (e.g., AAdvantage: 180M+ members, billions of annual accrual events), drift produces visibly wrong member-facing balances — trust erosion, customer-support cost, legal exposure for mis-stated loyalty obligations.
- Financial statements subject to SOX depend on exact ledger arithmetic. Double-precision violations introduce audit risk.
- Retroactive correction of propagated drift requires full ledger replay, which is prohibitively expensive. "Fix it later" is not an option.

### Non-Negotiable Rationale

This law is NON-NEGOTIABLE because:
1. Precision errors in monetary computation are **silent** — they do not throw exceptions
2. Errors **compound** — each operation adds drift
3. Errors are **irreversible at scale** — ledger replay is the only correction
4. Financial accuracy is a **regulatory obligation** (SOX, DOT consumer protection)
