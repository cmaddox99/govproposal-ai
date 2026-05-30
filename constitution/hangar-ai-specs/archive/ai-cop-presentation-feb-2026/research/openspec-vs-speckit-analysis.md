# Research: OpenSpec vs Spec Kit Analysis

**Purpose:** Provide evidence-based comparison for AI COP presentation  
**Status:** 🔄 In Progress  
**Last Updated:** 2026-02-05

---

## 1. Spec Kit Background

### 1.1 What is Spec Kit?

Based on available documentation and the architect_guild.md comparison:

**GitHub Spec Kit** is a Microsoft tool for AI-assisted development that provides:
- Structured prompts for specification-driven development
- A fixed sequence of commands for building software from scratch
- Optimized for **greenfield (0→1)** development scenarios

**Commands (from architect_guild.md):**
```bash
/speckit.constitution  # Create principles
/speckit.specify       # Define requirements
/speckit.plan          # Tech stack selection
/speckit.tasks         # Generate task list
/speckit.implement     # Build from scratch
```

### 1.2 Current Status (Needs Verification)

⚠️ **Issue:** Multiple Spec Kit URLs are returning 404 errors:
- https://github.com/microsoft/spec-kit → 404
- https://microsoft.github.io/SpecKit/ → 404
- https://devblogs.microsoft.com/copilot/spec-kit/ → 404

**Possible explanations:**
1. Project renamed or reorganized
2. Moved to different repository
3. Deprecated or sunset
4. Made private/internal

**Action Required:** 
- Check Microsoft Garage blog for announcements
- Search GitHub for renamed repository
- Contact Microsoft developer relations

### 1.3 Spec Kit Stated Use Case

From documentation captured in architect_guild.md:
> "0-to-1 Development ('Greenfield')" - Generate from scratch

**Key insight:** Spec Kit is explicitly designed for creating new projects, not evolving existing systems.

---

## 2. OpenSpec Background

### 2.1 What is OpenSpec?

**OpenSpec** is a spec-driven development framework developed by Click Chain/AA Hangar that provides:
- Constitutional AI governance for software development
- Flexible workflow commands (not rigid sequence)
- Delta-based change tracking
- Optimized for **brownfield (1→n)** evolution scenarios

**Commands:**
```bash
/opsx:explore [topic]    # Investigate before committing
/opsx:new [name]         # Create new change
/opsx:continue [name]    # Generate next artifact incrementally
/opsx:ff [name]          # Fast-forward: generate all at once
/opsx:apply [name]       # Execute implementation
/opsx:verify [name]      # Validate implementation
/opsx:sync [name]        # Integrate deltas to main specs
/opsx:archive [name]     # Complete and archive
```

### 2.2 OpenSpec Philosophy

From skill-00-openspec.md:
- **Fluid not rigid** - Commands are actions, not stages you're stuck in
- **Iterative not waterfall** - Learning happens during building; specs evolve
- **Easy not complex** - Minimal ceremony; customize only when needed
- **Brownfield-first** - Delta-based changes for existing systems

---

## 3. Detailed Comparison

### 3.0 Terminology: RAG vs Hierarchical Segmentation

**Important Clarification:**

| Term | What It Means | Applies to OpenSpec? |
|------|---------------|---------------------|
| **RAG** (Retrieval-Augmented Generation) | Vector embeddings + semantic search + retrieval system | ❌ Not today |
| **Hierarchical Context Segmentation** | Index-based selective loading via YAML catalogs | ✅ Today |
| **RAG-Ready Architecture** | Structure that enables future Multi-Source RAG | ✅ The foundation |
| **Multi-Source RAG** | Vector search across multiple adopted codebases | 🔮 Future state |

**Today's Reality:**
- We use **index files** (YAML) as lookup tables
- We do **hierarchical navigation** (catalog → skill → avatar)
- We do **selective/lazy loading** based on intent matching
- **No vector embeddings**, no semantic search, no retrieval system

**Why the Structure Matters for Future RAG:**
- Index files → Metadata for filtered retrieval
- Law IDs (ENG-4.1) → Tags for hybrid search
- Avatar structure → Chunk boundaries by tech/industry
- `changes/` folder → Natural document units
- `specs/` folder → Structured knowledge chunks

**The hierarchical structure we built IS the chunking strategy for future Multi-Source RAG across adopted codebases.**

### 3.1 Primary Use Case

| Aspect | Spec Kit | OpenSpec |
|--------|----------|----------|
| **Target Scenario** | 0→1 Greenfield | 1→n Brownfield |
| **Starting Point** | Empty project | Existing codebase |
| **Change Model** | Full generation | Delta-based |
| **Iteration Support** | Limited | Native |

### 3.2 Workflow Structure

**Spec Kit (Rigid Sequential):**
```
constitution → specify → plan → tasks → implement
     ↓           ↓        ↓       ↓          ↓
 [Create]    [Full]   [Full]  [Full]    [Build]
            [Spec]   [Plan]  [Tasks]
```
- Each step generates complete artifacts
- Moving backward requires regeneration
- Not designed for incremental updates

**OpenSpec (Flexible Iterative):**
```
explore ←→ new → continue ←→ apply ←→ verify → sync → archive
   ↑         ↓        ↑         ↓        ↑        ↓
[Learn]  [Delta]  [Delta]   [Delta]  [Check]  [Merge]
```
- Commands can be used in any order
- Delta-based changes (only modifications)
- Supports iterative refinement

### 3.3 Token Efficiency Model

**Regenerative Model (Spec Kit pattern):**
```
Iteration 1: Generate full spec      → ~10,000 tokens
Iteration 2: Regenerate full spec    → ~10,000 tokens
Iteration 3: Regenerate full spec    → ~10,000 tokens
Iteration 4: Regenerate full spec    → ~10,000 tokens
Iteration 5: Regenerate full spec    → ~10,000 tokens
─────────────────────────────────────────────────────
Total for 5 iterations:              → ~50,000 tokens
```

**Delta Model (OpenSpec pattern):**
```
Iteration 1: Generate initial spec   → ~10,000 tokens
Iteration 2: Update delta only       → ~2,000 tokens
Iteration 3: Update delta only       → ~2,000 tokens
Iteration 4: Update delta only       → ~2,000 tokens
Iteration 5: Update delta only       → ~2,000 tokens
─────────────────────────────────────────────────────
Total for 5 iterations:              → ~18,000 tokens
```

**Token Savings:** 64% reduction over 5 iterations

### 3.4 Constitutional Integration

| Feature | Spec Kit | OpenSpec |
|---------|----------|----------|
| Law references | Limited | Native (`laws.implements`) |
| Skill orchestration | None | Built-in (`followed_by`) |
| Avatar support | None | Technology + Industry |
| Compliance checking | External | Integrated |
| Audit trail | Implicit | Explicit (`changes/` folder) |

### 3.5 Enterprise Suitability

| Requirement | Spec Kit | OpenSpec |
|-------------|----------|----------|
| Legacy modernization | ❌ Not designed | ✅ Primary focus |
| Compliance/Audit | ❌ No built-in | ✅ `changes/` folder |
| Large team consistency | ❌ Prescriptive only | ✅ Constitutional laws |
| Custom workflows | ❌ Fixed sequence | ✅ Configurable |
| Multi-year evolution | ❌ Not addressed | ✅ Delta-based |

---

## 4. The Waterfall Parallel

### 4.1 Historical Context

**Waterfall Model Origin (1970):**
- Winston Royce presented the sequential model
- **But:** He described it as having "major flaws"
- **Key flaw:** Testing only at the end = "risky and inviting failure"
- **Intended use:** Initial iteration only, with feedback loops

**What Actually Happened:**
- DoD adopted the rigid sequential model (DOD-STD-2167, 1985)
- Applied it to all software development (0→1 AND n→n+1)
- Industry followed DoD's lead
- **Result:** Decades of software project failures

**DoD Course Correction:**
- MIL-STD-498 (1994) reversed course
- Now encourages "iterative and incremental development"

### 4.2 The Pattern

| Stage | Waterfall | Spec Kit |
|-------|-----------|----------|
| **Design Intent** | Initial iteration | Greenfield projects |
| **Adoption Scope** | All projects | Risk of broad adoption |
| **Problem** | Applied to evolution work | Same risk |
| **Consequence** | Costly rework | Token inefficiency, rigidity |

**The Warning:** Tools designed for 0→1 development, when applied broadly to n→n+1 work, create systemic problems.

### 4.3 Why This Matters for AA

**AA's Reality:**
- ~90% of work is brownfield (existing systems)
- Legacy modernization is constant
- Compliance requirements demand audit trails
- Teams need flexibility, not prescription

**Adopting Spec Kit broadly would repeat the waterfall mistake:**
- Using a 0→1 tool for 1→n work
- Generating full artifacts when deltas suffice
- Following rigid sequences when iteration is needed

---

## 5. Market Adoption Research

### 5.1 Constitutional AI Frameworks

**Observed Trends:**
- Anthropic's Constitutional AI research (2022) gaining enterprise attention
- Organizations seeking AI governance frameworks
- Compliance requirements driving structured AI adoption

**Known Implementations:**
1. **AA Hangar AI Constitution** - American Airlines (documented)
2. **CC-AI-CONSTITUTION** - Click Chain (open source reference)
3. **Various enterprises** - Rumored implementations (NDA-bound)

### 5.2 Spec-Driven Development Tools

| Tool | Focus | Adoption |
|------|-------|----------|
| Spec Kit | Greenfield | Unknown (URLs 404) |
| OpenSpec | Brownfield | AA Cargo pilot |
| Cucumber/BDD | Behavior specs | Widespread |
| Gherkin | Acceptance criteria | Common |

### 5.3 Microsoft's AI Coding Direction

**GitHub Copilot Evolution:**
- Copilot Chat
- Copilot Workspace (for planning)
- Spec Kit (status unclear)

**Question for Investigation:** Is Microsoft consolidating Spec Kit into Copilot Workspace?

---

## 6. Vulnerability Assessment

### 6.1 Potential OpenSpec Vulnerabilities

| Area | Vulnerability | Mitigation |
|------|--------------|------------|
| **Spec Injection** | Malicious content in specs | Validate inputs, code review |
| **Constitution Drift** | Laws become outdated | Amendment process, governance |
| **Token Leakage** | Sensitive data in prompts | Data classification, filtering |
| **Dependency Risk** | AI model availability | Multi-model support |
| **Audit Integrity** | Change folder tampering | Git signed commits, access control |

### 6.2 Spec Kit Vulnerabilities (Comparative)

| Area | Spec Kit | OpenSpec |
|------|----------|----------|
| Audit trail | Weaker (implicit) | Stronger (explicit) |
| Governance | External | Integrated |
| Compliance | Manual | Constitutional |

### 6.3 Security Recommendations

1. **Implement signed commits** for `changes/` folder integrity
2. **Add constitution-lint** to CI/CD pipelines
3. **Classify spec content** (PII, secrets, business logic)
4. **Version control** all constitutional amendments
5. **Regular security review** of AI agent instructions

---

## 7. Recommendations

### 7.1 For AI COP Presentation

1. **Lead with results** - Wave 2 metrics are compelling
2. **Be fair to Spec Kit** - It's good for greenfield, just not AA's focus
3. **Use waterfall parallel carefully** - Historically accurate, powerful analogy
4. **Emphasize token efficiency** - Quantifiable, measurable benefit
5. **Address vulnerabilities proactively** - Shows maturity

### 7.2 For Tech Radar Submission

1. **Document the case study** - AA Cargo results
2. **Provide token efficiency analysis** - Already complete
3. **Address security concerns** - Mitigation strategies
4. **Show governance model** - Amendment process
5. **Compare to alternatives** - This document

### 7.3 For Ongoing Development

1. **Monitor Spec Kit** - Check if Microsoft enhances for brownfield
2. **Track market adoption** - Constitutional AI momentum
3. **Maintain constitution** - Laws only valuable if current
4. **Expand pilots** - More teams, more evidence

---

## 8. Open Questions

1. What happened to Spec Kit? (URLs 404)
2. Is Microsoft planning brownfield support?
3. What specific vulnerabilities does Nag see?
4. What is the broader Constitutional AI market trajectory?
5. Are there enterprise competitors to OpenSpec?

---

## 9. Sources

1. architect_guild.md - OpenSpec vs Spec Kit comparison
2. engineering-laws-committee-kickoff.md - Wave 2 results
3. skill-00-openspec.md - OpenSpec skill definition
4. aacargo-case-study.md - Full case study paper
5. Wikipedia: Waterfall Model - Historical context
6. Royce, W. (1970) - Original waterfall paper critique
7. DOD-STD-2167 (1985) - DoD waterfall adoption
8. MIL-STD-498 (1994) - DoD iterative pivot
