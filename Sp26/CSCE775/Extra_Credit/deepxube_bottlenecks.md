# DeepXube Training Pipeline Bottleneck Analysis

Benchmarked on RTX 6000 Ada Generation (48GB), 500 training iterations each.

## Benchmark Results

| # | Domain | Config | Batch | Procs | Wall Time |
|---|--------|--------|-------|-------|-----------|
| 1 | Grid 7x7 | V, resnet\_fc.100H\_2B | 100 | 1 | 17.6s |
| 2 | Grid 7x7 | QFix, resnet\_fc.100H\_2B | 100 | 1 | 17.0s |
| 3 | Cube3 | V, resnet\_fc.5000H\_4B | 100 | 1 | 58.9s |
| 4 | Cube3 | V, resnet\_fc.5000H\_4B | 1000 | 1 | 4m 3s |
| 5 | NPuzzle 4 | V, resnet\_fc.1000H\_4B | 100 | 1 | 18.7s |
| 6 | Cube3 | V, resnet\_fc.5000H\_4B | 100 | 4 | 55.9s |

Observations from benchmarks:

- Network size dominates. Cube3 with the 5000H\_4B network is 3.4x slower than Grid/NPuzzle with smaller networks.
- Batch size scaling is poor. Cube3 batch 100 to 1000 went from 59s to 4m3s (4.1x slower for 10x more data per batch), suggesting the bottleneck shifts to data generation/search, not GPU compute.
- Multi-process barely helps. 4 procs was only 5% faster than 1 proc for Cube3. Subprocess overhead and synchronization eat the gains.

## High-Ticket Optimization Items

### 1. Replace Synchronous Queue Architecture with Async Pipeline

Impact: Massive. Files: `base/trainer.py`, `base/updater.py`.

The entire training loop blocks waiting for data generation via `from_q.get()`. GPU sits idle while CPU generates data. Queue size is hardcoded to 1. There is no overlap between training and data generation.

The fix is an async double-buffered pipeline. Prefetch the next batch on CPU while training the current batch on GPU. Use `torch.utils.data.DataLoader` with `pin_memory=True` and `prefetch_factor`.

### 2. Replace DataParallel with DistributedDataParallel (DDP)

Impact: Massive. File: `base/trainer.py:211`.

Currently uses `nn.DataParallel`, which is single-machine only and inefficient (GIL bottleneck, one process gathers all gradients). Cannot scale beyond 1 node.

The fix is switching to `torch.nn.parallel.DistributedDataParallel` with `torch.distributed` backend (NCCL for GPU, Gloo for CPU). This enables multi-node, multi-GPU with proper gradient all-reduce.

### 3. Vectorize Pathfinding Inner Loops

Impact: High. File: `base/pathfinding.py:472-488`.

The core search step has nested Python loops creating Node objects one by one:

```python
for node_idx, node in enumerate(nodes):
    for c_idx in range(len(states_c_l[node_idx])):
        node_c = Node(...)  # Pure Python object creation
```

For large action spaces, this is the CPU bottleneck. The same issue exists in `domain.expand()` with while loops and list comprehensions.

The fix is to batch node expansion into tensor operations. Replace Python heapq with a batched priority queue (or use beam search with tensor sorting).

### 4. Fix Neural Network Inference Queuing

Impact: High. Files: `nnet/nnet_utils.py:186-199`, `base/updater.py:331-399`.

All updater processes share a single input queue (`nnet_i_q`) to the GPU runner. Each search iteration blocks waiting for heuristic evaluation. With multiple GPUs, there is no load balancing. It just replicates the model with no batching across GPUs.

The fix is using a batched inference server pattern. Accumulate requests from all workers, batch them, run inference on GPU, scatter results back. Alternatively, use TorchServe or Triton for inference during search.

### 5. Eliminate Shared Memory Copy Chain

Impact: High. Files: `utils/data_utils.py:95-158`, `nnet/nnet_utils.py:235-245`.

Every inference request goes through: numpy to SharedNDArray (copy) to pickle to queue to unpickle to numpy view to GPU copy. That is 3+ full copies of the data per inference call.

The fix is using CUDA shared memory or `torch.multiprocessing` with CUDA tensors directly. Pin memory with `torch.Tensor.pin_memory()` for async GPU transfer.

### 6. Add Continuous State Space Support

Impact: High for new domains. Files: `base/domain.py`, `base/nnet_input.py`.

The domain interface assumes discrete, hashable states (used as dict keys in `closed_dict`). Continuous states cannot be hashed. The one-hot encoding pipeline assumes categorical inputs.

The fix is adding a `ContinuousDomain` mixin with approximate nearest-neighbor for closed-set checking (LSH or k-d trees), continuous input normalization, and skipping one-hot encoding.

### 7. Replay Buffer Needs GPU Pinning and Smarter Sampling

Impact: Medium. File: `base/trainer.py:62-114`.

Buffer is CPU-only numpy with random indexing (cache-unfriendly). No pinned memory for GPU transfer. For large continuous states, memory is O(buffer\_size x state\_dim) with no compression.

The fix is pinning buffer memory, using `torch.utils.data.DataLoader` for prefetched sampling, and considering prioritized experience replay for sample efficiency.

### 8. GIL Contention Across Worker Processes

Impact: Medium. File: `nnet/nnet_utils.py:37-39`.

`torch.set_num_threads(1)` is only set in GPU runner processes. Updater processes (doing Python-heavy pathfinding) fight over the GIL with numpy/torch operations. Adding CPU cores gives diminishing returns, as the benchmark showed 4 procs was only 5% faster than 1.

The fix is setting `torch.set_num_threads(1)` in all worker processes. Consider moving pathfinding hot loops to C++/Cython, or use `torch.jit` for domain operations.

## Priority Order for Implementation

| Priority | Item | Effort | Speedup Potential |
|----------|------|--------|-------------------|
| 1 | Async pipeline + prefetch | Medium | 2-5x (eliminates GPU idle) |
| 2 | DDP multi-GPU | Medium | Linear with GPU count |
| 3 | Vectorize pathfinding | High | 3-10x on large action spaces |
| 4 | Batched inference server | Medium | 2-4x during search |
| 5 | Eliminate copy chain | Low | 1.5-2x on large states |
| 6 | Continuous domain support | High | Enables new domain class |
| 7 | Replay buffer improvements | Low | 1.2-1.5x |
| 8 | GIL fixes | Low | 1.3-2x with many cores |

Items 1 and 2 are the biggest bang-for-buck. The async pipeline alone would likely double throughput since the GPU is currently idle roughly 50% of the time waiting for data. DDP scales linearly with GPU count. Together they would enable full utilization of multi-GPU setups.
