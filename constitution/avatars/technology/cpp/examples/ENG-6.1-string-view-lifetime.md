---
law_id: ENG-6.1
cpp_version_min: 17
cpp_version_note: >-
  std::string_view requires C++17. Lifetime rules are identical to
  const char* — see ENG-6.1-const-char-lifetime.md for the C++03/pre-C++17
  version of these traps.
avatar: cpp
rag_exclude: true  # placeholder — content pending; excluded from RAG routing
---

# [ENG-6.1](laws/engineering/eng-6-security.md): `std::string_view` Lifetime Traps (C++17)

> **Status:** Stub — content to be added by a future ESE task.
> See `hangar-ai-specs/changes/cpp-external-sources-enrichment/tasks.md`.

Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design Law),
`std::string_view` lifetime hazards cause undefined behavior identically to
`const char*` dangling pointer bugs.

## COMPLIANT

```cpp
// Placeholder — see ESE task for full content
```

> Placeholder — future ESE task.

## NON-COMPLIANT

> Placeholder — future ESE task.

## Edge Cases & Warnings

Per [ENG-6.1](laws/engineering/eng-6-security.md), SSO and reallocation
hazards from ENG-6.1-const-char-lifetime.md apply equally here.

> Placeholder — future ESE task.
