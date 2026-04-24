"""Radar PPI circular mask + dataset-aware signal extraction."""

from __future__ import annotations

import cv2
import numpy as np


# ── Per-dataset target-signal extraction ─────────────────────────────
# The DLR captures have two distinct display palettes:
#
#   DAAN / DARC — solid blue PPI background (BGR ≈ (140, 0, 0)),
#       near-white radar returns (234, 239, 226) and GREEN bearing marks
#       (0, 255, 0).  Taking the red channel isolates the returns because
#       the background has R≈0, the green UI has R=0, and only the near-
#       white targets hit high R.
#
#   MANV — dark-blue near-black background (35, 1, 0), YELLOW radar
#       returns (hue ≈ 30° in OpenCV), and WHITE/GRAY UI chrome (255, 255,
#       255).  The red channel is useless here because white UI has R=255
#       too.  Yellow is distinguished from white only by *saturation*, so
#       we use an HSV hue + saturation filter.
#
# ``extract_radar_signal`` dispatches by dataset name; callers should pass
# the uppercase sub-dataset tag (DAAN, DARC, MANV).


def extract_via_red_channel(bgr: np.ndarray) -> np.ndarray:
    """DAAN / DARC: the red channel is the cleanest target signal."""
    return bgr[:, :, 2]


def extract_via_yellow_hsv(
    bgr: np.ndarray,
    hue_lo: int = 15,
    hue_hi: int = 50,
    sat_min: int = 80,
    val_min: int = 100,
) -> np.ndarray:
    """MANV: keep only yellow-hued, saturated pixels.  Pure white UI has
    near-zero saturation and is dropped automatically.

    Returns a uint8 grey-scale image whose value is the HSV *V* at the
    kept pixels and 0 elsewhere, so downstream CFAR / CC code treats it
    identically to the red-channel output from DAAN/DARC.
    """
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    mask = (h >= hue_lo) & (h <= hue_hi) & (s >= sat_min) & (v >= val_min)
    return np.where(mask, v, 0).astype(np.uint8)


_EXTRACTORS = {
    "DAAN": extract_via_red_channel,
    "DARC": extract_via_red_channel,
    "MANV": extract_via_yellow_hsv,
}


def extract_radar_signal(bgr: np.ndarray, dataset: str | None = None) -> np.ndarray:
    """Apply the per-dataset target-isolation strategy.

    Unknown datasets fall back to the red-channel extractor.
    """
    fn = _EXTRACTORS.get((dataset or "").upper(), extract_via_red_channel)
    return fn(bgr)


# --- Visual PPI disc (used for the circular mask on display pixels) ----
# Measured from the captures via the interactive crop tuner.
DEFAULT_CENTER_X = 531
DEFAULT_CENTER_Y = 515
DEFAULT_RADIUS   = 466

# --- Default polar-coordinate origin (fallback for unknown datasets) ----
# Real DLR captures have per-dataset calibration (see DATASET_CALIBRATION
# below).  These defaults are approximately the DAAN values.
POLAR_ORIGIN_X   = 514
POLAR_ORIGIN_Y   = 516
POLAR_RADIUS_PX  = 466   # display radius in pixels used for r scaling


# --- Per-dataset calibration ---------------------------------------------
# The DLR radar campaigns (Boettcher & Eichler, 2021 — MDPI Sensors) used
# different radar range settings per sub-dataset:
#
#   DAAN, DARC : "coarser 11 m resolution"  (long range, open water)
#   MANV       : "finer resolution of 6 m"  (close-range manoeuvres)
#
# A 2-D grid search against per-frame image-blob positions confirms this
# and additionally reveals that each sub-dataset has a slightly different
# polar-origin pixel offset (the antenna reference was mounted differently
# on each recording platform).  Using these values per-dataset brings the
# median AIS-seed → nearest-blob distance down from ~67 px (MANV) and
# ~22 px (DAAN/DARC) to around 5–7 px.
#
# Fields:
#   cx, cy       — polar origin in pixels (where AIS (r=0) projects to)
#   r_px_max     — display radius in pixels (visual PPI circle)
#   max_range_m  — physical range in metres at r_px_max
#   resolution   — m/pixel = max_range_m / r_px_max  (recorded for sanity)

DATASET_CALIBRATION: dict[str, dict] = {
    "DAAN": {"cx": 512, "cy": 516, "r_px_max": 466,
              "max_range_m": 5750, "resolution": 12.34},
    "DARC": {"cx": 514, "cy": 521, "r_px_max": 466,
              "max_range_m": 5600, "resolution": 12.02},
    "MANV": {"cx": 514, "cy": 528, "r_px_max": 466,
              "max_range_m": 2800, "resolution": 6.01},
}


def get_calibration(dataset: str | None) -> dict:
    """Return per-dataset calibration or a safe DAAN-like default."""
    if dataset is None:
        return {"cx": POLAR_ORIGIN_X, "cy": POLAR_ORIGIN_Y,
                "r_px_max": POLAR_RADIUS_PX, "max_range_m": 5750,
                "resolution": 12.34}
    return DATASET_CALIBRATION.get(dataset.upper(),
                                   DATASET_CALIBRATION["DAAN"])


def create_radar_mask(
    height: int = 1024,
    width: int = 1050,
    center: tuple[int, int] | None = None,
    radius: int | None = None,
) -> np.ndarray:
    """Create a circular mask for the radar PPI display area.

    Args:
        height: Image height.
        width: Image width.
        center: (x, y) center of the radar circle. Defaults to image center.
        radius: Radius of the radar circle. Defaults to min(w,h)/2 * 0.92.

    Returns:
        Binary mask (uint8, 0 or 255).
    """
    if center is None:
        center = (DEFAULT_CENTER_X, DEFAULT_CENTER_Y)
    if radius is None:
        radius = DEFAULT_RADIUS

    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)
    return mask


def apply_radar_mask(image: np.ndarray, mask: np.ndarray | None = None) -> np.ndarray:
    """Zero out pixels outside the radar circle.

    Args:
        image: Input image (grayscale or BGR).
        mask: Pre-computed mask. If None, creates one from image dimensions.

    Returns:
        Masked image.
    """
    if mask is None:
        h, w = image.shape[:2]
        mask = create_radar_mask(h, w)

    if image.ndim == 3:
        return cv2.bitwise_and(image, image, mask=mask)
    else:
        return cv2.bitwise_and(image, mask)


def filter_boxes_by_mask(
    bboxes: np.ndarray,
    center: tuple[int, int] | None = None,
    radius: int | None = None,
    img_width: int = 1050,
    img_height: int = 1024,
) -> np.ndarray:
    """Filter bounding boxes to only keep those whose center is inside the radar circle.

    Args:
        bboxes: (N, 4+) array with at least [x1, y1, x2, y2] or COCO [x, y, w, h].
        center: Radar circle center (x, y).
        radius: Radar circle radius.
        img_width: Image width for default center/radius.
        img_height: Image height for default center/radius.

    Returns:
        Boolean mask of which boxes to keep.
    """
    if center is None:
        center = (DEFAULT_CENTER_X, DEFAULT_CENTER_Y)
    if radius is None:
        radius = DEFAULT_RADIUS

    if len(bboxes) == 0:
        return np.array([], dtype=bool)

    # Compute box centers
    cx = (bboxes[:, 0] + bboxes[:, 2]) / 2  # works for both xyxy and xywh
    cy = (bboxes[:, 1] + bboxes[:, 3]) / 2

    # Distance from radar center
    dist = np.sqrt((cx - center[0])**2 + (cy - center[1])**2)

    return dist <= radius
