---
law_id: ENG-6.1
cpp_version_min: 23
cpp_version_note: >-
  std::hazard_pointer requires C++23. For C++11/14 projects, see
  ENG-6.1-lock-free-cpp14.md (boost::lockfree ABA version-counter pattern).
avatar: cpp
rag_exclude: true  # placeholder — content pending; excluded from RAG routing
---

# [ENG-6.1](laws/engineering/eng-6-security.md): `std::hazard_pointer` (C++23)

> **Status:** Stub — content to be added by a future ESE task.
> See `hangar-ai-specs/changes/cpp-external-sources-enrichment/tasks.md`.

Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design Law),
hazard pointers provide safe memory reclamation for lock-free data structures
without the ABA problem and without garbage collection.

## COMPLIANT

```cpp
// Placeholder — see ESE task for full content
```

> Placeholder — future ESE task.

## NON-COMPLIANT

> Placeholder — future ESE task.

## Edge Cases & Warnings

Per [ENG-6.1](laws/engineering/eng-6-security.md), hazard pointer retirement
lists and reclamation ordering are the primary hazards.

> Placeholder — future ESE task.
