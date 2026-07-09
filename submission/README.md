# Submission Package

This directory contains the final CPU-only Task 2 inference package.

Build:

```bash
docker build -t medai:latest .
```

Run:

```bash
docker container run \
  -m 8G \
  --name medai \
  --rm \
  -v $PWD/PanCancerSeg_Test/:/workspace/inputs/ \
  -v $PWD/medai_outputs/:/workspace/outputs/ \
  medai:latest \
  /bin/bash -c "sh predict.sh"
```

Important implementation details:

- `CUDA_VISIBLE_DEVICES=""` is set by `predict.sh`.
- CPU thread counts default to 6 for OpenMP/MKL/OpenBLAS.
- Input NPZ files are read from `/workspace/inputs`.
- Output NIfTI masks are written to `/workspace/outputs`.
- `weights.pth` is the selected fine-tuned checkpoint used in the submitted container.

