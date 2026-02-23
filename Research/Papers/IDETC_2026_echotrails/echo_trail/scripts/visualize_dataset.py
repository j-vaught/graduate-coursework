#!/usr/bin/env python3
"""Create annotated GIF previews of generated radar datasets.

Reads images and YOLO labels from a scene output directory,
draws bounding boxes on each frame, and compiles into a GIF.

Usage:
    python visualize_dataset.py /path/to/scene_output/
    python visualize_dataset.py /path/to/scene_output/ --max-frames 100
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def parse_yolo_labels(label_path, img_w, img_h):
    """Parse YOLO label file and return list of (x1, y1, x2, y2) boxes."""
    boxes = []
    if not label_path.exists():
        return boxes
    with open(label_path) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 5:
                continue
            _, cx, cy, w, h = float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
            x1 = int((cx - w / 2) * img_w)
            y1 = int((cy - h / 2) * img_h)
            x2 = int((cx + w / 2) * img_w)
            y2 = int((cy + h / 2) * img_h)
            boxes.append((x1, y1, x2, y2))
    return boxes


def annotate_frame(img_path, label_path, max_width=640):
    """Load image, draw boxes, resize, return PIL Image."""
    img = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    boxes = parse_yolo_labels(label_path, img.width, img.height)
    for x1, y1, x2, y2 in boxes:
        draw.rectangle([x1, y1, x2, y2], outline="#00FF00", width=2)

    # Frame number overlay
    frame_num = img_path.stem.split("_")[-1]
    draw.text((5, 5), f"#{frame_num}", fill="white")

    # Object count
    draw.text((5, 20), f"{len(boxes)} obj", fill="#00FF00")

    # Resize for GIF
    if img.width > max_width:
        ratio = max_width / img.width
        new_h = int(img.height * ratio)
        img = img.resize((max_width, new_h), Image.LANCZOS)

    return img


def create_gif(scene_dir, max_frames=None, max_width=640, fps=10):
    """Create annotated GIF from scene output directory."""
    scene_dir = Path(scene_dir)

    # Find images and labels
    images_dir = scene_dir / "images"
    labels_dir = scene_dir / "YOLO_labels"

    if not images_dir.exists():
        print(f"No images/ directory found in {scene_dir}")
        sys.exit(1)

    image_files = sorted(images_dir.glob("*.png"))
    if not image_files:
        print(f"No PNG files found in {images_dir}")
        sys.exit(1)

    if max_frames:
        image_files = image_files[:max_frames]

    print(f"Processing {len(image_files)} frames from {scene_dir.name}...")
    has_labels = labels_dir.exists()
    if not has_labels:
        print("  Warning: no YOLO_labels/ directory found, drawing frames without boxes")

    frames = []
    label_counts = []
    for i, img_path in enumerate(image_files):
        label_path = labels_dir / (img_path.stem + ".txt") if has_labels else Path("/dev/null")
        frame = annotate_frame(img_path, label_path, max_width)
        frames.append(frame)

        n_boxes = len(parse_yolo_labels(label_path, 1, 1)) if has_labels else 0
        label_counts.append(n_boxes)

        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{len(image_files)} frames processed")

    # Stats
    total_labels = sum(label_counts)
    frames_with_labels = sum(1 for c in label_counts if c > 0)
    density = frames_with_labels / len(label_counts) * 100 if label_counts else 0
    avg_per_frame = total_labels / len(label_counts) if label_counts else 0
    print(f"  Labels: {total_labels} total, {avg_per_frame:.1f} avg/frame, {density:.0f}% frame coverage")

    # Save GIF
    gif_path = scene_dir / "preview.gif"
    duration_ms = int(1000 / fps)
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
        optimize=True,
    )
    print(f"  Saved: {gif_path} ({gif_path.stat().st_size / 1024 / 1024:.1f} MB)")
    return gif_path


def main():
    parser = argparse.ArgumentParser(description="Create annotated GIF from radar scene output")
    parser.add_argument("scene_dir", type=str, help="Path to scene output directory")
    parser.add_argument("--max-frames", type=int, default=None, help="Max frames to include")
    parser.add_argument("--max-width", type=int, default=640, help="Max GIF width in pixels")
    parser.add_argument("--fps", type=int, default=10, help="GIF frame rate")
    args = parser.parse_args()

    create_gif(args.scene_dir, args.max_frames, args.max_width, args.fps)


if __name__ == "__main__":
    main()
