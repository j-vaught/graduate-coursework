"""
Animated World-to-Camera Projection
Generates per-frame LaTeX/TikZ files → PDF → PNG → GIF

Left panel:  top-down world view with moving objects
Right panel: projected camera view with sky/water and solid colored rounded rectangles
"""

import os
import subprocess
import shutil
import numpy as np
from PIL import Image
from pathlib import Path

# ---------------------------------------------------------------------------
# Directories
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).parent.resolve()
FRAME_DIR = SCRIPT_DIR / "_anim_frames"
FRAME_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Brand palette
# ---------------------------------------------------------------------------
COLORS = {
    "garnet":    (115,   0,  10),
    "atlantic":  ( 70, 106, 159),
    "horseshoe": (101, 120,  11),
    "rose":      (204,  46,  64),
    "congaree":  ( 31,  65,  77),
    "black90":   ( 54,  54,  54),
    "black70":   ( 92,  92,  92),
    "black50":   (162, 162, 162),
    "black30":   (199, 199, 199),
    "black10":   (235, 235, 235),
    "white":     (255, 255, 255),
}

def rgb01(name):
    """Return 'r,g,b' string in 0-1 range for TikZ."""
    r, g, b = COLORS[name]
    return f"{r/255:.3f},{g/255:.3f},{b/255:.3f}"

# ---------------------------------------------------------------------------
# Camera parameters
# ---------------------------------------------------------------------------
HFOV_DEG      = 100.0
IMAGE_W       = 1920
IMAGE_H       = 1080
CAMERA_HEIGHT = 15.0
CAMERA_TILT   = -2.0

HFOV_RAD = np.deg2rad(HFOV_DEG)
fx = IMAGE_W / (2.0 * np.tan(HFOV_RAD / 2.0))
fy = fx
cx = IMAGE_W / 2.0
cy = IMAGE_H / 2.0

K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])

tilt_rad = np.deg2rad(CAMERA_TILT)
R_base = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], dtype=float)
R_tilt = np.array([
    [1, 0, 0],
    [0, np.cos(tilt_rad), -np.sin(tilt_rad)],
    [0, np.sin(tilt_rad),  np.cos(tilt_rad)],
], dtype=float)
R = R_tilt @ R_base
t_world = np.array([0, 0, CAMERA_HEIGHT])
t = -R @ t_world
Rt = np.hstack([R, t.reshape(3, 1)])
P = K @ Rt

# Horizon
d_cam = R @ np.array([0, 1, 0])
HORIZON_V = cy + fy * d_cam[1] / d_cam[2]

# ---------------------------------------------------------------------------
# Animation parameters
# ---------------------------------------------------------------------------
N_FRAMES = 80
FPS = 20

# ---------------------------------------------------------------------------
# Object definitions with trajectories
# (x0, y0) = start position, (vx, vy) = velocity in m/frame
# ---------------------------------------------------------------------------
OBJECTS = [
    {"label": "Fishing Vessel", "color": "garnet",
     "x0": -120, "y0": 180, "vx": 1.8, "vy": 0.5,
     "w": 12, "l": 30, "h": 8},
    {"label": "Cargo Ship", "color": "atlantic",
     "x0": 80, "y0": 250, "vx": -0.6, "vy": 1.5,
     "w": 25, "l": 80, "h": 15},
    {"label": "Sailboat", "color": "horseshoe",
     "x0": -180, "y0": 450, "vx": 1.2, "vy": -0.3,
     "w": 10, "l": 35, "h": 18},
    {"label": "Buoy", "color": "rose",
     "x0": 100, "y0": 150, "vx": 0.0, "vy": 0.0,
     "w": 4, "l": 4, "h": 3},
    {"label": "Tanker", "color": "congaree",
     "x0": 60, "y0": 750, "vx": -1.0, "vy": 0.4,
     "w": 40, "l": 180, "h": 20},
]


def get_position(obj, frame):
    x = obj["x0"] + obj["vx"] * frame
    y = obj["y0"] + obj["vy"] * frame
    return x, y


def project_point(X, Y, Z):
    p_h = np.array([X, Y, Z, 1.0])
    p_img = P @ p_h
    if p_img[2] <= 0:
        return None
    return p_img[0] / p_img[2], p_img[1] / p_img[2]


def project_bbox(x, y, obj):
    hw, hl, h = obj["w"] / 2, obj["l"] / 2, obj["h"]
    corners = [
        (x - hw, y - hl, 0), (x + hw, y - hl, 0),
        (x - hw, y + hl, 0), (x + hw, y + hl, 0),
        (x - hw, y - hl, h), (x + hw, y - hl, h),
        (x - hw, y + hl, h), (x + hw, y + hl, h),
    ]
    pixels = []
    for c in corners:
        pt = project_point(*c)
        if pt is not None:
            pixels.append(pt)
    if len(pixels) < 2:
        return None
    us = [p[0] for p in pixels]
    vs = [p[1] for p in pixels]
    return min(us), min(vs), max(us), max(vs)


# ---------------------------------------------------------------------------
# TikZ coordinate helpers
# ---------------------------------------------------------------------------
# Top-down view:  world X,Y mapped to TikZ cm
# View window: X in [-300, 300], Y in [-50, 950]  → 8cm wide, 8cm tall
TD_W, TD_H = 8.0, 8.0
TD_XMIN, TD_XMAX = -300, 300
TD_YMIN, TD_YMAX = -50, 950

def td_coord(x, y):
    """World (x,y) → TikZ (cm) in top-down panel."""
    tx = TD_W * (x - TD_XMIN) / (TD_XMAX - TD_XMIN)
    ty = TD_H * (y - TD_YMIN) / (TD_YMAX - TD_YMIN)
    return tx, ty

# Camera view: pixel (u,v) mapped to TikZ cm
# 12cm wide, proportional height
CAM_W = 12.0
CAM_H = CAM_W * IMAGE_H / IMAGE_W  # ~6.75 cm
CAM_X_OFF = TD_W + 1.5  # horizontal offset from top-down

def cam_coord(u, v):
    """Pixel (u,v) → TikZ (cm) in camera panel."""
    cx_ = CAM_X_OFF + CAM_W * u / IMAGE_W
    cy_ = CAM_H * (1.0 - v / IMAGE_H)  # flip v (image v=0 is top)
    return cx_, cy_


# ---------------------------------------------------------------------------
# Generate one LaTeX frame
# ---------------------------------------------------------------------------
def generate_frame_tex(frame_idx):
    lines = []
    lines.append(r"\documentclass[border=2pt]{standalone}")
    lines.append(r"\usepackage{tikz}")
    lines.append(r"\usetikzlibrary{calc}")
    lines.append(r"\begin{document}")
    lines.append(r"\begin{tikzpicture}")

    # --- Define colors ---
    for name, (r, g, b) in COLORS.items():
        lines.append(f"\\definecolor{{{name}}}{{RGB}}{{{r},{g},{b}}}")

    # Sky / water colors
    lines.append(r"\definecolor{skytop}{RGB}{115,158,209}")
    lines.append(r"\definecolor{skybot}{RGB}{199,222,245}")
    lines.append(r"\definecolor{watertop}{RGB}{82,128,140}")
    lines.append(r"\definecolor{waterbot}{RGB}{20,56,71}")

    # ===================================================================
    # TOP-DOWN VIEW
    # ===================================================================
    # Background
    lines.append(f"\\fill[black10] (0,0) rectangle ({TD_W},{TD_H});")

    # Grid
    for gx in range(-200, 300, 100):
        tx, _ = td_coord(gx, TD_YMIN)
        _, ty0 = td_coord(0, TD_YMIN)
        _, ty1 = td_coord(0, TD_YMAX)
        lines.append(f"\\draw[black30, very thin] ({tx:.3f},{ty0:.3f}) -- ({tx:.3f},{ty1:.3f});")
    for gy in range(0, 1000, 200):
        tx0, ty = td_coord(TD_XMIN, gy)
        tx1, _  = td_coord(TD_XMAX, gy)
        lines.append(f"\\draw[black30, very thin] ({tx0:.3f},{ty:.3f}) -- ({tx1:.3f},{ty:.3f});")

    # FOV wedge
    half_fov = HFOV_RAD / 2
    cam_x, cam_y = td_coord(0, 0)
    fov_range = 900
    n_arc = 60
    arc_angles = np.linspace(-half_fov, half_fov, n_arc)

    # Fill wedge
    wedge_pts = [(cam_x, cam_y)]
    for a in arc_angles:
        wx = fov_range * np.sin(a)
        wy = fov_range * np.cos(a)
        px, py = td_coord(wx, wy)
        wedge_pts.append((px, py))
    wedge_pts.append((cam_x, cam_y))
    pts_str = " -- ".join(f"({p[0]:.3f},{p[1]:.3f})" for p in wedge_pts)
    lines.append(f"\\fill[atlantic, opacity=0.08] {pts_str} -- cycle;")
    lines.append(f"\\draw[atlantic, dashed, thin] {pts_str};")

    # Range rings
    for rng in [200, 400, 600, 800]:
        arc_pts = []
        for a in np.linspace(-np.pi/2, np.pi/2, 80):
            rx = rng * np.cos(a)
            ry = rng * np.sin(a)
            px, py = td_coord(rx, ry)
            arc_pts.append((px, py))
        arc_str = " -- ".join(f"({p[0]:.3f},{p[1]:.3f})" for p in arc_pts)
        lines.append(f"\\draw[black30, dotted, very thin] {arc_str};")
        lx, ly = td_coord(10, rng)
        lines.append(f"\\node[black50, font=\\tiny] at ({lx:.3f},{ly:.3f}) {{{rng}m}};")

    # Camera marker
    lines.append(f"\\node[black90, font=\\tiny\\bfseries, below right] at ({cam_x:.3f},{cam_y:.3f}) {{Camera}};")
    lines.append(f"\\fill[black] ({cam_x:.3f},{cam_y:.3f}) -- "
                 f"({cam_x-0.15:.3f},{cam_y-0.25:.3f}) -- ({cam_x+0.15:.3f},{cam_y-0.25:.3f}) -- cycle;")

    # Objects in top-down
    for obj in OBJECTS:
        x, y = get_position(obj, frame_idx)
        col = obj["color"]
        hw = obj["w"] / 2
        hl = obj["l"] / 2
        x0t, y0t = td_coord(x - hw, y - hl)
        x1t, y1t = td_coord(x + hw, y + hl)
        w_cm = x1t - x0t
        h_cm = y1t - y0t
        lines.append(f"\\fill[{col}, opacity=0.7] ({x0t:.3f},{y0t:.3f}) rectangle ({x1t:.3f},{y1t:.3f});")
        lines.append(f"\\draw[{col}, thick] ({x0t:.3f},{y0t:.3f}) rectangle ({x1t:.3f},{y1t:.3f});")
        # Label
        lx, ly = td_coord(x + hw + 5, y)
        lines.append(f"\\node[{col}, font=\\tiny\\bfseries, right] at ({lx:.3f},{ly:.3f}) {{{obj['label']}}};")

    # Top-down title
    tx, ty = td_coord(0, TD_YMAX)
    lines.append(f"\\node[black90, font=\\small\\bfseries, above] at ({TD_W/2:.3f},{TD_H + 0.3:.3f}) {{Top-Down World View}};")

    # Axis labels
    lines.append(f"\\node[black70, font=\\tiny, below] at ({TD_W/2:.3f},-0.3) {{X (m, cross-range)}};")
    lines.append(f"\\node[black70, font=\\tiny, rotate=90, left] at (-0.3,{TD_H/2:.3f}) {{Y (m, range)}};")

    # Border
    lines.append(f"\\draw[black90, thick] (0,0) rectangle ({TD_W},{TD_H});")

    # ===================================================================
    # CAMERA VIEW
    # ===================================================================
    # Horizon in TikZ coords
    _, h_y = cam_coord(0, HORIZON_V)

    # Sky gradient
    sky_top_y = CAM_H
    lines.append(f"\\shade[top color=skytop, bottom color=skybot] "
                 f"({CAM_X_OFF:.3f},{h_y:.3f}) rectangle ({CAM_X_OFF + CAM_W:.3f},{sky_top_y:.3f});")

    # Water gradient
    lines.append(f"\\shade[top color=watertop, bottom color=waterbot] "
                 f"({CAM_X_OFF:.3f},0) rectangle ({CAM_X_OFF + CAM_W:.3f},{h_y:.3f});")

    # Horizon line
    lines.append(f"\\draw[white, opacity=0.6, thin] ({CAM_X_OFF:.3f},{h_y:.3f}) -- ({CAM_X_OFF + CAM_W:.3f},{h_y:.3f});")
    lines.append(f"\\node[white, opacity=0.7, font=\\tiny, above left] at ({CAM_X_OFF + CAM_W - 0.1:.3f},{h_y:.3f}) {{horizon}};")

    # Project objects into camera view
    for obj in OBJECTS:
        x, y = get_position(obj, frame_idx)
        if y <= 0:
            continue
        bbox = project_bbox(x, y, obj)
        if bbox is None:
            continue
        u_min, v_min, u_max, v_max = bbox
        # Check at least partially in frame
        if u_max < 0 or u_min > IMAGE_W or v_max < 0 or v_min > IMAGE_H:
            continue

        # Clamp to image bounds
        u_min_c = max(u_min, 0)
        v_min_c = max(v_min, 0)
        u_max_c = min(u_max, IMAGE_W)
        v_max_c = min(v_max, IMAGE_H)

        col = obj["color"]
        cx0, cy0 = cam_coord(u_min_c, v_max_c)  # bottom-left in TikZ
        cx1, cy1 = cam_coord(u_max_c, v_min_c)  # top-right in TikZ
        w_cm = cx1 - cx0
        h_cm = cy1 - cy0

        # Solid colored rounded rectangle, no text
        lines.append(f"\\fill[{col}, opacity=0.85, rounded corners=1.5pt] "
                     f"({cx0:.3f},{cy0:.3f}) rectangle ({cx1:.3f},{cy1:.3f});")
        lines.append(f"\\draw[{col}, thick, rounded corners=1.5pt] "
                     f"({cx0:.3f},{cy0:.3f}) rectangle ({cx1:.3f},{cy1:.3f});")

    # Camera view title
    lines.append(f"\\node[black90, font=\\small\\bfseries, above] at "
                 f"({CAM_X_OFF + CAM_W/2:.3f},{CAM_H + 0.3:.3f}) "
                 f"{{Projected Camera View (HFOV={HFOV_DEG:.0f}°, tilt={CAMERA_TILT:.0f}°)}};")

    # Border
    lines.append(f"\\draw[black90, thick] ({CAM_X_OFF:.3f},0) rectangle ({CAM_X_OFF + CAM_W:.3f},{CAM_H:.3f});")

    # Frame counter
    lines.append(f"\\node[black50, font=\\tiny] at ({CAM_X_OFF + CAM_W - 0.5:.3f},0.3) {{f{frame_idx:03d}}};")

    # Legend (bottom, between panels)
    leg_x = CAM_X_OFF + 0.3
    leg_y = -0.6
    for i, obj in enumerate(OBJECTS):
        col = obj["color"]
        lx = leg_x + i * 2.5
        lines.append(f"\\fill[{col}, rounded corners=1pt] ({lx:.3f},{leg_y:.3f}) rectangle ({lx+0.3:.3f},{leg_y+0.2:.3f});")
        lines.append(f"\\node[black90, font=\\tiny, right] at ({lx+0.35:.3f},{leg_y+0.1:.3f}) {{{obj['label']}}};")

    lines.append(r"\end{tikzpicture}")
    lines.append(r"\end{document}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Build all frames
# ---------------------------------------------------------------------------
print(f"Generating {N_FRAMES} frames...")

for i in range(N_FRAMES):
    tex_content = generate_frame_tex(i)
    tex_path = FRAME_DIR / f"frame_{i:03d}.tex"
    tex_path.write_text(tex_content)

    # Compile LaTeX → PDF
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
         f"-output-directory={FRAME_DIR}", str(tex_path)],
        capture_output=True, timeout=30,
    )
    if result.returncode != 0:
        print(f"  Frame {i:03d}: pdflatex FAILED")
        print(result.stdout.decode()[-500:])
        continue

    # PDF → PNG via pdftoppm
    pdf_path = FRAME_DIR / f"frame_{i:03d}.pdf"
    png_prefix = FRAME_DIR / f"frame_{i:03d}"
    subprocess.run(
        ["pdftoppm", "-png", "-r", "200", str(pdf_path), str(png_prefix)],
        capture_output=True, timeout=15,
    )

    # Clean up LaTeX artifacts
    for ext in [".aux", ".log", ".tex", ".pdf"]:
        p = FRAME_DIR / f"frame_{i:03d}{ext}"
        if p.exists():
            p.unlink()

    if (i + 1) % 10 == 0 or i == 0:
        print(f"  Frame {i+1:3d}/{N_FRAMES} done")

# ---------------------------------------------------------------------------
# Combine PNGs into GIF
# ---------------------------------------------------------------------------
print("Assembling GIF...")

png_files = sorted(FRAME_DIR.glob("frame_*.png"))
if not png_files:
    print("ERROR: No PNG frames found!")
    exit(1)

frames = [Image.open(f) for f in png_files]
output_path = SCRIPT_DIR / "world_camera_animation.gif"
frames[0].save(
    output_path,
    save_all=True,
    append_images=frames[1:],
    duration=int(1000 / FPS),
    loop=0,
    optimize=True,
)

print(f"Saved → {output_path}")
print(f"  {len(frames)} frames at {FPS} fps = {len(frames)/FPS:.1f}s")

# Clean up frame directory
shutil.rmtree(FRAME_DIR)
print("Cleaned up frame directory.")
