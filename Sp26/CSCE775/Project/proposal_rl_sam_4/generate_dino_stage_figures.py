"""
Generate figures for the DINO input/output stage visualization.
Produces: original images, resized versions, patch grid overlays,
GT mask overlay, and DINOv2 feature PCA heatmaps.
"""
import torch
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.decomposition import PCA
import os

# Brand colors
GARNET = "#73000A"
ATLANTIC = "#466A9F"
HORSESHOE = "#65780B"

OUT_DIR = "figures/dino_stage"
os.makedirs(OUT_DIR, exist_ok=True)

IMAGE_SIZE = 560
PATCH_SIZE = 14
GRID_SIZE = IMAGE_SIZE // PATCH_SIZE  # 40

# =============================================
# Load images
# =============================================
ref_img_orig = Image.open(f"{OUT_DIR}/ref_image.jpg")
gt_mask_orig = Image.open(f"{OUT_DIR}/gt_mask.jpg")
target_img_orig = Image.open(f"{OUT_DIR}/target_image.jpg")

print(f"Reference: {ref_img_orig.size}")
print(f"GT Mask:   {gt_mask_orig.size}")
print(f"Target:    {target_img_orig.size}")

# =============================================
# 1. Save original images with size labels
# =============================================
for name, img in [("ref_original", ref_img_orig), ("target_original", target_img_orig), ("gt_mask_original", gt_mask_orig)]:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(img)
    ax.set_title(f"{img.size[0]} x {img.size[1]}", fontsize=16, fontweight="bold")
    ax.axis("off")
    fig.savefig(f"{OUT_DIR}/{name}.png", bbox_inches="tight", dpi=150, pad_inches=0.1)
    plt.close(fig)
    print(f"Saved {name}")

# =============================================
# 2. Resize to 560x560 and save
# =============================================
ref_img_560 = ref_img_orig.resize((IMAGE_SIZE, IMAGE_SIZE))
gt_mask_560 = gt_mask_orig.resize((IMAGE_SIZE, IMAGE_SIZE))
target_img_560 = target_img_orig.resize((IMAGE_SIZE, IMAGE_SIZE))

for name, img in [("ref_resized", ref_img_560), ("target_resized", target_img_560), ("gt_mask_resized", gt_mask_560)]:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(img)
    ax.set_title(f"560 x 560", fontsize=16, fontweight="bold")
    ax.axis("off")
    fig.savefig(f"{OUT_DIR}/{name}.png", bbox_inches="tight", dpi=150, pad_inches=0.1)
    plt.close(fig)
    print(f"Saved {name}")

# =============================================
# 3. Patch grid overlay (40x40 grid on image)
# =============================================
for name, img in [("ref_grid", ref_img_560), ("target_grid", target_img_560)]:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(img)
    # Draw grid
    for i in range(GRID_SIZE + 1):
        ax.axhline(y=i * PATCH_SIZE, color="white", linewidth=0.3, alpha=0.6)
        ax.axvline(x=i * PATCH_SIZE, color="white", linewidth=0.3, alpha=0.6)
    ax.set_title(f"40 x 40 patch grid (14px each)", fontsize=14, fontweight="bold")
    ax.axis("off")
    fig.savefig(f"{OUT_DIR}/{name}.png", bbox_inches="tight", dpi=150, pad_inches=0.1)
    plt.close(fig)
    print(f"Saved {name}")

# =============================================
# 4. GT mask labeling on patch grid
# =============================================
gt_arr = np.array(gt_mask_560.convert("L"))
gt_binary = gt_arr > 128

# For each patch, determine if it's positive (>50% overlap with mask) or negative
patch_labels = np.zeros((GRID_SIZE, GRID_SIZE))
for r in range(GRID_SIZE):
    for c in range(GRID_SIZE):
        patch_region = gt_binary[r*PATCH_SIZE:(r+1)*PATCH_SIZE, c*PATCH_SIZE:(c+1)*PATCH_SIZE]
        patch_labels[r, c] = 1 if patch_region.mean() > 0.5 else 0

n_pos = int(patch_labels.sum())
n_neg = GRID_SIZE * GRID_SIZE - n_pos

fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(ref_img_560)
# Overlay colored patches
for r in range(GRID_SIZE):
    for c in range(GRID_SIZE):
        color = (0, 0.8, 0, 0.3) if patch_labels[r, c] == 1 else (0.8, 0, 0, 0.15)
        rect = mpatches.Rectangle((c*PATCH_SIZE, r*PATCH_SIZE), PATCH_SIZE, PATCH_SIZE,
                                   linewidth=0, facecolor=color)
        ax.add_patch(rect)
ax.set_title(f"GT Patch Labels ({n_pos} pos, {n_neg} neg)", fontsize=14, fontweight="bold")
ax.axis("off")
fig.savefig(f"{OUT_DIR}/ref_gt_patch_labels.png", bbox_inches="tight", dpi=150, pad_inches=0.1)
plt.close(fig)
print(f"Saved ref_gt_patch_labels ({n_pos} pos, {n_neg} neg)")

# =============================================
# 5. Run DINOv2 and extract features
# =============================================
print("\nLoading DINOv2 ViT-G/14...")
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Device: {device}")

# Use dinov2_vitg14 - the same model as in the paper
model = torch.hub.load("facebookresearch/dinov2", "dinov2_vitg14")
model = model.to(device)
model.eval()
print("DINOv2 loaded")

# Preprocess
from torchvision import transforms
transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

ref_tensor = transform(ref_img_orig).unsqueeze(0).to(device)
target_tensor = transform(target_img_orig).unsqueeze(0).to(device)

print("Extracting reference features...")
with torch.no_grad():
    ref_features = model.forward_features(ref_tensor)
    ref_patches = ref_features["x_norm_patchtokens"]  # [1, 1600, 1536]

print("Extracting target features...")
with torch.no_grad():
    target_features = model.forward_features(target_tensor)
    target_patches = target_features["x_norm_patchtokens"]  # [1, 1600, 1536]

ref_feat = ref_patches[0].cpu().numpy()    # [1600, 1536]
target_feat = target_patches[0].cpu().numpy()  # [1600, 1536]

print(f"Reference features: {ref_feat.shape}")
print(f"Target features:    {target_feat.shape}")

# =============================================
# 6. PCA visualization of features (3-component RGB)
# =============================================
print("\nComputing PCA...")
all_features = np.concatenate([ref_feat, target_feat], axis=0)  # [3200, 1536]
pca = PCA(n_components=3)
pca_result = pca.fit_transform(all_features)  # [3200, 3]

# Normalize to 0-1 for RGB display
pca_min = pca_result.min(axis=0)
pca_max = pca_result.max(axis=0)
pca_norm = (pca_result - pca_min) / (pca_max - pca_min + 1e-8)

ref_pca = pca_norm[:1600].reshape(GRID_SIZE, GRID_SIZE, 3)
target_pca = pca_norm[1600:].reshape(GRID_SIZE, GRID_SIZE, 3)

# Upscale for display
from PIL import Image as PILImage

for name, pca_map, orig_img in [("ref_pca_features", ref_pca, ref_img_560),
                                  ("target_pca_features", target_pca, target_img_560)]:
    # Feature map only
    fig, ax = plt.subplots(figsize=(6, 6))
    # Upscale PCA map to 560x560 using nearest neighbor
    pca_upscaled = np.repeat(np.repeat(pca_map, PATCH_SIZE, axis=0), PATCH_SIZE, axis=1)
    ax.imshow(pca_upscaled)
    ax.set_title(f"DINOv2 Features (PCA → RGB)", fontsize=14, fontweight="bold")
    ax.axis("off")
    fig.savefig(f"{OUT_DIR}/{name}.png", bbox_inches="tight", dpi=150, pad_inches=0.1)
    plt.close(fig)

    # Overlay on original image
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(orig_img)
    ax.imshow(pca_upscaled, alpha=0.5)
    ax.set_title(f"Features overlaid on image", fontsize=14, fontweight="bold")
    ax.axis("off")
    fig.savefig(f"{OUT_DIR}/{name}_overlay.png", bbox_inches="tight", dpi=150, pad_inches=0.1)
    plt.close(fig)
    print(f"Saved {name}")

# =============================================
# 7. Feature matrix block visualization
# =============================================
for name, feat in [("ref_feature_matrix", ref_feat), ("target_feature_matrix", target_feat)]:
    fig, ax = plt.subplots(figsize=(8, 4))
    # Show a subset for visibility (first 100 patches, first 200 dims)
    ax.imshow(feat[:100, :200], aspect="auto", cmap="RdBu_r", interpolation="nearest")
    ax.set_xlabel("Feature dimension (showing 200 of 1536)", fontsize=11)
    ax.set_ylabel("Patch index (showing 100 of 1600)", fontsize=11)
    ax.set_title(f"Feature Matrix: 1600 × 1536", fontsize=14, fontweight="bold")
    fig.savefig(f"{OUT_DIR}/{name}.png", bbox_inches="tight", dpi=150, pad_inches=0.1)
    plt.close(fig)
    print(f"Saved {name}")

# =============================================
# 8. Single-component heatmaps (top 3 PCA components)
# =============================================
for img_name, pca_map in [("ref", ref_pca), ("target", target_pca)]:
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for i, (ax, title) in enumerate(zip(axes, ["PC1", "PC2", "PC3"])):
        component = pca_map[:, :, i]
        component_up = np.repeat(np.repeat(component, PATCH_SIZE, axis=0), PATCH_SIZE, axis=1)
        im = ax.imshow(component_up, cmap="inferno")
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.axis("off")
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.suptitle(f"{img_name.capitalize()} — Top 3 PCA Components", fontsize=16, fontweight="bold")
    fig.savefig(f"{OUT_DIR}/{img_name}_pca_components.png", bbox_inches="tight", dpi=150, pad_inches=0.1)
    plt.close(fig)
    print(f"Saved {img_name}_pca_components")

print("\nAll figures generated!")
print(f"Output directory: {OUT_DIR}")
