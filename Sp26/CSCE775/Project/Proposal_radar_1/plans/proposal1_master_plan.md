# Detailed Work Plan: Proposal 1 (RL-Tuned Synthetic Marine Radar)

## 1) Goal and Decision Criterion
Build an environment-conditioned RL outer loop that tunes radar simulator parameters so a downstream maritime perception model achieves better real-data performance than fixed/random/non-RL tuning baselines.

Success decision:
- Primary: statistically significant gain on real-data task metric versus all non-RL baselines.
- Secondary: lower real-evaluation budget to reach a target score.

## 2) Reproducible Environment Stack
- OS: Ubuntu 22.04 (or equivalent Linux workstation).
- Python: 3.10.
- Core libs: PyTorch 2.x, NumPy, pandas, matplotlib, Stable-Baselines3.
- Training orchestration: `hydra` or YAML-config launcher.
- Experiment tracking: CSV + JSON artifact logging, fixed random seeds.

Environment profile to freeze in repo:
- `env_name`: `radar_sim2real_rl`
- `cuda`: required for inner-loop training, optional for policy-only ablations.
- `determinism`: fixed seeds (minimum 5), fixed split files.

## 3) Data Assets and Splits
- Real validation/test: PoLaRIS + LaRS-style maritime splits, with optional auxiliary stress subsets from RADIATE/CARRADA for robustness.
- Synthetic generation: parameterized radar simulator with environment tag (`lake`, `river`, `coast`).

Split protocol:
- Train: synthetic only (policy-controlled generator).
- Val: held-out real routes (used by outer loop reward).
- Test: unseen real routes and leave-one-environment-out split.

## 4) Simulator Parameterization and Constraints
Controlled parameters (example vector $\theta$):
- Speckle scale
- Attenuation coefficient
- Clutter floor
- Multipath gain
- Noise burst probability

Constraint policy:
- Hard bounds for physical plausibility.
- Out-of-range action clipping + penalty term in reward.
- Boundary-hit rate logged as realism diagnostic.

## 5) Model Stack
Inner-loop model candidates:
- Primary: MRISNet-like segmentation head.
- Secondary: radar detection baseline (RODNet-style).

Outer-loop controller:
- Algorithm: SAC (continuous action updates to $\theta$).
- State: current $\theta$, environment embedding, recent reward history, validation trend features.
- Action: bounded delta update to each simulator parameter.

## 6) Training and Evaluation Procedure
### 6.1 Inner/Outer Loop Schedule
- Outer step $t$: policy proposes $\Delta\theta_t$.
- Generate synthetic batch with $\theta_t$.
- Train/update inner model for fixed micro-epochs.
- Evaluate on real validation split and compute reward.
- Update SAC policy.

### 6.2 Reward Definition
\[
r_t = \Delta \mathrm{mIoU}_{real} - \lambda_1\lVert\theta_t-\theta_0\rVert_2 - \lambda_2\mathbb{1}(\theta_t\notin\Omega_{phys}).
\]

### 6.3 Baselines
1. Fixed simulator defaults.
2. Uniform random domain randomization.
3. Bayesian optimization tuner (same evaluation budget).
4. RL without environment conditioning.
5. RL with environment conditioning (proposed).

## 7) Metrics and Statistical Reporting
Primary metrics:
- Real-set mIoU or task-specific balanced accuracy.
- Sim-to-real gap reduction.

Secondary metrics:
- Calls-to-threshold (sample efficiency).
- Seed variance and 95% CI.
- Robustness under low-SNR/high-clutter slices.
- Boundary-hit realism diagnostics.

Statistical rules:
- Minimum 5 seeds per configuration.
- Paired significance test versus strongest non-RL baseline.

## 8) Compute Budget and Runtime Plan
- Outer-loop episodes: 100-300 (staged).
- Real validation calls cap: fixed per method for fair comparison.
- GPU budget: 1-2 GPUs for inner model updates; policy updates on same worker.

Runtime reduction plan:
- Phase A: low-dimensional $\theta$ subset.
- Phase B: full parameter vector.
- Phase C: stress-test and ablation only on top methods.

## 9) Week-by-Week Execution
1. Week 1: lock split protocol, metric definitions, and parameter bounds.
2. Week 2: fixed/random/BO baseline runs and logging sanity checks.
3. Week 3: SAC outer-loop prototype on reduced parameter subset.
4. Week 4: full action space + environment-conditioned variant.
5. Week 5: holdout environment experiments and robustness slices.
6. Week 6: ablations (conditioning off, realism penalty off, reduced state).
7. Week 7: error analysis, failure taxonomy, figure finalization.
8. Week 8: final write-up and reproducibility package.

## 10) Risks and Fallbacks
- Sparse/noisy reward: moving-average reward and repeated validation mini-batches.
- Policy instability: action normalization, entropy tuning, smaller update horizon.
- Inner-loop overfit to val routes: strict route-level test lockbox.
- Compute overrun: two-stage schedule and early stopping by confidence interval overlap.

## 11) Deliverables
- Updated IEEE draft with source-backed evidence figure.
- Reproducible config files and split manifests.
- Baseline vs proposed comparison tables with CIs.
- Final artifact bundle with scripts and exact run commands.
