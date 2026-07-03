# CLAUDE.md — sanad-core

Private Track-A workspace for Sanad (SanadFinance-LLM): train the Sanad-R reasoning
adapter (QLoRA SFT + DPO), build SanadBench, produce the 90-day evidence assets.
**Read first:** `docs/PROJECT_BRIEF.md` → `docs/sanad_90_day_execution_plan.md` (plan
of record) → `docs/sanadfinance_llm_unified_development_study.md` (the spec, "UDS").
Current step board: `docs/STATUS.md`. Environment truth: `docs/ENVIRONMENT.md`.

## What exists (as of 2026-07-03 — setup night)

- **Structure (skeleton only, no feature code):** `data/{d0,d1,d2,d3}/`,
  `eval/{frozen,dev,results}/`, `train/configs/`, `registry/`, `tools/`, `tests/`,
  `docs/`. All empty except seeds below.
- **Seeds:** `data/d1/coverage_matrix.csv` (header contract only),
  `data/d1/MANDATORY_CELLS.md` (pilot-25 coverage cells), `docs/STATUS.md`,
  `docs/ENVIRONMENT.md`, README with locked decisions D1–D4.
- **Environment:** uv venv (Python 3.11.15), torch 2.10.0+cu128, **unsloth
  2026.6.9** (floored — its caps bound torch/transformers/trl; see
  ENVIRONMENT.md friction log), transformers 4.57.6, trl 0.24.0, peft 0.19.1,
  bitsandbytes 0.49.2, vllm 0.19.1. Install: `uv sync --group train`. Smoke
  test 1 (capability (12,0) + bf16 matmul) **passed**; smoke tests 2–5 pending
  model downloads.
- **Tools:** `tools/gpu_check.py` (smoke test 1), `tools/download_bases.sh`
  (resumable; **never auto-starts — Salim launches downloads manually**),
  `tools/env.sh` (HF_HOME=`~/models/hf`, SANAD_CKPT_DIR=`~/ckpts` — also
  persisted in `~/.bashrc`).
- **Models (D1 FIXED 3 Jul 2026):** core engine Qwen3.5-9B (bf16 LoRA iteration
  base) + Qwen3.5-27B (4-bit QLoRA release candidate); Fanar-2-27B-Instruct as
  sovereign-deployment adapter + Arabic cross-check; Qwen3-32B fallback only;
  MoE variants excluded. **Not yet downloaded** — awaiting Salim's approval
  (the superseded old-D1 partial cache was deleted; `~/models/hf` is empty).
- **CI/tests:** `.github/workflows/ci.yml` (ruff + pytest, dev group only — never
  install the train group on runners), `tests/test_skeleton.py` structure guards.
- **Git:** `main` = genesis; work on `chore/environment-setup`; remote
  `https://github.com/albarami/sanad-core` (private) wired via `gh` HTTPS helper.

## What does NOT exist yet (do not assume, do not pre-build)

No eval harness (`eval/run.py` = Slice 1), no gold cases, no training configs, no
registry schema, no `sanad-bench` repo (Week 3, decision D4). Features arrive as
planned slices via the Planning Prompt — plan-first, reviewer-verified.

## Binding rules (from the brief — full text there)

- **R-A** nothing public before the provisional patent filing. Repo stays private
  (trade-secret perimeter, D2). Gold data never goes to third-party APIs except
  explicitly authorized synthesis flows.
- **R-B** `eval/frozen/` is sealed once created (Week 3): never train, tune, or
  debug on it.
- **R-C** every gold record is human-verified field-by-field by Salim. AI-drafted
  allowed; AI-graded is not.
- **R-D/R-E** gates reported as measured; Day-90 decided by the pre-committed matrix.
- **Compute provenance:** this workstation or personally paid cloud only.
- **Git discipline:** branch per slice → PR → CI green → reviewer APPROVE →
  **pause for Salim's explicit go before any push/merge** (house rule).
- **Model downloads:** manual-approval only — never launch or re-launch
  `tools/download_bases.sh` (or any `hf download`) without Salim's explicit go.
- **Storage:** weights/checkpoints/caches on WSL ext4 (`~/models`, `~/ckpts`) —
  never `/mnt/c` or `/mnt/d`, never in git.
- **Language balance (D3):** 50/50 Arabic/English in every corpus.

## Environment quickstart

```bash
uv sync --group train              # full GPU stack (12 GB venv)
source tools/env.sh                # storage env vars
uv run python tools/gpu_check.py   # smoke test 1
uv run ruff check . && uv run pytest -q
```

Blackwell note: if flash-attention ever fights sm_120, use
`attn_implementation="sdpa"` and log the workaround in `docs/ENVIRONMENT.md`.
