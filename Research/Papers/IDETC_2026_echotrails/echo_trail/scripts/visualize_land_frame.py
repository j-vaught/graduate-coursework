#!/usr/bin/env python3
"""Visualize Charleston land frames as polar radar images."""

import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import csv


def load_land_frame(csv_path: Path) -> np.ndarray:
    """Load a land frame CSV into a 2D array (angles x range bins)."""
    rows = []
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)  # skip header
        # Find where echo values start (column index 6 onward)
        for row in reader:
            # Columns: Status, Scale, Range, Gain, Angle, EchoValues, 1, 2, ...
            echo_values = [int(v) for v in row[6:]]
            rows.append(echo_values)
    return np.array(rows, dtype=np.uint8)


def render_polar(data: np.ndarray) -> np.ndarray:
    """Convert polar spoke data to a Cartesian image."""
    n_spokes, n_bins = data.shape
    size = n_bins * 2
    img = np.zeros((size, size), dtype=np.uint8)
    cx, cy = size // 2, size // 2

    for i in range(n_spokes):
        angle_rad = (i / n_spokes) * 2 * np.pi
        for j in range(n_bins):
            if data[i, j] == 0:
                continue
            x = int(cx + j * np.sin(angle_rad))
            y = int(cy - j * np.cos(angle_rad))
            if 0 <= x < size and 0 <= y < size:
                img[y, x] = max(img[y, x], data[i, j])

    return img


def main():
    land_dir = Path("/Volumes/MacShare/Code/Generative_Radar/Composite_tier/data/land_frames_charleston")
    out_dir = Path("/Volumes/MacShare/graduate-coursework/Research/Papers/IDETC_2026_echotrails/echo_trail/scripts/land_frame_previews")
    out_dir.mkdir(exist_ok=True)

    files = sorted(land_dir.glob("*.csv"))
    # Show first 6 frames as a grid
    n_show = min(6, len(files))

    fig, axes = plt.subplots(2, 3, figsize=(15, 10), facecolor="black")
    fig.suptitle(f"Charleston Land Frames (Composite_tier) — {len(files)} total",
                 color="white", fontsize=14, fontweight="bold")

    for idx, ax in enumerate(axes.flat):
        if idx >= n_show:
            ax.axis("off")
            continue

        f = files[idx]
        data = load_land_frame(f)
        img = render_polar(data)

        ax.imshow(img, cmap="gray", vmin=0, vmax=255)
        ax.set_title(f.stem, color="white", fontsize=8)
        ax.axis("off")

    plt.tight_layout()
    plt.savefig(out_dir / "charleston_land_frames_grid.png", dpi=150,
                bbox_inches="tight", facecolor="black")
    plt.close()
    print(f"Saved grid to {out_dir / 'charleston_land_frames_grid.png'}")

    # Also render a single frame at full res
    data = load_land_frame(files[0])
    img = render_polar(data)
    fig, ax = plt.subplots(1, 1, figsize=(10, 10), facecolor="black")
    ax.imshow(img, cmap="gray", vmin=0, vmax=255)
    ax.set_title(f"Land Frame: {files[0].stem}", color="white", fontsize=12)
    ax.axis("off")
    plt.savefig(out_dir / "charleston_land_frame_single.png", dpi=150,
                bbox_inches="tight", facecolor="black")
    plt.close()
    print(f"Saved single frame to {out_dir / 'charleston_land_frame_single.png'}")


if __name__ == "__main__":
    main()
