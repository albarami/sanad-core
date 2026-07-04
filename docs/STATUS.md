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
- [ ] Gold cases #1–3 authored (ṣukūk-certification template, UDS Appendix A first)
- [ ] Codex reviews case #1 derivation trace
- [ ] Book Week-6 IP-counsel intro call

## Notes
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
