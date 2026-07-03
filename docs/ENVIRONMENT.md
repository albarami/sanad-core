# ENVIRONMENT — build log & acceptance record

*Every value here is measured, not assumed (No-Free-Facts). Log every workaround —
this file becomes reusable IP for the SGEIP stack (execution plan §1, Step 0.3).*

## Machine (verified 2026-07-03)

| Item | Value | Evidence |
|---|---|---|
| GPU | NVIDIA GeForce RTX 5090, 32,607 MiB VRAM | `nvidia-smi` 2026-07-03 21:10 |
| Driver / CUDA UMD | 610.43.02 / CUDA 13.3 | `nvidia-smi` |
| Platform | WSL2 Ubuntu (kernel 6.6.114.1-microsoft-standard-WSL2) | `uname` |
| Disk (ext4 `/`) | 1007 GB total, 944 GB free at setup | `df -h` |
| Python | 3.11.15 (CPython) via uv 0.11.17 | `uv python list` |

## Storage layout (rule: WSL ext4 only — never /mnt/c or /mnt/d, 9P is too slow)

| Path | Purpose |
|---|---|
| `~/models/hf` | `HF_HOME` — model + dataset cache |
| `~/ckpts` | `SANAD_CKPT_DIR` — training checkpoints |
| `D:\data\sanad-core` | archive/overflow only (machine convention) |

Set persistently in `~/.bashrc` (marked block, added 2026-07-03) and per-shell via
`source tools/env.sh`.

## Install method

```bash
uv sync --group train    # torch from cu128 index (Blackwell sm_120) + full stack
```

Torch is pinned to the `https://download.pytorch.org/whl/cu128` index in
`pyproject.toml` (`[tool.uv.sources]`); everything resolves in one venv.

**Version policy (brief rev 3 Jul 2026):** Qwen3.5 needs current transformers,
vllm ≥0.19-class, and **latest unsloth** (Qwen3.5 support confirmed May 2026).
unsloth is floored in `pyproject.toml`; its caps bound the rest of the tree
(2026.6.9: `torch<2.11`, `transformers<=5.5.0`, `trl<=0.24`).

Installed versions (from `uv.lock` re-resolve, 2026-07-03 late):

- torch **2.10.0+cu128** (cu128 = Blackwell sm_120)
- **unsloth 2026.6.9** (+ unsloth-zoo 2026.6.7) — latest on PyPI at install time
- transformers 4.57.6 · datasets 3.6.0 · peft 0.19.1 · trl 0.24.0
- bitsandbytes 0.49.2 · accelerate 1.14.0 · **vllm 0.19.1** (the ≥0.19-class the brief names)
- huggingface-hub 0.36.2 (pulled below 1.x by transformers 4.57's cap; `hf` CLI
  verified working) · xformers 0.0.35 · triton 3.6.0
- flash-attn: **not installed** (not in the resolved tree; xformers + SDPA cover attention)

`llamafactory` (optional secondary trainer per brief) deliberately **not installed** —
add only if unsloth proves insufficient.

## Base models (D1 FIXED 3 Jul 2026; HF API probed same night — all public, un-gated)

| Repo | Role (D1) | Status |
|---|---|---|
| `Qwen/Qwen3.5-9B` | core engine — iteration base, bf16 LoRA | awaiting Salim's download approval |
| `Qwen/Qwen3.5-27B` | core engine — release candidate, 4-bit QLoRA | awaiting Salim's download approval |
| `QCRI/Fanar-2-27B-Instruct` | sovereign-deployment adapter + Arabic cross-check | awaiting Salim's download approval |
| `Qwen/Qwen3-32B` | fallback only (hybrid-arch tripwire) | opt-in via `--with-fallback` |

Downloads are **manual-approval only** — `tools/download_bases.sh` never
auto-starts. Disk at last check: 944 GB free (`~/models/hf` is empty — the
superseded-queue partial cache was deleted 2026-07-03).

## Acceptance = five smoke tests (PROJECT_BRIEF)

| # | Test | Status | Evidence |
|---|---|---|---|
| 1 | `torch.cuda.get_device_capability()` → `(12, 0)`; bf16 matmul runs | **PASS 2026-07-03** (initial on torch 2.11.0+cu128; **re-verified same night on final torch 2.10.0+cu128**) | `tools/gpu_check.py`: `capability: (12, 0)`, `bf16 matmul OK: (4096, 4096)` — passed even with ~31 GB VRAM held by an external process |
| 2 | Qwen3.5-9B loads (bf16) and generates, thinking mode on and off | PENDING (download approval) | — |
| 3 | Fanar-2-27B-Instruct loads 4-bit (~14–15 GB), generates with native chat template, `<think>` on/off | PENDING (download approval) | — |
| 4 | 10-step QLoRA on Qwen3.5-27B @ 8K ctx, no OOM (batch 1, grad-accum 16, grad ckpt) | PENDING | — |
| 5 | vLLM serves one model; curl/openai-client request returns | PENDING | — |

Setup night = tests queued; smoke tests 2–5 expected next session (per brief: "setup
tonight, smoke tests tomorrow").

## Workarounds & friction log

1. **`huggingface-hub` 1.x extras removed** — `[cli,hf_transfer]` extras no longer
   exist (the `hf` CLI ships in the base package; Xet replaced hf_transfer). Fixed by
   depending on plain `huggingface-hub`; dropped `HF_HUB_ENABLE_HF_TRANSFER` from
   `tools/env.sh`.
2. **External VRAM occupancy at setup** — 30.9/32.6 GB VRAM in use by a process
   outside this session on setup night. Harmless for install/downloads; **must be
   freed before smoke tests 2–5** (4-bit 27B needs ~14–15 GB).
3. **Flash-attention on sm_120** — not yet exercised. If wheels fail at smoke-test
   time, fall back to `attn_implementation="sdpa"` per brief and log it here.
4. **No SSH keys on machine** — GitHub over HTTPS with `gh` credential helper
   (account `albarami`, repo+workflow scopes).
5. **D1 revision mid-setup (2026-07-03 late)** — independent editor fixed D1 to
   Qwen3.5-9B/27B while the old queue was still downloading the superseded
   iteration model. Download killed and its 4.3 GB partial cache deleted (model
   name: git history / `~/models/download-20260703.log`); download policy is
   now manual-approval-only. `Qwen/Qwen3.5-9B` and `Qwen/Qwen3.5-27B` verified
   on HF (public, un-gated; MoE variants exist and are excluded per D1).
6. **unsloth staleness trap** — first resolve maximized torch (2.11.0) and
   transformers (5.13.0), which forced unsloth back to 2025.9.5 (pre-Qwen3.5).
   Fix: floor `unsloth>=2026.6.9` and let its caps pull torch→2.10.0+cu128,
   transformers→4.57.6, trl→0.24.0, vllm→0.19.1. Also restrict uv resolution to
   linux/x86_64 (`[tool.uv] environments`) — default multi-platform resolve
   fails on vllm's darwin/mlx split — and pin `requires-python <3.12`.
   **Watch item:** whether transformers 4.57.6 natively serves Qwen3.5's hybrid
   architecture is unverified until weights land — smoke test 2 arbitrates
   (unsloth vendors model patches). Pre-planned fallback if it fails: split
   vllm into its own venv, raise transformers to 5.5.0 for training.
