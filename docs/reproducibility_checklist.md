# Reproducibility Checklist

This checklist follows the structure of the MICCAI reproducibility checklist template in `checklists/`.

## Methods

- Mathematical setting and algorithm: described in `paper/paper.tex`, Sec. 2.
- Network architecture:
  - Lite ENSAM-derived compact SegResNet-style encoder and prompt-conditioned decoder.
  - Final instantiated model has approximately 1.32M trainable parameters.
  - Inference source code is in `submission/src/`.
- Evaluation metrics:
  - DSC and NSD are described in the paper.
  - Local evaluation script: `scripts/evaluate_npz_predictions.py`.

## Experiments

### Dataset

- Official Subtask 2 NPZ files from the Pan-cancer Segmentation challenge.
- Input keys required for inference: `imgs`, `recist`, `spacing`, `direction`, `origin`.
- Validation NPZ files additionally contain `gts` for local metric computation.
- Dataset is not redistributed in this repository.

### Preprocessing

- No extra resampling or intensity normalization during inference.
- The challenge-provided `imgs` array is already mapped to `[0, 255]`.
- RECIST markers are parsed label by label.
- The model uses RECIST-localized cropping and localized post-processing.

### Training Protocol

- Initialization: public Lite ENSAM checkpoint.
- Strategy: supervised fine-tuning and validation checkpoint selection.
- Batch size: 1.
- Learning rate: `1e-4`.
- Weight decay: `1e-4`.
- Iterations: 12,000.
- Epoch schedule: 2 fixed-length pseudo-epochs with 6000 iterations each.
- Loss: DiceCE.
- Training GPU: NVIDIA RTX 3090 during local experiments.
- Example command: `scripts/finetune_selected_checkpoint_example.sh`.

### Testing / Inference

- Final inference package: `submission/`.
- Docker command is documented in `README.md`.
- CPU-only inference is enforced by `CUDA_VISIBLE_DEVICES=""`.
- Output format: `uint8` NIfTI masks.

### Post-processing

- RECIST seed union with a 3D radius-1 neighborhood.
- RECIST-aware connected-component selection.
- Hole filling.
- Local-bounding-box implementation to avoid full-volume connected-component operations.

### Ablation Study

- Final paper table and figures are included in `paper/` and `assets/`.
- Lightweight experiment summaries are in `experiments/`.

## Results

- Final local validation: 0.7615 DSC / 0.8326 NSD.
- Same-machine Lite ENSAM checkpoint rerun: 0.6992 DSC / 0.7471 NSD.
- Mean CPU inference time: 3.29 s per validation case.
- Maximum official-like runtime: below 9 s in local validation.

## Qualitative Analysis

- Qualitative examples are shown in `paper/paper.pdf`.
- Figure source: `assets/`.

