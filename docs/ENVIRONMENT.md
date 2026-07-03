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
`pyproject.toml` (`[tool.uv.sources]`); everything resolves in one venv —
**234 packages, no unsloth↔vllm↔torch conflict at resolution (2026-07-03)**.

Installed versions (from `uv pip list`, 2026-07-03; venv = 12 GB):

- torch **2.11.0+cu128** (cuda build 12.8)
- unsloth 2025.9.5 (+ unsloth-zoo 2025.9.12) · transformers 5.13.0 · datasets 3.6.0
- peft 0.19.1 · trl 0.29.1 · bitsandbytes 0.49.2 · accelerate 1.14.0
- vllm 0.24.0 · huggingface-hub 1.22.0 · xformers 0.0.35 · triton 3.6.0
- flash-attn: **not installed** (not in the resolved tree; xformers + SDPA cover attention)

`llamafactory` (optional secondary trainer per brief) deliberately **not installed** —
add only if unsloth proves insufficient.

## Base models (HF API probed 2026-07-03 — all public, none gated, no token needed)

| Repo | Gated | Status |
|---|---|---|
| `Qwen/Qwen3-14B` | no | download queued |
| `QCRI/Fanar-2-27B-Instruct` | no | download queued |
| `Qwen/Qwen3-32B` | no | download queued (disk allows: 944 GB free) |

## Acceptance = five smoke tests (PROJECT_BRIEF)

| # | Test | Status | Evidence |
|---|---|---|---|
| 1 | `torch.cuda.get_device_capability()` → `(12, 0)`; bf16 matmul runs | **PASS 2026-07-03** | `tools/gpu_check.py`: `capability: (12, 0)`, `bf16 matmul OK: (4096, 4096), mean=+0.0080` — passed even with ~31 GB VRAM held by an external process |
| 2 | Qwen3-14B loads 4-bit and generates | PENDING (downloads overnight) | — |
| 3 | Fanar-2-27B-Instruct loads 4-bit (~14–15 GB), generates, `<think>` on/off | PENDING (downloads overnight) | — |
| 4 | 10-step QLoRA toy run @ 8K ctx, no OOM (27B: batch 1, grad-accum 16, grad ckpt) | PENDING | — |
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
