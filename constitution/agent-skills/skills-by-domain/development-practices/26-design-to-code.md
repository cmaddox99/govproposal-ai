---
skill:
  id: skill-26-design-to-code
  name: Design to Code
  category: design
  version: "2.0.0"

laws:
  implements:
    - id: ENG-2.3
      title: Vertical Slice Architecture Law
    - id: PRD-3.4
      title: Acceptance Criteria Law
  references:
    - id: ENG-4.1
      title: Atomic TDD Law
    - id: ENG-3.1
      title: Complexity Limits

triggers:
  phrases:
    - "Convert design to code"
    - "Figma to React"
    - "Generate components"
    - "Design handoff"

followed_by:
  - skill-06-atomic-tdd
  - skill-08-code-review
---

# Skill 26: Design to Code

> **Purpose:** Guide AI agents in automated design-to-code workflows using tools like Locofy, Figma MCP, and design handoff automation.

---

## Overview

This skill enables AI agents to bridge the gap between design and development, automating the translation of Figma designs into production-ready code while maintaining design fidelity and code quality.

### Key Capabilities
1. **Figma MCP integration** - Direct Figma access via Model Context Protocol
2. **Locofy workflows** - AI-powered design-to-code conversion
3. **Code generation** - React, Vue, HTML/CSS from designs
4. **Design token extraction** - Automated style guide generation
5. **Component mapping** - Design components to code components

---

## Constitutional Compliance

### Engineering Constitution
- **Article II, Section 2.1** - Simplicity: Generated code follows established patterns
- **Article III, Section 3.1** - Quality: Generated code meets quality standards
- **Article IV, Section 4.1** - Test-First: Generated components have test coverage
- **Article IV, Section 4.2** - Test Pyramid: Appropriate testing at each level

### Product Constitution
- **Article III, Section 3.2** - Acceptance Criteria: Design specs translate to tests
- **Article IV, Section 4.1** - Velocity: Accelerate design-to-implementation cycle

### Business Constitution
- **Article V, Section 5.1** - Accessibility: Generated code is accessible
- **Article II, Section 2.1** - Cost Management: Reduce manual translation effort

---

## Figma MCP Integration

### Setup and Configuration

```markdown
## Figma MCP Configuration

### Prerequisites
- Figma account with API access
- MCP server configured
- Design file with proper structure

### MCP Server Setup
```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "@anthropic/figma-mcp"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "${FIGMA_ACCESS_TOKEN}"
      }
    }
  }
}
```

### Available MCP Tools
- `figma_get_file` - Retrieve file structure
- `figma_get_node` - Get specific node details
- `figma_get_styles` - Extract design tokens
- `figma_get_components` - List components
- `figma_export_assets` - Export images/icons
```

### Figma API Patterns

```typescript
// Figma file structure navigation
interface FigmaNode {
  id: string;
  name: string;
  type: 'FRAME' | 'COMPONENT' | 'INSTANCE' | 'TEXT' | 'RECTANGLE' | 'GROUP';
  children?: FigmaNode[];
  absoluteBoundingBox?: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
  fills?: Paint[];
  strokes?: Paint[];
  effects?: Effect[];
  style?: TypeStyle;
}

// Extract component from Figma
async function extractComponent(fileKey: string, nodeId: string): Promise<ComponentSpec> {
  const node = await figma.getNode(fileKey, nodeId);

  return {
    name: node.name,
    type: mapNodeType(node.type),
    styles: extractStyles(node),
    children: node.children?.map(extractComponent),
    variants: extractVariants(node),
  };
}
```

---

## Locofy Workflow

### Project Setup

```markdown
## Locofy Configuration

### 1. Install Locofy Plugin
- Install Locofy plugin in Figma
- Connect to Locofy account
- Configure project settings

### 2. Prepare Figma File
- Use Auto Layout throughout
- Name layers meaningfully
- Apply consistent variants
- Tag interactive elements

### 3. Configure Code Settings
```json
{
  "framework": "react",
  "styling": "tailwind",
  "typescript": true,
  "componentLibrary": "custom",
  "outputPath": "./src/components",
  "naming": "PascalCase"
}
```
```

### Design Tagging for Locofy

```markdown
## Locofy Tagging Guidelines

### Component Tags
| Tag | Purpose | Example |
|-----|---------|---------|
| `#component` | Mark as reusable component | Button, Card |
| `#page` | Mark as full page | HomePage, Dashboard |
| `#section` | Mark as page section | Header, Footer |
| `#input` | Interactive input | TextField, Select |
| `#button` | Clickable button | Submit, Cancel |
| `#link` | Navigation link | NavItem, Breadcrumb |
| `#list` | Repeating items | ProductList, Menu |
| `#modal` | Overlay component | Dialog, Drawer |

### State Tags
| Tag | Purpose |
|-----|---------|
| `#default` | Default state |
| `#hover` | Hover state |
| `#active` | Active/pressed state |
| `#disabled` | Disabled state |
| `#loading` | Loading state |
| `#error` | Error state |

### Responsive Tags
| Tag | Purpose |
|-----|---------|
| `#desktop` | Desktop layout |
| `#tablet` | Tablet layout |
| `#mobile` | Mobile layout |
```

---

## Code Generation Patterns

### React Component Generation

```typescript
// Input: Figma component specification
interface FigmaComponentSpec {
  name: string;
  variants: Variant[];
  props: PropDefinition[];
  styles: StyleDefinition;
  children: FigmaComponentSpec[];
}

// Output: Generated React component
function generateReactComponent(spec: FigmaComponentSpec): string {
  return `
import React from 'react';
import { cn } from '@/lib/utils';

export interface ${spec.name}Props {
  ${spec.props.map(p => `${p.name}${p.required ? '' : '?'}: ${p.type};`).join('\n  ')}
  className?: string;
}

export const ${spec.name}: React.FC<${spec.name}Props> = ({
  ${spec.props.map(p => p.name).join(',\n  ')},
  className,
}) => {
  return (
    <${spec.element}
      className={cn(
        "${spec.styles.base}",
        ${generateVariantStyles(spec.variants)},
        className
      )}
      ${generateProps(spec)}
    >
      ${generateChildren(spec.children)}
    </${spec.element}>
  );
};

${spec.name}.displayName = '${spec.name}';
  `.trim();
}
```

### Tailwind CSS Extraction

```typescript
// Convert Figma styles to Tailwind classes
function figmaToTailwind(node: FigmaNode): string[] {
  const classes: string[] = [];

  // Spacing
  if (node.paddingLeft) classes.push(`pl-${spacingScale(node.paddingLeft)}`);
  if (node.paddingRight) classes.push(`pr-${spacingScale(node.paddingRight)}`);
  if (node.paddingTop) classes.push(`pt-${spacingScale(node.paddingTop)}`);
  if (node.paddingBottom) classes.push(`pb-${spacingScale(node.paddingBottom)}`);
  if (node.itemSpacing) classes.push(`gap-${spacingScale(node.itemSpacing)}`);

  // Layout
  if (node.layoutMode === 'HORIZONTAL') classes.push('flex', 'flex-row');
  if (node.layoutMode === 'VERTICAL') classes.push('flex', 'flex-col');
  if (node.primaryAxisAlignItems === 'CENTER') classes.push('justify-center');
  if (node.counterAxisAlignItems === 'CENTER') classes.push('items-center');

  // Sizing
  if (node.layoutSizingHorizontal === 'FILL') classes.push('w-full');
  if (node.layoutSizingVertical === 'FILL') classes.push('h-full');

  // Colors
  if (node.fills?.[0]?.type === 'SOLID') {
    const color = rgbToHex(node.fills[0].color);
    classes.push(`bg-[${color}]`);
  }

  // Border radius
  if (node.cornerRadius) classes.push(`rounded-${radiusScale(node.cornerRadius)}`);

  return classes;
}
```

### Design Token Generation

```typescript
// Extract design tokens from Figma styles
interface DesignTokens {
  colors: Record<string, string>;
  typography: Record<string, TypographyToken>;
  spacing: Record<string, string>;
  shadows: Record<string, string>;
  radii: Record<string, string>;
}

async function extractDesignTokens(fileKey: string): Promise<DesignTokens> {
  const styles = await figma.getStyles(fileKey);

  const tokens: DesignTokens = {
    colors: {},
    typography: {},
    spacing: {},
    shadows: {},
    radii: {},
  };

  // Extract color styles
  styles.filter(s => s.styleType === 'FILL').forEach(style => {
    const color = style.fills[0];
    if (color.type === 'SOLID') {
      tokens.colors[toTokenName(style.name)] = rgbToHex(color.color);
    }
  });

  // Extract text styles
  styles.filter(s => s.styleType === 'TEXT').forEach(style => {
    tokens.typography[toTokenName(style.name)] = {
      fontFamily: style.fontFamily,
      fontSize: `${style.fontSize}px`,
      fontWeight: style.fontWeight,
      lineHeight: style.lineHeightPercent ? `${style.lineHeightPercent}%` : 'normal',
      letterSpacing: style.letterSpacing ? `${style.letterSpacing}px` : 'normal',
    };
  });

  // Extract effect styles (shadows)
  styles.filter(s => s.styleType === 'EFFECT').forEach(style => {
    const shadow = style.effects.find(e => e.type === 'DROP_SHADOW');
    if (shadow) {
      tokens.shadows[toTokenName(style.name)] =
        `${shadow.offset.x}px ${shadow.offset.y}px ${shadow.radius}px ${rgbaToString(shadow.color)}`;
    }
  });

  return tokens;
}

// Output as CSS custom properties
function tokensToCSS(tokens: DesignTokens): string {
  return `
:root {
  /* Colors */
  ${Object.entries(tokens.colors).map(([k, v]) => `--color-${k}: ${v};`).join('\n  ')}

  /* Spacing */
  ${Object.entries(tokens.spacing).map(([k, v]) => `--spacing-${k}: ${v};`).join('\n  ')}

  /* Shadows */
  ${Object.entries(tokens.shadows).map(([k, v]) => `--shadow-${k}: ${v};`).join('\n  ')}

  /* Border Radius */
  ${Object.entries(tokens.radii).map(([k, v]) => `--radius-${k}: ${v};`).join('\n  ')}
}
  `.trim();
}
```

---

## Component Mapping

### Design to Code Component Map

```yaml
# component-map.yaml
mappings:
  # Buttons
  "Button/Primary":
    component: "@/components/ui/Button"
    props:
      variant: "primary"

  "Button/Secondary":
    component: "@/components/ui/Button"
    props:
      variant: "secondary"

  "Button/Ghost":
    component: "@/components/ui/Button"
    props:
      variant: "ghost"

  # Form elements
  "Input/Text":
    component: "@/components/ui/Input"
    props:
      type: "text"

  "Input/Password":
    component: "@/components/ui/Input"
    props:
      type: "password"

  "Select/Default":
    component: "@/components/ui/Select"

  # Layout
  "Card/Default":
    component: "@/components/ui/Card"

  "Modal/Default":
    component: "@/components/ui/Dialog"

  # Navigation
  "NavItem/Default":
    component: "@/components/ui/NavLink"
```

### Automated Component Resolution

```typescript
// Resolve Figma component to code component
async function resolveComponent(
  figmaComponent: string,
  mappings: ComponentMappings
): Promise<CodeComponent> {
  // Exact match
  if (mappings[figmaComponent]) {
    return mappings[figmaComponent];
  }

  // Variant match (Button/Primary/Hover -> Button/Primary)
  const baseName = figmaComponent.split('/').slice(0, 2).join('/');
  if (mappings[baseName]) {
    return mappings[baseName];
  }

  // Category match (Button/* -> Button)
  const category = figmaComponent.split('/')[0];
  if (mappings[category]) {
    return mappings[category];
  }

  // Generate new component
  return generateNewComponent(figmaComponent);
}
```

---

## Quality Assurance

### Generated Code Review Checklist

```markdown
## Generated Code Review

### Structure
- [ ] Component follows project conventions
- [ ] Proper TypeScript types defined
- [ ] Props interface is complete
- [ ] Default props are sensible

### Styling
- [ ] Uses design system tokens
- [ ] Responsive breakpoints correct
- [ ] No hardcoded values
- [ ] Tailwind classes optimized

### Accessibility
- [ ] Semantic HTML elements
- [ ] ARIA labels where needed
- [ ] Keyboard navigation works
- [ ] Focus management correct

### Performance
- [ ] No unnecessary re-renders
- [ ] Images optimized
- [ ] Lazy loading where appropriate

### Testing
- [ ] Unit tests generated
- [ ] Visual regression baseline
- [ ] Accessibility tests included
```

### Test Generation

```typescript
// Generate tests for component
function generateComponentTests(spec: ComponentSpec): string {
  return `
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ${spec.name} } from './${spec.name}';

describe('${spec.name}', () => {
  it('renders without crashing', () => {
    render(<${spec.name} ${generateTestProps(spec)} />);
    expect(screen.getByRole('${spec.role}')).toBeInTheDocument();
  });

  ${spec.variants.map(v => `
  it('renders ${v.name} variant correctly', () => {
    render(<${spec.name} variant="${v.name}" ${generateTestProps(spec)} />);
    expect(screen.getByRole('${spec.role}')).toHaveClass('${v.className}');
  });
  `).join('\n')}

  ${spec.interactive ? `
  it('handles click events', async () => {
    const onClick = jest.fn();
    render(<${spec.name} onClick={onClick} ${generateTestProps(spec)} />);

    await userEvent.click(screen.getByRole('${spec.role}'));
    expect(onClick).toHaveBeenCalledTimes(1);
  });
  ` : ''}

  it('applies custom className', () => {
    render(<${spec.name} className="custom-class" ${generateTestProps(spec)} />);
    expect(screen.getByRole('${spec.role}')).toHaveClass('custom-class');
  });

  // Accessibility tests
  it('meets accessibility requirements', async () => {
    const { container } = render(<${spec.name} ${generateTestProps(spec)} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
  `.trim();
}
```

---

## Workflow Integration

### Design-to-Code Pipeline

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Figma      │     │   Process    │     │   Output     │
│              │     │              │     │              │
│ Design File  │ ──► │ Extract      │ ──► │ Components   │
│ Components   │     │ Transform    │     │ Tokens       │
│ Styles       │     │ Generate     │     │ Tests        │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │   Review     │
                    │              │
                    │ Code Review  │
                    │ Visual QA    │
                    │ A11y Check   │
                    └──────────────┘
```

### Integration with Hangar SDD

```markdown
## Hangar SDD Integration

When generating code from designs:

1. **Create Change**: `/opsx:new ui-[component-name]`

2. **Link Design**: Add Figma link to change.md
   ```markdown
   ## References
   - Figma: [Link to design]
   - Component: [Node ID]
   ```

3. **Generate Code**: Use design-to-code tools

4. **Add Tests**: Ensure test coverage

5. **Review**: Follow code review skill

6. **Archive**: `/opsx:archive` when complete
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Blind acceptance of generated code | Quality issues | Always review and refine |
| Ignoring design system | Inconsistency | Map to existing components |
| Skipping accessibility | Exclusion, legal risk | Include a11y in generation |
| No test generation | Unverified code | Generate tests with components |
| Manual token updates | Drift between design/code | Automate token sync |
| One-way generation | No feedback loop | Review and iterate |

---

## Skill Relationships

### Prerequisites
- [25-UX Design](25-ux-design.md) - Design system and Figma workflows

### Complements
- [06-Atomic TDD](06-atomic-tdd.md) - Test-first refinement
- [08-Code Review](08-code-review.md) - Quality verification

### Leads To
- [07-Vertical Slice Dev](07-vertical-slice-dev.md) - Feature implementation
