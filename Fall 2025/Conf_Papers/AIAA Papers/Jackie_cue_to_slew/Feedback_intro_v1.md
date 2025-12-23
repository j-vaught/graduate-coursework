# Feedback on Introduction - v1

## Reviewer 1: Undergraduate Aerospace Student
**Perspective:** Enthusiastic but new to the field. Focuses on clarity, "big picture" understanding, and getting past jargon.

### General Impression
"The intro is pretty cool! I like the idea of using a zoom camera to check what the wide camera sees. It reminds me of how human eyes work—scanning and then focusing. However, some sentences are really dense, and I had to read them twice to understand what was actually happening."

### Critical Feedback
1.  **Jargon Density:**
    *   *Critique:* Terms like "discriminative detail," "class imbalance," and "spatially consistent" in the first few paragraphs are a bit heavy.
    *   *Suggestion:* Maybe start with a simpler analogy? Like, "Wide cameras are like peripheral vision, undefined and blurry. PTZ is the fovea."
2.  **The "Data Bottleneck" Concept:**
    *   *Critique:* You say performance is "bottlenecked by quality/quantity of training data." I thought better AI models (architectures) were the answer?
    *   *Suggestion:* Briefly explain *why* better models can't just fix pixelated blobs. A simple sentence like "No matter how smart the AI is, it can't invent details that aren't there" would help.
3.  **The "Airplane" Context:**
    *   *Critique:* You mention the "airplane-in-the-sky test case" at the very end.
    *   *Suggestion:* Bring this up earlier! It helps me visualize *what* we are looking for. "Imagine trying to spot a drone against a cloud..." captures attention faster than "Small object detection remains difficult."

### Questions Unanswered
*   "What exactly is a 'hard negative'? You mention it, but I don't really get why it's so important until later."
*   "Is this system for real-time tracking (like shooting things down) or just for making datasets? The title says 'Dataset Construction' but the text talks about 'tracking' and 'latency', which sounds like real-time ops."

---

## Reviewer 2: Aerospace Professor (European University)
**Perspective:** Formal, academic, values precise taxonomy, historical context, and clear contribution claims.

### General Impression
"The introduction is competent but somewhat informal in its structuring. It defines the problem well but lacks a distinct 'Contributions' summary that clearly separates your novel engineering from standard integration. The flow is logical, but the motivation could be more grounded in the specific deficits of current *aerospace* datasets rather than general 'small object' literature."

### Critical Feedback
1.  **Structure and Contributions:**
    *   *Critique:* The introduction blends the problem statement, method, and motivation into a continuous narrative. This is readable but makes it hard to pinpoint the exact novelties.
    *   *Suggestion:* I strongly recommend adding a bulleted list of research contributions at the end of the Introduction. State clearly: "The contributions of this paper are: 1) A novel active acquisition loop... 2) A homography-based label transfer method... 3) A specific dataset validation..."
2.  **Terminology Precision:**
    *   *Critique:* You use the term "Active Acquisition." In Control Theory, "Active Sensing" usually implies moving a sensor to minimize state estimation covariance. Here, you are maximizing *dataset utility*.
    *   *Suggestion:* Be careful to distinguish between "Active Tracking" (keeping target in view) and "Active Dataset Construction" (deciding *if* a target is worth zooming in on for training data). The intro blurs these slightly.
3.  **Literature Context:**
    *   *Critique:* "Active PTZ systems have long been studied..." is a bit vague.
    *   *Suggestion:* Cite a classic foundational paper here (e.g., Bajcsy’s Active Perception) to show you appreciate the roots of the field before jumping to "modern work."

### Questions Unanswered
*   "How does this approach differ fundamentally from simply recording high-res video and cropping it later? The argument for *active* mechanical zoom versus high-resolution full-frame recording (e.g., 4K/8K sensors) needs to be made stronger in the intro. Why is the mechanical complexity justified?"

---

## Reviewer 3: Aerospace Professor w/ CS & Robotics Background (MIT)
**Perspective:** Technical, systems-oriented, skeptical of "integration papers," looks for the "hard" problems (latency, dynamics, system limits).

### General Impression
"The premise is solid—data is the bottleneck, not the model. I agree. However, the introduction reads a bit too much like a 'system report' and not enough like a 'research paper'. You need to highlight the *hard* parts. Slewing a mechanical PTZ to catch a fast-moving, distant aircraft is a control and latency nightmare. The intro makes it sound too easy. Sell the difficulty."

### Critical Feedback
1.  **The Latency/Dynamics Problem:**
    *   *Critique:* You mention "compensating for mechanical latencies" in the abstract, but the Introduction glosses over it.
    *   *Suggestion:* In paragraph 3 ("The key idea..."), explicitly mention that the *core challenge* is the temporal mismatch. "The wide camera sees the past; the PTZ must aim at the future." This is the interesting dynamics problem. The intro focuses too much on the "static" concept of label transfer.
2.  **System vs. Method:**
    *   *Critique:* The intro focuses heavily on the "system" (hardware roles).
    *   *Suggestion:* Pivot the framing. The paper isn't just about a camera setup; it's about a *methodology* for self-supervised label generation. Frame it as "A method for physical verification of weak visual signals," rather than "We built a dual-camera rig."
3.  **The "Oracle" Claim:**
    *   *Critique:* You imply the PTZ is a "labeling oracle."
    *   *Suggestion:* Be careful. A PTZ view is better, but is it ground truth? What if the zoom is blurry? What if the handover fails? Acknowledge the *noise* in your oracle source early on. It adds credibility.

### Questions Unanswered
*   "What is the *yield*? How many 'active' samples can you actually get per minute? If mechanical slewing takes 2 seconds, your dataset generation rate is physically capped. This physical limit on data scale is a crucial constraint that should be mentioned in the intro."
*   "Is the homography assumption (static calibration) valid for a PTZ that vibrates and moves? I'd expect dynamic calibration or registration to be necessary. Handling this criticism in the intro (even briefly) would be smart."
