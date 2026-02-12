# Detailed Work Plan: Proposal 3 (Battery-Aware Multi-Sensor Exploration)

## 1) Goal and Decision Criterion
Learn a single policy that jointly controls ASV motion and sensor duty-cycling to maximize information gain per Joule under dynamic marine conditions.

Success decision:
- Primary: significant improvement in coverage efficiency ($m^2$/J) over frontier and energy-unaware RL baselines.
- Secondary: improved mission completion/return-to-base rate under low battery starts.

## 2) Reproducible Environment Stack
- Simulator: VRX/Gazebo or equivalent marine simulator with current/wave disturbance.
- Python: 3.10, PyTorch 2.x, Stable-Baselines3, ROS2 interface wrapper.
- Logging: per-step energy ledger (propulsion + each sensor), map entropy trajectory, action traces.
- Determinism: fixed map seeds, current profile seeds, and policy seeds (>=5).

## 3) Scenario and Split Design
Scenario families:
- Lake: low current, open water.
- River: directional current and narrow channels.
- Coast: wave disturbance and dynamic obstacles.

Split strategy:
- Train on generated maps from each family.
- Test on held-out maps plus mixed-transition episodes (lake->river, river->coast).
- Low-battery suite: 30%, 40%, 50% initial SoC.

## 4) MDP/POMDP Specification
State $s_t$:
- Local occupancy/entropy map patch.
- Pose and velocity.
- Battery state and recent energy-use vector.
- Sensor status vector.
- Environment-type embedding.

Action $a_t$:
- Motion: $v_t$, $\omega_t$.
- Sensor duty controls: binary/ternary modes for radar/lidar/camera sampling rates.

Reward:
\[
r_t = \lambda_1\Delta\mathrm{InfoGain} - \lambda_2\mathrm{EnergyCost} - \lambda_3\mathrm{CollisionRisk} - \lambda_4\mathrm{NoReturnPenalty}.
\]

## 5) Policy and Baselines
Proposed policy:
- Actor-critic (SAC/PPO hybrid depending on final action discretization).
- Shared encoder for map + energy state, separate heads for motion and sensor actions.

Baselines:
1. Frontier exploration with sensors always on.
2. Rule-based coverage with fixed safety battery threshold.
3. Energy-unaware RL.
4. Energy-aware RL without environment conditioning.
5. Proposed conditioned joint-control policy.

## 6) Energy Model and Calibration
Energy ledger components:
- Propulsion model with drag/current coupling.
- Sensor power draw per mode (idle/active/high-rate).
- Compute overhead for perception stack.

Calibration steps:
- Unit tests for monotonic energy consumption versus thrust and sensor mode.
- Sanity checks against published marine energy-aware planning trends.

## 7) Evaluation Metrics
Primary:
- Coverage efficiency ($m^2$/J).
- Mission success rate (goal reached or safe return before depletion).

Secondary:
- Total entropy reduction.
- Collision count / safety violations.
- High-power sensor duty ratio.
- Time-to-critical-battery threshold.

Reporting:
- Mean + 95% CI over seeds.
- Paired tests against strongest non-proposed baseline.

## 8) Stress and Failure Testing
- Sudden current direction changes.
- Sensor dropout episodes.
- Increased obstacle density.
- Delayed localization updates.

Failure diagnostics:
- Energy overspend root cause (motion vs sensing).
- Action entropy collapse.
- Return-to-base policy timing errors.

## 9) Compute Budget
- Policy training: single high-memory GPU.
- Parallel simulation workers: 8-16 CPU threads.
- Fixed episode budgets per method for fair comparison.

Runtime optimization:
- Curriculum from simplified hydrodynamics to full disturbance model.
- Early stopping for dominated policies.

## 10) Week-by-Week Execution
1. Week 1: simulator setup, energy ledger instrumentation, split definitions.
2. Week 2: frontier/rule baselines + metric scripts.
3. Week 3: RL environment and reward shaping validation.
4. Week 4: energy-unaware RL training.
5. Week 5: energy-aware no-context RL training.
6. Week 6: full conditioned joint-control training.
7. Week 7: stress tests and ablation runs.
8. Week 8: statistical analysis, final figures, and write-up.

## 11) Risks and Mitigation
- Reward sparsity: dense shaping using entropy delta and return-to-base progress.
- Unsafe exploration: shielded action layer and hard safety constraints.
- Sim-to-real energy mismatch: domain-randomized energy coefficients during training.
- Training instability: staged curriculum and conservative action scaling.

## 12) Deliverables
- Source-backed evidence figure and expanded paper manifest.
- Reproducible configs and simulator scenario definitions.
- Baseline/ablation comparison tables with CIs.
- Final IEEE draft with explicit claim-to-evidence mapping.
