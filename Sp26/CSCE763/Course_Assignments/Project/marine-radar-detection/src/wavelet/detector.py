"""Wavelet-based target detection using 2D Stationary Wavelet Transform."""

import numpy as np
import pywt

from .utils import binary_mask_to_bboxes, binary_mask_to_bboxes_with_scores


def detect_wavelet(
    image: np.ndarray,
    wavelet: str = "db4",
    level: int = 3,
    threshold_sigma: float = 3.0,
    subbands: list[str] | None = None,
    combine_mode: str = "max",
    min_area: int = 15,
    max_area: int = 50000,
    dilation: int = 0,
    box_padding: int = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Detect targets using 2D stationary wavelet transform.

    Target energy concentrates in high-frequency subbands while sea clutter
    is distributed across scales. Thresholding the HF coefficients isolates targets.

    Args:
        image: Grayscale input image (float [0,1] or uint8).
        wavelet: Wavelet family name.
        level: Number of decomposition levels.
        threshold_sigma: Threshold = mean + sigma * std of each subband.
        subbands: Which detail subbands to use ('LH', 'HL', 'HH').
        combine_mode: How to combine subbands ('max', 'sum', 'or').
        min_area: Minimum connected component area.

    Returns:
        Tuple of (bboxes, binary_mask, scores) where scores are normalised
        peak wavelet-coefficient magnitudes per component in [0, 1].
    """
    if subbands is None:
        subbands = ["LH", "HL", "HH"]

    if image.dtype == np.uint8:
        image = image.astype(np.float32) / 255.0

    # Pad to power of 2 for SWT
    h, w = image.shape
    new_h = int(2 ** np.ceil(np.log2(h)))
    new_w = int(2 ** np.ceil(np.log2(w)))
    padded = np.zeros((new_h, new_w), dtype=np.float32)
    padded[:h, :w] = image

    # 2D Stationary Wavelet Transform
    coeffs = pywt.swt2(padded, wavelet, level=level, trim_approx=True)

    # Combine high-frequency subbands and accumulate peak coefficient magnitude
    subband_map = {"LH": 0, "HL": 1, "HH": 2}
    detection_map = np.zeros((new_h, new_w), dtype=np.float32)
    coeff_magnitude = np.zeros((new_h, new_w), dtype=np.float32)

    for lvl_coeffs in coeffs[1:]:  # skip approximation
        for sb_name in subbands:
            sb_idx = subband_map[sb_name]
            detail = np.abs(lvl_coeffs[sb_idx])

            # Adaptive threshold
            mu = np.mean(detail)
            sigma = np.std(detail)
            thresh = mu + threshold_sigma * sigma
            binary = (detail > thresh).astype(np.float32)

            # Track maximum coefficient magnitude across subbands/levels
            coeff_magnitude = np.maximum(coeff_magnitude, detail)

            if combine_mode == "max":
                detection_map = np.maximum(detection_map, binary)
            elif combine_mode == "sum":
                detection_map += binary
            elif combine_mode == "or":
                detection_map = np.clip(detection_map + binary, 0, 1)

    # Crop back to original size
    detection_map = detection_map[:h, :w]
    coeff_magnitude = coeff_magnitude[:h, :w]

    if combine_mode == "sum":
        detection_map = (detection_map > 0).astype(np.uint8)
    else:
        detection_map = detection_map.astype(np.uint8)

    # Scores are derived from peak wavelet coefficient magnitude per component.
    # Normalise coeff_magnitude to [0, 1] so binary_mask_to_bboxes_with_scores
    # uses the mean-intensity path (no threshold_map) with a [0,1] scaled image.
    mag_max = coeff_magnitude.max()
    if mag_max > 0:
        coeff_norm = coeff_magnitude / mag_max
    else:
        coeff_norm = coeff_magnitude

    _, scores = binary_mask_to_bboxes_with_scores(
        detection_map, coeff_norm, threshold_map=None,
        min_area=min_area, max_area=max_area,
        dilation=dilation, box_padding=box_padding,
    )
    bboxes = binary_mask_to_bboxes(
        detection_map, min_area=min_area, max_area=max_area,
        dilation=dilation, box_padding=box_padding,
    )
    return bboxes, detection_map, scores
