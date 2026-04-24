"""Train YOLOv11 on the radar dataset.

Usage:
    python -m src.yolo.train --data data/processed/yolo/data.yaml
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from .model import train_yolov11


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="Path to YOLO data.yaml")
    ap.add_argument("--config", default=str(Path(__file__).parent / "config.yaml"))
    ap.add_argument("--output-dir", default="results/yolo")
    ap.add_argument("--seeds", nargs="+", type=int, default=None)
    ap.add_argument("--device", default=None)
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text())
    if args.device is not None:
        cfg["training"]["device"] = args.device
    seeds = args.seeds or cfg["training"]["seeds"]

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    for seed in seeds:
        print(f"\n--- YOLOv11 seed={seed} device={cfg['training']['device']} ---")
        train_yolov11(args.data, args.config, str(out), seed=seed)


if __name__ == "__main__":
    main()
