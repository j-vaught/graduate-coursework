= Introduction <sec:introduction>

The Segment Anything Model (SAM) @kirillov2023sam, released by Meta (formerly Facebook) in 2023, was one of the first models to allow for interactive, semi-automated segmentation. Although marketed as a one-shot segmentation model, it became common for many teams working on segmentation to use it to significantly speed up segmentation.

SAM takes in a point, a box, or a mask as an input and creates a segmentation mask as output. While this is good in theory, the reality is that the quality of the output is highly variable and sensitive to a variety of issues, like image input quality, point input quality, and of course, the nature of the image itself --- certainly an object of a person (of which there are millions of training examples) is trivial to segment as compared to something rarer with specific, small, and often occluded features like an electrical diagram for example.

Additionally, once a point is placed in SAM, it will create a hypothesis as to what it thinks you are trying to segment and create multiple tiers of segmentations. This is naturally useful and indeed preferred in many cases since the model must try to guess what the user is trying to segment from the initial click --- i.e., clicking on a logo on a person's shirt yields many possibilities for the model. Is the user trying to segment the person, the shirt, the logo, or something else?

While this is useful, it also creates a problem where when the user clicks on the shirt, the model may incorrectly create a hypothesis that the user is trying to segment the person. Then all later clicks will be interpreted in the context of that hypothesis. This will, can, and has led to a situation where the model becomes committed to a particular interpretation and fails to adjust its segmentation based on new input.

In the context of our work, we are only focusing on creating a solution to two of these issues: a) the sensitivity of SAM to the prompt points and their state, and b) the hypothesis commitment problem. While we do not address the image quality issue and the plethora of proposed solutions in that area, we do utilize a variety of different datasets in different domains to ensure that any solution we do develop remains agnostic to the image quality and domain.

In 

Given a prompt---a point, a box, or a mask---SAM produces remarkably accurate segmentation hypotheses across an extraordinary range of domains. The quality of SAM's output is, however, inextricably bound to the quality of its input: a well-placed click elicits a crisp mask, while a careless click yields a fragmented prediction.

This burden becomes acute in the _one-shot segmentation_ setting. A single labeled reference image defines the target class, and the system must autonomously segment that class in a novel query image without human intervention. The problem requires semantic understanding (inferring a class concept from one exemplar), spatial reasoning (identifying where the concept is instantiated), and interactive control (selecting and refining prompts until the segmentation is satisfactory).

#figure(
  image("../figures/fig_problem.pdf", width: 100%),
  caption: [The one-shot segmentation problem. Given a reference image with a known mask (support set) and a new query image of the same class, the system must produce an accurate segmentation mask by placing point prompts for SAM.],
) <fig:problem>

Automating prompt selection for SAM decomposes into five interacting sub-problems: understanding the target from one example, deciding where to click, interpreting SAM's mask feedback, knowing when to stop, and handling SAM's hypothesis commitment---where accumulated points targeting different object parts cause the decoder to lock into one interpretation. We conducted a systematic month-long investigation into automated prompt optimization, pursuing four progressively sophisticated approaches.

Our *first approach* treated prompt selection as a graph-based reinforcement learning problem. A Deep Q-Network was trained to select optimal prompt sequences from a graph of candidate locations. This formulation encountered fundamental design flaws---a lossy 8-dimensional state vector, misaligned proxy rewards, and an inappropriate training paradigm---and was abandoned after thorough failure analysis.

Our *second approach*, V1 PolicyTransformer, simplified the architecture substantially. A transformer-based policy ($tilde 27"M"$ parameters) was trained via behavioral cloning on oracle demonstrations followed by PPO fine-tuning @schulman2017ppo. This produced promising early results but suffered from catastrophic collapse during PPO fine-tuning.

Our *third approach*, V2 SubMaskPolicyTransformer ($tilde 37"M"$ parameters), addressed SAM's hypothesis commitment problem by introducing a sub-mask decomposition action space with five discrete actions. In practice, however, the decomposition action was never discovered during training---the policy consistently collapsed to a sub-optimal fixed point.

Our *fourth approach* deployed Qwen3-VL-8B @bai2025qwen25vl as a zero-shot interactive segmentation agent. This approach requires no task-specific training, leverages broad visual reasoning capabilities, and achieves 0.776 mean Dice with 1.3 clicks---outperforming all trained policies.

This work makes four primary contributions. First, it provides a comprehensive empirical analysis of four RL paradigms for SAM prompt optimization, including graph-based Q-learning, behavioral cloning with PPO, sub-mask decomposition with GRPO/PPO, and VLM-based zero-shot control. Second, it introduces a novel sub-mask decomposition action space that directly addresses SAM's hypothesis commitment problem, together with a detailed failure analysis of why policy gradient methods fail to discover it. Third, it presents the first application of a VLM as an interactive segmentation policy for SAM, using a three-phase decision loop with post-click review. Fourth, it provides a detailed failure analysis identifying three systematic failure modes: reward collapse under PPO, decomposition suppression under short-horizon credit assignment, and distribution shift cascade from behavioral cloning to on-policy learning.

Section @sec:related reviews related work. Section @sec:qlearning documents the Q-learning investigation and its failure analysis. Section @sec:dataset describes the evaluation protocol. Sections @sec:v1 through @sec:v3 present the three main architectures. Section @sec:results reports experimental results. Section @sec:discussion synthesizes lessons learned. Sections @sec:engineering and @sec:conclusion cover infrastructure and conclusions.
