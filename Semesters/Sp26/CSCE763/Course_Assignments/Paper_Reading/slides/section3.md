# Section 3: Results & Discussion (5 slides, ~5 min, 25 pts)

Covers both Experiment (10 pts) and Critical Comments (15 pts). Narrative arc: benchmarks → my demos → where it works → where it fails → broader limitations.

## Slide 1 — Benchmark Numbers
- **Layout:** Left 2/3 table, right 1/3 bar chart or radar chart
- **Left:** Zero-shot metric depth results (no fine-tuning on target dataset):
  - NYUv2 AbsRel 0.063, δ₁ 0.975 (indoor, structured rooms)
  - KITTI AbsRel 0.043, δ₁ 0.989 (outdoor driving, LiDAR GT)
  - ScanNet AbsRel 0.069, δ₁ 0.970 (indoor, handheld RGB-D)
  - DIODE Outdoor AbsRel 0.308, δ₁ 0.832 (diverse outdoor — note the drop)
- **Right:** Visual comparison — bar chart of AbsRel across datasets, garnet bars, DIODE bar highlighted in rose to foreshadow out-of-distribution trouble
- Emphasize: zero-shot results that beat methods fine-tuned on those datasets
- **Time:** 0:45

## Slide 2 — iPhone Demo Mosaic
- **Layout:** 3×3 grid, each cell = thumbnail RGB + depth colormap side by side
- All photos taken on my iPhone (3 lenses: ultra-wide 13mm, wide 26mm, telephoto 77mm)
- Test matrix:

| # | Condition | Lens | Why |
|---|-----------|------|-----|
| 1 | Indoor room, well-lit | Wide 26mm | Baseline easy case, compare to NYUv2 |
| 2 | Indoor room, dim/low-light | Wide 26mm | Noise robustness |
| 3 | Outdoor street, daytime | Wide 26mm | Compare to KITTI-like driving scenes |
| 4 | Outdoor far scene (>50m) | Telephoto 77mm | Long-range accuracy |
| 5 | Outdoor close object (<1m) | Ultra-wide 13mm | Near-field with extreme FOV |
| 6 | Object with known size | Wide 26mm | Metric verification (used on next slide) |
| 7 | Outdoor night/dusk | Wide 26mm | Low-light + mixed illumination |
| 8 | Reflective/transparent surface | Wide 26mm | Known failure mode (window, water) |
| 9 | Repeated texture (brick, tile) | Wide 26mm | Ambiguous depth cues |

- Each cell labeled with lens + condition, depth colormap uses brand palette
- Brief narration: walk through a few highlights, note which look great and which look suspicious
- **Time:** 1:15

## Slide 3 — Metric Verification
- **Layout:** Two columns
- **Left column:** Photo of object with known dimensions (textbook, door frame, or desk)
  - Annotated with measurement line overlay (garnet)
  - EXIF readout: focal length, sensor size
- **Right column:** Depth map with same measurement overlay
  - Predicted 3D distance between endpoints
  - Ground truth distance
  - Error percentage
- Takeaway: works well on rigid, textured, front-facing objects at moderate range
- Note: this is "metrology in the wild" — one of the paper's claimed downstream applications
- **Time:** 0:45

## Slide 4 — Marine Radar Use Case
- **Layout:** Two columns
- **Left column:** My application context
  - Fuse camera depth with marine radar to auto-label radar targets
  - Need metric depth at 50–500m over open water
  - Show: point cloud generated from a harbor/boat photo (demo 3 output)
- **Right column:** Why Metric3D v2 fails here
  - Water has no texture → depth network hallucinates (no visual features to match)
  - Horizon is at infinity → network clips or saturates
  - Spray, reflections, specular highlights violate Lambertian assumption
  - Training data: ~0 marine scenes in any of the 16 datasets (all terrestrial)
  - DIODE Outdoor AbsRel 0.308 is the canary — diverse outdoor already degrades heavily
- Connect back to benchmarks: performance is only as good as training distribution
- **Time:** 1:15

## Slide 5 — Strengths and Limitations
- **Layout:** Two columns, left = strengths, right = limitations
- **Strengths:**
  1. CSTM is elegant — single scaling factor, no architecture changes, pluggable to any backbone
  2. Consistency loss ($L_{d-n}$) learns normals from depth-only data — clever use of geometric constraints
  3. Comprehensive evaluation across 16+ benchmarks
  4. Immediately usable — PyTorch Hub, one-line inference, multiple model sizes
  5. Clean native normals — Depth Pro and DepthAnything produce depth only; deriving normals post-hoc is noisy
- **Limitations:**
  1. Requires camera intrinsics at inference — UniDepth and Depth Pro estimate $f$ internally
  2. Single-frame only — no temporal consistency for video (flickering)
  3. $f^c = 1000$ is ad hoc — no sensitivity analysis or theoretical justification
  4. Out-of-distribution collapse — marine, underwater, aerial, medical all absent from training
  5. Newer competitors closing the gap — MoGe (CVPR 2025) jointly predicts 3D points + normals + FOV without intrinsics
- **Time:** 1:00
