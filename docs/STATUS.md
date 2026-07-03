# STATUS — step board

*Update this file whenever a step changes state. Board seeded per PROJECT_BRIEF
"Seed files" spec on 2026-07-03.*

## Step 1 — Repos & setup
- [x] `sanad-core` repo initialized (main + `chore/environment-setup` branch) — 2026-07-03
- [x] Locked decisions D1–D4 recorded in README — 2026-07-03
- [x] Skeleton dirs + seed files materialized — 2026-07-03
- [x] uv env (Python 3.11) with train stack installed — torch 2.11.0+cu128, 2026-07-03
- [ ] Pushed to private remote `albarami/sanad-core` (awaiting Salim's push approval)
- [ ] `sanad-bench` repo — **do not create until Week 3** (D4)

## Step 2 — Smoke tests (record results in ENVIRONMENT.md)
- [x] 1. CUDA capability (12,0) + bf16 matmul — PASS 2026-07-03 (see ENVIRONMENT.md)
- [ ] 2. Qwen3-14B loads 4-bit, generates *(blocked on overnight download)*
- [ ] 3. Fanar-2-27B-Instruct loads 4-bit, generates, `<think>` on/off *(blocked on download)*
- [ ] 4. 10-step QLoRA toy run @ 8K ctx without OOM
- [ ] 5. vLLM serves a model; client request returns
- [ ] Overnight downloads queued: Qwen3-14B, Fanar-2-27B-Instruct (+ Qwen3-32B if disk allows)

## Step 3 — First gold work (after smoke tests)
- [ ] Gold cases #1–3 authored (ṣukūk-certification template, UDS Appendix A first)
- [ ] Codex reviews case #1 derivation trace
- [ ] Book Week-6 IP-counsel intro call

## Notes
- GPU had ~31/32.6 GB VRAM occupied by an external process during setup night —
  free it before smoke tests 2–5.
