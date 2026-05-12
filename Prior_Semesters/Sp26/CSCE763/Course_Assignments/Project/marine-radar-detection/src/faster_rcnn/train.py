"""Train Faster R-CNN with multi-seed runs.

You supply whichever split + image layout you built. No assumptions about
directory naming — pass explicit paths.

Usage:
    python -m src.faster_rcnn.train \\
        --train-ann    <path/to/train.json> \\
        --val-ann      <path/to/val.json> \\
        --train-images <path/to/train_images> \\
        --val-images   <path/to/val_images>
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml
from torch.utils.data import DataLoader

from .dataset import RadarDetectionDataset, coco_to_items
from .model import build_model, train_faster_rcnn


def _collate(batch):
    return tuple(zip(*batch))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-ann", required=True, help="Training COCO JSON")
    ap.add_argument("--val-ann", required=True, help="Validation COCO JSON")
    ap.add_argument("--train-images", required=True, help="Training image directory")
    ap.add_argument("--val-images", required=True, help="Validation image directory")
    ap.add_argument("--config", default=str(Path(__file__).parent / "config.yaml"))
    ap.add_argument("--output-dir", default="results/faster_rcnn")
    ap.add_argument("--seeds", nargs="+", type=int, default=None)
    ap.add_argument("--device", default=None)
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text())
    if args.device is not None:
        cfg["training"]["device"] = args.device
    seeds = args.seeds or cfg["training"]["seeds"]

    with open(args.train_ann) as f:
        train_items = coco_to_items(json.load(f))
    with open(args.val_ann) as f:
        val_items = coco_to_items(json.load(f))

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    for seed in seeds:
        print(f"\n--- Faster R-CNN seed={seed} device={cfg['training']['device']} ---")
        model = build_model(cfg)

        train_ds = RadarDetectionDataset(args.train_images, train_items)
        val_ds = RadarDetectionDataset(args.val_images, val_items)

        train_loader = DataLoader(
            train_ds,
            batch_size=cfg["training"]["batch_size"],
            shuffle=True,
            num_workers=cfg["training"]["workers"],
            collate_fn=_collate,
        )
        val_loader = DataLoader(
            val_ds,
            batch_size=cfg["training"]["batch_size"],
            shuffle=False,
            num_workers=cfg["training"]["workers"],
            collate_fn=_collate,
        )

        train_faster_rcnn(model, train_loader, val_loader, cfg, str(out), seed=seed)


if __name__ == "__main__":
    main()
