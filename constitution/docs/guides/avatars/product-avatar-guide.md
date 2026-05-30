# Product Avatar Guide

Best practices for creating rich, law-aligned product avatars that empower agents to cite and apply product laws.

---

## What is a Product Avatar?

A **product avatar** is a comprehensive guide to applying the Hangar AI Constitution within a specific product domain (Cargo, Loyalty, Check-In, etc.).

**Structure:**
- **manifest.yaml** - Configuration, law specializations, skill activation
- **personas.md** - User types and their journeys
- **guidance.md** - How to apply the constitution to this product
- **examples/** - Concrete demonstrations of each law (PRD-1.1 through PRD-5.1)
- **use-cases/** - End-to-end workflows combining multiple laws

**Key Difference from Technology Avatars:**
- Product avatars specialize in **product laws (PRD-*)** not technology choices
- Focus is on **user/customer value** not technical architecture
- Examples span **discovery through measurement** not just implementation

---

## Step 1: Before You Start

### Gather Information

You'll need to know:

**About the Product:**
- [ ] Official product name (used in {{ Product Display Name }})
- [ ] 2-3 sentence product description (what it does, why it matters)
- [ ] Primary business domain/category (e.g., "Cargo Booking & Operations")
- [ ] List of 4-5 core user journeys (booking, claims, tracking, etc.)

**About the Users:**
- [ ] 3-4 primary personas (who uses this product)
- [ ] Key goals for each persona
- [ ] Pain points they experience today
- [ ] How they measure success

**About Existing Context:**
- [ ] Product adoption stories or case studies (in current avatars)
- [ ] Recent product decisions or initiatives
- [ ] Related products or systems
- [ ] Team familiar with the domain

### Get Domain Expertise

Assign a **domain expert** (product manager or senior engineer familiar with this product):
- Reviews examples for accuracy and completeness
- Validates personas and journeys
- Ensures law applications are realistic
- Time commitment: 2-3 hours total

---

## Step 2: Create the Structure

### File Organization

```
avatars/product-type/{{ product-slug }}/
├── manifest.yaml                    ← Configuration (from manifest-template.yaml)
├── personas.md                      ← User types (from personas-template.md)
├── guidance.md                      ← Product-specific guidance
├── examples/                        ← NEW: Law demonstrations
│   ├── PRD-1.1-discovery.md        ← How to do discovery for this product
│   ├── PRD-2.1-journey.md          ← How to map journeys for this product
│   ├── PRD-3.1-roadmap.md          ← How to plan roadmap for this product
│   ├── PRD-4.1-mvp.md              ← How to define MVP for this product
│   └── PRD-5.1-metrics.md          ← How to measure success for this product
└── use-cases/                       ← NEW: Real workflows
    ├── use-case-1/
    │   ├── README.md               ← Overview
    │   ├── discovery/              ← Discovery phase artifacts
    │   ├── planning/               ← Planning phase artifacts
    │   ├── implementation/         ← Build phase artifacts
    │   └── results/                ← Measurement & results
    ├── use-case-2/
    └── use-case-3/
```

### Create Folders

```bash
# Create the structure
PRODUCT_SLUG=cargo-freight  # lowercase-with-dashes

mkdir -p avatars/product-type/$PRODUCT_SLUG/examples
mkdir -p avatars/product-type/$PRODUCT_SLUG/use-cases/{ use-case-1,use-case-2,use-case-3}
```

---

## Step 3: Create manifest.yaml

**Time:** 30 minutes  
**Resources:** manifest-template.yaml, existing technology avatars for reference

### Fill in the Template

Start with [manifest-template.yaml](../../templates/avatars/manifest-template.yaml):

```bash
# Copy the template
cp docs/templates/avatars/manifest-template.yaml avatars/product-type/$PRODUCT_SLUG/manifest.yaml

# Edit to fill in:
# - avatar.id (product-{{ slug }})
# - avatar.name (display name)
# - domain.category (product category)
# - domain.personas (names of personas)
# - core_journeys (4-5 main user journeys)
# - activates.skills (which domain skills to use)
# - specializes_laws (PRD-1.1 through PRD-5.1 mappings)
```

### Key Fields to Populate

| Field | Example | Notes |
|-------|---------|-------|
| `avatar.id` | `avatar-product-cargo` | Slug: lowercase, hyphens, no spaces |
| `avatar.name` | `Cargo & Freight` | Display name (can have spaces) |
| `domain.category` | `Cargo Booking & Operations` | 2-3 word category |
| `core_journeys` | `["Rate Quote to Booking", "Claims Processing"]` | 4-5 main workflows |
| `specializes_laws[*].id` | `PRD-1.1` | Must be PRD-1.1 through PRD-5.1 |
| `specializes_laws[*].example_file` | `examples/PRD-1.1-discovery.md` | File you'll create in Step 4 |

### Validation

```bash
# Check YAML syntax
python3 -c "import yaml; yaml.safe_load(open('avatars/product-type/$PRODUCT_SLUG/manifest.yaml'))"

# Should output: (no errors)
```

---

## Step 4: Create personas.md

**Time:** 1 hour  
**Resources:** personas-template.md, existing product context, domain expert input

### Research Personas

Identify 3-4 primary personas:

1. **Primary persona** - Main user/customer of product
2. **Secondary persona** - Important but less frequent user
3. **Enabling persona** - Support/admin role (if applicable)
4. **Advocacy persona** - Product champion or decision-maker

### Fill Template

Use [personas-template.md](../../templates/avatars/personas-template.md):

```bash
# Copy template
cp docs/templates/avatars/personas-template.md avatars/product-type/$PRODUCT_SLUG/personas.md

# Edit to fill:
# For each persona:
#   - Name (e.g., "Alice, Freight Forwarder")
#   - Role and organization type
#   - Goals (3 specific goals)
#   - Pain points (3 current challenges)
#   - Behaviors (3 ways they interact)
#   - Authentic quote
#   - Which laws matter most to them
```

### Make it Real

❌ Generic: "The user wants to book cargo"  
✅ Specific: "Alice, a freight forwarder, needs to book cargo in <2 minutes while on the phone with her customer"

For each persona:
- Ground in real behavior, not aspirational
- Connect to why they care about your product
- Show what success looks like for them

---

## Step 5: Create example files (PRD-1.1 through PRD-5.1)

**Time:** 3-4 hours (including domain expert review)  
**Resources:** example-template.md, law-citation-guide.md, product examples, domain expert

### One Example Per Law

Create 5 files:

| File | Law | What It Shows |
|------|-----|--------------|
| PRD-1.1-discovery.md | Continuous Discovery | How to research customer needs for your product |
| PRD-2.1-journey.md | User Journey Mapping | How to map workflows and identify touchpoints |
| PRD-3.1-roadmap.md | Roadmap Planning | How to prioritize features and plan releases |
| PRD-4.1-mvp.md | MVP & Product-Market Fit | How to define MVP and validate market fit |
| PRD-5.1-metrics.md | Metrics & Success | How to define KPIs and measure success |

### Guidance for Each Example

#### PRD-1.1: Discovery

**Show:** How you understand customer needs for this product

```
Describe:
1. Who you interviewed (which personas)
2. What you asked them
3. What you discovered
4. How it changed your thinking
5. What decision it led to

Token Budget: 750 tokens
Include: Quote from customer interview, discovery method, key finding
```

**Real Example: Cargo** "Interviewed 5 freight forwarders → discovered rate quote time was #1 pain (45 sec vs. competitor's 15 sec) → prioritized quote optimization"

#### PRD-2.1: Journey Mapping

**Show:** The workflow/journey for this product

```
Describe:
1. Who this journey is for (which persona)
2. The journey steps (start to finish)
3. Key touchpoints
4. Where friction/problems occur
5. What improvements matter most

Token Budget: 750 tokens
Include: Journey diagram or structured list, friction points, solution opportunities
```

**Real Example: Cargo** "Cargo booking journey: Find rate → Get quote → Review options → Confirm booking → Schedule pickup. Friction at 'Get quote' (slow) and 'Schedule pickup' (integration missing)."

#### PRD-3.1: Roadmap

**Show:** How to prioritize features for this product

```
Describe:
1. Features/improvements being considered
2. How you prioritized them (what criteria)
3. What ranked highest and why
4. Timeline/phases
5. Expected impact

Token Budget: 750 tokens
Include: Prioritization matrix, top 3-5 initiatives, quarterly roadmap
```

**Real Example: Cargo** "Prioritized by: (1) Customer impact (interviews), (2) Revenue impact, (3) Engineering effort. Q1: Quote optimization, Q2: Pickup integration, Q3: Rate alerts."

#### PRD-4.1: MVP & Product-Market Fit

**Show:** How to define minimum viable product and validate fit

```
Describe:
1. The problem you're solving
2. The MVP scope (what's in, what's out)
3. How you validated the need
4. Market fit indicators
5. Path to full product

Token Budget: 750 tokens
Include: MVP feature list, validation method, success metrics
```

**Real Example: Cargo** "MVP for freight tracking: Real-time location + proactive alerts. In: SMS + email notifications. Out: Mobile app, customs tracking. Validated: 15/16 testers said they'd use it daily."

#### PRD-5.1: Metrics & Success

**Show:** How you measure whether this product is successful

```
Describe:
1. What success means (business & user)
2. KPIs you track
3. Baseline (where you started)
4. Target (where you want to be)
5. How you report and act on metrics

Token Budget: 750 tokens
Include: KPI table, measurement methods, decision thresholds
```

**Real Example: Cargo** "Success metrics: Quote speed (target: <15s), Booking rate (target: 8%), Customer NPS (target: 45). Measured weekly. If quote speed > 20s, escalate to engineering."

### Apply Law Citations

For each example:
- Start with law reference: `[PRD-N.N: Title](path to law)`
- Cite specific practices/principles from law
- Show product-specific application
- Follow [law-citation-guide.md](law-citation-guide.md)

### Domain Expert Review

Before finalizing:
- [ ] Persona examples are accurate (asked domain expert: "Is this real?")
- [ ] Law citations match actual law content
- [ ] Token count ≤ 800 (run: `wc -w file.md * 0.75`)
- [ ] Examples demonstrate product differentiation (not generic)
- [ ] Law applications are realistic (not aspirational)

---

## Step 6: Create use-cases/ (Optional but Recommended)

**Time:** 3-4 hours  
**Resources:** use-case-template.md, existing product workflows, domain expert

### Define 2-3 Use Cases

Choose real workflows that combine multiple laws:

| Use Case | Laws | Description |
|----------|------|-------------|
| Booking Workflow | PRD-1.1, 2.1, 3.1, 4.1, 5.1 | Complete flow from discovery to measuring success |
| Claims Processing | PRD-1.1, 2.1, 5.1 | How to handle exceptions and measure satisfaction |
| Rate Optimization | PRD-3.1, 4.1, 5.1 | Planning and measuring pricing changes |

### Use-Case Structure

Each use case includes:

```
use-cases/booking-workflow/
├── README.md                    ← Overview of workflow
├── discovery/
│   ├── customer_research.md     ← Findings from PRD-1.1
│   ├── journey_map.md           ← Map from PRD-2.1
│   └── findings.md
├── planning/
│   ├── roadmap.md               ← Priorities from PRD-3.1
│   ├── mvp_spec.md              ← MVP from PRD-4.1
│   └── executable_spec.md
├── implementation/
│   ├── design.md
│   ├── code_review.md
│   └── testing.md
└── results/
    ├── metrics.md               ← KPIs from PRD-5.1
    ├── launch_notes.md
    └── analysis.md
```

Use [use-case-template.md](../../templates/avatars/use-case-template.md) to structure each phase.

---

## Step 7: Create guidance.md

**Time:** 1 hour  
**Resources:** manifest.yaml, examples, personas

### What Goes in guidance.md?

```markdown
# {{ Product Name }} Guidance

## Overview
{{ 2-3 sentence summary of product and why constitution matters }}

## Core Product Laws

{{ Reference the 5 PRD laws and when they apply to this product }}

## For Each Persona

For {{ Persona }}, start with:
- [PRD-1.1: Discovery](examples/PRD-1.1-discovery.md) to understand needs
- [PRD-2.1: Journey Mapping](examples/PRD-2.1-journey.md) to identify workflow
- {{ etc. }}

## Common Questions

- When do I use PRD-1.1 vs PRD-2.1? {{ Answer }}
- How long does each law take? {{ Estimate }}
- Can I skip any laws? {{ No/Yes - when }}

## Getting Started

1. Choose your persona
2. Start with [PRD-1.1 example](examples/PRD-1.1-discovery.md)
3. Follow the workflow for your use case
```

---

## Step 8: Validation

### Before Publishing

Run these checks:

```bash
# 1. Manifest YAML valid
python3 -c "import yaml; yaml.safe_load(open('manifest.yaml'))"

# 2. All example files exist
ls examples/PRD-*.md | wc -l  # Should be 5

# 3. All example files have citations
grep -l "\[PRD-" examples/PRD-*.md | wc -l  # Should be 5

# 4. Token counts
python3 -c "
import os, re
for f in os.listdir('examples'):
    if f.endswith('.md'):
        text = open(f'examples/{f}').read()
        tokens = len(text.split()) * 0.75
        status = '✓' if tokens < 850 else '✗'
        print(f'{status} {f}: {int(tokens)} tokens')
"

# 5. No broken law links (requires test access to laws/)
# Manual: Click each [PRD-N.N] link to verify
```

### Domain Expert Approval

- [ ] Personas are realistic and accurate
- [ ] Examples demonstrate real product applications
- [ ] Laws are applied correctly
- [ ] Use cases represent actual workflows
- [ ] Token counts are reasonable

---

## Checklist

### Pre-Creation

- [ ] Product name and slug defined
- [ ] 3-4 personas identified
- [ ] 4-5 core journeys listed
- [ ] Domain expert identified
- [ ] Existing product context gathered

### Creation (Per Example)

For each of the 5 examples (PRD-1.1 through PRD-5.1):

- [ ] Example file created from template
- [ ] Law reference added (opening paragraph)
- [ ] Product-specific context (not generic)
- [ ] Concrete example (not aspirational)
- [ ] Law principles explained
- [ ] Citations verified accurate
- [ ] Domain expert review completed
- [ ] Token count ≤ 800
- [ ] Related skills linked
- [ ] Related laws linked

### Post-Creation

- [ ] All 5 examples complete
- [ ] manifest.yaml points to all examples
- [ ] guidance.md created and reviewed
- [ ] use-cases/ complete (if included)
- [ ] All YAML validates
- [ ] No broken links
- [ ] Domain expert approval obtained
- [ ] Ready for RAG indexing

---

## Timeline

| Phase | Duration | Effort |
|-------|----------|--------|
| Information gathering | 1 hour | 1 person |
| manifest.yaml creation | 30 min | 1 person |
| personas.md creation | 1 hour | 1 person + 0.5 domain expert |
| 5 example files | 3 hours | 1 person |
| Domain expert review | 1.5 hours | Domain expert |
| use-cases/ (optional) | 3-4 hours | 1 person |
| Final validation | 30 min | 1 person |
| **Total** | **10-12 hours** | **1 person + 1 domain expert** |

---

## Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Example accuracy | 100% | Domain expert validation |
| Law citation coverage | 5/5 laws | Count PRD-*.md files |
| Token efficiency | ≤800 avg | wc -w × 0.75 |
| Broken links | 0 | Click each [PRD-N.N] |
| Use cases included | 2-3 min | Count use-cases/ folders |
| Domain expert approval | Yes | Sign-off on manifest.yaml |

---

## References

- [manifest-template.yaml](../../templates/avatars/manifest-template.yaml)
- [example-template.md](../../templates/avatars/example-template.md)
- [personas-template.md](../../templates/avatars/personas-template.md)
- [use-case-template.md](../../templates/avatars/use-case-template.md)
- [law-citation-guide.md](law-citation-guide.md)
- [Technology Avatar Example](../../../avatars/technology/java-spring/) (for reference)

---

**Last Updated:** February 23, 2026
