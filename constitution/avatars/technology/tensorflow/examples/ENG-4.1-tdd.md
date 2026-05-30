---
laws: [ENG-4.1]
avatar: [tensorflow]
title: Atomic TDD — Python/TensorFlow
---

# ENG-4.1: Atomic TDD — tensorflow

Every production behaviour must be covered by a unit test written **before** the implementation.
Tests must run without network, database, or file-system dependencies.

## Example

```
def test_model_prediction_within_confidence_interval():
    model = load_model('delay-predictor')
    preds = model.predict(X_test[:100])
    assert np.mean(np.abs(preds - y_test[:100])) < 15  # <15 min MAE
```

**Rule**: Each test verifies exactly one behaviour. No shared mutable state between tests.
