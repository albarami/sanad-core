# STATUS — step board

*Update this file whenever a step changes state. Board seeded per PROJECT_BRIEF
"Seed files" spec on 2026-07-03.*

## Step 1 — Repos & setup
- [x] `sanad-core` repo initialized (main + `chore/environment-setup` branch) — 2026-07-03
- [x] Locked decisions D1–D4 recorded in README — 2026-07-03
- [x] Skeleton dirs + seed files materialized — 2026-07-03
- [x] uv env (Python 3.11) — train/serve SPLIT via uv conflicting groups, both venvs built & verified 2026-07-03: train = unsloth 2026.6.9 + transformers 5.2.0 (pinned, friction 7) + torch 2.10 cu128; serve = vllm 0.24.0 + transformers 5.13 + torch 2.11 cu128. Swap: `uv sync --group train|serve`
- [ ] Pushed to private remote `albarami/sanad-core` (awaiting Salim's push approval)
- [ ] `sanad-bench` repo — **do not create until Week 3** (D4)

## Step 2 — Smoke tests (record results in ENVIRONMENT.md)
- [x] 1. CUDA capability (12,0) + bf16 matmul — PASS 2026-07-03, re-verified on final torch 2.10.0+cu128 (see ENVIRONMENT.md)
- [ ] 2. Qwen3.5-9B loads (bf16) and generates, thinking mode on/off *(blocked on download approval)*
- [ ] 3. Fanar-2-27B-Instruct (sovereign-adapter cross-check) loads 4-bit, generates, `<think>` on/off *(blocked on download approval)*
- [ ] 4. 10-step QLoRA on Qwen3.5-27B @ 8K ctx without OOM (batch 1, grad-accum 16, grad ckpt)
- [ ] 5. vLLM serves a model; client request returns — run in the **serve** venv
- [ ] Downloads (MANUAL — Salim approves launch): `tools/download_bases.sh` queues Qwen3.5-9B → Qwen3.5-27B → Fanar-2-27B-Instruct (`--with-fallback` adds Qwen3-32B). The 2026-07-03 auto-queued download of the superseded D1 iteration model was stopped when D1 was revised and its partial cache deleted (details: git history + `~/models/download-20260703.log`).

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
