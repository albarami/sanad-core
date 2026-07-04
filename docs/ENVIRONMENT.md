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

**SERVE venv** — **materialized and version-verified by smoke test 5,
2026-07-04**: `vllm 0.24.0 | transformers 5.13.0 | torch 2.11.0+cu128`
(runtime `import` check inside the synced venv — matches `uv.lock` exactly).
vllm vendors its own qwen3_5 implementation, so serving tracks current
transformers freely. **Serving on this card needs three workarounds**
(friction 12): `LD_LIBRARY_PATH=.venv/…/nvidia/cu13/lib`,
`--attention-backend TRITON_ATTN`, `VLLM_USE_FLASHINFER_SAMPLER=0`.
torchvision/torchaudio are declared in the serve group so they resolve
from the cu128 index (also friction 12). After the test the active `.venv`
was restored to TRAIN.

`llamafactory` (optional secondary trainer per brief) deliberately **not installed** —
add only if unsloth proves insufficient.

## Base models (D1 FIXED 3 Jul 2026; HF API probed same night — all public, un-gated)

| Repo | Role (D1) | Status |
|---|---|---|
| `Qwen/Qwen3.5-9B` | core engine — iteration base, bf16 LoRA | **DOWNLOADED 2026-07-04** — 4/4 shards, 19G |
| `Qwen/Qwen3.5-27B` | core engine — release candidate, 4-bit QLoRA | **DOWNLOADED 2026-07-04** — 11/11 shards, 52G |
| `QCRI/Fanar-2-27B-Instruct` | sovereign-deployment adapter + Arabic cross-check | **DOWNLOADED 2026-07-04** — 11/11 shards, 51G |
| `Qwen/Qwen3-32B` | fallback only (hybrid-arch tripwire) | NOT downloaded — fallback not triggered |

Downloads are **manual-approval only** — `tools/download_bases.sh` never
auto-starts. Queue completed 2026-07-04 ~09:33 (DONE markers for all three in
`~/models/download.out`; per-model logs `~/models/download-2026070{3,4}.log`).
Authenticated via `HF_TOKEN` in `.env` throughout the final run — **zero**
"unauthenticated" warnings (the overnight run was anonymous and hit the
DNS-flap saga in friction 8). `~/models/hf` holds **26 snapshot shard
symlinks (4+11+11) plus one zero-byte `.no_exist` sentinel** — a benign HF
cache marker at
`models--Qwen--Qwen3.5-27B/.no_exist/…/model.safetensors`, so
`find ~/models/hf/hub -name '*.safetensors' | wc -l` returns **27, not 26**
(26 real symlinks + 1 sentinel); **zero `.incomplete` files**. 29 orphaned
`.incomplete` blobs from killed attempts (28.7 GB) were deleted 2026-07-04
after verifying zero overlap with snapshot-referenced blobs; `AutoConfig`
re-verified for all three models post-cleanup (`Qwen3_5Config` ×2; Fanar-2 =
`Gemma3TextConfig`, `model_type=gemma3_text`). Sizes (measured 2026-07-04
14:24 UTC, after smoke tests 2–5): `~/models/hf` **121G**; `/home`
**805G free** of 1007G. (An earlier reading right after orphan-cleanup, before
the serve-venv and test artifacts, was ~118G cache / 865G free.)

## Acceptance = five smoke tests (PROJECT_BRIEF)

| # | Test | Status | Evidence |
|---|---|---|---|
| 1 | `torch.cuda.get_device_capability()` → `(12, 0)`; bf16 matmul runs | **PASS 2026-07-03** (initial on torch 2.11.0+cu128; **re-verified same night on final torch 2.10.0+cu128**) | `tools/gpu_check.py`: `capability: (12, 0)`, `bf16 matmul OK: (4096, 4096)` — passed even with ~31 GB VRAM held by an external process |
| 2 | Qwen3.5-9B loads (bf16) and generates, thinking mode on and off | **PASS 2026-07-04** | `Qwen3_5ForCausalLM`, bf16, sdpa; 16.7 GiB after load / 16.8 GiB peak; `enable_thinking=True` → reasoning trace then "42" (120 tok, 5.0s ≈ 24 tok/s on pure-torch linear-attention fallback, friction 11); `enable_thinking=False` → "42" in 5 tok / 0.2s |
| 3 | Fanar-2-27B-Instruct loads 4-bit (~14–15 GB), generates with native chat template, `<think>` on/off | **PASS 2026-07-04** | NF4 double-quant + bf16 compute → `Gemma3ForCausalLM`, 22s load, **14.9 GiB** after load / 15.2 GiB peak; native template: thinking ON by default (`<think>` trace, 156 tok), OFF via `no_thinking=True` template var (direct answer, 10 tok). **Requires `HF_DEACTIVATE_ASYNC_LOAD=1`** (friction 9) |
| 4 | 10-step QLoRA on Qwen3.5-27B @ 8K ctx, no OOM (batch 1, grad-accum 16, grad ckpt) | **FAIL 2026-07-04** — failed before step 1; **not** allocator OOM, **not** a capacity verdict (decision recorded, Salim 2026-07-04) | Load+PEFT themselves PASS (4-bit load 53s, 16.7 GiB; 79.7M trainable LoRA params; corpus sample 8551 tok → truncated 8192). Failure: `cudaErrorNotReady` / "CUDA driver error: device not ready" at accelerate `_convert_to_fp32 → tensor.float()`. Allocator at failure: **0 CUDA OOMs, 0 cudaMalloc retries, ~29.4 GiB peak allocated / ~29.7 GiB reserved of 31.8**. Workaround attempted: `UNSLOTH_DISABLE_DOUBLE_BUFFER=1` — removed the double-buffer path, failure persisted. Interpretation: WSL2 + torch 2.10.0+cu128 + unsloth/accelerate async/offload-path instability; train stack pinned `torch<2.11` by unsloth 2026.6.9 (no 2.10.1 exists). Qwen3-32B fallback **not triggered**. Open follow-up: vanilla ckpt/no-offload test, upstream to unsloth, or revisit train/serve dependency strategy (friction 10) |
| 5 | vLLM serves one model; curl/openai-client request returns | **PASS 2026-07-04** (serve venv) | `uv sync --group serve` → runtime-verified `vllm 0.24.0 / transformers 5.13.0 / torch 2.11.0+cu128`; `vllm serve Qwen/Qwen3.5-9B --max-model-len 8192 --gpu-memory-utilization 0.85 --attention-backend TRITON_ATTN` (+`VLLM_USE_FLASHINFER_SAMPLER=0`, `LD_LIBRARY_PATH` → `nvidia/cu13/lib`) ready in 145s; OpenAI chat completion returned `finish=stop`, 101 completion tokens (thinking trace → "42"); clean shutdown. Three sm_120/cu128 workarounds: friction 12 |

Session 2 (2026-07-04): downloads completed and verified (26 snapshot shards,
4+11+11), smoke tests 2–3 PASS, 4 FAIL-recorded (driver instability, decision
above), 5 run same session per Salim's approval.

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
8. **WSL2 DNS-proxy flap during downloads (2026-07-04 ~06:07–07:17)** — the
   WSL resolver proxy (`10.255.255.254`, Tailscale search domain in the path)
   intermittently stopped answering; established TCP flows kept streaming
   while fresh lookups failed (`LocalEntryNotFoundError: [Errno -3] Temporary
   failure in name resolution` fast-fails). Public resolvers (1.1.1.1/8.8.8.8)
   answered fine throughout. The overnight anonymous download stalled and one
   supervisor self-heal fired; final authenticated run (HF_TOKEN in `.env`)
   completed the queue. **Ops lessons logged:** (a) `du -sb` is a FALSE stall
   metric — Xet preallocates files to final apparent size; use file mtimes or
   `/proc/<pid>/io` write counters; (b) always `source tools/env.sh` before
   any manual `hf download` — one manual resume ran without `HF_HOME` and
   wrote ~30 GB to `~/.cache/huggingface` (deleted; storage rule: `~/models`
   only).
9. **transformers 5.x threaded weight loading races bnb quantize-on-load
   (27B-class)** — v5's parallel materialization (`core_model_loading.py`,
   4 workers) issues concurrent GPU copies + `quantize_4bit` launches; on
   this stack (WSL2, sm_120, torch 2.10) 27B-scale loads die with racy async
   CUDA errors surfacing at bnb `ops.cu:62` (message varies run-to-run:
   "out of memory" / "invalid configuration argument"), with ~29 GB free and
   0 allocator OOMs. 9B loads fine; bnb kernels pass standalone at every
   size/blocksize. **Fix: `HF_DEACTIVATE_ASYNC_LOAD=1`** (sequential
   materialization) — Fanar-2 then loads 4-bit in 22s. Required for any
   ≥27B 4-bit load in the train venv; harmless elsewhere.
10. **Smoke test 4 FAIL — training-time async instability (2026-07-04,
    decision: Salim)** — 10-step QLoRA on Qwen3.5-27B @ 8K fails before
    step 1 with `cudaErrorNotReady` ("CUDA driver error: device not ready")
    at accelerate `_convert_to_fp32 → tensor.float()`. Allocator: 0 OOMs,
    0 cudaMalloc retries, peak ~29.4 GiB alloc / ~29.7 reserved of 31.8 —
    **fits**; NOT capacity, NOT architecture ⇒ Qwen3-32B fallback not
    triggered. `UNSLOTH_DISABLE_DOUBLE_BUFFER=1` removed the double-buffered
    backward but not the failure. Interpretation: WSL2 + torch 2.10.0+cu128 +
    unsloth/accelerate async/offload-path instability; train stack pinned
    `torch<2.11` by unsloth 2026.6.9 and no torch 2.10.1 exists. Open
    follow-up (tomorrow's decision): vanilla checkpointing/no-offload test,
    upstream issue to unsloth, or revisit the train/serve dependency
    strategy.
11. **Gated-delta fast-path libs unavailable under torch 2.10** — fla
    (flash-linear-attention) cpp extensions want torch ≥2.11 and
    causal-conv1d is not installed; Qwen3.5 linear-attention layers run the
    pure-torch fallback (functional; smoke 2 measured ~24 tok/s generation).
    Revisit if/when the torch pin moves.
12. **Serve venv on sm_120 with cu128 torch — three workarounds (smoke 5,
    2026-07-04).** vllm 0.24.0 PyPI wheels link CUDA-13 runtime libs while
    our torch pins to the cu128 index; three distinct breaks, each fixed
    without moving any version pin:
    (a) `ImportError: libcudart.so.13` — the lib ships in the unified
    `nvidia/cu13` package but is off the extension RPATH in this mixed
    layout ⇒ `export LD_LIBRARY_PATH=.venv/lib/python3.11/site-packages/nvidia/cu13/lib`.
    (b) PyPI torchvision/torchaudio are CUDA-13 builds ⇒
    `RuntimeError: PyTorch and torchvision were compiled with different CUDA
    major versions`. Root cause: `[tool.uv.sources]` index routing applies
    only to DECLARED dependencies, and in the serve group they were
    transitive (via vllm). Fix: declare `torchvision`/`torchaudio` in the
    serve group ⇒ relock moved them to `+cu128` builds of the same versions
    (pyproject + uv.lock updated 2026-07-04).
    (c) The cu128 runtime's capability probe fails on SM 12.x ("SM 12.x
    requires CUDA >= 12.9"), so every FlashInfer entry point dies with
    "requires sm75 or higher" — both attention auto-selection and the
    topk/topp sampler JIT ⇒ `--attention-backend TRITON_ATTN` +
    `VLLM_USE_FLASHINFER_SAMPLER=0` (native torch sampling). Proper fix
    when desired: a cu129+/cu130 torch stack for serve — revisit alongside
    the friction-10 torch-2.11 question.
