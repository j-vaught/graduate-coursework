= The PPO Framework: Foundation and Prior Art <sec:ppo_framework>

== Overview and Motivation

The Plug-and-Play PPO framework @ppo2025cvpr is a CVPR 2025 paper that reframes SAM prompt optimization as a _heterogeneous graph optimization problem_ solved via Deep Reinforcement Learning. It is the direct conceptual predecessor to the Q-learning investigation documented in @sec:qlearning and constitutes the point of departure for every subsequent architecture developed in this work.

The key insight is that rather than learning to place clicks directly in pixel space, PPO constructs an explicit graph of candidate prompt locations and optimizes the graph's node membership so that the surviving nodes form a high-quality prompt set. This formulation shifts the optimization target from "which spatial coordinate should I click next" to "which elements of a pre-generated candidate pool should be retained"---a combinatorial subset-selection problem solved sequentially by a reinforcement learning agent. Feature extraction is delegated to DINOv2-ViT-G/14 @oquab2024dinov2, and the RL agent is a tabular Q-learner that operates on a dual-space heterogeneous graph whose edges encode both semantic similarity (in DINOv2 feature space) and geometric proximity (in pixel space).

The full system operates in three ordered stages.

DINOv2 feature matching against a labeled reference image generates a pool of approximately 5--10 positive candidate patches (regions whose features closely resemble the reference foreground) and 5--10 negative candidate patches (background regions with low similarity to the reference foreground). This first stage is deterministic and requires no learned parameters beyond DINOv2 itself.

In the second stage, the candidate pool is embedded in a heterogeneous graph, and a Q-learning agent iteratively adds or removes nodes to optimize a reward signal computed entirely from graph-internal metrics---feature distances and physical distances among the surviving nodes. SAM is not invoked at any point during this stage.

In the third stage, the pixel coordinates of the surviving positive and negative nodes are extracted and passed to SAM as point prompts. A segmentation mask is returned, and performance is evaluated against the ground-truth mask using Dice Similarity Coefficient (DSC) and 95th-percentile Hausdorff Distance ($"HD"_(95)$).

This architecture is elegant in its modularity: DINOv2 handles all semantic feature work, the Q-learning agent handles combinatorial prompt selection, and SAM handles the final segmentation. As @sec:ppo_relationship argues, the same modularity is the source of several latent design fragilities that our subsequent work exposed.

== Dual-Space Heterogeneous Graph Construction

The graph construction procedure is designed to produce a compact representation of the semantic and spatial relationships among candidate prompt points, using DINOv2 patch features as the semantic embedding space.

Both the reference and query images are resized to $560 times 560$ pixels prior to processing. The image is logically divided into a $40 times 40$ grid of non-overlapping $14 times 14$-pixel patches, yielding $N = 1600$ candidate patch locations indexed $0, 1, dots, 1599$. This tiling is chosen explicitly to match the patch size used by DINOv2-ViT-G/14, so that each grid cell corresponds to exactly one DINOv2 token with a 1536-dimensional feature vector.

The reference image's ground-truth mask is scanned to identify _reference foreground patches_---those whose pixel area overlaps substantially with the mask. DINOv2-ViT-G/14 is then applied to the query image, producing one 1536-D token per patch. For each query patch, L2 distance to the mean reference foreground feature is computed, and the $k^+$ nearest patches become the initial positive prompt candidates; the $k^-$ most distant patches (subject to a minimum pixel separation from the positives) become the initial negative prompt candidates. In practice $k^+ approx k^- approx 5$--$10$.

A NetworkX `MultiGraph` is constructed whose nodes are patch indices (integers in $\{0, dots, 1599\}$) annotated with a `category` attribute taking values `'pos'` or `'neg'`. Five edge types form the dual-space heterogeneous structure, each carrying a scalar weight normalized to $[0,1]$:

#figure(
  table(
    columns: (8em, 1fr),
    table.hline(),
    [*Edge Type*], [*Description*],
    table.hline(),
    [`feature_pos`],   [DINOv2 L2 distance within positive nodes.],
    [`physical_pos`],  [Pixel distance within positive nodes.],
    [`physical_neg`],  [Pixel distance within negative nodes.],
    [`feature_cross`], [DINOv2 L2 between positive and negative nodes.],
    [`physical_cross`],[Pixel distance between positive and negative nodes.],
    table.hline(),
  ),
  caption: [The five edge types of the dual-space heterogeneous graph. Each edge carries a scalar weight normalized to $[0,1]$.],
) <tab:edge_types>

The five edge types encode complementary objectives that the Q-learning reward signal balances. The `feature_pos` edges measure how semantically similar the surviving positive prompts are to each other in DINOv2's 1,536-dimensional embedding space; the reward encourages low values here, pulling the positive set toward a tight semantic cluster that consistently represents the target class. The `physical_pos` edges measure how far apart those same positive prompts are in pixel coordinates; the reward encourages high values, pushing the prompts to spread across the spatial extent of the target object rather than clustering in one region. These two objectives are in direct tension --- semantic cohesion favors nearby, similar patches, while spatial spread favors distant ones --- and the agent must learn a trade-off between them. The `physical_neg` edges serve a symmetric role for the negative (background) prompt set, encouraging spatial diversity among background anchors. The `feature_cross` edges measure the DINOv2 distance between positive and negative nodes; high values here indicate that the foreground and background prompt sets are well-separated in feature space, which the reward encourages as a proxy for class discriminability. Finally, `physical_cross` edges capture the spatial relationship between the two sets, encoding how the foreground--background boundary is distributed geometrically. Together, these five statistics define what the paper terms the _dual-space_ graph structure, where "dual" refers to the simultaneous representation of both feature-space and physical-space relationships within a single heterogeneous graph.

== Q-Learning Graph Optimization

The RL agent's task is to improve the prompt configuration by modifying the node membership of the heterogeneous graph.

The state $s_t$ is the full graph $cal(G)_t$ at step $t$, whose observable content reduces in practice to the set of mean pairwise edge weights across the five edge types computed over the current node membership. In the tabular Q-learning implementation, the state must be discretized or hashed to an integer key for lookup in the Q-table dictionary.

Five operation types are defined, each parameterized by a target node. The `remove_pos` and `remove_neg` operations delete a currently active positive or negative prompt node, respectively. The `restore_pos` and `restore_neg` operations reinstate a previously removed positive or negative node. Finally, `add` inserts a new node not in the initial candidate pool; this operation is penalized at $-10$ reward and is rarely if ever selected by a trained agent.

Feasibility constraints enforce a minimum of 5 active nodes per category and a maximum of 20. The effective branching factor at each step is therefore a function of the current graph size and ranges from tens to over a hundred valid actions.

The reward is a hand-designed linear combination of four graph-metric objectives plus one penalty term. Let $overline(d)^("feat",+)$ denote the mean within-positive feature distance, $overline(d)^("feat",times)$ the mean cross-group feature distance, $overline(d)^("phys",+)$ the mean within-positive physical distance, and $overline(d)^("phys",times)$ the mean cross-group physical distance. The step reward is:

$ r_t = +5 dot Delta(-overline(d)^("feat",+))
        +5 dot Delta(overline(d)^("feat",times))
        +1 dot Delta(overline(d)^("phys",+))
        +1 dot Delta(-overline(d)^("phys",times))
        -10 dot bb(1)["add"], $ <eq:ppo_reward>

where $Delta(dot)$ denotes the per-step change in the corresponding quantity. In words: the agent is rewarded for (i) reducing within-positive feature distance (semantic cohesion), (ii) increasing cross-group feature distance (class separability), (iii) increasing within-positive physical spread (geometric coverage), and (iv) decreasing cross-group physical distance (spatial compaction of the foreground--background interface); it is penalized for invoking the `add` operation.

SAM is _never_ queried during training. The entire reward signal is computed from graph-internal DINOv2 feature distances and Euclidean pixel distances. SAM is invoked only after the Q-learning optimization terminates, at inference time, to produce the final segmentation using the optimized prompt points. This architectural choice---placing SAM entirely outside the training loop---has significant consequences that @sec:ppo_relationship analyzes in detail.

The agent uses standard tabular Q-learning with $epsilon$-greedy exploration and experience replay, with the hyperparameters summarized in @tab:qlearn_hparams.

#figure(
  table(
    columns: (auto, auto, 1fr),
    table.hline(),
    [*Hyperparameter*], [*Value*], [*Description*],
    table.hline(),
    [Learning rate $alpha$],       [$0.1$],                           [Step size for Q-value updates.],
    [Discount factor $gamma$],     [$0.9$],                           [Temporal discounting of future rewards.],
    [Exploration $epsilon$],       [$1.0 arrow.r 0.1$, decay $0.995$],[$epsilon$-greedy schedule annealed per episode.],
    [Replay buffer],               [Capacity $10000$, batch $64$],    [Experience replay for off-policy updates.],
    [Training budget],             [$100000$ episodes, $100$ steps],  [Total training interactions.],
    [Q-table],                     [Python dictionary],               [Maps (state, action) pairs to scalar Q-values.],
    table.hline(),
  ),
  caption: [Tabular Q-learning hyperparameters for the PPO framework.],
) <tab:qlearn_hparams>

The tabular formulation implies that any two states that hash to the same key receive identical Q-value estimates regardless of the actual graph configurations they encode. The fidelity of the Q-table therefore depends critically on how much information the state representation retains---a point revisited in @sec:ppo_relationship.

== Full Inference Pipeline

At inference time the complete pipeline proceeds in seven stages. The reference image and ground-truth mask are first loaded and resized to $560 times 560$ pixels, as is the query image. DINOv2-ViT-G/14 is then applied to both images: reference foreground patches are identified from the ground-truth mask, and initial positive and negative candidate patches are selected via L2 feature matching. These candidates are used to construct the dual-space heterogeneous graph described in Section 3.2. The pre-trained Q-table is then loaded and the fully greedy ($epsilon = 0$) Q-learning loop is executed for $100$ steps, modifying node membership at each step. The pixel coordinates of surviving positive and negative node patch centers are extracted from the final graph $cal(G)_100$. These coordinate arrays are passed to SAM as point prompts to obtain the predicted segmentation mask. Finally, the mask is evaluated against the ground-truth using DSC and $"HD"_(95)$.

The pipeline is deterministic at inference (greedy Q-table lookups, no stochastic sampling), which makes results fully reproducible given a fixed Q-table and a fixed image pair. The DINOv2 forward pass is the dominant computational cost; the Q-learning loop at inference (100 table lookups) is negligible.

== Relationship to Our Work <sec:ppo_relationship>

PPO @ppo2025cvpr is not merely a related system---it is the direct architectural blueprint from which our Q-learning investigation was derived, and the latent design fragilities it contains are the same ones we independently re-encountered and formally characterized. This section draws explicit correspondences.

Our Q-learning system (@sec:qlearning) adopted three core elements from PPO without modification: (i) the dual-space heterogeneous graph structure with the same five edge-type taxonomy; (ii) the same five-operation action space (`remove_pos`, `remove_neg`, `restore_pos`, `restore_neg`, `add`); and (iii) DINOv2 feature distances as the basis of the reward signal. Our implementation differed in network architecture (MLP Q-value head rather than tabular), state encoding (8-dimensional summary vector rather than full graph), and training scale, but the fundamental optimization geometry was identical.

PPO's tabular Q-learning requires the continuous, high-dimensional graph state to be discretized or hashed into a dictionary key. Any hashing scheme that loses information about which specific nodes are active---their spatial positions, feature vectors, or polarity labels---produces the same _permutation ambiguity_ and _near-stationarity_ we documented in @sec:qlearn_postmortem: distinct spatial configurations of nodes collapse to the same table entry, and single-node removals shift mean edge statistics by only a few percent, making consecutive states nearly identical. Our 8-dimensional summary vector made this compression explicit; PPO's tabular key performs an implicit version of the same lossy compression. In both cases the consequence is the same: temporal difference learning cannot assign credit to individual node operations because those operations leave almost no trace in the representation.

@eq:ppo_reward makes explicit that PPO's reward optimizes DINOv2 feature distances, not SAM Dice. The assumed causal chain is:

$ "high DINO feature cohesion / separation" => "useful spatial prompt coverage" => "high SAM Dice". $

The middle link is empirically fragile. DINOv2 encodes appearance and semantic class; it does not encode whether a patch is at a _spatially informative_ location for SAM's mask decoder. A cluster of semantically similar patches in a single corner of the image maximizes feature cohesion while providing SAM almost no useful spatial signal. We documented precisely this collapse in @sec:qlearn_postmortem: episodes with the highest proxy reward consistently produced SAM Dice near zero. This outcome is not a failure of our implementation---it is the predictable consequence of optimizing a proxy that is not a monotone function of the true objective, as formalized by @ng1999reward. PPO's original evaluation may not have surfaced this failure if it was tested on image distributions where the DINOv2-to-spatial mapping happens to be well-calibrated; our one-shot segmentation setting exposed it directly.

PPO uses a tabular Q-learner with an experience replay buffer (capacity $10000$, batch size $64$). Tabular Q-learning with replay is off-policy by construction: the Q-table update at step $t$ draws from transitions collected under all prior policy versions stored in the buffer. As the policy improves and the graph configuration distribution shifts, older buffer entries become stale---they record state transitions under a policy that the current agent has already moved beyond. This distribution mismatch accelerates value overestimation and corrupts the temporal difference targets, the same issue we documented for our DQN variant. The problem is more severe in graph-structured environments than in fixed-state environments because the distribution of reachable graphs changes substantially as the Q-table learns to preferentially remove or restore particular node types.

PPO was designed for a _prompt refinement_ setting: starting from a pre-generated candidate pool, optimize the subset selection. The initial candidate pool is produced by a strong, task-aligned heuristic (DINOv2 feature matching), so the Q-learning agent begins from a state that is already semantically reasonable and needs only modest local adjustments. Our application attempted to use the same framework for _one-shot segmentation with interactive click placement_---a harder problem in which the agent must produce prompts for novel object classes with no prior spatial initialization. This amplification of task difficulty exposed the latent fragilities that PPO's original evaluation context may have partially obscured.

Our work makes four advances beyond @ppo2025cvpr. First, we identified and formally characterized the five failure modes documented in @sec:qlearn_postmortem, three of which---state compression, reward misalignment, and off-policy staleness---are structurally inherent to PPO's design rather than artifacts of our specific implementation choices. Second, we demonstrated in V1 (@sec:v1) that replacing the DINOv2 feature-distance proxy reward with direct SAM Dice scores---computed by querying SAM at every training step---resolves the reward misalignment: the true objective is substituted for the proxy, and the causal chain no longer has a broken link. Third, we demonstrated in V1 and V2 (@sec:v1, @sec:v2) that replacing the compressed graph summary with direct spatial feature representations---passing the $37 times 37 times 1024$ DINOv2 feature map to the policy network directly---resolves the state-information loss, allowing the policy network to retain full spatial structure and to distinguish prompt configurations that differ only in location. Fourth, we demonstrated in V3 (@sec:v3) that replacing the entire graph-optimization paradigm with VLM-based visual reasoning produces superior segmentation quality (0.776 mean Dice, 1.3 clicks) while requiring no task-specific training, establishing a strong upper bound for the one-shot segmentation setting and suggesting that the semantic understanding required for robust prompt placement is better acquired from web-scale vision-language pretraining than from reinforcement learning on a small task-specific dataset.

Taken together, these contributions form a systematic progression from the PPO baseline through failure analysis, architectural correction, and ultimately paradigm replacement. The PPO framework remains a valuable conceptual foundation: its dual-space graph structure cleanly separates semantic and spatial reasoning, and its action space design influenced every subsequent architecture in this work. The analysis here shows, however, that those contributions can be separated from the specific algorithmic commitments (tabular Q-learning, DINOv2 proxy reward, replay-based off-policy training) that ultimately limit the approach.
