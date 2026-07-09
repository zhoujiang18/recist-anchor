# Code Completeness Checklist

## Environments and Requirements

- Dockerfile: `submission/Dockerfile`.
- Python dependencies: `submission/requirements.txt`.
- CPU-only execution: `submission/predict.sh`.

## Dataset

- Dataset is not redistributed.
- Expected NPZ structure is documented in `README.md`.

## Preprocessing

- No separate preprocessing script is required for challenge NPZ files.
- Inference directly consumes challenge-provided NPZ files.

## Training

- Final training hyperparameters are documented in `README.md` and `docs/reproducibility_checklist.md`.
- Example training command: `scripts/finetune_selected_checkpoint_example.sh`.
- Historical full training logs and large intermediate checkpoints are excluded.

## Trained Models

- Final selected checkpoint: `submission/weights.pth`.

## Inference

- Docker build: `scripts/build_docker.sh`.
- Docker run command: documented in `README.md`.
- Prediction entry point: `submission/predict.sh`.
- Python inference implementation: `submission/predict.py`.

## Evaluation

- Local evaluation script: `scripts/evaluate_npz_predictions.py`.
- Reported metrics and summaries: `experiments/`.

## Results

- Main results table appears in `README.md`.
- Full manuscript: `paper/paper.pdf`.
- Figures: `assets/`.

## Known Reproducibility Boundaries

- Official hidden test data are not available.
- Challenge data and Docker tar submission are not tracked.
- The public Lite ENSAM checkpoint is acknowledged as the initialization source.

