"""
Demo 4: Metric Verification
Photograph an object with known dimensions, run Metric3D v2, and compare
predicted measurements to ground truth.

Usage:
    python demo4_metric_verification.py \
        --image textbook.jpg \
        --points "100,200 300,200" \
        --gt-distance 0.279 \
        --label "Textbook width" \
        --output ../figures/

The --points flag takes two pixel coordinates (x1,y1 x2,y2) between which
the ground-truth distance is known.
"""

import argparse
import os
import numpy as np
import cv2
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

SANDSTORM = np.array([255, 242, 227]) / 255.0
ATLANTIC = np.array([70, 106, 159]) / 255.0
CONGAREE = np.array([31, 65, 77]) / 255.0

depth_cmap = LinearSegmentedColormap.from_list('depth_brand', [
    SANDSTORM, ATLANTIC, CONGAREE
])


def measure_3d_distance(depth, p1, p2, fx, fy, cx, cy):
    """Compute 3D Euclidean distance between two pixel locations using depth."""
    u1, v1 = p1
    u2, v2 = p2

    z1 = depth[v1, u1]
    z2 = depth[v2, u2]

    x1 = (u1 - cx) * z1 / fx
    y1 = (v1 - cy) * z1 / fy

    x2 = (u2 - cx) * z2 / fx
    y2 = (v2 - cy) * z2 / fy

    dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    return dist, (x1, y1, z1), (x2, y2, z2)


def create_verification_figure(rgb, depth, p1, p2, pred_dist, gt_dist, label, output_path):
    """Create annotated figure showing measurement."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # RGB with measurement overlay
    axes[0].imshow(rgb)
    axes[0].plot([p1[0], p2[0]], [p1[1], p2[1]], '-o',
                 color='#73000A', linewidth=2, markersize=8, markerfacecolor='#CC2E40')
    mid_x = (p1[0] + p2[0]) / 2
    mid_y = (p1[1] + p2[1]) / 2
    axes[0].annotate(f'{label}\nGT: {gt_dist:.3f} m\nPred: {pred_dist:.3f} m',
                     xy=(mid_x, mid_y), fontsize=11, fontweight='bold',
                     color='white', ha='center',
                     bbox=dict(boxstyle='square,pad=0.3', facecolor='#73000A', alpha=0.85))
    axes[0].set_title('Measurement', fontsize=14, fontweight='bold', color='#363636')
    axes[0].axis('off')

    # Depth with measurement overlay
    vmax = np.percentile(depth[depth > 0], 98) if np.any(depth > 0) else depth.max()
    im = axes[1].imshow(depth, cmap=depth_cmap, vmin=0, vmax=vmax)
    axes[1].plot([p1[0], p2[0]], [p1[1], p2[1]], '-o',
                 color='#73000A', linewidth=2, markersize=8, markerfacecolor='#CC2E40')

    # Depth values at measurement points
    z1 = depth[p1[1], p1[0]]
    z2 = depth[p2[1], p2[0]]
    axes[1].annotate(f'{z1:.2f}m', xy=(p1[0], p1[1]), fontsize=9,
                     color='white', fontweight='bold',
                     bbox=dict(boxstyle='square,pad=0.2', facecolor='#466A9F', alpha=0.85),
                     xytext=(10, -15), textcoords='offset points')
    axes[1].annotate(f'{z2:.2f}m', xy=(p2[0], p2[1]), fontsize=9,
                     color='white', fontweight='bold',
                     bbox=dict(boxstyle='square,pad=0.2', facecolor='#466A9F', alpha=0.85),
                     xytext=(10, -15), textcoords='offset points')

    axes[1].set_title('Metric Depth', fontsize=14, fontweight='bold', color='#466A9F')
    axes[1].axis('off')
    plt.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04, label='Depth (m)')

    # Error annotation
    error_pct = abs(pred_dist - gt_dist) / gt_dist * 100
    fig.suptitle(f'Metric Verification: {label} | Error: {error_pct:.1f}%',
                 fontsize=16, fontweight='bold', color='#73000A', y=1.02)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Metric Depth Verification')
    parser.add_argument('--image', required=True)
    parser.add_argument('--depth', default=None, help='Pre-computed depth .npy')
    parser.add_argument('--points', required=True,
                        help='Two pixel coordinates: "x1,y1 x2,y2"')
    parser.add_argument('--gt-distance', type=float, required=True,
                        help='Ground truth distance in meters')
    parser.add_argument('--label', default='Measurement',
                        help='Label for the measurement')
    parser.add_argument('--focal', type=float, default=None)
    parser.add_argument('--output', default='../figures')
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    name = Path(args.image).stem

    # Parse points
    parts = args.points.strip().split()
    p1 = tuple(int(x) for x in parts[0].split(','))
    p2 = tuple(int(x) for x in parts[1].split(','))

    # Load image
    rgb = cv2.imread(args.image)
    rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    h, w = rgb.shape[:2]

    # Get depth
    if args.depth and os.path.exists(args.depth):
        depth = np.load(args.depth)
    else:
        print("Running Metric3D v2 inference...")
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

    # Measure
    pred_dist, pt3d_1, pt3d_2 = measure_3d_distance(depth, p1, p2, fx, fy, cx, cy)

    print(f"\n{'='*50}")
    print(f"Measurement: {args.label}")
    print(f"  Point 1: pixel ({p1[0]}, {p1[1]}) -> 3D ({pt3d_1[0]:.3f}, {pt3d_1[1]:.3f}, {pt3d_1[2]:.3f})")
    print(f"  Point 2: pixel ({p2[0]}, {p2[1]}) -> 3D ({pt3d_2[0]:.3f}, {pt3d_2[1]:.3f}, {pt3d_2[2]:.3f})")
    print(f"  Predicted distance: {pred_dist:.4f} m")
    print(f"  Ground truth:       {args.gt_distance:.4f} m")
    print(f"  Error:              {abs(pred_dist - args.gt_distance):.4f} m ({abs(pred_dist - args.gt_distance)/args.gt_distance*100:.1f}%)")
    print(f"{'='*50}")

    # Create figure
    out_path = os.path.join(args.output, f'{name}_verification.png')
    create_verification_figure(rgb, depth, p1, p2, pred_dist, args.gt_distance,
                               args.label, out_path)


if __name__ == '__main__':
    main()
