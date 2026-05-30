---
laws: [ENG-4.1]
avatar: [vector-databases]
title: Atomic TDD — Python/Vector DB
---

# ENG-4.1: Atomic TDD — vector-databases

Every production behaviour must be covered by a unit test written **before** the implementation.
Tests must run without network, database, or file-system dependencies.

## Example

```
def test_similarity_search_returns_relevant_laws():
    db = VectorDB(index='constitution')
    results = db.search('passenger refund DOT', top_k=3)
    law_ids = [r.metadata['law_id'] for r in results]
    assert 'BUS-2.3' in law_ids
```

**Rule**: Each test verifies exactly one behaviour. No shared mutable state between tests.
