#!/usr/bin/env python3
"""Standalone echo trail renderer for ablation study.

Reads raw grayscale PNGs from Stage 4 output and applies configurable
trail rendering with multiple decay functions, intensity encoding modes,
and color mapping strategies. Uses per-pixel max compositing (Eq. 5).

Usage:
    python apply_trails.py \
        --images-dir /path/to/images \
        --labels-dir /path/to/YOLO_labels \
        --output-dir /path/to/output \
        --trail-length 6 \
        --decay linear \
        --intensity-mode binary \
        --color-mode mono
"""

import argparse
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
from PIL import Image


# ---------------------------------------------------------------------------
# Decay functions  (paper Eq. 5)
# ---------------------------------------------------------------------------

def decay_exponential(k: int, N: int, tau: Optional[float] = None) -> float:
    """Exponential decay: f(k) = exp(-k / tau).

    Args:
        k: Frame age (0 = most recent history frame, N-1 = oldest).
        N: Trail length (total history frames).
        tau: Time constant. Defaults to N/3 for ~95% decay over N frames.
    """
    if tau is None:
        tau = max(N / 3.0, 1.0)
    return np.exp(-k / tau)


def decay_concave(k: int, N: int, p: float = 3.0) -> float:
    """Concave power decay: f(k) = max(0, 1 - (k/N)^p)."""
    return max(0.0, 1.0 - (k / N) ** p)


def decay_linear(k: int, N: int) -> float:
    """Linear decay: f(k) = 1 - k/N."""
    return max(0.0, 1.0 - k / N)


def decay_step(k: int, N: int) -> float:
    """Step (uniform) decay: f(k) = 1 if k < N else 0."""
    return 1.0 if k < N else 0.0


DECAY_FUNCTIONS = {
    "exponential": decay_exponential,
    "concave": decay_concave,
    "linear": decay_linear,
    "step": decay_step,
}


# ---------------------------------------------------------------------------
# Color mapping strategies
# ---------------------------------------------------------------------------

def colormap_mono(intensity: float, age_frac: float) -> Tuple[int, int, int]:
    """Monochrome green-on-black. Brightness encodes weight."""
    v = int(np.clip(intensity * 255, 0, 255))
    return (0, v, 0)


def colormap_twotone(intensity: float, age_frac: float,
                     is_current: bool = False) -> Tuple[int, int, int]:
    """Two-tone: current frame = green, trail = red (dimming with age)."""
    v = intensity
    if is_current:
        return (0, int(np.clip(v * 255, 0, 255)), 0)
    else:
        return (int(np.clip(v * 255, 0, 255)),
                0,
                0)


def colormap_gradient(intensity: float, age_frac: float) -> Tuple[int, int, int]:
    """Gradient: age maps green -> yellow -> red."""
    v = np.clip(intensity, 0, 1)
    if age_frac < 0.5:
        r = int(age_frac * 2 * 255 * v)
        g = int(255 * v)
    else:
        r = int(255 * v)
        g = int((1 - (age_frac - 0.5) * 2) * 255 * v)
    b = 0
    return (np.clip(r, 0, 255), np.clip(g, 0, 255), b)


def colormap_intensity(intensity: float, age_frac: float,
                       original_value: float = 0.0) -> Tuple[int, int, int]:
    """Intensity-mapped: original return strength -> color via jet-like ramp."""
    v = np.clip(original_value, 0, 1)
    weight = np.clip(intensity, 0, 1)
    if v < 0.25:
        r, g, b = 0, v * 4, 1.0
    elif v < 0.5:
        r, g, b = 0, 1.0, 1.0 - (v - 0.25) * 4
    elif v < 0.75:
        r, g, b = (v - 0.5) * 4, 1.0, 0
    else:
        r, g, b = 1.0, 1.0 - (v - 0.75) * 4, 0
    return (int(np.clip(r * weight * 255, 0, 255)),
            int(np.clip(g * weight * 255, 0, 255)),
            int(np.clip(b * weight * 255, 0, 255)))


COLOR_MODES = {
    "mono": "monochrome",
    "twotone": "two-tone",
    "gradient": "gradient",
    "intensity": "intensity-mapped",
}


# ---------------------------------------------------------------------------
# Core trail compositing (per-pixel max, paper Eq. 5)
# ---------------------------------------------------------------------------

def process_frame(
    frame_idx: int,
    image_files: List[Path],
    trail_length: int,
    decay_name: str,
    intensity_mode: str,
    color_mode: str,
    output_dir: Path,
) -> Optional[Path]:
    """Render one frame with echo trail overlay.

    Compositing uses per-pixel MAX across all weighted history frames,
    matching the paper's Eq. 5 formulation.
    """
    current_path = image_files[frame_idx]
    try:
        current_img = np.array(Image.open(current_path).convert("L"), dtype=np.float32)
        h, w = current_img.shape

        # Gather history frames
        history_start = max(0, frame_idx - trail_length)
        history_indices = list(range(history_start, frame_idx))

        decay_fn = DECAY_FUNCTIONS[decay_name]
        N = trail_length

        # Accumulate per-pixel max across 3 RGB channels
        canvas_r = np.zeros((h, w), dtype=np.float32)
        canvas_g = np.zeros((h, w), dtype=np.float32)
        canvas_b = np.zeros((h, w), dtype=np.float32)

        for hist_frame_idx in history_indices:
            age = frame_idx - hist_frame_idx  # 1..N
            k = age  # k=1 is most recent, k=N is oldest
            weight = decay_fn(k, N)
            if weight <= 0:
                continue

            age_frac = k / N  # 0..1, 0=newest, 1=oldest

            try:
                hist_gray = np.array(
                    Image.open(image_files[hist_frame_idx]).convert("L"),
                    dtype=np.float32,
                )
            except Exception:
                continue

            # Intensity encoding
            if intensity_mode == "binary":
                mask = (hist_gray > 0).astype(np.float32)
                pixel_weight = mask * weight
            else:  # proportional
                pixel_weight = (hist_gray / 255.0) * weight

            # Apply color mapping per-pixel
            if color_mode == "mono":
                fr = np.zeros_like(pixel_weight)
                fg = pixel_weight
                fb = np.zeros_like(pixel_weight)
            elif color_mode == "twotone":
                # Trail = red (dimming with age via pixel_weight)
                fr = pixel_weight
                fg = np.zeros_like(pixel_weight)
                fb = np.zeros_like(pixel_weight)
            elif color_mode == "gradient":
                # Green -> yellow -> red based on age
                if age_frac < 0.5:
                    fr = pixel_weight * (age_frac * 2)
                    fg = pixel_weight
                else:
                    fr = pixel_weight
                    fg = pixel_weight * (1 - (age_frac - 0.5) * 2)
                fb = np.zeros_like(pixel_weight)
            elif color_mode == "intensity":
                # Jet-like mapping based on original pixel value
                norm_val = hist_gray / 255.0
                fr = np.zeros_like(pixel_weight)
                fg = np.zeros_like(pixel_weight)
                fb = np.zeros_like(pixel_weight)
                # Piecewise jet ramp
                m1 = norm_val < 0.25
                m2 = (norm_val >= 0.25) & (norm_val < 0.5)
                m3 = (norm_val >= 0.5) & (norm_val < 0.75)
                m4 = norm_val >= 0.75
                fr[m3] = (norm_val[m3] - 0.5) * 4
                fr[m4] = 1.0
                fg[m1] = norm_val[m1] * 4
                fg[m2] = 1.0
                fg[m3] = 1.0
                fg[m4] = 1.0 - (norm_val[m4] - 0.75) * 4
                fb[m1] = 1.0
                fb[m2] = 1.0 - (norm_val[m2] - 0.25) * 4
                fr *= pixel_weight
                fg *= pixel_weight
                fb *= pixel_weight
            else:
                fr = np.zeros_like(pixel_weight)
                fg = pixel_weight
                fb = np.zeros_like(pixel_weight)

            # Per-pixel MAX compositing
            canvas_r = np.maximum(canvas_r, fr)
            canvas_g = np.maximum(canvas_g, fg)
            canvas_b = np.maximum(canvas_b, fb)

        # Composite current frame on top (always full intensity)
        current_norm = current_img / 255.0

        if color_mode == "mono":
            cur_r = np.zeros_like(current_norm)
            cur_g = current_norm
            cur_b = np.zeros_like(current_norm)
        elif color_mode == "twotone":
            # Current = green
            cur_r = np.zeros_like(current_norm)
            cur_g = current_norm
            cur_b = np.zeros_like(current_norm)
        elif color_mode == "gradient":
            # Current = bright green (age=0)
            cur_r = np.zeros_like(current_norm)
            cur_g = current_norm
            cur_b = np.zeros_like(current_norm)
        elif color_mode == "intensity":
            # Current frame uses same jet mapping
            norm_val = current_norm
            cur_r = np.zeros_like(current_norm)
            cur_g = np.zeros_like(current_norm)
            cur_b = np.zeros_like(current_norm)
            m1 = norm_val < 0.25
            m2 = (norm_val >= 0.25) & (norm_val < 0.5)
            m3 = (norm_val >= 0.5) & (norm_val < 0.75)
            m4 = norm_val >= 0.75
            cur_r[m3] = (norm_val[m3] - 0.5) * 4
            cur_r[m4] = 1.0
            cur_g[m1] = norm_val[m1] * 4
            cur_g[m2] = 1.0
            cur_g[m3] = 1.0
            cur_g[m4] = 1.0 - (norm_val[m4] - 0.75) * 4
            cur_b[m1] = 1.0
            cur_b[m2] = 1.0 - (norm_val[m2] - 0.25) * 4
            cur_r *= current_norm
            cur_g *= current_norm
            cur_b *= current_norm
        else:
            cur_r = np.zeros_like(current_norm)
            cur_g = current_norm
            cur_b = np.zeros_like(current_norm)

        # Current frame overrides trail via MAX
        canvas_r = np.maximum(canvas_r, cur_r)
        canvas_g = np.maximum(canvas_g, cur_g)
        canvas_b = np.maximum(canvas_b, cur_b)

        # Where current frame has signal, suppress trail color so green wins
        current_mask = current_norm > 0
        canvas_r[current_mask] = cur_r[current_mask]
        canvas_b[current_mask] = cur_b[current_mask]

        # Convert to uint8 RGB
        out = np.stack([
            np.clip(canvas_r * 255, 0, 255).astype(np.uint8),
            np.clip(canvas_g * 255, 0, 255).astype(np.uint8),
            np.clip(canvas_b * 255, 0, 255).astype(np.uint8),
        ], axis=-1)

        output_path = output_dir / current_path.name
        Image.fromarray(out, mode="RGB").save(output_path)
        return output_path

    except Exception as e:
        print(f"Error processing frame {frame_idx} ({current_path.name}): {e}")
        return None


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def apply_trails(
    images_dir: str,
    output_dir: str,
    labels_dir: Optional[str] = None,
    trail_length: int = 6,
    decay: str = "linear",
    intensity_mode: str = "binary",
    color_mode: str = "mono",
    threads: int = 8,
) -> Tuple[str, Optional[str]]:
    """Apply echo trails to a sequence of grayscale radar frames.

    Args:
        images_dir: Directory with sequential grayscale PNGs (Stage 4 output).
        output_dir: Base output directory for trail images.
        labels_dir: Directory with YOLO labels to copy alongside.
        trail_length: Number of history frames (N).
        decay: Decay function name (exponential, concave, linear, step).
        intensity_mode: Encoding mode (binary, proportional).
        color_mode: Color mapping (mono, twotone, gradient, intensity).
        threads: Number of worker threads.

    Returns:
        (trail_images_dir, trail_labels_dir) paths.
    """
    images_path = Path(images_dir)
    image_files = sorted(
        p for p in images_path.glob("*.png") if not p.name.startswith("._")
    )
    if not image_files:
        print(f"No PNG files found in {images_dir}")
        return None, None

    trail_images_dir = Path(output_dir) / "trail_images"
    trail_images_dir.mkdir(parents=True, exist_ok=True)

    config_str = (f"N={trail_length}, decay={decay}, "
                  f"intensity={intensity_mode}, color={color_mode}")
    print(f"Applying echo trails to {len(image_files)} frames ({config_str})")

    completed = 0
    total = len(image_files)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(
                process_frame,
                i, image_files, trail_length,
                decay, intensity_mode, color_mode,
                trail_images_dir,
            ): i
            for i in range(total)
        }

        for future in as_completed(futures):
            future.result()
            completed += 1
            if completed % 50 == 0 or completed == total:
                print(f"  Progress: {completed}/{total}")

    # Copy labels alongside trail images
    trail_labels_dir = None
    if labels_dir:
        labels_path = Path(labels_dir)
        label_files = sorted(labels_path.glob("*.txt"))
        if label_files:
            trail_labels_path = Path(output_dir) / "trail_labels"
            trail_labels_path.mkdir(parents=True, exist_ok=True)
            trail_labels_dir = str(trail_labels_path)
            for lf in label_files:
                shutil.copy2(str(lf), str(trail_labels_path / lf.name))
            print(f"  Copied {len(label_files)} label files")

    print(f"Trail images saved to: {trail_images_dir}")
    return str(trail_images_dir), trail_labels_dir


def main():
    parser = argparse.ArgumentParser(
        description="Standalone echo trail renderer for ablation study"
    )
    parser.add_argument("--images-dir", required=True,
                        help="Directory with grayscale PNGs (Stage 4 output)")
    parser.add_argument("--labels-dir", default=None,
                        help="Directory with YOLO labels to copy")
    parser.add_argument("--output-dir", required=True,
                        help="Output directory")
    parser.add_argument("--trail-length", type=int, default=6,
                        help="Number of history frames N (default: 6)")
    parser.add_argument("--decay", choices=list(DECAY_FUNCTIONS.keys()),
                        default="linear",
                        help="Decay function (default: linear)")
    parser.add_argument("--intensity-mode", choices=["binary", "proportional"],
                        default="binary",
                        help="Intensity encoding (default: binary)")
    parser.add_argument("--color-mode", choices=list(COLOR_MODES.keys()),
                        default="mono",
                        help="Color mapping (default: mono)")
    parser.add_argument("--threads", type=int, default=8,
                        help="Worker threads (default: 8)")

    args = parser.parse_args()

    apply_trails(
        images_dir=args.images_dir,
        output_dir=args.output_dir,
        labels_dir=args.labels_dir,
        trail_length=args.trail_length,
        decay=args.decay,
        intensity_mode=args.intensity_mode,
        color_mode=args.color_mode,
        threads=args.threads,
    )


if __name__ == "__main__":
    main()
