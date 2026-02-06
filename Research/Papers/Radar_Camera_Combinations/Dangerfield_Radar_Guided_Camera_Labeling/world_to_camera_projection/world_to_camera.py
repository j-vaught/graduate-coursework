"""
World-to-Camera Projection Demo (v2)
Projects objects from a top-down world view into an ideal pinhole
camera image with realistic sky/water rendering.

Improvements over v1:
  - Full [R|t] extrinsic matrix with configurable camera tilt
  - 8-corner 3D bounding boxes (objects have length along range)
  - Rendered sky gradient + water gradient separated by projected horizon
  - Objects drawn as filled silhouettes sitting on the water surface
  - Waterline contact points projected accurately
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap

# ---------------------------------------------------------------------------
# Brand palette
# ---------------------------------------------------------------------------
GARNET   = "#73000A"
BLACK    = "#000000"
WHITE    = "#FFFFFF"
BLACK90  = "#363636"
BLACK70  = "#5C5C5C"
BLACK50  = "#A2A2A2"
BLACK30  = "#C7C7C7"
BLACK10  = "#ECECEC"
ROSE     = "#CC2E40"
ATLANTIC = "#466A9F"
CONGAREE = "#1F414D"
HORSESHOE = "#65780B"
HONEYCOMB = "#A49137"
GRASS    = "#CED318"

OBJ_COLORS = [GARNET, ATLANTIC, HORSESHOE, ROSE, CONGAREE]

# ---------------------------------------------------------------------------
# Camera parameters
# ---------------------------------------------------------------------------
HFOV_DEG      = 100.0         # horizontal FOV (degrees)
IMAGE_W       = 1920           # image width (px)
IMAGE_H       = 1080           # image height (px)
CAMERA_HEIGHT = 15.0           # camera height above waterline (m)
CAMERA_TILT   = -2.0           # downward tilt in degrees (negative = look down)

HFOV_RAD = np.deg2rad(HFOV_DEG)
VFOV_RAD = 2 * np.arctan(IMAGE_H / IMAGE_W * np.tan(HFOV_RAD / 2))

# Focal length in pixels
fx = IMAGE_W / (2.0 * np.tan(HFOV_RAD / 2.0))
fy = fx
cx = IMAGE_W / 2.0
cy = IMAGE_H / 2.0

# Intrinsic matrix K (3x3)
K = np.array([
    [fx,  0, cx],
    [ 0, fy, cy],
    [ 0,  0,  1],
])

# ---------------------------------------------------------------------------
# Extrinsic matrix  [R | t]
# ---------------------------------------------------------------------------
# World frame:  X = right,  Y = forward (range),  Z = up
# Camera frame: x = right,  y = down,             z = forward (optical axis)
#
# Step 1: Base rotation — world to camera (looking along +Y, level)
#   R_base rotates  Y_world → z_cam,  Z_world → -y_cam,  X_world → x_cam
#
# Step 2: Apply tilt around the camera x-axis (pitch down)
#   R_tilt rotates in the y_cam-z_cam plane

tilt_rad = np.deg2rad(CAMERA_TILT)

R_base = np.array([
    [1,  0,  0],
    [0,  0, -1],
    [0,  1,  0],
], dtype=float)

R_tilt = np.array([
    [1,  0,                0              ],
    [0,  np.cos(tilt_rad), -np.sin(tilt_rad)],
    [0,  np.sin(tilt_rad),  np.cos(tilt_rad)],
], dtype=float)

R = R_tilt @ R_base

# Camera position in world coords: (0, 0, CAMERA_HEIGHT)
t_world = np.array([0, 0, CAMERA_HEIGHT])
t = -R @ t_world   # translation in camera frame

# Full 3x4 extrinsic
Rt = np.hstack([R, t.reshape(3, 1)])

# Full 3x4 projection matrix
P = K @ Rt

print("=" * 60)
print("CAMERA INTRINSICS & EXTRINSICS")
print("=" * 60)
print(f"  Horizontal FOV : {HFOV_DEG:.1f}°")
print(f"  Vertical FOV   : {np.degrees(VFOV_RAD):.1f}°")
print(f"  Image size      : {IMAGE_W} x {IMAGE_H} px")
print(f"  Focal length    : fx = fy = {fx:.1f} px")
print(f"  Principal point : ({cx:.1f}, {cy:.1f})")
print(f"  Camera height   : {CAMERA_HEIGHT:.1f} m")
print(f"  Camera tilt     : {CAMERA_TILT:.1f}°")
print()
print("  K =")
for row in K:
    print(f"      [{row[0]:9.2f}  {row[1]:9.2f}  {row[2]:9.2f}]")
print()
print("  R =")
for row in R:
    print(f"      [{row[0]:9.4f}  {row[1]:9.4f}  {row[2]:9.4f}]")
print(f"  t = [{t[0]:.4f}, {t[1]:.4f}, {t[2]:.4f}]")
print()
print("  P (3x4 projection) =")
for row in P:
    print(f"      [{row[0]:10.2f}  {row[1]:10.2f}  {row[2]:10.2f}  {row[3]:10.2f}]")
print()

# ---------------------------------------------------------------------------
# Projection functions
# ---------------------------------------------------------------------------
def project_point_world(X, Y, Z):
    """Project world point (X,Y,Z) through full P matrix → (u, v) or None."""
    p_h = np.array([X, Y, Z, 1.0])
    p_img = P @ p_h
    if p_img[2] <= 0:
        return None
    u = p_img[0] / p_img[2]
    v = p_img[1] / p_img[2]
    return u, v


def compute_horizon_v():
    """Compute the pixel row of the horizon (sea level at infinite range).
    At infinity, a point on the water (Z=0) at range Y→∞:
       lim_{Y→∞} project(0, Y, 0)  →  v_horizon
    The direction vector for (0, Y, 0) as Y→∞ is (0,1,0).
    In camera frame: d_cam = R @ [0,1,0]^T
    Horizon v = cy + fy * d_cam[1] / d_cam[2]
    """
    d_cam = R @ np.array([0, 1, 0])
    if abs(d_cam[2]) < 1e-9:
        return cy
    v_h = cy + fy * d_cam[1] / d_cam[2]
    return v_h


# ---------------------------------------------------------------------------
# World objects — now with length (depth along Y) for full 3D boxes
# ---------------------------------------------------------------------------
objects = [
    {"x":  -80, "y":  200, "w": 12, "l": 30,  "h": 8,
     "label": "Fishing Vessel", "color": OBJ_COLORS[0]},
    {"x":   30, "y":  350, "w": 25, "l": 80,  "h": 15,
     "label": "Cargo Ship",     "color": OBJ_COLORS[1]},
    {"x": -150, "y":  500, "w": 10, "l": 35,  "h": 18,
     "label": "Sailboat",       "color": OBJ_COLORS[2]},
    {"x":  100, "y":  150, "w": 4,  "l": 4,   "h": 3,
     "label": "Buoy",           "color": OBJ_COLORS[3]},
    {"x":  -20, "y":  800, "w": 40, "l": 180, "h": 20,
     "label": "Tanker",         "color": OBJ_COLORS[4]},
]


def project_object_3d(obj):
    """
    Project full 8-corner 3D bounding box.
    Box: center at (x, y), width w (cross-range), length l (along range),
         base at Z=0, top at Z=h.
    Returns (u_min, v_min, u_max, v_max) or None.
    """
    x, y = obj["x"], obj["y"]
    hw, hl, h = obj["w"] / 2, obj["l"] / 2, obj["h"]
    corners = [
        (x - hw, y - hl, 0), (x + hw, y - hl, 0),
        (x - hw, y + hl, 0), (x + hw, y + hl, 0),
        (x - hw, y - hl, h), (x + hw, y - hl, h),
        (x - hw, y + hl, h), (x + hw, y + hl, h),
    ]
    pixels = []
    for c in corners:
        pt = project_point_world(*c)
        if pt is not None:
            pixels.append(pt)
    if len(pixels) < 2:
        return None
    us = [p[0] for p in pixels]
    vs = [p[1] for p in pixels]
    return min(us), min(vs), max(us), max(vs)


def project_waterline(obj):
    """Project the waterline contact of an object (Z=0 base, front edge)."""
    x, y = obj["x"], obj["y"]
    hw, hl = obj["w"] / 2, obj["l"] / 2
    # Front-center at waterline
    return project_point_world(x, y - hl, 0)


# ---------------------------------------------------------------------------
# Run projections
# ---------------------------------------------------------------------------
horizon_v = compute_horizon_v()
print("=" * 60)
print("PROJECTION RESULTS")
print("=" * 60)
print(f"  Horizon at v = {horizon_v:.1f} px")
print()

projected = []
waterlines = []
for obj in objects:
    bbox = project_object_3d(obj)
    wl = project_waterline(obj)
    waterlines.append(wl)
    if bbox is None:
        print(f"  {obj['label']:20s}  — NOT VISIBLE")
        projected.append(None)
        continue
    u_min, v_min, u_max, v_max = bbox
    in_frame = (u_max >= 0 and u_min < IMAGE_W and v_max >= 0 and v_min < IMAGE_H)
    bearing = np.degrees(np.arctan2(obj["x"], obj["y"]))
    rng = np.sqrt(obj["x"]**2 + obj["y"]**2)
    print(f"  {obj['label']:20s}  range={rng:6.0f} m  bearing={bearing:+6.1f}°  "
          f"bbox=({u_min:7.1f}, {v_min:7.1f}) – ({u_max:7.1f}, {v_max:7.1f})  "
          f"size={u_max-u_min:.0f}x{v_max-v_min:.0f} px  "
          f"{'IN FRAME' if in_frame else 'PARTIAL/OUT'}")
    projected.append(bbox)
print()


# ---------------------------------------------------------------------------
# Render: sky + water gradients at projected horizon
# ---------------------------------------------------------------------------
def render_sky_water(ax, horizon_row, w, h):
    """Fill camera view with sky gradient above horizon, water below."""
    # Sky: light blue at horizon → deeper blue at top
    sky_top    = np.array([0.45, 0.62, 0.82])   # steel blue
    sky_bottom = np.array([0.78, 0.87, 0.96])   # pale sky near horizon
    # Water: dark teal at bottom → lighter teal near horizon
    water_top    = np.array([0.32, 0.50, 0.55])  # near horizon
    water_bottom = np.array([0.08, 0.22, 0.28])  # near camera (bottom of image)

    hr = int(np.clip(horizon_row, 0, h))

    # Build full image array
    img = np.zeros((h, w, 3))

    # Sky region (rows 0..hr)
    if hr > 0:
        for row in range(hr):
            frac = row / max(hr - 1, 1)  # 0 at top, 1 at horizon
            img[row, :, :] = sky_top * (1 - frac) + sky_bottom * frac

    # Water region (rows hr..h)
    water_rows = h - hr
    if water_rows > 0:
        for row in range(hr, h):
            frac = (row - hr) / max(water_rows - 1, 1)  # 0 at horizon, 1 at bottom
            img[row, :, :] = water_top * (1 - frac) + water_bottom * frac

    ax.imshow(img, extent=[0, w, h, 0], aspect="auto", zorder=0)


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
fig, (ax_top, ax_cam) = plt.subplots(1, 2, figsize=(18, 7),
                                      gridspec_kw={"width_ratios": [1, 1.5]})
fig.patch.set_facecolor(WHITE)

# ---- Top-down view --------------------------------------------------------
ax_top.set_facecolor(BLACK10)
ax_top.set_title("Top-Down World View", fontsize=14, fontweight="bold", color=BLACK90)
ax_top.set_xlabel("X  (m, cross-range)", fontsize=10, color=BLACK70)
ax_top.set_ylabel("Y  (m, range / forward)", fontsize=10, color=BLACK70)
ax_top.set_aspect("equal")
ax_top.grid(True, linewidth=0.4, color=BLACK30)

# FOV wedge
fov_range = 950
half_fov = HFOV_RAD / 2
angles = np.linspace(-half_fov, half_fov, 300)
wedge_x = fov_range * np.sin(angles)
wedge_y = fov_range * np.cos(angles)
ax_top.fill(np.concatenate([[0], wedge_x, [0]]),
            np.concatenate([[0], wedge_y, [0]]),
            alpha=0.08, color=ATLANTIC, zorder=1)
ax_top.plot(np.concatenate([[0], wedge_x, [0]]),
            np.concatenate([[0], wedge_y, [0]]),
            color=ATLANTIC, linewidth=1.0, linestyle="--", zorder=2)

# Camera
ax_top.plot(0, 0, marker="^", markersize=12, color=BLACK, zorder=5)
ax_top.annotate("Camera", (0, 0), textcoords="offset points",
                xytext=(10, -15), fontsize=9, color=BLACK90, fontweight="bold")

# Objects on top-down (show length as rectangle along Y)
for obj in objects:
    rect = plt.Rectangle(
        (obj["x"] - obj["w"] / 2, obj["y"] - obj["l"] / 2),
        obj["w"], obj["l"],
        linewidth=2, edgecolor=obj["color"],
        facecolor=obj["color"], alpha=0.65, zorder=4)
    ax_top.add_patch(rect)
    ax_top.annotate(obj["label"], (obj["x"], obj["y"]),
                    textcoords="offset points", xytext=(10, 6),
                    fontsize=8, color=obj["color"], fontweight="bold")

# Range rings
for r in [200, 400, 600, 800]:
    ring_angles = np.linspace(-np.pi / 2, np.pi / 2, 200)
    ax_top.plot(r * np.cos(ring_angles), r * np.sin(ring_angles),
                color=BLACK30, linewidth=0.6, linestyle=":", zorder=1)
    ax_top.text(5, r + 10, f"{r}m", fontsize=7, color=BLACK50)

ax_top.set_xlim(-300, 300)
ax_top.set_ylim(-50, 950)

# ---- Camera view ----------------------------------------------------------
ax_cam.set_title(f"Projected Camera View  (HFOV={HFOV_DEG:.0f}°, tilt={CAMERA_TILT:.0f}°)",
                 fontsize=14, fontweight="bold", color=BLACK90)
ax_cam.set_xlabel("u  (px)", fontsize=10, color=BLACK70)
ax_cam.set_ylabel("v  (px)", fontsize=10, color=BLACK70)
ax_cam.set_xlim(0, IMAGE_W)
ax_cam.set_ylim(IMAGE_H, 0)
ax_cam.set_aspect("equal")

# Sky + water background
render_sky_water(ax_cam, horizon_v, IMAGE_W, IMAGE_H)

# Horizon line
ax_cam.axhline(y=horizon_v, color=WHITE, linewidth=1.2, linestyle="-", alpha=0.6, zorder=2)
ax_cam.text(IMAGE_W - 10, horizon_v - 8, "horizon", fontsize=8, color=WHITE,
            ha="right", va="bottom", alpha=0.8, zorder=2)

# Draw projected objects as filled silhouettes + bounding boxes
for obj, bbox, wl in zip(objects, projected, waterlines):
    if bbox is None:
        continue
    u_min, v_min, u_max, v_max = bbox
    bw = u_max - u_min
    bh = v_max - v_min

    # Filled silhouette (darker fill for the "body" of the object)
    rect_fill = plt.Rectangle((u_min, v_min), bw, bh,
                               linewidth=0, facecolor=obj["color"],
                               alpha=0.50, zorder=3)
    ax_cam.add_patch(rect_fill)

    # Bounding box outline
    rect_outline = plt.Rectangle((u_min, v_min), bw, bh,
                                  linewidth=2, edgecolor=obj["color"],
                                  facecolor="none", zorder=4)
    ax_cam.add_patch(rect_outline)

    # Waterline marker (where object meets the water)
    if wl is not None:
        ax_cam.plot([u_min, u_max], [v_max, v_max], color=WHITE,
                    linewidth=1, alpha=0.5, zorder=4)

    # Label with range
    rng = np.sqrt(obj["x"]**2 + obj["y"]**2)
    label_y = max(v_min - 5, 12)
    ax_cam.text(u_min + bw / 2, label_y,
                f"{obj['label']}  ({rng:.0f} m)",
                fontsize=7.5, color=WHITE, fontweight="bold",
                ha="center", va="bottom",
                bbox=dict(boxstyle="square,pad=0.25", fc=obj["color"],
                          ec="none", alpha=0.9),
                zorder=5)

# Image border
for spine in ax_cam.spines.values():
    spine.set_edgecolor(BLACK90)
    spine.set_linewidth(1.5)

plt.tight_layout()
plt.savefig("world_to_camera_projection.png", dpi=200, bbox_inches="tight",
            facecolor=WHITE, edgecolor="none")
plt.show()
print("Saved → world_to_camera_projection.png")

# ---------------------------------------------------------------------------
# Math summary
# ---------------------------------------------------------------------------
print()
print("=" * 60)
print("MATH SUMMARY  (v2 — full extrinsic)")
print("=" * 60)
print(f"""
Pinhole Camera Model
────────────────────
    f = W / (2 * tan(FOV_h / 2))  =  {fx:.1f} px

         ┌ {fx:7.1f}     0    {cx:7.1f} ┐
    K =  │     0    {fy:7.1f}  {cy:7.1f} │
         └     0        0        1   ┘

Extrinsic [R | t]
─────────────────
Camera at world position (0, 0, {CAMERA_HEIGHT}) looking along +Y
with {CAMERA_TILT}° downward tilt.

    R = R_tilt({CAMERA_TILT}°) @ R_base

    R_base converts:  X_w → x_c,  Y_w → z_c,  Z_w → -y_c
    R_tilt  rotates:  pitch by {CAMERA_TILT}° around x_c axis

    t = -R @ [0, 0, {CAMERA_HEIGHT}]^T = [{t[0]:.2f}, {t[1]:.2f}, {t[2]:.2f}]

Full Projection
───────────────
    p_img = K @ [R | t] @ [X, Y, Z, 1]^T

    u = p_img[0] / p_img[2]
    v = p_img[1] / p_img[2]

Horizon
───────
    Direction to infinity along +Y at Z=0:
    d_cam = R @ [0, 1, 0]^T
    v_horizon = cy + fy * d_cam[1] / d_cam[2] = {horizon_v:.1f} px

    Sky:   rows 0 to {horizon_v:.0f}
    Water: rows {horizon_v:.0f} to {IMAGE_H}

3D Bounding Box
───────────────
Each object defined by (x, y, width, length, height).
8 corners projected; axis-aligned bbox taken in image space.
""")
