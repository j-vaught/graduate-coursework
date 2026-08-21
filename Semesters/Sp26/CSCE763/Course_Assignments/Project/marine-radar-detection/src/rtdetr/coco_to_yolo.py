"""COCO → YOLO format converter (sibling copy for RT-DETR).

Kept as a local duplicate so rtdetr/ stays self-contained. If you change
one converter, decide whether the other should change too.

Usage: see docstring in src.yolo.coco_to_yolo (identical interface).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def write_labels(coco_path: str | Path, image_dir: str | Path, label_dir: str | Path) -> int:
    with open(coco_path) as f:
        coco = json.load(f)

    imgs = {img["id"]: (img["width"], img["height"], Path(img["file_name"]).stem)
            for img in coco["images"]}

    by_img: dict[int, list[dict]] = {}
    for ann in coco["annotations"]:
        by_img.setdefault(ann["image_id"], []).append(ann)

    label_dir = Path(label_dir)
    label_dir.mkdir(parents=True, exist_ok=True)

    for img_id, (w, h, stem) in imgs.items():
        lines = []
        for ann in by_img.get(img_id, []):
            x, y, bw, bh = ann["bbox"]
            cx = (x + bw / 2) / w
            cy = (y + bh / 2) / h
            lines.append(f"{ann['category_id'] - 1} {cx:.6f} {cy:.6f} {bw / w:.6f} {bh / h:.6f}")
        (label_dir / f"{stem}.txt").write_text("\n".join(lines))
    return len(imgs)


def main() -> None:
    ap = argparse.ArgumentParser(description="Build YOLO-format labels from COCO for RT-DETR")
    ap.add_argument("--train-ann", required=True)
    ap.add_argument("--val-ann", required=True)
    ap.add_argument("--test-ann", required=True)
    ap.add_argument("--train-images", required=True)
    ap.add_argument("--val-images", required=True)
    ap.add_argument("--test-images", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    out = Path(args.out)
    for split, ann, images in [
        ("train", args.train_ann, args.train_images),
        ("val", args.val_ann, args.val_images),
        ("test", args.test_ann, args.test_images),
    ]:
        n = write_labels(ann, images, out / split / "labels")
        print(f"{split}: {n} labels in {out / split / 'labels'}")

    (out / "data.yaml").write_text(
        f"path: {out.resolve()}\n"
        f"train: {Path(args.train_images).resolve()}\n"
        f"val: {Path(args.val_images).resolve()}\n"
        f"test: {Path(args.test_images).resolve()}\n"
        "names:\n  0: target\n"
    )
    print(f"Wrote {out / 'data.yaml'}")


if __name__ == "__main__":
    main()
