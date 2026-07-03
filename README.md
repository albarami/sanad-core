# sanad-core — PRIVATE

Track-A workspace for **Sanad** (SanadFinance-LLM): training the Sanad-R reasoning
adapter (dual-axis verification methodology), building SanadBench, and producing the
90-day evidence assets. Read `docs/PROJECT_BRIEF.md` first; the spec is
`docs/sanadfinance_llm_unified_development_study.md` ("UDS") and the plan of record is
`docs/sanad_90_day_execution_plan.md`.

**This repository is inside the trade-secret perimeter (decision D2). Never make it
public. Training data, adapters, registry contents, and rule thresholds stay closed.**

## Locked decisions (Day 0 — recorded per execution plan Step 0.1)

- **D1 — Base models (FIXED 3 Jul 2026):** Core engine = Qwen3.5-9B (iteration
  base, bf16 LoRA — fits 32 GB) and Qwen3.5-27B (release candidate, 4-bit QLoRA);
  fallback if the hybrid architecture fights this card = Qwen3-32B.
  Fanar-2-27B-Instruct = sovereign-deployment adapter + Arabic-consistency
  cross-check in evals — NOT a core-engine candidate. ALLaM = later Saudi
  deployment target. Qwen3.5 MoE variants (35B-A3B, 122B-A10B) excluded: QLoRA
  unsupported on MoE, bf16 exceeds 32 GB. The Week-2 run is VERIFICATION with one
  reversion tripwire (Fanar-2 beats Qwen3.5-27B by ≥5 weighted points on the 25
  pilot cases), not open selection.
- **D2 — Open/closed line:** OPEN → SanadBench, eval harness, technical report,
  methodology. CLOSED → D1–D3 training data, adapters, source registry, rule
  weights/thresholds.
- **D3 — Language:** 50/50 Arabic/English in every corpus.
- **D4 — Names:** SanadBench (benchmark), Sanad-R (adapter). `sanad-bench` becomes a
  separate repo in Week 3 — not before.

## Hard rules in force

R-A no public disclosure before the provisional patent filing · R-B the 50-case frozen
eval set is sealed and never used for training or tuning · R-C every gold record is
human-verified field-by-field by Salim (AI-drafted allowed, AI-graded not) · R-D the
acceptance gate is reported as measured, including a loss · R-E Day-90 is decided by the
pre-committed matrix. **Compute provenance:** this workstation or personally paid cloud
rental only — never ministry or partner compute.

## Layout

```
data/d0..d3/     training corpora (D0 classical, D1 gold, D2 synthetic, D3 preference pairs)
eval/            frozen/ (sealed Week 3), dev/, results/
train/configs/   training run configs
registry/        source-registry seed (schema arrives with its slice)
tools/           environment & utility scripts
docs/            brief, UDS, execution plan, STATUS.md, ENVIRONMENT.md
```

## Environment (WSL2 · RTX 5090 · Python 3.11 via uv)

```bash
uv sync --group train          # full GPU stack (torch cu128, unsloth, trl, vllm, …)
source tools/env.sh            # HF_HOME + checkpoint dirs on WSL ext4
uv run python tools/gpu_check.py   # smoke test 1
```

Weights and checkpoints live in `~/models` and `~/ckpts` (WSL ext4 — never `/mnt/c|d`).
Setup details, the five acceptance smoke tests, and every workaround are logged in
`docs/ENVIRONMENT.md`. Current step board: `docs/STATUS.md`.
