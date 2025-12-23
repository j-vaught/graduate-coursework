
import cv2
import numpy as np
import matplotlib.pyplot as plt
import requests
import os

def run_sr_pipeline():
    # 1. Setup Paths and URLs
    work_dir = "/Users/jvaught/Downloads/COde/graduate-coursework/Fall 2025/Conf_Papers/AIAA Papers/Jackie_cue_to_slew/figures"
    os.chdir(work_dir)
    
    gt_path = "fig_ground_truth.png"
    output_path = "fig_sr_comparison.png" 
    
    # Using EDSR x4 (Standard benchmark model)
    model_name = "edsr"
    scale = 4
    model_filename = "EDSR_x4.pb"
    model_url = "https://github.com/Saafke/EDSR_Tensorflow/raw/master/models/EDSR_x4.pb"

    # 2. Download Model if missing
    if not os.path.exists(model_filename):
        print(f"Downloading {model_filename} from {model_url}...")
        try:
            r = requests.get(model_url, allow_redirects=True)
            with open(model_filename, 'wb') as f:
                f.write(r.content)
            print("Download complete.")
        except Exception as e:
            print(f"Failed to download model: {e}")
            return

    # 3. Load Ground Truth Image
    img_gt = cv2.imread(gt_path)
    if img_gt is None:
        print(f"Error: Could not load {gt_path}")
        return
    
    # Convert to RGB for matplotlib
    img_gt = cv2.cvtColor(img_gt, cv2.COLOR_BGR2RGB)
    h, w, c = img_gt.shape
    print(f"Original Image Size: {w}x{h}")


    # 4. Create "Extreme" Low-Res Input (Simulating ~15px target width)
    # The paper mentions 15x15 pixels, so let's aim for that.
    target_lr_width = 15
    
    # Calculate downsample factor
    downsample_factor = w / target_lr_width
    
    lr_w = int(w / downsample_factor)
    lr_h = int(h / downsample_factor)
    
    print(f"Downsampling to tiny size: {lr_w}x{lr_h} for input simulation")
    
    # Generated Low-Res Input
    img_lr = cv2.resize(img_gt, (lr_w, lr_h), interpolation=cv2.INTER_AREA)

    # ADD NOISE (Simulating sensor noise in low-light/long-range)
    # We add noise to the tiny image, so the noise gets 'blown up' in digital zoom
    noise_sigma = 25  # Adjust strength of noise
    gauss = np.random.normal(0, noise_sigma, img_lr.shape).astype('float32')
    img_lr_noisy = img_lr.astype('float32') + gauss
    img_lr = np.clip(img_lr_noisy, 0, 255).astype('uint8')

    # 5. Generate Panel 1: Digital Zoom (Nearest Neighbor from Tiny -> Original)
    img_digital = cv2.resize(img_lr, (w, h), interpolation=cv2.INTER_NEAREST)

    # 6. Generate Panel 2: Super-Resolution
    # Model expects input. It will upscale x4. 
    # Since our img_lr is very small (~30px), output will be ~120px.
    # We then resize that ~120px to FULL size (w,h) to display side-by-side.
    print("Running Super-Resolution...")
    try:
        # Re-convert to BGR for OpenCV DNN
        img_lr_bgr = cv2.cvtColor(img_lr, cv2.COLOR_RGB2BGR)
        
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        sr.readModel(model_filename)
        sr.setModel(model_name, scale)
        img_sr_bgr = sr.upsample(img_lr_bgr) # Output is 4x larger than lr
        
        # Now resize to match GT size for display
        # We use cubic here to simply "display" the SR result at large size without adding more 'pixels' blocks
        img_sr_native = cv2.cvtColor(img_sr_bgr, cv2.COLOR_BGR2RGB)
        img_sr = cv2.resize(img_sr_native, (w, h), interpolation=cv2.INTER_CUBIC)
        
    except Exception as e:
        print(f"SR Failed (likely missing opencv-contrib or model issue): {e}")
        # Fallback to Bicubic if SR fails
        print("Falling back to Bicubic interpolation.")
        img_sr = cv2.resize(img_lr, (w, h), interpolation=cv2.INTER_CUBIC)

    # 7. Create Composite Figure
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Helper to clean axes
    def clean_ax(ax, title, img):
        ax.imshow(img)
        ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
        # Add a black border
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(2)
        ax.set_xticks([])
        ax.set_yticks([])

    # Panel 1: Digital Zoom
    clean_ax(axes[0], "Digital Zoom (Crop)", img_digital)

    # Panel 2: Super-Resolution (with model name)
    clean_ax(axes[1], "Super-Resolution (EDSR)", img_sr)

    # Panel 3: Optical Zoom
    clean_ax(axes[2], "Optical Zoom (Ground Truth)", img_gt)

    plt.tight_layout()
    plt.savefig('fig_sr_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved fig_sr_comparison.png")

if __name__ == "__main__":
    run_sr_pipeline()
