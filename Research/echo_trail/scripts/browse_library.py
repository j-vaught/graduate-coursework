#!/usr/bin/env python3
"""Browse and filter the radar object library visually.

Creates contact sheet images of library objects grouped by size,
so you can identify good vs bad objects and set filtering thresholds.

Usage:
    python browse_library.py                    # Create overview contact sheets
    python browse_library.py --stats            # Print size/intensity statistics
    python browse_library.py --filter           # Show filtering recommendations
"""

import argparse
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

LIB_DIR = "/Volumes/MacShare/Code/Generative_Radar/Composite_tier/data/object_library_charleston"
OUTPUT_DIR = "/Volumes/MacShare/graduate-coursework/Research/Papers/IDETC_2026_echotrails/echo_trail/outputs/library_preview"


def load_all_objects():
    """Load all objects from library and return sorted list."""
    obj_dir = os.path.join(LIB_DIR, "objects")
    objects = []
    for fname in os.listdir(obj_dir):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(obj_dir, fname)) as f:
            obj = json.load(f)
        objects.append(obj)
    return objects


def render_object(obj, cell_size=64):
    """Render a single object's echo data as a small image."""
    echo_data = obj["echo_data"]
    if not echo_data or len(echo_data) == 0:
        img = Image.new("L", (cell_size, cell_size), 0)
        return img

    # echo_data is a list of pulse dicts, each with echoes
    n_pulses = len(echo_data)
    n_bins = max(len(p.get("echoes", [])) for p in echo_data) if isinstance(echo_data[0], dict) else 0

    if n_bins == 0:
        # Might be a flat list of lists
        if isinstance(echo_data[0], list):
            n_bins = max(len(row) for row in echo_data)
            arr = np.zeros((n_pulses, n_bins), dtype=np.uint8)
            for i, row in enumerate(echo_data):
                for j, val in enumerate(row):
                    arr[i, j] = min(255, int(val))
        else:
            img = Image.new("L", (cell_size, cell_size), 0)
            return img
    else:
        arr = np.zeros((n_pulses, n_bins), dtype=np.uint8)
        for i, pulse in enumerate(echo_data):
            echoes = pulse.get("echoes", [])
            for j, val in enumerate(echoes):
                arr[i, j] = min(255, int(val))

    # Create image from array, resize to cell
    img = Image.fromarray(arr, mode="L")
    # Scale up for visibility
    scale = max(1, cell_size // max(img.width, img.height))
    if scale > 1:
        img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)

    # Pad/crop to cell_size
    canvas = Image.new("L", (cell_size, cell_size), 0)
    x_off = (cell_size - img.width) // 2
    y_off = (cell_size - img.height) // 2
    canvas.paste(img, (max(0, x_off), max(0, y_off)))
    return canvas


def create_contact_sheet(objects, title, filename, cols=20, cell_size=64):
    """Create a contact sheet image of objects."""
    n = len(objects)
    rows = math.ceil(n / cols)
    label_h = 14

    width = cols * cell_size
    height = rows * (cell_size + label_h) + 40  # title bar

    img = Image.new("RGB", (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Title
    draw.text((10, 5), title, fill="white")
    draw.text((10, 20), f"{n} objects", fill=(150, 150, 150))

    y_start = 40
    for i, obj in enumerate(objects):
        col = i % cols
        row = i // cols
        x = col * cell_size
        y = y_start + row * (cell_size + label_h)

        # Render object
        cell = render_object(obj, cell_size)
        img.paste(Image.merge("RGB", [cell, cell, cell]), (x, y))

        # Label: area and mean intensity
        area = obj.get("area", 0)
        mi = obj.get("mean_intensity", 0)
        label = f"a{area}"
        draw.text((x + 2, y + cell_size), label, fill=(100, 200, 100))

    img.save(filename)
    print(f"  Saved: {filename} ({width}x{height})")
    return filename


def compute_fill_ratio(obj):
    """Compute fill ratio: fraction of bounding box pixels that are non-zero."""
    echo_data = obj["echo_data"]
    if not echo_data:
        return 0.0
    n_pulses = len(echo_data)
    if isinstance(echo_data[0], dict):
        n_bins = max(len(p.get("echoes", [])) for p in echo_data)
        if n_bins == 0:
            return 0.0
        total = n_pulses * n_bins
        nonzero = sum(1 for p in echo_data for v in p.get("echoes", []) if v > 0)
    elif isinstance(echo_data[0], list):
        n_bins = max(len(row) for row in echo_data)
        if n_bins == 0:
            return 0.0
        total = n_pulses * n_bins
        nonzero = sum(1 for row in echo_data for v in row if v > 0)
    else:
        return 0.0
    return nonzero / total if total > 0 else 0.0


def compute_aspect_ratio(obj):
    """Compute aspect ratio of bounding box (max/min dimension)."""
    echo_data = obj["echo_data"]
    if not echo_data:
        return 1.0
    n_pulses = len(echo_data)
    if isinstance(echo_data[0], dict):
        n_bins = max(len(p.get("echoes", [])) for p in echo_data)
    elif isinstance(echo_data[0], list):
        n_bins = max(len(row) for row in echo_data)
    else:
        return 1.0
    if n_bins == 0 or n_pulses == 0:
        return 1.0
    return max(n_pulses, n_bins) / max(1, min(n_pulses, n_bins))


def apply_quality_filter(obj, category):
    """Apply quality filters based on size category.

    Returns True if object passes filter (should be kept).
    """
    area = obj.get("area", 0)
    mi = obj.get("mean_intensity", 0)

    # Drop tiny and xlarge entirely
    if area < 10 or area >= 500:
        return False

    fill = compute_fill_ratio(obj)
    aspect = compute_aspect_ratio(obj)

    if category == "small":  # area 10-50: stricter filtering
        return fill >= 0.3 and mi >= 40 and mi <= 180 and aspect <= 8
    elif category == "medium":  # area 50-200: moderate filtering
        return fill >= 0.2 and mi >= 30 and aspect <= 10
    elif category == "large":  # area 200-500: light filtering
        return fill >= 0.15 and mi >= 25 and aspect <= 12
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stats", action="store_true", help="Print statistics only")
    parser.add_argument("--filter", action="store_true", help="Show filter recommendations")
    parser.add_argument("--filtered", action="store_true",
                        help="Generate contact sheets with quality filters applied")
    args = parser.parse_args()

    print("Loading library objects...")
    objects = load_all_objects()
    targets = [o for o in objects if o.get("category") == "target"]
    interference = [o for o in objects if o.get("category") == "interference"]
    print(f"  {len(targets)} targets, {len(interference)} interference")

    if args.stats or args.filter:
        areas = [o["area"] for o in targets]
        intensities = [o["mean_intensity"] for o in targets]
        print(f"\nTarget statistics:")
        print(f"  Area:      min={min(areas)}, median={sorted(areas)[len(areas)//2]}, max={max(areas)}")
        print(f"  Intensity: min={min(intensities):.0f}, median={sorted(intensities)[len(intensities)//2]:.0f}, max={max(intensities):.0f}")

        # Histogram by area
        bins = [(0, 10), (10, 50), (50, 100), (100, 500), (500, 1000), (1000, 5000)]
        print(f"\n  Area distribution:")
        for lo, hi in bins:
            count = sum(1 for a in areas if lo <= a < hi)
            print(f"    [{lo:5d}, {hi:5d}): {count:6d}  {'#' * min(50, count // 50)}")

        # Histogram by intensity
        ibins = [(0, 30), (30, 60), (60, 100), (100, 150), (150, 200), (200, 255)]
        print(f"\n  Intensity distribution:")
        for lo, hi in ibins:
            count = sum(1 for a in intensities if lo <= a < hi)
            print(f"    [{lo:3d}, {hi:3d}): {count:6d}  {'#' * min(50, count // 50)}")

        if args.filter:
            print(f"\n  Recommendation:")
            print(f"    Drop area < 10 (too small, likely noise): {sum(1 for a in areas if a < 10)} objects")
            print(f"    Drop area >= 500 (too large, artifacts): {sum(1 for a in areas if a >= 500)} objects")
            print(f"    Drop intensity < 30 (too faint): {sum(1 for i in intensities if i < 30)} objects")
            print(f"    Keep: 10 <= area < 500 AND quality filters")
            good = [o for o in targets if apply_quality_filter(o,
                    "small" if o["area"] < 50 else "medium" if o["area"] < 200 else "large")]
            print(f"    Remaining: {len(good)} objects ({100*len(good)/len(targets):.0f}%)")
        return

    # Create contact sheets by size category
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    import random
    random.seed(42)

    if args.filtered:
        # Show FILTERED objects with quality metrics
        size_ranges = [
            ("small", "small (area 10-50)", 10, 50),
            ("medium", "medium (area 50-200)", 50, 200),
            ("large", "large (area 200-500)", 200, 500),
        ]

        total_kept = 0
        total_orig = 0
        for cat, label, lo, hi in size_ranges:
            subset = [o for o in targets if lo <= o["area"] < hi]
            total_orig += len(subset)
            filtered = [o for o in subset if apply_quality_filter(o, cat)]
            rejected = [o for o in subset if not apply_quality_filter(o, cat)]
            total_kept += len(filtered)
            print(f"  {label}: {len(subset)} total -> {len(filtered)} kept, {len(rejected)} rejected")

            # Show kept objects
            sample = random.sample(filtered, min(200, len(filtered)))
            sample.sort(key=lambda o: o["mean_intensity"], reverse=True)
            fname = os.path.join(OUTPUT_DIR, f"filtered_kept_{cat}.png")
            create_contact_sheet(sample,
                f"KEPT {label} -- {len(filtered)}/{len(subset)}, showing {len(sample)}", fname)

            # Show rejected objects
            if rejected:
                rsample = random.sample(rejected, min(200, len(rejected)))
                rsample.sort(key=lambda o: o["mean_intensity"], reverse=True)
                fname = os.path.join(OUTPUT_DIR, f"filtered_rejected_{cat}.png")
                create_contact_sheet(rsample,
                    f"REJECTED {label} -- {len(rejected)}/{len(subset)}, showing {len(rsample)}", fname)

        print(f"\n  Total: {total_kept}/{total_orig} kept ({100*total_kept/total_orig:.0f}%)")
        print(f"  + tiny/xlarge dropped: {sum(1 for o in targets if o['area'] < 10 or o['area'] >= 500)} objects")
        print(f"  Final library size: {total_kept} objects")

    else:
        # Original unfiltered contact sheets
        targets.sort(key=lambda o: o["area"])
        size_ranges = [
            ("tiny (area 1-10)", 1, 10),
            ("small (area 10-50)", 10, 50),
            ("medium (area 50-200)", 50, 200),
            ("large (area 200-500)", 200, 500),
            ("xlarge (area 500+)", 500, 99999),
        ]

        for label, lo, hi in size_ranges:
            subset = [o for o in targets if lo <= o["area"] < hi]
            if not subset:
                print(f"  {label}: 0 objects, skipping")
                continue
            sample = random.sample(subset, min(200, len(subset)))
            sample.sort(key=lambda o: o["mean_intensity"], reverse=True)
            fname = os.path.join(OUTPUT_DIR, f"objects_{label.split('(')[0].strip()}.png")
            create_contact_sheet(sample, f"{label} -- {len(subset)} total, showing {len(sample)}", fname)

    print(f"\nContact sheets saved to: {OUTPUT_DIR}/")
    print("Review the images to decide filtering thresholds.")


if __name__ == "__main__":
    main()
