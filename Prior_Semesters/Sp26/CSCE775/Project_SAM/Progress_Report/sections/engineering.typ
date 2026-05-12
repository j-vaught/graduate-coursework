= Engineering Infrastructure <sec:engineering>

== Computational Pipeline <sec:compute>

DINOv2 ViT-L/14 @oquab2024dinov2 features are extracted once per image
and written to disk, eliminating redundant forward passes across oracle
generation, warmstart, and RL training. Images are resized to $518 times 518$
pixels---the smallest resolution whose side length is an exact multiple of the
$14$-pixel patch size---yielding a $37 times 37$ spatial grid. Each grid
position carries a $1,024$-dimensional descriptor, giving $1,369$ tokens
per image. For reference images, only patches whose ground-truth mask value
exceeds $0.5$ are retained, producing a variable-length foreground feature
sequence. All extracted features are serialized to `oracle_dino_cache.pt`
and memory-mapped at runtime so that multiple concurrent processes can read
from a single file without redundant I/O.

Ground-truth oracle trajectories are produced by brute-force search over the
DINOv2 grid. At each step, every candidate click is enumerated: $1,369$
grid positions $times$ 2 click types (positive / negative) yields $2,738$
candidates per decision step. SAM forward passes are batched in groups of
eight to saturate GPU throughput while keeping peak memory bounded. An
_autoclaim_ mode locks each episode to a dedicated process, preventing
mask interference when multiple instances generate data simultaneously.
Debug visual panels---showing the current mask, the candidate click heatmap,
and the selected click---are written to disk at configurable intervals for
offline inspection.

The frozen SAM ViT-H backbone @kirillov2023sam serves as the
segmentation oracle throughout all three paradigms. Image embeddings are
computed once per episode and reused for every click within that episode.
Click application follows an _incremental_ protocol: the dense logit map
from the previous step is passed as `mask_input` to the prompt encoder,
allowing the decoder to exploit accumulated evidence without reprocessing the
image. On the first click of a new sub-mask (or the first click of the
episode in V1), `multimask_output=True` is set and SAM produces three
candidate masks; the hypothesis with the highest predicted IoU is selected.
All subsequent clicks within the same sub-mask use single-mask output conditioned
on the inherited logit prior. Grid coordinates are mapped to image-space
click coordinates via $((x + 0.5) / 37) times W$, ensuring clicks
land at patch centers.

Two lightweight mock backends support rapid development and continuous
integration without GPU hardware or model weights. The mock DINOv2 encoder
downsamples the input image to $37 times 37$ and interprets the rescaled
pixel values as $1,024$-dimensional features by tiling the three color
channels. The mock SAM backend places a Gaussian bump ($sigma = 18$ pixels)
centered at the supplied click coordinate on a $256 times 256$ logit map
and accumulates bumps across clicks with appropriate sign for positive and
negative labels. Together these mocks enable full pipeline traversal---feature
lookup, environment steps, policy inference, reward computation---in seconds on
a CPU. Progressive smoke tests (`smoke_r5.py`, `smoke_r6.py`,
`smoke_r8.py`) validate each revision's end-to-end wiring against the
mock backends before any GPU run is attempted.

The Qwen3-VL-8B-Instruct model @bai2025qwen25vl runs on a local GPU
and requires approximately two seconds per inference call. Each action step
invokes the model three times in sequence: a _choose_ call selects the
next click coordinate, a _verify_ call checks the proposed action against
the current mask state, and a _review_ call resolves any discrepancy between
the two. The three-call overhead sums to roughly six seconds per action step,
which is acceptable given the VLM's substantially higher Dice efficiency
(@sec:results). Visual state is rendered as a four-panel PIL
composite---reference image with mask overlay, query image, current predicted
mask, and a click history overlay---and passed directly to the VLM as an inline
image.

== Storage and GPU Management <sec:storage_gpu>

All training runs query the free space on the primary SSD before writing any
artifacts. When free space falls below a 100 GB threshold, the run manager
automatically redirects checkpoints, CSV logs, and episode caches to a
secondary HDD overflow directory. The resolution order is: (1) preferred
run directory on the primary SSD, (2) overflow directory on the HDD, (3) a
fallback path at `/mnt/storage/${USER}/${name}`. The helper
`select_run_dir()` returns a three-tuple of `(path, is_overflow,
free_gb)` so callers can log which storage tier was selected.

The function `assert_gpu_is_free()` queries `nvidia-smi` for
current memory usage and raises an exception if any visible device exceeds a
configurable threshold (default: 1,024 MB already allocated). The check
respects the `CUDA_VISIBLE_DEVICES` environment variable, so
multi-user machines can designate reserved devices without modifying launch
scripts. This guard prevents training runs from silently absorbing a fragmented
GPU and crashing with an out-of-memory error hours into a run.

PPO and GRPO trainers maintain two checkpoint slots: _latest_ (overwritten
every save interval) and _best_ (retained when evaluation Dice improves).
The behavioral cloning warmstart additionally writes a _final_ snapshot at
the end of the last epoch. PPO checkpoints include full optimizer state,
enabling seamless mid-run resumption without gradient-history discontinuities.
Evaluation runs can specify an independent `eval_checkpoint_path` that
overrides the active training checkpoint, allowing retrospective scoring of any
saved snapshot.

Metrics are written to per-run CSV files: `warmstart_metrics.csv`,
`ppo_eval_metrics.csv`, `grpo_eval_metrics.csv`, and
`submask_ppo_eval_metrics.csv`. Per-update rows record Dice, mean
clicks, number of sub-masks, entropy, and all loss components (policy loss,
value loss, entropy bonus, KL penalty). V3 VLM runs write per-step JSON logs
capturing the action choice, chain-of-thought reasoning, raw coordinates, and
resulting Dice, enabling post-hoc analysis of failure modes without replaying
the full episode.

== Development Timeline <sec:timeline>

The entire project spans approximately one month, from repository initialization
on February 27 through the submission of this report on March 28, 2026, with
118 commits across the main, CODEX, and `j-vaught` branches.
@tab:timeline summarizes the major milestones.

#figure(
  table(
    columns: 2,
    table.hline(),
    [*Period*], [*Activity*],
    table.hline(),
    [Feb 27--28],  [Repository setup; baseline environment and evaluation harness],
    [Feb 28--Mar 2], [Q-learning era: Steps 1--10, NaN debugging, reward shaping attempts],
    [Mar 3],       [Q-learning abandoned; clean-slate redesign],
    [Mar 4],       [V1 implemented: PolicyTransformer, PPO trainer, BC warmstart, eval loop],
    [Mar 4],       [Oracle generation pipeline; warmstart training; first PPO fine-tuning run],
    [Mar 4],       [Multiple PPO hyperparameter sweeps (learning rate, entropy, clipping)],
    [Mar 9],       [CODEX branch: advanced training strategies, smoke-test infrastructure],
    [Mar 10--12],  [Oracle generation infrastructure hardened; DINOv2 precomputation cache],
    [Mar 19],      [V2: SubMaskPolicyTransformer, GRPO trainer, SubMask PPO environment],
    [Mar 20],      [Browser-based interactive mask refinement tool],
    [Mar 23],      [V3: VLM pipeline, GRPO trainer refinements; all branches merged],
    [Mar 28],      [Progress report],
    table.hline(),
  ),
  caption: [Condensed development timeline (Feb 27 -- Mar 28, 2026).],
) <tab:timeline>
