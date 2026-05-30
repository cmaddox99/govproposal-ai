# aa-citation-audit — Operator Runbook

**Tool:** `aa-citation-audit` v0.1.0  
**Project:** `citation-auditor-2026-001`  
**Law:** ENG-14.1 (NON-NEGOTIABLE), ENG-14.2 (conditional J6 activation)

---

## Install

```bash
cd tools/citation-auditor
pip install -e .
aa-citation-audit --version   # → aa-citation-audit v0.1.0
```

---

## Standard Invocation (pre-jury gate)

```bash
aa-citation-audit <artifact.md> --laws-dir laws
```

- **Exit 0** — all citations PASS (or WARN only); proceed to jury.
- **Exit 1** — ≥1 FAIL; correct artifact, re-run, then proceed to jury.
- **Exit 2** — tool/registry error; jury MUST HALT (fail-closed per ENG-14.1).

---

## Output Modes

| Mode | Command | Use |
|------|---------|-----|
| Console (colour) | `--output console` (default) | Human review |
| Stdout (plain) | `--output stdout` | CI parsing |
| Append to frontmatter | `--output append` | Write `citation_audit` block into artifact YAML |

---

## Fix Loop

1. Run audit: `aa-citation-audit stage-e-patterns.md --laws-dir laws`
2. For each `FAIL` row: find the cited ID in the artifact → correct to the real registry ID (check `laws/index.yaml`).
3. For each `WARN` row: the title you cited doesn't match the registry title — either correct the title phrase or verify the law ID is right.
4. Re-run → confirm exit 0.
5. Invoke jury.

---

## Write `citation_audit` Block to Artifact

```bash
aa-citation-audit stage-e-patterns.md --laws-dir laws --output append
```

Appends/overwrites `citation_audit:` YAML block in frontmatter. Required before jury invocation per ENG-6.7.

---

## J6 Activation (ENG-14.2)

J6 Citation Auditor (gpt-4.1) joins jury when ANY condition is met:
- L1 audit produced ≥1 WARN
- Artifact is Stage E or F in product-discovery workflow
- Artifact cites ≥5 distinct law IDs in frontmatter `law_citations`

---

## Audit Log

BUS-7.1 audit trail written to `~/.aa-citation-audit/audit.log` (JSON lines).  
Override: `AA_AUDIT_LOG_DIR=/path/to/dir`.

Each entry: `artifact`, `fail_count`, `warn_count`, `pass_count`, `tool_version`, `timestamp`, `sha256_artifact`.

---

## Running Against Mobile Discovery Artifacts

```bash
# Audit all disc-2026-006 stage artifacts
LAWS=/path/to/hangar-ai-constitution/laws
for f in /path/to/disc-2026-006/stage-*.md; do
  aa-citation-audit "$f" --laws-dir "$LAWS" --output append
done
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `RegistryLoadError` | `laws/index.yaml` missing or malformed | Verify `--laws-dir` points to constitution `laws/` directory |
| ID shows FAIL but looks right | Typo or wrong article (e.g. `ENG-4.11` vs `ENG-4.1`) | Check `laws/index.yaml` `law_ids.engineering` |
| WARN on valid law | Title phrase in artifact doesn't match registry | Use registry title verbatim or omit title phrase |
| Exit 2 in CI | Tool not installed | `pip install -e tools/citation-auditor` in CI setup step |

---

## HTML Artifact Scanning (v0.2.0+)

`aa-citation-audit` natively scans `.md`, `.html`, and `.htm` files — no extra flag required.

```bash
aa-citation-audit exec-deck.html --laws-dir laws/
```

### How it works

HTML files are processed by `_HTMLStripper`, which walks the parse tree and extracts **text nodes only**.  
The following content is **excluded** from scanning:

- `<script>` and `<style>` element bodies (including inline JS/CSS)
- HTML attribute values (e.g. `href`, `class`, `data-*`)
- HTML comments (`<!-- … -->`)
- CSS pseudo-content (`:before`/`:after` generated content)

Law IDs found in extracted text nodes are audited with the same L1/L2 rules as Markdown artifacts.

### `AuditError` on unclosed `<script>` or `<style>`

If the HTML contains an unclosed `<script>` or `<style>` tag, `_HTMLStripper` cannot safely isolate code content from text nodes and raises `AuditError` (exit 2).

**Fix:** Add the missing closing tag (`</script>` or `</style>`) and re-run.

Regression fixture: `tests/fixtures/scanner/artifact_html_unclosed_p.html`  
(Demonstrates that unclosed `<p>` tags — which are valid HTML — do **not** raise an error; only unclosed script/style blocks do.)

### Backward compatibility

Existing `.md` workflows are unchanged. The HTML path is a parallel code branch; Markdown files never pass through `_HTMLStripper`.

---

## L2 Contextual Mismatch — False-WARN Triage (v0.2.0+)

### What `WARN TITLE_MISMATCH` means

When a law ID is cited and an **explicit title phrase** appears nearby (within the L2 context window), the tool scores that phrase against the registry title using fuzzy similarity.  
A score **< 60** triggers `WARN TITLE_MISMATCH`.

### New L2 patterns in v0.2.0

v0.1.0 detected inline patterns (`ENG-X.Y Title`).  
v0.2.0 adds three structural patterns:

| Pattern | Example | Result |
|---------|---------|--------|
| Table cell | `\| ENG-6.4 \| No God Classes \|` | WARN (dual-anchor plain-text extraction) |
| Em-dash | `ENG-6.4 — No God Classes` | WARN |
| Before-ID parens | `God classes decomposed (ENG-6.4)` | WARN |

### Dual-anchor guard

Plain-text extraction from the context window is only performed when the window **both starts AND ends** with a structural separator matching `[|—–\-:()[\]]`.

This prevents false WARNs from colon-prose such as:

```
ENG-X.Y: This requirement explains that ...
```

Here the colon starts the window but there is no trailing separator, so the dual-anchor condition is **not met** → result is **PASS** (no title extracted, no mismatch scored).

### False-WARN triage quick reference

| Artifact text | Dual-anchor met? | Result | Action |
|---------------|-----------------|--------|--------|
| `\| ENG-6.4 \| No God Classes \|` | ✅ | WARN if phrase ≠ registry title | Correct title or law ID |
| `ENG-6.4 — No God Classes` | ✅ | WARN if phrase ≠ registry title | Correct title or law ID |
| `ENG-X.Y: This requirement ...` | ❌ (no trailing sep) | PASS | No action |
| `God classes decomposed (ENG-6.4)` | ✅ | WARN if phrase ≠ registry title | Correct title or law ID |

### Known limitation — pure-prose misapplication (J6/jury-documented)

Pure-prose misapplication (no structural separator around the ID) produces **PASS** because the dual-anchor guard correctly withholds extraction.

**Example:** `ENG-4.3 WireMock consumer contracts` → PASS (no surrounding separators).

This is a documented limitation. Per **ENG-12.1**, the **jury (human in the loop)** is the required control for pure-prose L2 detection. Flag these cases in the jury memo.

### Concrete examples — Jason's errors (disc-2026-004)

These fixtures were created by S-02 and live in `tests/fixtures/scanner/`:

**`artifact_regression_disc2026004_eng64.md`**  
ENG-6.4 misapplied with a god-class / SRP title phrase.  
The correct law for SRP / god-class decomposition is **ENG-3.4**.  
Expected audit result: `WARN TITLE_MISMATCH` on ENG-6.4.

**`artifact_regression_disc2026004_eng43.md`**  
ENG-4.3 misapplied with a WireMock consumer-contract title phrase.  
The correct law for WireMock consumer contracts is **ENG-4.9**.  
Expected audit result: depends on surrounding structure — WARN if dual-anchor is met, PASS (jury escalation required) if pure prose.
