# Notice

This repository is a reproducibility package for the medai Subtask 2 solution to the CVPR 2026 Pan-cancer Segmentation challenge.

The method is based on the public Lite ENSAM implementation/checkpoint and was adapted through supervised fine-tuning, validation checkpoint selection, and RECIST-aware localized post-processing.

Third-party components retain their original licenses and terms. Users should verify the license terms of:

- Lite ENSAM / FLARE25 upstream code and checkpoint.
- The challenge dataset.
- The base Docker image `mrigroupopbg/mri-python3`.
- Python dependencies listed in `submission/requirements.txt`.

The challenge data and Docker tar submission are not redistributed in this repository.

