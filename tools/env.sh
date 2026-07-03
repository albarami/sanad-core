# sanad-core environment — source this before training/download work:
#   source tools/env.sh
# Storage rule (PROJECT_BRIEF): caches/weights/checkpoints on WSL ext4,
# never /mnt/c or /mnt/d (9P I/O is too slow for training).
export HF_HOME="$HOME/models/hf"
export SANAD_CKPT_DIR="$HOME/ckpts"
