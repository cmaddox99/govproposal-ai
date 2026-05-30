## C++ Extended Reference Docs — Tasks

**Spec:** `cpp-extended-reference-docs`
**Parent PR:** #14 (c-plus-plus-avatar-enrichment)

---

### Phase 1 — Deliver Extended Reference File (DONE — Amendment O Step 16.6)

- [x] 1.1 Create `docs/guides/avatars/cpp/full-reference.md` with all content from `guidance.md`
- [x] 1.2 Remove BUS-* law citations from full-reference.md (V1/V2 domain boundary compliance)
- [x] 1.3 Rebuild `guidance.md` to ≤450 tokens (slim index)
- [x] 1.4 Update guidance section tests to read from full-reference.md
- [x] 1.5 Update `test_law_reference_coverage.py` — remove BUS-7.1/BUS-2.1 from section citation requirements

---

### Phase 2 — Update RAG Index

- [x] 2.1 Open `avatars/AVATAR-RAG-INDEX.yaml` — find the `cpp:` section
- [x] 2.2 Update all query entries that reference `guidance.md section_name` to reference `docs/guides/avatars/cpp/full-reference.md section_name`
- [x] 2.3 Update line 17 (`guidance_file: 200-450 tokens per guidance.md`) to reflect new two-file structure: guidance.md (index, 200-450 tokens) + full-reference.md (extended, on-demand)
- [x] 2.4 Write test: verify AVATAR-RAG-INDEX.yaml cpp section references full-reference.md for section queries
- [x] 2.5 Run full test suite — confirm 0 failures

---

### Phase 3 — PR and Close

- [x] 3.1 Commit: "docs(cpp): add extended reference docs (cpp-extended-reference-docs proposal)"
- [ ] 3.2 Open PR targeting main
- [ ] 3.3 Request governance review
