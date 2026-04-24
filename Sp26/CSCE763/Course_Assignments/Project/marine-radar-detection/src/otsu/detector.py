"""Otsu and SSOTSU (Speed-up Seed Point Otsu) for small-target detection."""

import cv2
import numpy as np
from skimage.filters import threshold_otsu

from .utils import binary_mask_to_bboxes, binary_mask_to_bboxes_with_scores

# The new image-grounded GT uses tight blob bounding boxes (no synthetic
# padding), so classical outputs should also emit tight boxes without
# dilation/padding to match IoU at 0.50.
DEFAULT_DILATION = 0
DEFAULT_BOX_PADDING = 0


def detect_otsu(
    image: np.ndarray,
    min_area: int = 10,
    max_area: int = 50000,
    dilation: int = DEFAULT_DILATION,
    box_padding: int = DEFAULT_BOX_PADDING,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Basic Otsu thresholding + connected component detection.

    Computes Otsu threshold on non-zero pixels only (handles masked images).
    """
    if image.dtype in (np.float32, np.float64):
        img_u8 = (image * 255).astype(np.uint8)
    else:
        img_u8 = image.copy()

    # Compute threshold on non-zero pixels only
    nonzero = img_u8[img_u8 > 0]
    if len(nonzero) < 100:
        empty = np.zeros((0, 4), dtype=np.float32)
        return empty, np.zeros_like(img_u8), np.zeros(0, dtype=np.float32)

    thresh = threshold_otsu(nonzero)
    binary = ((img_u8 > thresh) & (img_u8 > 0)).astype(np.uint8)

    bboxes = binary_mask_to_bboxes(
        binary, min_area=min_area, max_area=max_area,
        dilation=dilation, box_padding=box_padding,
    )

    threshold_map = np.full(binary.shape, float(thresh), dtype=np.float32)
    _, scores = binary_mask_to_bboxes_with_scores(
        binary, img_u8.astype(np.float32), threshold_map=threshold_map,
        min_area=min_area, max_area=max_area,
        dilation=dilation, box_padding=box_padding,
    )
    return bboxes, binary, scores


def detect_ssotsu(
    image: np.ndarray,
    block_size: int = 64,
    seed_threshold_factor: float = 1.5,
    region_grow_threshold: float = 0.8,
    min_area: int = 5,
    max_area: int = 50000,
    dilation: int = DEFAULT_DILATION,
    box_padding: int = DEFAULT_BOX_PADDING,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """SSOTSU: Speed-up Seed Point Otsu method for small target detection.

    Computes local Otsu on non-zero pixels only per block.
    """
    if image.dtype in (np.float32, np.float64):
        img_u8 = (image * 255).astype(np.uint8)
    else:
        img_u8 = image.copy()

    h, w = img_u8.shape
    seed_mask = np.zeros((h, w), dtype=np.uint8)

    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            block = img_u8[y: min(y + block_size, h), x: min(x + block_size, w)]
            nonzero_block = block[block > 0]
            if len(nonzero_block) < 10 or nonzero_block.std() < 1:
                continue
            try:
                local_thresh = threshold_otsu(nonzero_block)
            except ValueError:
                continue
            seed_thresh = local_thresh * seed_threshold_factor
            local_seeds = (block > seed_thresh) & (block > 0)
            seed_mask[y: y + block.shape[0], x: x + block.shape[1]] = local_seeds.astype(np.uint8)

    # Region growing
    result_mask = np.zeros_like(seed_mask)
    seed_points = np.argwhere(seed_mask > 0)
    visited = np.zeros_like(seed_mask, dtype=bool)

    for sy, sx in seed_points:
        if visited[sy, sx]:
            continue

        seed_intensity = float(img_u8[sy, sx])
        grow_thresh = seed_intensity * region_grow_threshold

        stack = [(sy, sx)]
        while stack:
            cy, cx = stack.pop()
            if cy < 0 or cy >= h or cx < 0 or cx >= w:
                continue
            if visited[cy, cx]:
                continue
            if img_u8[cy, cx] < grow_thresh:
                continue

            visited[cy, cx] = True
            result_mask[cy, cx] = 1

            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                    stack.append((ny, nx))

    bboxes = binary_mask_to_bboxes(
        result_mask, min_area=min_area, max_area=max_area,
        dilation=dilation, box_padding=box_padding,
    )

    # Build threshold map for scoring
    thresh_map = np.zeros(img_u8.shape, dtype=np.float32)
    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            block = img_u8[y: min(y + block_size, h), x: min(x + block_size, w)]
            nonzero_block = block[block > 0]
            if len(nonzero_block) < 10 or nonzero_block.std() < 1:
                local_t = 1.0
            else:
                try:
                    local_t = float(threshold_otsu(nonzero_block)) * seed_threshold_factor
                except ValueError:
                    local_t = 1.0
            thresh_map[y: y + block.shape[0], x: x + block.shape[1]] = max(local_t, 1.0)

    _, scores = binary_mask_to_bboxes_with_scores(
        result_mask, img_u8.astype(np.float32), threshold_map=thresh_map,
        min_area=min_area, max_area=max_area,
        dilation=dilation, box_padding=box_padding,
    )
    return bboxes, result_mask, scores
