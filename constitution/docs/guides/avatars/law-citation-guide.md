# Law Citation Guide

How to cite product laws (PRD-*) and engineering laws (ENG-*) in avatar examples, use cases, and guidance documents.

---

## Citation Principles

**Citation serves two purposes:**
1. **Traceability** - Connect examples back to authoritative laws
2. **RAG Indexing** - Enable fast law-to-example discovery for agents

**Citation Quality Metrics:**
- All citations point to valid law documents (no broken links)
- Citations include law ID and specific section
- Examples demonstrate actual law application (not just mentioning)
- Token overhead: < 50 tokens per example (citations + links)

---

## Citation Formats

### Format 1: Law Reference (Minimal - for inline mentions)

**Usage:** When briefly referencing a law in text

```markdown
Per [PRD-1.1: Continuous Discovery](../../../laws/product/discovery.md#section-1-1), 
research methods include interviews and surveys.
```

**Parts:**
- `PRD-1.1` = Law ID
- `Continuous Discovery` = Law title
- `../../../laws/product/discovery.md` = Absolute path to law document
- `#section-1-1` = Anchor link to specific section

### Format 2: Law Section Header (Medium - for dedicated sections)

**Usage:** When exploring one law in depth

```markdown
## Applying PRD-1.1: Continuous Discovery

**Law Reference:** [PRD-1.1: Continuous Discovery](../../../laws/product/discovery.md)

Key principles from the law:
- Principle 1 from PRD-1.1
- Principle 2 from PRD-1.1
```

**When to use:**
- Dedicating a major section to one law
- Creating examples that demonstrate specific law principles
- Building use cases around multiple laws

### Format 3: Law Mapping (Comprehensive - for structured docs)

**Usage:** When relating multiple laws to structure

```markdown
### Law Specialization Mapping

| Law ID | Title | Example File | Key Application |
|--------|-------|--------------|-----------------|
| PRD-1.1 | Continuous Discovery | examples/PRD-1.1-discovery.md | Understanding customer needs |
| PRD-2.1 | User Journey Mapping | examples/PRD-2.1-journey.md | Mapping touchpoints |
| PRD-3.1 | Roadmap Planning | examples/PRD-3.1-roadmap.md | Feature prioritization |
```

**When to use:**
- Manifest files showing which laws are specialized
- Index files showing law coverage
- Phase descriptions showing law application sequence

---

## Citation Accuracy Requirements

### ✅ Valid Citations

```markdown
✅ [PRD-1.1: Continuous Discovery](../../../laws/product/discovery.md)
   Reason: Law ID matches document, section anchor present

✅ [PRD-2.1 Journey Mapping](../../../laws/product/journey.md#section-2-1)
   Reason: Specific section anchor provided

✅ Per [PRD-5.1](../../../laws/product/metrics.md), metrics include...
   Reason: Inline reference with link to law document
```

### ❌ Invalid Citations

```markdown
❌ [PRD-1.1: Continuous Research](../../../laws/product/discovery.md)
   Problem: Title doesn't match actual law title

❌ See PRD-1.1 for details
   Problem: No link to law document (requires [PRD-1.1](path))

❌ [PRD-1.1](../laws/product/discovery.md)
   Problem: Path is incomplete (should be ../../../laws/)

❌ Per Continuous Discovery law...
   Problem: No ID or link (requires full format)
```

---

## Product Law Citation Checklist

When creating examples, use cases, or guidance documents:

### Discovery Phase (PRD-1.1)

- [ ] Cite PRD-1.1 when describing research methods
- [ ] Link to specific research techniques in law
- [ ] Example shows how discovery findings informed decision
- [ ] Citation format: `[PRD-1.1: Continuous Discovery](path)`

### User Journey Phase (PRD-2.1)

- [ ] Cite PRD-2.1 when mapping workflows
- [ ] Reference specific touchpoint categories from law
- [ ] Example demonstrates journey mapping for your product
- [ ] Citation format: `[PRD-2.1: User Journey Mapping](path)`

### Roadmap Phase (PRD-3.1)

- [ ] Cite PRD-3.1 when describing prioritization
- [ ] Reference ranking criteria from law
- [ ] Example shows roadmap decision based on PRD-3.1
- [ ] Citation format: `[PRD-3.1: Roadmap Planning](path)`

### MVP Phase (PRD-4.1)

- [ ] Cite PRD-4.1 when defining MVP
- [ ] Reference MVP definition criteria from law
- [ ] Example shows MVP validation process
- [ ] Citation format: `[PRD-4.1: MVP & Product-Market Fit](path)`

### Metrics Phase (PRD-5.1)

- [ ] Cite PRD-5.1 when defining KPIs
- [ ] Reference metric categories from law
- [ ] Example shows how metrics were chosen
- [ ] Citation format: `[PRD-5.1: Metrics & Success Definition](path)`

---

## Engineering Law Citations (in use cases)

When use cases cross into engineering implementation:

### Development Phase (ENG-6.1 TDD, ENG-7.1 Vertical Slice)

- [ ] Cite ENG-6.1 when describing test-driven development
- [ ] Cite ENG-7.1 when describing vertical slice implementation
- [ ] Format: `[ENG-6.1: Atomic TDD](../../../laws/engineering/security.md)`

### Code Quality Phase (ENG-4.1, ENG-4.2)

- [ ] Cite relevant engineering laws per phase
- [ ] Link to specific practices from laws
- [ ] Format: `[ENG-N.N: Title](../../../laws/engineering/{topic}.md)`

---

## Citation Validation

### Manual Checks

Before publishing:

1. **Link Works:** Click every citation link - does it reach the law document?
2. **ID Matches:** Does the ID in the text (PRD-1.1) match the actual law?
3. **Title Accurate:** Is the law title exactly as it appears in the law document?
4. **Section Reference:** If citing specific section, does anchor exist in law?

### Automated Checks

```bash
# Validate all citations in a directory
python3 scripts/validate-citations.py avatars/product-type/*/examples/

# Output example:
# ✓ PRD-1.1: Continuous Discovery - valid
# ✓ PRD-2.1: User Journey Mapping - valid
# ✗ PRD-X.X: Typo Title - ERROR: Law not found
# Total: 15 valid, 1 broken
```

---

## Common Citation Patterns

### Pattern 1: Opening Citation

**Used in:** First paragraph of any law-focused section

```markdown
## Applying PRD-1.1: Continuous Discovery

[PRD-1.1: Continuous Discovery](../../../laws/product/discovery.md) 
is the foundation of {{ product }} development. 
When {{ condition }}, follow this law to {{ outcome }}.
```

### Pattern 2: Practice Citation

**Used in:** Describing specific practice from law

```markdown
**Research Method (from PRD-1.1):**

Per [PRD-1.1: Continuous Discovery](../../../laws/product/discovery.md#practices), 
conduct interviews with {{ personas }} using {{ method }}.
```

### Pattern 3: Decision Citation

**Used in:** Explaining why a decision follows law

```markdown
**Why we chose Option A:**

[PRD-3.1: Roadmap Planning](../../../laws/product/roadmap.md#prioritization) 
recommends prioritizing by {{ criteria }}. 
Our choice of Option A scores highest on {{ criteria }}.
```

### Pattern 4: Result Citation

**Used in:** Connecting results to law application

```markdown
**Outcome:**

Following [PRD-2.1: User Journey Mapping](../../../laws/product/journey.md), 
we identified {{ finding }}, which led to {{ decision }}.

Result: {{ metric }} improved {{ amount }}.
```

---

## Token Optimization for Citations

**Target:** Overhead < 50 tokens per citation-heavy example (< 8% of 800 token budget)

### Optimization Strategy

```markdown
❌ Verbose (costs 80+ tokens):
[PRD-1.1: Continuous Discovery](../../../laws/product/discovery.md#section-1-1) 
describes research methods in detail, including interviews, surveys, 
and competitive analysis. When applying this law to cargo bookings...

✅ Concise (costs 35 tokens):
Per [PRD-1.1: Continuous Discovery](../../../laws/product/discovery.md), 
research methods guide our discovery. When applying to cargo bookings...
```

---

## Citation Review Checklist

Before submitting example files:

- [ ] All citations use format: `[ID: Title](path)`
- [ ] All paths verified correct (../../../laws/)
- [ ] All law IDs match actual laws (no typos)
- [ ] All law titles match exactly
- [ ] At least one citation per law referenced in text
- [ ] Citations are in opening and decision sections
- [ ] Citation overhead < 50 tokens
- [ ] Zero broken links (test with `validate-citations.py`)
- [ ] Product-focused (not generic law description)
- [ ] Example demonstrates law application (not just mentions)

---

## References

- [Product Laws Index](../../../laws/product/_domain.yaml)
- [Engineering Laws Index](../../../laws/engineering/_domain.yaml)
- [Example: Cargo Discovery](../../../avatars/product-type/cargo-freight/examples/PRD-1.1-discovery.md)

---

**Last Updated:** February 20, 2026  
**Maintained By:** Hangar AI Constitution Team  
**Related:** PRODUCT-AVATAR-GUIDE.md
