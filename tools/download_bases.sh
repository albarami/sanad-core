#!/usr/bin/env bash
# Base-model downloads — D1 (FIXED 3 Jul 2026): core engine Qwen3.5-9B +
# Qwen3.5-27B; Fanar-2-27B-Instruct as sovereign-deployment adapter and
# Arabic-consistency cross-check. Qwen3-32B is FALLBACK ONLY (opt-in).
#
# THIS SCRIPT NEVER AUTO-STARTS. Downloads are launched only by Salim,
# manually, after explicit approval:
#   nohup bash tools/download_bases.sh > ~/models/download.out 2>&1 &
# Fallback model included only when explicitly requested:
#   nohup bash tools/download_bases.sh --with-fallback > ~/models/download.out 2>&1 &
# Safe to re-run: hf download resumes partial downloads from the cache.
set -u
cd "$(dirname "$0")/.." || exit 1
source tools/env.sh

LOG="$HOME/models/download-$(date +%Y%m%d).log"
MODELS=(
    "Qwen/Qwen3.5-9B"
    "Qwen/Qwen3.5-27B"
    "QCRI/Fanar-2-27B-Instruct"
)
if [ "${1:-}" = "--with-fallback" ]; then
    MODELS+=("Qwen/Qwen3-32B")   # D1 fallback if hybrid arch fights this card
fi

for m in "${MODELS[@]}"; do
    echo "=== START $m $(date '+%F %T') ==="
    if uv run hf download "$m" >>"$LOG" 2>&1; then
        echo "=== DONE  $m $(date '+%F %T') | free: $(df -h "$HOME" | awk 'NR==2{print $4}') ==="
    else
        echo "=== FAILED $m (exit $?) $(date '+%F %T') — see $LOG ==="
    fi
done
echo "=== ALL QUEUED DOWNLOADS PROCESSED $(date '+%F %T') ==="
