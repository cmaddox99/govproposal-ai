# PRD-5.1 — Metrics & Success Definition: Customer Relations Operations

**Law:** PRD-5.1 Metrics & Success Definition  
**Avatar:** customer-relations-ops  
**Pattern:** Operational KPIs for AI-assisted complaint response system

---

## North Star Metrics

| Metric | Definition | Target | Current |
|--------|-----------|--------|---------|
| Draft Acceptance Rate | % of AI drafts accepted without major edit by CR Rep | >80% | 74% |
| Compliance Violation Rate | % of delivered drafts containing policy violations | 0% | 0% |
| PII-in-LLM Rate | % of LLM calls containing unredacted PII | 0% | 0% |
| Avg Review Time | Seconds from draft display to CR Rep accept/submit | <120s | 145s |
| Audit Trace Completeness | % of LLM calls with complete audit trace entry | 100% | 100% |

## Category-Level Metrics

| Complaint Category | Acceptance Rate | Avg Edit Rate | DOT Compliance |
|-------------------|----------------|---------------|----------------|
| Flight Disruption | 82% | 18% | 100% |
| Baggage | 79% | 21% | 100% |
| Disability/ADA | 71% | 29% | 100% |
| Customer Service | 85% | 15% | 100% |

## Success Thresholds (Launch Gates)

- **Red (block release)**: Compliance violation > 0%, PII-in-LLM > 0%
- **Yellow (review required)**: Acceptance rate < 75%, avg review > 180s
- **Green (proceed)**: Acceptance rate ≥ 80%, avg review ≤ 120s, all compliance gates pass

## Metric Collection

Metrics logged in append-only audit trace per case. Aggregated daily in operations dashboard. DOT response clock tracked separately per written complaint.
