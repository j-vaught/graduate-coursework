== SAM and Interactive Segmentation

SAM @kirillov2023sam and SAM 2 @ravi2024sam2 achieve strong segmentation given spatial prompts but exhibit well-documented failure modes on thin structures, branching objects, and low-contrast regions. Most consequential for interactive use is the hypothesis commitment problem: when multiple points target different object parts, the decoder commits early to one interpretation and resists correction. Expert annotators work around this by creating independent sub-masks --- a strategy our V2 automates.

Interactive segmentation methods including RITM @sofiiuk2022ritm, FocalClick @chen2022focalclick, and SimpleClick @liu2023simpleclick train end-to-end click-conditioned models but retrain the segmentation backbone. Our approach treats SAM as frozen and learns only the prompt policy --- a practical advantage (no 600M+ parameter retraining) but a harder optimization problem.
