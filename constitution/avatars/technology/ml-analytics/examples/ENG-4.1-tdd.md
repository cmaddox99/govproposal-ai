---
laws: [ENG-4.1]
avatar: [ml-analytics]
title: Atomic TDD — Python/ML Analytics
---

# ENG-4.1: Atomic TDD — ml-analytics

Every production behaviour must be covered by a unit test written **before** the implementation.
Tests must run without network, database, or file-system dependencies.

## Example

```
def test_feature_pipeline_no_data_leakage():
    X_train, X_test = split_no_overlap(df)
    pipe = build_pipeline()
    pipe.fit(X_train)
    score = pipe.score(X_test)
    assert score >= 0.70
```

**Rule**: Each test verifies exactly one behaviour. No shared mutable state between tests.
