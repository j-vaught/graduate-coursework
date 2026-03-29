= Dataset and Evaluation Protocol <sec:dataset>

== FSS-1000 Dataset

All experiments are conducted on FSS-1000 @li2020fss, a 1,000-class few-shot segmentation benchmark with 10 images per class and pixel-level masks. Images are loaded as RGB float32 tensors normalized to $[0, 1]$; masks are binarized at threshold 127. All images are resized to $518 times 518$ pixels ($37 times 14 = 518$), aligning with DINOv2 ViT-L/14's patch stride.

== Class-Disjoint Splits

The 1,000 classes are partitioned into 700 training, 150 validation, and 150 test classes via deterministic shuffle (seed=42). The partition is serialized to a JSON manifest consumed by all data loaders. Episode sampling is deterministic: class $= i mod N_("classes")$, support index $= j$, query index $= (j+1) mod 10$.

== Evaluation Metrics

#figure(
  table(
    columns: (9em, 11em, 1fr),
    table.hline(),
    [*Metric*], [*Formula*], [*Description*],
    table.hline(),
    [Dice], [$2|P sect G| \/ (|P| + |G|)$], [Primary segmentation quality metric.],
    [IoU], [$|P sect G| \/ |P union G|$], [Complementary overlap measure.],
    [Mean Clicks], [---], [Average point prompts per episode. Lower is better.],
    [Stop Success], [$S_tau$], [Episodes where the agent stops with Dice $>= tau$ ($tau = 0.85$).],
    [Num Sub-masks], [---], [Mean independently segmented regions per episode.],
    table.hline(),
  ),
  caption: [Evaluation metrics used throughout all experiments.],
) <tab:metrics>

== Baseline Methods

Three baselines are evaluated: centroid single-click (argmax of SAM logit map), random click (uniform random location selection), and top-$k$ similarity (select $k$ highest-logit positions).

== Oracle Policy

A brute-force greedy oracle evaluates all 1,369 grid positions at each step, testing both positive and negative clicks. Stopping criteria are: Dice $>= 0.95$, plateau ($< 0.005$ improvement over 3 clicks), or click cap (10). The oracle provides an upper bound on click placement quality.
