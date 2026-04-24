"""Segmentation dataset for U-Net on radar tiles (self-contained)."""
from __future__ import annotations

from pathlib import Path

import cv2
import torch
from torch.utils.data import Dataset


class RadarSegmentationDataset(Dataset):
    """Load paired tile + binary-mask images for U-Net training."""

    def __init__(
        self,
        image_dir: str | Path,
        mask_dir: str | Path,
        transforms=None,
    ):
        self.image_dir = Path(image_dir)
        self.mask_dir = Path(mask_dir)
        self.image_paths = sorted(self.image_dir.glob("*.png"))
        self.transforms = transforms

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        mask_path = self.mask_dir / img_path.name

        image = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
        mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)

        if self.transforms:
            transformed = self.transforms(image=image, mask=mask)
            image, mask = transformed["image"], transformed["mask"]

        image = torch.from_numpy(image).unsqueeze(0).float() / 255.0
        mask = torch.from_numpy(mask).unsqueeze(0).float() / 255.0
        return image, mask
