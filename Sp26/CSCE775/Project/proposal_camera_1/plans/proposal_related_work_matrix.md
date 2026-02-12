# Related Work Matrix: Proposal 2 (RL-Optimized IR/RGB Reg+Aug)

This matrix supports the proposal by contrasting our adaptive, joint pipeline against static or disjoint prior work.

## Core Claim
Existing pipelines typically use fixed registration (calibrated once) and global augmentation policies (found offline). Proposal 2 introduces an **online, instance-adaptive RL controller** that jointly selects registration complexity and augmentation intensity based on immediate environmental cues.

## Paper-by-Paper Comparison

| Prior Work | Main Idea | What it Solves | Limitation for Our Setting | Our Explicit Improvement |
|---|---|---|---|---|
| **Cubuk et al. 2019 (AutoAugment)** | Search for best fixed augmentation policy using RL | Automates data augmentation design | Finds a *static* policy for the whole dataset; huge compute cost during search | Learn a *dynamic* policy that adapts per image/batch; optimizes for current context. |
| **Cubuk et al. 2020 (RandAugment)** | Randomly select N ops with magnitude M | Removes search cost of AutoAugment | No learning; ignores image content; non-adaptive | RL agent *learns* to select ops based on frame quality/difficulty, not random. |
| **Ho et al. 2019 (PBA)** | Population Based Training for augmentation schedules | Efficient search for augmentation policy | Still produces a fixed schedule/policy for training; not instance-adaptive | Policy observes state (image stats) to make decisions; handles domain shifts at inference/test time if applicable. |
| **Mao et al. 2016 (DeepReg)** | CNNs for direct image registration | Faster, learnable registration | Supervised registration; doesn't decide *which* transform model fits best (e.g. rigid vs homography) | RL agent selects the *complexity* of the registration model needed (model selection). |
| **Zhang et al. 2020 (Deep Image Homography)** | Learn homography estimation via DL | Robust alignment | Fixed to one transform type (Homography); prone to failure if scene is non-planar | Agent can fall back to Rigid/Affine if Homography is unstable or unnecessary. |
| **Ma et al. 2019 (FusionGAN)** | GAN for IR/VI fusion | Generates fused images | Generative focus; doesn't explicitly optimize downstream detection robustness via pipeline control | We optimize the *input pipeline* (reg+aug) to maximize downstream discriminative performance. |
| **Tian et al. 2020 (Co-Contrastive)** | View-invariant representation learning | Self-supervised manifold alignment | Focuses on latent space; assumes roughly aligned views | We explicitly fix geometric misalignment via RL-controlled registration actions. |

## Improvement Claims to Defend in the Proposal

1.  **Dynamic vs. Static:** "While AutoAugment finds a single optimal policy for a dataset, our method adapts the strategy per-frame, allowing stronger augmentations for high-SNR images and conservative ones for degraded inputs."
2.  **Joint Reg+Aug:** "Prior work treats registration and augmentation as orthogonal. We hypothesize they are coupled (e.g., aggressive augmentation can break feature-based registration), and thus joint optimization via RL is superior."
3.  **Model Selection:** "Instead of forcing a complex Homography for every frame (risking overfitting/artifacts), our agent learns to switch to simpler Rigid transforms when adequate, preserving scene geometry."
4.  **Robustness Reward:** "We explicitly train the policy to maximize downstream consistency/robustness, creating a feedback loop absent in standard calibration or unsupervised registration."

## Evidence Plan for Each Claim

-   **Claim 1 (Dynamic):** Compare `RL-Policy` vs `AutoAugment-Fixed` on a mixed-weather test set. Show RL varies actions by weather type.
-   **Claim 2 (Joint):** Ablation: Optimize Reg only, Aug only, vs Joint.
-   **Claim 3 (Selection):** Plot histogram of chosen transforms (Rigid/Affine/Homography) vs. estimated scene depth variance.
-   **Claim 4 (Robustness):** Evaluate on "noisy alignment" synthetic tests; show RL recovers performance where baselines fail.

## Suggested Language for Proposal "Approach" Paragraph

"Standard multimodal pipelines rely on static calibration and global augmentation heuristics (e.g., RandAugment) that fail to account for instance-level variability in marine environments. We propose a **Context-Aware Deep RL Policy** that jointly optimizes registration model selection and augmentation parameters for every frame. Unlike static AutoML approaches, our agent observes frame-level quality metrics and environmental tags to dynamically balance alignment precision with augmentation diversity, directly maximizing downstream perception robustness."
