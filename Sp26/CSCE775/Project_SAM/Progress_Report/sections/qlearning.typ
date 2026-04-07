= Preliminary Investigation: The Q-Learning Approach <sec:qlearning>

Before arriving at the transformer-based policies described in the following sections,
we pursued a Deep Q-Network (DQN) approach that operated over a graph representation
of SAM prompt candidates. This effort consumed five days (February 28 -- March 3, 2026),
produced a concrete quantitative regression relative to a naive heuristic, and
ultimately informed a complete architectural pivot. We document it here both as a
cautionary account of proxy-reward failure and as motivation for the design decisions
made in V1--V3.

== System Architecture <sec:qlearning_arch>

The environment maintained a prompt graph $cal(G) = (cal(V), cal(E))$
whose nodes $v in cal(V)$ each represented a candidate prompt point carrying two
attributes: (i) a 1024-dimensional DINOv2 @oquab2024dinov2 feature vector sampled
at the corresponding image patch, and (ii) a binary polarity label (positive or negative).

The *state* presented to the network was an 8-dimensional summary vector $s_t$:

$ s_t = [
    (|cal(V)^+_t|)/(|cal(V)_t|),
    (|cal(V)^-_t|)/(|cal(V)_t|),
    (|cal(V)_t|)/(|cal(V)_0|),
    macron(d)^("feat",+)_t,
    macron(d)^("feat",-)_t,
    macron(d)^"phys"_t,
    macron(d)^"feat"_t,
    macron(d)^"comb"_t
  ] in RR^8, $ <eq:state>

where the components encode node counts, mean pairwise DINOv2 feature distances, mean physical distances, and combined metrics.

Five operation types were defined: `remove_pos`, `remove_neg`, `restore_pos`, `restore_neg`, and `add` (penalized at $-10$, never used). Actions were encoded as node identifiers $j \/ j_max$, a normalized index with no semantic content. The effective branching factor ranged from 60 to 120 valid actions per step.

SAM was never queried during training. The reward was a hand-tuned weighted sum of five DINOv2 feature-distance terms designed as a proxy for segmentation quality. SAM was queried only at episode end for diagnostic monitoring.

A `QValueMLP` network received the 8-dimensional state and output a scalar Q-value. Training used offline DQN with experience replay: 2,000 episodes of 100 steps each ($2 times 10^5$ transitions), epsilon-greedy exploration annealed from 1.0 to 0.05, and Adam with $eta = 10^(-3)$.

The initial NetworkX-based environment ran at 72 seconds per episode. A rewrite using dense PyTorch tensors (`FastGraphEnv`) achieved a $33 times$ speedup to 2.2 seconds per episode.

A heuristic baseline achieved 0.807 Dice. After 2,000 episodes of Q-learning, the trained agent achieved approximately 0.60 Dice---a regression of more than 20 points.

== Training Dynamics and Failure Cascade <sec:qlearning_failure>

The five-day development proceeded through apparent engineering progress before culminating in numerical instability and architectural post-mortem. @tab:dqn_timeline summarizes the timeline.

#figure(
  table(
    columns: 4,
    table.hline(),
    [*Day*], [*Date*], [*Event / Intervention*], [*Outcome*],
    table.hline(),
    [1], [Feb 28], [Initial DQN implementation with NetworkX environment], [72 s/episode; Dice $approx$ 0.55],
    [2], [Mar 1], [FastGraphEnv rewrite with dense PyTorch tensors], [$33 times$ speedup to 2.2 s/episode],
    [3], [Mar 2], [NaN loss divergence at episode 727], [Agent unrecoverable],
    [3], [Mar 2], [Fixes: reward clipping, LR reduction, Q-value clamping, distance sanitization], [NaN delayed but recurrent],
    [3], [Mar 2], [Full sanitization: nan_to_num on distances, min 2 active nodes], [NaN eliminated; Dice $approx$ 0.60],
    [4], [Mar 3], [50-page architectural post-mortem identifying 5 fundamental flaws], [Decision to abandon],
    [4], [Mar 3], [All Q-learning code deleted; V1 architecture started], [Clean slate],
    table.hline(),
  ),
  caption: [Timeline of the Q-learning investigation (Feb 28 -- Mar 3, 2026).],
) <tab:dqn_timeline>

== Post-Mortem Analysis: Five Fundamental Failures <sec:qlearn_postmortem>

Before the PolicyTransformer architecture described in Sections 3.1 and 3.2,
an earlier attempt framed prompt selection as a graph-pruning problem solved
with a tabular-style Deep Q-Network (DQN). The agent began with a complete
graph of $N = 25$ candidate nodes---one per spatial region of the image---and
learned to remove or restore nodes until the surviving subgraph defined a set
of SAM point prompts. Despite appearing tractable on paper, this formulation
contained five compounding design errors that made meaningful learning
impossible. We document them in detail because each one recurs as a distinct
failure class in the broader RL-for-segmentation literature, and understanding
them directly motivated the architectural pivot described in
@sec:pivot.

The entire graph state was summarized into an 8-dimensional vector before being
passed to the Q-network. This summary discarded _all_ spatial information
about where in the image each node resided. Two consequences followed
immediately.

First, _permutation ambiguity_: distinct spatial configurations of nodes
could produce identical 8D state vectors. A graph with strong foreground
coverage in the upper-left and a graph with identical coverage statistics in the
lower-right were indistinguishable to the agent. The Q-function therefore had
to learn a single action-value estimate for situations that genuinely required
different responses.

Second, _near-stationarity_: removing one node from a 25-node graph
changed the aggregate statistics by roughly 3% in L2 norm. Each action
produced almost no movement in state space, so the sequence of states visited
during an episode formed a tightly clustered cloud rather than a directed
trajectory. Credit assignment is only feasible when actions produce
distinguishable state transitions; here the transitions were effectively
invisible.

Together these two properties rendered temporal difference learning
ill-conditioned. The agent could not distinguish which node removals caused
which downstream reward changes, and the near-identical states meant the
same weight update was applied repeatedly to situations that differed only
in ways the representation had already erased.

The action space exposed two sources of irreducible confusion. The first was
the _initialization_: all episodes began with every node removed, meaning
the agent had to reconstruct a valid prompt configuration from an empty
starting state without observing any SAM output. This is equivalent to asking
a human annotator to click on a blank canvas and predict where the object will
appear. Starting from a solved or near-solved state and learning small
refinements would have been far more informative.

The second source was _node-ID encoding_. Nodes were identified by a
scalar $j \/ j_max$---a normalized index in the arbitrary order the nodes
happened to be stored. This index carried no semantic content; a node with
index 0.04 was not spatially, visually, or semantically similar to a node with
index 0.08. The Q-network was forced to discover spatial meaning from a
quantity that encoded none.

These two problems combined to produce an action space with 60--120 valid
choices per step. Epsilon-greedy exploration with a uniform distribution over
100 actions yields a less-than-1% probability of selecting any semantically
meaningful action, making empirical coverage of the reward landscape
practically impossible.

A further structural error was _reversibility without cost_. Each node
could be removed or restored, so the agent could oscillate between the same two
states indefinitely. Because the reward signal reflected final SAM quality
rather than incremental improvement, zero-cost oscillations were
indistinguishable from productive exploration. The environment was framing an
inherently combinatorial subset-selection problem as a sequential decision
process, but providing no mechanism to prevent the agent from circling the same
subset indefinitely.

This failure was the most consequential. The reward function measured
distances in DINOv2 feature space between the selected node features and the
reference foreground features. The underlying motivation was reasonable:
DINOv2 features correlate with semantic similarity, and semantically similar
regions are likely to belong to the same object class.

However, SAM does not operate on DINOv2 features. SAM's mask decoder receives
spatial point coordinates and produces a segmentation by attending to its own
internal image encoder's representation---a representation with no direct
coupling to DINOv2. The causal chain assumed by the reward was:

$ "high DINO similarity" arrow.r "good spatial coverage" arrow.r "high SAM Dice", $

but the middle link---spatial coverage from DINO similarity---does not hold in
general. DINOv2 features encode appearance and semantics; they do not
guarantee that a semantically similar patch lies in a useful spatial position
for SAM to leverage.

The empirical consequences were unambiguous. Episodes that received the
highest proxy rewards, indicating strong DINO feature alignment among surviving
nodes, consistently produced SAM Dice scores of 0.0. Far from correlation,
the relationship was _anti-correlated_: to maximize DINO feature
similarity, the agent learned to collapse the graph down to one or two
nodes---the most semantically coherent subset---which produced point prompts
that were clustered in a single image patch and gave SAM no coverage of the
target object's spatial extent.

This is a textbook instance of Goodhart's Law: when a measure becomes a
target, it ceases to be a good measure. Ng et al. @ng1999reward prove
formally that reward shaping functions must satisfy a potential-based
consistency condition to preserve the optimal policy. The DINO-distance proxy
violated this condition completely---it was not even a monotone transformation
of the true objective in the empirical distribution of states visited during
training. Correcting the proxy reward to the actual SAM Dice at every step
was not merely an improvement; it was a prerequisite for any signal-to-noise
ratio above zero.

DQN was designed for environments with small, fixed, discrete action spaces
(the original Atari benchmark has at most 18 actions). This environment
presented 60--120 valid actions per step with a variable count that changed as
nodes were added or removed. Standard DQN has no mechanism for handling
variable-cardinality action sets; the Q-head must be defined over a fixed
output dimension, which forced either padding (wasting capacity on invalid
actions) or re-parameterization (which reintroduced the ID-encoding problem).

A second mismatch was temporal. DQN is an _off-policy_ algorithm: it
trains on a replay buffer of past experiences collected under earlier policy
versions. In this environment, the graph state at time $t$ under policy
$pi_k$ is not the same distribution as the graph state at time $t$ under
policy $pi_(k+100)$. Replay buffer entries became stale, and the Q-network
was trained to predict values for state-action pairs that the current policy
would never visit, accelerating value overestimation in the high-dimensional
continuous input domain.

Critically, SAM was queried only at the _end_ of each episode---not at
every step. The intermediate reward signals during an episode were therefore
computed entirely from the DINO proxy, compounding Failure 3. The agent
received no closed-loop spatial feedback during the episode, making it
impossible to learn how individual node additions or removals changed SAM's
actual segmentation hypothesis.

The promotion gate used to advance from training to evaluation was too
permissive. It tested for non-trivial proxy reward improvement over a random
baseline---a condition the agent could satisfy by collapsing to one or two
high-similarity nodes (see Failure 3) without producing any usable
segmentation. As a consequence, checkpoints were promoted to validation
evaluation that had Dice scores indistinguishable from chance.

More fundamentally, training and validation measured entirely different
quantities. Training optimized the DINO-distance proxy; the validation gate
measured Dice against ground-truth masks. These two objectives pointed in
opposite directions in the empirical state distribution, so a policy that
improved on the training objective reliably degraded on the validation metric.
No amount of hyperparameter tuning could bridge a gap that was architectural
in origin.

== Lessons Learned and the Pivot Decision <sec:pivot>

The five failures described above are not independent. They form a
reinforcing cycle: the lossy state representation made credit assignment hard,
the misstructured action space made exploration unlikely to find good states,
the misaligned reward made the few good states unrecognizable to the agent, the
off-policy training algorithm amplified the distribution mismatch from all
three upstream errors, and the permissive evaluation gate hid the cumulative
damage until the policy was already far off course. Fixing any single failure
in isolation would not have produced a working system. Five distinct lessons
emerged, each of which drove a concrete architectural decision in the redesign.

A proxy reward that is not a monotone function of the true objective is worse
than no reward at all---it actively steers the policy away from useful
behavior. The redesigned agent uses actual SAM Dice scores, computed by
querying SAM on every step, as the sole reward signal. The DINO feature space
is retained as a representation tool but is never used as a reward. This
aligns directly with the theoretical requirement in @ng1999reward: the
reward function must preserve the ordering of policies under the true objective.

The 8D summary vector was the single most destructive design choice because
no learning algorithm can recover information that the state representation has
discarded. The redesigned system passes the full $37 times 37 times 1024$
DINOv2 feature tensor directly to the policy network, preserving spatial
structure at the patch level. The policy can now distinguish locations that
differ only in their spatial position, making credit assignment feasible.

Initializing episodes with an empty graph required the agent to solve a blind
reconstruction problem before any useful learning could occur. The redesigned
system starts from the current SAM prediction and places _additional_
corrective point prompts. The agent begins each episode with a non-zero
baseline quality and must learn to improve it, a far more tractable
signal-to-noise regime.

Node IDs carry no semantic content. The redesigned action space is a direct
spatial selection over the $37 times 37$ patch grid---the agent outputs
$(x, y)$ coordinates for the next click rather than an index into an
arbitrarily ordered list of nodes. Spatial coordinates have intrinsic
semantic structure: nearby coordinates refer to nearby image regions, and the
Q-function or policy can exploit spatial continuity directly. This collapses
the effective action space from 60--120 variable-cardinality choices to a
fixed 1,369-way spatial distribution, enabling standard architectures to
handle it without modification.

DQN's off-policy replay is harmful when the state distribution shifts rapidly
with the policy. The redesigned system uses Proximal Policy
Optimization @schulman2017ppo with SAM queried at every step. Each
policy gradient update is computed on rollouts collected under the current
policy, eliminating replay buffer staleness. The closed-loop feedback means
the agent observes SAM's actual mask response to every point it places,
giving it the temporal credit signal that was entirely absent in the DQN
formulation.

Taken together, these five lessons constitute a complete architectural
redesign rather than an incremental patch. The redesigned system retains the
high-level objective---learn to place point prompts for SAM using DINOv2
features and one-shot reference information---but replaces every major
subsystem: the state representation (8D summary $arrow.r$ full
$37 times 37 times 1024$ tensor), the action space (node-ID graph operations
$arrow.r$ direct $(x, y)$ point placement on the patch grid), the reward
signal (DINO feature-space proxy $arrow.r$ actual SAM Dice), the training
algorithm (offline DQN $arrow.r$ on-policy PPO), and the SAM query schedule
(episode-end only $arrow.r$ every step). This redesigned formulation is
what became the V1 PolicyTransformer described in @sec:v1,
and it is the architecture on which all subsequent results in this report are
built.
