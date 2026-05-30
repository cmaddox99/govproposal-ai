# ENG-10.3 Exception Request: Network Automation Avatar Manifest Token Budget

**Proposal ID:** network-automation-manifest-token-exception
**Date:** 2026-04-29
**Requestor:** Network Automation Avatar Maintainer
**Governing Law:** ENG-10.3 (Compliance Reporting Law)
**Schema Reference:** `docs/guides/avatar-model-schema.md §2` — token budget limits
**Precedent:** `hangar-ai-specs/changes/cpp-manifest-token-exception/PROPOSAL.md`
**Status:** PENDING APPROVAL

---

## 1. Exception Requested

**Artifact:** `avatars/product-type/network-automation/manifest.yaml`
**Current size:** ~580 tokens (230 words / 2,316 chars)
**Schema limit (§2):** 150 tokens (🔴 BLOCKING)
**Requested limit:** ≤ 1,000 tokens for product-type avatars

This request seeks a formal schema exception for the network-automation avatar's `manifest.yaml` token budget, consistent with the precedent established by the C++ avatar exception. The manifest exceeds the 150-token schema limit using only schema-permitted content blocks (`avatar`, `domain`, `core_journeys`, `activates`, `specializes_laws`).

---

## 2. Problem Statement

The `avatar-model-schema.md §2` imposes a 150-token BLOCKING limit on `manifest.yaml`. The network-automation manifest is ~580 tokens — ~3.9× the stated limit — using only schema-permitted blocks. The avatar specializes 9 PRD/BUS laws (each requiring an `id`, `title`, and `example_file` reference), enumerates 4 personas, 5 core journeys, 6 activated skills, and 2 workflows. Eliminating any of this content destroys legitimate constitutional structure required for RAG retrieval and law citation.

---

## 3. Cross-Avatar Evidence: 150t Limit Universally Violated

A scan of all 17 product-type avatars (2026-04-29) confirms the 150t limit is exceeded by every product avatar in the library:

| Avatar | Manifest Words | Approx Tokens |
|--------|---------------:|--------------:|
| ground-ops-staffing-analytics | 984 | ~1,200 |
| check-in-travel | 836 | ~1,050 |
| network-planning-optimization | 736 | ~920 |
| cargo-freight | 696 | ~870 |
| loyalty-aadvantage | 658 | ~820 |
| schedule-change-self-serve | 627 | ~785 |
| customer-relations-ops | 516 | ~645 |
| crew-training-scheduling | 453 | ~565 |
| customer-service | 452 | ~565 |
| passenger-booking | 450 | ~560 |
| internal-productivity | 440 | ~550 |
| gate-management | 405 | ~505 |
| airport-operations | 384 | ~480 |
| marketing-personalization | 283 | ~355 |
| crew-recovery-solver | 282 | ~355 |
| **network-automation** | **230** | **~580** |
| travel-docs-compliance | 218 | ~275 |

**Summary:** 17/17 (100%) product-type avatars exceed the 150t manifest limit. The network-automation manifest is the **2nd smallest** in the product-type library by word count and well below the median.

---

## 4. Two-File Architecture Justification

The network-automation avatar implements the two-file architecture described in `docs/articles/token-optimization-multi-rag-architecture.md`:

- **`guidance.md`** — always-loaded RAG anchor with non-negotiable laws and navigation pointers.
- **`manifest.yaml` (~580t)** — machine-readable configuration with product-domain metadata, persona enumeration, journey list, skill activation, and law specialization references.

The manifest's ~580 tokens sit comfortably within the article's 2–5K guidance for Level 3 avatar specialization and within the precedent's ≤1,000t request bound. No content can be removed without breaking schema compliance for `specializes_laws` (9 entries, each requiring id/title/example_file).

---

## 5. Mitigations Adopted

- The manifest contains **only the schema-permitted top-level blocks**; no forbidden blocks (e.g., `tiers`, `archetypes`, `authorities`).
- Detailed law application content lives in `examples/*.md` files (one per specialized law) — the manifest only carries `example_file` pointers.
- Persona detail lives in `examples/personas.md` — the manifest only carries persona names + the `personas_file` pointer.
- Use case detail lives under `use-cases/network-change-automation/` — referenced by the avatar registry, not embedded in the manifest.

---

## 6. Risk Assessment

| Risk | Severity | Mitigation |
|------|---------:|-----------|
| RAG context window pressure | LOW | Manifest not loaded on every query; total per-query load remains under 3,500t |
| Schema drift / precedent inflation | LOW | Bounded ≤1,000t request, well below cpp's ~985t; consistent with existing product avatars |
| Law citation completeness | NONE | All 9 specialized laws retain id/title/example_file — citation integrity preserved |

---

## 7. Approval Requested

Approve a token budget exception of **≤ 1,000 tokens** for `avatars/product-type/network-automation/manifest.yaml`, valid until the constitution-wide schema reconciliation tracked under `cpp-manifest-token-exception` is completed and the schema's 150t limit is formally revised.

**Required approvers:**
- Constitution Governance Lead
- Product Avatar Maintainer
- RAG Systems Review
