# PROJECT_BRIEF — sanad-core
*Read this first. Companion documents in this folder: `sanadfinance_llm_unified_development_study.md` (the spec — "UDS") and `sanad_90_day_execution_plan.md` (the plan of record).*

## What we're building
Sanad Track-A: a 90-day program to (1) train a Sanad reasoning adapter (dual-axis verification methodology, UDS Part I) on the local RTX 5090 via QLoRA SFT + DPO, (2) build SanadBench, a 200-case calibrated-verification benchmark, and (3) produce the evidence assets (gate report, arXiv paper, demo) per the execution plan. This repo holds training data, configs, the eval harness, and the source registry. **This is an ML training/data project — NOT the standard FastAPI scaffold. Set up a tailored environment.**

## Locked decisions (Day 0 — do not revisit during setup)
- **D1 Base candidates:** Qwen3-14B (iteration primary), Fanar-2-27B-Instruct, Qwen3-32B (control). ALLaM enters later as a sovereign adapter target.
- **D2 Open/closed:** OPEN → SanadBench, harness, technical report, methodology. CLOSED → D1–D3 training data, adapters, registry, rule thresholds. This repo is PRIVATE (trade-secret perimeter).
- **D3 Language:** 50/50 Arabic/English in every corpus.
- **D4 Names:** SanadBench (benchmark), Sanad-R (adapter). `sanad-bench` becomes a separate project folder in Week 3 — do not create it now.

## Hard rules in force (from the execution plan)
R-A: no public disclosure of anything before the provisional patent filing. · R-B: the 50-case frozen eval set (Week 3) is sealed and never used for training or tuning. · R-C: every gold record is human-verified field-by-field by Salim; AI-drafted is allowed, AI-graded is not. · R-D: the acceptance gate is reported as measured, including a loss. · R-E: Day-90 decided by the pre-committed matrix, not sentiment.
**Compute provenance:** all training on this workstation or personally paid cloud rental only. No ministry or partner compute, ever.

## Tailored environment spec (what "set it up" means here)
- WSL2 Ubuntu on this machine (RTX 5090, 32 GB VRAM — Blackwell sm_120). Python 3.11 via **uv** per machine standard; 3.12 acceptable only if a dependency forces it.
- Install (uv-managed venv): `torch` from the **cu128 index** (Blackwell support), `unsloth`, `transformers`, `datasets`, `peft`, `trl`, `bitsandbytes`, `accelerate`, `vllm`, plus `pandas scipy`. `llamafactory` optional (secondary trainer).
- Known Blackwell friction: if flash-attention wheels fail on sm_120, use PyTorch SDPA (`attn_implementation="sdpa"`) and log the workaround in `docs/ENVIRONMENT.md`. Correctness first, speed later.
- **Storage:** set `HF_HOME` and checkpoint dirs to WSL ext4 (e.g. `~/models`, `~/ckpts` — gitignored), NOT `/mnt/c` or `/mnt/d` (9P I/O is too slow for training). `D:\data\sanad-core` is archive/overflow only, per machine convention.
- Queue overnight downloads at the end of setup: Qwen3-14B, Fanar-2-27B-Instruct (and Qwen3-32B if disk allows).

## Environment acceptance = five smoke tests (record results in docs/ENVIRONMENT.md)
1. `torch.cuda.get_device_capability()` → `(12, 0)`; a bf16 matmul runs.
2. Qwen3-14B loads 4-bit and generates.
3. Fanar-2-27B-Instruct loads 4-bit (~14–15 GB), generates with its native chat template, `<think>` mode on and off.
4. A 10-step QLoRA run completes on a toy dataset at 8K context without OOM (27B: batch 1, grad-accum 16, gradient checkpointing).
5. vLLM serves one model and a curl/openai-client request returns.
(Tests 2–5 may wait for overnight downloads — that is expected; setup tonight, smoke tests tomorrow.)

## Skeleton to materialize (structure + seed files only — no feature code)
```
data/{d0,d1,d2,d3}/        eval/{frozen,dev,results}/     train/configs/
registry/                  docs/                          tools/
```
Seed files: `.gitignore` (weights, *.safetensors, *.gguf, ckpts, wandb, .env, data/**/raw/) · `docs/STATUS.md` (step board: Step 1 repos/setup, Step 2 smoke tests, Step 3 gold cases #1–3 + book IP counsel) · `docs/ENVIRONMENT.md` (template with the five tests) · `data/d1/coverage_matrix.csv` with header: `case_id,status,language,domain,rules_exercised,axis2_band,defect_seeded,source_grades_present,author_date,salim_verified,reviewer_verdict` · `data/d1/MANDATORY_CELLS.md`: pilot 25 cases must cover — each rule R1–R6 ≥2×; each band V1–V6 ≥1; shudhūdh ≥3, iʿlāl-screen ≥3, clean ≥10; 13 en / 12 ar; ≥5 finance cases from live-work shapes (ṣukūk certification, spreading/variance, disclosure conflict), ≥3 non-finance.

## After setup (do NOT build now — these arrive as planned slices via the Planning Prompt)
Slice 1: eval harness v0 (`eval/run.py` — dual-axis accuracy, derivation faithfulness, calibration/ECE, escalation P/R, schema validity). Slice 2: gold-case authoring workflow (Appendix A/B templates from UDS + coverage-matrix updater). Slice 3: base-model bake-off runner. Everything plan-first, reviewer-verified, per this machine's four-prompt workflow.

## Git
Private GitHub remote (`albarami/sanad-core`), push after setup approval. Pause-before-approve applies to any push per house rules.
