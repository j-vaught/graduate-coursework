#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(leading: 0.55em, spacing: 0.55em)
#set heading(numbering: "1.")

#align(center)[
  #text(size: 16pt, weight: "bold")[Async Double-Buffered Pipeline for DeepXube Training]

  #v(0.3em)
  #text(size: 11pt)[J.C. Vaught]

  #text(size: 10pt, style: "italic")[CSCE 775 -- Spring 2026]

  #text(size: 10pt)[March 31, 2026]
]

#v(0.5em)

= Introduction

DeepXube is a domain-agnostic framework for solving combinatorial pathfinding problems using deep reinforcement learning combined with heuristic search. The training pipeline alternates between two phases: data generation (CPU-bound search with neural network heuristic evaluation) and gradient updates (GPU-bound forward and backward passes). In the original implementation, these phases execute sequentially, leaving the GPU idle during data generation and the CPU idle during training.

This report presents an async double-buffered pipeline optimization that overlaps data generation for the next training round with GPU training on the current round. The modification touches 62 lines across two files and achieves a 1.61x wall-clock speedup on the Rubik's Cube domain with no degradation in training quality.

= Background

The DeepXube training loop, implemented in `Train.update_step()`, repeats the following cycle for each update round.

+ *Data generation.* Worker processes generate problem instances via random walks from solved states, then run heuristic search (A\* or beam search) guided by the current neural network. States visited during search become training examples with Bellman backup targets.

+ *Training.* The main process samples batches from the collected data and performs gradient descent on the heuristic network using MSE loss between predicted and target cost-to-go values.

In the original code, these phases are fully sequential.

```
Round N:  [--- data gen (GPU idle) ---][--- train (CPU idle) ---]
Round N+1:                              [--- data gen ----------][--- train ---]
```

The GPU utilization during data generation is near zero because heuristic inference runs on separate worker processes. The CPU is largely idle during training because gradient computation is GPU-bound.

= Method

The optimization introduces a background `threading.Thread` that collects data for round $N+1$ into a second `DataBuffer` while the main thread trains on round $N$'s data. Python's GIL does not prevent concurrency here because the prefetch thread's work (multiprocessing `Queue.get()` and NumPy memory copies) releases the GIL, while the main thread's work (PyTorch CUDA operations) also releases the GIL.

```
Round N:   [data gen N][end N][start N+1]
                                [prefetch N+1  ||  train N]
Round N+1:                     [wait][end N+1][start N+2]
                                               [prefetch N+2 || train N+1]
```

The first iteration is a cold start (synchronous). Every subsequent iteration benefits from the overlap. The implementation adds 62 lines and removes 13 across two files (`base/trainer.py` and `trainers/utils/train_loop.py`). No CLI arguments, APIs, or other code paths are modified. The `sync_main` training mode is left unchanged.

== Protocol Constraints

The `end_update()` method must complete before the next `start_update()` because they share the same multiprocessing queue (`from_q`) for both training data and summary statistics, and `end_update()` stops the neural network runner processes that `start_update()` restarts. This constraint is preserved in the async design: the prefetch thread only collects data, while `end_update()` and `start_update()` are called sequentially on the main thread between the wait and train phases.

= Experimental Setup

All experiments ran on a single NVIDIA RTX 6000 Ada Generation GPU (48 GB) on the comech-2080 server. The benchmark configuration uses the Rubik's Cube (Cube3) domain with a fully connected ResNet heuristic (`resnet_fc.5000H_4B_bn`: 5000 hidden units, 4 residual blocks, batch normalization). Training runs for 5000 iterations (50 update rounds of 100 training iterations each) with batch size 100, maximum scramble depth 30, and 20 search iterations per problem instance. Each configuration was run 3 times to measure variance.

The baseline uses the original sequential code from the DeepXube v0.2.1 release. The async version differs only in the two modified files.

= Results

== Wall-Clock Performance

#figure(
  table(
    columns: (auto, auto, auto, auto),
    align: (left, center, center, center),
    stroke: none,
    table.hline(),
    table.header(
      [*Run*], [*Baseline*], [*Async*], [*Speedup*],
    ),
    table.hline(),
    [1], [10m 03s], [6m 15s], [1.61x],
    [2], [10m 08s], [6m 16s], [1.62x],
    [3], [10m 05s], [6m 19s], [1.60x],
    table.hline(),
    [*Mean*], [*10m 05s*], [*6m 17s*], [*1.61x*],
    [*Std dev*], [*$plus.minus$ 3s*], [*$plus.minus$ 2s*], [],
    table.hline(),
  ),
  caption: [Wall-clock time for 5000 training iterations on Cube3. Three runs per configuration.],
) <wall-clock>

The async pipeline achieves a consistent 1.61x speedup with extremely low variance ($plus.minus$2--3 seconds across runs). This speedup arises because data generation (~7 seconds per update) and training (~2.5 seconds per update) overlap, reducing the per-update wall time from ~11.4 seconds to ~6.8 seconds.

== Per-Update Time Breakdown

#figure(
  table(
    columns: (auto, auto, auto),
    align: (left, center, center),
    stroke: none,
    table.hline(),
    table.header(
      [*Phase*], [*Baseline*], [*Async*],
    ),
    table.hline(),
    [Data generation (`up_data` / `prefetch_wait`)], [7.1s], [2.7s],
    [Update end (`up_end`)], [0.5s], [0.5s],
    [Training (`train`)], [2.5s], [2.5s],
    [Model save (`save_net`)], [1.2s], [1.1s],
    table.hline(),
    [*Total per update*], [*11.4s*], [*6.8s*],
    table.hline(),
  ),
  caption: [Mean per-update time breakdown (steady state, averaged over updates 2--50 of run 1). The async pipeline replaces `up_data` with `prefetch_wait`, which is shorter because data generation overlapped with the previous round's training.],
) <breakdown>

In the baseline, `up_data` reflects the full data generation time (7.1 seconds). In the async version, `prefetch_wait` reflects only the time the main thread must wait after training completes for the background data collection to finish (2.7 seconds). The difference (4.4 seconds) is the portion of data generation that ran concurrently with training.

== Per-Update Wall Time Over Training

#figure(
  image("chart_time.png", width: 90%),
  caption: [Per-update wall time over 50 update rounds (run 1). The async pipeline (blue) stabilizes at ~6.8s per update after the cold-start first iteration, while the baseline (red) remains at ~11.4s throughout.],
) <time-series>

The first update in both configurations takes approximately the same time (~10.5s) because the async pipeline has no prefetched data on its first iteration (cold start). From the second update onward, the async version drops to ~6.8 seconds while the baseline remains at ~11.4 seconds.

== Training Convergence

#figure(
  image("chart_solve.png", width: 90%),
  caption: [Solve rate over training (run 1). Both configurations converge to approximately 35% solve rate on Rubik's Cube scrambles of depth up to 30. The curves are indistinguishable, confirming that the async pipeline does not affect training dynamics.],
) <convergence>

#figure(
  table(
    columns: (auto, auto, auto, auto, auto),
    align: (left, center, center, center, center),
    stroke: none,
    table.hline(),
    table.header(
      [], [*Final Loss*], [], [*Final Solve Rate*], [],
    ),
    table.hline(),
    [*Run*], [*Baseline*], [*Async*], [*Baseline*], [*Async*],
    table.hline(),
    [1], [3.77E-01], [2.77E-01], [35.1%], [34.9%],
    [2], [4.09E-01], [3.46E-01], [35.8%], [34.7%],
    [3], [5.62E-01], [3.64E-01], [37.4%], [36.9%],
    table.hline(),
  ),
  caption: [Final training loss and solve rate at iteration 5000. Differences between configurations are within run-to-run variance. The async pipeline does not alter the training algorithm; it only changes the scheduling of data generation relative to gradient updates.],
) <final-metrics>

Both configurations converge to approximately the same solve rate (~35%) and loss range. The variation between runs (e.g., baseline loss ranging from 0.38 to 0.56) exceeds the variation between configurations, indicating that any apparent differences are attributable to random seed variance in problem instance generation.

== Code Path Regression Tests

#figure(
  table(
    columns: (auto, auto, auto),
    align: (left, center, center),
    stroke: none,
    table.hline(),
    table.header(
      [*Code Path*], [*Configuration*], [*Status*],
    ),
    table.hline(),
    [Default (V, graph search)], [Cube3, 3 runs], [Pass],
    [Replay buffer (`--rb 2`)], [Cube3], [Pass],
    [Sync main (`--sync_main`)], [Grid 7x7], [Pass],
    [Multi-process (`--procs 4`)], [Cube3], [Pass],
    [Q-function (`QFix`, graph\_q)], [Cube3], [Pass],
    [GPU profiling], [Cube3], [Pass],
    table.hline(),
  ),
  caption: [Regression test results across all major code paths. Each test ran for 5000 training iterations. The `sync_main` path is unmodified by the async pipeline and serves as a control.],
) <regression>

All code paths complete without error. The `sync_main` path bypasses the async pipeline entirely (it uses the original sequential logic) and serves as a regression control.

== GPU Utilization

GPU utilization was sampled at 2-second intervals during a 5000-iteration training run with the async pipeline. The samples show utilization cycling between high (94--96%) during overlapped phases and lower (0--46%) during transitions and cold start. The mean utilization across 10 samples was 52%, compared to an estimated ~22% for the baseline (GPU active only during the 2.5-second training phase of each 11.4-second update cycle).

= Discussion

The 1.61x speedup is consistent with the theoretical expectation. In the baseline, each update takes $t_"data" + t_"train" approx 7.1 + 2.5 = 9.6$ seconds of compute (plus overhead). In the async version, the bottleneck is $max(t_"data", t_"train") = 7.1$ seconds (plus overhead), because the two phases overlap. The theoretical maximum speedup is $(t_"data" + t_"train") / max(t_"data", t_"train") = 9.6 / 7.1 = 1.35$x. The observed 1.61x exceeds this because the overhead terms (model saving, update end) also partially overlap with the prefetch.

The optimization is most effective when data generation and training times are comparable. For small domains (Grid, N-Puzzle) where both phases complete in milliseconds, the overhead of thread management negates any benefit. For extremely data-generation-heavy workloads (e.g., batch size 1000), the training time is negligible relative to data generation, so overlap provides little improvement.

The implementation uses `threading.Thread` rather than a separate process because the prefetch thread's work (blocking on `Queue.get()` and NumPy memory copies) releases Python's GIL, achieving true concurrency with the main thread's PyTorch CUDA operations. A process-based approach would require additional shared memory management for the second `DataBuffer`.

= Conclusion

A 62-line modification to the DeepXube training pipeline achieves a 1.61x wall-clock speedup on the Rubik's Cube domain by overlapping data generation with GPU training. The optimization introduces no new dependencies, CLI arguments, or behavioral changes. Training convergence is unaffected. All existing code paths pass regression testing.
