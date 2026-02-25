# CSCE 763 - Paper Reading Presentation

## Assignment Details
- **Email deadline:** 11:59pm, Feb. 22 (tongy@cse.sc.edu) -- **PAST DUE, submit ASAP**
- **Presentation days:** Tuesday Mar 17, Thursday Mar 19, Tuesday Mar 24
- **Requirements:** Paper from official journal or conference (journal preferred)
- **Suggested venues:** IEEE TPAMI, IEEE TIP, CVPR, ICCV, ECCV, IEEE Trans. Medical Imaging

---

## Paper Options

### 1. Generative Image Dynamics
- **Authors:** Zhengqi Li, Richard Tucker, Noah Snavely, Aleksander Holynski
- **Venue:** CVPR 2024 (Best Paper Award), pp. 22884-22893
- **Summary:** Models natural oscillatory dynamics (trees swaying, candles flickering) from a single still image using a frequency-coordinated diffusion sampling process. Generates seamlessly looping videos or interactive simulations from one photograph.
- **Pros:** Best Paper award, visually compelling, bridges spectral analysis and diffusion models.

### 2. Mip-Splatting: Alias-free 3D Gaussian Splatting
- **Authors:** Zehao Yu, Anpei Chen, Binbin Huang, Torsten Sattler, Andreas Geiger
- **Venue:** CVPR 2024 (Best Student Paper Award), pp. 19447-19456
- **Summary:** Fixes aliasing artifacts in 3D Gaussian Splatting with a 3D smoothing filter and 2D Mip filter. Produces alias-free novel view synthesis across varying resolutions.
- **Pros:** Hot topic (3DGS), connects to classical signal processing (Nyquist, anti-aliasing), clean contribution.

### 3. Transformer-Based Visual Segmentation: A Survey
- **Authors:** Xiangtai Li, Henghui Ding, Haobo Yuan, et al.
- **Venue:** IEEE TPAMI, Vol. 46, No. 12, 2024, pp. 10138-10163
- **Summary:** Comprehensive survey of transformer-based segmentation (semantic, instance, panoptic, video, interactive). Unified taxonomy of architectures, training strategies, and benchmarks.
- **Pros:** TPAMI journal paper, surveys are presentation-friendly, segmentation is core CV.

### 4. Metric3D v2: Monocular Geometric Foundation Model for Zero-Shot Metric Depth and Surface Normal Estimation
- **Authors:** Mu Hu, Wei Yin, Chi Zhang, et al.
- **Venue:** IEEE TPAMI, Vol. 46, No. 12, 2024, pp. 10579-10596
- **Summary:** Foundation model for zero-shot metric depth and surface normal estimation from a single image. Solves the focal length ambiguity via canonical camera space transformation.
- **Pros:** TPAMI journal, fundamental problem (depth from single image), connects to 3D vision and robotics.

### 5. Minimalist Vision with Freeform Pixels
- **Authors:** Jeremy Klotz, Shree K. Nayar
- **Venue:** ECCV 2024 (Best Paper Award), LNCS Vol. 15079, pp. 325-342
- **Summary:** Co-designs freeform (arbitrarily shaped) camera pixels and inference jointly end-to-end. Demonstrates 8-pixel cameras that monitor spaces, measure lighting, and estimate traffic flow.
- **Pros:** ECCV Best Paper, provocative idea, great for audience engagement, bridges hardware and CV.

### 6. Diffusion Models in Low-Level Vision: A Survey
- **Authors:** Chunming He, Yuqi Shen, Chengyu Fang, et al.
- **Venue:** IEEE TPAMI, Vol. 47, No. 6, 2025, pp. 4630-4651
- **Summary:** Covers diffusion model approaches for super-resolution, denoising, deblurring, inpainting, colorization, and restoration. Categorizes methods by degradation/generation strategies.
- **Pros:** Most recent (2025 TPAMI), directly relevant to image processing, survey format is presentation-friendly.

### 7. A Survey on Open-Vocabulary Detection and Segmentation: Past, Present, and Future
- **Authors:** Chaoyang Zhu, Long Chen
- **Venue:** IEEE TPAMI, Vol. 46, No. 12, 2024, pp. 8954-8975
- **Summary:** Covers open-vocabulary detection and segmentation where models recognize categories unseen during training. Traces evolution from closed-set detection to CLIP-powered methods.
- **Pros:** TPAMI journal, frontier topic, connects classical detection with modern vision-language models.

---

## Recommendations

| If the course emphasizes... | Best picks |
|-----------------------------|-----------|
| Image processing fundamentals | #5 (Minimalist Vision) or #6 (Diffusion Low-Level) |
| Computer vision / recognition | #3 or #7 (surveys) |
| Maximum audience engagement | #1 (Generative Dynamics) or #5 (Minimalist Vision) |
| Safe choice (TPAMI journal) | #3, #4, #6, or #7 |
