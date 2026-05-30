---
skill:
  id: skill-25-ux-design
  name: UX Design
  category: design
  version: "2.0.0"

laws:
  implements:
    - id: PRD-3.1
      title: Journey Mapping Law
    - id: PRD-3.4
      title: Experience Principles Law
  references:
    - id: PRD-2.1
      title: User Research Law
    - id: PRD-3.4
      title: Acceptance Criteria Law

triggers:
  phrases:
    - "Design the UX"
    - "User interface design"
    - "Accessibility review"
    - "Design system"

followed_by:
  - skill-26-design-to-code
  - skill-02-user-journey-mapping
---

# Skill 25: UX Design

> **Purpose:** Guide AI agents in UX design practices including design systems, component libraries, and Figma workflows.

---

## Overview

This skill enables AI agents to assist with user experience design, ensuring designs are user-centered, accessible, consistent, and implementable.

### Key Capabilities
1. **Design system management** - Component libraries and design tokens
2. **User research synthesis** - Personas, journey maps, usability findings
3. **Wireframing and prototyping** - Low to high fidelity design
4. **Accessibility compliance** - WCAG guidelines and inclusive design
5. **Design documentation** - Specifications for handoff to development

---

## Constitutional Compliance

### Engineering Constitution
- **Article II, Section 2.1** - Simplicity: Design simple, intuitive interfaces
- **Article III, Section 3.1** - Quality: Designs are testable and measurable
- **Article VI, Section 6.1** - Observability: Analytics and user feedback integration

### Product Constitution
- **Article II, Section 2.1** - Evidence-Based: Design decisions backed by research
- **Article III, Section 3.1** - User Journey: Understand the journey before designing
- **Article III, Section 3.2** - Acceptance Criteria: Clear design specifications

### Business Constitution
- **Article V, Section 5.1** - Accessibility: Inclusive design for all users
- **Article III, Section 3.3** - Audit Trail: Design decisions documented

---

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                     UX DESIGN WORKFLOW                          │
├─────────────────────────────────────────────────────────────────┤
│  1. Research      → Understand users and context                │
│  2. Define        → Problem statement and requirements          │
│  3. Ideate        → Explore solutions                           │
│  4. Design        → Create wireframes and prototypes            │
│  5. Validate      → Test with users                             │
│  6. Specify       → Document for development                    │
│  7. Handoff       → Transfer to implementation                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Design System Structure

### Component Library Organization

```
design-system/
├── foundations/
│   ├── colors.json           # Color tokens
│   ├── typography.json       # Font scales and styles
│   ├── spacing.json          # Spacing scale
│   ├── shadows.json          # Elevation system
│   └── breakpoints.json      # Responsive breakpoints
├── components/
│   ├── atoms/                # Basic building blocks
│   │   ├── button/
│   │   ├── input/
│   │   ├── icon/
│   │   └── typography/
│   ├── molecules/            # Component combinations
│   │   ├── form-field/
│   │   ├── card/
│   │   ├── nav-item/
│   │   └── search-bar/
│   └── organisms/            # Complex components
│       ├── header/
│       ├── footer/
│       ├── sidebar/
│       └── data-table/
├── patterns/                 # Reusable patterns
│   ├── forms/
│   ├── navigation/
│   ├── feedback/
│   └── layouts/
└── documentation/
    ├── usage-guidelines.md
    ├── accessibility.md
    └── contribution.md
```

### Design Tokens

```json
{
  "color": {
    "primary": {
      "50": "#eff6ff",
      "100": "#dbeafe",
      "500": "#3b82f6",
      "600": "#2563eb",
      "700": "#1d4ed8",
      "900": "#1e3a8a"
    },
    "semantic": {
      "success": "{color.green.500}",
      "warning": "{color.yellow.500}",
      "error": "{color.red.500}",
      "info": "{color.blue.500}"
    }
  },
  "spacing": {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px",
    "2xl": "48px"
  },
  "typography": {
    "fontFamily": {
      "sans": "Inter, system-ui, sans-serif",
      "mono": "JetBrains Mono, monospace"
    },
    "fontSize": {
      "xs": "12px",
      "sm": "14px",
      "base": "16px",
      "lg": "18px",
      "xl": "20px",
      "2xl": "24px",
      "3xl": "30px"
    }
  }
}
```

---

## Figma Workflow

### File Organization

```
Project/
├── 🎨 Design System
│   ├── Foundations
│   ├── Components
│   └── Patterns
├── 📋 Wireframes
│   ├── Low-Fidelity
│   └── User Flows
├── 🖼️ UI Designs
│   ├── Desktop
│   ├── Tablet
│   └── Mobile
├── 🔄 Prototypes
│   ├── User Testing
│   └── Stakeholder Review
└── 📄 Specifications
    ├── Component Specs
    └── Interaction Specs
```

### Component Naming Convention

```
[Category]/[Component]/[Variant]/[State]

Examples:
- Button/Primary/Default
- Button/Primary/Hover
- Button/Primary/Disabled
- Input/Text/Default
- Input/Text/Error
- Card/Product/Compact
- Card/Product/Expanded
```

### Auto Layout Best Practices

```markdown
## Auto Layout Guidelines

### Spacing
- Use consistent spacing from design tokens
- Prefer auto layout over manual positioning
- Set min/max constraints for responsive behavior

### Constraints
- Use "Fill container" for flexible elements
- Use "Fixed width" only when necessary
- Set proper resizing behavior for all layers

### Nesting
- Limit nesting to 3-4 levels maximum
- Group related elements logically
- Name frames descriptively
```

---

## Accessibility Guidelines

### WCAG 2.1 Compliance Checklist

```markdown
## Accessibility Checklist

### Perceivable
- [ ] Color contrast ratio ≥ 4.5:1 for normal text
- [ ] Color contrast ratio ≥ 3:1 for large text
- [ ] Color is not the only means of conveying information
- [ ] Text alternatives for non-text content
- [ ] Captions for multimedia content

### Operable
- [ ] All functionality available via keyboard
- [ ] Focus indicators visible and clear
- [ ] No keyboard traps
- [ ] Skip navigation links provided
- [ ] Touch targets ≥ 44x44px

### Understandable
- [ ] Language of page identified
- [ ] Labels and instructions clear
- [ ] Error messages descriptive
- [ ] Consistent navigation patterns
- [ ] Input assistance provided

### Robust
- [ ] Valid HTML/semantic markup
- [ ] ARIA labels where needed
- [ ] Compatible with assistive technologies
```

### Color Contrast Examples

```markdown
## Contrast Requirements

| Text Size | Ratio Required | Example |
|-----------|---------------|---------|
| Normal (<18px) | 4.5:1 | #595959 on #FFFFFF |
| Large (≥18px bold, ≥24px) | 3:1 | #767676 on #FFFFFF |
| UI Components | 3:1 | Border, icons |
| Focus Indicator | 3:1 | Visible outline |
```

---

## User Research Integration

### Persona Template

```markdown
## Persona: [Name]

### Demographics
- **Role:** [Job title/role]
- **Age:** [Age range]
- **Tech Savviness:** [Low/Medium/High]

### Goals
1. [Primary goal]
2. [Secondary goal]
3. [Tertiary goal]

### Pain Points
1. [Frustration 1]
2. [Frustration 2]
3. [Frustration 3]

### Behaviors
- [Key behavior 1]
- [Key behavior 2]

### Quote
> "[Representative quote that captures their mindset]"

### Scenario
[Brief narrative of how they use the product]
```

### Usability Testing Notes Template

```markdown
## Usability Test: [Feature Name]

**Participant:** [ID]
**Date:** [Date]
**Task:** [Task description]

### Observations

| Time | Action | Observation | Severity |
|------|--------|-------------|----------|
| 0:30 | [Action] | [What happened] | [1-5] |

### Task Success
- [ ] Completed without assistance
- [ ] Completed with hints
- [ ] Failed to complete

### Satisfaction (1-5): [Score]

### Quotes
> "[Direct quote]"

### Recommendations
1. [Recommendation based on observation]
```

---

## Design Specification Format

### Component Specification

```markdown
## Component: [Name]

### Purpose
[What this component does and when to use it]

### Anatomy
[Diagram or description of parts]

### Variants
| Variant | Use Case |
|---------|----------|
| Primary | Main actions |
| Secondary | Alternative actions |
| Tertiary | Low-emphasis actions |

### States
- Default
- Hover
- Active
- Focus
- Disabled
- Loading

### Properties
| Property | Type | Default | Options |
|----------|------|---------|---------|
| size | enum | medium | small, medium, large |
| variant | enum | primary | primary, secondary, tertiary |
| disabled | boolean | false | true, false |

### Spacing
- Padding: 12px 24px
- Margin: 0
- Gap (with icon): 8px

### Accessibility
- Role: button
- Keyboard: Enter/Space to activate
- Focus: Visible outline

### Do's and Don'ts
✅ Do: [Good practice]
❌ Don't: [Anti-pattern]
```

---

## Design Review Checklist

```markdown
## Design Review: [Feature Name]

### Visual Design
- [ ] Follows design system
- [ ] Consistent spacing and alignment
- [ ] Typography hierarchy clear
- [ ] Color usage appropriate

### Interaction Design
- [ ] Clear affordances
- [ ] Feedback for all actions
- [ ] Error states defined
- [ ] Loading states defined
- [ ] Empty states defined

### Accessibility
- [ ] Color contrast passing
- [ ] Touch targets adequate
- [ ] Focus states visible
- [ ] Screen reader friendly

### Responsiveness
- [ ] Desktop layout defined
- [ ] Tablet layout defined
- [ ] Mobile layout defined
- [ ] Breakpoint behavior clear

### Handoff Readiness
- [ ] All states documented
- [ ] Interactions specified
- [ ] Assets exported
- [ ] Developer notes added
```

---

## Integration with Development

### Design-Development Sync

```markdown
## Design Sync Meeting Agenda

1. **New Designs** (15 min)
   - Walk through new designs
   - Clarify interactions
   - Identify technical constraints

2. **In Progress** (10 min)
   - Review implementation fidelity
   - Address questions
   - Update specs if needed

3. **Completed** (5 min)
   - Sign-off on implemented designs
   - Document any deviations

4. **Backlog** (10 min)
   - Prioritize upcoming work
   - Identify dependencies
```

### Feedback Loop

```
Design → Prototype → Test → Refine → Spec → Build → Review → Iterate
   ↑                                                              │
   └──────────────────────────────────────────────────────────────┘
```

---

## Anti-Patterns

### Design Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Designing in isolation | Misalignment with development | Regular sync meetings |
| Skipping wireframes | Missing user flows | Start low-fidelity first |
| Inconsistent components | Visual debt | Use design system |
| Ignoring edge cases | Incomplete implementation | Define all states |
| No accessibility review | Exclusion, legal risk | Include in checklist |
| Over-designing | Scope creep, delays | Design for MVP first |

---

## Skill Relationships

### Prerequisites
- [02-User Journey Mapping](../discovery-research/02-user-journey-mapping.md) - Understand user context

### Complements
- [26-Design to Code](26-design-to-code.md) - Automated design handoff

### Leads To
- [07-Vertical Slice Dev](07-vertical-slice-dev.md) - Implementation planning
