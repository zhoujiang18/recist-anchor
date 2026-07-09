#!/usr/bin/env bash
set -euo pipefail

# Example fine-tuning command for reproducing the selected checkpoint setup.
# The exact training entry point follows the public Lite ENSAM/FLARE25 codebase.
# Set these paths before running.

export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"
export PYTHONUNBUFFERED=1

UPSTREAM_REPO="${UPSTREAM_REPO:-/path/to/upstream_lite_ensam_or_flare25_repo}"
TRAIN_MODULE="${TRAIN_MODULE:-src.train_model}"
PYTHON_BIN="${PYTHON_BIN:-python}"
TRAIN_DIR="${TRAIN_DIR:-/path/to/train_npz}"
VAL_DIR="${VAL_DIR:-/path/to/validation_npz}"
PRETRAINED_CKPT="${PRETRAINED_CKPT:-/path/to/lite_ensam_checkpoint.pth}"
WORK_DIR="${WORK_DIR:-/path/to/work_dir}"
RUN_NAME="${RUN_NAME:-medai_finetune_seed2032_lr1e4_ep2_es6000}"

cd "${UPSTREAM_REPO}"

"${PYTHON_BIN}" -m "${TRAIN_MODULE}" \
  --train_dir "${TRAIN_DIR}" \
  --val_img_dir "${VAL_DIR}" \
  --checkpoint "${PRETRAINED_CKPT}" \
  --work_dir "${WORK_DIR}" \
  --task_name "${RUN_NAME}" \
  --device cuda:0 \
  --gpu_ids "${CUDA_VISIBLE_DEVICES}" \
  --num_workers 4 \
  --persistent_workers \
  --pin_memory \
  --prefetch_factor 2 \
  --batch_size 1 \
  --num_epochs 2 \
  --epoch_size 6000 \
  --lr 0.0001 \
  --weight_decay 0.0001
