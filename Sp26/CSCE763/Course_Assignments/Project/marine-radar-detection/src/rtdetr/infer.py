"""Run a trained RT-DETR checkpoint on the test set, save predictions, print AP."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
from tqdm import tqdm

from .model import predict_rt_detr


def _print_coco_ap(ann_path: str, pred_path: Path) -> None:
    from pycocotools.coco import COCO
    from pycocotools.cocoeval import COCOeval
    gt = COCO(ann_path)
    dt = gt.loadRes(str(pred_path))
    ev = COCOeval(gt, dt, "bbox")
    ev.evaluate(); ev.accumulate(); ev.summarize()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", required=True)
    ap.add_argument("--ann", required=True)
    ap.add_argument("--images", required=True)
    ap.add_argument("--out-dir", default="results/rtdetr")
    ap.add_argument("--conf", type=float, default=0.01)
    ap.add_argument("--device", default="0")
    args = ap.parse_args()

    with open(args.ann) as f:
        ann = json.load(f)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    preds: list[dict] = []
    for info in tqdm(ann["images"], desc="rtdetr"):
        img_path = Path(args.images) / info["file_name"]
        if not img_path.exists():
            continue
        img = cv2.imread(str(img_path))
        dets = predict_rt_detr(args.weights, img, conf=args.conf, device=args.device)
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
