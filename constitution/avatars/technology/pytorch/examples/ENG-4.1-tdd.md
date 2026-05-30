---
laws: [ENG-4.1]
avatar: [pytorch]
title: Atomic TDD — Python/PyTorch
---

# ENG-4.1: Atomic TDD — pytorch

Every production behaviour must be covered by a unit test written **before** the implementation.
Tests must run without network, database, or file-system dependencies.

## Example

```
def test_loss_decreases_over_10_epochs():
    model = DelayPredictor()
    losses = train(model, mock_loader, epochs=10)
    assert losses[-1] < losses[0]
```

**Rule**: Each test verifies exactly one behaviour. No shared mutable state between tests.
