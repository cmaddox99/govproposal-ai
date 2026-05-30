---
title: "{{ Product }} — {{ Use Case Name }}"
avatar_type: "product"
avatar_id: "avatar-product-{{ product }}"
artifact_type: "use-case"
token_budget: "1200-1500"
laws_applied:
  - "PRD-1.1"
  - "PRD-2.1"
exit_checklist:
  - item: "All phases have explicit law citations"
    status: "pend"
  - item: "Token budget ≤ 1500 tokens verified"
    status: "pend"
  - item: "Personas involved are product-type roles (not engineering)"
    status: "pend"
  - item: "Value delivered maps to a measurable outcome"
    status: "pend"
  - item: "Use case is specific to {{ product }} context"
    status: "pend"
audit_log:
  - date: "{YYYY-MM-DD}"
    actor: "{Agent or Human}"
    action: "Use case template instantiated"
    outcome: "DRAFTED"
template_version: "1.0.0"
template_path: "docs/templates/avatars/use-case-template.md"
---

# Use Case Template

Use this template to document workflows that combine product laws with real {{ product }} scenarios.  
**Location:** `avatars/product-type/{{ product }}/use-cases/{{ workflow-name }}/`  
**Token Budget:** 1200-1500 tokens per use case

---

# {{ Product }} Use Case: {{ Use Case Name }}

**Overview:**  
{{ 1-2 sentence summary of what this workflow achieves }}

**Personas Involved:**
- {{ Persona 1 }}
- {{ Persona 2 }}
- {{ Persona 3 }}

**Value Delivered:**
- {{ Benefit 1 }}
- {{ Benefit 2 }}
- {{ Benefit 3 }}

---

## Workflow

### Phase 1: Discovery (PRD-1.1 & PRD-2.1)

**Objective:** {{ What are we trying to understand? }}

**Activities:**
```
1. Research
   └─ Interviews with {{ personas }}
   └─ Document: customer_needs.md
   └─ Law: PRD-1.1 (Continuous Discovery)

2. Journey Mapping
   └─ Map current {{ product }} flow
   └─ Identify friction points
   └─ Document: journey_map.md
   └─ Law: PRD-2.1 (User Journey Mapping)

3. Analysis
   └─ Synthesize findings
   └─ Validate assumptions
   └─ Output: discovery_findings.md
```

**Deliverables:**
- {{ Deliverable 1 }} ({{ Responsible Party }})
- {{ Deliverable 2 }} ({{ Responsible Party }})

**Skills Applied:**
- [{{ Skill Name }}](../../../../../agent-skills/skills-by-domain/{{ domain }}/{{ skill-file }}.md)
- [{{ Skill Name }}](../../../../../agent-skills/skills-by-domain/{{ domain }}/{{ skill-file }}.md)

---

### Phase 2: Planning & Design (PRD-3.1 & PRD-4.1)

**Objective:** {{ What are we deciding? }}

**Activities:**
```
1. Roadmap Planning
   └─ Prioritize solutions per PRD-3.1
   └─ Define phases and milestones
   └─ Document: product_roadmap.md
   └─ Law: PRD-3.1 (Roadmap Planning)

2. MVP Definition
   └─ Define minimum viable {{ product }}
   └─ Validate market fit assumptions
   └─ Document: mvp_spec.md
   └─ Law: PRD-4.1 (MVP & PMF)

3. Specification
   └─ Create detailed specification
   └─ Define acceptance criteria
   └─ Document: executable_spec.md
```

**Deliverables:**
- {{ Deliverable 1 }} ({{ Responsible Party }})
- {{ Deliverable 2 }} ({{ Responsible Party }})

**Skills Applied:**
- [{{ Skill Name }}](../../../../../agent-skills/skills-by-domain/{{ domain }}/{{ skill-file }}.md)
- [{{ Skill Name }}](../../../../../agent-skills/skills-by-domain/{{ domain }}/{{ skill-file }}.md)

---

### Phase 3: Implementation (ENG-6.1, ENG-7.1)

**Objective:** {{ Build or experiment }}

**Activities:**
```
1. Development
   └─ Vertical slice implementation
   └─ Atomic TDD approach
   └─ Document: implementation.md
   └─ Laws: ENG-6.1 (TDD), ENG-7.1 (Vertical Slice)

2. Validation
   └─ Test with {{ persona }} representatives
   └─ Gather feedback
   └─ Document: feedback.md

3. Iteration
   └─ Refine based on feedback
   └─ Prepare for wider rollout
```

**Deliverables:**
- {{ Deliverable 1 }} ({{ Responsible Party }})
- {{ Deliverable 2 }} ({{ Responsible Party }})

**Skills Applied:**
- [{{ Skill Name }}](../../../../../agent-skills/skills-by-domain/{{ domain }}/{{ skill-file }}.md)
- [{{ Skill Name }}](../../../../../agent-skills/skills-by-domain/{{ domain }}/{{ skill-file }}.md)

---

### Phase 4: Launch & Measure (PRD-5.1)

**Objective:** {{ Release and measure success }}

**Activities:**
```
1. Metrics Definition
   └─ Define success KPIs per PRD-5.1
   └─ Set up measurement infrastructure
   └─ Document: metrics.md
   └─ Law: PRD-5.1 (Metrics & Success)

2. Release
   └─ Execute go-to-market plan
   └─ Monitor initial adoption
   └─ Document: launch_notes.md

3. Analysis
   └─ Measure against KPIs
   └─ Identify learnings
   └─ Plan next iteration
   └─ Document: results_analysis.md
```

**Deliverables:**
- {{ Deliverable 1 }} ({{ Responsible Party }})
- {{ Deliverable 2 }} ({{ Responsible Party }})

**Skills Applied:**
- [{{ Skill Name }}](../../../../../agent-skills/skills-by-domain/{{ domain }}/{{ skill-file }}.md)
- [{{ Skill Name }}](../../../../../agent-skills/skills-by-domain/{{ domain }}/{{ skill-file }}.md)

---

## Example Execution: {{ Specific {{ product }} Case }}

**Scenario:** {{ Concrete example of when this workflow is used }}

**Team Composition:**
- {{ Role 1 }}: {{ Responsibility }}
- {{ Role 2 }}: {{ Responsibility }}
- {{ Role 3 }}: {{ Responsibility }}

**Timeline:**
- Discovery Phase: {{ Duration }}
- Planning Phase: {{ Duration }}
- Implementation: {{ Duration }}
- Measurement: {{ Duration }}
- **Total:** {{ Total Duration }}

**Key Decisions:**
1. {{ Decision }} ({{ Phase }})
   - Law Applied: PRD-{{ Number }}
   - Outcome: {{ Result }}

2. {{ Decision }} ({{ Phase }})
   - Law Applied: PRD-{{ Number }}
   - Outcome: {{ Result }}

3. {{ Decision }} ({{ Phase }})
   - Law Applied: PRD-{{ Number }}
   - Outcome: {{ Result }}

**Results:**
- {{ Metric 1 }}: {{ Starting }} → {{ Ending }} ({{ Change }})
- {{ Metric 2 }}: {{ Starting }} → {{ Ending }} ({{ Change }})
- {{ Metric 3 }}: {{ Starting }} → {{ Ending }} ({{ Change }})

---

## Related Documentation

**Laws Applied:**
- [PRD-1.1: Continuous Discovery](../../../../../laws/product/discovery.md)
- [PRD-2.1: User Journey Mapping](../../../../../laws/product/journey.md)
- [PRD-3.1: Roadmap Planning](../../../../../laws/product/roadmap.md)
- [PRD-4.1: MVP & Product-Market Fit](../../../../../laws/product/experimentation.md)
- [PRD-5.1: Metrics & Success](../../../../../laws/product/metrics.md)

**Related Skills:**
- [Discovery & Research Domain](../../../../../agent-skills/skills-by-domain/discovery-research/)
- [Product Planning Domain](../../../../../agent-skills/skills-by-domain/product-planning/)

**Similar Use Cases:**
- [{{ Related Use Case 1 }}](../{{ related-slug }}/README.md)
- [{{ Related Use Case 2 }}](../{{ related-slug }}/README.md)

---

**Last Updated:** {{ YYYY-MM-DD }}  
**Product:** {{ Product Name }}  
**Use Case:** {{ Use Case Name }}  
**Status:** {{ Draft | Validated | Refined }}
