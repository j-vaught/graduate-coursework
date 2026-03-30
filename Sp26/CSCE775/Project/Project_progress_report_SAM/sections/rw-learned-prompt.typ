== Learned Prompt Placement

CPlot @liu2024cplot uses optimal transport for multi-click placement in a single forward pass. PseudoClick @chen2022pseudoclick generates synthetic click sequences for training. Both miss SAM's interactive feedback loop that our approach exploits.

No prior work combines learned RL click placement, learned sub-mask decomposition, VLM-based visual reasoning, and comprehensive failure analysis. AlignSAM does RL+SAM but no decomposition. SAMRefiner does decomposition but heuristically. No prior work uses VLMs for interactive SAM prompt placement.
