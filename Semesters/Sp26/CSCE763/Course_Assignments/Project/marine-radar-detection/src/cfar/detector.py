"""CFAR (Constant False Alarm Rate) detectors for marine radar.

Implements CA-CFAR, GO-CFAR, SO-CFAR, and OS-CFAR with 2D sliding reference windows.
"""

import numpy as np
from scipy.ndimage import uniform_filter

from .utils import binary_mask_to_bboxes, binary_mask_to_bboxes_with_scores


def _cfar_threshold_map(
    image: np.ndarray,
    guard: tuple[int, int],
    ref: tuple[int, int],
    pfa: float,
    mode: str = "CA",
    k_os: float = 0.75,
) -> np.ndarray:
    """Compute CFAR threshold map using efficient convolution-based estimation.

    Args:
        image: Input intensity image (float).
        guard: (guard_h, guard_w) half-sizes.
        ref: (ref_h, ref_w) half-sizes.
        pfa: Probability of false alarm.
        mode: One of 'CA', 'GO', 'SO', 'OS'.
        k_os: Order statistic fraction for OS-CFAR.

    Returns:
        Threshold map same shape as image.
    """
    gh, gw = guard
    rh, rw = ref

    ref_size = (2 * rh + 1, 2 * rw + 1)
    guard_size = (2 * gh + 1, 2 * gw + 1)

    if mode == "OS":
        return _os_cfar_threshold(image, guard, ref, pfa, k_os)

    # Number of reference cells
    n_ref = ref_size[0] * ref_size[1] - guard_size[0] * guard_size[1]
    # CFAR scaling factor (exponential assumption)
    alpha = n_ref * (pfa ** (-1.0 / n_ref) - 1)

    # Estimate local mean via convolution difference
    ref_sum = uniform_filter(image, size=ref_size, mode="reflect") * (ref_size[0] * ref_size[1])
    guard_sum = uniform_filter(image, size=guard_size, mode="reflect") * (
        guard_size[0] * guard_size[1]
    )
    background = (ref_sum - guard_sum) / max(n_ref, 1)

    if mode == "CA":
        threshold = alpha * background
    elif mode == "GO":
        # Greatest-of: use the max of leading/lagging half-window estimates
        # Split the reference window vertically around the CUT
        lead_size = (rh + gh + 1, 2 * rw + 1)
        lag_size = (rh + gh + 1, 2 * rw + 1)
        lead_origin = min((lead_size[0] - 1) // 2, rh // 2)
        leading = uniform_filter(image, size=lead_size, mode="reflect", origin=(-lead_origin, 0))
        lagging = uniform_filter(image, size=lag_size, mode="reflect", origin=(lead_origin, 0))
        threshold = alpha * np.maximum(leading, lagging)
    elif mode == "SO":
        lead_size = (rh + gh + 1, 2 * rw + 1)
        lag_size = (rh + gh + 1, 2 * rw + 1)
        lead_origin = min((lead_size[0] - 1) // 2, rh // 2)
        leading = uniform_filter(image, size=lead_size, mode="reflect", origin=(-lead_origin, 0))
        lagging = uniform_filter(image, size=lag_size, mode="reflect", origin=(lead_origin, 0))
        threshold = alpha * np.minimum(leading, lagging)
    else:
        raise ValueError(f"Unknown CFAR mode: {mode}")

    return threshold


def _os_cfar_threshold(
    image: np.ndarray,
    guard: tuple[int, int],
    ref: tuple[int, int],
    pfa: float,
    k_frac: float = 0.75,
) -> np.ndarray:
    """OS-CFAR via sliding window (slower, but exact)."""
    from skimage.util import view_as_windows

    gh, gw = guard
    rh, rw = ref
    h, w = image.shape

    # Pad image
    pad_h, pad_w = rh, rw
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode="reflect")

    threshold = np.zeros_like(image)
    win_h = 2 * rh + 1
    win_w = 2 * rw + 1

    guard_mask = np.ones((win_h, win_w), dtype=bool)
    cy, cx = rh, rw
    guard_mask[cy - gh: cy + gh + 1, cx - gw: cx + gw + 1] = False
    n_ref = guard_mask.sum()
    k_idx = int(k_frac * n_ref)
    alpha = n_ref * (pfa ** (-1.0 / n_ref) - 1)

    for i in range(h):
        for j in range(w):
            window = padded[i: i + win_h, j: j + win_w]
            ref_cells = window[guard_mask]
            sorted_cells = np.sort(ref_cells)
            threshold[i, j] = alpha * sorted_cells[min(k_idx, len(sorted_cells) - 1)]

    return threshold


def detect_cfar(
    image: np.ndarray,
    guard: tuple[int, int] = (3, 3),
    ref: tuple[int, int] = (10, 10),
    pfa: float = 1e-4,
    mode: str = "CA",
    k_os: float = 0.75,
    min_area: int = 20,
    dilation: int = 0,
    box_padding: int = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Run CFAR detection.

    Args:
        image: Input radar intensity image.
        guard: Guard cell half-sizes (rows, cols).
        ref: Reference window half-sizes.
        pfa: Probability of false alarm.
        mode: 'CA', 'GO', 'SO', or 'OS'.
        k_os: Order statistic rank fraction (OS-CFAR only).
        min_area: Minimum connected component area.
        dilation: Dilate binary mask before component extraction.
        box_padding: Pad each output box by this many pixels per side.

    Returns:
        Tuple of (bboxes, binary_mask, scores).
    """
    threshold = _cfar_threshold_map(image, guard, ref, pfa, mode, k_os)
    # Only detect where image has actual signal (not masked zeros)
    mask = ((image > threshold) & (image > 0)).astype(np.uint8)
    bboxes, scores = binary_mask_to_bboxes_with_scores(
        mask, image, threshold_map=threshold, min_area=min_area,
        dilation=dilation, box_padding=box_padding,
    )
    return bboxes, mask, scores
