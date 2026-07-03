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

## Install method — TWO CONFLICTING VENVS (train ⇄ serve)

No single dependency tree can hold latest-unsloth + vllm + qwen3_5-capable
transformers (friction 6–7). The split is implemented as uv **conflicting
dependency groups** in the one project; syncing swaps `.venv` in place:

```bash
uv sync --group train    # training/QLoRA, hf downloads, smoke tests 1–4
uv sync --group serve    # vLLM serving, smoke test 5
```

Torch resolves from the `https://download.pytorch.org/whl/cu128` index in both
groups (`[tool.uv.sources]`). Both forks live in the same `uv.lock`.

**TRAIN venv** (verified 2026-07-03 late):

- torch **2.10.0+cu128** · **unsloth 2026.6.9** (+ zoo 2026.6.7, latest on PyPI)
- **transformers 5.2.0** — pinned; see friction 7 for the pin's evidence chain
- trl 0.24.0 · peft 0.19.1 · datasets 3.6.0 · bitsandbytes 0.49.2
- accelerate 1.14.0 · huggingface-hub 1.22.0 (`hf` CLI working) · no vllm
- flash-attn: not installed (xformers/SDPA cover attention)

**SERVE venv** (verified 2026-07-03 late):

- torch **2.11.0+cu128** · **vllm 0.24.0** · transformers 5.13.0
- vllm vendors its own qwen3_5 implementation, so serving tracks current
  transformers freely

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
| 5 | vLLM serves one model; curl/openai-client request returns | PENDING — run in the **serve** venv (`uv sync --group serve`) | — |

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
   **Watch item — RESOLVED NEGATIVE by probe, see entry 7.**
7. **Qwen3.5 architecture probe (2026-07-03 late, zero-download):**
   `model_type: qwen3_5` / `Qwen3_5ForConditionalGeneration` is shared by all
   dense sizes (0.8B–27B config.json compared). transformers 4.57.6 does NOT
   have it (`CONFIG_MAPPING`: qwen3, qwen3_moe, qwen3_next — no qwen3_5);
   `AutoConfig.from_pretrained("Qwen/Qwen3.5-0.8B")` → `ValueError: The
   checkpoint you are trying to load has model type `qwen3_5` but Transformers
   does not recognize this architecture.` GitHub tag probe: qwen3_5 entered
   transformers at **v5.2.0** → viable window under unsloth's cap is
   **[5.2.0, 5.5.0]**. vllm (0.19.1–0.23) requires transformers `<5.0 or
   >5.5.0`; vllm 0.24 requires `>5.5` — **disjoint from [5.2, 5.5.0] in every
   case ⇒ no single venv can hold latest-unsloth + vllm + qwen3_5-capable
   transformers.** Mitigating fact: vllm 0.19.1 vendors its own qwen3_5
   implementation (`model_executor/models/qwen3_5.py` + config shims), so
   SERVING does not depend on the transformers version; the training/loading
   path (transformers + unsloth-zoo's qwen3_5 patches, incl. gated-delta ops)
   is what needs transformers ≥5.2. **RESOLVED 2026-07-03: Salim chose (b),
   the train/serve split** — implemented via uv conflicting groups (see
   Install method above).
   **Train transformers pin = 5.2.0, reasoning:** no artifact documents which
   5.x the unsloth-zoo qwen3_5 patches were *tested* against; verifiable
   evidence is authorship-era only — zoo's Qwen3.5 patch work landed in PR
   #495 (2026-02-25, "Qwen3Next and Qwen3.5 MoE Patches, Transformers v5
   fixes"), contemporaneous with transformers 5.2.0 (the release that
   introduced `qwen3_5`); the patches are defensively gated
   (`try: import transformers.models.qwen3_5_moe … except: return`) and the
   gated-delta vjp is pure torch (its only qwen3_5 reference is an mlx_vlm
   Apple-silicon path). Ambiguous ⇒ per the pre-committed rule, pin the
   LOWEST qwen3_5-registering release: **==5.2.0** (clears unsloth's
   exclusions, trl 0.24's ≥4.56.1, peft unconstrained). 5.2.x patch releases
   are a sanctioned bump if one proves needed.
   **Canary (config-only, zero weights) in the train venv: PASS 2026-07-03**
   — `AutoConfig.from_pretrained("Qwen/Qwen3.5-0.8B")` → `Qwen3_5Config`,
   `architectures=['Qwen3_5ForConditionalGeneration']`,
   `layer_types={'full_attention','linear_attention'}` (hybrid layout served
   natively). Smoke test 1 re-passed in the train venv same night.
   Note: huggingface-hub differs per venv (1.22.0 train / per-lock serve);
   `hf` CLI present in both.
