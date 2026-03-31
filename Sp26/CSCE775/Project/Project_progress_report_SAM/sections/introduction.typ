= Introduction <sec:introduction>

The Segment Anything Model (SAM) @kirillov2023sam, released by Meta (formerly Facebook) in 2023, was one of the first models to allow for interactive, semi-automated segmentation. Although marketed as a one-shot segmentation model, it became common for many teams working on segmentation to use it to significantly speed up segmentation.

SAM takes in a point, a box, or a mask as an input and creates a segmentation mask as output. While this is good in theory, the reality is that the quality of the output is highly variable and sensitive to a variety of issues, like image input quality, point input quality, and of course, the nature of the image itself --- certainly an object of a person (of which there are millions of training examples) is trivial to segment as compared to something rarer with specific, small, and often occluded features like an electrical diagram for example.

Additionally, once a point is placed in SAM, it will create a hypothesis as to what it thinks you are trying to segment and create multiple tiers of segmentations. This is naturally useful and indeed preferred in many cases since the model must try to guess what the user is trying to segment from the initial click --- i.e., clicking on a logo on a person's shirt yields many possibilities for the model. Is the user trying to segment the person, the shirt, the logo, or something else?

While this is useful, it also creates a problem where when the user clicks on the shirt, the model may incorrectly create a hypothesis that the user is trying to segment the person. Then all later clicks will be interpreted in the context of that hypothesis. This will, can, and has led to a situation where the model becomes committed to a particular interpretation and fails to adjust its segmentation based on new input.

In the context of our work, we are only focusing on creating a solution to two of these issues: a) the sensitivity of SAM to the prompt points and their state, and b) the hypothesis commitment problem. While we do not address the image quality issue and the plethora of proposed solutions in that area, we do utilize a variety of different datasets in different domains to ensure that any solution we do develop remains agnostic to the image quality and domain.

== One-shot segmentation with SAM

The set of aforementioned issues with SAM are somewhat manageable when a person is in the loop, as the user can provide feedback and a certain level of reasoning about the segmentation problem at hand. However, when we move to predominantly automated scenarios (i.e., automated dataset labeling as we see Meta and many AI companies foolishly attempting), the problem of accuracy becomes much more noticeable. A correction rate of 10% for a human annotator would not raise any flags since the 10% error signifies a 90% decrease of effort as opposed to manually labeling the images. This same 10% error rate becomes a massive problem once datasets scale to millions or tens and hundreds of millions of images, a scale simply unmanageable by human annotators.

=== Problem formulation

We find it important to first begin by formulating the problem of one-shot segmentation in a clear and understandable way (with all the pesky, error-prone mathematics brushed aside for now). The problem is explained as simply as I can manage as such: given a reference image, along with a reference mask/segmentation, can we develop a model or algorithm that can then segment that same object or class from the reference image in an arbitrary query image, and furthermore, can the model determine when the object class is not present in the image? No other work we were able to find explored the efficacy of these models when including images without the object class. A visual example of the problem is shown in @fig:problem.

#figure(
  image("../figures/fig_problem.pdf", width: 100%),
  caption: [The one-shot segmentation problem. Given a reference image with a known mask (support set) and a new query image of the same class, the system must produce an accurate segmentation mask by placing point prompts for SAM.],
) <fig:problem>

== Action Space
Although there are a multitude of attempts to decompose the problem of point-prompt based segmentation, we attempt to do so in a sense that is more applicable to reinforcement learning by breaking the problem down into a sequential decision process with a two-tiered action space, with one tier being spatial (i.e., where to click) and the other being semantic, i.e., deciding what the next step is or determining when the mask quality is adequate.

The first action space (or tier one, spatial) was somewhat already decided for us, since we were building on the work of @ppo2025cvpr who had built a graph-based solution to the problem, although there are many issues with their solution. Regardless, the decision to use DINO as the backbone for spatial prompt selection was decided on since many papers had shown promise. Therefore, the spatial action space was set to be a 37x37 grid of click/point locations as determined by the DINO architecture.

The second action space (or tier two, semantic) ended up changing quite a lot as we explored our approach, however I will do my best to summarize the choices here as well as justify them for the dear reader.

1. The most important action the model can take is to place a positive point, which is a point that is placed on the object of interest. This is, of course, a required action by SAM, and thus was not really examined under a close lens.

2. The second most important action the model can take is to place a negative point, which is a point that is placed on the background or on an object that is not the object of interest. This is also a required action by SAM, and was not really examined under a close lens.

3. While somewhat debated, I argued for, and we eventually agreed to add a STOP action to the model, allowing the model itself to decide when it was good enough. The reason for this action was the idea that a cutoff built into the harness itself would result in failure in novel spaces or spaces without ground truth data. It also allowed for us to explore the idea of rewarding the model on efficiency and learning to place less optimal clicks but fewer of them, allowing the process to be sped up.

4. Later, we decided to expand the action space to include a few more actions (see the V2 section for more details) that would allow the model to directly address the hypothesis commitment problem. This was done by allowing the model to place a decomposition action that would allow it to break down the mask into sub-masks and then place points on those sub-masks. The idea was that this would allow the model to escape from a bad hypothesis by breaking down the mask into smaller parts and then placing points on those parts to refine the segmentation. While this idea worked excellently for human annotators, we never saw results with the standard Transformer model we developed.

5. Finally, in the most recent version we added in a series of new actions including a review action, a reset action, and an undo action to undo the last step. In the most recent version we also added a third tier which was used by the model when deciding to place points, since we discovered (and literature has shown) that the VLMs are somewhat poor at deriving coordinates onto images or placing objects onto images, with Google being the best in the field at this so far. The third tier corrected this by allowing the model to adjust points before placing them, flipping them from positive to negative, vice versa, nudging them, or even moving them to a different location.

== Results

Although our work is severely behind schedule, we have completed a series of research breakthroughs and developed a few novel components to be implemented in the one-shot segmentation task. Additionally, due to the fact that we have a surplus of compute as compared to most students working on this project as well as access to the frontier coding agents with high token limits, we have been able to make significant progress. While we will give each approach proper and full treatment in later sections, a brief overview is available here to preview.

1. Our first approach treated prompt selection as a graph-based reinforcement learning problem. A Deep Q-Network was trained to select optimal prompt sequences from a graph of candidate locations. This formulation encountered a series of design flaws --- a lossy 8-dimensional state vector, misaligned proxy rewards, and an inappropriate training paradigm. Consequently, the effort was abandoned after thorough failure analysis.

2. Our second approach, V1 PolicyTransformer, simplified the architecture substantially. A transformer-based policy ($tilde 27"M"$ parameters) was trained via behavioral cloning on oracle demonstrations followed by PPO fine-tuning @schulman2017ppo. This produced promising early results but suffered from model collapse during PPO fine-tuning.

3. Our third approach, V2 SubMaskPolicyTransformer ($tilde 37"M"$ parameters), addressed SAM's hypothesis commitment problem by introducing a sub-mask decomposition action space with five discrete actions. In practice, however, the decomposition action was never discovered during training and the policy consistently collapsed to a sub-optimal fixed point.

4. Our fourth approach deployed Qwen3-VL-8B @bai2025qwen25vl as a zero-shot interactive segmentation agent. This approach requires no task-specific training, leverages broad visual reasoning capabilities, and achieves 0.776 mean Dice with 1.3 clicks --- outperforming all trained policies. This model also introduces the three-tier action space as well as the idea of multi-step reasoning with a post-click review action, which we found to be critical for performance.

== Contributions and Paper Structure

Finally, we use this section to give ourselves credit for our ingenuity.

This work makes four primary contributions to the field as of now, and we hope to make more contributions as we continue to work on this project.

First, our work provides a comprehensive empirical analysis of four RL paradigms for SAM prompt optimization, including graph-based Q-learning, behavioral cloning with PPO, sub-mask decomposition with GRPO/PPO, and VLM-based zero-shot control.

Second, it introduces a novel sub-mask decomposition action space that directly addresses SAM's hypothesis commitment problem, together with a failure analysis of why policy gradient methods fail to discover it.

Third, it presents the first application of a VLM as an interactive segmentation policy for SAM using a three-phase decision loop with post-click review.

Fourth, it provides a detailed failure analysis identifying three systematic failure modes: a) reward collapse under PPO, b) decomposition suppression under short-horizon credit assignment, and c) distribution shift cascade from behavioral cloning to on-policy learning.

Section @sec:related reviews related work. Section @sec:qlearning documents the Q-learning investigation and its failure analysis. Section @sec:dataset describes the evaluation protocol. Sections @sec:v1 through @sec:v3 present the three main architectures. Section @sec:results reports experimental results. Section @sec:discussion synthesizes lessons learned. Sections @sec:engineering and @sec:conclusion cover infrastructure and conclusions.
