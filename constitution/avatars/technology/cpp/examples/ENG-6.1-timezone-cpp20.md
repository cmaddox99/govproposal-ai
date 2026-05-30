---
law_id: ENG-6.1
cpp_version_min: 20
cpp_version_note: >-
  std::chrono::zoned_time requires C++20. For C++11/14 projects, see
  ENG-6.1-timezone-cpp14.md (HowardHinnant/date bridge, identical API).
  FAR 117 crew rest requires timezone-aware arithmetic in all versions.
avatar: cpp
rag_exclude: true  # placeholder — content pending; excluded from RAG routing
---

# [ENG-6.1](laws/engineering/eng-6-security.md): `std::chrono::zoned_time` (C++20)

> **Status:** Stub — content to be added by ESE-47.
> See `hangar-ai-specs/changes/cpp-external-sources-enrichment/tasks.md`.

Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design Law),
FAR 117 crew rest calculations must use timezone-aware time arithmetic.

## COMPLIANT

```cpp
// Placeholder — see ESE task for full content
```

> Placeholder — see ESE-47.

## NON-COMPLIANT

> Placeholder — see ESE-47.

## Edge Cases & Warnings

Per [ENG-6.1](laws/engineering/eng-6-security.md), DST transitions and leap
seconds are the primary hazards for aviation scheduling calculations.

> Placeholder — see ESE-47.
