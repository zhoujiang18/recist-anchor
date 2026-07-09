#!/bin/sh
set -eu

export CUDA_VISIBLE_DEVICES=""
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-6}"
export MKL_NUM_THREADS="${MKL_NUM_THREADS:-6}"
export OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-6}"
export PYTHONWARNINGS="${PYTHONWARNINGS:-ignore::FutureWarning}"

mkdir -p /workspace/outputs
cd /workspace/app

echo "medai Task 2 CPU inference"
echo "Inputs: /workspace/inputs"
echo "Outputs: /workspace/outputs"
echo "CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES}"
date '+START %F %T'

python predict.py \
  --load_path /workspace/inputs \
  --save_path /workspace/outputs \
  --model_checkpoint /workspace/weights.pth \
  --model_type medai_model_rope_mixed \
  --segmenter_type original \
  --segmenter_device cpu \
  --model_device cpu

date '+DONE %F %T'
