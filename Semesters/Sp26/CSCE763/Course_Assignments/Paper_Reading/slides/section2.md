# Section 2: Methodology (8 slides, ~8 min, 30 pts)

## Slide 1 — Camera Anatomy
- **Animation:** Exploded camera diagram — body, lens assembly, shutter, CMOS sensor, PCB
- Parts strip away one by one until only the essentials remain: lens, CMOS sensor, focal distance $f$
- Goal: reduce the camera to the components that matter for depth estimation
- **Time:** 0:45

## Slide 2 — Focal Length and Depth
- **Animation:** Start from simplified lens+sensor diagram from Slide 1
- Add an object and background in a 2D scene
- Lens slides closer/farther from sensor — rays change angle, projection on CMOS changes size
- Same scene, two focal lengths = two different projected sizes on the sensor
- Takeaway: without knowing $f$, metric depth is unrecoverable from a single image
- **Time:** 1:15

## Slide 3 — Metric3D v1 Pipeline
- **Animation (manim):** v1 pipeline appears block by block with annotations
- Pipeline: Input $I$ → CSTM → ConvNeXt encoder-decoder → Depth head → De-CSTM → Metric depth $D$
- Labels explain each block as they appear
- Highlight: CSTM is the key v1 contribution; everything else is a standard depth network
- Note: depth only, no surface normals, single forward pass (no iteration)
- **Time:** 1:00

## Slide 4 — v1 to v2 Transition
- **Animation (manim, continued from Slide 3):** Annotations fade, leaving bare v1 blocks
- Blocks rearrange and morph into v2 layout:
  - Backbone swaps from ConvNeXt to ViT
  - ConvGRU iterative refinement module inserts after decoder
  - Normal head splits off as second output branch
  - Consistency loss arrow ($L_{d-n}$) appears between depth and normal branches
- Once v2 layout settles, new annotations drop in
- Three additions highlighted: (1) ViT backbone, (2) joint ConvGRU refinement, (3) normal prediction with consistency loss
- **Time:** 1:15

## Slide 5 — Canonical Camera Transform
- **Live code outputs** from Metric3D inference, capturing intermediates at each CSTM stage
- Show for one photo:
  1. Original image + EXIF focal length readout
  2. Resized canonical image after CSTM ($\omega = f^c / f$)
  3. Canonical depth prediction $D_c$ (network output)
  4. De-canonicalized metric depth $D = D_c \cdot f / f^c$
- Then demonstrate the problem CSTM solves:
  - Same scene from two cameras (or simulated by crop/resize to mimic different $f$)
  - Without CSTM: depth predictions are inconsistent (different scale)
  - With CSTM: predictions agree
- Note on slide: "Requires known $f$" — limitation acknowledged
- **Time:** 1:00

## Slide 6 — Iterative Depth-Normal Refinement
- ConvGRU recurrent block operates at 1/4 resolution for efficiency
- Shared hidden state $H^t$ feeds two separate projection heads: $G_d$ (depth) and $G_n$ (normals)
- Each iteration $t$: $D^{t+1} = D^t + \Delta D$, $N^{t+1} = N^t + \Delta N$
- After $T$ steps (typically 3-4), upsample to full resolution. ReLU for depth, L2-normalize for normals
- Key novelty: first method to jointly iterate depth AND normals through a shared hidden state (prior work like RAFT iterated one task only)
- Depth-normal consistency loss $L_{d-n}$: computes pseudo-normals from depth gradients via least-squares, penalizes disagreement with predicted normals. Requires no labels — pure self-supervision. Bridges the gap of only ~20K outdoor normal annotations vs millions of depth labels.
- **Time:** 1:00

## Slide 7 — Random Proposal Normalization
- **Animation (4 frames):**
  - **Frame 1:** 2D side-view scene with depth profile — person at 2m, car at 15m, building at 50m. Show the depth value range.
  - **Frame 2:** Global normalization applied — mean/std computed over full depth range. Near-object detail crushed, loss gradients vanish on close objects. Flash the parallel: global histogram equalization on a high-dynamic-range image.
  - **Frame 3:** Random colored patch rectangles drop onto the depth map. Each patch gets its own local mean/std — all at similar scale now. Flash the parallel: CLAHE tiles on the same image.
  - **Frame 4:** Normalized patches shown side by side — local depth structure fully visible everywhere. Uniform loss gradients across all ranges. "Local contrast preserved."
- Course connection: same principle as adaptive histogram equalization from Ch. 3, applied in loss space instead of image space
- Present in both v1 and v2 (not a v2 novelty)
- **Time:** 1:00

## Slide 8 — Training at Scale
- v1: 8M images, 11 datasets, 10K+ camera models
- v2: 16M images, 16 datasets (added Waymo, MakerPortal3D, Virtual KITTI, etc.)
- CSTM is what makes mixed-camera training possible — without it, the model fails to converge on mixed data entirely (v1 ablation Table 7: "w/o CSTM" diverges)
- All datasets provide camera intrinsics — this is a requirement, not optional
- Critical data gap: only ~20K outdoor images have GT surface normals (mostly indoor ScanNet). This is why $L_{d-n}$ consistency loss matters — it lets the model learn normals from the millions of depth-only outdoor images.
- 48 A100 GPUs, 800K iterations, batch size 192
- **Time:** 0:40
