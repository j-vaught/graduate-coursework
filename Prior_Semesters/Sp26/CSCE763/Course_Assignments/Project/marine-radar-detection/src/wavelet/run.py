"""Run wavelet-SWT detector on the COCO test set, save predictions, print AP."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
import yaml
from tqdm import tqdm

from .detector import detect_wavelet

_CENTER = (531, 515)
_RADIUS = 466


def _create_mask(h, w):
    m = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(m, _CENTER, _RADIUS, 255, -1)
    return m


def _filter_by_mask(boxes):
    if len(boxes) == 0:
        return np.array([], dtype=bool)
    cx = (boxes[:, 0] + boxes[:, 2]) / 2
    cy = (boxes[:, 1] + boxes[:, 3]) / 2
    return np.hypot(cx - _CENTER[0], cy - _CENTER[1]) <= _RADIUS


def _format_preds(image_id, xyxy, scores):
    if len(xyxy) == 0:
        return []
    xywh = xyxy.astype(float).copy()
    xywh[:, 2] -= xywh[:, 0]
    xywh[:, 3] -= xywh[:, 1]
    return [
        {"image_id": int(image_id), "category_id": 1,
         "bbox": xywh[i].tolist(), "score": float(scores[i])}
        for i in range(len(xywh))
    ]


def _print_coco_ap(ann_path, pred_path):
    from pycocotools.coco import COCO
    from pycocotools.cocoeval import COCOeval
    gt = COCO(ann_path)
    dt = gt.loadRes(str(pred_path))
    ev = COCOeval(gt, dt, "bbox")
    ev.evaluate(); ev.accumulate(); ev.summarize()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ann", required=True)
    ap.add_argument("--images", required=True)
    ap.add_argument("--config", default=str(Path(__file__).parent / "config.yaml"))
    ap.add_argument("--out-dir", default="results/wavelet")
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text())["wavelet"]
    with open(args.ann) as f:
        ann = json.load(f)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    preds = []
    for info in tqdm(ann["images"], desc="wavelet"):
        img_path = Path(args.images) / info["file_name"]
        img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        img = cv2.bitwise_and(img, _create_mask(img.shape[0], img.shape[1]))
        imgf = img.astype(np.float32) / 255.0
        bboxes, _, scores = detect_wavelet(
            imgf,
            wavelet=cfg["wavelet"],
            level=cfg["level"],
            threshold_sigma=cfg["threshold_sigma"],
            subbands=cfg["subbands"],
            combine_mode=cfg["combine_mode"],
            min_area=cfg["min_area"],
            max_area=cfg.get("max_area", 50000),
        )
        if len(bboxes):
            keep = _filter_by_mask(bboxes)
            bboxes = bboxes[keep]
            scores = scores[keep]
        preds.extend(_format_preds(info["id"], bboxes, scores))

    pred_path = out_dir / "wavelet_predictions.json"
    pred_path.write_text(json.dumps(preds))
    print(f"\nSaved {len(preds)} predictions -> {pred_path}\n")
    _print_coco_ap(args.ann, pred_path)


if __name__ == "__main__":
    main()
