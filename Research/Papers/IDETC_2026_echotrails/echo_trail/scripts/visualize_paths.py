#!/usr/bin/env python3
"""Visualize object paths from a scene YAML on the water mask.

Renders each object's full trajectory as a colored line on the Cartesian
water mask image. Color-codes by speed class and annotates frame numbers.

Usage:
    python visualize_paths.py scene.yaml -o preview.png
    python visualize_paths.py scenes/a1_trail_length/*.yaml -o outputs/path_previews/
"""

import argparse
import math
import os
import random
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection
import numpy as np

# Add radar-scene-augmentation to path
PIPELINE_DIR = Path("/Volumes/MacShare/Code/radar-scene-augmentation/scene-generator")
sys.path.insert(0, str(PIPELINE_DIR))

from radar_core.annotations import AnnotationSet
from radar_core.converter import ConversionConfig, RadarConverter
from radar_core.csv_handler import NUM_RANGE_BINS
from radar_core.mask import BinaryMask, PolarMask, create_water_mask
from radar_core.motion import generate_path
from radar_core.scene import load_scene
from pipeline.data_loader import compute_valid_positions, find_water_edge_positions

# Default data paths
DATA_DIR = Path("/Volumes/MacShare/Code/radar-scene-augmentation/data")
DEFAULT_ANNOTATION = DATA_DIR / "annotation_charleston.json"

# Speed class thresholds (px/frame in polar space)
SPEED_CLASSES = {
    "stationary": (0.0, 0.01),
    "slow":       (0.01, 3.5),
    "medium":     (3.5, 8.0),
    "fast":       (8.0, float("inf")),
}

# Brand-aligned colors per speed class
SPEED_COLORS = {
    "stationary": "#FFFFFF",
    "slow":       "#466A9F",
    "medium":     "#A49137",
    "fast":       "#CC2E40",
}


def classify_speed(speed_val):
    """Map a speed value to its speed class name."""
    if isinstance(speed_val, str):
        return "medium"
    s = float(speed_val)
    for cls_name, (lo, hi) in SPEED_CLASSES.items():
        if lo <= s < hi:
            return cls_name
    return "fast"


def load_water_mask(annotation_path):
    """Load annotation and build water mask + converter."""
    annotations = AnnotationSet.load(str(annotation_path))
    config = ConversionConfig()
    converter = RadarConverter(config)
    size = converter.image_size()
    num_pulses = converter.num_pulses()

    water_mask_cart = create_water_mask(annotations, size, size)
    polar_water_mask = PolarMask.from_cartesian(water_mask_cart, converter)

    return converter, polar_water_mask, size, num_pulses


def build_cartesian_mask_image(converter, polar_mask, size):
    """Render water mask as an RGB image (blue=water, dark=land)."""
    cart_flat = converter.polar_mask_to_cartesian(polar_mask.data)
    cart_2d = cart_flat.reshape((size, size))

    img = np.zeros((size, size, 3), dtype=np.uint8)
    img[cart_2d, 0] = 15
    img[cart_2d, 1] = 25
    img[cart_2d, 2] = 50
    img[~cart_2d] = [10, 10, 10]

    return img


def polar_to_cartesian_xy(pulse_idx, bin_idx, converter):
    """Convert a polar (pulse, bin) position to Cartesian (x, y)."""
    num_pulses = converter.num_pulses()
    angle_rad = (pulse_idx / num_pulses) * 2.0 * math.pi
    x, y = converter.polar_to_cartesian_point(angle_rad, bin_idx)
    return x, y


def generate_all_paths(scene_config, polar_mask, num_pulses, margin=30):
    """Generate paths for all object groups in a scene config.

    Returns list of dicts with keys: name, positions, start_frame, end_frame,
    speed_class, speed_val, path_type.
    """
    valid_positions = compute_valid_positions(polar_mask, num_pulses, margin)
    edge_positions = find_water_edge_positions(polar_mask, num_pulses)

    seed = scene_config.seed if scene_config.seed is not None else 42
    rng = random.Random(seed)
    total_frames = scene_config.count

    tracks = []
    for group in scene_config.objects:
        path_type = group.path.type

        if path_type == "fixed":
            speed_val = 0.0
        else:
            speed_val = group.path.speed

        speed_class = classify_speed(speed_val)

        for i in range(group.count):
            try:
                positions, start_frame, end_frame = generate_path(
                    group.path, total_frames, valid_positions, edge_positions,
                    polar_mask, num_pulses, rng, allow_land=False,
                )
            except ValueError as e:
                print(f"  WARNING: Path generation failed for {group.name} #{i}: {e}")
                continue

            tracks.append({
                "name": f"{group.name}_{i}",
                "group": group.name,
                "positions": positions,
                "start_frame": start_frame,
                "end_frame": end_frame,
                "speed_class": speed_class,
                "speed_val": speed_val,
                "path_type": path_type,
            })

    return tracks


def render_paths(tracks, converter, bg_image, total_frames, output_path):
    """Render all tracks on the background image and save as PNG."""
    size = bg_image.shape[0]
    dpi = 150
    fig_inches = size / dpi

    fig, ax = plt.subplots(1, 1, figsize=(fig_inches, fig_inches), dpi=dpi)
    ax.imshow(bg_image, origin="upper", interpolation="nearest")
    ax.set_xlim(0, size)
    ax.set_ylim(size, 0)
    ax.axis("off")

    # Count objects per speed class
    class_counts = {"stationary": 0, "slow": 0, "medium": 0, "fast": 0}

    for track in tracks:
        positions = track["positions"]
        if not positions:
            continue

        speed_class = track["speed_class"]
        class_counts[speed_class] += 1
        color = SPEED_COLORS[speed_class]

        # Convert all positions to cartesian
        xs, ys = [], []
        for pulse, bin_idx in positions:
            x, y = polar_to_cartesian_xy(pulse, bin_idx, converter)
            xs.append(x)
            ys.append(y)

        if len(xs) < 2:
            # Single point — just draw a dot
            ax.plot(xs[0], ys[0], "o", color=color, markersize=3, zorder=5)
            continue

        # Draw path line
        ax.plot(xs, ys, color=color, linewidth=1.0, alpha=0.8, zorder=3)

        # Start dot
        ax.plot(xs[0], ys[0], "o", color=color, markersize=4, zorder=5)

        # End arrow
        dx = xs[-1] - xs[-2]
        dy = ys[-1] - ys[-2]
        length = math.sqrt(dx * dx + dy * dy)
        if length > 0:
            scale = min(15, length)
            ax.annotate(
                "", xy=(xs[-1], ys[-1]),
                xytext=(xs[-1] - dx / length * scale, ys[-1] - dy / length * scale),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.5),
                zorder=5,
            )

        # Frame number annotations at intervals
        n_positions = len(positions)
        interval = max(1, n_positions // 5)
        for idx in range(0, n_positions, interval):
            frame_num = track["start_frame"] + idx
            ax.text(
                xs[idx], ys[idx] - 8, str(frame_num),
                color=color, fontsize=3, ha="center", va="bottom",
                alpha=0.7, zorder=4,
            )

    # Legend
    legend_handles = []
    for cls_name in ["stationary", "slow", "medium", "fast"]:
        count = class_counts[cls_name]
        if count > 0:
            patch = mpatches.Patch(
                color=SPEED_COLORS[cls_name],
                label=f"{cls_name} ({count})",
            )
            legend_handles.append(patch)

    if legend_handles:
        legend = ax.legend(
            handles=legend_handles,
            loc="upper left",
            fontsize=6,
            framealpha=0.7,
            facecolor="#1a1a1a",
            edgecolor="#363636",
            labelcolor="white",
        )
        legend.get_frame().set_linewidth(0.5)

    # Title
    scene_name = Path(output_path).stem
    total_objects = sum(class_counts.values())
    ax.set_title(
        f"{scene_name}  |  {total_objects} objects  |  {total_frames} frames",
        color="white", fontsize=8, pad=4,
    )

    fig.patch.set_facecolor("#000000")
    fig.tight_layout(pad=0.5)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    fig.savefig(output_path, dpi=dpi, facecolor="#000000", bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {output_path}")


def visualize_scene(scene_yaml, output_path, annotation_path):
    """Full pipeline: load mask, parse scene, generate paths, render."""
    print(f"\nProcessing: {scene_yaml}")

    # Load water mask
    converter, polar_mask, size, num_pulses = load_water_mask(annotation_path)
    bg_image = build_cartesian_mask_image(converter, polar_mask, size)

    # Parse scene
    scene_config = load_scene(str(scene_yaml))
    total_frames = scene_config.count

    # Generate paths
    tracks = generate_all_paths(scene_config, polar_mask, num_pulses)
    print(f"  Generated {len(tracks)} tracks")

    # Render
    render_paths(tracks, converter, bg_image, total_frames, output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Visualize object paths from scene YAML on water mask."
    )
    parser.add_argument(
        "scenes", nargs="+", type=Path,
        help="One or more scene YAML files to visualize.",
    )
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("outputs/path_previews"),
        help="Output path. If a directory, PNGs are named after the YAML stem.",
    )
    parser.add_argument(
        "--annotation", type=Path, default=DEFAULT_ANNOTATION,
        help="Path to annotation JSON for water mask.",
    )
    args = parser.parse_args()

    for scene_yaml in args.scenes:
        if not scene_yaml.exists():
            print(f"  [error] Scene not found: {scene_yaml}")
            continue

        if args.output.suffix in (".png", ".jpg"):
            out_path = args.output
        else:
            out_path = args.output / f"{scene_yaml.stem}.png"

        visualize_scene(scene_yaml, str(out_path), args.annotation)


if __name__ == "__main__":
    main()
