"""
Demo 3: 3D Point Cloud from Metric Depth
Back-projects depth to 3D, exports PLY, renders rotating view as GIF.

Usage:
    python demo3_point_cloud.py --image photo.jpg --depth photo_depth.npy --output ../figures/
    python demo3_point_cloud.py --image photo.jpg --output ../figures/  # runs inference too

Prerequisites:
    pip install open3d trimesh
"""

import argparse
import os
import numpy as np
import cv2
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def depth_to_pointcloud(depth, rgb, fx, fy, cx, cy, max_depth=50.0):
    """Back-project depth map to 3D point cloud.

    X = (u - cx) * D / fx
    Y = (v - cy) * D / fy
    Z = D
    """
    h, w = depth.shape
    u, v = np.meshgrid(np.arange(w), np.arange(h))

    # Filter invalid depths
    valid = (depth > 0.1) & (depth < max_depth)

    z = depth[valid]
    x = (u[valid] - cx) * z / fx
    y = (v[valid] - cy) * z / fy

    points = np.stack([x, y, z], axis=1)
    colors = rgb[valid] / 255.0  # Normalize to [0,1]

    return points, colors


def save_ply(points, colors, filepath):
    """Save point cloud as PLY file."""
    n = len(points)
    header = f"""ply
format ascii 1.0
element vertex {n}
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
"""
    colors_uint8 = (colors * 255).clip(0, 255).astype(np.uint8)
    with open(filepath, 'w') as f:
        f.write(header)
        for i in range(n):
            f.write(f"{points[i,0]:.4f} {points[i,1]:.4f} {points[i,2]:.4f} "
                    f"{colors_uint8[i,0]} {colors_uint8[i,1]} {colors_uint8[i,2]}\n")
    print(f"  Saved PLY: {filepath} ({n} points)")


def render_rotating_gif(points, colors, output_path, n_frames=36):
    """Render a rotating point cloud as a GIF using Open3D offscreen."""
    try:
        import open3d as o3d

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        pcd.colors = o3d.utility.Vector3dVector(colors)

        # Downsample for performance
        if len(points) > 500000:
            pcd = pcd.voxel_down_sample(voxel_size=0.05)

        vis = o3d.visualization.Visualizer()
        vis.create_window(width=800, height=600, visible=False)
        vis.add_geometry(pcd)

        ctr = vis.get_view_control()
        frames = []

        for i in range(n_frames):
            ctr.rotate(360.0 / n_frames * 10, 0)
            vis.poll_events()
            vis.update_renderer()
            img = np.asarray(vis.capture_screen_float_buffer())
            frames.append((img * 255).astype(np.uint8))

        vis.destroy_window()

        # Save as GIF
        from PIL import Image
        pil_frames = [Image.fromarray(f) for f in frames]
        pil_frames[0].save(
            output_path,
            save_all=True,
            append_images=pil_frames[1:],
            duration=100,
            loop=0
        )
        print(f"  Saved rotating GIF: {output_path}")

    except ImportError:
        print("  Open3D not available -- saving static matplotlib view instead")
        render_static_views(points, colors, output_path)


def render_static_views(points, colors, output_path):
    """Fallback: render static 3D views with matplotlib."""
    # Subsample for matplotlib
    n = len(points)
    if n > 100000:
        idx = np.random.choice(n, 100000, replace=False)
        points = points[idx]
        colors = colors[idx]

    fig = plt.figure(figsize=(16, 6))

    for i, (elev, azim, title) in enumerate([
        (30, -60, 'Front View'),
        (30, -150, 'Side View'),
        (80, -60, 'Top-Down View')
    ]):
        ax = fig.add_subplot(1, 3, i + 1, projection='3d')
        ax.scatter(points[:, 0], points[:, 2], -points[:, 1],
                   c=colors, s=0.1, alpha=0.5)
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(title, fontsize=12, fontweight='bold', color='#363636')
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Z (m)')
        ax.set_zlabel('Y (m)')

    plt.tight_layout()
    out_png = output_path.replace('.gif', '.png')
    plt.savefig(out_png, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved static views: {out_png}")


def main():
    parser = argparse.ArgumentParser(description='3D Point Cloud from Metric Depth')
    parser.add_argument('--image', required=True, help='Input RGB image')
    parser.add_argument('--depth', default=None,
                        help='Pre-computed depth .npy file (if not provided, runs inference)')
    parser.add_argument('--focal', type=float, default=None,
                        help='Focal length in pixels (auto-detected from EXIF if not provided)')
    parser.add_argument('--output', default='../figures')
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    name = Path(args.image).stem

    # Load RGB
    rgb = cv2.imread(args.image)
    rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    h, w = rgb.shape[:2]

    # Get depth
    if args.depth and os.path.exists(args.depth):
        depth = np.load(args.depth)
        print(f"Loaded depth from {args.depth}")
    else:
        print("Running Metric3D v2 inference for depth...")
        from demo1_inference import load_model, run_inference
        model = load_model()
        depth, _ = run_inference(model, args.image, args.output)

    # Get focal length
    if args.focal:
        fx = fy = args.focal
    else:
        from demo1_inference import get_intrinsics_from_exif
        fx = fy = get_intrinsics_from_exif(args.image)

    cx, cy = w / 2.0, h / 2.0

    print(f"Image: {w}x{h}, focal: {fx:.0f}px")
    print(f"Depth range: {depth.min():.2f} - {depth.max():.2f} m")

    # Create point cloud
    points, colors = depth_to_pointcloud(depth, rgb, fx, fy, cx, cy)
    print(f"Generated {len(points)} 3D points")

    # Save PLY
    ply_path = os.path.join(args.output, f'{name}_pointcloud.ply')
    save_ply(points, colors, ply_path)

    # Render rotating view
    gif_path = os.path.join(args.output, f'{name}_pointcloud_rotate.gif')
    render_rotating_gif(points, colors, gif_path)

    print("\nDone!")


if __name__ == '__main__':
    main()
