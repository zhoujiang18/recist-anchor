#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import nibabel as nib
import numpy as np
from scipy import ndimage


def dice(gt: np.ndarray, pred: np.ndarray) -> float:
    gt = gt.astype(bool)
    pred = pred.astype(bool)
    denom = int(gt.sum()) + int(pred.sum())
    if denom == 0:
        return 1.0
    return 2.0 * float(np.logical_and(gt, pred).sum()) / float(denom)


def surface(mask: np.ndarray) -> np.ndarray:
    if not mask.any():
        return mask.astype(bool)
    structure = ndimage.generate_binary_structure(mask.ndim, 1)
    eroded = ndimage.binary_erosion(mask.astype(bool), structure=structure, border_value=0)
    return np.logical_xor(mask.astype(bool), eroded)


def normalized_surface_dice(gt: np.ndarray, pred: np.ndarray, spacing: np.ndarray, tolerance_mm: float) -> float:
    gt = gt.astype(bool)
    pred = pred.astype(bool)
    if not gt.any() and not pred.any():
        return 1.0
    if not gt.any() or not pred.any():
        return 0.0

    gt_surface = surface(gt)
    pred_surface = surface(pred)
    if not gt_surface.any() and not pred_surface.any():
        return 1.0
    if not gt_surface.any() or not pred_surface.any():
        return 0.0

    # distance_transform_edt returns distance to the nearest zero voxel.
    # Passing the inverse surface mask gives distance to the nearest surface voxel.
    spacing = np.asarray(spacing, dtype=float)
    if spacing.shape[0] == 3:
        sampling = spacing
    else:
        sampling = None
    dist_to_pred = ndimage.distance_transform_edt(~pred_surface, sampling=sampling)
    dist_to_gt = ndimage.distance_transform_edt(~gt_surface, sampling=sampling)

    gt_close = dist_to_pred[gt_surface] <= tolerance_mm
    pred_close = dist_to_gt[pred_surface] <= tolerance_mm
    return float(gt_close.sum() + pred_close.sum()) / float(gt_surface.sum() + pred_surface.sum())


def load_prediction(path: Path) -> np.ndarray:
    data = np.asanyarray(nib.load(str(path)).dataobj)
    return data.astype(np.uint8)


def case_stem(path: Path) -> str:
    name = path.name
    if name.endswith(".nii.gz"):
        return name[:-7]
    return path.stem


def evaluate_case(gt_npz: Path, pred_path: Path, tolerance_mm: float) -> dict[str, float | str]:
    with np.load(gt_npz, allow_pickle=True) as data:
        gt = data["gts"].astype(np.uint8)
        spacing = np.asarray(data["spacing"], dtype=float)
    pred = load_prediction(pred_path)
    if pred.shape != gt.shape:
        raise ValueError(f"Shape mismatch for {gt_npz.name}: gt={gt.shape}, pred={pred.shape}")

    labels = [int(label) for label in np.unique(gt) if int(label) != 0]
    if not labels:
        return {"case": gt_npz.name, "dsc": float("nan"), "nsd": float("nan"), "num_labels": 0}

    dsc_scores = []
    nsd_scores = []
    for label in labels:
        gt_label = gt == label
        pred_label = pred == label
        dsc_scores.append(dice(gt_label, pred_label))
        nsd_scores.append(normalized_surface_dice(gt_label, pred_label, spacing, tolerance_mm))

    return {
        "case": gt_npz.name,
        "dsc": float(np.mean(dsc_scores)),
        "nsd": float(np.mean(nsd_scores)),
        "num_labels": len(labels),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate NIfTI predictions against validation NPZ files.")
    parser.add_argument("--gt_npz_dir", required=True, type=Path)
    parser.add_argument("--pred_dir", required=True, type=Path)
    parser.add_argument("--out_csv", required=True, type=Path)
    parser.add_argument("--tolerance_mm", default=2.0, type=float)
    args = parser.parse_args()

    pred_by_stem = {case_stem(path): path for path in args.pred_dir.glob("*.nii.gz")}
    rows = []
    for gt_npz in sorted(args.gt_npz_dir.glob("*.npz")):
        pred_path = pred_by_stem.get(gt_npz.stem)
        if pred_path is None:
            raise FileNotFoundError(f"No prediction found for {gt_npz.name}")
        row = evaluate_case(gt_npz, pred_path, args.tolerance_mm)
        rows.append(row)
        print(f"{row['case']} DSC={row['dsc']:.4f} NSD={row['nsd']:.4f} labels={row['num_labels']}", flush=True)

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.out_csv.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["case", "dsc", "nsd", "num_labels"])
        writer.writeheader()
        writer.writerows(rows)

    dsc = float(np.nanmean([row["dsc"] for row in rows]))
    nsd = float(np.nanmean([row["nsd"] for row in rows]))
    print(f"MEAN DSC={dsc:.4f} NSD={nsd:.4f}")
    print(f"CSV={args.out_csv}")


if __name__ == "__main__":
    main()

