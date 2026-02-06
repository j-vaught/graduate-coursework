#!/usr/bin/env python3
"""Generate a radar PPI animation showing sequential camera target acquisition.

The camera arc starts wide, visits each moving object (labeling it with a
bounding box once identified), then labels stationary objects. Objects move
slowly across the PPI throughout.

Produces TikZ frames compiled to PDF/PNG, then stitched into MP4 and GIF.
"""

import math
import os
import subprocess
import shutil

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
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

PPI_RADIUS = 5.0
TRAIL_LENGTH = 5
BBOX_HALF = 0.35

# ---------------------------------------------------------------------------
# Object definitions
# ---------------------------------------------------------------------------

def _linear(x0, y0, x1, y1):
    def traj(t):
        return (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)
    return traj

def _arc_traj(cx, cy, r, a0_deg, a1_deg):
    a0 = math.radians(a0_deg)
    a1 = math.radians(a1_deg)
    def traj(t):
        a = a0 + (a1 - a0) * t
        return (cx + r * math.cos(a), cy + r * math.sin(a))
    return traj

# Stationary objects: key -> (x, y)
STATIONARY = {
    "B1": (2.0, 3.0),
    "V1": (-3.0, -1.5),
}

# Moving objects: key -> trajectory_func(t) -> (x, y), t in [0,1]
MOVING = {
    "S1": _linear(-4.0, 4.0, 3.0, -3.0),
    "S2": _linear(2.0, -4.5, -1.0, 4.5),
    "S3": _arc_traj(0.0, 0.0, 3.5, 210, 30),
}

# ---------------------------------------------------------------------------
# Animation timeline (segments)
# ---------------------------------------------------------------------------
# Segment types:
#   "init"  – scene visible, no bboxes, arc sits at start position
#   "move"  – arc transitions from current angle/width to target
#   "dwell" – arc tracks target; bbox appears after bbox_delay frames
#   "hold"  – everything stays, final view

ARC_INIT_ANGLE = 210.0   # starting direction (SW-ish)
ARC_INIT_WIDTH = 50.0    # starting FOV degrees
MOVING_ARC_WIDTH = 18.0  # wider shot for moving objects
STATIC_ARC_WIDTH = 10.0  # tighter for stationary objects

SEGMENTS = [
    {"type": "init",  "duration": 12},
    # --- Moving objects first ---
    {"type": "move",  "duration": 25, "target": "S1", "width": MOVING_ARC_WIDTH},
    {"type": "dwell", "duration": 14, "target": "S1", "bbox_delay": 8},
    {"type": "move",  "duration": 22, "target": "S2", "width": MOVING_ARC_WIDTH},
    {"type": "dwell", "duration": 14, "target": "S2", "bbox_delay": 8},
    {"type": "move",  "duration": 22, "target": "S3", "width": MOVING_ARC_WIDTH},
    {"type": "dwell", "duration": 14, "target": "S3", "bbox_delay": 8},
    # --- Stationary objects ---
    {"type": "move",  "duration": 20, "target": "B1", "width": STATIC_ARC_WIDTH},
    {"type": "dwell", "duration": 14, "target": "B1", "bbox_delay": 8},
    {"type": "move",  "duration": 20, "target": "V1", "width": STATIC_ARC_WIDTH},
    {"type": "dwell", "duration": 14, "target": "V1", "bbox_delay": 8},
    # --- Final hold ---
    {"type": "hold",  "duration": 15},
]

# Compute total frames and segment start indices
_seg_starts = []
_total = 0
for seg in SEGMENTS:
    _seg_starts.append(_total)
    _total += seg["duration"]
NUM_FRAMES = _total

# Pre-compute the absolute frame at which each object's bbox appears
BBOX_APPEAR_FRAME = {}
for i, seg in enumerate(SEGMENTS):
    if seg["type"] == "dwell":
        BBOX_APPEAR_FRAME[seg["target"]] = _seg_starts[i] + seg["bbox_delay"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ease_in_out(t):
    """Smooth ease-in-out (cubic)."""
    t = max(0.0, min(1.0, t))
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - (-2 * t + 2) ** 3 / 2


def _angle_diff(a, b):
    """Shortest signed angle from a to b (degrees)."""
    d = (b - a) % 360
    if d > 180:
        d -= 360
    return d


def _obj_pos(key, t_global):
    """Get object position at global time t (0..1)."""
    if key in STATIONARY:
        return STATIONARY[key]
    return MOVING[key](t_global)


def _angle_to(key, t_global):
    """Angle from radar center to object (degrees)."""
    x, y = _obj_pos(key, t_global)
    return math.degrees(math.atan2(y, x))


# ---------------------------------------------------------------------------
# Arc state computation
# ---------------------------------------------------------------------------

def _get_arc_state(frame_idx):
    """Return (center_angle, width) of the camera arc for a given frame."""
    t_global = frame_idx / (NUM_FRAMES - 1)

    # Find which segment this frame belongs to
    seg_idx = 0
    for i, start in enumerate(_seg_starts):
        if i + 1 < len(_seg_starts) and frame_idx >= _seg_starts[i + 1]:
            continue
        seg_idx = i
        break

    seg = SEGMENTS[seg_idx]
    seg_start = _seg_starts[seg_idx]
    local_frame = frame_idx - seg_start
    local_t = local_frame / max(1, seg["duration"] - 1)

    if seg["type"] == "init":
        return ARC_INIT_ANGLE, ARC_INIT_WIDTH

    elif seg["type"] == "move":
        target = seg["target"]
        target_width = seg["width"]

        # Figure out where the arc was at the end of the previous segment
        prev_angle, prev_width = _get_arc_state(seg_start - 1) if seg_start > 0 else (ARC_INIT_ANGLE, ARC_INIT_WIDTH)

        # Target angle is where the object is NOW (tracks moving objects)
        target_angle = _angle_to(target, t_global)

        e = _ease_in_out(local_t)
        angle = prev_angle + _angle_diff(prev_angle, target_angle) * e
        width = prev_width + (target_width - prev_width) * e
        return angle, width

    elif seg["type"] == "dwell":
        target = seg["target"]
        # Track the target continuously
        angle = _angle_to(target, t_global)
        # Width stays at whatever the preceding move segment targeted
        prev_seg = SEGMENTS[seg_idx - 1]
        width = prev_seg.get("width", MOVING_ARC_WIDTH)
        return angle, width

    elif seg["type"] == "hold":
        # Stay where we were at end of previous segment
        return _get_arc_state(seg_start - 1) if seg_start > 0 else (ARC_INIT_ANGLE, ARC_INIT_WIDTH)

    return ARC_INIT_ANGLE, ARC_INIT_WIDTH


# ---------------------------------------------------------------------------
# TikZ generation
# ---------------------------------------------------------------------------

def _rgb_tex(name, rgb):
    r, g, b = rgb
    return f"\\definecolor{{{name}}}{{RGB}}{{{r},{g},{b}}}"


def make_tex(frame_idx):
    """Return complete LaTeX source for one frame."""
    t_global = frame_idx / (NUM_FRAMES - 1)

    colordefs = "\n".join(_rgb_tex(n, c) for n, c in COLORS.items())

    body = []

    # Background + border
    body.append(r"\fill[White] (-5.8,-5.8) rectangle (5.8,5.8);")
    body.append(r"\draw[Black, thick] (-5.8,-5.8) rectangle (5.8,5.8);")

    # Range rings
    for r in range(1, 6):
        body.append(f"\\draw[30Black, thin] (0,0) circle ({r}cm);")
        body.append(f"\\node[30Black, font=\\tiny] at ({r - 0.3}, 0.25) {{{r} km}};")

    # Cardinal labels
    off = PPI_RADIUS + 0.45
    for lbl, x, y in [("N", 0, off), ("S", 0, -off), ("E", off, 0), ("W", -off, 0)]:
        body.append(f"\\node[Black, font=\\small\\bfseries] at ({x},{y}) {{{lbl}}};")

    # Radar centre
    body.append(r"\fill[Black] (0,0) circle (0.06cm);")

    # --- Camera arc ---
    arc_center, arc_width = _get_arc_state(frame_idx)
    a1 = arc_center - arc_width / 2
    a2 = arc_center + arc_width / 2
    body.append(
        f"\\fill[Rose, opacity=0.18] (0,0) -- ({a1:.2f}:{PPI_RADIUS}) "
        f"arc ({a1:.2f}:{a2:.2f}:{PPI_RADIUS}) -- cycle;"
    )
    body.append(
        f"\\draw[Rose, thick] (0,0) -- ({a1:.2f}:{PPI_RADIUS}) "
        f"arc ({a1:.2f}:{a2:.2f}:{PPI_RADIUS}) -- cycle;"
    )

    # --- Stationary objects ---
    for key, (sx, sy) in STATIONARY.items():
        body.append(f"\\fill[Congaree] ({sx},{sy}) circle (0.10cm);")

        if key in BBOX_APPEAR_FRAME and frame_idx >= BBOX_APPEAR_FRAME[key]:
            x0, y0 = sx - BBOX_HALF, sy - BBOX_HALF
            x1, y1 = sx + BBOX_HALF, sy + BBOX_HALF
            body.append(f"\\draw[Atlantic, thick] ({x0},{y0}) rectangle ({x1},{y1});")
            body.append(
                f"\\node[Atlantic, font=\\tiny, anchor=south west] "
                f"at ({x1 + 0.05},{y1 + 0.05}) {{{key}}};"
            )

    # --- Moving objects ---
    for key, traj in MOVING.items():
        cx, cy = traj(t_global)

        # Trail dots
        for k in range(TRAIL_LENGTH, 0, -1):
            t_trail = t_global - k * (1.0 / (NUM_FRAMES - 1))
            if t_trail < 0:
                continue
            tx, ty = traj(t_trail)
            opacity = 1.0 - k / (TRAIL_LENGTH + 1)
            body.append(
                f"\\fill[Congaree, opacity={opacity:.2f}] "
                f"({tx:.4f},{ty:.4f}) circle (0.06cm);"
            )

        # Detection dot
        body.append(f"\\fill[Congaree] ({cx:.4f},{cy:.4f}) circle (0.10cm);")

        # Bounding box only after camera has identified this object
        if key in BBOX_APPEAR_FRAME and frame_idx >= BBOX_APPEAR_FRAME[key]:
            x0, y0 = cx - BBOX_HALF, cy - BBOX_HALF
            x1, y1 = cx + BBOX_HALF, cy + BBOX_HALF
            body.append(
                f"\\draw[Garnet, thick] ({x0:.4f},{y0:.4f}) "
                f"rectangle ({x1:.4f},{y1:.4f});"
            )
            body.append(
                f"\\node[Garnet, font=\\tiny, anchor=south west] "
                f"at ({x1 + 0.05:.4f},{y1 + 0.05:.4f}) {{{key}}};"
            )

    # Frame counter
    body.append(
        f"\\node[Black, font=\\tiny, anchor=north east] "
        f"at (5.65,5.65) {{Frame {frame_idx + 1}/{NUM_FRAMES}}};"
    )

    tikz_body = "\n    ".join(body)
    return rf"""\documentclass[tikz,border=2pt]{{standalone}}
\usepackage{{tikz}}
{colordefs}
\begin{{document}}
\begin{{tikzpicture}}
    {tikz_body}
\end{{tikzpicture}}
\end{{document}}
"""


# ---------------------------------------------------------------------------
# Pipeline (unchanged)
# ---------------------------------------------------------------------------

def compile_frame(frame_idx):
    tex_name = f"frame_{frame_idx:03d}.tex"
    pdf_name = f"frame_{frame_idx:03d}.pdf"
    png_name = f"frame_{frame_idx:03d}.png"

    tex_path = os.path.join(TEMP_DIR, tex_name)
    pdf_path = os.path.join(TEMP_DIR, pdf_name)
    png_path = os.path.join(TEMP_DIR, png_name)

    with open(tex_path, "w") as f:
        f.write(make_tex(frame_idx))

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

    ppm_prefix = os.path.join(TEMP_DIR, f"frame_{frame_idx:03d}")
    subprocess.run(
        ["pdftoppm", "-r", str(DPI), "-png", pdf_path, ppm_prefix],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )

    ppm_output = ppm_prefix + "-1.png"
    if os.path.exists(ppm_output):
        os.rename(ppm_output, png_path)

    if not os.path.exists(png_path):
        print(f"  [ERROR] PNG not generated for frame {frame_idx}")
        return None
    return png_path


def stitch_video():
    png_pattern = os.path.join(TEMP_DIR, "frame_%03d.png")

    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS), "-i", png_pattern,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", OUTPUT_MP4,
    ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"  MP4 written: {OUTPUT_MP4}")

    palette = os.path.join(TEMP_DIR, "palette.png")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS), "-i", png_pattern,
        "-vf", "palettegen", palette,
    ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS), "-i", png_pattern,
        "-i", palette, "-lavfi", "paletteuse", OUTPUT_GIF,
    ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"  GIF written: {OUTPUT_GIF}")


def cleanup():
    if os.path.isdir(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
        print("  Cleaned up temporary files.")


def main():
    os.makedirs(TEMP_DIR, exist_ok=True)
    print(f"Generating {NUM_FRAMES} PPI frames ({NUM_FRAMES / FPS:.1f}s at {FPS}fps)...")
    for i in range(NUM_FRAMES):
        print(f"  Frame {i + 1}/{NUM_FRAMES}", end="")
        png = compile_frame(i)
        if png:
            print(" -> OK")
        else:
            print(" -> FAILED")
            return
    print("Stitching video...")
    stitch_video()
    print("Cleaning up...")
    cleanup()
    print("Done!")


if __name__ == "__main__":
    main()
