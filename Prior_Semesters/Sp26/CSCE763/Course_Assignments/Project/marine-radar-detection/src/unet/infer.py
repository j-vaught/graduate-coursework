"""Run a trained U-Net checkpoint on the test set, save predictions, print AP."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
import torch
import yaml
from tqdm import tqdm

from .model import UNet, predict_unet


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
    ap.add_argument("--out-dir", default="results/unet")
    ap.add_argument("--device", default="0")
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text())
    device = f"cuda:{args.device}" if args.device.isdigit() else args.device
    post = cfg.get("postprocessing", {})
    threshold = post.get("threshold", 0.5)
    min_area = post.get("min_area", 15)

    with open(args.ann) as f:
        ann = json.load(f)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    model = UNet(
        in_channels=cfg["model"]["in_channels"],
        num_classes=cfg["model"]["num_classes"],
    )
    model.load_state_dict(torch.load(args.weights, map_location="cpu", weights_only=True))

    preds: list[dict] = []
    for info in tqdm(ann["images"], desc="unet"):
        img_path = Path(args.images) / info["file_name"]
        if not img_path.exists():
            continue
        img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
        tensor = torch.from_numpy(img).unsqueeze(0).float() / 255.0

        bboxes, pred_mask = predict_unet(
            model, tensor, device=device, threshold=threshold, min_area=min_area,
        )

        scores = np.ones(len(bboxes), dtype=np.float32)
        for j, box in enumerate(bboxes):
            x1, y1, x2, y2 = box.astype(int)
            region = pred_mask[max(0, y1):y2, max(0, x1):x2]
            if region.size > 0:
                scores[j] = float(region.mean())

        for i in range(len(bboxes)):
            x1, y1, x2, y2 = bboxes[i]
            preds.append({
                "image_id": info["id"], "category_id": 1,
                "bbox": [float(x1), float(y1), float(x2 - x1), float(y2 - y1)],
                "score": float(scores[i]),
            })

    stem = Path(args.weights).stem
    pred_path = out_dir / f"{stem}_predictions.json"
    pred_path.write_text(json.dumps(preds))
    print(f"\nSaved {len(preds)} predictions -> {pred_path}\n")
    _print_coco_ap(args.ann, pred_path)


if __name__ == "__main__":
    main()
