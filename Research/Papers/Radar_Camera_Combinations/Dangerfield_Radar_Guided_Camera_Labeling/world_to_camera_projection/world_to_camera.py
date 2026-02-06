"""
World-to-Camera Projection Demo
Demonstrates projecting objects from a top-down world view into
an ideal pinhole camera's image plane.

Camera model: pinhole with 100° horizontal FOV
Objects: 5 maritime targets at varying ranges and bearings
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# ---------------------------------------------------------------------------
# Brand palette
# ---------------------------------------------------------------------------
GARNET = "#73000A"
BLACK = "#000000"
WHITE = "#FFFFFF"
BLACK90 = "#363636"
BLACK70 = "#5C5C5C"
BLACK50 = "#A2A2A2"
BLACK30 = "#C7C7C7"
BLACK10 = "#ECECEC"
ROSE = "#CC2E40"
ATLANTIC = "#466A9F"
CONGAREE = "#1F414D"
HORSESHOE = "#65780B"
HONEYCOMB = "#A49137"

OBJ_COLORS = [GARNET, ATLANTIC, HORSESHOE, ROSE, CONGAREE]

# ---------------------------------------------------------------------------
# Camera parameters
# ---------------------------------------------------------------------------
HFOV_DEG = 100.0                       # horizontal field of view (degrees)
IMAGE_W = 1920                         # image width  (px)
IMAGE_H = 1080                         # image height (px)
CAMERA_HEIGHT = 15.0                   # camera mounted 15 m above waterline

HFOV_RAD = np.deg2rad(HFOV_DEG)
VFOV_RAD = 2 * np.arctan(IMAGE_H / IMAGE_W * np.tan(HFOV_RAD / 2))
VFOV_DEG = np.deg2rad(VFOV_RAD)       # for reference

# Focal length in pixels (from horizontal FOV)
fx = IMAGE_W / (2.0 * np.tan(HFOV_RAD / 2.0))
fy = fx                                # square pixels
cx = IMAGE_W / 2.0                     # principal point
cy = IMAGE_H / 2.0

# Intrinsic matrix K
K = np.array([
    [fx,  0, cx],
    [ 0, fy, cy],
    [ 0,  0,  1],
])

print("=" * 60)
print("CAMERA INTRINSICS")
print("=" * 60)
print(f"  Horizontal FOV : {HFOV_DEG:.1f}°")
print(f"  Vertical FOV   : {np.degrees(VFOV_RAD):.1f}°")
print(f"  Image size      : {IMAGE_W} x {IMAGE_H} px")
print(f"  Focal length    : fx = fy = {fx:.1f} px")
print(f"  Principal point : ({cx:.1f}, {cy:.1f})")
print(f"  Camera height   : {CAMERA_HEIGHT:.1f} m above water")
print()
print("  K =")
for row in K:
    print(f"      [{row[0]:9.2f}  {row[1]:9.2f}  {row[2]:9.2f}]")
print()

# ---------------------------------------------------------------------------
# World objects  (top-down coordinates: +X = right, +Y = forward / range)
# Each object has (x_world, y_world, width, height_above_water, label)
# ---------------------------------------------------------------------------
objects = [
    {"x":  -80, "y":  200, "w": 12, "h": 8,  "label": "Fishing Vessel",  "color": OBJ_COLORS[0]},
    {"x":   30, "y":  350, "w": 25, "h": 15, "label": "Cargo Ship",      "color": OBJ_COLORS[1]},
    {"x": -150, "y":  500, "w": 18, "h": 10, "label": "Sailboat",        "color": OBJ_COLORS[2]},
    {"x":  100, "y":  150, "w": 6,  "h": 3,  "label": "Buoy",            "color": OBJ_COLORS[3]},
    {"x":  -20, "y":  800, "w": 40, "h": 20, "label": "Tanker",          "color": OBJ_COLORS[4]},
]

# ---------------------------------------------------------------------------
# Projection math
# ---------------------------------------------------------------------------
# Camera sits at world origin looking along +Y (forward).
# World frame:  X = right,  Y = forward (range),  Z = up
# Camera frame: x = right,  y = down,              z = forward (optical axis)
#
# Rotation from world to camera (90° tilt so Z_world -> -y_cam, Y_world -> z_cam):
#   x_cam =  X_world
#   y_cam = -Z_world
#   z_cam =  Y_world
#
# For a point at (X, Y, Z_top) in world coords the camera-frame coords are:
#   p_cam = [X,  -(Z_top),  Y]
# where Z_top is the height above water of the point.

def project_point(X, Y, Z):
    """Project a world point (X=right, Y=forward, Z=up) into pixel coords."""
    p_cam = np.array([X, -Z, Y])       # world -> camera frame
    if p_cam[2] <= 0:
        return None                     # behind camera
    p_img = K @ p_cam
    u = p_img[0] / p_img[2]
    v = p_img[1] / p_img[2]
    return u, v


def project_object(obj):
    """
    Project an object's bounding footprint into image-space bounding box.
    Returns (u_min, v_min, u_max, v_max) or None if not visible.

    We project the 8 corners of a 3-D bounding box:
        base at Z=0 (waterline),  top at Z=h
        left  at X - w/2,        right at X + w/2
        near  at Y (front face), far   at Y (same — treat as thin along range for simplicity)
    """
    x, y, w, h = obj["x"], obj["y"], obj["w"], obj["h"]
    corners_world = [
        (x - w / 2, y, 0),
        (x + w / 2, y, 0),
        (x - w / 2, y, h),
        (x + w / 2, y, h),
    ]
    # Shift Z by camera height (camera is at Z = CAMERA_HEIGHT)
    pixels = []
    for (X, Y, Z) in corners_world:
        Z_rel = Z - CAMERA_HEIGHT       # relative to camera
        pt = project_point(X, Y, Z_rel)
        if pt is not None:
            pixels.append(pt)
    if len(pixels) < 2:
        return None
    us = [p[0] for p in pixels]
    vs = [p[1] for p in pixels]
    return min(us), min(vs), max(us), max(vs)


# ---------------------------------------------------------------------------
# Run projection
# ---------------------------------------------------------------------------
print("=" * 60)
print("PROJECTION RESULTS")
print("=" * 60)

projected = []
for obj in objects:
    bbox = project_object(obj)
    if bbox is None:
        print(f"  {obj['label']:20s}  — NOT VISIBLE (behind camera or out of frame)")
        projected.append(None)
        continue

    u_min, v_min, u_max, v_max = bbox
    in_frame = (u_max >= 0 and u_min < IMAGE_W and v_max >= 0 and v_min < IMAGE_H)

    bearing = np.degrees(np.arctan2(obj["x"], obj["y"]))

    print(f"  {obj['label']:20s}  range={obj['y']:5.0f} m  bearing={bearing:+6.1f}°  "
          f"bbox=({u_min:7.1f}, {v_min:7.1f}) – ({u_max:7.1f}, {v_max:7.1f})  "
          f"{'IN FRAME' if in_frame else 'OUT OF FRAME'}")
    projected.append(bbox if in_frame else bbox)  # keep for drawing even if partially out

print()

# ---------------------------------------------------------------------------
# Figure: side-by-side top-down view + camera view
# ---------------------------------------------------------------------------
fig, (ax_top, ax_cam) = plt.subplots(1, 2, figsize=(16, 7),
                                      gridspec_kw={"width_ratios": [1, 1.4]})
fig.patch.set_facecolor(WHITE)

# ---- Top-down view --------------------------------------------------------
ax_top.set_facecolor(BLACK10)
ax_top.set_title("Top-Down World View", fontsize=14, fontweight="bold", color=BLACK90)
ax_top.set_xlabel("X  (m, cross-range)", fontsize=10, color=BLACK70)
ax_top.set_ylabel("Y  (m, range / forward)", fontsize=10, color=BLACK70)
ax_top.set_aspect("equal")
ax_top.grid(True, linewidth=0.4, color=BLACK30)

# Draw camera FOV wedge
fov_range = 900
half_fov = HFOV_RAD / 2
left_edge  = np.array([-fov_range * np.sin(half_fov), fov_range * np.cos(half_fov)])
right_edge = np.array([ fov_range * np.sin(half_fov), fov_range * np.cos(half_fov)])
angles = np.linspace(-half_fov, half_fov, 200)
wedge_x = fov_range * np.sin(angles)
wedge_y = fov_range * np.cos(angles)
ax_top.fill(np.concatenate([[0], wedge_x, [0]]),
            np.concatenate([[0], wedge_y, [0]]),
            alpha=0.10, color=ATLANTIC, zorder=1)
ax_top.plot(np.concatenate([[0], wedge_x, [0]]),
            np.concatenate([[0], wedge_y, [0]]),
            color=ATLANTIC, linewidth=1.0, linestyle="--", zorder=2)

# Camera position
ax_top.plot(0, 0, marker="^", markersize=12, color=BLACK, zorder=5)
ax_top.annotate("Camera", (0, 0), textcoords="offset points",
                xytext=(10, -15), fontsize=9, color=BLACK90, fontweight="bold")

# Plot objects
for obj in objects:
    rect = plt.Rectangle((obj["x"] - obj["w"] / 2, obj["y"] - obj["w"] / 4),
                          obj["w"], obj["w"] / 2,
                          linewidth=2, edgecolor=obj["color"],
                          facecolor=obj["color"], alpha=0.7, zorder=4)
    ax_top.add_patch(rect)
    ax_top.annotate(obj["label"], (obj["x"], obj["y"]),
                    textcoords="offset points", xytext=(8, 6),
                    fontsize=8, color=obj["color"], fontweight="bold")

ax_top.set_xlim(-300, 300)
ax_top.set_ylim(-50, 900)

# ---- Camera view ----------------------------------------------------------
ax_cam.set_facecolor(CONGAREE)          # dark "sky / sea" background
ax_cam.set_title(f"Projected Camera View  (HFOV = {HFOV_DEG:.0f}°)",
                 fontsize=14, fontweight="bold", color=BLACK90)
ax_cam.set_xlabel("u  (px)", fontsize=10, color=BLACK70)
ax_cam.set_ylabel("v  (px)", fontsize=10, color=BLACK70)
ax_cam.set_xlim(0, IMAGE_W)
ax_cam.set_ylim(IMAGE_H, 0)            # image coords: v increases downward
ax_cam.set_aspect("equal")

# Draw horizon line (Z=0 plane from camera height)
# Horizon is at v = cy + fy * (CAMERA_HEIGHT) / inf → v = cy  (at infinity)
ax_cam.axhline(y=cy, color=BLACK50, linewidth=0.8, linestyle="--", zorder=1)
ax_cam.annotate("horizon", (IMAGE_W - 80, cy), textcoords="offset points",
                xytext=(0, -10), fontsize=8, color=BLACK50)

# Draw bounding boxes
for obj, bbox in zip(objects, projected):
    if bbox is None:
        continue
    u_min, v_min, u_max, v_max = bbox
    bw = u_max - u_min
    bh = v_max - v_min
    rect = plt.Rectangle((u_min, v_min), bw, bh,
                          linewidth=2, edgecolor=obj["color"],
                          facecolor=obj["color"], alpha=0.35, zorder=3)
    ax_cam.add_patch(rect)
    # Outline
    rect2 = plt.Rectangle((u_min, v_min), bw, bh,
                           linewidth=2, edgecolor=obj["color"],
                           facecolor="none", zorder=4)
    ax_cam.add_patch(rect2)

    # Label
    label_y = max(v_min - 8, 15)
    ax_cam.text(u_min + bw / 2, label_y, f"{obj['label']}  ({obj['y']}m)",
                fontsize=7, color=WHITE, fontweight="bold",
                ha="center", va="bottom",
                bbox=dict(boxstyle="square,pad=0.2", fc=obj["color"], ec="none", alpha=0.85),
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
# Print the full math summary
# ---------------------------------------------------------------------------
print()
print("=" * 60)
print("MATH SUMMARY")
print("=" * 60)
print("""
Pinhole Camera Model
────────────────────
Given horizontal FOV (θ_h) and image width (W):

    f_x = W / (2 · tan(θ_h / 2))

Intrinsic matrix:

         ┌ f_x   0   c_x ┐
    K =  │  0   f_y  c_y  │
         └  0    0    1   ┘

where c_x = W/2, c_y = H/2 (principal point at image center).

Coordinate Transform (World → Camera)
──────────────────────────────────────
World:  X = right,  Y = forward (range),  Z = up
Camera: x = right,  y = down,             z = forward (optical axis)

For a camera at height h looking forward along +Y:

    ┌ x_cam ┐     ┌ 1   0   0 ┐ ┌ X_world         ┐
    │ y_cam │  =  │ 0   0  -1 │ │ Z_world - h_cam  │
    └ z_cam ┘     └ 0   1   0 ┘ └ Y_world          ┘

Projection
──────────
    ┌ u·w ┐         ┌ x_cam ┐
    │ v·w │  =  K · │ y_cam │
    └  w  ┘         └ z_cam ┘

    u = (u·w) / w ,   v = (v·w) / w

Key Observations
────────────────
• Objects farther away → smaller bounding boxes (1/range scaling)
• Objects off-center → shifted toward image edges
• Objects beyond ±θ_h/2 bearing → outside the frame
• Apparent vertical position depends on camera height + object height
""")
