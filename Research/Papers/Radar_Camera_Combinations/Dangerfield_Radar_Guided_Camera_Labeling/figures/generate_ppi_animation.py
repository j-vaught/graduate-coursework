#!/usr/bin/env python3
"""Generate a radar PPI animation with urgency + slew-efficiency camera scheduling.

Score_i = w_U * U_i + w_S * S_i

  Urgency:        U_i = 1 - t_rem / t_max   (how soon target exits radar range)
  Slew efficiency: S_i = 1 - |dtheta| / 180  (how close target is to current heading)

  Weights: w_U = 0.7, w_S = 0.3

The camera repeatedly picks the highest-scoring unlabeled target, slews to
it, dwells until a bounding box is generated, then re-scores.

Objects are designed to showcase the algorithm:
  A — Fast outbound (NE)      → high urgency, labeled early
  B — Moderate outbound (SSW) → moderate urgency + near camera start
  C — Slow inbound (NW)       → low urgency, deferred
  D — Stationary, close       → zero urgency, labeled on slew convenience
  E — Stationary, far (SW)    → zero urgency, near camera start direction
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


STATIONARY = {
    "D": (0.9, 0.5),       # Close, bearing ~29deg, range ~1.0 km
    "E": (-2.5, -4.2),     # Far SW, bearing ~239deg, range ~4.9 km
}

MOVING = {
    "A": _linear(2.5, 2.5, 6.5, 6.0),      # Fast outbound NE, exits range
    "B": _linear(-1.5, -3.5, -3.5, -5.5),   # Moderate outbound SSW, exits range
    "C": _linear(-3.8, 2.5, -1.0, 1.0),     # Slow inbound from NW
}

ALL_KEYS = list(MOVING.keys()) + list(STATIONARY.keys())

# ---------------------------------------------------------------------------
# Scoring parameters
# ---------------------------------------------------------------------------
ARC_INIT_ANGLE = 210.0
ARC_INIT_WIDTH = 50.0
MOVING_ARC_WIDTH = 18.0
STATIC_ARC_WIDTH = 10.0
DWELL_DURATION = 14
BBOX_DELAY = 8
INIT_DURATION = 14
HOLD_DURATION = 18

W_U = 0.7   # urgency weight
W_S = 0.3   # slew-efficiency weight
T_MAX = 1.0 # normalising horizon (full animation in t-units)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ease_in_out(t):
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
    if key in STATIONARY:
        return STATIONARY[key]
    return MOVING[key](t_global)


def _obj_range(key, t_global):
    x, y = _obj_pos(key, t_global)
    return math.hypot(x, y)


def _angle_to(key, t_global):
    x, y = _obj_pos(key, t_global)
    return math.degrees(math.atan2(y, x))


def _radial_velocity(key, t_global, dt=0.001):
    """Radial velocity (positive = outbound, negative = inbound)."""
    if key in STATIONARY:
        return 0.0
    r1 = _obj_range(key, t_global)
    r2 = _obj_range(key, min(1.0, t_global + dt))
    return (r2 - r1) / dt


def _compute_score(key, t_global, cam_angle):
    """Return (score, U, S) for a target at the given time and camera heading."""
    # --- Urgency ---
    v_r = _radial_velocity(key, t_global)
    if v_r > 0.05:  # outbound
        r = _obj_range(key, t_global)
        remaining = PPI_RADIUS - r
        if remaining <= 0:
            U = 1.0
        else:
            t_rem = remaining / v_r
            U = max(0.0, min(1.0, 1.0 - t_rem / T_MAX))
    else:
        U = 0.0  # inbound or stationary

    # --- Slew efficiency ---
    target_angle = _angle_to(key, t_global)
    delta_theta = abs(_angle_diff(cam_angle, target_angle))
    S = 1.0 - delta_theta / 180.0

    score = W_U * U + W_S * S
    return score, U, S


# ---------------------------------------------------------------------------
# Dynamic timeline builder — urgency + slew scoring
# ---------------------------------------------------------------------------

def _build_segments():
    """Build segments by repeatedly picking the highest-scoring unlabeled target."""
    est_total = INIT_DURATION + len(ALL_KEYS) * 38 + HOLD_DURATION

    segments = [{"type": "init", "duration": INIT_DURATION}]
    labeled = set()
    cursor = INIT_DURATION
    cam_angle = ARC_INIT_ANGLE

    print("=" * 78)
    print("CAMERA SCHEDULING  —  Score = 0.7·U + 0.3·S")
    print("=" * 78)

    step = 0
    while len(labeled) < len(ALL_KEYS):
        step += 1
        t_now = min(cursor / est_total, 0.99)

        # Score all unlabeled targets
        scores = {}
        for key in ALL_KEYS:
            if key in labeled:
                continue
            scores[key] = _compute_score(key, t_now, cam_angle)

        # Print score table
        ranked = sorted(scores.items(), key=lambda kv: kv[1][0], reverse=True)
        print(f"\nStep {step}  (frame ~{cursor}, t={t_now:.2f}, "
              f"camera at {cam_angle:.0f}deg)")
        print(f"{'Object':>8} {'U':>6} {'S':>6} {'Score':>7}  Note")
        print(f"{'------':>8} {'-----':>6} {'-----':>6} {'------':>7}  ----")
        for key, (sc, U, S) in ranked:
            v_r = _radial_velocity(key, t_now)
            if key in STATIONARY:
                note = "stationary"
            elif v_r > 0.05:
                note = f"outbound (v_r={v_r:.1f})"
            elif v_r < -0.05:
                note = f"inbound  (v_r={v_r:.1f})"
            else:
                note = "crossing"
            marker = " <-- PICK" if key == ranked[0][0] else ""
            print(f"{key:>8} {U:>6.2f} {S:>6.2f} {sc:>7.3f}  {note}{marker}")

        best_key = ranked[0][0]

        # Move duration proportional to angular distance
        target_angle = _angle_to(best_key, t_now)
        ang = abs(_angle_diff(cam_angle, target_angle))
        move_dur = max(15, min(30, int(ang / 7)))

        is_moving = best_key in MOVING
        width = MOVING_ARC_WIDTH if is_moving else STATIC_ARC_WIDTH

        segments.append({
            "type": "move", "duration": move_dur,
            "target": best_key, "width": width,
        })
        segments.append({
            "type": "dwell", "duration": DWELL_DURATION,
            "target": best_key, "bbox_delay": BBOX_DELAY,
        })

        labeled.add(best_key)
        cursor += move_dur + DWELL_DURATION
        cam_angle = target_angle

    segments.append({"type": "hold", "duration": HOLD_DURATION})

    print("\n" + "=" * 78)
    order = [s["target"] for s in segments if s["type"] == "dwell"]
    print(f"Final acquisition order: {' -> '.join(order)}")
    print("=" * 78)

    return segments


SEGMENTS = _build_segments()

# Compute segment start frames
_seg_starts = []
_total = 0
for seg in SEGMENTS:
    _seg_starts.append(_total)
    _total += seg["duration"]
NUM_FRAMES = _total

# Pre-compute absolute frame each bbox appears
BBOX_APPEAR_FRAME = {}
for i, seg in enumerate(SEGMENTS):
    if seg["type"] == "dwell":
        BBOX_APPEAR_FRAME[seg["target"]] = _seg_starts[i] + seg["bbox_delay"]

print(f"\nTotal frames: {NUM_FRAMES} ({NUM_FRAMES / FPS:.1f}s)")
for key in [s["target"] for s in SEGMENTS if s["type"] == "dwell"]:
    print(f"  {key}: bbox at frame {BBOX_APPEAR_FRAME[key]}")


# ---------------------------------------------------------------------------
# Arc state computation
# ---------------------------------------------------------------------------

def _get_arc_state(frame_idx):
    t_global = frame_idx / max(1, NUM_FRAMES - 1)

    seg_idx = 0
    for i in range(len(_seg_starts)):
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
        prev_angle, prev_width = (
            _get_arc_state(seg_start - 1) if seg_start > 0
            else (ARC_INIT_ANGLE, ARC_INIT_WIDTH)
        )
        target_angle = _angle_to(seg["target"], t_global)
        e = _ease_in_out(local_t)
        angle = prev_angle + _angle_diff(prev_angle, target_angle) * e
        width = prev_width + (seg["width"] - prev_width) * e
        return angle, width

    elif seg["type"] == "dwell":
        angle = _angle_to(seg["target"], t_global)
        prev_seg = SEGMENTS[seg_idx - 1]
        width = prev_seg.get("width", MOVING_ARC_WIDTH)
        return angle, width

    elif seg["type"] == "hold":
        return (
            _get_arc_state(seg_start - 1) if seg_start > 0
            else (ARC_INIT_ANGLE, ARC_INIT_WIDTH)
        )

    return ARC_INIT_ANGLE, ARC_INIT_WIDTH


# ---------------------------------------------------------------------------
# TikZ generation
# ---------------------------------------------------------------------------

def _rgb_tex(name, rgb):
    r, g, b = rgb
    return f"\\definecolor{{{name}}}{{RGB}}{{{r},{g},{b}}}"


def make_tex(frame_idx):
    t_global = frame_idx / max(1, NUM_FRAMES - 1)
    colordefs = "\n".join(_rgb_tex(n, c) for n, c in COLORS.items())

    body = []

    body.append(r"\fill[White] (-5.8,-5.8) rectangle (5.8,5.8);")
    body.append(r"\draw[Black, thick] (-5.8,-5.8) rectangle (5.8,5.8);")

    for r in range(1, 6):
        body.append(f"\\draw[30Black, thin] (0,0) circle ({r}cm);")
        body.append(f"\\node[30Black, font=\\tiny] at ({r - 0.3}, 0.25) {{{r} km}};")

    off = PPI_RADIUS + 0.45
    for lbl, x, y in [("N", 0, off), ("S", 0, -off), ("E", off, 0), ("W", -off, 0)]:
        body.append(f"\\node[Black, font=\\small\\bfseries] at ({x},{y}) {{{lbl}}};")

    body.append(r"\fill[Black] (0,0) circle (0.06cm);")

    # Camera arc
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

    # Stationary objects
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

    # Moving objects
    for key, traj in MOVING.items():
        cx, cy = traj(t_global)

        # Skip if outside radar range
        if math.hypot(cx, cy) > PPI_RADIUS + 0.5:
            continue

        for k in range(TRAIL_LENGTH, 0, -1):
            t_trail = t_global - k * (1.0 / max(1, NUM_FRAMES - 1))
            if t_trail < 0:
                continue
            tx, ty = traj(t_trail)
            if math.hypot(tx, ty) > PPI_RADIUS + 0.5:
                continue
            opacity = 1.0 - k / (TRAIL_LENGTH + 1)
            body.append(
                f"\\fill[Congaree, opacity={opacity:.2f}] "
                f"({tx:.4f},{ty:.4f}) circle (0.06cm);"
            )

        body.append(f"\\fill[Congaree] ({cx:.4f},{cy:.4f}) circle (0.10cm);")

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
# Pipeline
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
            cwd=TEMP_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
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
    print(f"\nGenerating {NUM_FRAMES} PPI frames ({NUM_FRAMES / FPS:.1f}s at {FPS}fps)...")
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
