# Search Results: Latency & Optical vs. Generative Zoom

## 1. Latency Comparison: Edge Super-Resolution vs. Mechanical Zoom
*   **Edge Super-Resolution (SR) on Jetson Orin:**
    *   Lightweight SR models (e.g., SwiftSRGAN, optimized YOLOX) can achieve inference times of **20ms--35ms** on Jetson Orin hardware using TensorRT optimization [1, 6].
    *   However, high-fidelity models (e.g., Real-ESRGAN) on larger input patches can scale up to **300ms+**, making them slower than real-time requirements [8].
*   **Mechanical Zoom Latency:**
    *   Typical autofocus/zoom lenses have a latency of **2--6 frames (66ms--200ms)** for rapid movements [9].
*   **Conclusion for Paper:** The mechanical latency (~150ms) is comparable to heavy SR models but slower than lightweight ones. The defensive argument must therefore rely on **correctness**, not speed.

## 2. Optical Zoom vs. Super-Resolution (Generative)
*   **Ground Truth Argument:**
    *   Optical zoom preserves actual photonic data ("true resolution"), whereas Super-Resolution "hallucinates" or estimates details based on learned priors [1, 9].
    *   For dataset creation, optical zoom is superior because it provides a **ground truth label**. Using SR to label small objects introduces "confirmation bias" (the model learns from its own hallucinations).
    *   Optical zoom is standard for industrial inspection where distinct defects must be resolved without artifacting [9].

## 3. The "Gap": Active Acquisition vs. Tracking
*   **Existing Literature:**
    *   Most PTZ literature focuses on **Continuous Tracking** (keeping a target in the center of the frame while moving) [1, 10].
    *   "Active Vision" usually implies searching or multi-camera coordination for coverage [2].
*   **Your Contribution:**
    *   Your method is **"Slew-to-Classification"** (or "Active Acquisition"): discrete, rapid movements to query a target for identification, rather than continuous video tracking. This is distinct from standard surveillance.

## References Found
1.  [NVIDIA Jetson Benchmarks]
2.  [Active Silicon - Autofocus Block Camera Latency]
3.  [Standard Object Detection vs Super-Resolution Performance studies]
