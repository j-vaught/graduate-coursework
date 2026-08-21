"""Run a trained Faster R-CNN checkpoint on the test set, save predictions, print AP."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
import torch
import yaml
from tqdm import tqdm

from .model import build_model, predict_faster_rcnn


def _print_coco_ap(ann_path: str, pred_path: Path) -> None:
    from pycocotools.coco import COCO
    from pycocotools.cocoeval import COCOeval
    gt = COCO(ann_path)
    dt = gt.loadRes(str(pred_path))
    ev = COCOeval(gt, dt, "bbox")
    ev.evaluate(); ev.accumulate(); ev.summarize()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", required=True, help=".pth checkpoint")
    ap.add_argument("--ann", required=True, help="COCO test JSON")
    ap.add_argument("--images", required=True)
    ap.add_argument("--config", default=str(Path(__file__).parent / "config.yaml"))
    ap.add_argument("--out-dir", default="results/faster_rcnn")
    ap.add_argument("--conf", type=float, default=0.01)
    ap.add_argument("--device", default="0")
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text())
    device = f"cuda:{args.device}" if args.device.isdigit() else args.device

    with open(args.ann) as f:
        ann = json.load(f)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    model = build_model(cfg)
    model.load_state_dict(torch.load(args.weights, map_location="cpu", weights_only=True))

    preds: list[dict] = []
    for info in tqdm(ann["images"], desc="faster_rcnn"):
        img_path = Path(args.images) / info["file_name"]
        if not img_path.exists():
            continue
        img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
        img3 = np.stack([img] * 3, axis=-1)
        tensor = torch.from_numpy(img3).permute(2, 0, 1).float() / 255.0

        dets = predict_faster_rcnn(model, tensor, device=device, score_thresh=args.conf)
        for i in range(len(dets)):
            x1, y1, x2, y2 = dets[i, :4]
            score = float(dets[i, 4]) if dets.shape[1] > 4 else 1.0
            preds.append({
                "image_id": info["id"], "category_id": 1,
                "bbox": [float(x1), float(y1), float(x2 - x1), float(y2 - y1)],
                "score": score,
            })

    stem = Path(args.weights).stem
    pred_path = out_dir / f"{stem}_predictions.json"
    pred_path.write_text(json.dumps(preds))
    print(f"\nSaved {len(preds)} predictions -> {pred_path}\n")
    _print_coco_ap(args.ann, pred_path)


if __name__ == "__main__":
    main()
