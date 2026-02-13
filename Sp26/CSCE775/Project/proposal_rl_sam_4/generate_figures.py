"""
Generate real SAM + DINOv2 figures for the PPO explainer using a real
underwater coral reef photograph (Wikimedia Commons, CC license).

Image: "Colorful underwater landscape of a coral reef"
  - Two small fish visible among colorful coral formations

Produces:
  figures/fig1_prompt_sensitivity.png  - Good vs bad prompt placement on real photo
  figures/fig2_dino_features.png       - DINOv2 patch feature visualization
  figures/fig3_sam_iterative.png       - Iterative prompt refinement (simulated RL)
  figures/fig4_multi_object.png        - Segmenting different objects (fish vs coral)
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


def load_real_image():
    """Load the real coral reef image and resize to workable dimensions."""
    path = os.path.join(FIGDIR, "real_reef2.jpg")
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not find {path}")
    # Resize to 1024 wide (SAM's preferred input size) keeping aspect ratio
    h, w = img.shape[:2]
    new_w = 1024
    new_h = int(h * new_w / w)
    img = cv2.resize(img, (new_w, new_h))
    return img


def load_sam():
    from segment_anything import sam_model_registry, SamPredictor
    ckpt = os.path.join(os.path.dirname(__file__), "sam_vit_b.pth")
    sam = sam_model_registry["vit_b"](checkpoint=ckpt)
    sam.to(DEVICE)
    return SamPredictor(sam)


def plot_points(ax, pos_points, neg_points, radius=10):
    """Draw prompt points on an axis."""
    for pt in pos_points:
        ax.add_patch(Circle(pt, radius, color=HORSESHOE, zorder=5, linewidth=0))
        ax.annotate("+", pt, color="white", fontsize=9, ha="center", va="center",
                    fontweight="bold", zorder=6)
    for pt in neg_points:
        ax.add_patch(Circle(pt, radius, color=ROSE, zorder=5, linewidth=0))
        ax.annotate("\u2212", pt, color="white", fontsize=9, ha="center", va="center",
                    fontweight="bold", zorder=6)


def overlay_mask(ax, mask, color, alpha=0.45):
    """Overlay a colored mask on the current axis."""
    colored = np.zeros((*mask.shape, 4))
    r, g, b = tuple(int(color.lstrip("#")[i:i+2], 16) / 255 for i in (0, 2, 4))
    colored[mask > 0] = [r, g, b, alpha]
    ax.imshow(colored)


def mask_outline(ax, mask, color=BLACK50, lw=1.5):
    """Draw contour outline of a mask."""
    mask_u8 = (mask > 0).astype(np.uint8) * 255
    contours, _ = cv2.findContours(mask_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        pts = cnt.squeeze()
        if len(pts.shape) == 2 and len(pts) > 2:
            ax.plot(np.append(pts[:, 0], pts[0, 0]),
                    np.append(pts[:, 1], pts[0, 1]),
                    color=color, linewidth=lw, linestyle="--", zorder=4)


# ── FIGURE 1: Prompt Sensitivity ────────────────────────────────────────
def generate_fig1(img_rgb, predictor):
    """Show how different prompt placements produce different SAM masks."""
    h, w = img_rgb.shape[:2]
    predictor.set_image(img_rgb)

    # The two small fish in the image are roughly at:
    # Fish 1 (left): around (480, 390) in the 1024-wide image
    # Fish 2 (right): around (570, 400)
    # Pink coral: bottom-left ~(200, 500)
    # Staghorn coral: center ~(550, 350)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Panel A: Prompts on coral (wrong object for "fish" task)
    pts_a = np.array([[200, 480], [350, 500]])
    lab_a = np.array([1, 1])
    masks_a, scores_a, _ = predictor.predict(
        point_coords=pts_a, point_labels=lab_a, multimask_output=True)
    best_a = masks_a[np.argmax(scores_a)]

    axes[0].imshow(img_rgb)
    overlay_mask(axes[0], best_a, GARNET, 0.45)
    plot_points(axes[0], pts_a, [])
    axes[0].set_title("Prompts on Coral\n(Wrong object segmented)",
                      color=GARNET, fontsize=13, fontweight="bold")
    axes[0].axis("off")

    # Panel B: One prompt near fish but ambiguous
    pts_b = np.array([[500, 400]])
    lab_b = np.array([1])
    masks_b, scores_b, _ = predictor.predict(
        point_coords=pts_b, point_labels=lab_b, multimask_output=True)
    best_b = masks_b[np.argmax(scores_b)]

    axes[1].imshow(img_rgb)
    overlay_mask(axes[1], best_b, HONEYCOMB, 0.45)
    plot_points(axes[1], pts_b, [])
    axes[1].set_title("Single Ambiguous Prompt\n(Uncertain boundary)",
                      color=HONEYCOMB, fontsize=13, fontweight="bold")
    axes[1].axis("off")

    # Panel C: Well-placed prompts on fish + negative on coral
    pts_pos = np.array([[480, 390], [500, 395], [465, 385]])
    pts_neg = np.array([[200, 480], [700, 300]])
    all_pts = np.vstack([pts_pos, pts_neg])
    all_lab = np.array([1, 1, 1, 0, 0])
    masks_c, scores_c, _ = predictor.predict(
        point_coords=all_pts, point_labels=all_lab, multimask_output=True)
    best_c = masks_c[np.argmax(scores_c)]

    axes[2].imshow(img_rgb)
    overlay_mask(axes[2], best_c, HORSESHOE, 0.45)
    plot_points(axes[2], pts_pos, pts_neg)
    axes[2].set_title("Targeted Prompts + Negatives\n(Clean fish segmentation)",
                      color=HORSESHOE, fontsize=13, fontweight="bold")
    axes[2].axis("off")

    fig.suptitle("SAM Prompt Sensitivity on Real Underwater Photo",
                 fontsize=15, fontweight="bold", color=BLACK90, y=1.02)
    plt.tight_layout()
    out = os.path.join(FIGDIR, "fig1_prompt_sensitivity.png")
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved {out}")


# ── FIGURE 2: DINOv2 Feature Visualization ──────────────────────────────
def generate_fig2(img_rgb):
    """Show DINOv2 PCA features and similarity map on real image."""
    from transformers import AutoModel, AutoImageProcessor

    print("  Loading DINOv2...")
    processor = AutoImageProcessor.from_pretrained("facebook/dinov2-small")
    model = AutoModel.from_pretrained("facebook/dinov2-small").to(DEVICE)
    model.eval()

    h_img, w_img = img_rgb.shape[:2]
    pil_img = Image.fromarray(img_rgb)
    inputs = processor(images=pil_img, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        outputs = model(**inputs)
    features = outputs.last_hidden_state[0, 1:, :].cpu().numpy()
    n_patches = features.shape[0]
    h_p = w_p = int(np.sqrt(n_patches))

    # PCA → RGB
    from numpy.linalg import svd
    feat_c = features - features.mean(axis=0)
    U, S, Vt = svd(feat_c, full_matrices=False)
    pca3 = U[:, :3] * S[:3]
    for c in range(3):
        mn, mx = pca3[:, c].min(), pca3[:, c].max()
        if mx - mn > 1e-8:
            pca3[:, c] = (pca3[:, c] - mn) / (mx - mn)
    pca_img = pca3.reshape(h_p, w_p, 3)
    pca_up = cv2.resize(pca_img, (w_img, h_img), interpolation=cv2.INTER_NEAREST)

    # Similarity to a query point on one of the fish (~480, 390 in image coords)
    qx, qy = 480, 390
    patch_row = int(qy / h_img * h_p)
    patch_col = int(qx / w_img * w_p)
    query_idx = min(patch_row * w_p + patch_col, n_patches - 1)
    query_feat = features[query_idx]
    sims = features @ query_feat / (
        np.linalg.norm(features, axis=1) * np.linalg.norm(query_feat) + 1e-8)
    sim_map = sims.reshape(h_p, w_p)
    sim_up = cv2.resize(sim_map, (w_img, h_img), interpolation=cv2.INTER_LINEAR)

    # Similarity to coral query (~200, 480)
    cx, cy = 200, 480
    cpatch_row = int(cy / h_img * h_p)
    cpatch_col = int(cx / w_img * w_p)
    coral_idx = min(cpatch_row * w_p + cpatch_col, n_patches - 1)
    coral_feat = features[coral_idx]
    coral_sims = features @ coral_feat / (
        np.linalg.norm(features, axis=1) * np.linalg.norm(coral_feat) + 1e-8)
    coral_map = coral_sims.reshape(h_p, w_p)
    coral_up = cv2.resize(coral_map, (w_img, h_img), interpolation=cv2.INTER_LINEAR)

    fig, axes = plt.subplots(2, 2, figsize=(16, 11))

    # Top-left: Original
    axes[0, 0].imshow(img_rgb)
    axes[0, 0].add_patch(Circle((qx, qy), 14, color=GARNET, linewidth=2.5,
                                fill=False, zorder=5))
    axes[0, 0].annotate("fish query", (qx, qy), (qx + 40, qy - 50), color=GARNET,
                        fontsize=10, fontweight="bold",
                        arrowprops=dict(arrowstyle="->", color=GARNET, lw=1.5))
    axes[0, 0].add_patch(Circle((cx, cy), 14, color=ATLANTIC, linewidth=2.5,
                                fill=False, zorder=5))
    axes[0, 0].annotate("coral query", (cx, cy), (cx - 30, cy - 60), color=ATLANTIC,
                        fontsize=10, fontweight="bold",
                        arrowprops=dict(arrowstyle="->", color=ATLANTIC, lw=1.5))
    axes[0, 0].set_title("Original Photo", fontsize=13, fontweight="bold", color=BLACK90)
    axes[0, 0].axis("off")

    # Top-right: PCA features
    axes[0, 1].imshow(pca_up)
    axes[0, 1].set_title("DINOv2 Features (PCA \u2192 RGB)", fontsize=13,
                         fontweight="bold", color=ATLANTIC)
    axes[0, 1].axis("off")

    # Bottom-left: Fish similarity
    im1 = axes[1, 0].imshow(sim_up, cmap="RdYlGn", vmin=-0.2, vmax=1.0)
    axes[1, 0].add_patch(Circle((qx, qy), 14, color=GARNET, linewidth=2.5,
                                fill=False, zorder=5))
    axes[1, 0].set_title("Similarity to Fish Query", fontsize=13,
                         fontweight="bold", color=GARNET)
    axes[1, 0].axis("off")
    plt.colorbar(im1, ax=axes[1, 0], fraction=0.046, pad=0.04)

    # Bottom-right: Coral similarity
    im2 = axes[1, 1].imshow(coral_up, cmap="RdYlGn", vmin=-0.2, vmax=1.0)
    axes[1, 1].add_patch(Circle((cx, cy), 14, color=ATLANTIC, linewidth=2.5,
                                fill=False, zorder=5))
    axes[1, 1].set_title("Similarity to Coral Query", fontsize=13,
                         fontweight="bold", color=ATLANTIC)
    axes[1, 1].axis("off")
    plt.colorbar(im2, ax=axes[1, 1], fraction=0.046, pad=0.04)

    fig.suptitle("DINOv2 Feature Extraction on Real Reef Photo\n"
                 "Similar regions light up \u2014 this is how the system finds prompt candidates",
                 fontsize=14, fontweight="bold", color=BLACK90, y=1.01)
    plt.tight_layout()
    out = os.path.join(FIGDIR, "fig2_dino_features.png")
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved {out}")


# ── FIGURE 3: Iterative Refinement ─────────────────────────────────────
def generate_fig3(img_rgb, predictor):
    """Simulate RL iterative prompt refinement on the real image."""
    h, w = img_rgb.shape[:2]

    # Target: segment the fish (around 480, 390)
    # Simulate RL improving prompts over steps
    steps = [
        {
            "title": "Step 0: Random Candidates",
            "pos": np.array([[300, 300], [700, 200], [150, 350], [600, 500], [450, 250]]),
            "neg": np.array([[50, 50], [900, 100]]),
        },
        {
            "title": "Step 30: Removing Bad Points",
            "pos": np.array([[450, 350], [500, 400], [550, 380]]),
            "neg": np.array([[200, 480], [800, 300]]),
        },
        {
            "title": "Step 60: Refining Placement",
            "pos": np.array([[475, 385], [490, 395], [460, 390], [505, 388]]),
            "neg": np.array([[200, 480], [700, 300], [400, 500]]),
        },
        {
            "title": "Step 100: Optimized",
            "pos": np.array([[480, 390], [470, 385], [495, 393], [465, 395], [488, 382]]),
            "neg": np.array([[200, 480], [700, 300], [550, 500], [400, 300]]),
        },
    ]

    colors = [GARNET, HONEYCOMB, ATLANTIC, HORSESHOE]
    fig, axes = plt.subplots(1, 4, figsize=(22, 5.5))

    for step, ax, col in zip(steps, axes, colors):
        predictor.set_image(img_rgb)
        all_pts = np.vstack([step["pos"], step["neg"]])
        all_lab = np.array([1] * len(step["pos"]) + [0] * len(step["neg"]))

        masks, scores, _ = predictor.predict(
            point_coords=all_pts, point_labels=all_lab, multimask_output=True)
        best = masks[np.argmax(scores)]
        mask_area_pct = best.sum() / (h * w) * 100

        ax.imshow(img_rgb)
        overlay_mask(ax, best, col, 0.45)
        mask_outline(ax, best, col, 2.0)
        plot_points(ax, step["pos"], step["neg"], radius=8)
        ax.set_title(f"{step['title']}\nMask area: {mask_area_pct:.1f}%",
                     fontsize=11, fontweight="bold", color=col)
        ax.axis("off")

    fig.suptitle("Simulated RL Prompt Optimization on Real Reef Photo\n"
                 "The agent learns to place \u001b[32m+ prompts on the fish "
                 "and \u2212 prompts on coral",
                 fontsize=13, fontweight="bold", color=BLACK90, y=1.03)
    # Fix: use plain text for suptitle
    fig.texts[0].set_text(
        "Simulated RL Prompt Optimization on Real Reef Photo")
    plt.tight_layout()
    out = os.path.join(FIGDIR, "fig3_sam_iterative.png")
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved {out}")


# ── FIGURE 4: Multi-Object Segmentation ────────────────────────────────
def generate_fig4(img_rgb, predictor):
    """Show SAM segmenting different objects with different prompts."""
    h, w = img_rgb.shape[:2]
    predictor.set_image(img_rgb)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Panel A: Segment pink coral (bottom-left)
    pts_coral = np.array([[180, 480], [250, 520], [130, 500]])
    lab_coral = np.array([1, 1, 1])
    masks_c, scores_c, _ = predictor.predict(
        point_coords=pts_coral, point_labels=lab_coral, multimask_output=True)
    best_coral = masks_c[np.argmax(scores_c)]

    axes[0].imshow(img_rgb)
    overlay_mask(axes[0], best_coral, ROSE, 0.5)
    mask_outline(axes[0], best_coral, ROSE, 2.0)
    plot_points(axes[0], pts_coral, [])
    axes[0].set_title("Prompt \u2192 Pink Coral", fontsize=13,
                      fontweight="bold", color=ROSE)
    axes[0].axis("off")

    # Panel B: Segment branching coral (center)
    pts_branch = np.array([[550, 350], [600, 380], [500, 370]])
    neg_branch = np.array([[200, 480], [480, 390]])
    all_branch = np.vstack([pts_branch, neg_branch])
    lab_branch = np.array([1, 1, 1, 0, 0])
    masks_b, scores_b, _ = predictor.predict(
        point_coords=all_branch, point_labels=lab_branch, multimask_output=True)
    best_branch = masks_b[np.argmax(scores_b)]

    axes[1].imshow(img_rgb)
    overlay_mask(axes[1], best_branch, ATLANTIC, 0.5)
    mask_outline(axes[1], best_branch, ATLANTIC, 2.0)
    plot_points(axes[1], pts_branch, neg_branch)
    axes[1].set_title("Prompt \u2192 Branching Coral", fontsize=13,
                      fontweight="bold", color=ATLANTIC)
    axes[1].axis("off")

    # Panel C: Segment fish
    pts_fish = np.array([[480, 390], [470, 385], [495, 393]])
    neg_fish = np.array([[200, 480], [700, 300], [550, 500]])
    all_fish = np.vstack([pts_fish, neg_fish])
    lab_fish = np.array([1, 1, 1, 0, 0, 0])
    masks_f, scores_f, _ = predictor.predict(
        point_coords=all_fish, point_labels=lab_fish, multimask_output=True)
    best_fish = masks_f[np.argmax(scores_f)]

    axes[2].imshow(img_rgb)
    overlay_mask(axes[2], best_fish, HORSESHOE, 0.5)
    mask_outline(axes[2], best_fish, HORSESHOE, 2.0)
    plot_points(axes[2], pts_fish, neg_fish)
    axes[2].set_title("Prompt \u2192 Fish", fontsize=13,
                      fontweight="bold", color=HORSESHOE)
    axes[2].axis("off")

    fig.suptitle("Same Image, Different Prompts \u2192 Different Objects Segmented\n"
                 "The RL agent must learn which object to target and where to place prompts",
                 fontsize=14, fontweight="bold", color=BLACK90, y=1.03)
    plt.tight_layout()
    out = os.path.join(FIGDIR, "fig4_multi_object.png")
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved {out}")


# ── Main ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.edgecolor"] = BLACK90
    plt.rcParams["axes.linewidth"] = 1.0

    print("Loading real reef image...")
    img_bgr = load_real_image()
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    print(f"  Image size: {img_rgb.shape[1]}x{img_rgb.shape[0]}")

    print("\nLoading SAM ViT-B...")
    predictor = load_sam()

    print("\n=== Figure 1: Prompt Sensitivity ===")
    generate_fig1(img_rgb, predictor)

    print("\n=== Figure 2: DINOv2 Features ===")
    generate_fig2(img_rgb)

    print("\n=== Figure 3: Iterative Refinement ===")
    generate_fig3(img_rgb, predictor)

    print("\n=== Figure 4: Multi-Object Segmentation ===")
    generate_fig4(img_rgb, predictor)

    print("\nAll figures saved to:", FIGDIR)
