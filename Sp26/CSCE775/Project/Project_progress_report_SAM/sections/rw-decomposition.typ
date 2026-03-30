== Multi-Mask Decomposition and Refinement

SAMRefiner @lin2025samrefiner uses heuristic split-then-merge rules for SAM mask refinement. UnSAM @wang2024unsam applies divide-and-conquer normalization for unsupervised segmentation. Neither uses learned decomposition strategies. Our V2 learns when and how to decompose via RL; our V3 leverages VLM reasoning.
