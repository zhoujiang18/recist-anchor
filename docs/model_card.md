# Model Card

## Model

RECIST-anchored lightweight 3D lesion segmentation for CPU-only inference.

## Intended Use

This model is intended for the Pan-cancer Segmentation challenge Subtask 2 setting: generating a 3D lesion segmentation mask from a preprocessed CT NPZ volume and a RECIST diameter marker.

It is a research challenge submission and is not intended for clinical deployment.

## Inputs

- 3D CT volume in NPZ format.
- RECIST marker in NPZ format.
- Spatial metadata.

## Outputs

- `uint8` NIfTI multi-label lesion mask.

## Training Data

Official released Subtask 2 training data. No private external dataset was used.

## Initialization

Public Lite ENSAM checkpoint.

## Limitations

- The method depends on RECIST marker quality and label consistency.
- If the RECIST marker is missing or placed far from the lesion center, the method can under-segment or return an empty mask.
- Validation results are local public-validation estimates and may not directly predict hidden-test ranking.

