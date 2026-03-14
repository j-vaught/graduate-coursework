# Section 1: Introduction & Background (3 min, 10 pts)

## Slide 0 — Title
- Paper title, authors, TPAMI 2024, presenter: J.C. Vaught
- **Time:** 0:30

## Slide 1 — Why Depth Matters
- **Layout:** Split vertically into two columns
- **Left column:** General applications (autonomous driving, robotics, AR/VR, 3D reconstruction)
- **Right column:** Personal use case — using camera + depth to label objects in marine radar; most depth models fail at long range
- **Time:** 0:45

## Slide 2 — Existing Solutions
- **Layout:** 4 quadrants (2x2 grid). Each quadrant split vertically: left half = text + limitations, right half = visual/diagram
- **TL:** LiDAR (accurate but expensive, sparse, no color)
- **TR:** Stereo cameras (requires calibration, fixed baseline limits range)
- **BL:** Structured light (indoor only, short range)
- **BR:** SfM/MVS (needs multiple views, slow, fails on dynamic scenes)
- **Time:** 1:00

## Slide 3 — Monocular Depth Estimation
- **Layout:** Split into thirds
- **Left 2/3:** Timeline/arrow progression — relative depth (MiDaS/DPT) → affine-invariant (DepthAnything/Marigold) → metric depth (ZoeDepth, Metric3D v2). Shows the field narrowing toward the goal.
- **Right 1/3:** Stylized TikZ block diagram — RGB image block feeds down (arrow) into depth map block. Simple, iconic.
- **Time:** 0:45

## Slide 4 — Metric3D v2 Results
- **Layout:** 3 equal columns
- **Left 1/3:** Text — zero-shot, beats fine-tuned methods. Key numbers (NYUv2 AbsRel 0.063, KITTI 0.043).
- **Middle 1/3:** RGB → depth colormap
- **Right 1/3:** RGB → surface normals
- **Time:** 0:30
