# D1 gold-record schema

Derived from UDS Appendix B (training-record schema) and UDS §2 (dual-axis
grades + derivation rules R1–R6). Approved in PLAN v2 (Slice 1).

## Where the contract lives

- **Enforced contract:** `tools/sanad_schema.py` — pydantic v2 models. This is
  the source of truth; a record is *gold-shaped* iff it constructs here.
- **Documentation artifact:** `gold.schema.json` — emitted from the pydantic
  models via `python -m tools.sanad_schema`. Regenerate it whenever the models
  change; do not hand-edit.
- **Validator:** `tools/validate_gold.py`.

## Records

- One record per file: `gold-0001.json`, `gold-0002.json`, … (zero-padded 4
  digits), pretty-printed so diffs are reviewable and R-C field-by-field
  verification is legible.
- Trainer JSONL (`input`/`target`/`meta`, one record per line) is built later
  from the per-record files:

  ```bash
  jq -c . data/d1/gold-*.json > data/d1/gold.jsonl
  ```

## Validating

```bash
uv run python -m tools.validate_gold data/d1/gold-0001.json --emit-coverage
```

- **Tier-A** (hard-fail): schema, enum membership, `score`∈band, Axis-1
  `axis1_score`∈grade band, band↔grade-name agreement, confidence-interval
  bounds, and the single coverage invariant
  `meta.rules_exercised == ⋃ verdict.rules_cited` (and the same for
  `defects_seeded` / `defect_mechanisms`).
- **Tier-B** (hard-fail): derivation-trace completeness, reading the structured
  `rules_cited` / `defect_mechanisms` / `escalation` only — the prose
  `derivation_trace` is never parsed. Every verdict cites a band-setting rule
  (R1 or R3); a defect mechanism implies R3; shudhūdh caps at V4 unless a
  fabrication signal is present; a V6/mawdu verdict must cite R3 and carry a
  fabrication signal (`fraud_alert.issued` or an `ilal` mechanism).
- **Tier-C** (WARN, non-blocking this slice): R2 independence, R5 conflict
  presence, and registry-grade match — the last deferred until the source
  registry slice exists.

## Transliteration standard (corpus rule)

Latin transliteration of Sanad vocabulary is written in **uniform ASCII, no
diacritics**, throughout every field of a record — `analysis` prose, verdict
`derivation_trace` tags, and source `content` alike. Canonical spellings:
`saduq`, `dabt`, `sahih`, `hasan`, `daif`, `mawdu`, `shudhudh`, `ilal`,
`tawatur`, `isnad`, `matn`, `matruk`, `sukuk`, `lafzi`. This matches the enum
tokens, the deployment text, and clean tokenization.

Arabic-language records (`language: "ar"`) keep proper Arabic script in their
Arabic content; the ASCII rule governs **Latin transliteration only**, so it
does not touch native Arabic script.

Verdict `derivation_trace` entries are full reasoning sentences that state *why*
the cited rule produces the result (rule, evidence, and resulting band/score) —
not compressed labels — so the trace is pedagogically complete for training.

## Field conventions

- `Source.type` is a free string; recommended vocabulary: `regulatory_filing`,
  `corporate_ir`, `financial_media`, `anonymous_channel` (extend as needed).
- Grade / band tokens and their score bands are defined in
  `tools/sanad_schema.py` (`GRADE_RANGE`, `BAND_RANGE`, `BAND_TO_GRADE`).
- `confidence_interval` is an uncertainty interval and MAY cross band
  boundaries; it only has to bracket the score inside `[0, 100]`.

## Coverage matrix

`coverage_matrix.csv` keeps its existing 11 columns. Multi-valued cells are
`;`-joined; the finance shape rides the existing `domain` column as
`family:shape` (e.g. `islamic_finance:sukuk_certification`). The row is emitted
by `validate_gold.py --emit-coverage` and appended only after the record passes.

## Grading precedents (accumulated doctrine)

Case-law from certified records, applied to future grading. Each is a human R-C
judgment that the validator permits but does not itself adjudicate.

- **S6 "as-analyzed" (exemplar: gold-0002).** Grade an evidentiary artifact by
  what analysis concludes it *is*, not by how it presents. A certificate that
  *looks* like an S1/S2 board attestation but is invalid after examination is
  graded **S6** (invalid/unreliable, not proven fabricated). The issuing body's
  institutional authority is conceptually separate and is not downgraded — we
  grade the artifact, not the institution.

- **V4-not-V6 for a chronological-impossibility ilal (exemplar: gold-0002).** A
  confirmed ilal that is *validity-defeating but not fabrication* — e.g. a
  certificate dated outside the signatory's valid horizon — demotes the dependent
  claim to **V4 daif, with escalation and no fraud_alert**, reserving V6 (+
  fraud_alert) for *proven* fabrication. ilal adjudication is a human act (UDS
  §6.1); the validator enforces only structural completeness.

- **V5 (daif_jiddan) from category-misattribution (exemplar: gold-0005).** A weak
  (S5) base plus a SEVERE NON-FABRICATION ilal in the load-bearing datum — where
  the central support is materially MISCLASSIFIED (e.g. a stale "potential
  resource" estimate presented as current "proven reserves"), which are different
  evidentiary categories, not weaker/stronger versions of the same claim — lands
  at V5. Distinct from V4 (thin-but-honest: claim may be true, chain merely weak)
  and from V6 (proven fabrication). No fraud_alert unless intent/fabrication is
  proven.

**The coherent low-verdict ladder** (rising source/defect severity; fabrication
presumed unproven until proven):
- **V4 daif** — a thin-but-honest weak chain (the claim may be true, the chain is
  merely weak: gold-0004, pending Stage B), or a single validity-defeating ilal on
  an otherwise-strong-looking claim (gold-0002, claim 3).
- **V5 daif_jiddan** — a weak base *plus* a severe non-fabrication ilal
  (category-misattribution) in the load-bearing datum (gold-0005).
- **V6 mawdu** — proven fabrication / manipulation signature, fraud_alert issued
  (gold-0001, claim 3).

## R-C lifecycle (label discipline)

AI may draft the **structure**; **grades are the founder's** (record #1 is
transcribed verbatim from UDS Appendix A). A record stays
`review_status: draft` with `salim_verified=no` / `reviewer_verdict=pending`
until Salim verifies **every field** and assigns final grades — only then does
it become `gold_approved`. AI-graded records are never admitted (R-C).
