# Training and Inference Experiment Summary

## Selected Checkpoint

The selected checkpoint was chosen by public-validation DSC/NSD after supervised fine-tuning from the public Lite ENSAM checkpoint.

| Item | Value |
| --- | --- |
| Seed | 2032 |
| Learning rate | 1e-4 |
| Batch size | 1 |
| Total iterations | 12,000 |
| Epoch schedule | 2 fixed-length pseudo-epochs |
| Iterations per pseudo-epoch | 6000 |
| Loss | DiceCE |
| Weight decay | 1e-4 |
| Selection criterion | Best validation Dice checkpoint |

## Follow-up Experiments

Several additional runs were tested after selecting the checkpoint:

- Decoder/prompt-only fine-tuning with a lower learning rate.
- Boundary-loss fine-tuning.
- Fixed crop margins around RECIST.
- Adaptive margins based on RECIST diameter.
- RECIST-derived ellipsoid guards/clipping.
- Slice propagation.
- Morphological operations.

The final validation score was best with the selected checkpoint plus RECIST seed union and localized connected-component post-processing.

