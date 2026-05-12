"""Morphological detection pipeline: Otsu binarization -> opening -> connected components."""

import cv2
import numpy as np
from skimage.filters import threshold_otsu

from .utils import binary_mask_to_bboxes_with_props, binary_mask_to_bboxes_with_scores


def detect_morphological(
    image: np.ndarray,
    opening_kernel_size: int = 3,
    opening_iterations: int = 1,
    closing_kernel_size: int = 5,
    closing_iterations: int = 1,
    min_area: int = 20,
    max_area: int = 50000,
    min_eccentricity: float = 0.0,
    max_eccentricity: float = 0.99,
    dilation: int = 0,
    box_padding: int = 0,
) -> tuple[np.ndarray, np.ndarray, list[dict], np.ndarray]:
    """Morphological detection pipeline.

    Pipeline: Otsu threshold (on non-zero pixels only) -> opening -> closing ->
    dilation -> connected components with region property filtering + box padding.

    Args:
        image: Grayscale input image (uint8 or float [0,1]).

    Returns:
        Tuple of (bboxes, binary_mask, region_properties, scores).
    """
    if image.dtype in (np.float32, np.float64):
        img_u8 = (image * 255).astype(np.uint8)
    else:
        img_u8 = image.copy()

    # Compute Otsu threshold only on non-zero pixels (masked images have zeros outside PPI)
    nonzero = img_u8[img_u8 > 0]
    if len(nonzero) < 100:
        empty = np.zeros((0, 4), dtype=np.float32)
        return empty, np.zeros_like(img_u8), [], np.zeros(0, dtype=np.float32)

    thresh = threshold_otsu(nonzero)
    # Apply threshold only where pixels are non-zero (inside PPI)
    binary = ((img_u8 > thresh) & (img_u8 > 0)).astype(np.uint8)

    # Morphological opening to remove noise
    kernel_open = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (opening_kernel_size, opening_kernel_size)
    )
    opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_open, iterations=opening_iterations)

    # Morphological closing to fill gaps
    kernel_close = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (closing_kernel_size, closing_kernel_size)
    )
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel_close, iterations=closing_iterations)

    # Connected component extraction with property filtering
    bboxes, props = binary_mask_to_bboxes_with_props(
        closed,
        min_area=min_area,
        max_area=max_area,
        min_eccentricity=min_eccentricity,
        max_eccentricity=max_eccentricity,
    )

    # Scores
    threshold_map = np.full(closed.shape, float(thresh), dtype=np.float32)
    _, scores = binary_mask_to_bboxes_with_scores(
        closed,
        img_u8.astype(np.float32),
        threshold_map=threshold_map,
        min_area=min_area,
        max_area=max_area,
        dilation=dilation,
        box_padding=box_padding,
    )

    # Re-extract bboxes with dilation and padding for the actual output
    from .utils import binary_mask_to_bboxes
    bboxes = binary_mask_to_bboxes(
        closed, min_area=min_area, max_area=max_area,
        dilation=dilation, box_padding=box_padding,
    )

    return bboxes, closed, props, scores
