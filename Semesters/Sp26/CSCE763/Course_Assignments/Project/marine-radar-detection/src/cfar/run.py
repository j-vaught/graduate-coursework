"""Run a CFAR variant on the COCO test set, save predictions, print AP.

Usage:
    python -m src.cfar.run --ann data/processed/annotations/test.json \\
                           --images data/processed/images \\
                           --variant ca_cfar
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
import yaml
from tqdm import tqdm

from .detector import detect_cfar

METHODS = ["ca_cfar", "go_cfar", "so_cfar", "os_cfar"]

# ── Inline helpers (per-folder sovereignty — no shared code) ────────────
_CENTER = (531, 515)
_RADIUS = 466


def _create_mask(h: int, w: int) -> np.ndarray:
    m = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(m, _CENTER, _RADIUS, 255, -1)
    return m


def _filter_by_mask(boxes: np.ndarray) -> np.ndarray:
    if len(boxes) == 0:
        return np.array([], dtype=bool)
    cx = (boxes[:, 0] + boxes[:, 2]) / 2
    cy = (boxes[:, 1] + boxes[:, 3]) / 2
    return np.hypot(cx - _CENTER[0], cy - _CENTER[1]) <= _RADIUS


def _format_preds(image_id: int, xyxy: np.ndarray, scores: np.ndarray) -> list[dict]:
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


def _print_coco_ap(ann_path: str, pred_path: Path) -> None:
    from pycocotools.coco import COCO
    from pycocotools.cocoeval import COCOeval
    gt = COCO(ann_path)
    dt = gt.loadRes(str(pred_path))
    ev = COCOeval(gt, dt, "bbox")
    ev.evaluate(); ev.accumulate(); ev.summarize()


def run(variant: str, cfg: dict, image_dir: str, coco_images: list[dict]) -> list[dict]:
    mode = {"ca_cfar": "CA", "go_cfar": "GO", "so_cfar": "SO", "os_cfar": "OS"}[variant]
    extra: dict = {}
    if variant == "os_cfar":
        extra["k_os"] = cfg["k"]

    preds: list[dict] = []
    for info in tqdm(coco_images, desc=variant):
        img_path = Path(image_dir) / info["file_name"]
        img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        mask = _create_mask(img.shape[0], img.shape[1])
        img = cv2.bitwise_and(img, mask)
        imgf = img.astype(np.float32) / 255.0
        bboxes, _, scores = detect_cfar(
            imgf,
            tuple(cfg["guard_cells"]),
            tuple(cfg["reference_cells"]),
            cfg["pfa"],
            mode=mode,
            min_area=cfg["min_area"],
            **extra,
        )
        if len(bboxes):
            keep = _filter_by_mask(bboxes)
            bboxes = bboxes[keep]
            scores = scores[keep]
        preds.extend(_format_preds(info["id"], bboxes, scores))
    return preds


def main() -> None:
    ap = argparse.ArgumentParser(description="Run CFAR family on COCO test set")
    ap.add_argument("--ann", required=True, help="Path to COCO test JSON")
    ap.add_argument("--images", required=True, help="Directory of PPI images")
    ap.add_argument("--config", default=str(Path(__file__).parent / "config.yaml"))
    ap.add_argument("--variant", default="ca_cfar", choices=METHODS)
    ap.add_argument("--out-dir", default="results/cfar")
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text())[args.variant]
    with open(args.ann) as f:
        ann = json.load(f)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    preds = run(args.variant, cfg, args.images, ann["images"])

    pred_path = out_dir / f"{args.variant}_predictions.json"
    pred_path.write_text(json.dumps(preds))
    print(f"\nSaved {len(preds)} predictions -> {pred_path}\n")
    _print_coco_ap(args.ann, pred_path)


if __name__ == "__main__":
    main()
