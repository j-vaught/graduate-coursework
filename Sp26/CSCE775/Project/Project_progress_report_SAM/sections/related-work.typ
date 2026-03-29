= Related Work <sec:related>

#include "rw-foundation-models.typ"

== SAM and Interactive Segmentation

SAM @kirillov2023sam and SAM 2 @ravi2024sam2 achieve strong segmentation given spatial prompts but exhibit well-documented failure modes on thin structures, branching objects, and low-contrast regions. Most consequential for interactive use is the hypothesis commitment problem: when multiple points target different object parts, the decoder commits early to one interpretation and resists correction. Expert annotators work around this by creating independent sub-masks --- a strategy our V2 automates.

Interactive segmentation methods including RITM @sofiiuk2022ritm, FocalClick @chen2022focalclick, and SimpleClick @liu2023simpleclick train end-to-end click-conditioned models but retrain the segmentation backbone. Our approach treats SAM as frozen and learns only the prompt policy --- a practical advantage (no 600M+ parameter retraining) but a harder optimization problem.

#include "rw-interactive-segmentation.typ"

#include "rw-prompt-learning.typ"

== RL for Click and Prompt Optimization

AlignSAM @huang2024alignsam is the closest prior work, training an RL agent for iterative SAM point prompts in a single-mask regime. SeedNet @song2018seednet demonstrated RL for seed placement in pre-SAM interactive segmentation. AIES @aies2024 uses a DQN to select prompt types (point vs box vs mask) for medical imaging. TEPO @cheng2023tepo addresses temporally-extended prompts across 3D slices. IteR-MRL @liao2020itermrl applies multi-agent RL for 3D medical segmentation.

#include "rw-rl-vision.typ"

== Multi-Mask Decomposition and Refinement

SAMRefiner @lin2025samrefiner uses heuristic split-then-merge rules for SAM mask refinement. UnSAM @wang2024unsam applies divide-and-conquer normalization for unsupervised segmentation. Neither uses learned decomposition strategies. Our V2 learns when and how to decompose via RL; our V3 leverages VLM reasoning.

#include "rw-reward-shaping.typ"

#include "rw-imitation-learning.typ"

#include "rw-vlm.typ"

#include "rw-few-shot-seg.typ"

== Learned Prompt Placement

CPlot @liu2024cplot uses optimal transport for multi-click placement in a single forward pass. PseudoClick @chen2022pseudoclick generates synthetic click sequences for training. Both miss SAM's interactive feedback loop that our approach exploits.

No prior work combines learned RL click placement, learned sub-mask decomposition, VLM-based visual reasoning, and comprehensive failure analysis. AlignSAM does RL+SAM but no decomposition. SAMRefiner does decomposition but heuristically. No prior work uses VLMs for interactive SAM prompt placement.
