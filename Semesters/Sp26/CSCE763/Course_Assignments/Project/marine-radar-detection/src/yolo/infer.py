"""Run a trained YOLOv11 checkpoint on the test set, save predictions, print AP."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import yaml
from tqdm import tqdm

from .model import predict_yolov11, predict_sahi


def _print_coco_ap(ann_path: str, pred_path: Path) -> None:
    from pycocotools.coco import COCO
    from pycocotools.cocoeval import COCOeval
    gt = COCO(ann_path)
    dt = gt.loadRes(str(pred_path))
    ev = COCOeval(gt, dt, "bbox")
    ev.evaluate(); ev.accumulate(); ev.summarize()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", required=True, help=".pt checkpoint")
    ap.add_argument("--ann", required=True, help="COCO test JSON")
    ap.add_argument("--images", required=True, help="Image directory")
    ap.add_argument("--config", default=str(Path(__file__).parent / "config.yaml"))
    ap.add_argument("--out-dir", default="results/yolo")
    ap.add_argument("--conf", type=float, default=0.01)
    ap.add_argument("--device", default="0")
    ap.add_argument("--sahi", action="store_true", help="Use SAHI tiled inference")
    args = ap.parse_args()

    with open(args.ann) as f:
        ann = json.load(f)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    preds: list[dict] = []
    for info in tqdm(ann["images"], desc="yolo"):
        img_path = Path(args.images) / info["file_name"]
        if not img_path.exists():
            continue
        if args.sahi:
            dets = predict_sahi(args.weights, str(img_path), args.config)
            for d in dets:
                b = d["bbox"]
                preds.append({
                    "image_id": info["id"], "category_id": 1,
                    "bbox": [b[0], b[1], b[2] - b[0], b[3] - b[1]],
                    "score": d["score"],
                })
        else:
            img = cv2.imread(str(img_path))
            for x1, y1, x2, y2, score in predict_yolov11(
                args.weights, img, conf=args.conf, device=args.device
            ):
                preds.append({
                    "image_id": info["id"], "category_id": 1,
                    "bbox": [float(x1), float(y1), float(x2 - x1), float(y2 - y1)],
                    "score": float(score),
                })

    stem = Path(args.weights).stem
    pred_path = out_dir / f"{stem}_predictions.json"
    pred_path.write_text(json.dumps(preds))
    print(f"\nSaved {len(preds)} predictions -> {pred_path}\n")
    _print_coco_ap(args.ann, pred_path)


if __name__ == "__main__":
    main()
