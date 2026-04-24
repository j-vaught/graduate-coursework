"""AIS-anchored, image-grounded ground-truth generator.

The DLR ``polarMeas.json`` annotations list per-object boundary points in
polar coordinates and an AIS-derived identity for each object.  The legacy
``polar_to_coco.py`` converter DBSCAN-clusters those points directly, which
is the wrong primitive for radar imagery: radar returns are contiguous
pixel blobs, not sparse point clouds, and DBSCAN produces padded,
uniformly-sized boxes that are not aligned with the actual bright returns.

This module replaces that logic with an *image-grounded* approach:

    1.  Per-target AIS centroid in pixel coordinates (from polar points)
    2.  Threshold the red channel inside the PPI circular mask
    3.  Morphological closing (5x5 ellipse) to bridge vessel-fragmentation
    4.  Connected-component labelling → candidate blobs
    5.  Greedy centroid-to-blob matching within a pixel radius
    6.  Emit each matched blob's tight bounding box as GT

Unclaimed blobs can be returned as an auxiliary *unlabelled-target* list.

The module is self-contained and pure-function where possible; drive it
from a script for a full dataset conversion.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import cv2
import numpy as np

from sklearn.cluster import DBSCAN

from radar_mask import (
    DEFAULT_CENTER_X,
    DEFAULT_CENTER_Y,
    DEFAULT_RADIUS,
    POLAR_ORIGIN_X,
    POLAR_ORIGIN_Y,
    POLAR_RADIUS_PX,
    create_radar_mask,
    extract_radar_signal,
    get_calibration,
)


# ── Constants (tunable) ──────────────────────────────────────────────
INTENSITY_THRESHOLD = 25        # red-channel value above which a pixel is "bright"
CLOSING_KERNEL      = (5, 5)    # ellipse, bridges 1–2 px fragmentation gaps
MIN_BLOB_AREA       = 10        # reject single-pixel speckle
MAX_BLOB_AREA       = 8_000     # reject outer-ring / land blobs
MATCH_RADIUS_PX     = 30        # AIS seed must be within this of a blob centroid
MAX_RANGE_M         = 6000.0    # DLR PPI display range (all three sub-sets)

# Polar DBSCAN: an AIS record bundles many boundary points covering MULTIPLE
# visible vessels. We first DBSCAN-split that point cloud in metres so each
# resulting sub-cluster seeds one image-blob match.
POLAR_DBSCAN_EPS_M      = 200.0
POLAR_DBSCAN_MIN_SAMPLE = 5

# Per-dataset match radius. After discovering and fixing the MANV range-
# scale bug (MANV uses 6 m/px vs. 11 m/px for DAAN/DARC per Boettcher &
# Eichler 2021), all three sub-datasets reach median AIS-to-blob offsets
# of 5–7 px. A 20-px radius is now tight enough to reject wrong matches
# in every dataset.
DATASET_MATCH_RADIUS = {
    "DAAN": 20,
    "DARC": 20,
    "MANV": 20,
}


# ── Data classes ─────────────────────────────────────────────────────
@dataclass
class Blob:
    """One connected bright-pixel region."""
    cx: float          # centroid x, pixel coords
    cy: float
    x1: int            # bbox in pixel coords
    y1: int
    x2: int
    y2: int
    area: int
    peak: int          # peak intensity within the blob


@dataclass
class AISObject:
    """AIS-correlated object parsed from polarMeas.json."""
    obj_id: int
    heading: float
    points_polar: list[list[float]]           # [[r_m, θ_rad], ...]
    centroid_px: tuple[float, float] = (0.0, 0.0)


@dataclass
class AISSeed:
    """One AIS-anchored pixel-space seed (cluster from a parent AISObject)."""
    obj_id: int
    heading: float
    cluster_idx: int
    centroid_px: tuple[float, float]
    n_points: int


@dataclass
class MatchResult:
    """Output of a single-frame AIS→blob matching run."""
    matched: list[tuple[AISSeed, Blob]] = field(default_factory=list)
    unclaimed_blobs: list[Blob] = field(default_factory=list)
    unmatched_ais:  list[AISSeed] = field(default_factory=list)


# ── Polar parsing and projection ─────────────────────────────────────
def parse_frame_annotations(frame_entry: list) -> list[AISObject]:
    """Walk the flat ``[obj_id, heading, [r, θ], …]`` list into objects.

    Integer elements introduce a new object; subsequent list elements are
    its boundary points until the next integer.
    """
    objs: list[AISObject] = []
    i = 0
    n = len(frame_entry)
    while i < n:
        v = frame_entry[i]
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            # Accept both ints and floats for the id — the spec is "integer"
            # but some rows carry 0.0.
            if not isinstance(v, int):
                # Heuristic: identifiers are integers, floats are points.
                # Real data shows ids are always ints.
                i += 1
                continue
            obj_id = int(v)
            heading = float(frame_entry[i + 1]) if i + 1 < n else 0.0
            i += 2
            pts: list[list[float]] = []
            while i < n and isinstance(frame_entry[i], list):
                pts.append([float(frame_entry[i][0]), float(frame_entry[i][1])])
                i += 1
            objs.append(AISObject(obj_id=obj_id, heading=heading,
                                  points_polar=pts))
        else:
            i += 1
    return objs


def polar_to_pixel(
    r_m: float,
    theta_rad: float,
    cx: int = POLAR_ORIGIN_X,
    cy: int = POLAR_ORIGIN_Y,
    r_px_max: int = POLAR_RADIUS_PX,
    max_range_m: float = MAX_RANGE_M,
) -> tuple[float, float]:
    """Project a single polar boundary point to pixel coordinates.

    Uses the *polar origin* (antenna reference) rather than the visual
    PPI disc centre — these differ by ~17 px in the DLR captures.
    """
    r_px = (r_m / max_range_m) * r_px_max
    px = cx + r_px * np.sin(theta_rad)
    py = cy - r_px * np.cos(theta_rad)
    return float(px), float(py)


def compute_centroids(
    objects: Iterable[AISObject],
    **proj_kwargs,
) -> list[AISObject]:
    """Attach ``centroid_px`` (mean of projected boundary points) to each AIS object."""
    out = []
    for obj in objects:
        if not obj.points_polar:
            continue
        xs: list[float] = []
        ys: list[float] = []
        for r, th in obj.points_polar:
            x, y = polar_to_pixel(r, th, **proj_kwargs)
            xs.append(x); ys.append(y)
        obj.centroid_px = (float(np.mean(xs)), float(np.mean(ys)))
        out.append(obj)
    return out


def split_ais_to_seeds(
    objects: Iterable[AISObject],
    eps_m: float = POLAR_DBSCAN_EPS_M,
    min_samples: int = POLAR_DBSCAN_MIN_SAMPLE,
    **proj_kwargs,
) -> list[AISSeed]:
    """Split each AIS object's point cloud into per-target pixel-space seeds.

    The DLR polar-annotation records a single AIS object by listing the
    boundary points of every visible radar return it correlates with; in a
    frame with 4 vessels each AIS object carries ≈ 300 points spread across
    4 spatially-separated blobs. We DBSCAN-cluster those points in metres
    (preserves the units used by the DLR format) and convert each resulting
    cluster to one pixel-space seed with an averaged centroid.
    """
    seeds: list[AISSeed] = []
    for obj in objects:
        if not obj.points_polar:
            continue
        pts = np.asarray(obj.points_polar, dtype=np.float64)   # (N, 2) [r_m, θ_rad]
        # Project to Cartesian metres so Euclidean distance is meaningful.
        xs_m = pts[:, 0] * np.sin(pts[:, 1])
        ys_m = pts[:, 0] * np.cos(pts[:, 1])
        xy_m = np.column_stack([xs_m, ys_m])

        if len(xy_m) < min_samples:
            # Too few points to cluster — emit a single seed from their mean.
            cxm, cym = xy_m.mean(axis=0)
            r_m  = float(np.hypot(cxm, cym))
            th   = float(np.arctan2(cxm, cym))
            px, py = polar_to_pixel(r_m, th, **proj_kwargs)
            seeds.append(AISSeed(obj_id=obj.obj_id, heading=obj.heading,
                                 cluster_idx=0, centroid_px=(px, py),
                                 n_points=len(xy_m)))
            continue

        labels = DBSCAN(eps=eps_m, min_samples=min_samples).fit(xy_m).labels_
        for lbl in sorted(set(labels)):
            if lbl == -1:       # DBSCAN noise
                continue
            cluster_xy = xy_m[labels == lbl]
            cxm, cym = cluster_xy.mean(axis=0)
            r_m = float(np.hypot(cxm, cym))
            th  = float(np.arctan2(cxm, cym))
            px, py = polar_to_pixel(r_m, th, **proj_kwargs)
            seeds.append(AISSeed(obj_id=obj.obj_id, heading=obj.heading,
                                 cluster_idx=int(lbl),
                                 centroid_px=(px, py),
                                 n_points=int(len(cluster_xy))))
    return seeds


# ── Image-grounded blob extraction ───────────────────────────────────
def extract_blobs(
    bgr_image: np.ndarray,
    radar_mask: np.ndarray | None = None,
    threshold: int = INTENSITY_THRESHOLD,
    closing_kernel: tuple[int, int] = CLOSING_KERNEL,
    min_area: int = MIN_BLOB_AREA,
    max_area: int = MAX_BLOB_AREA,
    dataset: str | None = None,
) -> list[Blob]:
    """Detect bright connected-component blobs inside the PPI disc.

    ``dataset`` (DAAN / DARC / MANV) selects the colour-isolation strategy
    via ``extract_radar_signal`` — DAAN and DARC use the red channel,
    MANV uses a yellow-hue HSV filter that rejects white UI chrome.
    """
    signal = extract_radar_signal(bgr_image, dataset=dataset)

    # Apply the circular mask so we ignore UI chrome and outside-disc pixels
    if radar_mask is None:
        h, w = signal.shape
        radar_mask = create_radar_mask(h, w)
    signal_masked = cv2.bitwise_and(signal, radar_mask)

    # Binary threshold
    binary = (signal_masked > threshold).astype(np.uint8)

    # Morphological closing to bridge single-vessel fragmentation
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, closing_kernel)
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # Connected components with per-component stats
    n_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        closed, connectivity=8)

    blobs: list[Blob] = []
    for lbl in range(1, n_labels):   # skip background label 0
        x, y, w, h, area = stats[lbl]
        if area < min_area or area > max_area:
            continue
        peak = int(signal_masked[labels == lbl].max())
        cx, cy = centroids[lbl]
        blobs.append(Blob(cx=float(cx), cy=float(cy),
                          x1=int(x), y1=int(y),
                          x2=int(x + w), y2=int(y + h),
                          area=int(area), peak=peak))
    return blobs


# ── Greedy matching ─────────────────────────────────────────────────
def greedy_match(
    ais_seeds: list[AISSeed],
    blobs: list[Blob],
    match_radius: float = MATCH_RADIUS_PX,
) -> MatchResult:
    """Assign each AIS pixel-space seed to its nearest blob within radius."""
    result = MatchResult()
    claimed = [False] * len(blobs)

    # Process seeds with the most supporting boundary points first — they
    # come from well-sampled vessels and deserve priority on close matches.
    for seed in sorted(ais_seeds, key=lambda s: -s.n_points):
        acx, acy = seed.centroid_px
        best_idx = -1
        best_d = match_radius
        for i, b in enumerate(blobs):
            if claimed[i]:
                continue
            d = np.hypot(b.cx - acx, b.cy - acy)
            if d < best_d:
                best_d = d; best_idx = i
        if best_idx >= 0:
            claimed[best_idx] = True
            result.matched.append((seed, blobs[best_idx]))
        else:
            result.unmatched_ais.append(seed)

    result.unclaimed_blobs = [b for b, c in zip(blobs, claimed) if not c]
    return result


# ── High-level frame processing ─────────────────────────────────────
def process_frame(
    bgr_image: np.ndarray,
    frame_entry: list | None,
    radar_mask: np.ndarray | None = None,
    dataset: str | None = None,
    **kwargs,
) -> MatchResult:
    """End-to-end: parse a frame's polar annotations, split each AIS record
    into per-target seeds (using per-dataset polar calibration), extract
    bright blobs (with per-dataset colour isolation), greedy-match and
    return the match result."""
    objects = parse_frame_annotations(frame_entry or [])
    # Per-dataset polar calibration (antenna origin + display range)
    cal = get_calibration(dataset)
    seeds = split_ais_to_seeds(
        objects,
        eps_m=kwargs.get("polar_eps_m", POLAR_DBSCAN_EPS_M),
        min_samples=kwargs.get("polar_min_samples", POLAR_DBSCAN_MIN_SAMPLE),
        cx=cal["cx"], cy=cal["cy"],
        r_px_max=cal["r_px_max"],
        max_range_m=cal["max_range_m"],
    )
    blobs = extract_blobs(
        bgr_image, radar_mask=radar_mask, dataset=dataset,
        **{k: v for k, v in kwargs.items()
           if k in {"threshold", "closing_kernel", "min_area", "max_area"}},
    )
    # Dataset-aware match radius (unless overridden explicitly)
    match_r = kwargs.get("match_radius")
    if match_r is None:
        match_r = DATASET_MATCH_RADIUS.get((dataset or "").upper(),
                                           MATCH_RADIUS_PX)
    return greedy_match(seeds, blobs, match_radius=match_r)


# ── Dataset-level COCO conversion ───────────────────────────────────
def convert_dataset(
    dataset_dir: Path | str,
    dataset_name: str,
    include_unclaimed: bool = False,
    **kwargs,
) -> dict:
    """Produce a COCO-format annotation dict from a DLR sub-dataset."""
    dataset_dir = Path(dataset_dir)
    polar_path = dataset_dir / "polarMeas.json"
    images_dir = dataset_dir / "radarImages"

    with open(polar_path) as f:
        polar_data = json.load(f)

    coco: dict = {
        "images": [],
        "annotations": [],
        "categories": [
            {"id": 1, "name": "vessel"},
            {"id": 2, "name": "unlabelled"},
        ] if include_unclaimed else [{"id": 1, "name": "vessel"}],
    }

    image_id = 1
    ann_id = 1
    radar_mask = create_radar_mask(1024, 1050)

    for key in sorted(polar_data.keys(), key=lambda k: int(k)):
        frame_num = int(key)
        fname = f"{frame_num:03d}.png"
        img_path = images_dir / fname
        if not img_path.exists():
            continue

        bgr = cv2.imread(str(img_path))
        if bgr is None:
            continue

        frame_entry = polar_data[key]
        if frame_entry is None:
            continue

        result = process_frame(bgr, frame_entry, radar_mask=radar_mask,
                               dataset=dataset_name, **kwargs)

        out_fname = f"{dataset_name}_{fname}"
        coco["images"].append({
            "id": image_id,
            "file_name": out_fname,
            "width": 1050,
            "height": 1024,
            "frame": frame_num,
            "dataset": dataset_name,
        })

        # Matched AIS targets
        for seed, blob in result.matched:
            bw = blob.x2 - blob.x1
            bh = blob.y2 - blob.y1
            coco["annotations"].append({
                "id": ann_id,
                "image_id": image_id,
                "category_id": 1,
                "bbox": [blob.x1, blob.y1, bw, bh],
                "area": int(bw * bh),
                "iscrowd": 0,
                "segmentation": [],
                "ais_obj_id": seed.obj_id,
                "ais_cluster": seed.cluster_idx,
                "heading": seed.heading,
                "blob_peak": blob.peak,
            })
            ann_id += 1

        # Optional: unclaimed blobs as category-2
        if include_unclaimed:
            for blob in result.unclaimed_blobs:
                bw = blob.x2 - blob.x1
                bh = blob.y2 - blob.y1
                coco["annotations"].append({
                    "id": ann_id,
                    "image_id": image_id,
                    "category_id": 2,
                    "bbox": [blob.x1, blob.y1, bw, bh],
                    "area": int(bw * bh),
                    "iscrowd": 0,
                    "segmentation": [],
                    "blob_peak": blob.peak,
                })
                ann_id += 1

        image_id += 1

    return coco


def convert_all_datasets(
    raw_dir: Path | str,
    datasets: list[str] | None = None,
    **kwargs,
) -> dict:
    """Merge DAAN+DARC+MANV with globally unique image / annotation ids."""
    raw_dir = Path(raw_dir)
    datasets = datasets or ["DAAN", "DARC", "MANV"]
    merged = {
        "images": [],
        "annotations": [],
        "categories": [{"id": 1, "name": "vessel"}],
    }
    img_off = 0
    ann_off = 0
    for ds in datasets:
        d = raw_dir / ds
        if not (d / "polarMeas.json").exists():
            continue
        sub = convert_dataset(d, ds, **kwargs)
        id_map = {}
        for img in sub["images"]:
            new_id = img["id"] + img_off
            id_map[img["id"]] = new_id
            merged["images"].append({**img, "id": new_id})
        for ann in sub["annotations"]:
            merged["annotations"].append({
                **ann,
                "id": ann["id"] + ann_off,
                "image_id": id_map[ann["image_id"]],
            })
        if sub["images"]:
            img_off = max(i["id"] for i in merged["images"])
        if sub["annotations"]:
            ann_off = max(a["id"] for a in merged["annotations"])
        merged["categories"] = sub["categories"]   # take last (consistent)
    return merged
