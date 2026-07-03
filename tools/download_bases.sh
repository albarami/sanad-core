#!/usr/bin/env bash
# Overnight base-model downloads (PROJECT_BRIEF: queue at end of setup).
# Sequential so the iteration primary (Qwen3-14B) lands first. Safe to
# re-run: hf download resumes partial downloads from the cache.
#   nohup bash tools/download_bases.sh > ~/models/download.out 2>&1 &
set -u
cd "$(dirname "$0")/.." || exit 1
source tools/env.sh

LOG="$HOME/models/download-$(date +%Y%m%d).log"
MODELS=(
    "Qwen/Qwen3-14B"
    "QCRI/Fanar-2-27B-Instruct"
    "Qwen/Qwen3-32B"
)

for m in "${MODELS[@]}"; do
    echo "=== START $m $(date '+%F %T') ==="
    if uv run hf download "$m" >>"$LOG" 2>&1; then
        echo "=== DONE  $m $(date '+%F %T') | free: $(df -h "$HOME" | awk 'NR==2{print $4}') ==="
    else
        echo "=== FAILED $m (exit $?) $(date '+%F %T') — see $LOG ==="
    fi
done
echo "=== ALL QUEUED DOWNLOADS PROCESSED $(date '+%F %T') ==="
