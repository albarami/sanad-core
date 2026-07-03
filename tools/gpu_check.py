"""Smoke test 1 (PROJECT_BRIEF acceptance): CUDA capability + bf16 matmul.

Expected on this machine: RTX 5090 -> capability (12, 0), Blackwell sm_120.
Run:  uv run python tools/gpu_check.py
Log the output in docs/ENVIRONMENT.md.
"""

import sys


def main() -> int:
    import torch

    print(f"torch {torch.__version__} | cuda build {torch.version.cuda}")
    if not torch.cuda.is_available():
        print("FAIL: torch.cuda.is_available() is False")
        return 1

    cap = torch.cuda.get_device_capability()
    props = torch.cuda.get_device_properties(0)
    vram_gb = props.total_memory / 1024**3
    print(f"device: {props.name} | capability: {cap} | VRAM: {vram_gb:.1f} GB")

    x = torch.randn(4096, 4096, device="cuda", dtype=torch.bfloat16)
    y = x @ x
    torch.cuda.synchronize()
    print(f"bf16 matmul OK: {tuple(y.shape)}, mean={y.float().mean().item():+.4f}")

    if cap != (12, 0):
        print(f"WARN: capability {cap} != (12, 0) — is this the 5090?")
        return 2
    print("PASS: smoke test 1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
