"""Regenerate DINO stage images without titles or borders.

The original PNGs from generate_dino_stage_figures.py have matplotlib titles
baked in. This script crops out the title region and re-saves clean versions.
For the overlay, it composites the cropped PCA onto the resized reference image.
"""
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = "figures/dino_stage"

# =============================================
# 1. Original and resized reference images (from raw JPGs - no titles)
# =============================================
ref_img = Image.open(f"{OUT_DIR}/ref_image.jpg")
ref_560 = ref_img.resize((560, 560))

for name, img in [
    ("ref_original_clean", ref_img),
    ("ref_resized_clean", ref_560),
]:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(img)
    ax.axis("off")
    fig.savefig(f"{OUT_DIR}/{name}.png", bbox_inches="tight", dpi=150, pad_inches=0)
    plt.close(fig)
    print(f"Saved {name}")

# =============================================
# 2. PCA features - crop title from existing PNGs
# =============================================
def crop_title(img_path):
    """Load a PNG and crop off the white title band at the top."""
    img = Image.open(img_path)
    arr = np.array(img)
    row_means = arr[:, :, :3].mean(axis=(1, 2))
    # Find the last predominantly white row (mean > 250) before stable
    # image content. Scan from top, find last white row in first 20% of image.
    search_limit = len(row_means) // 5
    last_white = 0
    for i in range(search_limit):
        if row_means[i] > 250:
            last_white = i
    # Crop from just after the last white row
    crop_start = last_white + 1
    print(f"  Cropping {img_path}: removing top {crop_start} rows")
    cropped = arr[crop_start:]
    return Image.fromarray(cropped)

ref_pca_clean = crop_title(f"{OUT_DIR}/ref_pca_features.png")
fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(ref_pca_clean)
ax.axis("off")
fig.savefig(f"{OUT_DIR}/ref_pca_features_clean.png", bbox_inches="tight", dpi=150, pad_inches=0)
plt.close(fig)
print("Saved ref_pca_features_clean")

# =============================================
# 3. Overlay - composite cropped PCA onto resized image
# =============================================
pca_arr = np.array(ref_pca_clean.resize((560, 560))) / 255.0
ref_arr = np.array(ref_560) / 255.0
overlay = 0.5 * ref_arr + 0.5 * pca_arr[:, :, :3]
overlay = np.clip(overlay, 0, 1)

fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(overlay)
ax.axis("off")
fig.savefig(f"{OUT_DIR}/ref_pca_features_overlay_clean.png", bbox_inches="tight", dpi=150, pad_inches=0)
plt.close(fig)
print("Saved ref_pca_features_overlay_clean")

# =============================================
# 4. Prompts image
# =============================================
prompts = plt.imread("figures/ppo_step1_initial_prompts.png")
fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(prompts)
ax.axis("off")
fig.savefig(f"{OUT_DIR}/prompts_clean.png", bbox_inches="tight", dpi=150, pad_inches=0)
plt.close(fig)
print("Saved prompts_clean")
