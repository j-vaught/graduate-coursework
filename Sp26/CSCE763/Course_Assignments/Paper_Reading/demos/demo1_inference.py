"""
Demo 1: Metric3D v2 Inference
Run on GPU server (comech) via SSH. Generates depth maps and surface normals.

Usage:
    python demo1_inference.py --images path/to/images/ --output ../figures/
    python demo1_inference.py --images img1.jpg img2.jpg --output ../figures/
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

# Brand colors for colormaps
GARNET = np.array([115, 0, 10]) / 255.0
ATLANTIC = np.array([70, 106, 159]) / 255.0
CONGAREE = np.array([31, 65, 77]) / 255.0
WHITE = np.array([1.0, 1.0, 1.0])
SANDSTORM = np.array([255, 242, 227]) / 255.0

# Custom depth colormap: sandstorm (near) -> atlantic (mid) -> congaree (far)
depth_cmap = LinearSegmentedColormap.from_list('depth_brand', [
    SANDSTORM, ATLANTIC, CONGAREE
])

# Custom normal colormap is not needed -- normals use RGB encoding directly


def load_model(model_name='metric3d_vit_large'):
    """Load Metric3D v2 from PyTorch Hub."""
    model = torch.hub.load('yvanyin/metric3d', model_name, pretrain=True)
    model.cuda().eval()
    return model


def get_intrinsics_from_exif(image_path):
    """Attempt to extract focal length from EXIF data.
    Falls back to a reasonable default if EXIF is unavailable."""
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
        img = Image.open(image_path)
        exif = img._getexif()
        if exif:
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == 'FocalLengthIn35mmFilm':
                    # Convert 35mm equivalent to pixels (assuming typical sensor)
                    focal_35mm = float(value)
                    w, h = img.size
                    # 35mm film is 36mm wide
                    focal_px = focal_35mm * w / 36.0
                    print(f"  EXIF focal length: {focal_35mm}mm (35mm equiv) -> {focal_px:.0f}px")
                    return focal_px
                elif tag == 'FocalLength':
                    focal_mm = float(value)
                    w, h = img.size
                    # Assume typical crop factor ~1.5
                    focal_px = focal_mm * 1.5 * w / 36.0
                    print(f"  EXIF focal length: {focal_mm}mm -> {focal_px:.0f}px (estimated)")
                    return focal_px
    except Exception as e:
        print(f"  EXIF extraction failed: {e}")

    # Default: assume ~50mm equivalent on 35mm
    w = cv2.imread(image_path).shape[1]
    focal_px = 50.0 * w / 36.0
    print(f"  Using default focal length: 50mm equiv -> {focal_px:.0f}px")
    return focal_px


def run_inference(model, image_path, output_dir):
    """Run Metric3D v2 inference on a single image."""
    name = Path(image_path).stem
    print(f"\nProcessing: {image_path}")

    # Load image
    rgb = cv2.imread(image_path)
    if rgb is None:
        print(f"  ERROR: Could not read {image_path}")
        return
    rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    h, w = rgb.shape[:2]

    # Get intrinsics
    focal_px = get_intrinsics_from_exif(image_path)
    intrinsic = [focal_px, focal_px, w / 2.0, h / 2.0]

    # Prepare input (resize to model input size)
    input_size = (616, 1064)  # Standard Metric3D v2 input
    scale = min(input_size[0] / h, input_size[1] / w)
    rgb_resized = cv2.resize(rgb, (int(w * scale), int(h * scale)),
                             interpolation=cv2.INTER_LINEAR)

    # Pad to exact input size
    pad_h = input_size[0] - rgb_resized.shape[0]
    pad_w = input_size[1] - rgb_resized.shape[1]
    rgb_padded = np.pad(rgb_resized, ((0, pad_h), (0, pad_w), (0, 0)),
                        mode='constant', constant_values=0)

    # Normalize
    mean = np.array([123.675, 116.28, 103.53])
    std = np.array([58.395, 57.12, 57.375])
    rgb_norm = (rgb_padded.astype(np.float32) - mean) / std
    rgb_tensor = torch.from_numpy(rgb_norm).permute(2, 0, 1).unsqueeze(0).float().cuda()

    # Adjust intrinsics for resize
    intrinsic_scaled = [intrinsic[0] * scale, intrinsic[1] * scale,
                        intrinsic[2] * scale, intrinsic[3] * scale]

    # Inference
    with torch.no_grad():
        pred_depth, confidence, output_dict = model.inference({
            'input': rgb_tensor,
            'intrinsic': intrinsic_scaled
        })

    # Extract outputs and remove padding
    depth = pred_depth.squeeze().cpu().numpy()
    depth = depth[:int(h * scale), :int(w * scale)]
    depth = cv2.resize(depth, (w, h), interpolation=cv2.INTER_LINEAR)

    # De-canonical transform
    canonical_focal = 1000.0
    depth = depth * (focal_px / canonical_focal)

    # Surface normals
    if 'prediction_normal' in output_dict:
        normals = output_dict['prediction_normal'][:, :3, :, :].squeeze().cpu().numpy()
        normals = normals[:, :int(h * scale), :int(w * scale)]
        normals = np.transpose(normals, (1, 2, 0))
        normals = cv2.resize(normals, (w, h), interpolation=cv2.INTER_LINEAR)
        # Normalize
        norm_mag = np.linalg.norm(normals, axis=2, keepdims=True)
        normals = normals / (norm_mag + 1e-8)
        # Convert to RGB visualization: [-1,1] -> [0,255]
        normal_vis = ((normals + 1) / 2 * 255).clip(0, 255).astype(np.uint8)
    else:
        normal_vis = None
        print("  WARNING: No normal prediction in output")

    # Save individual outputs
    np.save(os.path.join(output_dir, f'{name}_depth.npy'), depth)

    # Create side-by-side visualization
    fig_w = 18 if normal_vis is not None else 12
    n_cols = 3 if normal_vis is not None else 2
    fig, axes = plt.subplots(1, n_cols, figsize=(fig_w, 6))

    # RGB
    axes[0].imshow(rgb)
    axes[0].set_title('Input RGB', fontsize=14, fontweight='bold', color='#363636')
    axes[0].axis('off')

    # Depth
    vmax = np.percentile(depth[depth > 0], 98) if np.any(depth > 0) else depth.max()
    im_d = axes[1].imshow(depth, cmap=depth_cmap, vmin=0, vmax=vmax)
    axes[1].set_title('Metric Depth (m)', fontsize=14, fontweight='bold', color='#466A9F')
    axes[1].axis('off')
    cbar = plt.colorbar(im_d, ax=axes[1], fraction=0.046, pad=0.04)
    cbar.set_label('Depth (m)', fontsize=10)

    # Normals
    if normal_vis is not None:
        axes[2].imshow(normal_vis)
        axes[2].set_title('Surface Normals', fontsize=14, fontweight='bold', color='#1F414D')
        axes[2].axis('off')

    plt.tight_layout()
    out_path = os.path.join(output_dir, f'{name}_metric3d_results.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: {out_path}")
    print(f"  Depth range: {depth.min():.2f} - {depth.max():.2f} m")

    return depth, normal_vis


def main():
    parser = argparse.ArgumentParser(description='Metric3D v2 Inference Demo')
    parser.add_argument('--images', nargs='+', required=True,
                        help='Image paths or directory')
    parser.add_argument('--output', default='../figures',
                        help='Output directory')
    parser.add_argument('--model', default='metric3d_vit_large',
                        choices=['metric3d_vit_small', 'metric3d_vit_large', 'metric3d_vit_giant2'],
                        help='Model variant')
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    # Collect image paths
    image_paths = []
    for p in args.images:
        if os.path.isdir(p):
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
                image_paths.extend(glob.glob(os.path.join(p, ext)))
        else:
            image_paths.append(p)

    print(f"Found {len(image_paths)} images")
    print(f"Loading model: {args.model}")
    model = load_model(args.model)

    for img_path in sorted(image_paths):
        run_inference(model, img_path, args.output)

    print("\nDone! All results saved to:", args.output)


if __name__ == '__main__':
    main()
