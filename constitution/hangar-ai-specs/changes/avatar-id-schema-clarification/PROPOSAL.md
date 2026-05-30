# Proposal: Avatar ID Format Schema Clarification

**Proposal ID:** avatar-id-schema-clarification
**Submitted:** April 15, 2026
**Status:** 🟡 ACTIVE — schema clarification, no breaking changes
**Branch:** `feat/avatar-id-schema-clarification`
**Scope:** `docs/guides/avatar-model-schema.md §3` and `workflows/avatar-workflow.md §Phase 2`

---

## Laws Cited (ENG-11.2 Compliance)

| Law ID | Title | Relevance |
|--------|-------|-----------|
| [ENG-11.1](laws/engineering/eng-11-hangar-sdd.md) | Hangar SDD Law | Governs proposal lifecycle |
| [ENG-10.1](laws/engineering/eng-10-constitution.md) | Constitution Compliance | Schema §3 defines the `avatar.id` format rule |
| [ENG-6.7](laws/engineering/eng-6-security.md) | Audit Trail Law | Schema changes must be traceable |

---

## Problem Statement

`avatar-model-schema.md §3` specifies:

```yaml
avatar:
  id: avatar-{type}-{domain-slug}      # must match directory name exactly
```

However, **46 of 46 deployed avatars** do **not** follow this pattern consistently:

| Pattern | Count | Examples |
|---------|-------|---------|
| `avatar-{type}-{slug}` (schema literal) | 19 | `avatar-technology-cpp`, `avatar-product-loyalty`, `avatar-industry-aviation-faa` |
| `avatar-{slug}` (no type prefix) | 27 | `avatar-java-spring`, `avatar-angular`, `avatar-dotnet-core` |

The 27 avatars using `avatar-{slug}` technically violate the schema literal `avatar-{type}-{domain-slug}`, but the `avatars/index.yaml` and `AVATAR-RAG-INDEX.yaml` entries for all 27 are self-consistent — the violation is only between the manifest and the schema comment, not between the manifest and the registry.

Additionally, the avatar-workflow Phase 2 Step 2.1 check states:
> `avatar.id matches directory slug exactly`

For a C++ avatar at `avatars/technology/cpp/`, "exactly" is ambiguous: does it mean `avatar-cpp` (just the slug) or `avatar-technology-cpp` (type + slug)? Both plausibly "match" the directory.

### Evidence
- Surfaced during avatar-scan-cpp.md §1.2 review (PR #14)
- 59% of avatars (27/46) use the `avatar-{slug}` pattern
- All 19 product-type and industry avatars use `avatar-{type}-{slug}`
- Technology avatars are split: 4 use `avatar-technology-{slug}`, 23 use `avatar-{slug}`

---

## Root Cause

The schema was written before the full avatar registry existed. The comment `avatar-{type}-{domain-slug}` was intended as a template but was never enforced uniformly. As product-type and industry avatars were created first (they needed domain namespacing to avoid slug collisions), they adopted the full-qualified form. Many technology avatars were created later and used the shorter form, which is unambiguous in the technology directory.

---

## Proposed Solution: Dual-Pattern Allowlist

Update `avatar-model-schema.md §3` to explicitly permit both patterns, with a clear recommendation:

### Canonical Form (Recommended for new avatars)

```yaml
avatar:
  id: avatar-{type}-{domain-slug}
```

**Examples:** `avatar-technology-cpp`, `avatar-product-loyalty`, `avatar-industry-aviation-faa`

**When to use:** Always for product-type and industry avatars (slug collision risk). Recommended for new technology avatars.

### Legacy Form (Permitted for existing avatars)

```yaml
avatar:
  id: avatar-{domain-slug}
```

**Examples:** `avatar-java-spring`, `avatar-angular`, `avatar-dotnet-core`

**When to use:** Existing avatars that already use this form. Do NOT rename — it would break `index.yaml`, `AVATAR-RAG-INDEX.yaml`, and all associated tests.

### Validation Rule

The `avatar.id` is **valid** if it satisfies:
```
avatar.id starts with "avatar-"
AND
avatar.id contains the directory slug (exact substring match)
AND
avatar.id is registered in avatars/index.yaml
```

The avatar-workflow Phase 2 Step 2.1 check should be updated to use this rule rather than an exact slug match.

---

## Deliverables

| # | Artifact | Description | Status |
|---|----------|-------------|--------|
| D1 | `docs/guides/avatar-model-schema.md §3` | Update `avatar.id` format definition with dual-pattern allowlist | ⬜ Pending |
| D2 | `workflows/avatar-workflow.md §Phase 2 Step 2.1` | Update `avatar.id matches directory slug exactly` check to use new validation rule | ⬜ Pending |
| D3 | `hangar-ai-specs/README.md` | Register proposal in active proposals table | ⬜ Pending |

> **No avatar manifest files need to change.** This is a schema clarification, not a data migration. All 46 existing avatars remain valid under the new dual-pattern rule.

---

## Success Criteria

| Criterion | Measurement |
|-----------|-------------|
| Both patterns explicitly documented | Schema §3 has a table showing both forms with examples |
| Validation rule is unambiguous | Phase 2 Step 2.1 check updated with clear matching logic |
| No existing avatars broken | All 46 avatars remain valid; no `id:` fields changed |
| Constitution lint still passes | `aa-constitution-lint .` → 17/17 pass |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Future avatars choose wrong pattern | Medium | Low | Schema now has explicit guidance: canonical form for new avatars |
| Schema clarification triggers mass-rename | Low | High | Proposal explicitly prohibits renaming existing avatars |
| Workflow validation becomes too permissive | Low | Low | New rule still requires `starts with "avatar-"` and `registered in index.yaml` |

---

## Non-Breaking Guarantee

This proposal makes **zero changes** to:
- Any `avatar/**/manifest.yaml` file
- `avatars/index.yaml`
- `AVATAR-RAG-INDEX.yaml`
- Any test file

Only `docs/guides/avatar-model-schema.md §3` and `workflows/avatar-workflow.md §Phase 2` are modified.

---

## Relationship to Other Proposals

| Proposal | Relationship |
|----------|-------------|
| `cpp-avatar-manifest-restructure` (PR #14) | This proposal closes the avatar.id advisory documented in that proposal's Proposal C section |
| `cpp-manifest-token-exception` (PR #30) | Independent — no relationship |

---

## Evidence Sources

- [High confidence] Automated analysis of all 46 `avatars/*/*/manifest.yaml` files: 27 use `avatar-{slug}`, 19 use `avatar-{type}-{slug}`
- [High confidence] `avatars/index.yaml` and `AVATAR-RAG-INDEX.yaml` are self-consistent for all 46 avatars under their current `id:` values
- [Medium confidence] Avatar-workflow Phase 2 Step 2.1 check is ambiguous — "matches directory slug exactly" is not precise enough to resolve `avatar-cpp` vs `avatar-technology-cpp`
