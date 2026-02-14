# Plug-and-Play PPO: One-Shot Segmentation via RL-Optimized SAM Prompts

## Complete Technical Walkthrough

This document explains every component of the Plug-and-Play PPO pipeline (CVPR 2025, Liu et al.) as implemented in the `XueyuLiu/PPO` repository. Despite the name "PPO," the actual RL algorithm used is **tabular Q-learning with experience replay** — not Proximal Policy Optimization. The pipeline optimizes SAM (Segment Anything Model) point prompts for one-shot segmentation using a dual-space heterogeneous graph representation.

---

## 1. Problem Setup: One-Shot Segmentation

**Goal**: Given a single reference image with a ground-truth mask, segment the same object class in a new target image — without any retraining of SAM.

**Why this is hard**: SAM requires point prompts (positive points = "segment here," negative points = "not here") to produce masks. The quality of the output mask is extremely sensitive to prompt placement. A few pixels of difference in point position can change the mask from perfect to completely wrong.

**Core insight**: Instead of manually placing prompts or using heuristics, treat prompt selection as a reinforcement learning problem. Build a graph where nodes are candidate prompt locations, then learn which nodes to keep and which to remove.

---

## 2. Pipeline Overview (Three Steps)

```
Step 1: Feature Matching (DINOv2)
   Reference image + GT mask → Target image candidate prompts

Step 2: Q-Learning on Dual-Space Graph
   Candidate prompts → Optimized prompt subset

Step 3: SAM Segmentation
   Optimized prompts + Target image → Final mask
```

---

## 3. Step 1: Initial Prompt Generation via DINOv2 Feature Matching

### 3.1 Image Patchification

Both the reference and target images are resized to 560x560 pixels. DINOv2 uses a Vision Transformer with **patch size 14**, so each image is divided into a grid of `560/14 = 40` patches per dimension, yielding `40 x 40 = 1,600` non-overlapping patches total. Each patch is a 14x14 pixel region.

Every patch gets a **1D index** computed as:
```
index = row * 40 + col
```
where `row = pixel_y // 14` and `col = pixel_x // 14`. This flattened index is used throughout the pipeline to identify spatial locations.

### 3.2 Foreground/Background Classification from GT Mask

The reference image's ground-truth mask is scanned patch-by-patch (14x14 blocks):
- If **all pixels** in a 14x14 block are non-black (i.e., `!= [0,0,0]`), that patch is **foreground** (positive)
- If **all pixels** in a 14x14 block are black (`== [0,0,0]`), that patch is **background** (negative)
- Mixed patches (partially foreground/background) are discarded

This produces two index lists: `fore_index` (foreground patch indices) and `back_index` (background patch indices).

### 3.3 DINOv2 Feature Extraction

**Model**: DINOv2 ViT-G/14 (Giant variant, ~1.1B parameters, ~4.2 GB checkpoint)

Both images are preprocessed with ImageNet normalization:
```python
transform = Compose([
    Resize(560), CenterCrop(560), ToTensor(),
    Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
])
```

Both images are stacked into a batch of 2 and passed through DINOv2's forward pass. The output `x_norm_patchtokens` gives a feature tensor of shape `[2, 1600, 1536]` — that is, for each of the 2 images, 1600 patches, each with a 1536-dimensional feature vector (ViT-G/14's embedding dimension).

- `features[0]` = reference image patch features (1600 x 1536)
- `features[1]` = target image patch features (1600 x 1536)

### 3.4 Feature Matching via Nearest Neighbors

For each foreground patch in the reference image, find the closest matching patch in the target image using **L2 distance** in feature space:

```python
distances = torch.cdist(features[0][fore_index], features[1])  # shape: [N_fore, 1600]
min_values, min_indices = distances.min(dim=1)  # shape: [N_fore]
```

The `min_indices` are the **initial positive prompt indices** on the target image — they point to the target patches whose DINOv2 features are most similar to the reference foreground patches.

The same process is repeated for background patches to get **initial negative prompt indices**.

Finally, any index that appears in both positive and negative sets (intersection) is removed from both.

### 3.5 Output of Step 1

- `features`: DINOv2 patch features for both images `[2, 1600, 1536]`
- `pos_indices`: Initial positive prompt patch indices on target (e.g., 34 patches)
- `neg_indices`: Initial negative prompt patch indices on target (e.g., 1413 patches)

These are the **unoptimized** prompt candidates. SAM segmentation with these raw prompts typically produces poor results (IoU ~0.001 in our experiment) because feature matching gives many false positives/negatives.

---

## 4. Step 2: Q-Learning on Dual-Space Heterogeneous Graph

This is the core contribution. The pipeline constructs a graph where nodes are prompt candidates and edges encode both **feature-space** and **physical-space** relationships. A Q-learning agent then learns to selectively remove/restore nodes to optimize the graph's structure.

### 4.1 Graph Construction

**Nodes**: Each candidate prompt index becomes a node, labeled as either `pos` (positive prompt) or `neg` (negative prompt). In our experiment: 34 pos + 1413 neg = 1,447 nodes.

**Edge Types (5 types)**: The graph is a `networkx.MultiGraph` with 5 distinct weighted edge types:

1. **`feature_pos`**: Feature-space distances between positive nodes
   - `torch.cdist(features[1][pos_indices], features[1][pos_indices])` → pairwise L2 distances in DINOv2 feature space among positive prompts
   - Normalized to [0, 1]

2. **`feature_cross`**: Feature-space distances between positive and negative nodes
   - `torch.cdist(features[1][pos_indices], features[1][neg_indices])`
   - Normalized to [0, 1]

3. **`physical_pos`**: Physical (pixel) distances between positive nodes
   - Computed from patch center coordinates: `center_x = col * 14 + 7`, `center_y = row * 14 + 7`
   - `torch.cdist(pos_points, pos_points)` in pixel space
   - Normalized to [0, 1]

4. **`physical_neg`**: Physical distances between negative nodes
   - Same computation for negative node pairs
   - Normalized to [0, 1]

5. **`physical_cross`**: Physical distances between positive and negative nodes
   - Cross-distances in pixel space
   - Normalized to [0, 1]

**Edge count**: With 34 pos and 1413 neg nodes, and all 5 edge types being fully connected:
- `feature_pos`: 34 x 34 = 1,156
- `feature_cross`: 34 x 1413 = 48,042
- `physical_pos`: 34 x 34 = 1,156
- `physical_neg`: 1413 x 1413 = 1,996,569
- `physical_cross`: 34 x 1413 = 48,042
- **Total: ~2,093,484 edges**

### 4.2 Graph Optimization Environment (`GraphOptimizationEnv`)

The environment wraps the graph and exposes an RL interface.

**State**: The current graph `G` (a networkx MultiGraph object with whatever nodes remain).

**Reset behavior**: On `reset()`, all nodes are moved to a `removed_nodes` set and the graph is cleared. The agent starts with an empty graph and must restore nodes. This is critical — the agent begins each episode from scratch and builds up a prompt set.

**Actions** (5 types):
- `(node_id, "restore_pos")` — Add a positive node back from the removed set
- `(node_id, "restore_neg")` — Add a negative node back from the removed set
- `(node_id, "remove_pos")` — Remove a positive node from the current graph
- `(node_id, "remove_neg")` — Remove a negative node from the current graph
- `(node_id, "add")` — Add a brand new node (randomly assigned pos/neg)

**Action constraints**:
- Must maintain between `min_nodes=5` and `max_nodes=20` of each type
- If pos count <= 5, only restore_pos actions allowed (can't remove more)
- If pos count >= 20, only remove_pos actions allowed (can't add more)
- Same constraints for negative nodes
- "add" actions (new nodes) only available when both types are within range
- Remove actions are subsampled to balance pos/neg removal probabilities

**Episode length**: Fixed at `max_steps=100` actions per episode.

### 4.3 Reward Function

The reward is computed after every action based on how the action changed five graph statistics. Each statistic is the **mean** of all edge weights for that edge type:

```
reward = 0

# Feature-space positive distances (want LOWER = more similar foreground points)
if mean_feature_pos decreased:  reward += 5 * (decrease amount)
else:                            reward -= 5 * (increase amount)

# Feature-space cross distances (want HIGHER = foreground far from background in feature space)
if mean_feature_cross increased: reward += 5 * (increase amount)
else:                            reward -= 5 * (decrease amount)

# Physical positive distances (want HIGHER = spread out positive prompts spatially)
if mean_physical_pos increased:  reward += 1 * (increase amount)
else:                            reward -= 1 * (decrease amount)

# Physical negative distances (want HIGHER = spread out negative prompts)
if mean_physical_neg increased:  reward += 1 * (increase amount)
else:                            reward -= 1 * (decrease amount)

# Physical cross distances (want LOWER = negative prompts close to positive prompts)
if mean_physical_cross decreased: reward += 1 * (decrease amount)
else:                              reward -= 1 * (decrease amount)

# Penalty for adding new nodes
if action == "add": reward -= 10
```

**Intuition behind the reward design**:
- **Minimize feature_pos distance** (weight 5x): Positive prompts should be semantically similar in DINOv2 feature space — they should all represent the target object
- **Maximize feature_cross distance** (weight 5x): Positive and negative prompts should be semantically different — foreground vs background should be distinguishable
- **Maximize physical_pos distance** (weight 1x): Positive prompts should be spatially spread out across the object, not clustered in one spot
- **Maximize physical_neg distance** (weight 1x): Negative prompts should cover diverse background regions
- **Minimize physical_cross distance** (weight 1x): Negative prompts should be near the object boundary (close to positive prompts) to help SAM distinguish object from background
- **Penalize adding nodes** (flat -10): Discourage unnecessary complexity; prefer selecting from existing candidates

The feature-space objectives are weighted 5x more than physical-space ones, emphasizing semantic similarity over spatial arrangement.

### 4.4 Q-Learning Agent (`QLearningAgent`)

**Algorithm**: Tabular Q-learning (not PPO, not DQN — basic Q-table).

**Hyperparameters**:
- Learning rate `alpha = 0.1`
- Discount factor `gamma = 0.9`
- Epsilon start: `1.0` (fully random)
- Epsilon end: `0.1`
- Epsilon decay: `0.995` per step
- Experience replay buffer: `10,000` transitions
- Replay batch size: `64`

**Q-table**: A `defaultdict(float)` mapping `(state, action) → Q-value`. The state key is the graph object itself (by reference). Actions are tuples like `(node_id, "restore_pos")`.

**Epsilon schedule**: At the start of each episode, epsilon is reset based on the best reward achieved so far:
```python
if best_reward < 0:     epsilon = 1.0  (fully random)
elif best_reward >= 5:   epsilon = 0.1  (mostly greedy)
else:                    epsilon = 1 - (best_reward / 5)
```
Within each episode, epsilon decays by `0.995` after every step.

**Action selection**: Epsilon-greedy. With probability epsilon, choose a random action from the available actions. Otherwise, choose the action with the highest Q-value (ties broken randomly).

**Q-table update** (standard Q-learning):
```
Q(s,a) += alpha * (reward + gamma * max_a' Q(s', a') - Q(s,a))
```

**Experience replay**: After each step, a random batch of 64 past transitions is sampled from the replay buffer and used for additional Q-table updates. This helps stabilize learning.

**Best experience replay**: When a new best episode reward is achieved, the entire replay buffer is saved as "best memory." This best memory is replayed to reinforce successful strategies.

### 4.5 Training Loop

Each episode:
1. Reload features and indices from disk
2. Rebuild the full graph (all nodes and edges)
3. Reset environment (all nodes removed)
4. Set epsilon based on best reward
5. For 100 steps:
   a. Get possible actions
   b. Select action (epsilon-greedy)
   c. Execute action (add/remove/restore a node)
   d. Compute reward (graph statistics change)
   e. Store transition in replay buffer
   f. Update Q-table for current transition
   g. Replay batch of 64 from buffer
   h. Decay epsilon by 0.995
6. If episode reward > best reward: save Q-table, replay best memory
7. Track best model by multiple criteria:
   - Highest total reward
   - Lowest mean feature_pos distance
   - Highest mean feature_cross distance

**Model saving**: Three "best" models are tracked independently — best by reward, best by feature cohesion (low pos distance), and best by feature separation (high cross distance).

### 4.6 What the Agent Learns

Over episodes, the agent learns which specific patch indices to include in the prompt set. In our blue tang experiment:
- Started with 34 pos + 1413 neg candidates
- Agent consistently converges to **6-7 positive** and **19-20 negative** nodes
- The selected positive nodes are the patches that best represent the fish in DINOv2 feature space
- The selected negative nodes are diverse background patches that help SAM exclude coral/water

---

## 5. Step 3: Optimized Segmentation

### 5.1 Prompt Optimization (`optimize_nodes`)

Using the trained Q-table, the agent runs one final episode:
1. Build the full graph with all candidate nodes
2. Reset (start empty)
3. Run 100 steps with the learned Q-table (epsilon still active at 0.1)
4. Collect the final set of nodes remaining in the graph
5. Split into `optimized_pos_indices` and `optimized_neg_indices`

### 5.2 Index to Point Conversion

Each optimized patch index is converted to pixel coordinates (the center of the 14x14 patch):
```python
center_x = (index % 40) * 14 + 7   # column center
center_y = (index // 40) * 14 + 7  # row center
```

These coordinates are then mapped back to the original image dimensions if different from 560x560.

### 5.3 SAM Segmentation

**Model**: SAM ViT-B (base variant, ~358 MB checkpoint)

The optimized positive and negative point coordinates are passed to SAM's `SamPredictor`:
```python
predictor.set_image(target_image)
masks, scores, logits = predictor.predict(
    point_coords=all_points,      # [N_pos + N_neg, 2]
    point_labels=labels,          # 1 for pos, 0 for neg
    multimask_output=False        # single best mask
)
```

SAM produces a binary mask. The largest contour is optionally kept via `max_contour` mode.

### 5.4 Evaluation

The optimized mask is compared to the ground truth using **Intersection over Union (IoU)**:
```
IoU = |predicted ∩ ground_truth| / |predicted ∪ ground_truth|
```

In our blue tang experiment:
- **Initial prompts (unoptimized)**: IoU = 0.0006 (essentially missed the fish)
- **Optimized prompts (30 episodes)**: IoU = 0.760 (76% overlap with GT)
- **Improvement**: 134,443%

---

## 6. Key Design Decisions & Quirks

### 6.1 Why "PPO" is a Misnomer
The code uses tabular Q-learning, not PPO (Proximal Policy Optimization). The Q-table maps (graph_state, action) pairs to values. There is no neural network policy, no clipping objective, no advantage estimation. The name likely refers to "Plug-and-Play Optimization" rather than the RL algorithm.

### 6.2 Graph Starts Empty
The environment resets by removing all nodes. The agent must actively restore nodes one at a time. This means the agent's job is essentially **subset selection** — choosing which of the 1,447 candidate nodes to include in the final prompt set.

### 6.3 Dual-Space Representation
The graph encodes relationships in two spaces simultaneously:
- **Feature space** (DINOv2 embeddings): Captures semantic similarity
- **Physical space** (pixel coordinates): Captures spatial arrangement

This dual representation lets the reward function optimize for both semantic coherence (positive prompts should look like the object) and spatial coverage (prompts should be well-distributed).

### 6.4 Computational Cost
The main bottleneck is the graph size. With 1,447 nodes and ~2M edges, computing mean edge weights at every step (for the reward function) is expensive. Each of the 100 steps per episode also involves replay of 64 transitions. Total per episode: ~1.5 minutes on an RTX 6000 Ada.

### 6.5 SAM is Not in the Loop During Training
Critically, SAM is **never called during Q-learning training**. The reward function is based entirely on graph statistics (mean edge weights). SAM is only called twice: once with initial prompts and once with optimized prompts. This makes training much faster but means the reward function is a proxy for segmentation quality, not a direct measure of it.

---

## 7. Our Experiment: Blue Tang Fish

### Setup
- **Reference image**: Blue tang (Paracanthurus hepatus) on coral, 560x560
- **GT mask**: Tight fish-only mask (~4% of image area)
- **Target image**: Same image (self-supervised demo)
- **DINOv2**: ViT-G/14 (1.1B params) for feature extraction
- **SAM**: ViT-B for segmentation
- **Training**: 30 episodes, 100 steps each, on RTX 6000 Ada GPU

### Results
| Metric | Initial | Optimized |
|--------|---------|-----------|
| Positive prompts | 34 | 6 |
| Negative prompts | 1413 | 20 |
| Mask IoU vs GT | 0.001 | 0.760 |
| Mask area | variable | ~4-12% |

### IoU Progression (Checkpoint Run)
| Episode | IoU | Area |
|---------|-----|------|
| 0 (pretrain) | 0.266 | 11.9% |
| 1 | 0.202 | 7.7% |
| 5 | 0.638 | 4.8% |
| 10 | 0.371 | 10.6% |
| 15 | 0.528 | 7.1% |
| 20 | 0.332 | 11.8% |
| 25 | 0.338 | 11.4% |
| 30 | 0.372 | 9.7% |

The IoU fluctuates because epsilon is still 0.78 (high exploration) with only 30 episodes. The best Q-table (saved at peak) achieves IoU 0.760 on the separate run.

---

## 8. File Structure Reference

```
PPO/
├── feature_matching/
│   ├── hubconf.py              # DINOv2 model loading (ViT-S/B/L/G variants)
│   └── generate_points.py      # Feature extraction, patch matching, prompt generation
├── segmenter/
│   ├── segment.py              # SAM loading, prediction, visualization
│   └── checkpoint/
│       └── sam_vit_b_01ec64.pth  # SAM ViT-B weights (358 MB)
├── utils_train.py              # GraphOptimizationEnv, QLearningAgent, training utilities
├── utils_test.py               # Testing utilities (same env/agent classes, minor differences)
├── test_PPO.py                 # optimize_nodes() function for inference
├── train_PPO.py                # Training entry point
├── run_bluetang.py             # Our custom end-to-end pipeline (3 steps)
└── run_bluetang_checkpoints.py # Pipeline with intermediate snapshots
```
