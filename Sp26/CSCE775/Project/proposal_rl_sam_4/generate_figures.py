"""
Generate real SAM + DINOv2 figures for the PPO explainer using three real
underwater photographs (Wikimedia Commons, CC license).

Images:
  1. Blue tang (Paracanthurus hepatus) on coral - Public Domain
  2. Clownfish in purple anemone - CC BY-SA 3.0
  3. Butterflyfish on Great Barrier Reef coral - CC BY-SA 4.0

Produces 4 figures per image (12 total):
  figures/{prefix}_fig1_prompt_sensitivity.png
  figures/{prefix}_fig2_dino_features.png
  figures/{prefix}_fig3_sam_iterative.png
  figures/{prefix}_fig4_multi_object.png
"""

import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
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


# ── Image configs with object coordinates ────────────────────────────────
# Each config defines prompt coordinates for the 1024-wide resized version

IMAGE_CONFIGS = {
    "bluetang": {
        "file": "candidate_bluetang.jpg",
        "label": "Blue Tang on Coral",
        # Blue tang centered ~(510, 380) in 1024x814 resized image
        # Coral is the background everywhere
        # See prompt_configs_reference.txt for tested configs
        "fig1": {
            "wrong_obj": {  # prompts on coral -> 87.7% mask
                "pos": [[200, 600], [800, 600], [500, 700]],
                "neg": [[500, 380]],
                "title": "Prompts on Coral\n(Wrong object segmented)",
            },
            "ambiguous": {  # one prompt near fish edge -> 10.8%
                "pos": [[550, 430]],
                "title": "Single Ambiguous Prompt\n(Uncertain boundary)",
            },
            "targeted": {  # tight fish + neg coral -> 4.0%
                "pos": [[508, 380], [500, 390], [520, 375], [495, 395], [515, 385]],
                "neg": [[150, 300], [850, 600], [500, 700], [300, 200]],
                "title": "Targeted Prompts + Negatives\n(Clean fish segmentation)",
            },
        },
        "dino_queries": {
            "fish": {"xy": (510, 380), "label": "fish query"},
            "coral": {"xy": (200, 600), "label": "coral query"},
        },
        "fig3_steps": [
            # Step 0: random far-away points -> 87.3% huge mask
            {"title": "Step 0: Random Candidates",
             "pos": [[100, 100], [900, 700], [50, 600]],
             "neg": []},
            # Step 30: one point near fish edge -> 10.8%
            {"title": "Step 30: Near Fish",
             "pos": [[550, 430]],
             "neg": []},
            # Step 60: cluster on fish body -> 10.9%
            {"title": "Step 60: Fish Cluster",
             "pos": [[505, 375], [515, 390], [495, 385], [520, 400]],
             "neg": [[200, 600], [800, 200], [500, 700]]},
            # Step 100: tight optimized -> 4.0%
            {"title": "Step 100: Optimized",
             "pos": [[508, 380], [500, 390], [520, 375], [495, 395], [515, 385]],
             "neg": [[150, 300], [850, 600], [500, 700], [300, 200]]},
        ],
        "fig4_objects": [
            {"name": "Background Coral", "color": ROSE,
             "pos": [[200, 600], [800, 600], [500, 700]],
             "neg": [[500, 380]]},
            {"name": "Full Fish", "color": ATLANTIC,
             "pos": [[505, 375], [515, 390], [495, 385], [520, 400]],
             "neg": [[200, 600], [800, 200], [500, 700]]},
            {"name": "Tight Fish Only", "color": HORSESHOE,
             "pos": [[508, 380], [500, 390], [520, 375], [495, 395], [515, 385]],
             "neg": [[150, 300], [850, 600], [500, 700], [300, 200]]},
        ],
    },
    "clownfish": {
        "file": "candidate_clownfish.jpg",
        "label": "Clownfish in Anemone",
        # Portrait 1024x1280. Lower fish ~(410,550), Upper ~(590,285), Anemone ~(400,1050)
        # See prompt_configs_reference.txt for tested configs
        "fig1": {
            "wrong_obj": {  # anemone base -> 24.2%
                "pos": [[400, 1050], [500, 1100], [350, 1000]],
                "title": "Prompts on Anemone\n(Wrong object segmented)",
            },
            "ambiguous": {  # tentacles -> 0.9%
                "pos": [[500, 600], [450, 650], [550, 580]],
                "title": "Prompts on Tentacles\n(Uncertain boundary)",
            },
            "targeted": {  # tight lower fish -> 1.0%
                "pos": [[410, 545], [400, 560], [420, 550], [395, 555], [415, 540]],
                "neg": [[500, 650], [400, 1000], [600, 300]],
                "title": "Targeted Prompts + Negatives\n(Clean fish segmentation)",
            },
        },
        "dino_queries": {
            "fish": {"xy": (410, 550), "label": "fish query"},
            "coral": {"xy": (400, 1050), "label": "anemone query"},
        },
        "fig3_steps": [
            # Step 0: random corners -> 80.8%
            {"title": "Step 0: Random Candidates",
             "pos": [[100, 100], [900, 1100], [50, 800]],
             "neg": []},
            # Step 30: anemone base (wrong object) -> 24.2%
            {"title": "Step 30: Wrong Object",
             "pos": [[400, 1050], [500, 1100], [350, 1000]],
             "neg": []},
            # Step 60: one point on lower fish -> 0.2%
            {"title": "Step 60: Found Fish",
             "pos": [[420, 540]],
             "neg": []},
            # Step 100: tight lower fish -> 1.0%
            {"title": "Step 100: Optimized",
             "pos": [[410, 545], [400, 560], [420, 550], [395, 555], [415, 540]],
             "neg": [[500, 650], [400, 1000], [600, 300]]},
        ],
        "fig4_objects": [
            {"name": "Purple Anemone", "color": ROSE,
             "pos": [[400, 1050], [500, 1100], [350, 1000]],
             "neg": []},
            {"name": "Lower Clownfish", "color": ATLANTIC,
             "pos": [[410, 545], [400, 560], [420, 550], [395, 555], [415, 540]],
             "neg": [[500, 650], [400, 1000], [600, 300]]},
            {"name": "Upper Clownfish", "color": HORSESHOE,
             "pos": [[590, 280], [610, 290], [580, 300]],
             "neg": [[400, 560], [500, 700]]},
        ],
    },
    "butterflyfish": {
        "file": "candidate_butterflyfish.jpg",
        "label": "Butterflyfish on Reef",
        # 1024x768. Left fish ~(340,375), Right fish ~(475,410), Pink coral ~(750,480)
        # See prompt_configs_reference.txt for tested configs
        "fig1": {
            "wrong_obj": {  # big coral mass -> 28.3%
                "pos": [[400, 300], [500, 350], [600, 400], [300, 450]],
                "title": "Prompts on Coral Mass\n(Wrong object segmented)",
            },
            "ambiguous": {  # one pt on left fish -> 0.7%
                "pos": [[340, 380]],
                "title": "Single Ambiguous Prompt\n(Uncertain boundary)",
            },
            "targeted": {  # tight left fish -> 1.2%
                "pos": [[340, 375], [355, 385], [330, 370], [345, 390], [335, 380]],
                "neg": [[750, 480], [550, 200], [200, 500], [600, 300]],
                "title": "Targeted Prompts + Negatives\n(Clean fish segmentation)",
            },
        },
        "dino_queries": {
            "fish": {"xy": (340, 375), "label": "fish query"},
            "coral": {"xy": (750, 480), "label": "coral query"},
        },
        "fig3_steps": [
            # Step 0: random far -> 86.6%
            {"title": "Step 0: Random Candidates",
             "pos": [[50, 50], [950, 700], [100, 600], [900, 100]],
             "neg": []},
            # Step 30: big coral mass (wrong) -> 28.3%
            {"title": "Step 30: Wrong Object",
             "pos": [[400, 300], [500, 350], [600, 400], [300, 450]],
             "neg": []},
            # Step 60: one pt left fish -> 0.7%
            {"title": "Step 60: Found Fish",
             "pos": [[340, 380]],
             "neg": []},
            # Step 100: tight left fish -> 1.2%
            {"title": "Step 100: Optimized",
             "pos": [[340, 375], [355, 385], [330, 370], [345, 390], [335, 380]],
             "neg": [[750, 480], [550, 200], [200, 500], [600, 300]]},
        ],
        "fig4_objects": [
            {"name": "Pink Coral", "color": ROSE,
             "pos": [[750, 480], [720, 500], [780, 460]],
             "neg": [[350, 370], [480, 420]]},
            {"name": "Left Butterflyfish", "color": ATLANTIC,
             "pos": [[340, 375], [355, 385], [330, 370], [345, 390], [335, 380]],
             "neg": [[750, 480], [550, 200], [200, 500], [600, 300]]},
            {"name": "Right Butterflyfish", "color": HORSESHOE,
             "pos": [[475, 410], [490, 420], [465, 405]],
             "neg": [[750, 480], [340, 375]]},
        ],
    },
}


def load_image(filename):
    """Load image and resize to 1024 wide, keeping aspect ratio."""
    path = os.path.join(FIGDIR, filename)
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not find {path}")
    h, w = img.shape[:2]
    new_w = 1024
    new_h = int(h * new_w / w)
    img = cv2.resize(img, (new_w, new_h))
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def load_sam():
    from segment_anything import sam_model_registry, SamPredictor
    ckpt = os.path.join(os.path.dirname(__file__), "sam_vit_b.pth")
    sam = sam_model_registry["vit_b"](checkpoint=ckpt)
    sam.to(DEVICE)
    return SamPredictor(sam)


def plot_points(ax, pos_points, neg_points, radius=12):
    for pt in pos_points:
        ax.add_patch(Circle(pt, radius, color="#00FF00", zorder=5, linewidth=2,
                            edgecolor="white"))
        ax.annotate("+", pt, color="white", fontsize=11, ha="center", va="center",
                    fontweight="bold", zorder=6)
    for pt in neg_points:
        ax.add_patch(Circle(pt, radius, color="#FF0000", zorder=5, linewidth=2,
                            edgecolor="white"))
        ax.annotate("\u2212", pt, color="white", fontsize=11, ha="center", va="center",
                    fontweight="bold", zorder=6)


# High-contrast overlay colors (bright, saturated, visible against any background)
MASK_COLORS = {
    "red":     "#FF2020",
    "cyan":    "#00FFFF",
    "yellow":  "#FFFF00",
    "magenta": "#FF00FF",
    "green":   "#00FF80",
    "orange":  "#FF8800",
}


def overlay_mask(ax, mask, color, alpha=0.55):
    colored = np.zeros((*mask.shape, 4))
    r, g, b = tuple(int(color.lstrip("#")[i:i+2], 16) / 255 for i in (0, 2, 4))
    colored[mask > 0] = [r, g, b, alpha]
    ax.imshow(colored)


def mask_outline(ax, mask, color="white", lw=3.0):
    mask_u8 = (mask > 0).astype(np.uint8) * 255
    contours, _ = cv2.findContours(mask_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        pts = cnt.squeeze()
        if len(pts.shape) == 2 and len(pts) > 2:
            # Draw black shadow outline first for contrast
            ax.plot(np.append(pts[:, 0], pts[0, 0]),
                    np.append(pts[:, 1], pts[0, 1]),
                    color="black", linewidth=lw + 2, solid_capstyle="round", zorder=3)
            # Draw colored outline on top
            ax.plot(np.append(pts[:, 0], pts[0, 0]),
                    np.append(pts[:, 1], pts[0, 1]),
                    color=color, linewidth=lw, solid_capstyle="round", zorder=4)


def predict_best(predictor, pos, neg=None):
    """Run SAM prediction and return the best mask."""
    pts = np.array(pos)
    labs = np.ones(len(pos), dtype=int)
    if neg is not None and len(neg) > 0:
        pts = np.vstack([pts, np.array(neg)])
        labs = np.concatenate([labs, np.zeros(len(neg), dtype=int)])
    masks, scores, _ = predictor.predict(
        point_coords=pts, point_labels=labs, multimask_output=True)
    return masks[np.argmax(scores)]


# ── FIGURE 1: Prompt Sensitivity ────────────────────────────────────────
def generate_fig1(img_rgb, predictor, cfg, prefix, label):
    h, w = img_rgb.shape[:2]
    predictor.set_image(img_rgb)
    fig1 = cfg["fig1"]

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    title_bbox = dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="none", alpha=0.85)

    # Panel A: Wrong object
    c = fig1["wrong_obj"]
    mask_a = predict_best(predictor, c["pos"])
    axes[0].imshow(img_rgb)
    overlay_mask(axes[0], mask_a, MASK_COLORS["red"], 0.55)
    mask_outline(axes[0], mask_a, MASK_COLORS["red"])
    plot_points(axes[0], c["pos"], [])
    axes[0].set_title(c["title"], color=GARNET, fontsize=14, fontweight="bold",
                      bbox=title_bbox)
    axes[0].axis("off")

    # Panel B: Ambiguous
    c = fig1["ambiguous"]
    mask_b = predict_best(predictor, c["pos"])
    axes[1].imshow(img_rgb)
    overlay_mask(axes[1], mask_b, MASK_COLORS["yellow"], 0.55)
    mask_outline(axes[1], mask_b, MASK_COLORS["yellow"])
    plot_points(axes[1], c["pos"], [])
    axes[1].set_title(c["title"], color=BLACK90, fontsize=14, fontweight="bold",
                      bbox=title_bbox)
    axes[1].axis("off")

    # Panel C: Targeted
    c = fig1["targeted"]
    mask_c = predict_best(predictor, c["pos"], c.get("neg", []))
    axes[2].imshow(img_rgb)
    overlay_mask(axes[2], mask_c, MASK_COLORS["cyan"], 0.55)
    mask_outline(axes[2], mask_c, MASK_COLORS["cyan"])
    plot_points(axes[2], c["pos"], c.get("neg", []))
    axes[2].set_title(c["title"], color=CONGAREE, fontsize=14, fontweight="bold",
                      bbox=title_bbox)
    axes[2].axis("off")

    fig.suptitle(f"SAM Prompt Sensitivity \u2014 {label}",
                 fontsize=16, fontweight="bold", color=BLACK90, y=1.02)
    plt.tight_layout()
    out = os.path.join(FIGDIR, f"{prefix}_fig1_prompt_sensitivity.png")
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved {out}")


# ── FIGURE 2: DINOv2 Feature Visualization ──────────────────────────────
def generate_fig2(img_rgb, cfg, prefix, label):
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

    queries = cfg["dino_queries"]
    fish_q = queries["fish"]
    coral_q = queries["coral"]

    def compute_sim_map(qx, qy):
        pr = int(qy / h_img * h_p)
        pc = int(qx / w_img * w_p)
        idx = min(pr * w_p + pc, n_patches - 1)
        qf = features[idx]
        sims = features @ qf / (
            np.linalg.norm(features, axis=1) * np.linalg.norm(qf) + 1e-8)
        sm = sims.reshape(h_p, w_p)
        return cv2.resize(sm, (w_img, h_img), interpolation=cv2.INTER_LINEAR)

    fish_sim = compute_sim_map(*fish_q["xy"])
    coral_sim = compute_sim_map(*coral_q["xy"])

    fig, axes = plt.subplots(2, 2, figsize=(16, 11))

    axes[0, 0].imshow(img_rgb)
    fx, fy = fish_q["xy"]
    cx, cy = coral_q["xy"]
    axes[0, 0].add_patch(Circle((fx, fy), 14, color=GARNET, linewidth=2.5,
                                fill=False, zorder=5))
    axes[0, 0].annotate(fish_q["label"], (fx, fy), (fx + 40, fy - 50),
                        color=GARNET, fontsize=10, fontweight="bold",
                        arrowprops=dict(arrowstyle="->", color=GARNET, lw=1.5))
    axes[0, 0].add_patch(Circle((cx, cy), 14, color=ATLANTIC, linewidth=2.5,
                                fill=False, zorder=5))
    axes[0, 0].annotate(coral_q["label"], (cx, cy), (cx - 30, cy - 60),
                        color=ATLANTIC, fontsize=10, fontweight="bold",
                        arrowprops=dict(arrowstyle="->", color=ATLANTIC, lw=1.5))
    axes[0, 0].set_title("Original Photo", fontsize=13, fontweight="bold", color=BLACK90)
    axes[0, 0].axis("off")

    axes[0, 1].imshow(pca_up)
    axes[0, 1].set_title("DINOv2 Features (PCA \u2192 RGB)", fontsize=13,
                         fontweight="bold", color=ATLANTIC)
    axes[0, 1].axis("off")

    im1 = axes[1, 0].imshow(fish_sim, cmap="RdYlGn", vmin=-0.2, vmax=1.0)
    axes[1, 0].add_patch(Circle((fx, fy), 14, color=GARNET, linewidth=2.5,
                                fill=False, zorder=5))
    axes[1, 0].set_title(f"Similarity to {fish_q['label'].title()}", fontsize=13,
                         fontweight="bold", color=GARNET)
    axes[1, 0].axis("off")
    plt.colorbar(im1, ax=axes[1, 0], fraction=0.046, pad=0.04)

    im2 = axes[1, 1].imshow(coral_sim, cmap="RdYlGn", vmin=-0.2, vmax=1.0)
    axes[1, 1].add_patch(Circle((cx, cy), 14, color=ATLANTIC, linewidth=2.5,
                                fill=False, zorder=5))
    axes[1, 1].set_title(f"Similarity to {coral_q['label'].title()}", fontsize=13,
                         fontweight="bold", color=ATLANTIC)
    axes[1, 1].axis("off")
    plt.colorbar(im2, ax=axes[1, 1], fraction=0.046, pad=0.04)

    fig.suptitle(f"DINOv2 Feature Extraction \u2014 {label}\n"
                 "Similar regions light up \u2014 this is how the system finds prompt candidates",
                 fontsize=14, fontweight="bold", color=BLACK90, y=1.01)
    plt.tight_layout()
    out = os.path.join(FIGDIR, f"{prefix}_fig2_dino_features.png")
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved {out}")


# ── FIGURE 3: Iterative Refinement ─────────────────────────────────────
def generate_fig3(img_rgb, predictor, cfg, prefix, label):
    h, w = img_rgb.shape[:2]
    steps = cfg["fig3_steps"]
    mask_cols = [MASK_COLORS["red"], MASK_COLORS["orange"], MASK_COLORS["cyan"], MASK_COLORS["green"]]
    title_cols = [GARNET, BLACK90, CONGAREE, HORSESHOE]
    title_bbox = dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="none", alpha=0.85)

    fig, axes = plt.subplots(1, 4, figsize=(22, 5.5))
    for step, ax, mcol, tcol in zip(steps, axes, mask_cols, title_cols):
        predictor.set_image(img_rgb)
        mask = predict_best(predictor, step["pos"], step["neg"])
        mask_area_pct = mask.sum() / (h * w) * 100

        ax.imshow(img_rgb)
        overlay_mask(ax, mask, mcol, 0.55)
        mask_outline(ax, mask, mcol)
        plot_points(ax, step["pos"], step["neg"], radius=8)
        ax.set_title(f"{step['title']}\nMask area: {mask_area_pct:.1f}%",
                     fontsize=12, fontweight="bold", color=tcol, bbox=title_bbox)
        ax.axis("off")

    fig.suptitle(f"Simulated RL Prompt Optimization \u2014 {label}",
                 fontsize=14, fontweight="bold", color=BLACK90, y=1.03)
    plt.tight_layout()
    out = os.path.join(FIGDIR, f"{prefix}_fig3_sam_iterative.png")
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved {out}")


# ── FIGURE 4: Multi-Object Segmentation ────────────────────────────────
def generate_fig4(img_rgb, predictor, cfg, prefix, label):
    h, w = img_rgb.shape[:2]
    objects = cfg["fig4_objects"]

    fig4_mask_cols = [MASK_COLORS["red"], MASK_COLORS["cyan"], MASK_COLORS["yellow"]]
    fig4_title_cols = [GARNET, CONGAREE, BLACK90]
    title_bbox = dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="none", alpha=0.85)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    for obj, ax, mcol, tcol in zip(objects, axes, fig4_mask_cols, fig4_title_cols):
        predictor.set_image(img_rgb)
        mask = predict_best(predictor, obj["pos"], obj.get("neg", []))

        ax.imshow(img_rgb)
        overlay_mask(ax, mask, mcol, 0.55)
        mask_outline(ax, mask, mcol)
        plot_points(ax, obj["pos"], obj.get("neg", []))
        ax.set_title(f"Prompt \u2192 {obj['name']}", fontsize=14,
                     fontweight="bold", color=tcol, bbox=title_bbox)
        ax.axis("off")

    fig.suptitle(f"Same Image, Different Prompts \u2192 Different Objects \u2014 {label}\n"
                 "The RL agent must learn which object to target and where to place prompts",
                 fontsize=15, fontweight="bold", color=BLACK90, y=1.03)
    plt.tight_layout()
    out = os.path.join(FIGDIR, f"{prefix}_fig4_multi_object.png")
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved {out}")


# ── Main ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.edgecolor"] = BLACK90
    plt.rcParams["axes.linewidth"] = 1.0

    print("Loading SAM ViT-B...")
    predictor = load_sam()

    # Process images in order: blue tang first, then clownfish, then butterflyfish
    order = ["bluetang", "clownfish", "butterflyfish"]

    # Load DINOv2 once (will be loaded inside fig2 on first call, cached after)
    for name in order:
        cfg = IMAGE_CONFIGS[name]
        prefix = name
        label = cfg["label"]

        print(f"\n{'='*60}")
        print(f"  Processing: {label} ({cfg['file']})")
        print(f"{'='*60}")

        img_rgb = load_image(cfg["file"])
        print(f"  Image size: {img_rgb.shape[1]}x{img_rgb.shape[0]}")

        print(f"\n  --- Fig 1: Prompt Sensitivity ---")
        generate_fig1(img_rgb, predictor, cfg, prefix, label)

        print(f"\n  --- Fig 2: DINOv2 Features ---")
        generate_fig2(img_rgb, cfg, prefix, label)

        print(f"\n  --- Fig 3: Iterative Refinement ---")
        generate_fig3(img_rgb, predictor, cfg, prefix, label)

        print(f"\n  --- Fig 4: Multi-Object Segmentation ---")
        generate_fig4(img_rgb, predictor, cfg, prefix, label)

    print(f"\nAll figures saved to: {FIGDIR}")
