# Critical Feedback on "Related Works" Section

## 1. Reviewer: Undergraduate Aerospace Student
**Perspective:** I'm interested in the drone/hardware part. I know some basics of coding, but the heavy ML theory flies over my head a bit. I just want to know why this matters.

### General Feedback
I think the section is a bit intimidating. There are a lot of big words and heavy concepts (like "spatio-temporal cubes," "bi-directional pseudo label recovery," "difficulty-calibrated uncertainty") that make it hard to follow. If the point of the paper is about a dual-camera system, do we really need a history lesson on all these algorithm tricks?

### Critical Points & What to Cut
*   **Too much detail on other papers:** In Section B (PTZ), you spend a whole paragraph talking about "VIGIA-E" and "patch selection." Is that what we are doing? If not, maybe just say "Other people select zooming patches based on density [11], whereas we track single targets."
*   **Section A is dense:** The paragraph about the "four pillars" of small object detection feels like a textbook definition. I'd condense that into one sentence: "Current software methods try to hallucinate details or use time-history, but they are slow and can't fix the lack of pixels."
*   **Active Learning vs. Auto-Labeling:** Section C is really confusing. You talk about "Pseudo-Labeling" and "Active Learning" separately. To me, they sound similar. Can you just say "We use the robot to verify the label instead of a human"?

### Unanswered Questions
*   "What exactly is a 'hard negative'? You mention it, but I assume it's just something the computer gets wrong. A simple example (like 'a bird looking like a plane') right there would help."
*   "Why are we talking about Deep Reinforcement Learning (RL) in section B if our system uses a standard controller?"

---

## 2. Reviewer: European Aerospace Professor
**Perspective:** I value precision, conciseness, and academic rigor. I dislike "flowery" language and "storytelling." I want to know exactly where this work fits in the literature without the fluff.

### General Feedback
The text is excessively verbose. It reads more like a literature survey than a focused Related Works section. You are using too many adjectives and narrative bridges ("This insight has motivated...", "These examples highlight a trend...", "draws inspiration from..."). This style occupies valuable page space without adding technical substance.

### Critical Points & What to Cut
*   **Reduce Narrative Fluff:**
    *   *Examples to cut:* "The core issue remains one of pixel-level information loss...", "This can be seen as a form of active data acquisition."
    *   *Fix:* State facts directly. "Small object detection suffers from information loss [1]." instead of "The core issue remains..."
*   **Condense Section C (Pseudo-Labeling):** You devote nearly an entire column to explaining the definition of self-training and active learning. This is standard knowledge.
    *   *Cut:* The descriptions of ASTOD and PPAL [12, 15] are too detailed. We do not need to know how they "cluster" or "rank detections" unless your method specifically improves on *that exact step*.
    *   *Recommendation:* Merge the "Pseudo-Labeling" and "Active Learning" explanations into one tight paragraph: "While Active Learning typically queries a human for uncertain samples [14], and Pseudo-Labeling uses high-confidence model predictions [12], our approach uses a sensor query to resolve uncertainty."
*   **Section B (PTZ):** The discussion on "reproducible benchmarks" [7] is irrelevant unless you are evaluating on that specific benchmark. Remove the meta-discussion about how "Standard tracking benchmarks do not capture these effects."

### Unanswered Questions
*   "You cite 'super-resolution' methods as being computationally intensive. Is there a citation comparing the latency of a super-res GAN vs. the 150ms mechanical latency of your system? That is the trade-off you are implicitly arguing for."

---

## 3. Reviewer: MIT Aero/CS Professor
**Perspective:** I know the references. I know the field. I'm looking for the *gap*. If you spend too long explaining basic concepts, I assume you don't have a strong contribution. I will call out "hand-waving."

### General Feedback
Technically correct, but the signal-to-noise ratio is low. You are "over-selling" standard concepts. For instance, you frame "checking a zoom camera" as "Active Learning," which is a bit of a stretch. It's valid, but you belabor the point for 40 lines of text.

### Critical Points & What to Cut
*   **Stop Lecturing:** We know what YOLO is. We know what self-training is.
    *   *Cut:* "Modern object detectors, however, have largely shifted toward deep learning models..." -> Everyone knows this. Delete.
    *   *Cut:* "YOLO-family detectors in particular are popular..." -> Just cite YOLO in the methdology. You don't need to justify its existence here.
*   **Focus on the Gap:** The real gap is that *PTZ tracking usually implies continuous video tracking*, whereas you are doing *discrete spot-checks*.
    *   *Critique:* Section B talks about "keeping a small object centered." But your system seems to be "Slew-to-confirm." The literature review should highlight *slew-to-classification* or *active identification* rather than general tracking.
*   **Specific Cuts:**
    *   The entire paragraph relating to "Deep Reinforcement Learning" [9] in Section B should likely go unless you are using RL. It sets up a false expectation.
    *   The VIGIA-E [11] paragraph is long. It can be reduced to: "Recent works like VIGIA-E [11] manage PTZ attention by selecting high-density regions; in contrast, we prioritize individual low-confidence targets."

### Unanswered Questions
*   "You dismiss super-resolution [2] quickly. Why can't we just run a super-res model on the crop? Modern edge devices are fast. You need to defend why *mechanical* zoom is superior to *generative* upscaling for this specific 'aircraft' use case (answer: ground truth correctness)."

---

# Summary of Actionable Edits to Fix "Long and Windy"
1.  **Delete the "History of Deep Learning" in 2.1:** Remove sentences explaining that "Modern object detectors have shifted to deep learning."
2.  **Compress 2.3 (Pseudo-labeling) by 60%:** Don't explain *how* ASTOD or PPAL work. Just say they exist as methods to filter noise, and your method replaces their statistical filters with a "ground truth" sensor filter.
3.  **Remove RL and Anomaly Detection details in 2.2:** If you aren't doing anomaly detection or RL, citing them with full sentence descriptions distracts the reader. List them as "various control strategies [9, 10]" and move on.
4.  **Remove Adverbs/Adjectives:** Ctrl+F for words like "intriguingly," "crucial," "substantial," "favorable," "unique," "considerable." Remove them. Let the data show it is substantial.
