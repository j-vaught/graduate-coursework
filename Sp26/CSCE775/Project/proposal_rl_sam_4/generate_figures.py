"""
Generate real SAM + DINOv2 figures for the PPO explainer.

Produces:
  figures/fig1_prompt_sensitivity.png  - Good vs bad prompt placement on a real image
  figures/fig2_dino_features.png       - DINOv2 patch feature visualization
  figures/fig3_sam_iterative.png       - Iterative prompt refinement (simulated RL steps)
"""

import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image
import cv2
import os

# Brand colors
GARNET = "#73000A"
ATLANTIC = "#466A9F"
CONGAREE = "#1F414D"
HORSESHOE = "#65780B"
ROSE = "#CC2E40"
HONEYCOMB = "#A49137"
BLACK90 = "#363636"
BLACK70 = "#5C5C5C"
BLACK50 = "#A2A2A2"
BLACK30 = "#C7C7C7"
BLACK10 = "#ECECEC"

FIGDIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGDIR, exist_ok=True)

DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {DEVICE}")

# ── Create a synthetic scene with clear objects ──────────────────────────
def make_scene():
    """Create a 512x512 synthetic underwater scene with distinct objects."""
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    # Water background gradient
    for y in range(512):
        b = int(120 + 80 * (y / 512))
        g = int(80 + 40 * (y / 512))
        img[y, :] = [30, g, b]

    mask_fish = np.zeros((512, 512), dtype=np.uint8)
    mask_coral = np.zeros((512, 512), dtype=np.uint8)

    # Fish body (ellipse)
    cv2.ellipse(img, (280, 200), (100, 50), -10, 0, 360, (60, 160, 200), -1)
    cv2.ellipse(mask_fish, (280, 200), (100, 50), -10, 0, 360, 255, -1)
    # Fish tail
    pts_tail = np.array([[175, 190], [140, 155], (140, 225)], np.int32)
    cv2.fillPoly(img, [pts_tail], (50, 140, 180))
    cv2.fillPoly(mask_fish, [pts_tail], 255)
    # Fish eye
    cv2.circle(img, (330, 185), 8, (220, 220, 220), -1)
    cv2.circle(img, (332, 183), 3, (20, 20, 20), -1)
    # Fish fin
    pts_fin = np.array([[260, 170], (280, 130), (310, 165)], np.int32)
    cv2.fillPoly(img, [pts_fin], (45, 130, 170))
    cv2.fillPoly(mask_fish, [pts_fin], 255)

    # Coral cluster (irregular blob)
    pts_coral = np.array([
        [80, 420], [60, 380], [90, 350], [130, 360],
        [160, 390], [170, 430], [150, 460], [100, 470], [70, 450]
    ], np.int32)
    cv2.fillPoly(img, [pts_coral], (180, 100, 80))
    cv2.fillPoly(mask_coral, [pts_coral], 255)
    # Coral branches
    cv2.ellipse(img, (100, 355), (25, 15), -30, 0, 360, (200, 110, 70), -1)
    cv2.ellipse(mask_coral, (100, 355), (25, 15), -30, 0, 360, 255, -1)
    cv2.ellipse(img, (140, 365), (20, 12), 20, 0, 360, (190, 95, 65), -1)
    cv2.ellipse(mask_coral, (140, 365), (20, 12), 20, 0, 360, 255, -1)

    # Starfish
    mask_star = np.zeros((512, 512), dtype=np.uint8)
    cx, cy = 420, 380
    for angle in range(0, 360, 72):
        rad = np.radians(angle)
        ex, ey = int(cx + 35 * np.cos(rad)), int(cy + 35 * np.sin(rad))
        cv2.line(img, (cx, cy), (ex, ey), (200, 160, 50), 12)
        cv2.line(mask_star, (cx, cy), (ex, ey), 255, 12)
    cv2.circle(img, (cx, cy), 14, (210, 170, 60), -1)
    cv2.circle(mask_star, (cx, cy), 14, 255, -1)

    # Some seaweed strands
    for sx in [350, 370, 450, 470]:
        for dy in range(0, 80, 2):
            y = 512 - dy
            x = sx + int(8 * np.sin(dy * 0.15))
            cv2.circle(img, (x, y), 3, (40, 130 + dy // 2, 50), -1)

    # Sandy bottom
    for _ in range(300):
        rx, ry = np.random.randint(0, 512), np.random.randint(460, 512)
        cv2.circle(img, (rx, ry), np.random.randint(1, 4),
                   (160 + np.random.randint(-20, 20),
                    140 + np.random.randint(-20, 20),
                    100 + np.random.randint(-20, 20)), -1)

    return img, mask_fish, mask_coral, mask_star


def compute_iou(pred_mask, gt_mask):
    intersection = np.logical_and(pred_mask > 0, gt_mask > 0).sum()
    union = np.logical_or(pred_mask > 0, gt_mask > 0).sum()
    return intersection / union if union > 0 else 0.0


# ── FIGURE 1: Prompt Sensitivity with real SAM ──────────────────────────
def generate_fig1_prompt_sensitivity(img, mask_fish):
    from segment_anything import sam_model_registry, SamPredictor

    ckpt = os.path.join(os.path.dirname(__file__), "sam_vit_b.pth")
    sam = sam_model_registry["vit_b"](checkpoint=ckpt)
    sam.to(DEVICE)
    predictor = SamPredictor(sam)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    predictor.set_image(img_rgb)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Panel A: Bad prompts (on coral, ambiguous location)
    bad_points = np.array([[100, 400], [150, 380]])  # on the coral
    bad_labels = np.array([1, 1])
    masks_bad, scores_bad, _ = predictor.predict(
        point_coords=bad_points, point_labels=bad_labels, multimask_output=True
    )
    best_bad = masks_bad[np.argmax(scores_bad)]
    iou_bad = compute_iou(best_bad, mask_fish)

    axes[0].imshow(img_rgb)
    axes[0].imshow(best_bad, alpha=0.4, cmap=LinearSegmentedColormap.from_list(
        "garnet", ["white", GARNET], N=2))
    for pt in bad_points:
        axes[0].add_patch(Circle(pt, 8, color=GARNET, zorder=5))
        axes[0].annotate("+", pt, color="white", fontsize=8, ha="center", va="center",
                         fontweight="bold", zorder=6)
    axes[0].set_title(f"Bad Prompts (on coral)\nFish IoU = {iou_bad:.2f}", color=GARNET,
                      fontsize=12, fontweight="bold")
    axes[0].axis("off")

    # Panel B: Mediocre prompts (edge of fish)
    med_points = np.array([[190, 200], [350, 210]])
    med_labels = np.array([1, 1])
    masks_med, scores_med, _ = predictor.predict(
        point_coords=med_points, point_labels=med_labels, multimask_output=True
    )
    best_med = masks_med[np.argmax(scores_med)]
    iou_med = compute_iou(best_med, mask_fish)

    axes[1].imshow(img_rgb)
    axes[1].imshow(best_med, alpha=0.4, cmap=LinearSegmentedColormap.from_list(
        "honey", ["white", HONEYCOMB], N=2))
    for pt in med_points:
        axes[1].add_patch(Circle(pt, 8, color=HONEYCOMB, zorder=5))
        axes[1].annotate("+", pt, color="white", fontsize=8, ha="center", va="center",
                         fontweight="bold", zorder=6)
    axes[1].set_title(f"Edge Prompts\nFish IoU = {iou_med:.2f}", color=HONEYCOMB,
                      fontsize=12, fontweight="bold")
    axes[1].axis("off")

    # Panel C: Good prompts (center of fish + negative on coral)
    good_pos = np.array([[280, 200], [250, 190], [310, 195]])
    good_neg = np.array([[110, 410]])
    all_points = np.vstack([good_pos, good_neg])
    all_labels = np.array([1, 1, 1, 0])
    masks_good, scores_good, _ = predictor.predict(
        point_coords=all_points, point_labels=all_labels, multimask_output=True
    )
    best_good = masks_good[np.argmax(scores_good)]
    iou_good = compute_iou(best_good, mask_fish)

    axes[2].imshow(img_rgb)
    axes[2].imshow(best_good, alpha=0.4, cmap=LinearSegmentedColormap.from_list(
        "horse", ["white", HORSESHOE], N=2))
    for pt in good_pos:
        axes[2].add_patch(Circle(pt, 8, color=HORSESHOE, zorder=5))
        axes[2].annotate("+", pt, color="white", fontsize=8, ha="center", va="center",
                         fontweight="bold", zorder=6)
    for pt in good_neg:
        axes[2].add_patch(Circle(pt, 8, color=ROSE, zorder=5))
        axes[2].annotate("−", pt, color="white", fontsize=8, ha="center", va="center",
                         fontweight="bold", zorder=6)
    axes[2].set_title(f"Good Prompts (centered + negative)\nFish IoU = {iou_good:.2f}",
                      color=HORSESHOE, fontsize=12, fontweight="bold")
    axes[2].axis("off")

    fig.suptitle("SAM Prompt Sensitivity: Where You Click Matters",
                 fontsize=14, fontweight="bold", color=BLACK90, y=1.02)
    plt.tight_layout()
    out = os.path.join(FIGDIR, "fig1_prompt_sensitivity.png")
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {out}")
    return predictor


# ── FIGURE 2: DINOv2 Feature Visualization ──────────────────────────────
def generate_fig2_dino_features(img):
    from transformers import AutoModel, AutoImageProcessor

    print("Loading DINOv2...")
    processor = AutoImageProcessor.from_pretrained("facebook/dinov2-small")
    model = AutoModel.from_pretrained("facebook/dinov2-small").to(DEVICE)
    model.eval()

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    inputs = processor(images=pil_img, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        outputs = model(**inputs)
    # last_hidden_state: (1, num_patches+1, dim) -- skip CLS token
    features = outputs.last_hidden_state[0, 1:, :].cpu().numpy()  # (N, D)
    h = w = int(np.sqrt(features.shape[0]))

    # PCA to 3 components for RGB visualization
    from numpy.linalg import svd
    feat_centered = features - features.mean(axis=0)
    U, S, Vt = svd(feat_centered, full_matrices=False)
    pca3 = U[:, :3] * S[:3]
    # Normalize each channel to [0, 1]
    for c in range(3):
        mn, mx = pca3[:, c].min(), pca3[:, c].max()
        if mx - mn > 1e-8:
            pca3[:, c] = (pca3[:, c] - mn) / (mx - mn)

    pca_img = pca3.reshape(h, w, 3)
    pca_img_up = cv2.resize(pca_img, (512, 512), interpolation=cv2.INTER_NEAREST)

    # Also compute feature similarity to a point on the fish (center)
    fish_patch_idx = (200 // (512 // h)) * w + (280 // (512 // w))
    fish_patch_idx = min(fish_patch_idx, features.shape[0] - 1)
    fish_feat = features[fish_patch_idx]
    similarities = features @ fish_feat / (
        np.linalg.norm(features, axis=1) * np.linalg.norm(fish_feat) + 1e-8
    )
    sim_map = similarities.reshape(h, w)
    sim_map_up = cv2.resize(sim_map, (512, 512), interpolation=cv2.INTER_LINEAR)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    axes[0].imshow(img_rgb)
    axes[0].set_title("Original Scene", fontsize=12, fontweight="bold", color=BLACK90)
    axes[0].add_patch(Circle((280, 200), 12, color=GARNET, linewidth=2, fill=False, zorder=5))
    axes[0].annotate("query", (280, 200), (280, 150), color=GARNET, fontsize=9,
                     fontweight="bold", ha="center",
                     arrowprops=dict(arrowstyle="->", color=GARNET))
    axes[0].axis("off")

    axes[1].imshow(pca_img_up)
    axes[1].set_title("DINOv2 Features (PCA → RGB)", fontsize=12,
                      fontweight="bold", color=ATLANTIC)
    axes[1].axis("off")

    im = axes[2].imshow(sim_map_up, cmap="RdYlGn", vmin=0, vmax=1)
    axes[2].set_title("Cosine Similarity to Fish Center", fontsize=12,
                      fontweight="bold", color=HORSESHOE)
    axes[2].add_patch(Circle((280, 200), 12, color=GARNET, linewidth=2, fill=False, zorder=5))
    axes[2].axis("off")
    plt.colorbar(im, ax=axes[2], fraction=0.046, pad=0.04)

    fig.suptitle("DINOv2 Feature Extraction: How the System 'Sees' the Image",
                 fontsize=14, fontweight="bold", color=BLACK90, y=1.02)
    plt.tight_layout()
    out = os.path.join(FIGDIR, "fig2_dino_features.png")
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {out}")


# ── FIGURE 3: Iterative SAM refinement (simulated RL) ──────────────────
def generate_fig3_iterative_refinement(img, mask_fish, predictor):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Simulate RL steps: start with bad prompts, progressively improve
    steps = [
        {
            "label": "Step 0: Random Candidates",
            "pos": np.array([[200, 300], [400, 100], [100, 200], [350, 350], [250, 250]]),
            "neg": np.array([[50, 50], [480, 480]]),
        },
        {
            "label": "Step 30: RL Removing Bad Points",
            "pos": np.array([[250, 200], [300, 190], [200, 210]]),
            "neg": np.array([[100, 400], [420, 380]]),
        },
        {
            "label": "Step 60: RL Adding Strategic Points",
            "pos": np.array([[260, 195], [290, 200], [240, 185], [310, 205], [220, 200]]),
            "neg": np.array([[100, 410], [420, 380], [400, 100]]),
        },
        {
            "label": "Step 100: Optimized Prompts",
            "pos": np.array([[280, 200], [250, 190], [310, 195], [230, 205], [300, 180]]),
            "neg": np.array([[110, 410], [420, 380], [250, 350]]),
        },
    ]

    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    colors_step = [GARNET, HONEYCOMB, ATLANTIC, HORSESHOE]

    for i, (step, ax, col) in enumerate(zip(steps, axes, colors_step)):
        predictor.set_image(img_rgb)
        all_pts = np.vstack([step["pos"], step["neg"]])
        all_labels = np.array([1] * len(step["pos"]) + [0] * len(step["neg"]))

        masks, scores, _ = predictor.predict(
            point_coords=all_pts, point_labels=all_labels, multimask_output=True
        )
        best = masks[np.argmax(scores)]
        iou = compute_iou(best, mask_fish)

        ax.imshow(img_rgb)

        # Show mask overlay
        cmap = LinearSegmentedColormap.from_list("c", ["white", col], N=2)
        ax.imshow(best, alpha=0.35, cmap=cmap)

        # Show GT outline
        contours, _ = cv2.findContours(mask_fish, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            pts = cnt.squeeze()
            if len(pts.shape) == 2:
                ax.plot(pts[:, 0], pts[:, 1], color=BLACK50, linewidth=1, linestyle="--")

        # Plot points
        for pt in step["pos"]:
            ax.add_patch(Circle(pt, 7, color=HORSESHOE, zorder=5))
            ax.annotate("+", pt, color="white", fontsize=7, ha="center", va="center",
                        fontweight="bold", zorder=6)
        for pt in step["neg"]:
            ax.add_patch(Circle(pt, 7, color=ROSE, zorder=5))
            ax.annotate("−", pt, color="white", fontsize=7, ha="center", va="center",
                        fontweight="bold", zorder=6)

        ax.set_title(f"{step['label']}\nFish IoU = {iou:.2f}",
                     fontsize=11, fontweight="bold", color=col)
        ax.axis("off")

    fig.suptitle("Simulated RL Prompt Optimization: Iterative Refinement with SAM",
                 fontsize=14, fontweight="bold", color=BLACK90, y=1.02)
    plt.tight_layout()
    out = os.path.join(FIGDIR, "fig3_sam_iterative.png")
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {out}")


# ── Main ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.edgecolor"] = BLACK90
    plt.rcParams["axes.linewidth"] = 1.0

    print("Creating synthetic scene...")
    img, mask_fish, mask_coral, mask_star = make_scene()

    # Save the scene for reference
    scene_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    Image.fromarray(scene_rgb).save(os.path.join(FIGDIR, "scene.png"))

    print("\n=== Figure 1: Prompt Sensitivity ===")
    predictor = generate_fig1_prompt_sensitivity(img, mask_fish)

    print("\n=== Figure 2: DINOv2 Features ===")
    generate_fig2_dino_features(img)

    print("\n=== Figure 3: Iterative Refinement ===")
    generate_fig3_iterative_refinement(img, mask_fish, predictor)

    print("\nAll figures saved to:", FIGDIR)
