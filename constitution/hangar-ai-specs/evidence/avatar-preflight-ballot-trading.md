# Avatar Pre-flight Evidence — Ballot Trading
Date: 2026-04-27 | Mode: Generate | Workflow: avatar-workflow

## Confirmed Type
`product` — "Ballot Trading" is an AA product domain governing pilot trip-pairing trades.

## Deduplication Result
- Tier 1 (Exact): No `avatars/product-type/ballot-trading/` exists — PROCEED
- Tier 2 (Semantic): Nearest neighbor is `crew-training-scheduling` (FAA/DO-178C training compliance). Overlap score: <30% — distinct journeys, distinct law focus. PROCEED.

## Law Boundary Acknowledged
`type: product` — PRD-* and BUS-* laws permitted. ENG-1.x–ENG-5.x and ENG-7.x–ENG-12.x are FORBIDDEN. ENG-6.x conditionally permitted. User acknowledged: YES.

## 5 Agreed RAG Query Patterns
| # | Query | Expected File |
|---|---|---|
| Q1 | "How do we discover pilot trip trading pain points?" | `examples/PRD-1.1-discovery.md` |
| Q2 | "What is the core journey for a pilot submitting a ballot trade?" | `examples/PRD-2.1-journey.md` |
| Q3 | "What are the success metrics for ballot trading?" | `examples/PRD-5.1-metrics.md` |
| Q4 | "What are the non-negotiable rules for ballot trading?" | `guidance.md` |
| Q5 | "Walk me through a real-time pilot trip trade workflow" | `use-cases/pilot-trip-trade/README.md` |

## Taxonomy Category
"Crew Self-Service & Trip Trading" — not in existing product-type taxonomy.
Taxonomy extension proposal filed at: `hangar-ai-specs/changes/taxonomy-extension-ballot-trading/PROPOSAL.md`
Avatar will not be committed to `index.yaml` until taxonomy extension is approved or mapped to existing category.
