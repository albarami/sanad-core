# STATUS — step board

*Update this file whenever a step changes state. Board seeded per PROJECT_BRIEF
"Seed files" spec on 2026-07-03.*

## Step 1 — Repos & setup
- [x] `sanad-core` repo initialized (main + `chore/environment-setup` branch) — 2026-07-03
- [x] Locked decisions D1–D4 recorded in README — 2026-07-03
- [x] Skeleton dirs + seed files materialized — 2026-07-03
- [x] uv env (Python 3.11) — train/serve SPLIT via uv conflicting groups. **TRAIN built & version-verified 2026-07-03, currently active:** unsloth 2026.6.9 + transformers 5.2.0 (pinned, friction 7) + torch 2.10 cu128. **SERVE lock-resolved only, not materialized** (uv.lock pins vllm 0.24.0 + transformers 5.13 + torch 2.11 cu128) — smoke test 5 materializes and verifies it via `uv sync --group serve`
- [x] Pushed to private remote `albarami/sanad-core` (Salim approved 2026-07-03) — PR #1 open
- [ ] `sanad-bench` repo — **do not create until Week 3** (D4)

## Step 2 — Smoke tests (record results in ENVIRONMENT.md)
- [x] 1. CUDA capability (12,0) + bf16 matmul — PASS 2026-07-03, re-verified on final torch 2.10.0+cu128 (see ENVIRONMENT.md)
- [x] 2. Qwen3.5-9B loads (bf16) and generates, thinking mode on/off — **PASS 2026-07-04** (16.7 GiB, thinking toggle verified; ENVIRONMENT.md)
- [x] 3. Fanar-2-27B-Instruct (sovereign-adapter cross-check) loads 4-bit, generates, `<think>` on/off — **PASS 2026-07-04** (14.9 GiB, native `no_thinking` toggle; needs `HF_DEACTIVATE_ASYNC_LOAD=1`, friction 9)
- [ ] 4. 10-step QLoRA on Qwen3.5-27B @ 8K ctx without OOM (batch 1, grad-accum 16, grad ckpt) — **FAIL 2026-07-04, recorded by decision**: `cudaErrorNotReady` driver/runtime instability before step 1; NOT allocator OOM (0 OOMs, peak 29.4/31.8 GiB — recipe fits), NOT a capacity/architecture verdict ⇒ **Qwen3-32B fallback not triggered**. Follow-up = tomorrow's decision (ENVIRONMENT.md friction 10)
- [x] 5. vLLM serves a model; client request returns — **PASS 2026-07-04**: serve venv materialized & version-verified (vllm 0.24.0 / transformers 5.13.0 / torch 2.11.0+cu128); Qwen3.5-9B served, OpenAI-format request returned 101 tokens; three sm_120 workarounds required (ENVIRONMENT.md friction 12)
- [x] Downloads — **COMPLETE 2026-07-04**: 26 snapshot shards (4+11+11; 9B 19G, 27B 52G, Fanar 51G) plus one zero-byte `.no_exist` sentinel (so `find … -name '*.safetensors'` returns 27, not 26); zero `.incomplete` files. Authenticated queue, DONE markers in `~/models/download.out`; orphaned partials cleaned (28.7 GB); AutoConfig re-verified ×3. Cache/disk (measured 2026-07-04 14:24 UTC): `~/models/hf` 121G, `/home` 805G free. DNS-flap saga + ops lessons: ENVIRONMENT.md friction 8. The 2026-07-03 auto-queued download of the superseded D1 iteration model was stopped when D1 was revised and its partial cache deleted (details: git history + `~/models/download-20260703.log`).

## Step 3 — First gold work (after smoke tests)
- [x] **Slice 1 complete** — gold-record schema (`tools/sanad_schema.py`, pydantic v2 + emitted `data/d1/gold.schema.json`), validator (`tools/validate_gold.py`, Tier-A/B/C), tests (`tests/test_gold_validator.py`, 23 passing), `data/d1/SCHEMA.md` — 2026-07-05
- [x] Gold case #1 authored + **R-C certified gold_approved** (`data/d1/gold-0001.json`, UDS Appendix A ṣukūk-certification worked example; coverage_matrix.csv row: salim_verified=yes, reviewer_verdict=approved) — 2026-07-05
- [x] **Slice 2 complete** — gold case #2 authored + **R-C certified gold_approved** (`data/d1/gold-0002.json`, Arabic chronological-impossibility iʿlāl in a Saudi ṣukūk-certification scenario; coverage row: salim_verified=yes, reviewer_verdict=approved). Adds a permanent `TODO_` placeholder guard to the validator (exit code 4) — 2026-07-06
- [x] **Batch 1 (English) complete** — gold-0003 (financial spreading, shudhudh, V2/V4), gold-0005 (first **V5 daif_jiddan** exemplar — category-misattribution iʿlāl), gold-0007 (first **non-finance** case, V1 on S1+R4+R6) authored + **R-C certified gold_approved**; V5 precedent documented in `data/d1/SCHEMA.md` — 2026-07-06
- [ ] Batch 1 (Arabic) — gold-0004 (disclosure, clean V4), gold-0006 (variance, R2 V3) pending Salim's authored Arabic
- [ ] Further pilot cases per MANDATORY_CELLS gaps (iʿlāl +1, non-finance +2, clean +7, language balance toward 13 en / 12 ar)
- [ ] Codex reviews case #1 derivation trace
- [ ] Book Week-6 IP-counsel intro call

## Notes
- 2026-07-06 (Batch 1, English three): gold-0003, gold-0005, gold-0007 landed —
  R-C certified gold_approved. gold-0003 (financial-spreading shudhudh, V2 + V4),
  gold-0005 (the first **V5 daif_jiddan** exemplar — category-misattribution iʿlāl
  on a weak base, fabrication unproven), gold-0007 (first **non-finance** case, V1
  on an S1 anchor + R4 + R6, no R2 — downstream echoes are not independent chains).
  **All six Axis-2 bands (V1–V6) and all six rules (R1–R6) are now exercised**
  across the corpus. New precedent documented in `data/d1/SCHEMA.md`: **V5 from
  category-misattribution** — a weak (S5) base + a severe non-fabrication iʿlāl in a
  miscategorized load-bearing datum → V5 (the coherent ladder: thin-honest V4 <
  severe-hidden-defect V5 < proven-fabrication V6). Batch 1 Arabic two (gold-0004,
  gold-0006) remain pending Salim's authored Arabic.
- 2026-07-06 (Slice 2): gold record #2 landed — `data/d1/gold-0002.json`, Arabic
  (Salim-authored, transcribed verbatim) chronological-impossibility iʿlāl in a
  Saudi ṣukūk-certification scenario, R-C certified gold_approved. Coverage now
  covers **six new cells**: Arabic (first `ar` record), R6 (first temporal-validity
  exercise), iʿlāl (first), and bands V2/V3/V4 (first of each). Two precedents
  recorded: (1) the certification artifact is graded **S6 as-analyzed** (an invalid
  attestation after the temporal check) without impugning the board's standing;
  (2) a **chronological-impossibility iʿlāl with fabrication unproven → V4 +
  escalation, no fraud alert** — distinct from a fabrication-class iʿlāl → V6. New
  permanent corpus safeguard: the validator rejects any record carrying an
  unresolved `TODO_` authoring placeholder (exit code 4) before coverage emission.
- 2026-07-05 (Slice 1): gold-record schema + validator + certified record #1
  landed. Two corpus-standard decisions set here: (1) UDS Appendix A's rule list
  for the sukuk example is corrected — the rejection verdict is R3-produced, so
  record #1's rules_exercised = R1,R2,R3,R4,R5 (single invariant:
  meta.rules_exercised == union of per-verdict rules_cited); (2) **ASCII
  transliteration standard** — all Latin transliteration of Sanad vocabulary is
  uniform ASCII (saduq, dabt, sahih, mawdu, shudhudh, ilal, tawatur, isnad,
  matn); `ar` records keep native Arabic script (see `data/d1/SCHEMA.md`).
- GPU had ~31/32.6 GB VRAM occupied by an external process during setup night —
  free it before smoke tests 2–5.
- 2026-07-03 late: independent editor revised PROJECT_BRIEF/execution plan — D1
  fixed to Qwen3.5-9B/27B core engine. All repo files re-synced to the revised
  brief; env re-resolved for latest unsloth (see ENVIRONMENT.md friction log).
- 2026-07-03 latest: zero-download architecture probe — transformers 4.57.6
  lacks qwen3_5 (needs ≥5.2; unsloth caps at 5.5.0; vllm constraint-disjoint
  from that window). Salim chose the train/serve split (option b) —
  implemented, canary **PASS** in train venv (`Qwen3_5Config` resolves,
  hybrid layer_types visible), smoke test 1 re-passed. Downloads still HELD
  for Salim's explicit approval (ENVIRONMENT.md friction entry 7).
- 2026-07-03 review round 1: reviewer REJECTED PR #1 on three doc-accuracy
  findings (cache-state claim stale after canary; serve venv described as
  installed when swap-on-demand; "all empty" understated deliverables). All
  three fixed; stale superseded-D1 lock dir cleaned from `~/models/hf`.
- 2026-07-03 review round 2: residual provenance finding — the serve venv
  "built & verified once" claim had no durable evidence (only the ephemeral
  setup-session transcript; uv.lock proves resolution, not materialization).
  Per No-Free-Facts, wording downgraded to lock-resolved-only; smoke test 5
  will materialize serve and record the evidence.
- 2026-07-03 review round 2 verdict: **APPROVE** — independent reviewer
  verified round-2 fix against durable evidence (train venv live-inspected;
  serve lock-only wording; cache inventory; no secrets tracked). Phase 0
  environment sign-off obtained. Merge + downloads remain gated on Salim's
  explicit word.
- 2026-07-04: PR #1 squash-merged to main (Salim's go). Downloads approved,
  completed 09:33 after a WSL2 DNS-flap night (1 supervisor self-heal, final
  run authenticated; friction 8). Smoke tests: 2 PASS, 3 PASS (async-load
  workaround, friction 9), 4 **FAIL recorded by Salim's decision** — driver
  instability (`cudaErrorNotReady`), not OOM/capacity/architecture; no more
  test-4 variants tonight; Qwen3-32B fallback NOT triggered (friction 10).
  Test 5 separately approved and run same session (result in ENVIRONMENT.md).
