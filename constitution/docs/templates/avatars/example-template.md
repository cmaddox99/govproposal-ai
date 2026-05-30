---
title: "{{ Product }} — {{ Law Title }} Example"
avatar_type: "product"
avatar_id: "avatar-product-{{ product }}"
artifact_type: "example"
law: "PRD-{{ Law Number }}"
token_budget: "750-800"
laws_applied:
  - "PRD-{{ Law Number }}"
exit_checklist:
  - item: "Law reference is accurate and links to the correct law file"
    status: "pend"
  - item: "Example scenario is specific to {{ product }} context"
    status: "pend"
  - item: "Token budget ≤ 800 tokens verified"
    status: "pend"
  - item: "Outcome demonstrates the law producing measurable value"
    status: "pend"
audit_log:
  - date: "{YYYY-MM-DD}"
    actor: "{Agent or Human}"
    action: "Example template instantiated"
    outcome: "DRAFTED"
template_version: "1.0.0"
template_path: "docs/templates/avatars/example-template.md"
---

# Product Avatar Example Template

Use this template for each example file demonstrating a product law in action.  
**Location:** `avatars/product-type/{{ product }}/examples/PRD-{{ law-number }}-{{ law-slug }}.md`  
**Token Budget:** 750-800 tokens max

---

## Example: {{ Law-Specific Context }} (PRD-{{ Law Number }} {{ Law Title }})

**Law Reference:** [PRD-{{ Law Number }}: {{ Law Title }}](../../../laws/product/{{ law-topic }}.md)

**What This Example Shows:**
- {{ What the example demonstrates about applying this law }}
- {{ Specific {{ product }} context for this law }}
- {{ Expected outcomes }}

---

## Context: Why This Matters for {{ Product }}

{{ 2-3 sentences explaining the business value of this law for your specific product }}

**Key Principles from PRD-{{ Law Number }}:**
- Principle 1 as stated in law
- Principle 2 as stated in law
- Principle 3 as stated in law

---

## {{ Product }}-Specific Application

### Example Scenario
{{ Concrete scenario name: e.g., "New Feature Discovery: {{ Feature }}" }}

**Situation:** {{ What prompted using this law }}

**Challenge:** {{ What problem needs solving }}

**Approach (per PRD-{{ Law Number }}):**
```yaml
step_1_research:
  - activity: "{{ Activity 1 }}"
  - activity: "{{ Activity 2 }}"
  - deliverable: "{{ Output }}"

step_2_synthesis:
  - activity: "{{ Activity 1 }}"
  - deliverable: "{{ Output }}"

step_3_action:
  - activity: "{{ Activity }}"
  - result: "{{ Outcome }}"
```

---

## Real {{ Product }} Example

**Feature/Initiative:** {{ Specific {{ product }} example }}

**Discovery Process:**
1. {{ Step 1 and what was learned }}
2. {{ Step 2 and what was learned }}
3. {{ Step 3 and decision made }}

**Key Findings:**
```
research_findings:
  finding_1: "{{ Finding }}"
  finding_2: "{{ Finding }}"
  finding_3: "{{ Finding }}"

metrics:
  metric_1: "{{ Metric description }}: {{ Change }}"
  metric_2: "{{ Metric description }}: {{ Change }}"
```

**Applied Decision:**
{{ How the law was applied based on findings }}

---

## When to Apply PRD-{{ Law Number }}

✅ **Use this law when:**
- {{ Trigger 1 }}
- {{ Trigger 2 }}
- {{ Trigger 3 }}

❌ **Don't skip this law even if:**
- {{ Common excuse 1 }}
- {{ Common excuse 2 }}

---

## Related Skills

**Skills that complement this law:**
- [{{ Skill Name }}](../../../agent-skills/skills-by-domain/{{ domain }}/{{ skill-file }}.md)
- [{{ Skill Name }}](../../../agent-skills/skills-by-domain/{{ domain }}/{{ skill-file }}.md)

**Related Laws:**
- [PRD-{{ Related Number }}: {{ Related Title }}](../../../laws/product/{{ related-topic }}.md)

---

## Questions to Ask

When applying PRD-{{ Law Number }} to {{ product }}, ask:
1. {{ Question that validates understanding }}?
2. {{ Question that validates application }}?
3. {{ Question that prevents skipping }}?

---

**Last Updated:** {{ YYYY-MM-DD }}  
**Author:** {{ Name }}  
**Domain:** {{ product }}  
**Law:** PRD-{{ Law Number }}  
**Token Count:** {{ Actual tokens }}
