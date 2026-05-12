"""
Demo 2: Competitor Comparison (Metric3D v2 vs DepthAnything v2)
Generates side-by-side comparisons showing metric vs relative depth.

Usage:
    python demo2_competitor_comparison.py --images path/to/images/ --output ../figures/

Prerequisites:
    pip install transformers depth-anything-v2  # or use HuggingFace pipeline
"""

import argparse
import os
import glob
import numpy as np
import torch
import cv2
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Brand colors
SANDSTORM = np.array([255, 242, 227]) / 255.0
ATLANTIC = np.array([70, 106, 159]) / 255.0
CONGAREE = np.array([31, 65, 77]) / 255.0
GARNET = np.array([115, 0, 10]) / 255.0

depth_cmap = LinearSegmentedColormap.from_list('depth_brand', [
    SANDSTORM, ATLANTIC, CONGAREE
])


def load_metric3d(model_name='metric3d_vit_large'):
    """Load Metric3D v2."""
    model = torch.hub.load('yvanyin/metric3d', model_name, pretrain=True)
    model.cuda().eval()
    return model


def load_depth_anything():
    """Load DepthAnything v2 via HuggingFace transformers."""
    from transformers import pipeline
    pipe = pipeline(
        task="depth-estimation",
        model="depth-anything/Depth-Anything-V2-Large-hf",
        device=0
    )
    return pipe


def run_metric3d(model, image_path):
    """Run Metric3D v2 and return metric depth in meters."""
    from demo1_inference import get_intrinsics_from_exif

    rgb = cv2.imread(image_path)
    rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    h, w = rgb.shape[:2]

    focal_px = get_intrinsics_from_exif(image_path)

    input_size = (616, 1064)
    scale = min(input_size[0] / h, input_size[1] / w)
    rgb_resized = cv2.resize(rgb, (int(w * scale), int(h * scale)))

    pad_h = input_size[0] - rgb_resized.shape[0]
    pad_w = input_size[1] - rgb_resized.shape[1]
    rgb_padded = np.pad(rgb_resized, ((0, pad_h), (0, pad_w), (0, 0)),
                        mode='constant', constant_values=0)

    mean = np.array([123.675, 116.28, 103.53])
    std = np.array([58.395, 57.12, 57.375])
    rgb_norm = (rgb_padded.astype(np.float32) - mean) / std
    rgb_tensor = torch.from_numpy(rgb_norm).permute(2, 0, 1).unsqueeze(0).float().cuda()

    intrinsic_scaled = [focal_px * scale, focal_px * scale,
                        w / 2.0 * scale, h / 2.0 * scale]

    with torch.no_grad():
        pred_depth, confidence, output_dict = model.inference({
            'input': rgb_tensor,
            'intrinsic': intrinsic_scaled
        })

    depth = pred_depth.squeeze().cpu().numpy()
    depth = depth[:int(h * scale), :int(w * scale)]
    depth = cv2.resize(depth, (w, h))
    depth = depth * (focal_px / 1000.0)  # de-canonical

    return depth, rgb


def run_depth_anything(pipe, image_path):
    """Run DepthAnything v2 and return relative depth (arbitrary scale)."""
    from PIL import Image
    img = Image.open(image_path)
    result = pipe(img)
    depth = np.array(result['depth'])
    return depth


def create_comparison(image_path, metric_depth, relative_depth, rgb, output_dir):
    """Create side-by-side comparison figure."""
    name = Path(image_path).stem

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # RGB
    axes[0].imshow(rgb)
    axes[0].set_title('Input RGB', fontsize=14, fontweight='bold', color='#363636')
    axes[0].axis('off')

    # Metric3D v2 (metric depth)
    vmax = np.percentile(metric_depth[metric_depth > 0], 98)
    im1 = axes[1].imshow(metric_depth, cmap=depth_cmap, vmin=0, vmax=vmax)
    axes[1].set_title('Metric3D v2 (metric, meters)', fontsize=14,
                       fontweight='bold', color='#73000A')
    axes[1].axis('off')
    cbar1 = plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
    cbar1.set_label('Depth (m)', fontsize=10)

    # DepthAnything v2 (relative depth)
    im2 = axes[2].imshow(relative_depth, cmap='gray')
    axes[2].set_title('DepthAnything v2 (relative, no units)', fontsize=14,
                       fontweight='bold', color='#5C5C5C')
    axes[2].axis('off')
    cbar2 = plt.colorbar(im2, ax=axes[2], fraction=0.046, pad=0.04)
    cbar2.set_label('Relative depth (a.u.)', fontsize=10)

    plt.tight_layout()
    out_path = os.path.join(output_dir, f'{name}_comparison.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: {out_path}")


def main():
    parser = argparse.ArgumentParser(description='Metric vs Relative Depth Comparison')
    parser.add_argument('--images', nargs='+', required=True)
    parser.add_argument('--output', default='../figures')
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    image_paths = []
    for p in args.images:
        if os.path.isdir(p):
            for ext in ['*.jpg', '*.jpeg', '*.png']:
                image_paths.extend(glob.glob(os.path.join(p, ext)))
        else:
            image_paths.append(p)

    print(f"Found {len(image_paths)} images")
    print("Loading Metric3D v2...")
    metric3d = load_metric3d()
    print("Loading DepthAnything v2...")
    da_pipe = load_depth_anything()

    for img_path in sorted(image_paths):
        print(f"\nProcessing: {img_path}")
        metric_depth, rgb = run_metric3d(metric3d, img_path)
        relative_depth = run_depth_anything(da_pipe, img_path)

        # Resize relative depth to match
        relative_depth = cv2.resize(relative_depth, (rgb.shape[1], rgb.shape[0]))

        create_comparison(img_path, metric_depth, relative_depth, rgb, args.output)

    print("\nDone!")


if __name__ == '__main__':
    main()
