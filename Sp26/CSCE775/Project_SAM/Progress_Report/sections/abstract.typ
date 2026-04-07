#block(width: 100%, inset: (x: 2em))[
  #text(weight: "bold", size: 12pt)[Abstract]
  #v(0.5em)

 This work investigates reinforcement learning (RL) and vision-language model (VLM) strategies for automated prompt optimization in the Segment Anything Model (SAM) by Meta, presenting four  approaches evaluated on the FSS-1000 few-shot segmentation benchmark against a brute-forced baseline of 0.807 Dice.

  We first implemented a Deep Q-Network (DQN) agent operating over graph-structured prompt representations with DINO-derived proxy rewards, derived from existing work from the Plug-and-Play PPO framework @ppo2025cvpr. This approach was deemed a failure, achieving only *0.60 Dice*, whiwch we attributed to lossy state encoding, severe reward misalignment between proxy objectives and true segmentation quality, and an ill-suited training paradigm after an analysis. 

  The second approach introduced a novel, single-mask PolicyTransformer (~27M parameters) trained via behavioral cloning (BC) followed by Proximal Policy Optimization (PPO). BC warmstarting achieved *0.549 Dice* with *91% action accuracy*, but, unfortunately, subsequent PPO fine-tuning peaked at *0.49 Dice* before policy collapse.

  The third approach extended the architecture to a, once again, novel SubMaskPolicyTransformer (~37M parameters) incorporating a five-action space, as compared to the prior 3-action space, designed to enable hierarchical sub-mask decomposition. Despite training via both GRPO (plateau at *0.43 Dice*) and PPO (*peak 0.60 Dice* before collapse), the policy never discovered meaningful sub-mask behavior, with the number of sub-masks at effectively 1.0 throughout training.

  The fourth approach replaced learned policies entirely with zero-shot VLM inference using Qwen3-VL-7B, employing a four-panel visual state renderer and a three-phase decision loop. This approach achieved *0.853 Dice with a mean of 1.4 clicks*, and a cross-architecture ablation yielded *0.776 mean Dice with 1.3 clicks*.

  These results demonstrate that supervised warmstarting is insufficient to stabilize RL fine-tuning, that emergent compositional behaviors such as sub-mask decomposition are not discovered through reward alone, that proxy reward signals introduce dangerous optimization misalignment, and that zero-shot VLM reasoning can surpass all trained policies without any task-specific optimization.
]
