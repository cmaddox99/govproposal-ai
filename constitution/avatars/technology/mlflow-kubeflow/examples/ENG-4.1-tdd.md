---
laws: [ENG-4.1]
avatar: [mlflow-kubeflow]
title: Atomic TDD — Python/MLflow-Kubeflow
---

# ENG-4.1: Atomic TDD — mlflow-kubeflow

Every production behaviour must be covered by a unit test written **before** the implementation.
Tests must run without network, database, or file-system dependencies.

## Example

```
def test_model_registration_increments_version():
    client = MlflowClient()
    v1 = register_model('risk-scorer', 'model.pkl')
    v2 = register_model('risk-scorer', 'model_v2.pkl')
    assert v2.version > v1.version
```

**Rule**: Each test verifies exactly one behaviour. No shared mutable state between tests.
