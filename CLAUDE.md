# CLAUDE.md — sanad-core

Private Track-A workspace for Sanad (SanadFinance-LLM): train the Sanad-R reasoning
adapter (QLoRA SFT + DPO), build SanadBench, produce the 90-day evidence assets.
**Read first:** `docs/PROJECT_BRIEF.md` → `docs/sanad_90_day_execution_plan.md` (plan
of record) → `docs/sanadfinance_llm_unified_development_study.md` (the spec, "UDS").
Current step board: `docs/STATUS.md`. Environment truth: `docs/ENVIRONMENT.md`.

## What exists (as of 2026-07-03 — setup night)

- **Skeleton dirs (empty, `.gitkeep`-held, no feature code):**
  `data/{d0,d2,d3}/`, `eval/{frozen,dev,results}/`, `train/configs/`,
  `registry/`.
- **Seeds & docs:** `data/d1/coverage_matrix.csv` (header contract only),
  `data/d1/MANDATORY_CELLS.md` (pilot-25 coverage cells), `docs/STATUS.md`,
  `docs/ENVIRONMENT.md`, README with locked decisions D1–D4.
- **Setup deliverables (real files, not feature code):** `tools/gpu_check.py`,
  `tools/download_bases.sh`, `tools/env.sh`; `tests/test_skeleton.py`
  (structure guards); `.github/workflows/ci.yml`; `pyproject.toml` + `uv.lock`
  (conflicting train/serve groups); `.python-version`; `.env.example`.
- **Environment — TWO CONFLICTING VENVS, one materialized at a time** (uv
  conflict groups; syncing swaps `.venv` in place). **TRAIN is the currently
  active venv:** unsloth 2026.6.9, transformers **5.2.0 pinned** (lowest
  qwen3_5-registering release; evidence chain in ENVIRONMENT.md friction 7 —
  do not bump casually), trl 0.24.0, torch 2.10.0+cu128, no vllm. **SERVE is
  lock-resolved but NOT currently installed** — verified once at build
  (2026-07-03: vllm 0.24.0, transformers 5.13, torch 2.11.0+cu128);
  `uv sync --group serve` re-materializes it (smoke test 5 does this). Smoke
  test 1 **passed** (re-verified in train venv); config-only Qwen3.5 canary
  **passed** (train venv resolves `Qwen3_5Config`, hybrid layer_types); smoke
  tests 2–4 run in train, 5 in serve — pending model downloads.
- **Tools:** `tools/gpu_check.py` (smoke test 1), `tools/download_bases.sh`
  (resumable; **never auto-starts — Salim launches downloads manually**),
  `tools/env.sh` (HF_HOME=`~/models/hf`, SANAD_CKPT_DIR=`~/ckpts` — also
  persisted in `~/.bashrc`).
- **Models (D1 FIXED 3 Jul 2026):** core engine Qwen3.5-9B (bf16 LoRA iteration
  base) + Qwen3.5-27B (4-bit QLoRA release candidate); Fanar-2-27B-Instruct as
  sovereign-deployment adapter + Arabic cross-check; Qwen3-32B fallback only;
  MoE variants excluded. **Not yet downloaded** — awaiting Salim's approval.
  `~/models/hf` holds only hub metadata + the canary's **config-only**
  Qwen3.5-0.8B tree (56 KB); **zero model weights** (exact inventory in
  ENVIRONMENT.md).
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
uv sync --group train              # training venv (unsloth/QLoRA, smoke 1–4, hf downloads)
uv sync --group serve              # serving venv (vLLM, smoke 5) — swaps .venv in place
source tools/env.sh                # storage env vars
uv run python tools/gpu_check.py   # smoke test 1
uv run ruff check . && uv run pytest -q
```

Blackwell note: if flash-attention ever fights sm_120, use
`attn_implementation="sdpa"` and log the workaround in `docs/ENVIRONMENT.md`.
