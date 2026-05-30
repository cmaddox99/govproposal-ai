---
laws: [ENG-4.1]
avatar: [sagemaker]
title: Atomic TDD — Python/SageMaker
---

# ENG-4.1: Atomic TDD — sagemaker

Every production behaviour must be covered by a unit test written **before** the implementation.
Tests must run without network, database, or file-system dependencies.

## Example

```
def test_training_job_completes_under_budget():
    job = create_training_job(config=MOCK_CONFIG)
    wait_for_completion(job, timeout=120)
    assert job.status == 'Completed'
    assert job.billing_seconds < 7200
```

**Rule**: Each test verifies exactly one behaviour. No shared mutable state between tests.
