# Final Experiment Summary

This document summarizes the final public-validation experiments included in the paper and README.

## Task

Subtask 2 requires converting a 3D CT volume and a sparse 2D RECIST diameter marker into a 3D lesion mask under CPU-only inference constraints.

## Final Method

The final method uses:

1. A fine-tuned Lite ENSAM-derived lightweight 3D model.
2. RECIST-derived per-lesion prompts.
3. RECIST seed union using a 3D radius-1 neighborhood.
4. RECIST-aware connected-component selection.
5. Hole filling.
6. Local-bounding-box post-processing to avoid full-volume connected-component operations.

## Main Validation Results

Metrics are averaged over 49 public validation cases.

| Method | DSC | NSD | Mean CPU time |
| --- | ---: | ---: | ---: |
| Lite ENSAM public checkpoint rerun | 0.6992 | 0.7471 | 4.03 s |
| Fine-tuned selected model only | 0.7424 | 0.8005 | 3.98 s |
| RECIST CC + hole filling | 0.7558 | 0.8185 | 8.83 s |
| Final localized method | **0.7615** | **0.8326** | **3.29 s** |

## Key Engineering Fix

A full-volume 3D connected-component implementation can be too slow for thick CT scans. The final code restricts connected-component analysis and hole filling to the union bounding box of the predicted mask and RECIST marker. On tested validation cases, this preserved the exact output mask while avoiding severe CPU runtime failures.

## Not Retained

The following variants were tested but did not consistently improve both DSC and NSD:

- 3x test-time augmentation.
- Two-model and weighted ensembles.
- Decoder-only low-learning-rate fine-tuning.
- Boundary-loss fine-tuning.
- Ellipsoid constraints from RECIST diameter.
- Slice-wise propagation.
- Morphological smoothing.
- Adaptive crop margins.

## Final Submission Properties

- CPU-only inference.
- 8 GB Docker memory limit tested.
- Output format: `uint8` NIfTI.
- Multi-label lesion IDs are preserved.
- No private external data.
- No pseudo labels from previous challenge-winning algorithms.
- No algorithm distillation.

