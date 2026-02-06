#!/usr/bin/env python3
"""Generate a 50-frame radar PPI animation with stationary and moving objects.

Produces TikZ frames compiled to PDF/PNG, then stitched into MP4 and GIF.
"""

import math
import os
import subprocess
import shutil
import glob

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
NUM_FRAMES = 50
DPI = 300
FPS = 10
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(SCRIPT_DIR, "_ppi_tmp")
OUTPUT_MP4 = os.path.join(SCRIPT_DIR, "radar_ppi_animation.mp4")
OUTPUT_GIF = os.path.join(SCRIPT_DIR, "radar_ppi_animation.gif")

# Brand colours (RGB 0-255)
COLORS = {
    "Garnet":    (115, 0, 10),
    "Black":     (0, 0, 0),
    "White":     (255, 255, 255),
    "30Black":   (199, 199, 199),
    "Atlantic":  (70, 106, 159),
    "Congaree":  (31, 65, 77),
    "Rose":      (204, 46, 64),
}

# ---------------------------------------------------------------------------
# Beam arc (camera FOV wedge)
# ---------------------------------------------------------------------------
# Target: B1 at (2.0, 3.0) -> angle ≈ 56.3°
BEAM_TARGET = STATIONARY[0] if 'STATIONARY' in dir() else ("B1", 2.0, 3.0)
BEAM_TARGET_ANGLE = math.degrees(math.atan2(3.0, 2.0))  # ~56.3°
BEAM_START_ANGLE = 210.0   # start pointing roughly SW
BEAM_START_WIDTH = 50.0    # degrees
BEAM_END_WIDTH = 5.0       # degrees

# PPI radius in TikZ cm (maps to 5 km)
PPI_RADIUS = 5.0

# ---------------------------------------------------------------------------
# Object definitions
# ---------------------------------------------------------------------------

# Stationary objects: (label, x, y)
STATIONARY = [
    ("B1", 2.0, 3.0),
    ("V1", -3.0, -1.5),
]

# Moving objects: (label, trajectory_func)
# trajectory_func(t) -> (x, y) where t in [0, 1]

def _linear(x0, y0, x1, y1):
    """Return a linear trajectory function."""
    def traj(t):
        return (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)
    return traj

def _arc(cx, cy, r, a0_deg, a1_deg):
    """Return an arc trajectory function."""
    a0 = math.radians(a0_deg)
    a1 = math.radians(a1_deg)
    def traj(t):
        a = a0 + (a1 - a0) * t
        return (cx + r * math.cos(a), cy + r * math.sin(a))
    return traj

MOVING = [
    ("S1", _linear(-4.0, 4.0, 3.0, -3.0)),
    ("S2", _linear(2.0, -4.5, -1.0, 4.5)),
    ("S3", _arc(0.0, 0.0, 3.5, 210, 30)),
]

TRAIL_LENGTH = 5  # number of trailing dots
BBOX_HALF = 0.35  # half-size of bounding box


def _ease_in_out(t):
    """Smooth ease-in-out (cubic)."""
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - (-2 * t + 2) ** 3 / 2

# ---------------------------------------------------------------------------
# TikZ template
# ---------------------------------------------------------------------------

def rgb_tex(name, rgb):
    r, g, b = rgb
    return f"\\definecolor{{{name}}}{{RGB}}{{{r},{g},{b}}}"

def make_tex(frame_idx):
    """Return complete LaTeX source for one frame."""
    t = frame_idx / (NUM_FRAMES - 1)  # 0..1

    # Colour definitions
    colordefs = "\n".join(rgb_tex(n, c) for n, c in COLORS.items())

    # --- Build TikZ body ---
    body_lines = []

    # White background with black border (no rounded edges)
    body_lines.append(
        r"\fill[White] (-5.8,-5.8) rectangle (5.8,5.8);"
    )
    body_lines.append(
        r"\draw[Black, thick] (-5.8,-5.8) rectangle (5.8,5.8);"
    )

    # Range rings (1-5 km)
    for r in range(1, 6):
        body_lines.append(
            f"\\draw[30Black, thin] (0,0) circle ({r}cm);"
        )
        # Range label
        body_lines.append(
            f"\\node[30Black, font=\\tiny] at ({r - 0.3}, 0.25) {{{r} km}};"
        )

    # Cardinal direction labels
    off = PPI_RADIUS + 0.45
    for label, x, y in [("N", 0, off), ("S", 0, -off),
                         ("E", off, 0), ("W", -off, 0)]:
        body_lines.append(
            f"\\node[Black, font=\\small\\bfseries] at ({x},{y}) {{{label}}};"
        )

    # Radar centre dot
    body_lines.append(r"\fill[Black] (0,0) circle (0.06cm);")

    # --- Beam arc (camera FOV wedge) ---
    e = _ease_in_out(t)
    beam_center = BEAM_START_ANGLE + (BEAM_TARGET_ANGLE - BEAM_START_ANGLE) * e
    beam_width = BEAM_START_WIDTH + (BEAM_END_WIDTH - BEAM_START_WIDTH) * e
    beam_a1 = beam_center - beam_width / 2
    beam_a2 = beam_center + beam_width / 2
    body_lines.append(
        f"\\fill[Rose, opacity=0.18] (0,0) -- ({beam_a1:.2f}:{PPI_RADIUS}) "
        f"arc ({beam_a1:.2f}:{beam_a2:.2f}:{PPI_RADIUS}) -- cycle;"
    )
    body_lines.append(
        f"\\draw[Rose, thick] (0,0) -- ({beam_a1:.2f}:{PPI_RADIUS}) "
        f"arc ({beam_a1:.2f}:{beam_a2:.2f}:{PPI_RADIUS}) -- cycle;"
    )

    # --- Stationary objects ---
    for label, sx, sy in STATIONARY:
        # Detection dot
        body_lines.append(
            f"\\fill[Congaree] ({sx},{sy}) circle (0.10cm);"
        )
        # Bounding box — Atlantic
        x0, y0 = sx - BBOX_HALF, sy - BBOX_HALF
        x1, y1 = sx + BBOX_HALF, sy + BBOX_HALF
        body_lines.append(
            f"\\draw[Atlantic, thick] ({x0},{y0}) rectangle ({x1},{y1});"
        )
        # Label
        body_lines.append(
            f"\\node[Atlantic, font=\\tiny, anchor=south west] at ({x1 + 0.05},{y1 + 0.05}) {{{label}}};"
        )

    # --- Moving objects ---
    for label, traj in MOVING:
        cx, cy = traj(t)

        # Trail dots (fading)
        for k in range(TRAIL_LENGTH, 0, -1):
            t_trail = t - k * (1.0 / (NUM_FRAMES - 1))
            if t_trail < 0:
                continue
            tx, ty = traj(t_trail)
            opacity = 1.0 - k / (TRAIL_LENGTH + 1)
            body_lines.append(
                f"\\fill[Congaree, opacity={opacity:.2f}] ({tx:.4f},{ty:.4f}) circle (0.06cm);"
            )

        # Current detection dot
        body_lines.append(
            f"\\fill[Congaree] ({cx:.4f},{cy:.4f}) circle (0.10cm);"
        )

        # Bounding box — Garnet
        x0, y0 = cx - BBOX_HALF, cy - BBOX_HALF
        x1, y1 = cx + BBOX_HALF, cy + BBOX_HALF
        body_lines.append(
            f"\\draw[Garnet, thick] ({x0:.4f},{y0:.4f}) rectangle ({x1:.4f},{y1:.4f});"
        )

        # Label
        body_lines.append(
            f"\\node[Garnet, font=\\tiny, anchor=south west] at ({x1 + 0.05:.4f},{y1 + 0.05:.4f}) {{{label}}};"
        )

    # Frame counter
    body_lines.append(
        f"\\node[Black, font=\\tiny, anchor=north east] at (5.65,5.65) {{Frame {frame_idx + 1}/{NUM_FRAMES}}};"
    )

    tikz_body = "\n    ".join(body_lines)

    tex_src = rf"""\documentclass[tikz,border=2pt]{{standalone}}
\usepackage{{tikz}}
{colordefs}
\begin{{document}}
\begin{{tikzpicture}}
    {tikz_body}
\end{{tikzpicture}}
\end{{document}}
"""
    return tex_src


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def compile_frame(frame_idx):
    """Write, compile, and convert a single frame. Returns png path."""
    tex_name = f"frame_{frame_idx:03d}.tex"
    pdf_name = f"frame_{frame_idx:03d}.pdf"
    png_name = f"frame_{frame_idx:03d}.png"

    tex_path = os.path.join(TEMP_DIR, tex_name)
    pdf_path = os.path.join(TEMP_DIR, pdf_name)
    png_path = os.path.join(TEMP_DIR, png_name)

    # Write tex
    with open(tex_path, "w") as f:
        f.write(make_tex(frame_idx))

    # Compile (two passes as per user preference)
    for _ in range(2):
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_name],
            cwd=TEMP_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            print(f"  [ERROR] pdflatex failed on frame {frame_idx}")
            print(result.stdout.decode(errors="replace")[-1500:])
            return None

    # Convert PDF -> PNG
    ppm_prefix = os.path.join(TEMP_DIR, f"frame_{frame_idx:03d}")
    subprocess.run(
        ["pdftoppm", "-r", str(DPI), "-png", pdf_path, ppm_prefix],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # pdftoppm appends -1 to single-page PDFs
    ppm_output = ppm_prefix + "-1.png"
    if os.path.exists(ppm_output):
        os.rename(ppm_output, png_path)

    if not os.path.exists(png_path):
        print(f"  [ERROR] PNG not generated for frame {frame_idx}")
        return None

    return png_path


def stitch_video():
    """Combine PNGs into MP4 and GIF."""
    png_pattern = os.path.join(TEMP_DIR, "frame_%03d.png")

    # MP4
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-framerate", str(FPS),
            "-i", png_pattern,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
            OUTPUT_MP4,
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(f"  MP4 written: {OUTPUT_MP4}")

    # GIF via palette for quality
    palette = os.path.join(TEMP_DIR, "palette.png")
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-framerate", str(FPS),
            "-i", png_pattern,
            "-vf", "palettegen",
            palette,
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-framerate", str(FPS),
            "-i", png_pattern,
            "-i", palette,
            "-lavfi", "paletteuse",
            OUTPUT_GIF,
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(f"  GIF written: {OUTPUT_GIF}")


def cleanup():
    """Remove temporary directory."""
    if os.path.isdir(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
        print("  Cleaned up temporary files.")


def main():
    os.makedirs(TEMP_DIR, exist_ok=True)

    print(f"Generating {NUM_FRAMES} PPI frames...")
    for i in range(NUM_FRAMES):
        print(f"  Frame {i + 1}/{NUM_FRAMES}", end="")
        png = compile_frame(i)
        if png:
            print(f" -> OK")
        else:
            print(f" -> FAILED")
            return

    print("Stitching video...")
    stitch_video()

    print("Cleaning up...")
    cleanup()

    print("Done!")


if __name__ == "__main__":
    main()
