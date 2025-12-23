
import cv2
import numpy as np
import requests
import os

def run_sr_pipeline():
    # 1. Setup Paths and URLs
    work_dir = "/Users/jvaught/Downloads/COde/graduate-coursework/Fall 2025/Conf_Papers/AIAA Papers/Jackie_cue_to_slew/figures"
    os.chdir(work_dir)
    
    gt_path = "fig_ground_truth.png"
    
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
    
    # Keep in BGR for OpenCV processing, convert to RGB only for saving
    h, w, c = img_gt.shape
    print(f"Original Image Size: {w}x{h}")

    # 4. Create "Extreme" Low-Res Input (Simulating ~15px target width)
    target_lr_width = 15
    downsample_factor = w / target_lr_width
    lr_w = int(w / downsample_factor)
    lr_h = int(h / downsample_factor)
    
    print(f"Downsampling to tiny size: {lr_w}x{lr_h} for input simulation")
    
    # Generated Low-Res Input
    img_lr = cv2.resize(img_gt, (lr_w, lr_h), interpolation=cv2.INTER_AREA)

    # ADD NOISE (Reduced from 25 to 12 for subtler effect)
    noise_sigma = 12
    gauss = np.random.normal(0, noise_sigma, img_lr.shape).astype('float32')
    img_lr_noisy = img_lr.astype('float32') + gauss
    img_lr = np.clip(img_lr_noisy, 0, 255).astype('uint8')

    # 5. Generate Panel 1: Digital Zoom (Nearest Neighbor from Tiny -> Original)
    img_digital = cv2.resize(img_lr, (w, h), interpolation=cv2.INTER_NEAREST)

    # 6. Generate Panel 2: Super-Resolution
    print("Running Super-Resolution...")
    try:
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        sr.readModel(model_filename)
        sr.setModel(model_name, scale)
        img_sr_native = sr.upsample(img_lr)  # Output is 4x larger than lr
        
        # Resize to match GT size for display
        img_sr = cv2.resize(img_sr_native, (w, h), interpolation=cv2.INTER_CUBIC)
        
    except Exception as e:
        print(f"SR Failed (likely missing opencv-contrib or model issue): {e}")
        print("Falling back to Bicubic interpolation.")
        img_sr = cv2.resize(img_lr, (w, h), interpolation=cv2.INTER_CUBIC)

    # 7. Create Optical Zoom display copy with light noise (do NOT edit original)
    optical_noise_sigma = 5  # Light noise for realism
    optical_gauss = np.random.normal(0, optical_noise_sigma, img_gt.shape).astype('float32')
    img_optical_display = np.clip(img_gt.astype('float32') + optical_gauss, 0, 255).astype('uint8')

    # 8. Save each panel as a separate PNG (no matplotlib framing)
    cv2.imwrite('panel_digital.png', img_digital)
    print("Saved panel_digital.png")
    
    cv2.imwrite('panel_sr.png', img_sr)
    print("Saved panel_sr.png")
    
    cv2.imwrite('panel_optical.png', img_optical_display)
    print("Saved panel_optical.png")

    print("All panels saved. Use fig_sr_comparison.tex to compose the final figure.")

if __name__ == "__main__":
    run_sr_pipeline()
