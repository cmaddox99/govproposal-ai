---
domain: product
article: IV
title: Roadmap Laws
laws:
  - id: PRD-4.1
    title: Outcome-Based Roadmap Law
    summary: Roadmaps SHALL communicate outcomes, not features
  - id: PRD-4.2
    title: Now/Next/Later Framework Law
    summary: Roadmaps SHALL use time horizons, not fixed dates
  - id: PRD-4.3
    title: Dependency Management Law
    summary: Dependencies MUST be identified and managed with clear ownership
  - id: PRD-4.4
    title: Roadmap Communication Law
    summary: Roadmaps SHALL be communicated appropriately to each audience
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article IV: Roadmap Laws

## Section 4.1: Outcome-Based Roadmap Law

**Law ID:** `PRD-4.1`

Roadmaps SHALL communicate outcomes, not features.

### Example

```
❌ WRONG (Feature roadmap)
Q1: Build dashboard
Q2: Add reporting
Q3: Mobile app

✅ CORRECT (Outcome roadmap)
Q1: Users can identify issues in <30 seconds (via dashboard)
Q2: Teams can demonstrate ROI to leadership (via reporting)
Q3: Field workers can act on alerts immediately (via mobile)
```

---

## Section 4.2: Now/Next/Later Framework Law

**Law ID:** `PRD-4.2`

Roadmaps SHALL use time horizons, not fixed dates.

| Horizon | Timeframe | Certainty | Detail Level |
|---------|-----------|-----------|--------------|
| **Now** | 0-4 weeks | High (80%+) | Detailed stories, assigned |
| **Next** | 1-3 months | Medium (50%) | Themes, rough scope |
| **Later** | 3-12 months | Low (20%) | Strategic bets, outcomes |

### Rules

- NOW items have clear acceptance criteria
- NEXT items have problem statements
- LATER items have hypotheses to validate

---

## Section 4.3: Dependency Management Law

**Law ID:** `PRD-4.3`

Dependencies MUST be identified and managed.

### Dependency Types

| Type | Example | Management |
|------|---------|------------|
| **Technical** | API not ready | Sequence work, use mocks |
| **Team** | Design needed first | Cross-team planning |
| **External** | Third-party integration | Early engagement, fallback plan |
| **Data** | Analytics not in place | Instrument early |

### Dependency Documentation

```
Feature: [Name]
Depends on:
- [ ] [Dependency 1] - Owner: [Team] - Status: [In progress]
- [ ] [Dependency 2] - Owner: [Team] - Status: [Blocked]

Blockers:
- [Blocker description] - Escalated to: [Name] - ETA: [Date]
```

---

## Section 4.4: Roadmap Communication Law

**Law ID:** `PRD-4.4`

Roadmaps SHALL be communicated appropriately to each audience.

| Audience | Focus | Update Frequency |
|----------|-------|------------------|
| **Executives** | Strategic outcomes, OKR alignment | Quarterly |
| **Stakeholders** | Themes, timing, dependencies | Monthly |
| **Engineering** | Detailed scope, technical approach | Sprint |
| **Customers** | Value delivery, timing ranges | As committed |

### External Communication Rules

- No specific dates (use quarters or "coming soon")
- Outcomes, not features
- Always include "subject to change" caveat
- Never promise what isn't validated
