---
skill:
  id: skill-28-content-transformation
  name: Content Transformation
  category: design
  version: "1.0.0"

laws:
  implements:
    - id: PRD-3.4
      title: Acceptance Criteria Law
    - id: ENG-2.3
      title: Vertical Slice Architecture Law
  references:
    - id: BUS-7.1
      title: Audit Trail Law
    - id: ENG-4.1
      title: Atomic TDD Law
    - id: PRD-5.1
      title: MVP Law

triggers:
  phrases:
    - "Transform presentation"
    - "Convert slides to brand"
    - "Apply brand standards"
    - "Document transformation"
    - "Migrate content format"
    - "Standardize documents"

followed_by:
  - skill-25-ux-design
  - skill-21-prompt-engineering
  - skill-16-documentation
---

# Skill 28: Content Transformation

> **Purpose:** Guide AI agents in transforming documents and presentations to comply with brand/design standards while preserving content integrity.

---

## Overview

This skill enables AI agents to automate the transformation of documents (PowerPoint, Word, etc.) from arbitrary styling to organization-defined brand standards.

### Key Capabilities

1. **Brand standard extraction** - Parse template documents to extract design rules
2. **Content analysis** - Identify content types, structure, and current styling
3. **Style mapping** - Map source styles to brand-compliant equivalents
4. **Content-preserving transformation** - Apply changes without losing content
5. **Diff generation** - Create before/after comparisons for review
6. **Human-in-the-loop workflow** - Enable review and approval

---

## Constitutional Compliance

### Engineering Constitution
- **Article II, Section 2.3** - Vertical Slice: Transform one element type at a time
- **Article IV, Section 4.1** - Test-First: Transformation rules tested before implementation
- **Article III, Section 3.1** - Complexity Limits: Single-responsibility transformers

### Product Constitution
- **Article III, Section 3.4** - Acceptance Criteria: Clear rules for "brand compliant"
- **Article V, Section 5.1** - MVP: Start with most common transformation cases

### Business Constitution
- **Article VII, Section 7.1** - Audit Trail: Log all transformations for compliance

---

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│             CONTENT TRANSFORMATION WORKFLOW                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. EXTRACT        Extract brand rules from template             │
│       │                                                          │
│       ▼                                                          │
│  2. ANALYZE        Parse source content, identify elements       │
│       │                                                          │
│       ▼                                                          │
│  3. MAP            Create source-to-brand mapping                │
│       │                                                          │
│       ▼                                                          │
│  4. TRANSFORM      Apply transformations preserving content      │
│       │                                                          │
│       ▼                                                          │
│  5. DIFF           Generate before/after comparison              │
│       │                                                          │
│       ▼                                                          │
│  6. REVIEW         Human reviews and approves changes            │
│       │                                                          │
│       ▼                                                          │
│  7. EXPORT         Generate final compliant output               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Brand Rule Extraction

### Template Analysis

```python
# Example: Extract brand rules from Gold Standard template

def extract_brand_rules(template_path: str) -> BrandRules:
    """
    Parse template document and extract design tokens.
    
    Returns:
        BrandRules containing colors, fonts, layouts, etc.
    """
    template = parse_document(template_path)
    
    return BrandRules(
        colors=extract_color_palette(template),
        fonts=extract_font_definitions(template),
        layouts=extract_layout_patterns(template),
        spacing=extract_spacing_rules(template),
        components=extract_component_styles(template)
    )
```

### Brand Rules Schema

```yaml
# brand-rules.yaml
version: "1.0.0"
extracted_from: "Gold-Standard.pptx"
extracted_date: "2026-02-04"

colors:
  primary:
    - name: "AA Blue"
      hex: "#0078D4"
      rgb: [0, 120, 212]
      usage: "Headers, primary buttons"
    - name: "AA Red"
      hex: "#C8102E"
      rgb: [200, 16, 46]
      usage: "Accents, alerts"
  
  background:
    - name: "White"
      hex: "#FFFFFF"
    - name: "Light Gray"
      hex: "#F5F5F5"
  
  text:
    - name: "Dark"
      hex: "#1A1A1A"
    - name: "Muted"
      hex: "#666666"

fonts:
  heading:
    family: "American Sans"
    fallback: "Arial, sans-serif"
    sizes:
      h1: 44
      h2: 32
      h3: 24
  
  body:
    family: "American Sans"
    fallback: "Arial, sans-serif"
    sizes:
      regular: 18
      small: 14

layouts:
  title_slide:
    logo_position: "top-right"
    title_position: "center"
    
  content_slide:
    header_height: 80
    margin: 40
    
spacing:
  base: 8
  scale: [8, 16, 24, 32, 48, 64]
```

---

## Content Analysis

### Element Detection

```python
# Example: Analyze source document elements

def analyze_content(source_path: str) -> ContentAnalysis:
    """
    Parse source document and identify transformable elements.
    """
    doc = parse_document(source_path)
    
    return ContentAnalysis(
        slides=[analyze_slide(s) for s in doc.slides],
        colors=detect_colors_used(doc),
        fonts=detect_fonts_used(doc),
        images=detect_images(doc),
        charts=detect_charts(doc)
    )

def analyze_slide(slide) -> SlideAnalysis:
    return SlideAnalysis(
        layout_type=detect_layout(slide),
        elements=[
            Element(
                type=detect_type(el),
                content=extract_content(el),
                current_style=extract_style(el),
                position=extract_position(el)
            )
            for el in slide.elements
        ]
    )
```

---

## Style Mapping

### Color Mapping Strategy

```python
# Map non-brand colors to nearest brand equivalent

def create_color_mapping(
    source_colors: List[Color],
    brand_colors: BrandColors
) -> Dict[Color, Color]:
    """
    Create mapping from source colors to brand palette.
    
    Strategy:
    1. Exact match - use directly
    2. Similar match - map to nearest
    3. No match - suggest based on usage context
    """
    mapping = {}
    
    for source in source_colors:
        # Try exact match
        if exact := find_exact_match(source, brand_colors):
            mapping[source] = exact
            continue
        
        # Find nearest by color distance
        nearest = find_nearest_color(source, brand_colors)
        mapping[source] = nearest
    
    return mapping
```

### Font Mapping Strategy

```python
def create_font_mapping(
    source_fonts: List[Font],
    brand_fonts: BrandFonts
) -> Dict[Font, Font]:
    """
    Map source fonts to brand equivalents.
    
    Strategy:
    1. Preserve size hierarchy
    2. Map to appropriate brand font family
    3. Adjust sizes proportionally
    """
    mapping = {}
    
    for source in source_fonts:
        target_family = brand_fonts.get_equivalent(source.family)
        target_size = adjust_size(source.size, brand_fonts.scale)
        
        mapping[source] = Font(
            family=target_family,
            size=target_size,
            weight=source.weight,
            style=source.style
        )
    
    return mapping
```

---

## Transformation Engine

### Transformation Rules

```python
class TransformationEngine:
    """
    Apply brand transformations while preserving content.
    """
    
    def __init__(self, brand_rules: BrandRules):
        self.brand = brand_rules
        self.color_mapper = ColorMapper(brand_rules.colors)
        self.font_mapper = FontMapper(brand_rules.fonts)
        self.layout_adjuster = LayoutAdjuster(brand_rules.layouts)
    
    def transform(self, source: Document) -> TransformResult:
        """
        Transform source document to brand standards.
        
        Returns:
            TransformResult with transformed doc and change log
        """
        changes = ChangeLog()
        output = source.copy()
        
        # Transform colors
        for element in output.get_colored_elements():
            old_color = element.fill_color
            new_color = self.color_mapper.map(old_color)
            if old_color != new_color:
                element.fill_color = new_color
                changes.add(ColorChange(element, old_color, new_color))
        
        # Transform fonts
        for text_element in output.get_text_elements():
            old_font = text_element.font
            new_font = self.font_mapper.map(old_font)
            if old_font != new_font:
                text_element.font = new_font
                changes.add(FontChange(text_element, old_font, new_font))
        
        # Adjust layouts
        for slide in output.slides:
            layout_changes = self.layout_adjuster.adjust(slide)
            changes.extend(layout_changes)
        
        return TransformResult(
            document=output,
            change_log=changes,
            summary=self.summarize(changes)
        )
```

---

## Diff Generation

### Before/After Comparison

```python
def generate_diff(
    original: Document,
    transformed: Document,
    change_log: ChangeLog
) -> DiffReport:
    """
    Generate visual and textual diff of changes.
    """
    return DiffReport(
        slides=[
            SlideDiff(
                slide_number=i+1,
                before_image=render_slide(orig),
                after_image=render_slide(trans),
                changes=change_log.for_slide(i)
            )
            for i, (orig, trans) in enumerate(
                zip(original.slides, transformed.slides)
            )
        ],
        summary=DiffSummary(
            total_changes=len(change_log),
            color_changes=len(change_log.color_changes),
            font_changes=len(change_log.font_changes),
            layout_changes=len(change_log.layout_changes)
        )
    )
```

---

## Human-in-the-Loop Review

### Review Interface Requirements

```markdown
## Review UI Requirements

### Must Have
- [ ] Side-by-side before/after view
- [ ] Zoom and pan capability
- [ ] Change list with jump-to
- [ ] Approve/reject per change
- [ ] Bulk approve category
- [ ] Export approved version

### Nice to Have
- [ ] Manual override option
- [ ] Comment on changes
- [ ] Save review state
- [ ] Undo/redo in preview
```

---

## Supported Formats

| Format | Extension | Library | Status |
|--------|-----------|---------|--------|
| PowerPoint | .pptx | python-pptx | ✅ Supported |
| Word | .docx | python-docx | 🔄 Planned |
| PDF | .pdf | PyPDF2, reportlab | 🔄 Planned |
| Google Slides | - | Google API | 🔄 Planned |

---

## Testing Requirements

Per ENG-4.1 (Atomic TDD), all transformation logic must be tested:

```python
# Example test structure

class TestColorMapper:
    def test_exact_match_returns_brand_color(self):
        brand = BrandColors([Color("#0078D4", "AA Blue")])
        mapper = ColorMapper(brand)
        
        result = mapper.map(Color("#0078D4"))
        
        assert result.hex == "#0078D4"
    
    def test_similar_color_maps_to_nearest(self):
        brand = BrandColors([Color("#0078D4", "AA Blue")])
        mapper = ColorMapper(brand)
        
        result = mapper.map(Color("#0070C0"))  # Similar blue
        
        assert result.hex == "#0078D4"  # Maps to brand blue

class TestTransformationEngine:
    def test_content_preserved_after_transformation(self):
        engine = TransformationEngine(brand_rules)
        source = create_test_document("Hello World")
        
        result = engine.transform(source)
        
        assert extract_all_text(result.document) == "Hello World"
```

---

## Metrics & Observability

Per ENG-5.5, transformations should be observable:

```yaml
# Metrics to track
metrics:
  - name: transformation_duration_seconds
    type: histogram
    labels: [document_type, slide_count]
    
  - name: changes_applied_total
    type: counter
    labels: [change_type]
    
  - name: human_overrides_total
    type: counter
    labels: [change_type, override_reason]
    
  - name: transformation_errors_total
    type: counter
    labels: [error_type]
```

---

## AI Integration Points

This skill integrates with **skill-21-prompt-engineering** for:

1. **Content type detection** - "Is this a header or body text?"
2. **Layout suggestions** - "Recommend layout for this content"
3. **Edge case handling** - "How should I transform this unusual element?"

Example prompt template:

```python
CONTENT_TYPE_PROMPT = """
You are analyzing a PowerPoint slide element.

Element details:
- Text content: {text}
- Font size: {font_size}
- Position: {position}
- Slide context: {slide_context}

Classify this element as one of:
- TITLE: Main slide title
- SUBTITLE: Secondary heading
- HEADING: Section heading
- BODY: Regular body text
- CAPTION: Image caption or footnote
- LABEL: Chart/diagram label

Respond with just the classification.
"""
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| skill-25-ux-design | Design system concepts |
| skill-26-design-to-code | Similar transformation patterns |
| skill-21-prompt-engineering | AI-assisted decisions |
| skill-16-documentation | Documenting brand rules |

---

## Example Usage

```bash
# CLI usage example
slide-transformer transform \
  --template Gold-Standard.pptx \
  --input Raw-Dirty.pptx \
  --output Transformed.pptx \
  --diff-report diff.html

# Python API usage
from slide_transformer import TransformationEngine, BrandRules

rules = BrandRules.from_template("Gold-Standard.pptx")
engine = TransformationEngine(rules)

result = engine.transform("Raw-Dirty.pptx")
result.save("Transformed.pptx")
result.generate_diff("diff.html")
```
