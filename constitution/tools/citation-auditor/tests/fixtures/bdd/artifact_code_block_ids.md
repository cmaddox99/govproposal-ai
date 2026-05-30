---
title: Code Block Exclusion Fixture
---

This artifact tests T-07 code-block stripping (Phase 3 §4.3).

## Valid body citation

The ENG-3.5 naming law applies here.

## Fenced block — should be stripped

```python
# This is Python code — ENG-99.9 is in a fenced block and must NOT be extracted
def example():
    # ENG-0.0 also inside fenced block — must NOT be extracted
    return "law_id: ENG-99.9"
```

## Tilde fenced block — also stripped

~~~yaml
ENG-0.0: also inside tilde fence
~~~

## Inline code — should be stripped

Use `ENG-99.9` as the draft law placeholder (backtick-wrapped — must NOT be extracted).

## Multiline fenced block spanning many lines

```
Line 1
Line 2
Line 3 — ENG-0.0 buried in here
Line 4
Line 5
Line 6
Line 7
Line 8
Line 9
Line 10 — still inside fence
```

Only ENG-3.5 from the body should produce a result.
