# DeepXube Training Pipeline — Bottleneck Analysis & Optimization Plan

## Architecture Overview

The system implements a self-play-style training loop where heuristic/policy neural networks are trained by generating data through heuristic search (A\*, beam search) and performing Bellman or tree backups. The pipeline has three layers: data generation (CPU workers), neural network inference (GPU), and training (GPU).

---

## Bottlenecks

### 1. Single-GPU Training (Highest Impact)

- Uses `nn.DataParallel`, the slow, old-school multi-GPU approach with Python GIL contention in scatter/gather.
- No `DistributedDataParallel` (DDP) support. No `torchrun`, no `torch.distributed.init_process_group`, no rank handling, no `DistributedSampler`.
- `get_device()` in `nnet_utils.py:29` hard-codes `device = torch.device("cuda:0")`.
- On an 8xA100 node, 7 GPUs sit idle unless DataParallel is enabled, and even then GPU 0 is the bottleneck due to asymmetric memory loading.
- Multi-node training is impossible. The multiprocessing context uses `spawn` with POSIX shared memory and Python `Queue` objects, which do not cross machine boundaries.

**Key files:** `nnet/nnet_utils.py`, `base/trainer.py`

### 2. No Mixed Precision

- No `torch.cuda.amp.autocast`, no `GradScaler`, no `torch.compile`.
- All forward and backward passes run in FP32.
- A100 and H200 tensor cores provide 2-8x throughput for BF16/FP16 matrix multiplications. This is left entirely on the table.

**Key files:** `trainers/utils/train_utils.py` (`train_heur_nnet_step`, `train_policy_nnet_step`)

### 3. Serialized Inference Bottleneck

- `start_nnet_fn_runners` in `nnet_utils.py:178` starts exactly one inference process per entry in `CUDA_VISIBLE_DEVICES`.
- All CPU worker processes share a single `nnet_i_q` queue. Each worker puts inputs onto the queue and blocks on its personal `nnet_o_q`.
- Only one neural network evaluation executes at a time per GPU, regardless of how many CPU workers exist.
- With `--procs 32` and 1 GPU, 32 workers fight over 1 inference slot.
- No request batching across workers. The nnet runner services one request at a time.

**Key files:** `nnet/nnet_utils.py` (`nnet_fn_runner`, `start_nnet_fn_runners`)

### 4. nnet Runners Respawned Every Update Cycle

- `start_nnet_runners` and `stop_nnet_runners` are called inside `start_update` and `end_update` in the updater base class.
- The inference process is torn down and respawned on every update round.
- Each restart incurs process spawn overhead, model deserialization, and CUDA context initialization (several seconds per cycle).

**Key files:** `base/updater.py` (`start_update`, `end_update`)

### 5. No Async Data Loading

- `DataBuffer.sample()` in `base/trainer.py` uses `np.random.randint` and indexes NumPy arrays on the main process.
- No prefetch workers, no `pin_memory` tensors, no asynchronous host-to-device transfers.
- The training loop is fully synchronous: CPU stalls waiting for GPU to complete before issuing the next batch transfer.
- No overlapping of data loading with computation.

**Key files:** `base/trainer.py` (`DataBuffer.sample`, `_train`)

### 6. CPU-Side Inefficiencies in Search

- `get_all_descendants()` in `base/pathfinding.py:87` uses `list.pop(0)`, which is O(n) per pop, making the BFS O(n^2) for deep trees.
- Node expansion in `PathFindNode._expand` is a nested Python for-loop over states. No NumPy or Cython vectorization.
- Closed-set lookup in `graph_search.py:85` uses Python `dict.get()` per node. Cache-unfriendly for large open sets.
- Beam selection converts lists to arrays and back wastefully.

**Key files:** `base/pathfinding.py`, `pathfinding/graph_search.py`, `pathfinding/beam_search.py`

---

## Optimization Plan

### Priority 1 — Replace DataParallel with DDP

Wrap the training step in `torch.distributed` using `torchrun`. Replace `nn.DataParallel` with `nn.parallel.DistributedDataParallel`. On 8xA100 this alone gives near-linear scaling for the backward pass via NCCL all-reduce instead of scatter/gather. The `DataBuffer` per-rank can be smaller and the worker count divided by world size.

- **Expected speedup:** ~linear with GPU count (e.g., ~8x on 8-GPU node)
- **Effort:** Medium

### Priority 2 — Add BF16 Mixed Precision (AMP)

Wrap the forward pass in `train_heur_nnet_step` and `train_policy_nnet_step` with `torch.autocast(device_type='cuda', dtype=torch.bfloat16)` and add `torch.amp.GradScaler`. On A100/H200 with BF16 tensor cores, throughput for the ResNet FC layers roughly doubles with no stability loss since BF16 has the same exponent range as FP32.

- **Expected speedup:** ~2x training throughput
- **Effort:** Easy (< 20 lines changed)

### Priority 3 — Batched Inference Server per GPU

Replace the serialized single-request inference queue with a micro-batching server. Each GPU hosts a server process that accumulates requests from multiple CPU workers within a short timeout window (e.g., 5ms), stacks them into one batch, runs the forward pass, and fans out results. This turns N sequential RPC calls into one batched forward pass.

- **Expected speedup:** ~3-5x search throughput
- **Effort:** Medium

### Priority 4 — Keep nnet Runners Alive Across Updates

Move `start_nnet_runners` out of `start_update` and `stop_nnet_runners` out of `end_update`. Spawn them once at training start and keep them alive for the full run. Eliminates several seconds of process spawn + model reload overhead per update cycle.

- **Expected speedup:** Removes constant overhead per update
- **Effort:** Easy

### Priority 5 — Pin Memory and Async GPU Transfers

Convert `DataBuffer` to store pinned-memory tensors or pre-allocate a pinned buffer. Use `tensor.to(device, non_blocking=True)` and overlap next-batch sampling with the current backward pass via double buffering. Fully hides PCIe transfer latency.

- **Expected speedup:** Hides transfer latency entirely
- **Effort:** Easy

### Priority 6 — Fix O(n^2) BFS in HER

Replace `fifo.pop(0)` in `get_all_descendants` with `collections.deque` and `popleft()`, which is O(1). Changes BFS from O(n^2) to O(n).

- **Expected speedup:** Significant for deep search trees
- **Effort:** Trivial (1-line change)

### Priority 7 — torch.compile for Single-GPU

If only one GPU is used, `torch.compile(nnet, mode="reduce-overhead")` with BF16 AMP gives 20-40% speedup on repeated fixed-shape batches by fusing operations and eliminating Python dispatch overhead.

- **Expected speedup:** 20-40% single-GPU
- **Effort:** Easy

---

## Summary Table

| Component | Current State | Bottleneck Type | Fix | Impact | Effort |
|---|---|---|---|---|---|
| Multi-GPU training | `DataParallel` / single GPU | GPU utilization | DDP with `torchrun` | ~8x on 8-GPU | Medium |
| Precision | FP32 throughout | Tensor core waste | BF16 AMP + GradScaler | ~2x throughput | Easy |
| Inference during search | Single shared queue per GPU | Serialized IPC | Batching inference server | ~3-5x search | Medium |
| nnet runner lifecycle | Respawned every update | Process spawn overhead | Keep alive across updates | Removes overhead | Easy |
| Data loading | Synchronous NumPy + CPU→GPU | Transfer latency | Pin memory + non-blocking | Hides latency | Easy |
| HER BFS | O(n^2) `list.pop(0)` | CPU | `collections.deque` | Fixes quadratic | Trivial |
| Single-GPU compile | No JIT compilation | Python dispatch | `torch.compile` | 20-40% | Easy |
| Multi-node | Not supported | Architecture gap | NCCL + dist init | Enables scaling | Hard |

The three highest-leverage items for HPC with A100s/H200s are DDP, BF16 AMP, and replacing the serialized inference queue with a batching server. Together these should yield 5-15x wall-clock speedup.
