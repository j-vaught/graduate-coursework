"""Torchvision-style dataset for Faster R-CNN on radar tiles (self-contained)."""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import torch
from torch.utils.data import Dataset


class RadarDetectionDataset(Dataset):
    """Load tile images + COCO-derived boxes for torchvision detection models."""

    def __init__(
        self,
        image_dir: str | Path,
        annotations: list[dict],
        transforms=None,
    ):
        """
        Args:
            image_dir: Directory containing tile images.
            annotations: List of dicts with 'file_name', 'boxes' (N,4) in xyxy, 'labels' (N,).
            transforms: Optional albumentations/torchvision transforms.
        """
        self.image_dir = Path(image_dir)
        self.annotations = annotations
        self.transforms = transforms

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, idx):
        ann = self.annotations[idx]
        img_path = self.image_dir / ann["file_name"]
        image = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
        image = np.stack([image] * 3, axis=-1)  # grayscale → 3-channel

        boxes = np.array(ann["boxes"], dtype=np.float32)
        labels = np.array(ann["labels"], dtype=np.int64)
        if boxes.size == 0:
            boxes = np.zeros((0, 4), dtype=np.float32)
            labels = np.zeros((0,), dtype=np.int64)

        if self.transforms:
            transformed = self.transforms(image=image, bboxes=boxes, labels=labels)
            image = transformed["image"]
            boxes = np.array(transformed["bboxes"], dtype=np.float32)
            labels = np.array(transformed["labels"], dtype=np.int64)
            if boxes.size == 0:
                boxes = np.zeros((0, 4), dtype=np.float32)
                labels = np.zeros((0,), dtype=np.int64)

        image = torch.from_numpy(image).permute(2, 0, 1).float() / 255.0
        target = {
            "boxes": torch.as_tensor(boxes, dtype=torch.float32).reshape(-1, 4),
            "labels": torch.as_tensor(labels, dtype=torch.int64),
        }
        return image, target


def coco_to_items(coco: dict) -> list[dict]:
    """Flatten a COCO annotations dict into torchvision-style per-image items."""
    by_img: dict[int, list[dict]] = {}
    for ann in coco["annotations"]:
        by_img.setdefault(ann["image_id"], []).append(ann)
    items = []
    for img in coco["images"]:
        anns = by_img.get(img["id"], [])
        boxes, labels = [], []
        for a in anns:
            x, y, w, h = a["bbox"]
            boxes.append([x, y, x + w, y + h])
            labels.append(a["category_id"])
        items.append({"file_name": img["file_name"], "boxes": boxes, "labels": labels})
    return items
