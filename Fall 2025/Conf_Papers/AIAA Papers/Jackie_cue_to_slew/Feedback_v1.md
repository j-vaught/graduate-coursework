# Critical Feedback on Abstract

## Current Abstract for Reference
> Small objects in wide-field video streams often occupy only a handful of pixels, leading to low detector confidence, unstable localization, and noisy labels that limit dataset quality and model improvement. This paper describes an automated dataset construction system that couples (i) a fixed wide-angle camera running a real-time YOLO-family detector with (ii) a pan--tilt--zoom (PTZ) camera that is programmatically commanded to lock onto candidate targets and zoom in to obtain higher-resolution evidence. The PTZ observation acts as a label-quality amplifier: high-confidence detections in the zoomed view are transferred back to the wide view using calibrated cross-camera geometry and time-synchronized PTZ telemetry. The result is a fully automated pipeline that continuously harvests training examples, hard negatives, and metadata for small-object detection. A concrete test case is presented for airplanes against sky backgrounds, where objects are distant, small, fast-moving, and subject to atmospheric distortion. We provide system design, calibration and control formulations, dataset curation rules, and an evaluation protocol to quantify confidence uplift, label precision, and downstream small-object detection performance.

---

## Reviewer 1: Undergraduate Aerospace Student
**Perspective:** Enthusiastic, familiar with basic concepts (drones, cameras) but gets lost in dense jargon. Values clarity and "the point."

**Feedback:**
*   **"Handful of pixels":** I actually like this phrase! It makes the problem instantly visualizing.
*   **Jargon Alert:** "Hard negatives" -- I'm not entirely sure what this means in this context. Is it when the camera mistakenly thinks a bird is a plane? Maybe clarify slightly or simplify.
*   **"YOLO-family":** I know what YOLO is, but maybe say "object detection algorithms" first?
*   **The "So What?":** The middle part gets a bit heavy with "cross-camera geometry" and "telemetry." I get that it zooms in, but you could emphasize *why* that's so cool earlier. Like, "The PTZ camera acts like a robotic eye that double-checks the wide camera's work."
*   **Missing Info:** You say "airplanes against sky backgrounds." Does this work for other stuff too? Or just planes? It sounds really specific.

**Questions:**
*   Does the system work at night?
*   How fast does the camera have to move to catch a fast plane?

---

## Reviewer 2: European Aerospace Professor
**Perspective:** Formal, academic, precise. Dislikes colloquialisms and vague claims. Focuses on the "contribution" and positioning within the literature (Active Vision).

**Feedback:**
*   **Tone Critique:** "Handful of pixels" is too colloquial for an AIAA technical paper. Consider "limited spatial resolution" or "severe pixel scarcity."
*   **Specificity:** "YOLO-family detector" is vague. Are you using v5, v8? Or is the system agnostic? If it is architecture-agnostic, state that clearly rather than using the informal "family" grouping.
*   **"Label-quality amplifier":** This is a marketing term. Use precise language. "Resolution-enhanced verification" or "Multi-scale evidence fusion" would be more appropriate.
*   **Claim Verification:** You claim "fully automated." In my experience, "fully" is a dangerous word. Are there truly no manual calibration steps or post-hoc filtering? If there are heuristics key to this automation (like the "curation rules" mentioned at the end), they are the contribution, not the "automation" itself.
*   **Missing Context:** The abstract implies this is a novel concept, but active vision tracking has a long history. You should briefly hint at *how* this differs from standard PTZ tracking—specifically the *dataset construction* angle versus just tracking.

**Questions:**
*   What is the quantified re-identification accuracy between the wide and PTZ views? The abstract mentions "transfer," but this is non-trivial.
*   Is the "calibration" static or dynamic?

---

## Reviewer 3: MIT Aero/CS Professor
**Perspective:** Systems-oriented, deep learning expert. Looks for algorithmic novelty, scalability, and performance metrics. Skeptical of "system papers" without hard numbers.

**Feedback:**
*   **The "Hook":** The premise is strong—using hardware (active sensing) to solve a software (data) problem. I would bring this "hardware-for-data" trade-off to the very first sentence.
*   **Mechanism Clarity:** "Programmatically commanded to lock onto" is a bit of a magic black box in this summary. Is this open-loop pointing based on the wide detections, or closed-loop visual servoing? The distinction matters for the "fast-moving" claim.
*   **Data vs. Model:** You mention "model improvement" in the first sentence but "dataset construction" as the main contribution. Be careful not to conflate them. Is the paper about the *system* or the *resulting model performance*? The end of the abstract suggests both, but usually, one is the primary contribution.
*   **Metrics:** "Quantify confidence uplift" is good, but vague. "We demonstrate a 2x increase in mAP" or "Reduces labeling cost by 90%" is better. Give me a number in the abstract if you have it.
*   **"Time-synchronized":** This is the hardest part of multi-camera systems. If you solved this robustly, highlight *how* briefly (e.g., "hardware triggers" vs "software NTP").

**Questions:**
*   What is the latency of the control loop? "Real-time" is subjective. 30Hz? 10Hz?
*   Does the system handle multiple targets? "Lock onto candidate targets" implies a serial process. What is the scheduling policy?

---

## Summary of Actionable Improvements
1.  **Refine Terminology:** Replace "handful of pixels" with "low spatial resolution" (Reviewer 2) but keep the accessibility (Reviewer 1).
2.  **Clarify the "Automation":** Be specific about the "human-out-of-the-loop" aspect to satisfy Reviewer 2.
3.  **Define the Control Loop:** Briefly specify if it's open-loop predictive or closed-loop tracking (Reviewer 3).
4.  **Add a "Hero Number":** If the paper has a strong result (e.g., "boosts mAP by 15%"), add it to the final sentence (Reviewer 3).
5.  **Scope the "YOLO" claim:** Clarify if the system is architecture-agnostic (Reviewer 2).
