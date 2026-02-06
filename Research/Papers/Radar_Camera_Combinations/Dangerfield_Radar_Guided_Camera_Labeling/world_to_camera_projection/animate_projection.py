"""
Animated Radar PPI + Camera Projection
Generates per-frame LaTeX/TikZ files → PDF → PNG → GIF

Left panel:  Radar PPI display (dark circular scope, range rings,
             bearing lines, sweep beam, bright blips)
Right panel: Projected camera view with sky/water and solid colored
             rounded rectangles

Camera is co-located with the radar at the origin.
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
    "honeycomb": (164, 145,  55),
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
# PPI display parameters
# ---------------------------------------------------------------------------
PPI_RADIUS_CM = 4.0              # TikZ radius of the PPI circle
PPI_CX, PPI_CY = 4.0, 4.0       # TikZ center of the PPI circle
PPI_MAX_RANGE = 1000.0           # max range displayed (m)
SWEEP_RPM = 24                   # radar sweep speed (revolutions per minute)
SWEEP_DEG_PER_FRAME = (SWEEP_RPM * 360.0) / (FPS * 60)  # degrees per frame

def ppi_coord(x_world, y_world):
    """World (x=right, y=forward) → TikZ (cm) on the PPI scope.
    PPI convention: up = forward = 0° bearing, right = +90°.
    """
    rng = np.sqrt(x_world**2 + y_world**2)
    r_cm = PPI_RADIUS_CM * min(rng / PPI_MAX_RANGE, 1.0)
    bearing = np.arctan2(x_world, y_world)  # angle from forward
    tx = PPI_CX + r_cm * np.sin(bearing)
    ty = PPI_CY + r_cm * np.cos(bearing)
    return tx, ty

# Camera view: pixel (u,v) mapped to TikZ cm
CAM_W = 12.0
CAM_H = CAM_W * IMAGE_H / IMAGE_W  # ~6.75 cm
CAM_X_OFF = PPI_CX + PPI_RADIUS_CM + 1.5  # offset right of PPI

def cam_coord(u, v):
    """Pixel (u,v) → TikZ (cm) in camera panel."""
    cx_ = CAM_X_OFF + CAM_W * u / IMAGE_W
    cy_ = CAM_H * (1.0 - v / IMAGE_H)
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

    # PPI scope colors
    lines.append(r"\definecolor{ppigrid}{RGB}{199,199,199}")
    lines.append(r"\definecolor{ppifov}{RGB}{70,106,159}")

    # ===================================================================
    # RADAR PPI DISPLAY
    # ===================================================================
    R_cm = PPI_RADIUS_CM
    ocx, ocy = PPI_CX, PPI_CY

    # Clip everything to the PPI circle
    lines.append(f"\\begin{{scope}}")
    lines.append(f"\\clip ({ocx:.3f},{ocy:.3f}) circle ({R_cm:.3f});")

    # White background
    lines.append(f"\\fill[white] ({ocx-R_cm:.3f},{ocy-R_cm:.3f}) "
                 f"rectangle ({ocx+R_cm:.3f},{ocy+R_cm:.3f});")

    # Range rings (full circles, clipped)
    for rng in [200, 400, 600, 800, 1000]:
        r_cm = R_cm * rng / PPI_MAX_RANGE
        lines.append(f"\\draw[ppigrid, very thin] ({ocx:.3f},{ocy:.3f}) circle ({r_cm:.3f});")

    # Bearing lines every 30 degrees
    for bearing_deg in range(0, 360, 30):
        b_rad = np.deg2rad(bearing_deg)
        ex = ocx + R_cm * np.sin(b_rad)
        ey = ocy + R_cm * np.cos(b_rad)
        lines.append(f"\\draw[ppigrid, very thin] ({ocx:.3f},{ocy:.3f}) -- ({ex:.3f},{ey:.3f});")

    # Camera FOV wedge overlay
    half_fov = HFOV_RAD / 2
    n_arc = 60
    fov_r_cm = R_cm
    arc_angles = np.linspace(-half_fov, half_fov, n_arc)
    wedge_pts = [(ocx, ocy)]
    for a in arc_angles:
        wx = ocx + fov_r_cm * np.sin(a)
        wy = ocy + fov_r_cm * np.cos(a)
        wedge_pts.append((wx, wy))
    wedge_pts.append((ocx, ocy))
    pts_str = " -- ".join(f"({p[0]:.3f},{p[1]:.3f})" for p in wedge_pts)
    lines.append(f"\\fill[ppifov, opacity=0.08] {pts_str} -- cycle;")
    lines.append(f"\\draw[ppifov, opacity=0.35, thin] "
                 f"({ocx:.3f},{ocy:.3f}) -- ({wedge_pts[1][0]:.3f},{wedge_pts[1][1]:.3f});")
    lines.append(f"\\draw[ppifov, opacity=0.35, thin] "
                 f"({ocx:.3f},{ocy:.3f}) -- ({wedge_pts[-2][0]:.3f},{wedge_pts[-2][1]:.3f});")

    # Object blips — solid colored circles
    for obj in OBJECTS:
        x, y = get_position(obj, frame_idx)
        rng = np.sqrt(x**2 + y**2)
        if rng > PPI_MAX_RANGE:
            continue
        bx, by = ppi_coord(x, y)
        col = obj["color"]
        blip_r = max(0.07, R_cm * obj["w"] / PPI_MAX_RANGE * 0.6)
        lines.append(f"\\fill[{col}] ({bx:.3f},{by:.3f}) circle ({blip_r:.3f});")

    lines.append(f"\\end{{scope}}")

    # PPI circle border
    lines.append(f"\\draw[black90, thick] ({ocx:.3f},{ocy:.3f}) circle ({R_cm:.3f});")

    # Range labels outside circle
    for rng in [200, 400, 600, 800]:
        r_cm = R_cm * rng / PPI_MAX_RANGE
        lx = ocx + 0.12
        ly = ocy + r_cm
        lines.append(f"\\node[black50, font=\\fontsize{{4}}{{4}}\\selectfont, "
                     f"right] at ({lx:.3f},{ly:.3f}) {{{rng}m}};")

    # Bearing labels
    for bdeg, blabel in [(0, "0°"), (90, "90°"), (180, "180°"), (270, "270°")]:
        b_rad = np.deg2rad(bdeg)
        lx = ocx + (R_cm + 0.3) * np.sin(b_rad)
        ly = ocy + (R_cm + 0.3) * np.cos(b_rad)
        lines.append(f"\\node[black50, font=\\fontsize{{4}}{{4}}\\selectfont] "
                     f"at ({lx:.3f},{ly:.3f}) {{{blabel}}};")

    # Title
    lines.append(f"\\node[black90, font=\\small\\bfseries, above] at "
                 f"({ocx:.3f},{ocy + R_cm + 0.6:.3f}) {{Radar PPI}};")

    # Center crosshair (radar/camera location)
    lines.append(f"\\fill[black90] ({ocx:.3f},{ocy:.3f}) circle (0.04);")
    lines.append(f"\\draw[black70, very thin] ({ocx-0.12:.3f},{ocy:.3f}) -- ({ocx+0.12:.3f},{ocy:.3f});")
    lines.append(f"\\draw[black70, very thin] ({ocx:.3f},{ocy-0.12:.3f}) -- ({ocx:.3f},{ocy+0.12:.3f});")
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

    # Project objects into camera view — sort back-to-front (furthest first)
    cam_objects = []
    for obj in OBJECTS:
        x, y = get_position(obj, frame_idx)
        if y <= 0:
            continue
        bbox = project_bbox(x, y, obj)
        if bbox is None:
            continue
        u_min, v_min, u_max, v_max = bbox
        if u_max < 0 or u_min > IMAGE_W or v_max < 0 or v_min > IMAGE_H:
            continue
        rng = np.sqrt(x**2 + y**2)
        # Project radar detection point (object center at waterline Z=0)
        radar_pt = project_point(x, y, 0)
        cam_objects.append((rng, obj, bbox, radar_pt))

    # Draw furthest first so closer objects overlap on top
    cam_objects.sort(key=lambda t: t[0], reverse=True)

    # --- Actual object bounding boxes (drawn first = camera layer) ---
    for rng, obj, bbox, radar_pt in cam_objects:
        u_min, v_min, u_max, v_max = bbox
        u_min_c = max(u_min, 0)
        v_min_c = max(v_min, 0)
        u_max_c = min(u_max, IMAGE_W)
        v_max_c = min(v_max, IMAGE_H)

        col = obj["color"]
        cx0, cy0 = cam_coord(u_min_c, v_max_c)
        cx1, cy1 = cam_coord(u_max_c, v_min_c)

        # Solid colored rounded rectangle with white outline
        lines.append(f"\\fill[{col}, rounded corners=1.5pt] "
                     f"({cx0:.3f},{cy0:.3f}) rectangle ({cx1:.3f},{cy1:.3f});")
        lines.append(f"\\draw[white, thick, rounded corners=1.5pt] "
                     f"({cx0:.3f},{cy0:.3f}) rectangle ({cx1:.3f},{cy1:.3f});")

    # --- Radar prediction overlay (drawn ON TOP of camera image) ---
    # Circles on the Z=0 water surface, perspective-projected.
    N_CIRCLE_PTS = 48
    circle_angles = np.linspace(0, 2 * np.pi, N_CIRCLE_PTS, endpoint=False)

    for rng, obj, bbox, radar_pt in cam_objects:
        x, y = get_position(obj, frame_idx)
        water_radius = max(15.0, rng * 0.06)

        proj_pts = []
        for a in circle_angles:
            wx = x + water_radius * np.cos(a)
            wy = y + water_radius * np.sin(a)
            pt = project_point(wx, wy, 0)
            if pt is not None:
                pu, pv = pt
                if 0 <= pu <= IMAGE_W and 0 <= pv <= IMAGE_H:
                    proj_pts.append(cam_coord(pu, pv))

        if len(proj_pts) < 3:
            continue

        pts_str = " -- ".join(f"({p[0]:.3f},{p[1]:.3f})" for p in proj_pts)
        lines.append(f"\\fill[honeycomb, opacity=0.20] {pts_str} -- cycle;")
        lines.append(f"\\draw[honeycomb, thick] {pts_str} -- cycle;")
        if radar_pt is not None:
            ru, rv = radar_pt
            if 0 <= ru <= IMAGE_W and 0 <= rv <= IMAGE_H:
                cdx, cdy = cam_coord(ru, rv)
                lines.append(f"\\fill[honeycomb] ({cdx:.3f},{cdy:.3f}) circle (0.03);")

    # Camera view title
    lines.append(f"\\node[black90, font=\\small\\bfseries, above] at "
                 f"({CAM_X_OFF + CAM_W/2:.3f},{CAM_H + 0.3:.3f}) "
                 f"{{Projected Camera View (HFOV={HFOV_DEG:.0f}°, tilt={CAMERA_TILT:.0f}°)}};")

    # Border
    lines.append(f"\\draw[black90, thick] ({CAM_X_OFF:.3f},0) rectangle ({CAM_X_OFF + CAM_W:.3f},{CAM_H:.3f});")

    # Frame counter
    lines.append(f"\\node[black50, font=\\tiny] at ({CAM_X_OFF + CAM_W - 0.5:.3f},0.3) {{f{frame_idx:03d}}};")

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
